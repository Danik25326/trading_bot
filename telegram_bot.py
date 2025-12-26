import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Отримуємо токен з змінних середовища
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробник команди /start"""
    await update.message.reply_text(
        "🤖 Бот для сигналів Pocket Option активований!\n"
        "Я буду надсилати сигнали кожні 5 хвилин з вірогідністю >70%."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробник команди /help"""
    await update.message.reply_text(
        "📈 Команди:\n"
        "/start - Запустити бота\n"
        "/help - Допомога\n"
        "/status - Статус бота\n"
        "/test - Тестовий сигнал"
    )

async def send_signal_message(chat_id: int, message: str, application: Application):
    """Надсилає повідомлення з сигналом"""
    try:
        await application.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Помилка відправки повідомлення: {e}")

# 👇 ОСНОВНА ФУНКЦІЯ, ЯКУ ІМПОРТУЄ main.py
async def start_bot():
    """Запускає Telegram бота"""
    if not TOKEN:
        logging.error("❌ Не знайдено TELEGRAM_BOT_TOKEN")
        return
    
    logging.info("🚀 Запуск Telegram бота...")
    
    # Створюємо додаток
    application = Application.builder().token(TOKEN).build()
    
    # Додаємо обробники команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Ініціалізуємо та запускаємо
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    logging.info("✅ Бот запущено та очікує повідомлень...")
    
    # Тримаємо бота активним
    await asyncio.Event().wait()

# Альтернативна назва функції (якщо ви використовували іншу)
async def main():
    """Альтернативна назва для запуску"""
    await start_bot()

# Експортуємо функції
__all__ = ['start_bot', 'send_signal_message']
