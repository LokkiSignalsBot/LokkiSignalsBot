import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()

application = Application.builder().token(BOT_TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Бот работает!")

# Пример команды /signal_pepe
async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 Сигнал по PEPE: вход при пробое уровня 🔔")

# Обработка webhook
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"ok": True}

# 🔧 Добавим корневой маршрут (уберет ошибку 404 при GET-запросе)
@app.get("/")
async def root():
    return {"message": "✅ LokkiSignalsBot is running"}

# Стартовые действия при запуске
@app.on_event("startup")
async def on_startup():
    await application.bot.set_webhook(url=WEBHOOK_URL + "/webhook")
    await application.initialize()
    await application.start()
    print("✅ Webhook установлен и бот запущен")
