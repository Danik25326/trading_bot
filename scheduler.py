import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from trading.signal_generator import check_and_generate_signals

async def start_scheduler():
    """Запускає планувальник для перевірки сигналів кожні N хвилин."""
    scheduler = AsyncIOScheduler()
    interval_min = int(os.getenv("ANALYSIS_INTERVAL_MINUTES", 5))

    # Додаємо завдання, яке виконується кожні `interval_min` хвилин
    scheduler.add_job(
        check_and_generate_signals,
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
