# VelosocialBot/handlers/events.py
import logging
import json
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramAPIError
from database.db import get_connection
from bot.utils.safe_messages import safe_answer

router = Router()
logger = logging.getLogger(__name__)

# Limits for event participants
MIN_PARTICIPANTS = 2
MAX_PARTICIPANTS = 50


class EventCreation(StatesGroup):
    DESCRIPTION = State()
    ROUTE = State()
    DATE = State()
    PARTICIPANTS = State()


@router.message(Command("create_event"))
async def create_event(message: Message, state: FSMContext) -> None:
    """Инициализация создания события"""
    try:
        await state.clear()
        await safe_answer(
            message,
            "📝 Введите описание события (например: "
            "'Вечерний заезд по набережной'):"
        )
        await state.set_state(EventCreation.DESCRIPTION)
    except Exception as e:
        logger.error(f"Ошибка в create_event: {str(e)}")
        await safe_answer(message, "❌ Ошибка создания события")


@router.message(EventCreation.DESCRIPTION, F.text)
async def handle_event_description(
        message: Message,
        state: FSMContext) -> None:
    """Обработка описания события"""
    try:
        await state.update_data(description=message.text)
        await safe_answer(
            message,
            (
                "🗺️ Укажите маршрут (например: 'Москва, Парк Горького "
                "→ Воробьевы горы'):"
            )
        )
        await state.set_state(EventCreation.ROUTE)
    except Exception as e:
        logger.error(f"Ошибка в handle_event_description: {str(e)}")


@router.message(EventCreation.ROUTE, F.text)
async def handle_event_route(message: Message, state: FSMContext) -> None:
    """Обработка маршрута"""
    try:
        await state.update_data(route=message.text)
        await safe_answer(
            message,
            (
                "⏰ Введите дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ "
                "(например: 25.12.2024 18:30):"
            )
        )
        await state.set_state(EventCreation.DATE)
    except Exception as e:
        logger.error(f"Ошибка в handle_event_route: {str(e)}")


@router.message(EventCreation.DATE, F.text)
async def handle_event_date(message: Message, state: FSMContext) -> None:
    """Обработка даты и времени"""
    try:
        date_str = message.text
        event_date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")

        if event_date < datetime.now():
            await safe_answer(message, "❌ Дата не может быть в прошлом!")
            return

        await state.update_data(event_date=event_date.isoformat())
        await safe_answer(
            message,
            (
                "👥 Введите максимальное число участников "
                f"(от {MIN_PARTICIPANTS} до {MAX_PARTICIPANTS}):"
            ),
        )
        await state.set_state(EventCreation.PARTICIPANTS)

    except ValueError:
        await safe_answer(
            message,
            "❌ Неверный формат даты! Используйте ДД.ММ.ГГГГ ЧЧ:ММ",
        )
    except Exception as e:
        logger.error(f"Ошибка в handle_event_date: {str(e)}")


@router.message(EventCreation.PARTICIPANTS, F.text)
async def handle_event_participants(
        message: Message,
        state: FSMContext) -> None:
    """Финализация создания события"""
    try:
        max_participants = int(message.text)
        if not (MIN_PARTICIPANTS <= max_participants <= MAX_PARTICIPANTS):
            raise ValueError

        data = await state.get_data()

        # Создание группы
        try:
            chat = await message.bot.create_new_supergroup_chat(
                title=f"Заезд: {data['description'][:20]}",
                user_ids=[message.from_user.id]
            )
        except TelegramAPIError as e:
            logger.error(f"Ошибка создания чата: {e}", exc_info=True)
            await safe_answer(message, "❌ Не удалось создать чат")
            await state.clear()
            return

        try:
            invite = await message.bot.create_chat_invite_link(chat_id=chat.id)
            invite_link = invite.invite_link
        except TelegramAPIError as e:
            logger.error(f"Ошибка получения ссылки на чат: {e}", exc_info=True)
            await safe_answer(message, "❌ Не удалось создать ссылку на чат")
            await state.clear()
            return

        # Сохранение в БД
        conn = await get_connection()
        async with conn:
            await conn.execute('''
                INSERT INTO events (
                    creator_id, description, route,
                    event_date, max_participants, chat_id, participants
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                message.from_user.id,
                data['description'],
                data['route'],
                data['event_date'],
                max_participants,
                chat.id,
                json.dumps([message.from_user.id])
            ))
            await conn.commit()

        await safe_answer(
            message,
            f"✅ Событие создано!\nСсылка на чат: {invite_link}",
            disable_web_page_preview=True
        )
        await state.clear()

    except ValueError:
        await safe_answer(
            message,
            f"❌ Введите число от {MIN_PARTICIPANTS} до {MAX_PARTICIPANTS}!"
        )
    except Exception as e:
        logger.error(f"Ошибка в handle_event_participants: {str(e)}")
        await safe_answer(message, "❌ Ошибка создания события")
        await state.clear()


@router.message(Command("cancel"))
async def cancel_event_creation(message: Message, state: FSMContext) -> None:
    """Отмена создания события"""
    await safe_answer(message, "❌ Создание события отменено")
    await state.clear()
