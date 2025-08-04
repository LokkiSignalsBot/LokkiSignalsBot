import os
import time
import requests
from telegram import Bot

# Переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Telegram бот
bot = Bot(token=BOT_TOKEN)

# Монеты и уровни сигналов
MONITOR = {
    "PEPEUSDT": {"buy_below": 0.00001160, "sell_above": 0.00001200},
    "TRXUSDT":  {"buy_below": 0.1200,     "sell_above": 0.1250},
    "ENAUSDT":  {"buy_below": 0.530,      "sell_above": 0.570},
    "MEMEUSDT": {"buy_below": 0.0180,     "sell_above": 0.0200},
    "SUIUSDT":  {"buy_below": 0.610,      "sell_above": 0.650}
}

# Получение текущей цены
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url)
        return float(response.json()["price"])
    except Exception as e:
        print(f"Ошибка получения цены {symbol}: {e}")
        return None

# Основной цикл
def check_prices():
    while True:
        for symbol, levels in MONITOR.items():
            price = get_price(symbol)
            if price is None:
                continue
            message = None
            if price <= levels["buy_below"]:
                message = f"🟢 BUY сигнал по {symbol} — Цена: {price}"
            elif price >= levels["sell_above"]:
                message = f"🔴 SELL сигнал по {symbol} — Цена: {price}"
            if message:
                bot.send_message(chat_id=CHAT_ID, text=message)
                print(f"Отправлено: {message}")
        time.sleep(30)  # проверка каждые 30 сек

# Старт
if __name__ == "__main__":
    check_prices()
