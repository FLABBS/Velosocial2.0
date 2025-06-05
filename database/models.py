# VelosocialBot/database/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List

@dataclass
class User:
    """Модель пользователя для БД (без изменений)"""
    telegram_id: int
    username: Optional[str] = None
    bike_type: Optional[str] = None  # 'road', 'mtb', 'city'
    skill_level: Optional[str] = None  # 'beginner', 'intermediate', 'pro'
    bio: Optional[str] = None
    contacts: Optional[Dict[str, str]] = None  # {'telegram': '@username'}
    lat: Optional[float] = None
    lon: Optional[float] = None
    is_visible: bool = False
    last_updated: datetime = datetime.now()

    def validate(self):
        """Валидация данных (синхронная, не требует изменений)"""
        if self.bike_type and self.bike_type not in {'road', 'mtb', 'city'}:
            raise ValueError("Недопустимый тип велосипеда")
        if self.skill_level and self.skill_level not in {'beginner', 'intermediate', 'pro'}:
            raise ValueError("Недопустимый уровень подготовки")

@dataclass
class Event:
    """Модель события для БД (без изменений)"""
    creator_id: int
    description: str
    route: str
    event_date: datetime
    max_participants: int = 10
    chat_id: Optional[str] = None  # ID Telegram-чата
    participants: Optional[List[int]] = None  # Список telegram_id
    id: Optional[int] = None  # Автоинкрементный ID

    def add_participant(self, user_id: int):
        """Добавление участника (синхронная логика)"""
        if self.participants is None:
            self.participants = []
        if user_id not in self.participants:
            self.participants.append(user_id)