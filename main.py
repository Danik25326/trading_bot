import asyncio
import logging
from dotenv import load_dotenv
from bot.telegram_bot import start_bot
from scheduler import start_scheduler

# Завантажуємо змінні середовища
load_dotenv()

# Налаштування логування, щоб бачити помилки
logging.basicConfig(level=logging.INFO)

async def main():
    """Головна асинхронна функція для запуску бота та планувальника."""
    # Запускаємо Telegram-бота в одному потоці
    bot_task = asyncio.create_task(start_bot())
    # Запускаємо планувальник перевірки сигналів в іншому
    scheduler_task = asyncio.create_task(start_scheduler())

    # Чекаємо завершення обох задач (практично – нескінченно)
    await asyncio.gather(bot_task, scheduler_task)

if __name__ == "__main__":
    asyncio.run(main())
