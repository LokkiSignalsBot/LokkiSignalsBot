import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import requests

# Получение переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", default=10000))

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Flask-приложение
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

# Telegram Application
application = Application.builder().token(BOT_TOKEN).build()


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает! ✅")


# Регистрируем команду
application.add_handler(CommandHandler("start", start))


# Webhook endpoint для Telegram
@app.route("/", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.run(application.process_update(update))
        return "ok", 200


# Устанавливаем Webhook при запуске
def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"
    response = requests.get(url)
    print("Webhook setup response:", response.text)


if __name__ == "__main__":
    set_webhook()
    print(f"Starting Flask app on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT)
