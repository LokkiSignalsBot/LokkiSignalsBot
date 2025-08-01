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
        "1000PEPEUSDT": {"buy_below": 0.00001150, "sell_above": 0.00001190},
        "TRXUSDT": {"buy_below": 0.0985, "sell_above": 0.1030},
        "ENAUSDT": {"buy_below": 0.475, "sell_above": 0.520},
        "MEMEUSDT": {"buy_below": 0.0155, "sell_above": 0.0170}
    }

    for symbol, levels in targets.items():
        try:
            price = get_price(symbol)
            if price <= levels["buy_below"]:
                send_signal(f"🔵 LONG сигнал по {symbol} — цена: {price}")
            elif price >= levels["sell_above"]:
                send_signal(f"🔴 SHORT сигнал по {symbol} — цена: {price}")
        except Exception as e:
            print(f"Ошибка анализа {symbol}: {e}")

if __name__ == "__main__":
    while True:
        analyze()
        time.sleep(60)
