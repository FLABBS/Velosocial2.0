# VelosocialBot/main.py
import asyncio
import logging
import logging.config
from pathlib import Path
import yaml

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TELEGRAM_TOKEN, BOT_DEFAULT, LOGGING, GDPR_SETTINGS
from database.db import init_db
from .handlers import common, profile, map, events
from .utils.gdpr import cleanup_old_locations

# Загрузка текстовых шаблонов
with open(
    Path(__file__).resolve().parent.parent / "texts.yml",
    "r",
    encoding="utf-8",
) as f:
    TEXTS = yaml.safe_load(f)

# Настройка логгирования через dictConfig
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

async def main() -> None:
    # Инициализация БД
    await init_db()

    # Создание объектов бота и диспетчера
    bot = Bot(token=TELEGRAM_TOKEN, default=BOT_DEFAULT)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
    dp.include_routers(
        common.router,
        profile.router,
        map.router,
        events.router
    )

    # Настройка планировщика задач (GDPR-очистка)
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        cleanup_old_locations,
        "interval",
        hours=GDPR_SETTINGS["auto_cleanup_hours"],
        jitter=300  # Разброс ±5 минут для распределения нагрузки
    )
    scheduler.start()

    # Запуск бота
    logger.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
