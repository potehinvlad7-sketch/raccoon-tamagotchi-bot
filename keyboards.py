from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from storage import get_shop_categories

BTN_STATUS = "📊 Статус"
BTN_MENU = "📋 Меню"
BTN_CARE = "❤️ Уход"
BTN_TRAINING = "💪 Тренировка"
BTN_TRAVEL = "🗺 Путешествие"
BTN_SHOP = "🏪 Магазин"
BTN_INVENTORY = "🎒 Инвентарь"
BTN_MY_RACCOON = "🦝 Мой енот"
BTN_HELP = "❔ Помощь"
BTN_CONTACT_ADMIN = "📨 Написать админу"
BTN_LETTER_TO_RACCOON = "✉️ Письмо"
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


TRAVEL_LOCATIONS = {
    "forest_clearing": {"button": "🌱 Лесная поляна", "name": "Лесная поляна", "min_level": 1},
    "quiet_thicket": {"button": "🌿 Тихая чаща", "name": "Тихая чаща", "min_level": 2},
    "mushroom_path": {"button": "🍄 Грибная тропа", "name": "Грибная тропа", "min_level": 3},
    "old_deadfall": {"button": "🪵 Старый бурелом", "name": "Старый бурелом", "min_level": 4},
    "misty_stream": {"button": "💧 Туманный ручей", "name": "Туманный ручей", "min_level": 5},
    "stone_ravine": {"button": "🪨 Каменный овраг", "name": "Каменный овраг", "min_level": 6},
    "forest_ruins": {"button": "🏚 Лесные руины", "name": "Лесные руины", "min_level": 7},
    "abandoned_watchhut": {"button": "🌲 Заброшенная сторожка", "name": "Заброшенная сторожка", "min_level": 8},
    "mossy_bridge": {"button": "🌉 Мшистый мост", "name": "Мшистый мост", "min_level": 9},
    "foxglove_meadow": {"button": "🌸 Лисья поляна", "name": "Лисья поляна", "min_level": 10},
    "hollow_stump_camp": {"button": "🪵 Лагерь в полом пне", "name": "Лагерь в полом пне", "min_level": 11},
    "glowing_mushroom_grove": {"button": "🍄 Светящийся грибной бор", "name": "Светящийся грибной бор", "min_level": 12},
    "silver_leaf_path": {"button": "🍃 Серебряная тропа", "name": "Серебряная тропа", "min_level": 13},
    "raven_crossing": {"button": "🐦‍⬛ Вороний переход", "name": "Вороний переход", "min_level": 14},
    "old_hunter_trail": {"button": "🏹 Старая охотничья тропа", "name": "Старая охотничья тропа", "min_level": 15},
    "sleepy_pine_hill": {"button": "🌲 Сонный сосновый холм", "name": "Сонный сосновый холм", "min_level": 16},
    "dewberry_lowland": {"button": "🫐 Ежевичная низина", "name": "Ежевичная низина", "min_level": 17},
    "foggy_swamp": {"button": "🌫 Туманное болото", "name": "Туманное болото", "min_level": 18},
    "frog_song_marsh": {"button": "🐸 Трясина жабьих песен", "name": "Трясина жабьих песен", "min_level": 19},
    "reed_maze": {"button": "🌾 Камышовый лабиринт", "name": "Камышовый лабиринт", "min_level": 20},
    "sunken_log_path": {"button": "🪵 Затонувшая тропа", "name": "Затонувшая тропа", "min_level": 21},
    "firefly_pool": {"button": "✨ Пруд светляков", "name": "Пруд светляков", "min_level": 22},
    "wet_root_tunnel": {"button": "🕳 Мокрый корневой лаз", "name": "Мокрый корневой лаз", "min_level": 23},
    "heron_shallows": {"button": "🪶 Цаплиные отмели", "name": "Цаплиные отмели", "min_level": 24},
    "stone_pass": {"button": "🪨 Каменный перевал", "name": "Каменный перевал", "min_level": 25},
    "windy_cliff_path": {"button": "🌬 Ветреная тропа", "name": "Ветреная тропа", "min_level": 26},
    "pebble_watch": {"button": "🪨 Галечный дозор", "name": "Галечный дозор", "min_level": 27},
    "goat_grass_slope": {"button": "🐐 Склон козьей травы", "name": "Склон козьей травы", "min_level": 28},
    "echoing_gully": {"button": "🔊 Эхо-лощина", "name": "Эхо-лощина", "min_level": 29},
    "cracked_boulder_gate": {"button": "🪨 Треснувшие валуны", "name": "Треснувшие валуны", "min_level": 30},
    "pine_needle_ridge": {"button": "🌲 Хребет хвойных игл", "name": "Хребет хвойных игл", "min_level": 31},
    "cloudberry_shelf": {"button": "☁️ Морошковый уступ", "name": "Морошковый уступ", "min_level": 32},
    "stormcrow_peak": {"button": "🐦‍⬛ Пик буревестников", "name": "Пик буревестников", "min_level": 33},
    "dry_stream_bed": {"button": "🏜 Сухое русло", "name": "Сухое русло", "min_level": 34},
    "old_settlement_ruins": {"button": "🏚 Руины старого поселения", "name": "Руины старого поселения", "min_level": 35},
    "overgrown_well": {"button": "🕳 Заросший колодец", "name": "Заросший колодец", "min_level": 36},
    "broken_cart_square": {"button": "🛞 Площадь сломанной телеги", "name": "Площадь сломанной телеги", "min_level": 37},
    "moss_roof_houses": {"button": "🏚 Дома под мхом", "name": "Дома под мхом", "min_level": 38},
    "forgotten_pantry": {"button": "🥫 Забытая кладовая", "name": "Забытая кладовая", "min_level": 39},
    "chimney_crow_roost": {"button": "🐦‍⬛ Вороньи трубы", "name": "Вороньи трубы", "min_level": 40},
    "cracked_chapel_yard": {"button": "🕯 Двор треснувшей часовни", "name": "Двор треснувшей часовни", "min_level": 41},
    "cellar_of_whispers": {"button": "🕳 Подвал шёпотов", "name": "Подвал шёпотов", "min_level": 42},
    "ivy_clock_tower": {"button": "🕰 Башня в плюще", "name": "Башня в плюще", "min_level": 43},
    "moonlit_mill": {"button": "🌙 Лунная мельница", "name": "Лунная мельница", "min_level": 44},
    "starry_thicket": {"button": "🌌 Звёздная чаща", "name": "Звёздная чаща", "min_level": 45},
    "firefly_constellation_path": {"button": "✨ Тропа светлячных созвездий", "name": "Тропа светлячных созвездий", "min_level": 46},
    "silver_moth_glade": {"button": "🦋 Поляна серебряных мотыльков", "name": "Поляна серебряных мотыльков", "min_level": 47},
    "night_bloom_garden": {"button": "🌺 Ночной цветник", "name": "Ночной цветник", "min_level": 48},
    "owl_mirror_lake": {"button": "🦉 Зеркальное озеро сов", "name": "Зеркальное озеро сов", "min_level": 49},
    "comet_fallen_clearing": {"button": "☄️ Поляна упавшей кометы", "name": "Поляна упавшей кометы", "min_level": 50},
    "whispering_fern_field": {"button": "🌿 Поле шепчущих папоротников", "name": "Поле шепчущих папоротников", "min_level": 51},
    "blue_moon_copse": {"button": "🔵 Роща синей луны", "name": "Роща синей луны", "min_level": 52},
    "astral_burrow": {"button": "🌠 Звёздная нора", "name": "Звёздная нора", "min_level": 53},
    "lanternroot_path": {"button": "🏮 Тропа фонарных корней", "name": "Тропа фонарных корней", "min_level": 54},
    "underground_roots": {"button": "🕯 Подземные корни", "name": "Подземные корни", "min_level": 55},
    "root_cathedral": {"button": "⛪ Корневой собор", "name": "Корневой собор", "min_level": 56},
    "blind_mole_tunnels": {"button": "🕳 Тоннели слепых кротов", "name": "Тоннели слепых кротов", "min_level": 57},
    "amber_resin_caves": {"button": "🟠 Янтарные пещеры", "name": "Янтарные пещеры", "min_level": 58},
    "fossil_nest": {"button": "🦴 Ископаемое гнездо", "name": "Ископаемое гнездо", "min_level": 59},
    "deep_moss_chamber": {"button": "🌿 Глубокая моховая зала", "name": "Глубокая моховая зала", "min_level": 60},
    "echo_root_maze": {"button": "🔊 Лабиринт эхо-корней", "name": "Лабиринт эхо-корней", "min_level": 61},
    "buried_stream": {"button": "💧 Погребённый ручей", "name": "Погребённый ручей", "min_level": 62},
    "stone_seed_vault": {"button": "🪨 Хранилище каменных семян", "name": "Хранилище каменных семян", "min_level": 63},
    "sleeping_earth_heart": {"button": "🫀 Спящее сердце земли", "name": "Спящее сердце земли", "min_level": 64},
    "giants_graveyard": {"button": "🦴 Кладбище великанов", "name": "Кладбище великанов", "min_level": 65},
    "rib_bone_valley": {"button": "🦴 Долина рёбер", "name": "Долина рёбер", "min_level": 66},
    "skull_hill": {"button": "💀 Черепной холм", "name": "Черепной холм", "min_level": 67},
    "mammoth_moss_field": {"button": "🦣 Мамонтово моховое поле", "name": "Мамонтово моховое поле", "min_level": 68},
    "bone_wind_passage": {"button": "🌬 Костяной проход ветров", "name": "Костяной проход ветров", "min_level": 69},
    "giant_finger_bridge": {"button": "🦴 Мост пальца великана", "name": "Мост пальца великана", "min_level": 70},
    "ancient_battlefield": {"button": "⚔️ Древнее поле битвы", "name": "Древнее поле битвы", "min_level": 71},
    "white_antler_grove": {"button": "🦌 Роща белых рогов", "name": "Роща белых рогов", "min_level": 72},
    "hollow_bone_caves": {"button": "🦴 Полые костяные пещеры", "name": "Полые костяные пещеры", "min_level": 73},
    "last_giant_camp": {"button": "🔥 Последний лагерь великана", "name": "Последний лагерь великана", "min_level": 74},
    "forgotten_raccoon_castle": {"button": "🏰 Забытый енотовый замок", "name": "Забытый енотовый замок", "min_level": 75},
    "tailguard_gate": {"button": "🦝 Врата хвостатой стражи", "name": "Врата хвостатой стражи", "min_level": 76},
    "dusty_banner_hall": {"button": "🏳️ Пыльный зал знамён", "name": "Пыльный зал знамён", "min_level": 77},
    "moon_key_corridor": {"button": "🗝 Лунный коридор ключей", "name": "Лунный коридор ключей", "min_level": 78},
    "cracked_throne_room": {"button": "👑 Треснувший тронный зал", "name": "Треснувший тронный зал", "min_level": 79},
    "pantry_of_kings": {"button": "🍯 Королевская кладовая", "name": "Королевская кладовая", "min_level": 80},
    "armor_rat_barracks": {"button": "🛡 Казармы бронекрысов", "name": "Казармы бронекрысов", "min_level": 81},
    "knight_raccoon_gallery": {"button": "🖼 Галерея енотов-рыцарей", "name": "Галерея енотов-рыцарей", "min_level": 82},
    "silver_crown_tower": {"button": "👑 Башня серебряной короны", "name": "Башня серебряной короны", "min_level": 83},
    "royal_burrow_keep": {"button": "🏰 Королевская нора-крепость", "name": "Королевская нора-крепость", "min_level": 84},
    "black_grove": {"button": "🌑 Чёрная роща", "name": "Чёрная роща", "min_level": 85},
    "shadow_birch_path": {"button": "🌑 Тропа теневых берёз", "name": "Тропа теневых берёз", "min_level": 86},
    "cursed_acorn_field": {"button": "🌰 Поле проклятых желудей", "name": "Поле проклятых желудей", "min_level": 87},
    "silent_owl_court": {"button": "🦉 Суд безмолвных сов", "name": "Суд безмолвных сов", "min_level": 88},
    "thornmoon_thicket": {"button": "🌙 Терновая чаща луны", "name": "Терновая чаща луны", "min_level": 89},
    "black_sap_swamp": {"button": "🖤 Болото чёрной смолы", "name": "Болото чёрной смолы", "min_level": 90},
    "hollow_shadow_den": {"button": "🕳 Логово пустой тени", "name": "Логово пустой тени", "min_level": 91},
    "eclipse_root_circle": {"button": "🌘 Круг корней затмения", "name": "Круг корней затмения", "min_level": 92},
    "dead_star_clearing": {"button": "✴️ Поляна мёртвой звезды", "name": "Поляна мёртвой звезды", "min_level": 93},
    "night_crown_forest": {"button": "👑 Лес ночной короны", "name": "Лес ночной короны", "min_level": 94},
    "path_of_legends": {"button": "👑 Тропа легенд", "name": "Тропа легенд", "min_level": 95},
    "first_legend_step": {"button": "✨ Первый шаг легенды", "name": "Первый шаг легенды", "min_level": 96},
    "elder_tail_shrine": {"button": "🦝 Святилище старшего хвоста", "name": "Святилище старшего хвоста", "min_level": 97},
    "skyroot_summit": {"button": "🌌 Вершина небесных корней", "name": "Вершина небесных корней", "min_level": 98},
    "gate_before_legend": {"button": "🚪 Врата перед легендой", "name": "Врата перед легендой", "min_level": 99},
    "raccoon_legend_throne": {"button": "👑 Трон легендарного енота", "name": "Трон легендарного енота", "min_level": 100},
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
            [KeyboardButton(text=BTN_MY_RACCOON), KeyboardButton(text=BTN_MENU)],
            [KeyboardButton(text=BTN_TRAVEL), KeyboardButton(text=BTN_LETTER_TO_RACCOON)],
        ],
        resize_keyboard=True,
    )


