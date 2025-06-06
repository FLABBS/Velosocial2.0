# VelosocialBot/config.py
import os
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# --- Основные настройки ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Токен бота

# --- Настройки бота (aiogram 3.7.0+) ---
BOT_DEFAULT = DefaultBotProperties(
    parse_mode=ParseMode.HTML,          # HTML-разметка по умолчанию
    link_preview_is_disabled=True       # Отключить превью ссылок
)

# --- Яндекс API ---
YANDEX_MAPS_API_KEY = os.getenv("YANDEX_MAPS_API_KEY")  # Static API (карты)
YANDEX_GEOCODER_API_KEY = os.getenv("YANDEX_GEOCODER_API_KEY")  # Геокодер

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
    "path": os.path.join(
        os.path.dirname(__file__), "database"
    ),  # Путь к папке
}

# --- Настройки геокодера ---
GEOCODER_SETTINGS = {
    "timeout": 5,                   # Таймаут запроса (сек)
    "lang": "ru_RU",                # Язык ответов
    "results_limit": 1              # Максимум результатов
}

# --- Логирование ---
# Чтение уровня логирования из переменной окружения
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Конфигурация для logging.config.dictConfig
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": os.path.join(os.path.dirname(__file__), "bot.log"),
            "maxBytes": 1048576,  # 1 MB
            "backupCount": 3,
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console", "file"],
    },
}
