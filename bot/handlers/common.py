# VelosocialBot/handlers/common.py
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Обработчик команды /start"""
    try:
        await message.answer(
            "🚴♂️ Добро пожаловать в Velosocial!\n\n"
            "Я помогу вам найти компанию для велопрогулок.\n"
            "Используйте команды:\n"
            "/profile - создать/изменить профиль\n"
            "/find - найти велосипедистов рядом\n"
            "/create_event - организовать заезд\n"
            "/help - справка по командам"
        )
    except TelegramAPIError as e:
        logger.error(f"Ошибка в команде /start: {e}")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Обработчик команды /help"""
    try:
        await message.answer(
            "📋 Список доступных команд:\n\n"
            "/start - начать работу с ботом\n"
            "/profile - управление профилем\n"
            "/find - поиск велосипедистов и событий\n"
            "/create_event - создать новое событие\n"
            "/hide_me - скрыть мои геоданные\n"
            "/help - показать эту справку"
        )
    except TelegramAPIError as e:
        logger.error(f"Ошибка в команде /help: {e}")


@router.errors()
async def error_handler(event, exception: Exception) -> None:
    """Глобальный обработчик ошибок"""
    logger.error(
        msg="Ошибка при обработке запроса:",
        exc_info=exception
    )

    if event.message:
        try:
            await event.message.answer(
                "⚠️ Произошла непредвиденная ошибка. "
                "Попробуйте повторить действие позже."
            )
        except TelegramAPIError as e:
            logger.error(f"Ошибка при отправке сообщения об ошибке: {e}")
