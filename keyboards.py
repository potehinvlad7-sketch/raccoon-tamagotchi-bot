from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

BTN_STATUS = "📊 Статус"
BTN_CARE = "🧼 Уход"
BTN_TRAINING = "💪 Тренировки"
BTN_TRAVEL = "🌲 Путешествие"
BTN_SHOP = "🛒 Магазин"
BTN_INVENTORY = "🎒 Инвентарь"
BTN_MY_RACCOON = "🦝 Мой енот"
BTN_HELP = "❔ Помощь"
BTN_BACK = "⬅️ В главное меню"
BTN_BATTLE_ATTACK = "⚔️ Атаковать"
BTN_BATTLE_RUN = "🏃 Сбежать"

BTN_GENDER_MALE = "♂️ Мальчик"
BTN_GENDER_FEMALE = "♀️ Девочка"

BTN_CARE_APPLE = "🍎 Яблоко"
BTN_CARE_HEARTY_SNACK = "🥪 Сытный перекус"
BTN_CARE_FOREST_HONEY = "🍯 Лесной мёд"
BTN_CARE_SOAP = "🧼 Мыло"
BTN_CARE_SHAMPOO = "🫧 Шампунь"
BTN_CARE_COMB = "🪮 Гребень"
BTN_CARE_BALL = "🎾 Мячик"
BTN_CARE_YARN_BALL = "🧶 Клубок"
BTN_CARE_FUN_TOY = "🪀 Игрушка"
BTN_CARE_SMALL_ENERGY = "⚡ Малое зелье"
BTN_CARE_BIG_ENERGY = "🔋 Большое зелье"

BTN_TRAIN_STRENGTH = "💪 Сила"
BTN_TRAIN_AGILITY = "💨 Ловкость"
BTN_TRAIN_INSTINCT = "🌙 Инстинкт"


TRAVEL_LOCATIONS = {
    "forest_clearing": {"button": "🌿 Лесная поляна", "name": "Лесная поляна", "min_level": 1},
    "quiet_thicket": {"button": "🌲 Тихая чаща", "name": "Тихая чаща", "min_level": 1},
    "mushroom_path": {"button": "🍄 Грибная тропа", "name": "Грибная тропа", "min_level": 2},
    "old_deadfall": {"button": "🪵 Старый бурелом", "name": "Старый бурелом", "min_level": 3},
    "misty_stream": {"button": "💧 Туманный ручей", "name": "Туманный ручей", "min_level": 5},
    "stone_ravine": {"button": "🪨 Каменный овраг", "name": "Каменный овраг", "min_level": 7},
    "forest_ruins": {"button": "🏚 Лесные руины", "name": "Лесные руины", "min_level": 10},
}


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


def travel_menu_keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    rows: list[list[KeyboardButton]] = []
    for idx in range(0, len(buttons), 2):
        chunk = buttons[idx:idx + 2]
        rows.append([KeyboardButton(text=item) for item in chunk])
    rows.append([KeyboardButton(text=BTN_BACK)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def battle_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_BATTLE_ATTACK), KeyboardButton(text=BTN_BATTLE_RUN)],
        ],
        resize_keyboard=True,
    )


def care_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_CARE_APPLE), KeyboardButton(text=BTN_CARE_HEARTY_SNACK), KeyboardButton(text=BTN_CARE_FOREST_HONEY)],
            [KeyboardButton(text=BTN_CARE_SOAP), KeyboardButton(text=BTN_CARE_SHAMPOO), KeyboardButton(text=BTN_CARE_COMB)],
            [KeyboardButton(text=BTN_CARE_BALL), KeyboardButton(text=BTN_CARE_YARN_BALL), KeyboardButton(text=BTN_CARE_FUN_TOY)],
            [KeyboardButton(text=BTN_CARE_SMALL_ENERGY), KeyboardButton(text=BTN_CARE_BIG_ENERGY)],
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


def shop_categories_inline_keyboard(categories: list[dict]) -> object:
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(
            text=f"{category.get('emoji', '🛒')} {category.get('title', 'Категория')}",
            callback_data=f"shop:category:{category.get('id', '')}",
        )
    builder.button(text="⬅️ Назад", callback_data="shop:back:main")
    builder.adjust(2, 1)
    return builder.as_markup()


def shop_items_inline_keyboard(category_id: str, items: list[dict]) -> object:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=f"{item.get('name', 'Предмет')} — {item.get('price', 0)} 🪙", callback_data=f"shop:buy:{item.get('id', '')}")
    builder.button(text="⬅️ Категории", callback_data="shop:back:categories")
    builder.button(text="🏠 Главное меню", callback_data="shop:back:main")
    builder.adjust(1, 1, 1)
    return builder.as_markup()
