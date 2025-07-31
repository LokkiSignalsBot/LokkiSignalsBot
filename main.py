from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

# Примеры команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Бот работает.")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 PEPE сигнал: вход по 0.00001050, стоп 0.00000995, тейк 0.00001180")

# Роут Telegram webhook
@app.post("/")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}

# Добавляем команды
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("signal_pepe", signal_pepe))

# Запускаем Webhook при старте
@app.on_event("startup")
async def on_startup():
    await application.bot
