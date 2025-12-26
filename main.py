import asyncio
import logging
from aiohttp import web
from dotenv import load_dotenv

# Додаємо HTTP сервер для Render health checks
async def health_check(request):
    return web.Response(text="Bot is alive")

async def start_background_tasks(app):
    """Запускаємо бота і планувальник у фоновому режимі"""
    from bot.telegram_bot import start_bot
    from scheduler import start_scheduler
    
    # Запускаємо в окремих задачах
    app['bot_task'] = asyncio.create_task(start_bot())
    app['scheduler_task'] = asyncio.create_task(start_scheduler())
    logging.info("Фонові задачі запущено")

async def cleanup_background_tasks(app):
    """Коректне закриття при виході"""
    app['bot_task'].cancel()
    app['scheduler_task'].cancel()
    await asyncio.gather(app['bot_task'], app['scheduler_task'], return_exceptions=True)

async def main_app():
    """Головний додаток з HTTP сервером"""
    load_dotenv()
    
    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/', health_check)  # Кореневий шлях теж
    
    # Додаємо фонові задачі
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    return app

if __name__ == "__main__":
    # Це потрібно для Render
    logging.basicConfig(level=logging.INFO)
    web.run_app(main_app(), port=10000)  # Render сам призначає порт
