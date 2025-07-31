import os
import asyncio
from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

telegram_app = Application.builder().token(BOT_TOKEN).build()
app = FastAPI()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Бот успешно работает!")

telegram_app.add_handler(CommandHandler("start", start))

# При старте FastAPI — запускаем Telegram Webhook
@app.on_event("startup")
async def startup():
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(telegram_app.start())
