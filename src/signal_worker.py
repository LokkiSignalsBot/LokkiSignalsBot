import os
import time
import requests
from telegram import Bot

# Переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

# Монеты для отслеживания
SYMBOLS = {
    "PEPEUSDT": 0.00001150,
    "ENAUSDT": 0.540,
    "TRXUSDT": 0.1220,
    "SUIUSDT": 1.050
}

def get_price(symbol):
    """Получить цену монеты через публичный API Binance"""
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return float(r.json()["price"])
    except Exception as e:
        print(f"Ошибка при получении цены {symbol}: {e}")
        return None

def send_signal(message):
    """Отправить сигнал в Telegram"""
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"Сигнал отправлен: {message}")
    except Exception as e:
        print(f"Ошибка при отправке в Telegram: {e}")

if __name__ == "__main__":
    while True:
        for symbol, level in SYMBOLS.items():
            price = get_price(symbol)
            if price:
                print(f"{symbol}: {price}")
                if price <= level:
                    send_signal(f"🔔 {symbol} достиг уровня {price} (порог {level})")
        time.sleep(60)  # проверка каждую минуту
