# VelosocialBot/utils/filters.py
from typing import Optional, Tuple

# Допустимые значения для фильтров
BIKE_TYPES = {"road", "mtb", "city"}
SKILL_LEVELS = {"beginner", "intermediate", "pro"}

def build_user_filters(
    bike_type: Optional[str] = None,
    skill_level: Optional[str] = None
) -> Tuple[str, list]:
    """
    Генерирует SQL-условия для фильтрации пользователей.
    (Функция остается синхронной, не требует изменений)

    :param bike_type: Тип велосипеда ('road', 'mtb', 'city')
    :param skill_level: Уровень подготовки ('beginner', 'intermediate', 'pro')
    :return: Кортеж (SQL-условие, параметры)
    """
    conditions = []
    params = []

    if bike_type and bike_type in BIKE_TYPES:
        conditions.append("bike_type = ?")
        params.append(bike_type)

    if skill_level and skill_level in SKILL_LEVELS:
        conditions.append("skill_level = ?")
        params.append(skill_level)

    sql_condition = " AND ".join(conditions) if conditions else "1=1"
    return sql_condition, params


def validate_filter_params(
    bike_type: Optional[str],
    skill_level: Optional[str]
) -> bool:
    """
    Проверяет корректность параметров фильтрации.
    (Функция остается без изменений)

    :param bike_type: Тип велосипеда
    :param skill_level: Уровень подготовки
    :return: True если параметры валидны
    """
    valid_bike = bike_type in BIKE_TYPES.union({None})
    valid_skill = skill_level in SKILL_LEVELS.union({None})
    return valid_bike and valid_skill