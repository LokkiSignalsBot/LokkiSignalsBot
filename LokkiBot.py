from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

"BOT_TOKEN=8233879922:AAHUEhrah5xIM3oa0t3MxFyqntY6F2BNeFo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает. ✅")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
