import os
from fastapi import FastAPI, Request
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# === Константы ===
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_HOST = "https://lokki-signals-bot.onrender.com"
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
PORT = 10000

# === FastAPI ===
app = FastAPI()

# === Бот-приложение ===
application = Application.builder().token(BOT_TOKEN).build()

# === Команды ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Бот запущен и готов к работе!")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал по PEPE: вход от 0.000011500, тейк 0.000011900, стоп 0.000011450")

async def signal_xrp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал по XRP: вход от 0.62, тейк 0.655, стоп 0.598")

async def signal_trx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал по TRX: вход от 0.1295, тейк 0.136, стоп 0.125")

async def signal_ena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал по ENA: вход от 0.445, тейк 0.472, стоп 0.432")

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 Твой текущий портфель: PEPE, XRP, ENA, TRX. Баланс и позиции обновляются вручную.")

async def alert_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 Уведомления включены.")

async def alert_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔕 Уведомления отключены.")

# === Роутинг команд ===
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("signal_pepe", signal_pepe))
application.add_handler(CommandHandler("signal_xrp", signal_xrp))
application.add_handler(CommandHandler("signal_trx", signal_trx))
application.add_handler(CommandHandler("signal_ena", signal_ena))
application.add_handler(CommandHandler("portfolio", portfolio))
application.add_handler(CommandHandler("alert_on", alert_on))
application.add_handler(CommandHandler("alert_off", alert_off))


# === Webhook эндпоинт ===
@app.post(WEBHOOK_PATH)
async def webhook_handler(жrequest: Request):
    update = Update.de_json(await request.json(), application.bot)
    await application.update_queue.put(update)
    return {"ok": True}


# === Запуск при старте Render ===
@app.on_event("startup")
async def on_startup():
    await application.bot.set_webhook(WEBHOOK_URL)
