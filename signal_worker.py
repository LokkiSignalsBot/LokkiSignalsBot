import os
import time
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=BOT_TOKEN)

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    res = requests.get(url)
    return float(res.json()["price"])

def send_signal(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

def analyze():
    targets = {
        "1000PEPEUSDT": {"buy_below": 0.000011400, "sell_above": 0.000011900},
        "TRXUSDT": {"buy_below": 0.3200, "sell_above": 0.3300},
        "ENAUSDT": {"buy_below": 0.4750, "sell_above": 0.5000},
        "MEMEUSDT": {"buy_below": 0.0170, "sell_above": 0.0195},
    }

    for symbol, levels in targets.items():
        try:
            price = get_price(symbol)
            if price <= levels["buy_below"]:
                send_signal(f"🔽 Возможен вход в LONG по {symbol} — цена: {price}")
            elif price >= levels["sell_above"]:
                send_signal(f"🔼 Возможен вход в SHORT по {symbol} — цена: {price}")
        except Exception as e:
            print(f"Ошибка анализа {symbol}: {e}")

if __name__ == "__main__":
    while True:
        analyze()
        time.sleep(60)  # каждый 1 минуту
