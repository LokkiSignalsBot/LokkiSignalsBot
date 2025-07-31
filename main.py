import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8233879922:AAGHqdKZmSY853TCboDfNFV8DqRQdpYxOSU"
WEBHOOK_URL = "https://lokki-signals-bot.onrender.com"

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает через Webhook.")

# Основная функция запуска
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    # Установка Webhook
    await application.bot.set_webhook(WEBHOOK_URL)
    await application.initialize()
    await application.start()
    await application.updater.start_polling()  # <-- обязательная строка для инициализации, даже если polling не нужен
    await application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
