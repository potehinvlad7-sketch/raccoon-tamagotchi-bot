from aiogram import F, Router
from aiogram.types import Message

from keyboards import (
    BTN_BACK,
    BTN_BUY_BIG_ENERGY,
    BTN_BUY_COMB,
    BTN_BUY_ENERGY,
    BTN_BUY_FOOD,
    BTN_BUY_FOREST_HONEY,
    BTN_BUY_FUN_TOY,
    BTN_BUY_HEARTY_SNACK,
    BTN_BUY_SHAMPOO,
    BTN_BUY_SOAP,
    BTN_BUY_TOY,
    BTN_BUY_YARN_BALL,
    BTN_CARE,
    BTN_CARE_APPLE,
    BTN_CARE_BALL,
    BTN_CARE_BIG_ENERGY,
    BTN_CARE_COMB,
    BTN_CARE_FOREST_HONEY,
    BTN_CARE_FUN_TOY,
    BTN_CARE_HEARTY_SNACK,
    BTN_CARE_SHAMPOO,
    BTN_CARE_SMALL_ENERGY,
    BTN_CARE_SOAP,
    BTN_CARE_YARN_BALL,
    BTN_HELP,
    BTN_INVENTORY,
    BTN_MY_RACCOON,
    BTN_SHOP,
    BTN_STATUS,
    BTN_TRAIN_AGILITY,
    BTN_TRAIN_INSTINCT,
    BTN_TRAIN_STRENGTH,
    BTN_TRAINING,
    BTN_TRAVEL,
    care_menu_keyboard,
    main_menu_keyboard,
    shop_menu_keyboard,
    training_menu_keyboard,
    TRAVEL_LOCATIONS,
    travel_menu_keyboard,
)
from storage import (
    exp_to_next_level,
    get_pet_max_needs,
    get_runaway_risk,
    get_item_catalog,
    get_shop_items,
    get_user,
    get_travel_event,
    get_travel_locations,
    perform_travel,
    shop_purchase,
    touch_user_needs,
    train_skill,
    update_pet_mood,
    update_pet_need,
)

router = Router()

MOOD_MAP = {"happy": "счастливый", "normal": "обычное", "tired": "уставший", "distressed": "тревожный"}
RISK_MAP = {"low": "низкий", "medium": "средний", "high": "высокий"}
TRAVEL_EVENT_MAP = {
    "peaceful walk through the forest": "спокойная прогулка по лесной тропе 🌲",
    "raccoon found extra berries": "енот нашёл горсть лесных ягод 🍓",
    "raccoon got muddy": "енот испачкался в мокрой земле 🐾",
}

TRAVEL_BUTTON_TO_ID = {value["button"]: key for key, value in TRAVEL_LOCATIONS.items()}
SKILL_LABELS = {"strength": "💪 Сила", "agility": "💨 Ловкость", "instinct": "🌙 Инстинкт"}
SCROLL_LABELS = {
    "strength_scroll": "📜 Свиток силы",
    "agility_scroll": "📜 Свиток ловкости",
    "instinct_scroll": "📜 Свиток инстинкта",
}


def _resolve_travel_location_id(button_text: str | None) -> str | None:
    if not button_text:
        return None
    direct = TRAVEL_BUTTON_TO_ID.get(button_text)
    if direct:
        return direct

    normalized = " ".join(button_text.split()).strip()
    if not normalized:
        return None

    for location_id, location in TRAVEL_LOCATIONS.items():
        button = str(location.get("button", "")).strip()
        if normalized == " ".join(button.split()):
            return location_id
    return None


def format_bar(value: int, maximum: int = 100, length: int = 10) -> str:
    safe_maximum = maximum if maximum > 0 else 100
    clamped = max(0, min(value if isinstance(value, int) else 0, safe_maximum))
    filled = round((clamped / safe_maximum) * length)
    return f"{'█' * filled}{'░' * (length - filled)} {clamped}/{safe_maximum}"


def _localize_mood(mood: str) -> str:
    return MOOD_MAP.get(mood, mood)


def _localize_event(event: str | None) -> str:
    if not event:
        return "пока не было"
    direct = get_travel_event(event)
    if isinstance(direct, dict):
        return str(direct.get("text", event))
    normalized = event.strip().lower().rstrip(".")
    return TRAVEL_EVENT_MAP.get(normalized, event)


