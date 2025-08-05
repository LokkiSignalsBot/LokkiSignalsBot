import os
import time
import hmac
import hashlib
import requests
import pandas as pd
import numpy as np
from urllib.parse import urlencode
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_API_BASE = os.getenv("BINANCE_API_BASE", "https://api.binance.com")

bot = Bot(token=BOT_TOKEN)

HEADERS = {
    "X-MBX-APIKEY": BINANCE_API_KEY,
    "User-Agent": "Mozilla/5.0"
}

MONITOR = {
    "PEPEUSDT": {"buy_below": 0.00001060, "sell_above": 0.00001090},
    "TRXUSDT": {"buy_below": 0.1180, "sell_above": 0.1220},
    "ENAUSDT": {"buy_below": 0.525, "sell_above": 0.540},
    "MEMEUSDT": {"buy_below": 0.0175, "sell_above": 0.0192},
    "SUIUSDT": {"buy_below": 0.595, "sell_above": 0.615}
}

def sign_request(params):
    """Подписывает запрос к Binance API."""
    query_string = urlencode(params)
    signature = hmac.new(
        BINANCE_API_SECRET.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    params["signature"] = signature
    return params

def fetch_price(symbol: str) -> float:
    url = f"{BINANCE_API_BASE}/api/v3/ticker/price"
    params = {"symbol": symbol}
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"[ERROR] Ошибка при получении цены {symbol}: {e}")
        return None

def fetch_klines(symbol, interval="15m", limit=100):
    url = f"{BINANCE_API_BASE}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = df["close"].astype(float)
        return df
    except Exception as e:
        print(f"[!] Ошибка при получении свечей {symbol}: {e}")
        return None

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_ema(series, period=21):
    return series.ewm(span=period, adjust=False).mean()

def get_signal(symbol, price, rsi, ema, levels, last_signal):
    message = None
    if price <= levels["buy_below"] and rsi < 30 and price > ema and last_signal.get(symbol) != "buy":
        message = f"🟢 BUY сигнал по {symbol}\nЦена: {price:.8f}\nRSI: {rsi:.2f} < 30\nEMA: {ema:.8f}"
        last_signal[symbol] = "buy"
    elif price >= levels["sell_above"] and rsi > 70 and price < ema and last_signal.get(symbol) != "sell":
        message = f"🔴 SELL сигнал по {symbol}\nЦена: {price:.8f}\nRSI: {rsi:.2f} > 70\nEMA: {ema:.8f}"
        last_signal[symbol] = "sell"
    return message

if __name__ == "__main__":
    print("[START] signal_worker запущен")
    last_signal = {}
    sent = set()
    while True:
        for symbol, levels in MONITOR.items():
            df = fetch_klines(symbol)
            if df is None or df.empty:
                continue

            close_prices = df["close"]
            rsi_series = calculate_rsi(close_prices)
            ema_series = calculate_ema(close_prices)
            current_rsi = rsi_series.iloc[-1]
            current_ema = ema_series.iloc[-1]
            current_price = close_prices.iloc[-1]

            message = get_signal(symbol, current_price, current_rsi, current_ema, levels, last_signal)
            if message:
                try:
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    print(f"[✔] {symbol} → {message.replace(chr(10), ' | ')}")
                except Exception as e:
                    print(f"[!] Ошибка отправки в Telegram: {e}")

        time.sleep(60)
