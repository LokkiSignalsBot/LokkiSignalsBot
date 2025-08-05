import requests
import time
import os
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

SYMBOLS = ["TRXUSDT", "SUIUSDT", "PEPEUSDT", "ENAUSDT", "MEMEUSDT"]

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception as e:
        print(f"Ошибка при получении цены {symbol}: {e}")
        return None

def main():
    while True:
        for symbol in SYMBOLS:
            price = get_price(symbol)
            if price:
                print(f"{symbol}: {price}")
                # Пример простого условия для сигнала
                if symbol == "PEPEUSDT" and price < 0.00001150:
                    bot.send_message(chat_id=CHAT_ID, text=f"📉 {symbol} упал до {price}, возможен вход в LONG")
                elif symbol == "PEPEUSDT" and price > 0.00001190:
                    bot.send_message(chat_id=CHAT_ID, text=f"📈 {symbol} вырос до {price}, возможен вход в SHORT")
        time.sleep(30)

if __name__ == "__main__":
    main()
