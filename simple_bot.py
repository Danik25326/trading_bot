import os
import asyncio
import logging
from dotenv import load_dotenv

load_dotenv()

async def test_bot():
    """Найпростіший тест бота"""
    logging.basicConfig(level=logging.INFO)
    logging.info("Бот запущено на Render!")
    
    # Тут можна додати простий код для перевірки
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token:
        logging.info("Токен Telegram знайдено")
    else:
        logging.error("Токен Telegram не знайдено")
    
    # Тримаємо скрипт активним
    while True:
        await asyncio.sleep(60)
        logging.info("Бот ще працює...")

if __name__ == "__main__":
    asyncio.run(test_bot())
