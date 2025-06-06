# VelosocialBot/utils/filters.py
from typing import Optional, Tuple

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

    if bike_type and bike_type in {'road', 'mtb', 'city'}:
        conditions.append("bike_type = ?")
        params.append(bike_type)

    if skill_level and skill_level in {'beginner', 'intermediate', 'pro'}:
        conditions.append("skill_level = ?")
        params.append(skill_level)

    sql_condition = " AND ".join(conditions) if conditions else "1=1"
    return sql_condition, params


def build_search_query(
    bbox: Tuple[float, float, float, float],
    bike_type: Optional[str] = None,
    skill_level: Optional[str] = None,
    limit: int = 5,
    offset: int = 0,
) -> Tuple[str, list]:
    """Формирует SELECT-запрос для поиска пользователей.

    Все значения подставляются через плейсхолдеры, чтобы избежать SQL-инъекций.

    :param bbox: Границы поиска (lat_min, lat_max, lon_min, lon_max)
    :param bike_type: Тип велосипеда
    :param skill_level: Уровень подготовки
    :param limit: Количество записей
    :param offset: Смещение для постраничного вывода
    :return: Кортеж (SQL-запрос, параметры)
    """

    query_parts = [
        "SELECT * FROM users",
        "WHERE is_visible = 1",
        "AND lat BETWEEN ? AND ?",
        "AND lon BETWEEN ? AND ?",
    ]
    params = list(bbox)

    if bike_type and bike_type in {"road", "mtb", "city"}:
        query_parts.append("AND bike_type = ?")
        params.append(bike_type)

    if skill_level and skill_level in {"beginner", "intermediate", "pro"}:
        query_parts.append("AND skill_level = ?")
        params.append(skill_level)

    query_parts.append("LIMIT ?")
    query_parts.append("OFFSET ?")
    params.extend([limit, offset])

    return "\n".join(query_parts), params


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
    valid_bike = bike_type in {None, 'road', 'mtb', 'city'}
    valid_skill = skill_level in {None, 'beginner', 'intermediate', 'pro'}
    return valid_bike and valid_skill
