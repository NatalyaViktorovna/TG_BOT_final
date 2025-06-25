import os
import logging
import asyncio
from flask import Flask, request
from bot import setup_bot
from telegram import Update

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

# Flask-приложение
app = Flask(__name__)

# Telegram-приложение (Application)
telegram_app = setup_bot()

@app.route('/')
def home():
    return "🤖 Telegram Translator Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update_data = request.get_json(force=True)
        update = Update.de_json(update_data, telegram_app.bot)

        # Передаём обновление в очередь
        asyncio.get_event_loop().create_task(telegram_app.update_queue.put(update))

        return "OK", 200
    except Exception as e:
        logger.exception("Webhook processing error")
        return f"Error: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
