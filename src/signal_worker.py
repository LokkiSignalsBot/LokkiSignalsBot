import os
import time
import requests
from telegram import Bot

# Загружаем токены из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")

# Заголовки для авторизации на Binance API
HEADERS = {
    "X-MBX-APIKEY": BINANCE_API_KEY
}

# Монеты и их уровни для сигналов
SYMBOLS = {
    "PEPEUSDT": 0.00001150,
    "ENAUSDT": 0.540,
    "TRXUSDT": 0.1220,
    "SUIUSDT": 1.200
}

bot = Bot(token=BOT_TOKEN)

def get_price(symbol):
    """Получаем цену с Binance API"""
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"[ERROR] Не удалось получить цену {symbol}: {e}")
        return None

def send_signal(message):
    """Отправляем сигнал в Telegram"""
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"[INFO] Сигнал отправлен: {message}")
    except Exception as e:
        print(f"[ERROR] Не удалось отправить сообщение в Telegram: {e}")

def main():
    while True:
        for symbol, level in SYMBOLS.items():
            price = get_price(symbol)
            if price is None:
                continue

            if price <= level:
                send_signal(f"🔔 {symbol} упал до {price} — ниже уровня {level}")
            else:
                print(f"{symbol}: {price} (без сигнала)")

        time.sleep(30)  # Проверка каждые 30 секунд

if __name__ == "__main__":
    main()
