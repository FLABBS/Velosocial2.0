# VelosocialBot/database/db.py
import aiosqlite
import os
from datetime import datetime
from config import DATABASE, GDPR_SETTINGS

DB_PATH = os.path.join(DATABASE["path"], DATABASE["name"])
# Ensure the database directory exists
os.makedirs(DATABASE["path"], exist_ok=True)

async def init_db() -> None:
    """Инициализация таблиц в базе данных."""
    async with aiosqlite.connect(DB_PATH) as conn:
        # Таблица пользователей
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                bike_type TEXT CHECK(bike_type IN ('road', 'mtb', 'city')),
                skill_level TEXT CHECK(skill_level IN ('beginner', 'intermediate', 'pro')),
                bio TEXT,
                contacts TEXT,
                lat REAL,
                lon REAL,
                is_visible BOOLEAN DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Таблица событий
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                route TEXT,
                event_date TIMESTAMP NOT NULL,
                max_participants INTEGER DEFAULT 10,
                chat_id TEXT,
                participants TEXT,
                FOREIGN KEY(creator_id) REFERENCES users(id)
            )
        ''')
        await conn.commit()

async def get_connection() -> aiosqlite.Connection:
    return await aiosqlite.connect(DB_PATH)

async def cleanup_old_locations() -> None:
    """Очищает устаревшие геоданные (GDPR)."""
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
            UPDATE users 
            SET lat = NULL, lon = NULL, is_visible = 0
            WHERE last_updated < datetime('now', ?)
        ''', (f"-{GDPR_SETTINGS['location_ttl_hours']} hours",))
        await conn.commit()