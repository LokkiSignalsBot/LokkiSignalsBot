import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Проверка наличия токена
if not BOT_TOKEN:
    raise RuntimeError("❌ Переменная окружения BOT_TOKEN не установлена.")

# Инициализация Telegram-приложения
application = Application.builder().token(BOT_TOKEN).build()

# Инициализация FastAPI
app = FastAPI()

# ==== Команды ====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Бот работает!")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 PEPE: вход от 0.000011500, тейк 0.000011900, стоп 0.000011400.")

async def signal_xrp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📉 XRP: следим за уровнем 0.60 — возможен отскок.")

async def signal_trx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 TRX: рост при пробое 0.1300.")

async def signal_ena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 ENA: накопление в зоне 0.68–0.70, возможен рост.")

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 Портфель:\n- PEPE: $300\n- XRP: $150\n- TRX: $50\n- Остальное в Earn/USDT")

async def alert_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 Уведомления включены.")

async def alert_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔕 Уведомления выключены.")

# ==== Регистрация команд ====

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("signal_pepe", signal_pepe))
application.add_handler(CommandHandler("signal_xrp", signal_xrp))
application.add_handler(CommandHandler("signal_trx", signal_trx))
application.add_handler(CommandHandler("signal_ena", signal_ena))
application.add_handler(CommandHandler("portfolio", portfolio))
application.add_handler(CommandHandler("alert_on", alert_on))
application.add_handler(CommandHandler("alert_off", alert_off))

# ==== Webhook ====

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
    except Exception as e:
        print(f"Ошибка обработки Webhook: {e}")
    return {"ok": True}

# ==== Инициализация Telegram при запуске ====

@app.on_event("startup")
async def startup():
    await application.initialize()
    print("✅ Telegram-бот инициализирован.")

# ==== Главная страница ====
@app.get("/")
async def root():
    return {"ok": True}
