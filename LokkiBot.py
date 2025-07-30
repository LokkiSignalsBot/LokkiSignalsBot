import os
import asyncio
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask-приложение
app = Flask(__name__)

# Токен Telegram-бота и URL для Webhook
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 5000))

# Инициализация Telegram-приложения
application = Application.builder().token(BOT_TOKEN).build()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает. Используй команды /signal_pepe, /signal_xrp, /signal_trx, /signal_ena")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 PEPE сигнал: LONG от 0.000011600, TP: 0.000011900, SL: 0.000011500")

async def signal_xrp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 XRP сигнал: ожидается")

async def signal_trx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 TRX сигнал: ожидается")

async def signal_ena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 ENA сигнал: ожидается")

# Регистрация команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("signal_pepe", signal_pepe))
application.add_handler(CommandHandler("signal_xrp", signal_xrp))
application.add_handler(CommandHandler("signal_trx", signal_trx))
application.add_handler(CommandHandler("signal_ena", signal_ena))

# Webhook endpoint
@app.route("/", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.process_update(update))
        return "ok", 200

# Устанавливаем Webhook при запуске
def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url=https://lokki-signals-bot.onrender.com/"
    response = requests.get(url)
    print("Webhook setup response:", response.text)

if __name__ == "__main__":
    set_webhook()
    print(f"Starting Flask app on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
