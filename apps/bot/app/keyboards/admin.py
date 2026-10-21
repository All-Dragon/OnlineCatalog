from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


CREATE_PRODUCT_TEXT = "Создать товар"


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=CREATE_PRODUCT_TEXT)],
        ],
        resize_keyboard=True,
    )
