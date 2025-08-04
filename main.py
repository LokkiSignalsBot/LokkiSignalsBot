import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # например: https://lokki-signals-bot.onrender.com

app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Бот работает через Webhook!")

# Пример команды /signal_pepe
async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 Сигнал по PEPE: вход 0.00001150, тейк 0.00001190, стоп 0.00001130")

# Обработка webhook
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"ok": True}

# Запускаем при старте и устанавливаем Webhook
@app.on_event("startup")
async def on_startup():
    await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    await application.initialize()
    await application.start()
    print("✅ Webhook установлен")

@app.on_event("shutdown")
async def on_shutdown():
    await application.stop()
