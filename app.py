import os
import logging
from flask import Flask, request
from bot import setup_bot

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

# Flask-приложение
app = Flask(__name__)

# Telegram Bot application (создаём один раз)
telegram_app = setup_bot()

@app.route('/')
def home():
    return "🤖 Telegram Translator Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработка входящих Telegram webhook-запросов"""
    try:
        update_data = request.get_json(force=True)
        telegram_app.update_queue.put_nowait(update_data)
        return "OK", 200
    except Exception as e:
        logger.exception("Webhook processing error")
        return f"Error: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
