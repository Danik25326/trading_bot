import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from telegram_bot import start_bot

# КРИТИЧНО: Додаємо поточну директорію до Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Тепер імпортуємо модулі ВСЕРЕДИНИ функції
load_dotenv()
logging.basicConfig(level=logging.INFO)

async def main():
    logging.info("=== START BOT ===")
    logging.info(f"Current directory: {current_dir}")
    logging.info(f"Python path: {sys.path}")
    
    # Перевірка наявності папок
    bot_dir = os.path.join(current_dir, 'bot')
    trading_dir = os.path.join(current_dir, 'trading')
    
    logging.info(f"Bot dir exists: {os.path.exists(bot_dir)}")
    logging.info(f"Trading dir exists: {os.path.exists(trading_dir)}")
    
    if os.path.exists(bot_dir):
        logging.info(f"Files in bot/: {os.listdir(bot_dir)}")
    
    # Імпорт ВСЕРЕДИНИ функції після додавання шляху
    try:
        # Відносний імпорт
        from bot.telegram_bot import start_bot
        from scheduler import start_scheduler
        
        logging.info("✅ All modules imported successfully")
        
        # Запускаємо бота та планувальник
        bot_task = asyncio.create_task(start_bot())
        scheduler_task = asyncio.create_task(start_scheduler())
        
        await asyncio.gather(bot_task, scheduler_task)
        
    except ImportError as e:
        logging.error(f"❌ Import error: {e}")
        # Детальна інформація
        import traceback
        logging.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    asyncio.run(main())