def _status_text(pet: dict) -> str:
    mood = _localize_mood(update_pet_mood(pet))
    risk = get_runaway_risk(pet)
    max_needs = get_pet_max_needs(pet)
    lines = [
        f"🦝 Енот: {pet.get('name', '-')}",
        f"😊 Настроение: {mood}",
        "",
        "🍽 Сытость",
        format_bar(pet.get("satiety", 80), max_needs["satiety"]),
        "",
        "🧼 Чистота",
        format_bar(pet.get("cleanliness", 80), max_needs["cleanliness"]),
        "",
        "💞 Любовь",
        format_bar(pet.get("love", 80), max_needs["love"]),
        "",
        "⚡ Энергия",
        format_bar(pet.get("energy", 80), max_needs["energy"]),
    ]
    if risk in RISK_MAP:
        lines.extend(["", f"⚠️ Риск побега: {RISK_MAP[risk]}", "Еноту нужно больше любви."])
    return "\n".join(lines)


def _raccoon_profile_text(pet: dict) -> str:
    mood = _localize_mood(update_pet_mood(pet))
    skills = pet.get("skills", {}) if isinstance(pet.get("skills"), dict) else {}
    level = pet.get("level", 1)
    safe_level = level if isinstance(level, int) and level > 0 else 1
    exp = pet.get("exp", 0)
    safe_exp = exp if isinstance(exp, int) and exp >= 0 else 0
    max_needs = get_pet_max_needs(pet)
    return (
        f"🦝 {pet.get('name', '-')}\n\n"
        f"📌 Уровень: {safe_level}\n"
        f"✨ Опыт: {safe_exp} / {exp_to_next_level(safe_level)}\n"
        f"😊 Настроение: {mood}\n"
        f"📈 Максимум шкал: {max_needs['satiety']}\n\n"
        "💪 Навыки:\n"
        f"• Сила: {skills.get('strength', 0)}\n"
        f"• Ловкость: {skills.get('agility', 0)}\n"
        f"• Инстинкт: {skills.get('instinct', 0)}"
    )


def _inventory_text(pet: dict) -> str:
    inventory = pet.get("inventory", {}) if isinstance(pet.get("inventory"), dict) else {}
    return (
        "🎒 Инвентарь\n\n"
        f"🪙 Монеты: {pet.get('currency', 0)}\n\n"
        "🍽 Еда:\n"
        f"• 🍎 Яблоки: {inventory.get('food', 0)}\n"
        f"• 🥪 Сытные перекусы: {inventory.get('hearty_snack', 0)}\n"
        f"• 🍯 Лесной мёд: {inventory.get('forest_honey', 0)}\n\n"
        "🧼 Чистота:\n"
        f"• 🧼 Мыло: {inventory.get('soap', 0)}\n"
        f"• 🫧 Шампунь: {inventory.get('fluffy_shampoo', 0)}\n"
        f"• 🪮 Гребень: {inventory.get('comb', 0)}\n\n"
        "💞 Забота:\n"
        f"• 🎾 Мячики: {inventory.get('toy', 0)}\n"
        f"• 🧶 Клубки: {inventory.get('yarn_ball', 0)}\n"
        f"• 🪀 Игрушки: {inventory.get('fun_toy', 0)}\n\n"
        "⚡ Энергия:\n"
        f"• ⚡ Малые зелья: {inventory.get('energy_potion', 0)}\n"
        f"• 🔋 Большие зелья: {inventory.get('big_energy_potion', 0)}\n\n"
        "📜 Свитки:\n"
        f"• 📜 Свиток силы: {inventory.get('strength_scroll', 0)}\n"
        f"• 📜 Свиток ловкости: {inventory.get('agility_scroll', 0)}\n"
        f"• 📜 Свиток инстинкта: {inventory.get('instinct_scroll', 0)}"
    )

@router.message(F.text == BTN_STATUS)
async def show_status(message: Message) -> None:
    if message.from_user is None:
        return
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    await message.answer(_status_text(pet), reply_markup=main_menu_keyboard())


@router.message(F.text == BTN_MY_RACCOON)
async def show_raccoon(message: Message) -> None:
    if message.from_user is None:
        return
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    await message.answer(_raccoon_profile_text(pet), reply_markup=main_menu_keyboard())


