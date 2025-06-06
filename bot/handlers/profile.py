# VelosocialBot/handlers/profile.py
import os
import json
import logging
from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db import get_connection

router = Router()
logger = logging.getLogger(__name__)
PROFILES_DIR = Path(__file__).parent.parent / "profiles"
os.makedirs(PROFILES_DIR, exist_ok=True)
MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5 MB


class ProfileStates(StatesGroup):
    PHOTO = State()
    BIKE_TYPE = State()
    SKILL_LEVEL = State()
    BIO = State()
    CONTACTS = State()


@router.message(Command("profile"))
async def profile_setup(message: Message, state: FSMContext) -> None:
    """Инициализация создания профиля"""
    try:
        await state.clear()
        await message.answer("📸 Пришлите фото для профиля (или /skip):")
        await state.set_state(ProfileStates.PHOTO)
    except Exception as e:
        logger.error(f"Ошибка в profile_setup: {e}", exc_info=True)
        await message.answer("⚠️ Ошибка инициализации профиля")


@router.message(ProfileStates.PHOTO, F.photo)
async def handle_photo(message: Message, state: FSMContext) -> None:
    """Обработка фотографии"""
    try:
        user = message.from_user
        await state.update_data(
            telegram_id=user.id,
            username=user.username or "Без имени"
        )

        # Получаем фото с максимальным разрешением
        largest_photo = max(message.photo, key=lambda p: p.file_size)

        # Проверка размера файла
        if (
            largest_photo.file_size
            and largest_photo.file_size > MAX_PHOTO_SIZE
        ):
            await message.answer(
                "❌ Фото слишком большое. Максимальный размер 5 МБ."
            )
            return

        photo_file = await message.bot.get_file(largest_photo.file_id)

        # Сохранение фото асинхронно
        photo_path = PROFILES_DIR / f"{user.id}.jpg"
        await message.bot.download_file(
            photo_file.file_path, destination=photo_path
        )
        await state.update_data(photo=str(photo_path))

        # Создаем клавиатуру для выбора типа велосипеда
        builder = InlineKeyboardBuilder()
        buttons = [
            ("Шоссе 🚴♂️", "road"),
            ("MTB 🏔", "mtb"),
            ("Городской 🏙", "city")
        ]
        for text, data in buttons:
            builder.button(text=text, callback_data=data)
        builder.adjust(2, 1)

        await message.answer(
            "🚲 Выберите тип велосипеда:",
            reply_markup=builder.as_markup(),
        )
        await state.set_state(ProfileStates.BIKE_TYPE)

    except Exception as e:
        logger.error(f"Ошибка в handle_photo: {e}", exc_info=True)
        await message.answer("⚠️ Ошибка обработки фото")


@router.message(ProfileStates.PHOTO, Command("skip"))
async def handle_skip_photo(message: Message, state: FSMContext) -> None:
    """Пропуск загрузки фото"""
    try:
        user = message.from_user
        await state.update_data(
            telegram_id=user.id,
            username=user.username or "Без имени",
            photo=None
        )

        # Создаем клавиатуру для выбора типа велосипеда
        builder = InlineKeyboardBuilder()
        buttons = [
            ("Шоссе 🚴♂️", "road"),
            ("MTB 🏔", "mtb"),
            ("Городской 🏙", "city")
        ]
        for text, data in buttons:
            builder.button(text=text, callback_data=data)
        builder.adjust(2, 1)

        await message.answer(
            "🚲 Выберите тип велосипеда:",
            reply_markup=builder.as_markup(),
        )
        await state.set_state(ProfileStates.BIKE_TYPE)
    except Exception as e:
        logger.error(f"Ошибка в handle_skip_photo: {e}", exc_info=True)
        await message.answer("⚠️ Ошибка при пропуске фото")


