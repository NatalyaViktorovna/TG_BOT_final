import os
import logging
from flask import Flask, request, jsonify
from bot import setup_bot, process_update

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

app = Flask(__name__)
setup_bot()

@app.route('/')
def home():
    return "🤖 Telegram Translator Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update_data = request.get_json(force=True)
        process_update(update_data)  # Убрали asyncio
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.exception("Webhook error")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
