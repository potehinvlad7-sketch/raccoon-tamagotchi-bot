from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def gender_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="male"), KeyboardButton(text="female")],
        ],
        resize_keyboard=True,
    )


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Status"), KeyboardButton(text="My Raccoon")],
            [KeyboardButton(text="Help")],
        ],
        resize_keyboard=True,
    )
