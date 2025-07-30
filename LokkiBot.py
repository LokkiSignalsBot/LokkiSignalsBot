import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", default=8443))

# Логирование
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Flask-приложение
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

# Инициализация Telegram App
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Бот успешно запущен и готов к работе!")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Актуальный сигнал по PEPE: вход от 0.000011600, тейк 0.000011900")

# Роут Webhook
@app.route("/", methods=["POST"])
def receive_update():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(telegram_app.process_update(update))
    return "ok"

# Регистрируем команды
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("signal_pepe", signal_pepe))

# Установка Webhook и запуск сервера
async def set_webhook():
    await bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Webhook установлен: {WEBHOOK_URL}")

if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=PORT)
