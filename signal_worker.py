
        print(f"[INFO] {symbol}: {price:.8f} (threshold {threshold})")  # лог в консоль
        if price <= threshold:
            message = f"📉 Сигнал на покупку {symbol}\nЦена: {price:.8f} USDT\nПорог: {threshold}"
            try:
                bot.send_message(chat_id=CHAT_ID, text=message)
                print(f"[SENT] {symbol} сигнал отправлен")
            except Exception as e:
                print(f"[ERROR] Telegram: {e}")

def main():
    try:
        bot.send_message(chat_id=CHAT_ID, text="🤖 Бот сигналов запущен и следит за рынком.")
    except Exception as e:
        print(f"[ERROR] Стартовое сообщение не отправлено: {e}")

    while True:
        analyze_and_send()
        time.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
