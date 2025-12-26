import os
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from trading.signal_generator import SignalGenerator

async def start_scheduler(bot):
    """Запускає планувальник для перевірки сигналів кожні N хвилин."""
    scheduler = AsyncIOScheduler()
    interval_min = int(os.getenv("ANALYSIS_INTERVAL_MINUTES", 5))
    
    # Створюємо генератор сигналів
    signal_generator = SignalGenerator(bot)  # Передаємо бота в генератор
    
    # Додаємо завдання, яке виконується кожні `interval_min` хвилин
    scheduler.add_job(
        signal_generator.check_and_generate_signals,
        'interval',
        minutes=interval_min,
        id='market_scan'
    )
    scheduler.start()
    logging.info(f"Планувальник сигналів запущено. Перевірка кожні {interval_min} хв.")
    
    # Необхідно тримати програму живою
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
