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
    "PEPEUSDT": {"buy_below": 0.00001080, "sell_above": 0.00001130},
    "TRXUSDT": {"buy_below": 0.1180, "sell_above": 0.1230},
    "ENAUSDT": {"buy_below": 0.528, "sell_above": 0.550},
    "MEMEUSDT": {"buy_below": 0.0178, "sell_above": 0.0195},
    "SUIUSDT": {"buy_below": 0.597, "sell_above": 0.622}
}

def fetch_price(symbol: str) -> float:
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception as e:
        print(f"[ERROR] Fetch price {symbol}: {e}")
        return None

def fetch_klines(symbol, interval="15m", limit=100):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        data = requests.get(url, timeout=10).json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = df["close"].astype(float)
        return df
    except Exception as e:
        print(f"[ERROR] Fetch klines {symbol}: {e}")
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

def send_msg(symbol, price, signal_type):
    try:
        emoji = "🟢" if signal_type == "buy" else "🔴"
        text = f"{emoji} {signal_type.upper()} сигнал по {symbol}\nЦена: {price}"
        bot.send_message(chat_id=CHAT_ID, text=text)
        print(f"[✔] {symbol} → {signal_type.upper()} → {price}")
    except Exception as e:
        print(f"[ERROR] Send to Telegram: {e}")

if __name__ == "__main__":
    print("[START] signal_worker запущен")
    sent = set()
    while True:
        for symbol, level in MONITOR.items():
            price = fetch_price(symbol)
            if price is None:
                continue

            print(f"[CHECK] {symbol} = {price}")
            key_buy = f"{symbol}_buy"
            key_sell = f"{symbol}_sell"

            if price < level["buy_below"] and key_buy not in sent:
                send_msg(symbol, price, "buy")
                sent.add(key_buy)
                sent.discard(key_sell)

            elif price > level["sell_above"] and key_sell not in sent:
                send_msg(symbol, price, "sell")
                sent.add(key_sell)
                sent.discard(key_buy)

            if price >= level["buy_below"] and key_buy in sent:
                sent.remove(key_buy)
            if price <= level["sell_above"] and key_sell in sent:
                sent.remove(key_sell)

        time.sleep(30)
