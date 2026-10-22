from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo


CREATE_PRODUCT_TEXT = "Создать товар"


def get_catalog_keyboard(
    mini_app_url: str,
    *,
    is_admin: bool = False,
) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(
                text="Открыть каталог",
                web_app=WebAppInfo(url=mini_app_url),
            ),
        ],
    ]

    if is_admin:
        keyboard.append([KeyboardButton(text=CREATE_PRODUCT_TEXT)])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
