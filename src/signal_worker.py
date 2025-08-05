import asyncio
import os
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

SYMBOLS = ["PEPEUSDT", "TRXUSDT", "ENAUSDT", "SUIUSDT", "MEMEUSDT"]

async def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"[ERROR] Не удалось получить цену {symbol}: {e}")
        return None

async def check_prices():
    while True:
        for symbol in SYMBOLS:
            price = await get_price(symbol)
            if price:
                message = f"{symbol} → {price}"
                await bot.send_message(chat_id=CHAT_ID, text=message)
        await asyncio.sleep(60)  # проверка каждую минуту

if __name__ == "__main__":
    asyncio.run(check_prices())
