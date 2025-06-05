# VelosocialBot/config.py
import os
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# --- Основные настройки ---
TELEGRAM_TOKEN = "7544908894:AAFbDrA2u79O6ymTwdbY_UfXAzluDVmpCSk"  # Токен бота

# --- Настройки бота (aiogram 3.7.0+) ---
BOT_DEFAULT = DefaultBotProperties(
    parse_mode=ParseMode.HTML,          # HTML-разметка по умолчанию
    link_preview_is_disabled=True       # Отключить превью ссылок
)

# --- Яндекс API ---
YANDEX_MAPS_API_KEY = "a2662caf-b2d7-4f64-a308-b7dca6aa499f"       # Static API (карты)
YANDEX_GEOCODER_API_KEY = "1e213321-3419-4509-bc92-2c7aef39a2d6"  # Геокодер

# --- Настройки карты ---
MAP_SETTINGS = {
    "default_zoom": 13,             # Стартовый зум
    "map_size": "600,400",          # Ширина x высота (пиксели)
    "user_icon": "pm2rdl",          # Иконка текущего пользователя (красная)
    "others_icon": "pm2grl",        # Иконки других пользователей (зелёная)
    "max_distance_km": 5            # Радиус поиска (км)
}

# --- Настройки GDPR ---
GDPR_SETTINGS = {
    "location_ttl_hours": 24,       # Хранение геоданных (часы)
    "auto_cleanup_hours": 6         # Интервал очистки БД (часы)
}

# --- Настройки базы данных ---
DATABASE = {
    "name": "velosocial.db",        # Имя файла SQLite
    "path": os.path.join(os.path.dirname(__file__), "database")  # Путь к папке
}

# --- Настройки геокодера ---
GEOCODER_SETTINGS = {
    "timeout": 5,                   # Таймаут запроса (сек)
    "lang": "ru_RU",                # Язык ответов
    "results_limit": 1              # Максимум результатов
}

# --- Логирование ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": LOG_LEVEL
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "level": LOG_LEVEL,
            "filename": os.path.join(os.path.dirname(__file__), "velosocial.log"),
            "maxBytes": 1048576,
            "backupCount": 3,
            "encoding": "utf-8"
        }
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console", "file"]
    }
}
