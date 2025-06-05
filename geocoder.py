# VelosocialBot/utils/geocoder.py
import logging
import aiohttp
from typing import Optional, Tuple
from config import YANDEX_GEOCODER_API_KEY, GEOCODER_SETTINGS

logger = logging.getLogger(__name__)


async def address_to_coords(address: str) -> Optional[Tuple[float, float]]:
    """
    Асинхронное преобразование адреса в координаты через Yandex Geocoder API.

    :param address: Адрес для геокодирования
    :return: Кортеж (lat, lon) или None при ошибке
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://geocode-maps.yandex.ru/1.x/",
                    params={
                        "apikey": YANDEX_GEOCODER_API_KEY,
                        "geocode": address,
                        "format": "json",
                        "lang": GEOCODER_SETTINGS["lang"],
                        "results": GEOCODER_SETTINGS["results_limit"]
                    },
                    timeout=aiohttp.ClientTimeout(
                        total=GEOCODER_SETTINGS["timeout"]
                    )
            ) as response:
                if response.status != 200:
                    logger.error(f"Geocoder API error: {response.status}")
                    return None

                data = await response.json()
                feature = data["response"]["GeoObjectCollection"][
                    "featureMember"
                ][0]
                pos = feature["GeoObject"]["Point"]["pos"]
                lon, lat = map(float, pos.split())
                return (lat, lon)

    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logger.error(f"Geocoder request failed: {e}")
    except (KeyError, IndexError) as e:
        logger.error(f"Geocoder parsing error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    return None
