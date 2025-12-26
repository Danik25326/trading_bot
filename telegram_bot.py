import os
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN не встановлено в .env файлі")
        self.bot = Bot(token=self.token)
        self.application = Application.builder().token(self.token).build()
        
    async def start_command(self, update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /start"""
        user = update.effective_user
        await update.message.reply_text(
            f"Привіт, {user.first_name}!\n"
            f"Я бот для торгових сигналів Pocket Option.\n"
            f"Сигнали генеруються кожні 5 хвилин з ймовірністю >70%."
        )
    
    async def help_command(self, update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /help"""
        help_text = """
Доступні команди:
/start - Початок роботи
/help - Це повідомлення
/status - Статус бота
/signals - Останні сигнали (якщо є)
        """
        await update.message.reply_text(help_text)
    
    async def status_command(self, update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /status"""
        # Тут можна додати перевірку статусу з'єднань
        await update.message.reply_text("Бот активний. Очікуйте сигнали!")
    
    def setup_handlers(self):
        """Налаштування обробників команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        # Додайте інші команди за потреби
    
    async def send_message(self, chat_id: int, text: str):
        """Надіслати повідомлення в конкретний чат"""
        try:
            await self.bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Помилка відправки повідомлення: {e}")
    
    async def run(self):
        """Запуск бота"""
        self.setup_handlers()
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        logger.info("Telegram бот запущений")

    async def stop(self):
        """Зупинка бота"""
        await self.application.stop()
