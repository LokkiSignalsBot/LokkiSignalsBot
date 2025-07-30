import os
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает через Webhook!")


# Запуск Telegram Application
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))


# Webhook endpoint
@app.route("/", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
        return "ok", 200


# Установка Webhook и запуск Flask
if __name__ == "__main__":
    async def run():
        await application.initialize()
        await application.bot.set_webhook(url=WEBHOOK_URL)
        await application.start()
        app.run(host="0.0.0.0", port=PORT)

    import asyncio
    asyncio.run(run())
