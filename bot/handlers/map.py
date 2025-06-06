# VelosocialBot/handlers/map.py
import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import MAP_SETTINGS
from database.db import get_connection
from services.maps import generate_map
from services.geocoder import address_to_coords
from bot.utils.filters import build_search_query
from typing import Tuple, cast

router = Router()
logger = logging.getLogger(__name__)

# Константы для кнопок
ACTION_SEARCH = "search"
ACTION_FILTERS = "filters"
ACTION_REFRESH = "refresh"


@router.message(Command("find"))
async def handle_find(message: Message) -> None:
    """Обработчик команды /find"""
    try:
        builder = InlineKeyboardBuilder()
        builder.button(text="📍 По геолокации",
                       callback_data=f"{ACTION_SEARCH}:geo")
        builder.button(text="🏠 По адресу",
                       callback_data=f"{ACTION_SEARCH}:address")
        await message.answer(
            "🔍 Выберите способ поиска:",
            reply_markup=builder.as_markup(),
        )
    except Exception as e:
        logger.error(f"Ошибка в handle_find: {str(e)}")


@router.callback_query(F.data.startswith(f"{ACTION_SEARCH}:"))
async def handle_search(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработка выбора метода поиска"""
    try:
        method = callback.data.split(":")[1]
        await state.update_data(
            search_method=method,
            page=1,
            page_size=5,
        )

        if method == "geo":
            await callback.message.edit_text(
                "📍 Отправьте вашу геолокацию (кнопка в меню ввода)"
            )
        elif method == "address":
            await callback.message.edit_text(
                "🏠 Введите адрес (пример: Москва, Парк Горького)"
            )

        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка в handle_search: {str(e)}")


@router.message(F.location)
async def handle_geo_location(message: Message, state: FSMContext) -> None:
    """Обработка геолокации"""
    data = await state.get_data()
    if data.get("search_method") != "geo":
        return

    lat = message.location.latitude
    lon = message.location.longitude
    await process_search(message, state, lat, lon)


@router.message(F.text)
async def handle_text_address(message: Message, state: FSMContext) -> None:
    """Обработка текстового адреса"""
    data = await state.get_data()
    if data.get("search_method") != "address":
        return

    coords = await address_to_coords(message.text)
    if not coords:
        await message.answer("❌ Адрес не найден")
        return

    await process_search(message, state, *coords)


async def process_search(
    message: Message,
    state: FSMContext,
    lat: float,
    lon: float,
) -> None:
    """Основная логика поиска"""
    try:
        data = await state.get_data()
        filters = data.get("filters", {})
        page = int(data.get("page", 1))
        page_size = int(data.get("page_size", 5))
        offset = (page - 1) * page_size

        conn = await get_connection()
        async with conn:
            cursor = await conn.cursor()
            radius_km = cast(int, MAP_SETTINGS["max_distance_km"])
            bbox = calculate_bbox(lat, lon, radius_km)
            query, q_params = build_search_query(
                bbox,
                bike_type=filters.get("bike_type"),
                skill_level=filters.get("skill_level"),
                limit=page_size,
                offset=offset,
            )

            await cursor.execute(query, q_params)

            users = await cursor.fetchall()

        markers = [
            f"{user[8]},{user[7]},{MAP_SETTINGS['others_icon']}"
            for user in users
        ]
        markers.append(f"{lon},{lat},{MAP_SETTINGS['user_icon']}")
        map_url = generate_map(lat, lon, markers)

        response = f"🚴 Найдено: {len(users)} велосипедистов\n"
        start_idx = offset + 1
        for idx, user in enumerate(users, start=start_idx):
            response += f"{idx}. {user[2]} ({user[3]})\n"

        builder = InlineKeyboardBuilder()
        builder.button(text="⚙️ Фильтры", callback_data=ACTION_FILTERS)
        builder.button(text="🔄 Обновить", callback_data=ACTION_REFRESH)

        if message.photo:
            await message.edit_media(
                InputMediaPhoto(media=map_url, caption=response)
            )
            await message.edit_reply_markup(
                reply_markup=builder.as_markup()
            )
        else:
            await message.answer_photo(
                photo=map_url,
                caption=response,
                reply_markup=builder.as_markup(),
            )

    except Exception as e:
        logger.error(f"Ошибка в process_search: {str(e)}")


@router.callback_query(F.data == ACTION_FILTERS)
async def handle_filters(callback: CallbackQuery) -> None:
    """Управление фильтрами"""
    try:
        builder = InlineKeyboardBuilder()
        builder.button(text="Тип велосипеда ▼",
                       callback_data="filter:bike_type")
        builder.button(text="Уровень подготовки ▼",
                       callback_data="filter:skill_level")
        builder.button(text="✅ Применить", callback_data="filter:apply")
        builder.adjust(1, 1, 1)

        await callback.message.edit_reply_markup(
            reply_markup=builder.as_markup()
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка в handle_filters: {str(e)}")


def calculate_bbox(lat: float, lon: float,
                   radius_km: int) -> Tuple[float, float, float, float]:
    """Рассчет границ поиска (без изменений)"""
    delta = radius_km / 111.0
    return (lat - delta, lat + delta, lon - delta, lon + delta)
