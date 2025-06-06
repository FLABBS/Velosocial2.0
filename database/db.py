# VelosocialBot/database/db.py
import aiosqlite
import os
from datetime import datetime
from config import DATABASE, GDPR_SETTINGS

DB_PATH = os.path.join(DATABASE["path"], DATABASE["name"])


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
                skill_level TEXT CHECK(
                    skill_level IN ('beginner', 'intermediate', 'pro')
                ),
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
