import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Получаем токен из переменных окружения
TOKEN = os.environ.get("TELEGRAM_TOKEN")

    app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path=TOKEN,
        webhook_url=f"https://lokki-signals-bot.onrender.com/{TOKEN}"
    )

if __name__ == '__main__':
    main()
