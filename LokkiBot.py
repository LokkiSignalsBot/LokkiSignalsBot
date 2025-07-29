from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот запущен.")

app = Application.builder().token("8021467739:AAHqkVoZnCeJbifEI-DchPzoMKks98zfGA").build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