@router.message(F.text == BTN_INVENTORY)
async def show_inventory(message: Message) -> None:
    if message.from_user is None:
        return
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    await message.answer(_inventory_text(pet), reply_markup=main_menu_keyboard())


@router.message(F.text == BTN_HELP)
async def show_help(message: Message) -> None:
    await message.answer(
        "🦝 Это RPG-тамагочи про енота.\n\n"
        "• Уход поддерживает сытость, чистоту, любовь и энергию.\n"
        "• Тренировки тратят энергию и свитки, дают навыки и опыт.\n"
        "• Путешествия дают опыт, монеты и случайные события.\n"
        "• Магазин пополняет припасы.\n"
        "• Инвентарь показывает монеты и предметы.\n"
        "• Потребности меняются со временем, когда ты возвращаешься в бота.",
        reply_markup=main_menu_keyboard(),
    )


@router.message(F.text == BTN_CARE)
async def care_menu(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await message.answer("Выбери действие ухода:", reply_markup=care_menu_keyboard())


@router.message(F.text == BTN_TRAINING)
async def training_menu(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await message.answer(
        "💪 Тренировки\n\n"
        "Для тренировки нужен подходящий свиток, который редко находится в путешествиях.\n\n"
        "• Сила — 📜 Свиток силы\n"
        "• Ловкость — 📜 Свиток ловкости\n"
        "• Инстинкт — 📜 Свиток инстинкта",
        reply_markup=training_menu_keyboard(),
    )


async def _train(message: Message, skill: str, title: str) -> None:
    if message.from_user is None:
        return
    success, levels_gained, user, scroll_key = train_skill(message.from_user.id, skill)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not success:
        if isinstance(pet, dict) and not scroll_key:
            await message.answer("Енот слишком устал. Нужна энергия ⚡", reply_markup=training_menu_keyboard())
            return
        scroll_label = SCROLL_LABELS.get(scroll_key or "", "подходящий свиток")
        await message.answer(
            f"Нужен {scroll_label}. Его можно редко найти в путешествиях.",
            reply_markup=training_menu_keyboard(),
        )
        return

    level_up_line = f"\n\n✨ Новый уровень! Енот достиг уровня {pet.get('level', 1)}." if levels_gained > 0 and isinstance(pet, dict) else ""
    await message.answer(
        f"{title}\n\n"
        "Енот развернул свиток и тренировался до хруста веток.\n\n"
        "Потрачено:\n"
        "• ⚡ Энергия: -15\n"
        f"• {SCROLL_LABELS.get(scroll_key or '', '📜 Свиток')}: -1\n\n"
        "Результат:\n"
        f"• {SKILL_LABELS.get(skill, 'Навык')}: +1\n"
        "• ✨ Опыт: +5"
        f"{level_up_line}",
        reply_markup=training_menu_keyboard(),
    )


@router.message(F.text == BTN_TRAVEL)
async def travel_menu(message: Message) -> None:
    if message.from_user is None:
        return
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    travel = pet.get("travel", {}) if isinstance(pet.get("travel"), dict) else {}
    locations = get_travel_locations()
    level = pet.get("level", 1) if isinstance(pet.get("level"), int) else 1
    unlocked = [loc["button"] for loc in locations.values() if level >= loc.get("min_level", 1)]
    locked_lines = [f"🔒 {loc['name']} — с уровня {loc['min_level']}" for loc in locations.values() if level < loc.get("min_level", 1)]
    locked_text = "\n".join(locked_lines) if locked_lines else "—"
    await message.answer(
        "🌲 Путешествия\n\n"
        f"• Всего прогулок: {travel.get('total_travels', 0)}\n"
        f"• Последнее событие: {_localize_event(travel.get('last_event'))}\n\n"
        "Доступные места:\n"
        + ("\n".join(f"• {b}" for b in unlocked) if unlocked else "—")
        + "\n\n"
        + locked_text,
        reply_markup=travel_menu_keyboard(unlocked),
    )


@router.message(F.text == BTN_SHOP)
async def shop_menu(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await message.answer("Магазин припасов 🛒", reply_markup=shop_menu_keyboard())


@router.message(F.text == BTN_BACK)
async def back_to_main(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())


async def _perform_care_action(message: Message, item_key: str) -> None:
    if message.from_user is None:
        return
    catalog = get_item_catalog()
    item = catalog.get(item_key, {})
    success, _ = update_pet_need(message.from_user.id, inventory_item=item_key)
    if not success:
        await message.answer("Такого предмета нет в инвентаре. Загляни в магазин 🛒", reply_markup=care_menu_keyboard())
        return
    await message.answer(
        f"Енот использовал {item.get('name', 'предмет').lower()} {item.get('emoji', '')}\n"
        f"{_need_label(item.get('need', ''))} +{item.get('restore', 0)}.",
        reply_markup=care_menu_keyboard(),
    )


def _need_label(need: str) -> str:
    return {"satiety": "Сытость", "cleanliness": "Чистота", "love": "Любовь", "energy": "Энергия"}.get(need, "Параметр")


@router.message(F.text == BTN_CARE_APPLE)
async def care_apple(message: Message) -> None:
    await _perform_care_action(message, "food")


@router.message(F.text == BTN_CARE_HEARTY_SNACK)
async def care_hearty_snack(message: Message) -> None:
    await _perform_care_action(message, "hearty_snack")


@router.message(F.text == BTN_CARE_FOREST_HONEY)
async def care_forest_honey(message: Message) -> None:
    await _perform_care_action(message, "forest_honey")


@router.message(F.text == BTN_CARE_SOAP)
async def care_soap(message: Message) -> None:
    await _perform_care_action(message, "soap")


@router.message(F.text == BTN_CARE_SHAMPOO)
async def care_shampoo(message: Message) -> None:
    await _perform_care_action(message, "fluffy_shampoo")


@router.message(F.text == BTN_CARE_COMB)
async def care_comb(message: Message) -> None:
    await _perform_care_action(message, "comb")


@router.message(F.text == BTN_CARE_BALL)
async def care_ball(message: Message) -> None:
    await _perform_care_action(message, "toy")


@router.message(F.text == BTN_CARE_YARN_BALL)
async def care_yarn_ball(message: Message) -> None:
    await _perform_care_action(message, "yarn_ball")


@router.message(F.text == BTN_CARE_FUN_TOY)
async def care_fun_toy(message: Message) -> None:
    await _perform_care_action(message, "fun_toy")


@router.message(F.text == BTN_CARE_SMALL_ENERGY)
async def care_small_energy(message: Message) -> None:
    await _perform_care_action(message, "energy_potion")


@router.message(F.text == BTN_CARE_BIG_ENERGY)
async def care_big_energy(message: Message) -> None:
    await _perform_care_action(message, "big_energy_potion")


@router.message(F.text == BTN_TRAIN_STRENGTH)
async def train_strength(message: Message) -> None:
    await _train(message, "strength", "Тренировка силы завершена 💪")


@router.message(F.text == BTN_TRAIN_AGILITY)
async def train_agility(message: Message) -> None:
    await _train(message, "agility", "Тренировка ловкости завершена 💨")


@router.message(F.text == BTN_TRAIN_INSTINCT)
async def train_instinct(message: Message) -> None:
    await _train(message, "instinct", "Тренировка инстинкта завершена 🌙")


@router.message(F.text.in_(set(TRAVEL_BUTTON_TO_ID.keys())))
async def travel_to_location(message: Message) -> None:
    if message.from_user is None:
        return
    location_id = _resolve_travel_location_id(message.text)
    if not location_id:
        return

    success, levels_gained, missing, user, location, event, result = perform_travel(message.from_user.id, location_id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return

    level = pet.get("level", 1) if isinstance(pet.get("level"), int) else 1
    available = [loc["button"] for loc in get_travel_locations().values() if level >= loc.get("min_level", 1)]

    if not success:
        req_map = {"energy": "⚡ Энергия", "satiety": "🍽 Сытость", "cleanliness": "🧼 Чистота", "level": "📌 Уровень"}
        req_lines = []
        for item in missing:
            name = item.split(" >= ")[0]
            value = item.split(" >= ")[1] if " >= " in item else "?"
            req_lines.append(f"• {req_map.get(name, name)}: нужно минимум {value}")
        await message.answer(
            "Енот пока не готов к путешествию:\n" + "\n".join(req_lines),
            reply_markup=travel_menu_keyboard(available),
        )
        return

    location_name = (location or {}).get("name", "Локация")
    spent = result or {}
    reward_lines = [f"• ✨ Опыт: +{spent.get('exp', 0)}", f"• 🪙 Монеты: +{spent.get('currency', 0)}"]
    if spent.get("event_exp", 0):
        reward_lines.append(f"• ✨ Бонус опыта: +{spent['event_exp']}")
    if spent.get("event_currency", 0):
        reward_lines.append(f"• 🪙 Бонус монет: +{spent['event_currency']}")

    item_map = {
        "food": "🍎 Яблоко",
        "forest_honey": "🍯 Лесной мёд",
        "strength_scroll": "📜 Свиток силы",
        "agility_scroll": "📜 Свиток ловкости",
        "instinct_scroll": "📜 Свиток инстинкта",
    }
    item_lines = [f"Получено: {item_map[key]} x{value}" for key, value in spent.items() if key in item_map and isinstance(value, int)]
    level_up_line = f"\n\n✨ Новый уровень! Енот достиг уровня {pet.get('level', 1)}." if levels_gained > 0 else ""
    text = (
        f"🌲 {location_name}\n\n"
        "Енот вернулся из прогулки, весь важный и немного в листьях.\n\n"
        "Потрачено:\n"
        f"• ⚡ Энергия: -{spent.get('energy', 0)}\n"
        f"• 🍽 Сытость: -{spent.get('satiety', 0)}\n"
        f"• 🧼 Чистота: -{spent.get('cleanliness', 0)}\n\n"
        "Награда:\n"
        + "\n".join(reward_lines)
        + "\n\nСобытие:\n"
        + _localize_event((event or {}).get("id") if isinstance(event, dict) else None)
        + ("\n" + "\n".join(item_lines) if item_lines else "")
        + level_up_line
    )
    await message.answer(text, reply_markup=travel_menu_keyboard(available))


async def _buy_item_action(message: Message, item_key: str, item_label: str) -> None:
    if message.from_user is None:
        return
    prices = get_shop_items()
    price = prices.get(item_key, 0)
    success, _, balance, count, _ = shop_purchase(message.from_user.id, item_key)
    if not success:
        await message.answer(
            f"Не хватает монет.\nЦена: {price}\nТвой баланс: {balance}",
            reply_markup=shop_menu_keyboard(),
        )
        return
    await message.answer(
        "Покупка успешна!\n"
        f"Предмет: {item_label}\n"
        f"Монет осталось: {balance}\n"
        f"Теперь в инвентаре: {count}",
        reply_markup=shop_menu_keyboard(),
    )


@router.message(F.text == BTN_BUY_FOOD)
async def buy_food(message: Message) -> None:
    await _buy_item_action(message, "food", "Яблоко")


@router.message(F.text == BTN_BUY_HEARTY_SNACK)
async def buy_hearty_snack(message: Message) -> None:
    await _buy_item_action(message, "hearty_snack", "Сытный перекус")


@router.message(F.text == BTN_BUY_FOREST_HONEY)
async def buy_forest_honey(message: Message) -> None:
    await _buy_item_action(message, "forest_honey", "Лесной мёд")


@router.message(F.text == BTN_BUY_SOAP)
async def buy_soap(message: Message) -> None:
    await _buy_item_action(message, "soap", "Мыло")


@router.message(F.text == BTN_BUY_SHAMPOO)
async def buy_shampoo(message: Message) -> None:
    await _buy_item_action(message, "fluffy_shampoo", "Шампунь")


@router.message(F.text == BTN_BUY_COMB)
async def buy_comb(message: Message) -> None:
    await _buy_item_action(message, "comb", "Гребень")


@router.message(F.text == BTN_BUY_TOY)
async def buy_toy(message: Message) -> None:
    await _buy_item_action(message, "toy", "Мячик")


@router.message(F.text == BTN_BUY_YARN_BALL)
async def buy_yarn_ball(message: Message) -> None:
    await _buy_item_action(message, "yarn_ball", "Клубок")


@router.message(F.text == BTN_BUY_FUN_TOY)
async def buy_fun_toy(message: Message) -> None:
    await _buy_item_action(message, "fun_toy", "Игрушка")


@router.message(F.text == BTN_BUY_ENERGY)
async def buy_energy_potion(message: Message) -> None:
    await _buy_item_action(message, "energy_potion", "Малое зелье")


@router.message(F.text == BTN_BUY_BIG_ENERGY)
async def buy_big_energy_potion(message: Message) -> None:
    await _buy_item_action(message, "big_energy_potion", "Большое зелье")