@router.callback_query(
    ProfileStates.BIKE_TYPE,
    F.data.in_({"road", "mtb", "city"}),
)
async def handle_bike_type(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработка типа велосипеда"""
    try:
        await state.update_data(bike_type=callback.data)

        # Создаем клавиатуру для выбора уровня подготовки
        builder = InlineKeyboardBuilder()
        buttons = [
            ("Начинающий 🌱", "beginner"),
            ("Любитель 🚴♀️", "intermediate"),
            ("Профи 🔥", "pro")
        ]
        for text, data in buttons:
            builder.button(text=text, callback_data=data)
        builder.adjust(2, 1)

        await callback.message.edit_text(
            text="📊 Укажите ваш уровень подготовки:",
            reply_markup=builder.as_markup()
        )
        await state.set_state(ProfileStates.SKILL_LEVEL)
    except Exception as e:
        logger.error(f"Ошибка в handle_bike_type: {e}", exc_info=True)
        await callback.answer("⚠️ Ошибка выбора типа")


@router.callback_query(
    ProfileStates.SKILL_LEVEL,
    F.data.in_({"beginner", "intermediate", "pro"}),
)
async def handle_skill_level(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Обработка уровня подготовки"""
    try:
        await state.update_data(skill_level=callback.data)
        await callback.message.edit_text(
            "✏️ Напишите краткое описание о себе (максимум 200 символов):"
        )
        await state.set_state(ProfileStates.BIO)
    except Exception as e:
        logger.error(f"Ошибка в handle_skill_level: {e}", exc_info=True)
        await callback.answer("⚠️ Ошибка выбора уровня")


@router.message(ProfileStates.BIO, F.text)
async def handle_bio(message: Message, state: FSMContext) -> None:
    """Обработка описания профиля"""
    try:
        await state.update_data(bio=message.text[:200])

        # Создаем клавиатуру для выбора контактов
        builder = InlineKeyboardBuilder()
        buttons = [
            ("Telegram", "telegram"),
            ("WhatsApp", "whatsapp")
        ]
        for text, data in buttons:
            builder.button(text=text, callback_data=data)

        await message.answer(
            "📱 Выберите контакты для связи:",
            reply_markup=builder.as_markup(),
        )
        await state.set_state(ProfileStates.CONTACTS)
    except Exception as e:
        logger.error(f"Ошибка в handle_bio: {e}", exc_info=True)
        await message.answer("⚠️ Ошибка ввода описания")


@router.callback_query(
    ProfileStates.CONTACTS,
    F.data.in_({"telegram", "whatsapp"}),
)
async def handle_contacts(callback: CallbackQuery, state: FSMContext) -> None:
    """Финализация создания профиля"""
    try:
        data = await state.get_data()
        logger.debug(f"Данные для сохранения: {data}")

        # Проверка обязательных полей
        required_fields = [
            "telegram_id",
            "username",
            "bike_type",
            "skill_level",
            "bio",
        ]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Отсутствует поле: {field}")

        # Формирование контактов
        user = callback.from_user
        contacts = {
            callback.data: user.username or user.full_name or "Не указан"
        }

        # Сохранение в БД
        conn = await get_connection()
        async with conn:
            await conn.execute('''
                INSERT INTO users (
                    telegram_id, username, bike_type, 
                    skill_level, bio, contacts
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(telegram_id) DO UPDATE SET
                    username = excluded.username,
                    bike_type = excluded.bike_type,
                    skill_level = excluded.skill_level,
                    bio = excluded.bio,
                    contacts = excluded.contacts
            ''', (
                data["telegram_id"],
                data["username"],
                data["bike_type"],
                data["skill_level"],
                data["bio"],
                json.dumps(contacts, ensure_ascii=False)
            ))
            await conn.commit()

        await callback.message.edit_text("✅ Профиль успешно сохранен!")

    except ValueError as e:
        logger.error(f"Ошибка валидации: {e}", exc_info=True)
        await callback.message.answer(f"❌ {str(e)}")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        await callback.message.answer("❌ Ошибка сохранения профиля")
    finally:
        await state.clear()
