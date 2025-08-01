import os
import time
import requests
from telegram import Bot

# Получение токена и chat_id из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

# Монеты и их пороги для сигнала
SYMBOLS = {
    "PEPEUSDT": 0.00001150,
    "ENAUSDT": 0.540,
    "TRXUSDT": 0.1220,
    "MEMEUSDT": 0.0180
}

# Получение цены с Binance
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"[ERROR] {symbol}: {e}")
        return None

# Проверка условий и отправка сигнала
def analyze_and_send():
    for symbol, threshold in SYMBOLS.items():
        price = get_price(symbol)
        if price is None:
            continue
        if price <= threshold:
            message = f"📉 Сигнал на покупку {symbol}\nЦена: {price:.8f} USDT\nПорог: {threshold}"
            try:
                bot.send_message(chat_id=CHAT_ID, text=message)
                print(f"[INFO] Отправлен сигнал по {symbol}")
            except Exception as e:
                print(f"[ERROR] Ошибка при отправке в Telegram: {e}")

# Основной цикл
def main():
    print("🔄 Запуск анализа сигналов...")
    while True:
        analyze_and_send()
        time.sleep(30)

if __name__ == "__main__":
    main()
