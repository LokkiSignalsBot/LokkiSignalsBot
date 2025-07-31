import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Получаем токен из переменных окружения
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Переменная для хранения состояния уведомлений
alerts_enabled = {}

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает ✅")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал PEPE: Ждём точку входа...")

async def signal_xrp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал XRP: Ждём точку входа...")

async def signal_trx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал TRX: Ждём точку входа...")

async def signal_ena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Сигнал ENA: Ждём точку входа...")

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 Портфель: в разработке...")

async def alert_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alerts_enabled[update.effective_chat.id] = True
    await update.message.reply_text("🔔 Уведомления включены!")

async def alert_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alerts_enabled[update.effective_chat.id] = False
    await update.message.reply_text("🔕 Уведомления отключены!")

def main():
    app = Application.builder().token(TOKEN).build()

    # Регистрируем команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal_pepe", signal_pepe))
    app.add_handler(CommandHandler("signal_xrp", signal_xrp))
    app.add_handler(CommandHandler("signal_trx", signal_trx))
    app.add_handler(CommandHandler("signal_ena", signal_ena))
    app.add_handler(CommandHandler("portfolio", portfolio))
    app.add_handler(CommandHandler("alert_on", alert_on))
    app.add_handler(CommandHandler("alert_off", alert_off))

    # Webhook запуск
    app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path=TOKEN,
        webhook_url=f"https://lokki-signals-bot.onrender.com/{TOKEN}"
    )

if __name__ == '__main__':
    main()
