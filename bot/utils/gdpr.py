# VelosocialBot/utils/gdpr.py
import logging
from datetime import datetime, timedelta
from database.db import get_connection
from config import GDPR_SETTINGS

logger = logging.getLogger(__name__)

async def cleanup_old_locations() -> None:
    """Асинхронная очистка устаревших геоданных пользователей согласно GDPR"""
    try:
        async with get_connection() as conn:
            # Рассчет времени устаревания
            ttl_hours = GDPR_SETTINGS["location_ttl_hours"]
            cutoff_time = datetime.now() - timedelta(hours=ttl_hours)

            # Выполнение SQL-запроса
            cursor = await conn.cursor()
            await cursor.execute('''
                UPDATE users 
                SET 
                    lat = NULL,
                    lon = NULL,
                    is_visible = 0
                WHERE 
                    last_updated < ?
                    AND is_visible = 1
            ''', (cutoff_time,))

            affected_rows = cursor.rowcount
            await conn.commit()
            logger.info(f"GDPR: Очищено {affected_rows} записей")

    except Exception as e:
        logger.error(f"Ошибка GDPR-очистки: {str(e)}")
        raise