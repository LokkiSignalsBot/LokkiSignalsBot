import os
import time
import requests
from telegram import Bot

# Загружаем переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

bot = Bot(token=BOT_TOKEN)

# Список монет для отслеживания (Futures)
SYMBOLS = ["PEPEUSDT", "TRXUSDT", "ENAUSDT", "MEMEUSDT", "SUIUSDT"]

# Порог для сигнала (можно менять)
PRICE_LIMITS = {
    "PEPEUSDT": 0.00001150,
    "TRXUSDT": 0.1220,
    "ENAUSDT": 0.540,
    "MEMEUSDT": 0.0180,
    "SUIUSDT": 3.300
}

def get_futures_price(symbol):
    url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"[ERROR] Не удалось получить цену {symbol}: {e}")
        return None

def send_signal(symbol, price):
    message = f"📊 {symbol} на фьючерсах: {price}\n"
    message += f"Порог для входа: {PRICE_LIMITS[symbol]}"
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    while True:
        for symbol in SYMBOLS:
            price = get_futures_price(symbol)
            if price is not None:
                print(f"{symbol}: {price}")
                if price <= PRICE_LIMITS[symbol]:
                    send_signal(symbol, price)
        time.sleep(60)

if __name__ == "__main__":
    main()
