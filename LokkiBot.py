import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот запущен и готов работать.")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сигнал по PEPE: Пока нет новой точки входа.")

async def signal_trx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сигнал по TRX: Пока нет новой точки входа.")

async def signal_ena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сигнал по ENA: Пока нет новой точки входа.")

async def signal_xrp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сигнал по XRP: Пока нет новой точки входа.")

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Портфель пока пуст. Ожидаем сделок.")

# Основная функция
async def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
    PORT = int(os.environ.get("PORT", "5000"))

    application = Application.builder().token(TOKEN).build()

    # Хендлеры
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("signal_pepe", signal_pepe))
    application.add_handler(CommandHandler("signal_trx", signal_trx))
    application.add_handler(CommandHandler("signal_ena", signal_ena))
    application.add_handler(CommandHandler("signal_xrp", signal_xrp))
    application.add_handler(CommandHandler("portfolio", portfolio))

    # Устанавливаем Webhook
    await application.bot.set_webhook(url=WEBHOOK_URL)

    # Запуск через Webhook
    await application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
