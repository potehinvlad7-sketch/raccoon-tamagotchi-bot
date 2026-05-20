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
            [KeyboardButton(text="Status"), KeyboardButton(text="Care")],
            [KeyboardButton(text="Training"), KeyboardButton(text="Travel")],
            [KeyboardButton(text="My Raccoon"), KeyboardButton(text="Help")],
        ],
        resize_keyboard=True,
    )


def travel_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Short Forest Trip")],
            [KeyboardButton(text="Back to main menu")],
        ],
        resize_keyboard=True,
    )


def care_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Feed"), KeyboardButton(text="Clean")],
            [KeyboardButton(text="Play"), KeyboardButton(text="Energy potion")],
            [KeyboardButton(text="Back to main menu")],
        ],
        resize_keyboard=True,
    )


def training_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Train Strength"), KeyboardButton(text="Train Agility")],
            [KeyboardButton(text="Train Instinct")],
            [KeyboardButton(text="Back to main menu")],
        ],
        resize_keyboard=True,
    )
