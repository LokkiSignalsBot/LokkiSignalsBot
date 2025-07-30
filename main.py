import os
from telegram.ext import Application, CommandHandler

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

# Команда /start
async def start(update, context):
    await update.message.reply_text("Бот успешно запущен!")

# Создаем и запускаем приложение
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
