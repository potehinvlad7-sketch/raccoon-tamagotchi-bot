from aiogram import F, Router
from aiogram.types import Message

from keyboards import (
    BTN_BACK,
    BTN_BUY_ENERGY,
    BTN_BUY_FOOD,
    BTN_BUY_SOAP,
    BTN_BUY_TOY,
    BTN_CARE,
    BTN_CLEAN,
    BTN_ENERGY,
    BTN_FEED,
    BTN_HELP,
    BTN_INVENTORY,
    BTN_MY_RACCOON,
    BTN_PLAY,
    BTN_SHOP,
    BTN_STATUS,
    BTN_TRAIN_AGILITY,
    BTN_TRAIN_INSTINCT,
    BTN_TRAIN_STRENGTH,
    BTN_TRAINING,
    BTN_TRAVEL,
    BTN_TRIP_FOREST,
    care_menu_keyboard,
    main_menu_keyboard,
    shop_menu_keyboard,
    training_menu_keyboard,
    travel_menu_keyboard,
)
from storage import (
    exp_to_next_level,
    get_pet_max_needs,
    get_runaway_risk,
    get_shop_items,
    get_user,
    perform_short_forest_trip,
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
    "raccoon found extra berries": "енот нашёл горсть лесных ягод 🍓",
    "peaceful walk through the forest": "спокойная прогулка по лесной тропе 🌲",
    "raccoon got muddy": "енот испачкался в мокрой земле 🐾",
}



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
    return TRAVEL_EVENT_MAP.get(event.strip().lower(), event)


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
        f"• 🍎 Еда: {inventory.get('food', 0)}\n"
        f"• 🧼 Мыло: {inventory.get('soap', 0)}\n"
        f"• 🎾 Игрушки: {inventory.get('toy', 0)}\n"
        f"• ⚡ Зелья энергии: {inventory.get('energy_potion', 0)}"
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
        "• Тренировки тратят энергию, дают навыки и опыт.\n"
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
    await message.answer("Выбери тренировку:", reply_markup=training_menu_keyboard())


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
    await message.answer(
        "🌲 Путешествия\n\n"
        f"• Всего прогулок: {travel.get('total_travels', 0)}\n"
        f"• Последнее событие: {_localize_event(travel.get('last_event'))}\n\n"
        "Куда отправим енота?",
        reply_markup=travel_menu_keyboard(),
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


async def _perform_care_action(message: Message, need: str, amount: int, item: str, ok_message: str, missing_message: str) -> None:
    if message.from_user is None:
        return
    success = update_pet_need(message.from_user.id, need=need, amount=amount, inventory_item=item)
    if not success:
        await message.answer(missing_message, reply_markup=care_menu_keyboard())
        return
    await message.answer(ok_message, reply_markup=care_menu_keyboard())


@router.message(F.text == BTN_FEED)
async def care_feed(message: Message) -> None:
    await _perform_care_action(message, "satiety", 50, "food", "Енот с удовольствием перекусил 🍎", "Еды нет. Загляни в магазин 🛒")


@router.message(F.text == BTN_CLEAN)
async def care_clean(message: Message) -> None:
    await _perform_care_action(message, "cleanliness", 50, "soap", "Енот снова чистый и пушистый 🧼", "Мыла нет. Загляни в магазин 🛒")


@router.message(F.text == BTN_PLAY)
async def care_play(message: Message) -> None:
    await _perform_care_action(message, "love", 50, "toy", "Енот радостно поиграл с тобой 🎾", "Игрушек нет. Загляни в магазин 🛒")


@router.message(F.text == BTN_ENERGY)
async def care_energy(message: Message) -> None:
    await _perform_care_action(message, "energy", 50, "energy_potion", "Енот выпил зелье и приободрился ⚡", "Зелий энергии нет. Загляни в магазин 🛒")


async def _train(message: Message, skill_name: str, success_message: str) -> None:
    if message.from_user is None:
        return
    trained, levels_gained, user = train_skill(message.from_user.id, skill_name)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    if not trained:
        await message.answer("Енот слишком устал для тренировки. Дай ему восстановить энергию ⚡", reply_markup=training_menu_keyboard())
        return
    level_up_line = f"\nНовый уровень! Енот достиг уровня {pet.get('level', 1)} ✨" if levels_gained > 0 else ""
    await message.answer(f"{success_message}{level_up_line}", reply_markup=training_menu_keyboard())


@router.message(F.text == BTN_TRAIN_STRENGTH)
async def train_strength(message: Message) -> None:
    await _train(message, "strength", "Тренировка силы завершена 💪")


@router.message(F.text == BTN_TRAIN_AGILITY)
async def train_agility(message: Message) -> None:
    await _train(message, "agility", "Тренировка ловкости завершена 💨")


@router.message(F.text == BTN_TRAIN_INSTINCT)
async def train_instinct(message: Message) -> None:
    await _train(message, "instinct", "Тренировка инстинкта завершена 🌙")


@router.message(F.text == BTN_TRIP_FOREST)
async def short_forest_trip(message: Message) -> None:
    if message.from_user is None:
        return
    success, levels_gained, missing, user = perform_short_forest_trip(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    if not success:
        req_map = {"energy": "энергия (минимум 30)", "satiety": "сытость (минимум 30)", "cleanliness": "чистота (минимум 20)"}
        req_lines = "\n".join(f"• {req_map.get(item, item)}" for item in missing)
        await message.answer(f"Енот пока не готов к путешествию:\n{req_lines}", reply_markup=travel_menu_keyboard())
        return
    level_up_line = f"\nНовый уровень! Енот достиг уровня {pet.get('level', 1)} ✨" if levels_gained > 0 else ""
    event = _localize_event(pet.get("travel", {}).get("last_event"))
    await message.answer(
        "Прогулка завершена 🌲\n"
        "Потрачено: энергия -20, сытость -10, чистота -5\n"
        "Награда: опыт +10, монеты +5\n"
        f"Событие: {event}{level_up_line}",
        reply_markup=travel_menu_keyboard(),
    )


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
    await _buy_item_action(message, "food", "Еда")


@router.message(F.text == BTN_BUY_SOAP)
async def buy_soap(message: Message) -> None:
    await _buy_item_action(message, "soap", "Мыло")


@router.message(F.text == BTN_BUY_TOY)
async def buy_toy(message: Message) -> None:
    await _buy_item_action(message, "toy", "Игрушка")


@router.message(F.text == BTN_BUY_ENERGY)
async def buy_energy_potion(message: Message) -> None:
    await _buy_item_action(message, "energy_potion", "Зелье энергии")
