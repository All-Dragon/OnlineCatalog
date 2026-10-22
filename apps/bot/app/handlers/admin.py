import logging
from io import BytesIO

from aiogram import Bot, F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message
from httpx import HTTPStatusError

from app.clients.catalog import CatalogClient
from app.core.config import settings
from app.keyboards.catalog import CREATE_PRODUCT_TEXT, get_catalog_keyboard


logger = logging.getLogger(__name__)


admin_router = Router(name="admin")

MAX_PHOTO_BYTES = 5 * 1024 * 1024


@admin_router.message(Command("create"))
@admin_router.message(F.text == CREATE_PRODUCT_TEXT)
async def handle_create_command(message: Message) -> None:
    user = message.from_user

    if user is None:
        return

    if user.id != settings.telegram_admin_id:
        logger.info(
            "Denied product creation command: user_id=%s",
            user.id,
        )

        keyboard = None

        if message.chat.type == ChatType.PRIVATE:
            keyboard = get_catalog_keyboard(
                mini_app_url=str(settings.mini_app_url),
            )

        await message.answer(
            "У меня есть товар.\n\n"
            "Открой каталог, чтобы посмотреть товары.",
            reply_markup=keyboard,
        )
        return

    logger.debug(
        "Sending product creation instructions: user_id=%s",
        user.id,
    )

    await message.answer(
        "Отправь фотографию товара и его название "
        "в подписи одним сообщением."
    )


@admin_router.message(F.photo)
async def handle_product_photo(
    message: Message,
    bot: Bot,
    catalog_client: CatalogClient,
) -> None:
    user = message.from_user

    if user is None:
        return

    if user.id != settings.telegram_admin_id:
        logger.info(
            "Denied product photo: user_id=%s",
            user.id,
        )
        keyboard = None

        if message.chat.type == ChatType.PRIVATE:
            keyboard = get_catalog_keyboard(
                mini_app_url=str(settings.mini_app_url),
            )

        await message.answer(
            "У меня есть товар.\n\n"
            "Открой каталог, чтобы посмотреть товары.",
            reply_markup=keyboard,
        )
        return

    title = (message.caption or "").strip()

    if not title or len(title) > 255:
        await message.answer(
            "Добавь название в подпись к фотографии: "
            "от 1 до 255 символов."
        )
        return

    if not message.photo:
        return

    photo = max(
        message.photo,
        key=lambda item: item.width * item.height,
    )

    if photo.file_size is not None and photo.file_size > MAX_PHOTO_BYTES:
        await message.answer("Размер фотографии не должен превышать 5 МиБ.")
        return

    with BytesIO() as buffer:
        await bot.download(
            photo,
            destination=buffer,
            timeout=15,
        )
        photo_data = buffer.getvalue()

    if len(photo_data) > MAX_PHOTO_BYTES:
        await message.answer("Размер фотографии не должен превышать 5 МиБ.")
        return

    try:
        product = await catalog_client.create_product(
            title=title,
            source_chat_id=message.chat.id,
            source_message_id=message.message_id,
            photo=photo_data,
        )
    except HTTPStatusError as error:
        if error.response.status_code not in {413, 415, 422}:
            raise

        logger.info(
            "API rejected product input: chat_id=%s message_id=%s status=%s",
            message.chat.id,
            message.message_id,
            error.response.status_code,
        )

        await message.answer(
            "Не удалось принять товар. Проверь название и фотографию "
            "и отправь их одним новым сообщением."
        )
        return

    logger.info(
        "Product accepted: product_id=%s chat_id=%s message_id=%s",
        product.id,
        message.chat.id,
        message.message_id,
    )

    await message.answer(f"Товар сохранён. ID: {product.id}")
