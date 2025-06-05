from services.yamaps import generate_map
from bot.handlers.map import calculate_bbox
from config import MAP_SETTINGS, YANDEX_MAPS_API_KEY


def test_generate_map_url():
    lat, lon = 55.75, 37.61
    markers = [f"{lon},{lat},{MAP_SETTINGS['user_icon']}"]
    url = generate_map(lat, lon, markers)
    assert url.startswith("https://static-maps.yandex.ru/1.x/?")
    assert f"apikey={YANDEX_MAPS_API_KEY}" in url
    assert f"size={MAP_SETTINGS['map_size']}" in url


def test_calculate_bbox():
    bbox = calculate_bbox(10.0, 20.0, 5)
    delta = 5 / 111.0
    assert bbox == (10.0 - delta, 10.0 + delta, 20.0 - delta, 20.0 + delta)
