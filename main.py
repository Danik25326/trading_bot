import asyncio
import logging
from dotenv import load_dotenv
from bot.telegram_bot import TelegramBot
from scheduler import start_scheduler

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Головна асинхронна функція для запуску бота та планувальника."""
    # Ініціалізація бота
    bot = TelegramBot()
    
    # Запускаємо Telegram-бота в одному потоці
    bot_task = asyncio.create_task(bot.run())
    # Запускаємо планувальник перевірки сигналів в іншому
    scheduler_task = asyncio.create_task(start_scheduler(bot))  # Передаємо бота в планувальник
    
    # Чекаємо завершення обох задач
    await asyncio.gather(bot_task, scheduler_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинено")
