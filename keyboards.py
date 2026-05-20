from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

BTN_STATUS = "📊 Статус"
BTN_CARE = "🧼 Уход"
BTN_TRAINING = "💪 Тренировки"
BTN_TRAVEL = "🌲 Путешествие"
BTN_SHOP = "🛒 Магазин"
BTN_INVENTORY = "🎒 Инвентарь"
BTN_MY_RACCOON = "🦝 Мой енот"
BTN_HELP = "❔ Помощь"
BTN_BACK = "⬅️ В главное меню"

BTN_GENDER_MALE = "♂️ Мальчик"
BTN_GENDER_FEMALE = "♀️ Девочка"

BTN_FEED = "🍎 Покормить"
BTN_CLEAN = "🧼 Почистить"
BTN_PLAY = "🎾 Поиграть"
BTN_ENERGY = "⚡ Зелье энергии"

BTN_TRAIN_STRENGTH = "💪 Сила"
BTN_TRAIN_AGILITY = "💨 Ловкость"
BTN_TRAIN_INSTINCT = "🌙 Инстинкт"

BTN_TRIP_FOREST = "🌲 Короткая прогулка в лес"

BTN_BUY_FOOD = "🍎 Купить еду — 5 монет"
BTN_BUY_SOAP = "🧼 Купить мыло — 7 монет"
BTN_BUY_TOY = "🎾 Купить игрушку — 8 монет"
BTN_BUY_ENERGY = "⚡ Купить зелье энергии — 12 монет"


def gender_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_GENDER_MALE), KeyboardButton(text=BTN_GENDER_FEMALE)],
        ],
        resize_keyboard=True,
    )


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_STATUS), KeyboardButton(text=BTN_CARE)],
            [KeyboardButton(text=BTN_TRAINING), KeyboardButton(text=BTN_TRAVEL)],
            [KeyboardButton(text=BTN_SHOP), KeyboardButton(text=BTN_INVENTORY)],
            [KeyboardButton(text=BTN_MY_RACCOON), KeyboardButton(text=BTN_HELP)],
        ],
        resize_keyboard=True,
    )


def travel_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_TRIP_FOREST)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )


def care_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_FEED), KeyboardButton(text=BTN_CLEAN)],
            [KeyboardButton(text=BTN_PLAY), KeyboardButton(text=BTN_ENERGY)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )


def training_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_TRAIN_STRENGTH), KeyboardButton(text=BTN_TRAIN_AGILITY)],
            [KeyboardButton(text=BTN_TRAIN_INSTINCT)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )


def shop_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_BUY_FOOD), KeyboardButton(text=BTN_BUY_SOAP)],
            [KeyboardButton(text=BTN_BUY_TOY), KeyboardButton(text=BTN_BUY_ENERGY)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )
