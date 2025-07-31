import os
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET_PATH = os.getenv("WEBHOOK_SECRET_PATH")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CHAT_ID = int(os.getenv("CHAT_ID"))

app = FastAPI()
bot = Bot(token=BOT_TOKEN)

application = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Бот запущен и готов к работе!")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал по PEPE: ждите обновления...")

async def signal_xrp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал по XRP: ждите обновления...")

async def signal_trx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал по TRX: ждите обновления...")

async def signal_ena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал по ENA: ждите обновления...")

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 Ваш портфель: скоро здесь появится информация.")

async def alert_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 Уведомления включены.")

async def alert_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔕 Уведомления выключены.")

# Регистрация хендлеров
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("signal_pepe", signal_pepe))
application.add_handler(CommandHandler("signal_xrp", signal_xrp))
application.add_handler(CommandHandler("signal_trx", signal_trx))
application.add_handler(CommandHandler("signal_ena", signal_ena))
application.add_handler(CommandHandler("portfolio", portfolio))
application.add_handler(CommandHandler("alert_on", alert_on))
application.add_handler(CommandHandler("alert_off", alert_off))

@app.post(f"/{WEBHOOK_SECRET_PATH}")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await application.update_queue.put(update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await bot.set_webhook(url=WEBHOOK_URL + f"/{WEBHOOK_SECRET_PATH}")
    await application.start()
    print("✅ Bot started with Webhook")

@app.on_event("shutdown")
async def on_shutdown():
    await application.stop(
