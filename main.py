import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))
WEBHOOK_URL = "https://lokki-signals-bot2.onrender.com"

bot = Bot(token=BOT_TOKEN)
app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

# === Команды ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Бот Lokki Signals работает!")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 PEPE: пока нет сигнала.")

async def signal_xrp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 XRP: пока нет сигнала.")

async def signal_trx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 TRX: пока нет сигнала.")

async def signal_ena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 ENA: пока нет сигнала.")

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 Портфель: данные не подключены.")

async def alert_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 Уведомления ВКЛЮЧЕНЫ.")

async def alert_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔕 Уведомления ВЫКЛЮЧЕНЫ.")

# === Регистрация команд ===
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("signal_pepe", signal_pepe))
application.add_handler(CommandHandler("signal_xrp", signal_xrp))
application.add_handler(CommandHandler("signal_trx", signal_trx))
application.add_handler(CommandHandler("signal_ena", signal_ena))
application.add_handler(CommandHandler("portfolio", portfolio))
application.add_handler(CommandHandler("alert_on", alert_on))
application.add_handler(CommandHandler("alert_off", alert_off))

# === Webhook endpoint ===
@app.post("/")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"status": "ok"}

# === Инициализация и запуск Telegram-приложения при старте ===
@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.start()

@app.on_event("shutdown")
async def on_shutdown():
    await application.stop()
    await application.shutdown()
