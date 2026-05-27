from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from storage import get_shop_categories

BTN_STATUS = "📊 Статус"
BTN_CARE = "⚔️ Магия и меч"
BTN_TRAINING = "💪 Тренировки"
BTN_MAGIC = "✨ Магия"
BTN_POTIONS = "🧪 Зелья"
BTN_SKILLS = "📊 Навыки"
BTN_TRAVEL = "🌲 Путешествие"
BTN_SHOP = "🛒 Магазин"
BTN_INVENTORY = "🎒 Инвентарь"
BTN_MY_RACCOON = "🦝 Мой енот"
BTN_HELP = "❔ Помощь"
BTN_CONTACT_ADMIN = "📨 Написать админу"
BTN_LETTER_TO_RACCOON = "💌 Дать енотику письмо"
BTN_CANCEL = "❌ Отмена"
BTN_BACK = "⬅️ В главное меню"
BTN_SHOP_BACK = "⬅️ Назад"
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
BTN_CARE_SLEEP = "😴 Сон"

BTN_TRAIN_STRENGTH = "💪 Сила"
BTN_TRAIN_AGILITY = "💨 Ловкость"
BTN_TRAIN_INSTINCT = "🌙 Инстинкт"



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
            [KeyboardButton(text=BTN_MY_RACCOON)],
            [KeyboardButton(text=BTN_HELP)],
            [KeyboardButton(text=BTN_LETTER_TO_RACCOON)],
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
            [KeyboardButton(text=BTN_CARE_SLEEP)],
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


def magic_and_sword_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_TRAINING), KeyboardButton(text=BTN_POTIONS)],
            [KeyboardButton(text=BTN_MAGIC), KeyboardButton(text=BTN_SKILLS)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )


def magic_and_sword_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=BTN_TRAINING, callback_data="magic_sword:train"),
                InlineKeyboardButton(text=BTN_POTIONS, callback_data="magic_sword:potions"),
            ],
            [
                InlineKeyboardButton(text=BTN_MAGIC, callback_data="magic_sword:magic"),
                InlineKeyboardButton(text=BTN_SKILLS, callback_data="magic_sword:skills"),
            ],
            [InlineKeyboardButton(text=BTN_BACK, callback_data="magic_sword:main")],
        ]
    )


def magic_training_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💪 Сила", callback_data="magic_train:strength"),
                InlineKeyboardButton(text="🐾 Ловкость", callback_data="magic_train:agility"),
            ],
            [InlineKeyboardButton(text="👁 Инстинкт", callback_data="magic_train:instinct")],
            [InlineKeyboardButton(text=BTN_BACK, callback_data="magic_train:back")],
        ]
    )


def magic_potions_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ Малое зелье", callback_data="magic_potion:small_energy"),
                InlineKeyboardButton(text="🔋 Большое зелье", callback_data="magic_potion:large_energy"),
            ],
            [InlineKeyboardButton(text=BTN_BACK, callback_data="magic_potion:back")],
        ]
    )


def magic_single_back_inline_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=BTN_BACK, callback_data=callback_data)]])


def build_shop_keyboard() -> ReplyKeyboardMarkup:
    categories = list(get_shop_categories().values())
    rows: list[list[KeyboardButton]] = []
    for idx in range(0, len(categories), 2):
        chunk = categories[idx:idx + 2]
        rows.append([KeyboardButton(text=f"{category.get('emoji', '🛒')} {category.get('title', 'Категория')}") for category in chunk])
    rows.append([KeyboardButton(text=BTN_SHOP_BACK)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def build_buy_button(item_id: str, item_name: str, item_emoji: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=f"Купить {item_emoji} {item_name}", callback_data=f"shop_buy:{item_id}")


def build_shop_item_keyboard(category_id: str, items: list[dict]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for item in items:
        item_id = str(item.get("id", "")).strip()
        if not item_id:
            continue
        item_name = str(item.get("name", "Предмет"))
        item_emoji = str(item.get("emoji", "🛒"))
        rows.append([build_buy_button(item_id, item_name, item_emoji)])
    rows.append([InlineKeyboardButton(text="⬅️ Категории", callback_data=f"shop_back:{category_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def pet_care_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🍗 Покормить", callback_data="pet_care:feed"),
                InlineKeyboardButton(text="🧼 Помыть", callback_data="pet_care:clean"),
            ],
            [
                InlineKeyboardButton(text="💖 Поиграть", callback_data="pet_care:play"),
                InlineKeyboardButton(text="😴 Сон", callback_data="pet_care:sleep"),
            ],
            [InlineKeyboardButton(text="🔙 В меню", callback_data="pet_care:menu")],
        ]
    )


def cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_CANCEL)]],
        resize_keyboard=True,
    )
