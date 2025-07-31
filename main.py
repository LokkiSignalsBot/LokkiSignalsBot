():
    await application.bot.set_webhook(WEBHOOK_URL)
    await application.initialize()
    asyncio.create_task(application.start())

# При остановке
@app.on_event("shutdown")
async def on_shutdown():
    await application.stop()

# Хендлеры
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("signal_pepe", signal_pepe))
application.add_handler(CommandHandler("signal_xrp", signal_xrp))
application.add_handler(CommandHandler
async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 Портфель: скоро будет отображаться.")

async def alert_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 Уведомления включены.")

async def alert_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔕 Уведомления отключены.")

# === Telegram bot ===
application = ApplicationBuilder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("signal_pepe", signal_pepe))
application.add_handler(CommandHandler("signal_xrp", signal_xrp))
application.add_handler(CommandHandler("signal_trx", signal_trx))
application.add_handler(CommandHandler("signal_ena", signal_ena))
application.add_handler(CommandHandler("portfolio", portfolio))
application.add_handler(CommandHandler("alert_on", alert_on))
application.add_handler(CommandHandler("alert_off", alert_off))

@app.post("/webhook/{token}")
async def process_webhook(token: str, request: Request):
    if token != BOT_TOKEN:
        return {"ok": False, "description": "Invalid token"}
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"ok": True}

@app.on_event("startup")
async def startup():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL + f"/webhook/{BOT_TOKEN}")
    await application.start()

@app.on_event("shutdown")
async def shutdown():
    await application.stop()
