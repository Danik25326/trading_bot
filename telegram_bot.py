import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот працює! Очікуйте сигнали...")

async def start_bot():
    """Основна функція запуску бота"""
    if not TOKEN:
        logging.error("No TELEGRAM_BOT_TOKEN")
        return
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    
    logging.info("Starting Telegram bot...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Тримаємо бота активним
    await asyncio.Event().wait()

# Альтернативна назва для сумісності
async def main():
    await start_bot()

if __name__ == "__main__":
    asyncio.run(start_bot())
