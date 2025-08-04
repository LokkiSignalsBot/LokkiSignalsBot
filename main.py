import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Бот работает!")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 PEPE: сигнал скоро появится!")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("signal_pepe", signal_pepe))

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"message": "✅ LokkiSignalsBot is running"}

@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.start()
    await application.bot.set_webhook(url=WEBHOOK_URL + "/webhook")
    print("✅ Webhook установлен и бот запущен.")
