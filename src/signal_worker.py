import os
import time
import requests
import pandas as pd
import numpy as np
from telegram import Bot
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

BINANCE_API = "https://api.binance.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# Монеты и уровни
MONITOR = {
    "PEPEUSDT": {"buy_below": 0.00001060, "sell_above": 0.00001090},
    "TRXUSDT": {"buy_below": 0.1180, "sell_above": 0.1220},
    "ENAUSDT": {"buy_below": 0.525, "sell_above": 0.540},
    "MEMEUSDT": {"buy_below": 0.0175, "sell_above": 0.0192},
    "SUIUSDT": {"buy_below": 0.595, "sell_above": 0.615}
}

def fetch_price(symbol: str) -> float:
    url = f"{BINANCE_API}/api/v3/ticker/price"
    try:
        response = requests.get(url, headers=HEADERS, params={"symbol": symbol}, timeout=10)
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception as e:
        print(f"[ERROR] Ошибка при получении цены {symbol}: {e}")
        return None

def fetch_klines(symbol, interval="15m", limit=100):
    url = f"{BINANCE_API}/api/v3/klines"
    try:
        response = requests.get(url, headers=HEADERS, params={"symbol": symbol, "interval": interval, "limit": limit}, timeout=10)
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
    if price <= levels["buy_below"] and rsi < 30 and price > ema and last_signal.get(symbol) != "buy":
        last_signal[symbol] = "buy"
        return f"🟢 BUY сигнал по {symbol}\nЦена: {price:.8f}\nRSI: {rsi:.2f}\nEMA: {ema:.8f}"
    elif price >= levels["sell_above"] and rsi > 70 and price < ema and last_signal.get(symbol) != "sell":
        last_signal[symbol] = "sell"
        return f"🔴 SELL сигнал по {symbol}\nЦена: {price:.8f}\nRSI: {rsi:.2f}\nEMA: {ema:.8f}"
    return None

if __name__ == "__main__":
    print("[START] signal_worker запущен")
    sent = set()
    last_signal = {}

    while True:
        for symbol, levels in MONITOR.items():
            price = fetch_price(symbol)
            if price is None:
                continue

            df = fetch_klines(symbol)
            if df is None or df.empty:
                continue

            close_prices = df["close"]
            rsi = calculate_rsi(close_prices).iloc[-1]
            ema = calculate_ema(close_prices).iloc[-1]

            message = get_signal(symbol, price, rsi, ema, levels, last_signal)
            if message and f"{symbol}_{last_signal[symbol]}" not in sent:
                try:
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    sent.add(f"{symbol}_{last_signal[symbol]}")
                    print(f"[✔] {symbol} → {message.replace(chr(10), ' | ')}")
                except Exception as e:
                    print(f"[!] Ошибка отправки в Telegram: {e}")

        time.sleep(30)
