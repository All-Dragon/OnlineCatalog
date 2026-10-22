import logging

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.types import Message

from app.core.config import settings
from app.keyboards.catalog import get_catalog_keyboard


logger = logging.getLogger(__name__)

fallback_router = Router(name="fallback")


@fallback_router.message(F.chat.type == ChatType.PRIVATE)
async def handle_regular_message(message: Message) -> None:
    logger.debug(
        "Sending catalog invitation: chat_id=%s",
        message.chat.id,
    )

    is_admin = (
        message.from_user is not None
        and message.from_user.id == settings.telegram_admin_id
    )

    await message.answer(
        "У меня есть товар.\n\n"
        "Нажми «Открыть каталог», чтобы посмотреть товары.",
        reply_markup=get_catalog_keyboard(
            mini_app_url=str(settings.mini_app_url),
            is_admin=is_admin,
        ),
    )
