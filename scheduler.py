import os
import sys
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Додаємо шлях для імпортів
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def start_scheduler():
    """Запускає планувальник для перевірки сигналів"""
    try:
        from trading.signal_generator import SignalGenerator
        
        scheduler = AsyncIOScheduler()
        interval_min = int(os.getenv("ANALYSIS_INTERVAL_MINUTES", 5))
        
        generator = SignalGenerator()
        
        # Додаємо завдання
        scheduler.add_job(
            generator.check_and_generate_signals,
            'interval',
            minutes=interval_min,
            id='market_scan'
        )
        
        scheduler.start()
        logging.info(f"Планувальник запущено. Перевірка кожні {interval_min} хв.")
        
        # Тримаємо планувальник активним
        await asyncio.Event().wait()
        
    except ImportError as e:
        logging.error(f"Помилка імпорту в scheduler: {e}")
        raise
