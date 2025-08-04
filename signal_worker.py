
import os
import time
import requests
import pandas as pd
import numpy as np
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

MONITOR = {
    "PEPEUSDT": {"buy_below": 0.00001160, "sell_above": 0.00001200},
    "TRXUSDT":  {"buy_below": 0.1200,     "sell_above": 0.1250},
    "ENAUSDT":  {"buy_below": 0.530,      "sell_above": 0.570},
    "MEMEUSDT": {"buy_below": 0.0180,     "sell_above": 0.0200},
    "SUIUSDT":  {"buy_below": 0.610,      "sell_above": 0.650}
}

def fetch_klines(symbol, interval="15m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
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

def monitor():
    last_signal = {}
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

if __name__ == "__main__":
    print("✅ signal_worker (с RSI и EMA) запущен.")
    monitor()
