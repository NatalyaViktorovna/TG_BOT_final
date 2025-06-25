import os
import asyncio
from db import log_message_to_db, init_db
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
from openai_service import translate_text

init_db()

# Инициализация бота (без глобальной переменной)
def setup_bot():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
    
    application = ApplicationBuilder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application

# Асинхронная обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        user_id = update.effective_user.id
        username = update.effective_user.username or "unknown"
        
        # Параллельный запуск синхронных функций
        translated, _ = await asyncio.gather(
            asyncio.to_thread(translate_text, user_text),
            asyncio.to_thread(log_message_to_db, user_id, username, user_text, "<pending>")
        )
        
        await update.message.reply_text(translated)
    except Exception as e:
        print(f"Message handling error: {e}")

# Обработка вебхука
async def process_update(update_data: dict):
    try:
        application = setup_bot()  # Или передавать application как параметр
        update = Update.de_json(update_data, application.bot)
        await application.process_update(update)
        return True
    except Exception as e:
        print(f"Webhook processing failed: {e}")
        return False
