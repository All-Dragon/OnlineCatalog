import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.core.config import settings
from app.keyboards.admin import get_admin_keyboard


logger = logging.getLogger(__name__)


start_router = Router(name="start")


@start_router.message(CommandStart())
async def handle_start(message: Message) -> None:
    logger.debug("Handling start: chat_id=%s", message.chat.id)

    keyboard = None

    if (
        message.from_user is not None
        and message.from_user.id == settings.telegram_admin_id
    ):
        keyboard = get_admin_keyboard()

    await message.answer(
        "У меня есть товар.\n\n"
        "Здесь можно посмотреть каталог товаров с названиями "
        "и фотографиями. Каталог открывается прямо в Telegram.\n\n"
        "Список команд и инструкция: /help",
        reply_markup=keyboard,
    )


@start_router.message(Command("help"))
async def handle_help(message: Message) -> None:
    logger.debug("Handling help: chat_id=%s", message.chat.id)

    text = (
        "Этот бот помогает просматривать каталог товаров.\n\n"
        "Команды:\n"
        "/start - приветствие и переход к каталогу\n"
        "/help - справка о боте\n\n"
        "Для просмотра каталога регистрация не требуется."
    )

    if (
        message.from_user is not None
        and message.from_user.id == settings.telegram_admin_id
    ):
        text += (
            "\n\nДля администратора:\n"
            "/create - инструкция по добавлению товара\n\n"
            "Отправь фотографию и название в подписи "
            "одним сообщением."
        )

    await message.answer(text)
