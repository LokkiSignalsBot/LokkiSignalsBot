from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8233879922:AAGHqdKZmSY853TCboDfNFV8DqRQdpYxOSU"
CHAT_ID = 8233879922  # заменишь, если нужно

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает ✅")

async def signal_pepe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 PEPE сигнал: LONG от 0.00001159, тейк 0.00001190, стоп 0.00001150")

async def signal_xrp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 XRP сигнал: ожидается пробой уровня 0.60 — следим за входом.")

async def signal_trx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 TRX сигнал: лонг от 0.1300, тейк 0.1350, стоп 0.1275.")

async def signal_ena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 ENA сигнал: ждём закрепа выше 0.72 — может быть точка входа.")

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 Портфель: PEPE — $11.59, XRP — $15.20, TRX — $9.80")

alerts_enabled = {}

async def alert_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alerts_enabled[update.effective_chat.id] = True
    await update.message.reply_text("🔔 Уведомления включены!")

async def alert_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alerts_enabled[update.effective_chat.id] = False
    await update.message.reply_text("🔕 Уведомления выключены.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal_pepe", signal_pepe))
    app.add_handler(CommandHandler("signal_xrp", signal_xrp))
    app.add_handler(CommandHandler("signal_trx", signal_trx))
    app.add_handler(CommandHandler("signal_ena", signal_ena))
    app.add_handler(CommandHandler("portfolio", portfolio))
    app.add_handler(CommandHandler("alert_on", alert_on))
    app.add_handler(CommandHandler("alert_off", alert_off))

    app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path=BOT_TOKEN,
        webhook_url=f"https://lokki-signals-bot.onrender.com/{BOT_TOKEN}"
    )

if __name__ == '__main__':
    main()
