import time
import requests
import os
from telegram import Bot

# Получение токена и chat_id из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

# Монеты для отслеживания
SYMBOLS = ["TRXUSDT", "SUIUSDT", "PEPEUSDT", "ENAUSDT"]

# Публичный URL Binance (без API-ключа, не даёт 451 ошибку)
BASE_URL = "https://api.binance.com/api/v3/ticker/price?symbol="

def get_price(symbol):
    try:
        response = requests.get(BASE_URL + symbol, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"[ERROR] Не удалось получить цену {symbol}: {e}")
        return None

def send_signal(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"[ERROR] Ошибка отправки в Telegram: {e}")

if __name__ == "__main__":
    print("✅ Signal Worker запущен")
    send_signal("🚀 Signal Worker запущен и отслеживает цены.")

    while True:
        for symbol in SYMBOLS:
            price = get_price(symbol)
            if price:
                print(f"{symbol}: {price}")
                # Пример условия — ты можешь заменить на свой анализ
                if symbol == "PEPEUSDT" and price > 0.00001190:
                    send_signal(f"📈 {symbol} пробил уровень! Цена: {price}")
        time.sleep(15)  # Пауза, чтобы не спамить API