def main_inline_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BTN_MY_RACCOON, callback_data="menu:pet")],
            [InlineKeyboardButton(text=BTN_CARE, callback_data="menu:care")],
            [InlineKeyboardButton(text=BTN_TRAVEL, callback_data="menu:travel")],
            [InlineKeyboardButton(text=BTN_INVENTORY, callback_data="menu:inventory")],
            [InlineKeyboardButton(text=BTN_SHOP, callback_data="menu:shop")],
            [InlineKeyboardButton(text=BTN_TRAINING, callback_data="menu:train")],
            [InlineKeyboardButton(text=BTN_LETTER_TO_RACCOON, callback_data="menu:letter")],
        ],
    )


def care_inline_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍗 Покормить", callback_data="care:feed")],
            [InlineKeyboardButton(text="🧼 Помыть", callback_data="care:clean")],
            [InlineKeyboardButton(text="💖 Поиграть", callback_data="care:play")],
            [InlineKeyboardButton(text=BTN_CARE_SLEEP, callback_data="care:sleep")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:main")],
        ],
    )


def shop_inline_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍗 Еда", callback_data="shop:food")],
            [InlineKeyboardButton(text="🧴 Хозмаг", callback_data="shop:household")],
            [InlineKeyboardButton(text="🧸 Игрушки", callback_data="shop:toys")],
            [InlineKeyboardButton(text="🧪 Зелья", callback_data="shop:potions")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:main")],
        ],
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
    rows.append([InlineKeyboardButton(text="⬅️ Категории", callback_data="menu:shop")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_CANCEL)]],
        resize_keyboard=True,
    )
