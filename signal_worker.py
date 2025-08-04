import os
import asyncio
import time
import requests
from telegram import Bot

# Получение токена и chat_id из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=BOT_TOKEN)

# Монеты и их пороги для сигнала
SYMBOLS = {
    "PEPEUSDT": 0.00001150,
    "ENAUSDT": 0.540,
    "TRXUSDT": 0.1220,
    "MEMEUSDT": 0.0180
}

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"[ERROR] Ошибка получения цены {symbol}: {e}")
        return None

def analyze_and_send():
    for symbol, threshold in SYMBOLS.items():
        price = get_price(symbol)
        if price is None:
            continue

        print(f"[INFO] {symbol}: {price:.8f} (threshold {threshold})")

        if price <= threshold:
            message = f"📉 Сигнал на покупку {symbol}\nЦена: {price:.8f} USDT\nПорог: {threshold}"
            try:
                bot.send_message(chat_id=CHAT_ID, text=message)
                print(f"[SENT] {symbol} сигнал отправлен")
            except Exception as e:
                print(f"[ERROR] Telegram: {e}")

async def main():
    try:
        bot.send_message(chat_id=CHAT_ID, text="🤖 Бот сигналов запущен и следит за рынком.")
    except Exception as e:
        print(f"[ERROR] Стартовое сообщение не отправлено: {e}")

    while True:
        analyze_and_send()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
