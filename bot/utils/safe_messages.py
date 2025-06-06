import logging
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError

logger = logging.getLogger(__name__)

async def safe_answer(message: Message, *args, **kwargs) -> bool:
    """Safely send a reply to the user.

    Logs any TelegramAPIError that occurs during message delivery.
    Returns True if the message was successfully sent, False otherwise.
    """
    try:
        await message.answer(*args, **kwargs)
        return True
    except TelegramAPIError as e:
        logger.error(f"Message delivery failed: {e}", exc_info=True)
        return False
