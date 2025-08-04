import os
import time
import requests
import pandas as pd
import numpy as np
from telegram import Bot
from dotenv import load_dotenv

print("[START] signal_worker запускается...")

try:
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("❌ Переменные окружения BOT_TOKEN и CHAT_ID не заданы!")

    bot = Bot(token=BOT_TOKEN)

    HEADERS = {"User-Agent": "Mozilla/5.0"}

    MONITOR = {
        "PEPEUSDT": {"buy_below": 0.00001060, "sell_above": 0.00001090},
        "TRXUSDT": {"buy_below": 0.1180, "sell_above": 0.1220},
        "ENAUSDT": {"buy_below": 0.525, "sell_above": 0.540},
        "MEMEUSDT": {"buy_below": 0.0175, "sell_above": 0.0192},
        "SUIUSDT": {"buy_below": 0.595, "sell_above": 0.615}
    }

    def fetch_price(symbol: str) -> float:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()
            return float(data["price"])
        except Exception as e:
            print(f"[ERROR] Не удалось получить цену {symbol}: {e}")
            return None

    print("[INFO] Бот успешно запущен и готов к проверке цен.")

    sent = set()
    while True:
        try:
            for sym, lvl in MONITOR.items():
                price = fetch_price(sym)
                if price is None:
                    continue

                print(f"[CHECK] {sym} = {price}")

                key_buy = f"{sym}_buy"
                key_sell = f"{sym}_sell"

                if price < lvl["buy_below"] and key_buy not in sent:
                    bot.send_message(chat_id=CHAT_ID, text=f"🟢 BUY сигнал по {sym} — цена: {price}")
                    sent.add(key_buy)
                    sent.discard(key_sell)

                elif price > lvl["sell_above"] and key_sell not in sent:
                    bot.send_message(chat_id=CHAT_ID, text=f"🔴 SELL сигнал по {sym} — цена: {price}")
                    sent.add(key_sell)
                    sent.discard(key_buy)

                if price >= lvl["buy_below"] and key_buy in sent:
                    sent.remove(key_buy)
                if price <= lvl["sell_above"] and key_sell in sent:
                    sent.remove(key_sell)

            time.sleep(30)

        except Exception as loop_error:
            print(f"[ERROR] Ошибка в основном цикле: {loop_error}")
            time.sleep(10)

except Exception as main_error:
    print(f"[FATAL] Ошибка при старте скрипта: {main_error}")
