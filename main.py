import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Додаємо поточну директорію до шляху Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def main():
    """Спрощена версія без HTTP сервера"""
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    
    # Імпортуємо тут, після налаштування шляхів
    try:
        from bot.telegram_bot import start_bot
        from scheduler import start_scheduler
        
        logging.info("Запуск бота...")
        
        # Запускаємо обидва компоненти
        bot_task = asyncio.create_task(start_bot())
        scheduler_task = asyncio.create_task(start_scheduler())
        
        # Чекаємо на обидві задачі
        await asyncio.gather(bot_task, scheduler_task)
        
    except ImportError as e:
        logging.error(f"Помилка імпорту: {e}")
        logging.error("Перевірте структуру файлів та __init__.py")
        raise

if __name__ == "__main__":
    # Для Render - просто запускаємо asyncio
    asyncio.run(main())
