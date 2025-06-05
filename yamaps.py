# VelosocialBot/utils/yamaps.py
from config import YANDEX_MAPS_API_KEY, MAP_SETTINGS

def generate_map(lat: float, lon: float, markers: list[str]) -> str:
    """
    Генерирует URL статической карты Яндекс с метками.
    (Функция остается синхронной, т.к. не требует асинхронных операций)

    :param lat: Широта центра карты
    :param lon: Долгота центра карты
    :param markers: Список меток в формате "долгота,широта,стиль"
    :return: URL изображения карты
    """
    base_url = "https://static-maps.yandex.ru/1.x/?"
    params = {
        "ll": f"{lon},{lat}",
        "z": MAP_SETTINGS["default_zoom"],
        "size": MAP_SETTINGS["map_size"],
        "l": "map",
        "pt": "~".join(markers),
        "apikey": YANDEX_MAPS_API_KEY
    }
    return f"{base_url}{'&'.join(f'{k}={v}' for k, v in params.items())}"
