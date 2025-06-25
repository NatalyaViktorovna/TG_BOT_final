import os
from db import log_message_to_db, init_db
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
from openai_service import translate_text

init_db()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name or "unknown"
    translated = translate_text(user_text)

    log_message_to_db(user_id=user_id, username=username, original=user_text, translated=translated)
    await update.message.reply_text(translated)

def setup_bot():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise Exception("TELEGRAM_BOT_TOKEN is not set")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app