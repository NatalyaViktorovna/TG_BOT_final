import os
import logging
from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from bot import setup_bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

bot_application = setup_bot()
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

if not WEBHOOK_URL:
    logger.warning("⚠️ WEBHOOK_URL is not set — webhook won't be configured.")
else:
    logger.info(f"✅ WEBHOOK_URL is set: {WEBHOOK_URL}")

@app.route("/webhook", methods=["POST"])
def webhook():
    if bot_application:
        update = request.get_json(force=True)
        bot_application.update_queue.put_nowait(update)
        return jsonify({"status": "ok"}), 200
    return jsonify({"error": "Bot not initialized"}), 500

@app.route("/")
def index():
    return "🚀 Telegram bot is running."