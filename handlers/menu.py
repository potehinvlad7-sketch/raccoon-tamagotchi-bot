import random

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramAPIError

from keyboards import (
    BTN_BACK,
    BTN_BATTLE_ATTACK,
    BTN_BATTLE_RUN,
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
    BTN_CANCEL,
    BTN_CONTACT_ADMIN,
    BTN_LETTER_TO_RACCOON,
    BTN_MY_RACCOON,
    BTN_SHOP,
    BTN_SHOP_BACK,
    BTN_STATUS,
    BTN_TRAIN_AGILITY,
    BTN_TRAIN_INSTINCT,
    BTN_TRAIN_STRENGTH,
    BTN_TRAINING,
    BTN_TRAVEL,
    battle_menu_keyboard,
    care_menu_keyboard,
    main_menu_keyboard,
    build_shop_keyboard,
    build_shop_item_keyboard,
    cancel_keyboard,
    training_menu_keyboard,
    TRAVEL_LOCATIONS,
    travel_menu_keyboard,
)
from config import ADMIN_IDS
from handlers.admin_profile import format_admin_user_full
from storage import (
    calculate_enemy_win_chance,
    exp_to_next_level,
    get_enemy,
    get_pet_max_needs,
    get_runaway_risk,
    get_item_catalog,
    get_shop_categories,
    get_shop_item,
    get_shop_items_by_category,
    shop_purchase,
    get_user,
    get_travel_event,
    get_travel_locations,
    perform_travel,
    resolve_battle_attack,
    resolve_battle_run,
    touch_user_needs,
    train_skill,
    update_pet_mood,
    update_pet_need,
)

router = Router()


class AdminMessageState(StatesGroup):
    waiting_for_admin_message = State()

MOOD_MAP = {"happy": "счастливый", "normal": "обычное", "tired": "уставший", "distressed": "тревожный"}
RISK_MAP = {"low": "низкий", "medium": "средний", "high": "высокий"}
TRAVEL_EVENT_MAP = {
    "peaceful walk through the forest": "спокойная прогулка по лесной тропе 🌲",
    "raccoon found extra berries": "енот нашёл горсть лесных ягод 🍓",
    "raccoon got muddy": "енот испачкался в мокрой земле 🐾",
}

TRAVEL_BUTTON_TO_ID = {value["button"]: key for key, value in TRAVEL_LOCATIONS.items()}
GROUP_FLAVOR_LINES = [
    "🦝 {name} гордо показывает найденный листочек.",
    "🌿 {name} выглядит немного уставшим после путешествий.",
    "✨ {name} внимательно смотрит по сторонам.",
]
SKILL_LABELS = {"strength": "💪 Сила", "agility": "💨 Ловкость", "instinct": "🌙 Инстинкт"}
SCROLL_LABELS = {
    "strength_scroll": "📜 Свиток силы",
    "agility_scroll": "📜 Свиток ловкости",
    "instinct_scroll": "📜 Свиток инстинкта",
}
ITEM_LABELS = {
    "food": "🍎 Яблоко",
    "hearty_snack": "🥪 Сытный перекус",
    "forest_honey": "🍯 Лесной мёд",
    "soap": "🧼 Мыло",
    "comb": "🪮 Гребень",
    "toy": "🎾 Мячик",
    "energy_potion": "⚡ Малое зелье энергии",
    "strength_scroll": "📜 Свиток силы",
    "agility_scroll": "📜 Свиток ловкости",
    "instinct_scroll": "📜 Свиток инстинкта",
}
SHOP_CATEGORY_TO_BUTTON = {
    "food": "🍖 Еда",
    "household": "🧺 Быт",
    "toys": "🧸 Игрушки",
    "potions": "🧪 Зелья",
    "weapons": "🗡️ Оружие",
    "armor": "🛡️ Броня",
    "accessories": "💍 Аксессуары",
    "materials": "🪵 Материалы",
}
SHOP_BUTTON_TO_CATEGORY = {label: category_id for category_id, label in SHOP_CATEGORY_TO_BUTTON.items()}


def get_enemy_name(enemy_id: str) -> str:
    return str(get_enemy(enemy_id).get("name", "Неизвестный противник"))


def get_location_title(location_id: str) -> str:
    return str(TRAVEL_LOCATIONS.get(location_id, {}).get("name", "Локация"))


def format_battle_intro(pet_name: str, location_id: str, enemy_id: str) -> str:
    return (
        "⚔️ Встреча с противником\n\n"
        f"🌲 Гуляя по локации «{get_location_title(location_id)}», {pet_name} услышал шорох в траве.\n"
        f"Из листвы выскочила {get_enemy_name(enemy_id)}.\n\n"
        "Что делать?"
    )


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
    if isinstance(pet.get("battle"), dict):
        lines.extend(["", "⚔️ Активная стычка: ждёт твоего решения."])
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


def _group_raccoon_profile_text(pet: dict) -> str:
    mood = _localize_mood(update_pet_mood(pet))
    level = pet.get("level", 1)
    safe_level = level if isinstance(level, int) and level > 0 else 1
    exp = pet.get("exp", 0)
    safe_exp = exp if isinstance(exp, int) and exp >= 0 else 0
    max_needs = get_pet_max_needs(pet)
    name = str(pet.get("name", "Енот"))
    base = (
        f"🦝 {name}\n\n"
        f"⭐ Уровень: {safe_level}\n"
        f"✨ Опыт: {safe_exp} / {exp_to_next_level(safe_level)}\n\n"
        f"🍖 Сытость: {pet.get('satiety', 0)}/{max_needs['satiety']}\n"
        f"🧼 Чистота: {pet.get('cleanliness', 0)}/{max_needs['cleanliness']}\n"
        f"❤️ Любовь: {pet.get('love', 0)}/{max_needs['love']}\n"
        f"⚡ Энергия: {pet.get('energy', 0)}/{max_needs['energy']}\n\n"
        f"😊 Настроение: {mood}"
    )
    if random.random() < 0.5:
        return f"{base}\n\n{random.choice(GROUP_FLAVOR_LINES).format(name=name)}"
    return base


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


def format_travel_result_after_battle(pet: dict, battle: dict, section_title: str, section_lines: list[str]) -> str:
    pet_name = str(pet.get("name", "Енот"))
    level_up_line = ""
    if int(battle.get("levels_gained", 0)) > 0:
        level_up_line = f"\n\n✨ Новый уровень! {pet_name} достиг уровня {pet.get('level', 1)}."
    regular_event = _localize_event(battle.get("event_id")) if battle.get("event_id") else "пока не было"
    item_lines = [
        f"• {ITEM_LABELS[item]} x{amount}"
        for item, amount in (battle.get("items_delta", {}) if isinstance(battle.get("items_delta"), dict) else {}).items()
        if isinstance(amount, int) and amount > 0 and item in ITEM_LABELS
    ]
    return (
        f"{TRAVEL_LOCATIONS.get(battle.get('location_id', ''), {}).get('button', '🌲 Локация')}\n\n"
        f"{pet_name} вернулся из прогулки, весь важный и немного в листьях.\n\n"
        "Потрачено:\n"
        f"• ⚡ Энергия: -{battle.get('spent_energy', 0)}\n"
        f"• 🍽 Сытость: -{battle.get('spent_satiety', 0)}\n"
        f"• 🧼 Чистота: -{battle.get('spent_cleanliness', 0)}\n\n"
        "Награда:\n"
        f"• ✨ Опыт: +{battle.get('base_exp', 0)}\n"
        f"• 🪙 Монеты: +{battle.get('base_currency', 0)}\n\n"
        "Событие:\n"
        f"{regular_event}\n\n"
        f"{section_title}\n"
        + "\n".join(section_lines)
        + ("\n\nДополнительно из события:\n" + "\n".join(item_lines) if item_lines else "")
        + level_up_line
    )

@router.message(F.text == BTN_STATUS)
async def show_status(message: Message) -> None:
    if message.from_user is None:
        return
    touch_user_needs(message.from_user.id)
    sender_text = "💌 Енотик принес новое письмо\n\n" + format_admin_user_full(message.from_user.id)
    message_text = f"💬 Письмо:\n\n{message.text}"

    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, sender_text)
            await message.bot.send_message(admin_id, message_text)
        except TelegramAPIError:
            continue

    await state.clear()
    await message.answer("✨ Ваш енотик убежал доставлять письмо ArtRaccoon.", reply_markup=main_menu_keyboard())


@router.message(AdminMessageState.waiting_for_admin_message)
async def contact_admin_non_text(message: Message) -> None:
    await message.answer("Пожалуйста, отправьте текстовое сообщение.")


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
    await message.answer("🛒 Магазин", reply_markup=build_shop_keyboard())


@router.message(F.text == BTN_BACK)
async def back_to_main(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())


@router.message(F.text == BTN_SHOP_BACK)
async def back_from_shop(message: Message) -> None:
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
        if "battle_pending" in missing:
            await message.answer("Сначала разберись с текущим противником.", reply_markup=battle_menu_keyboard())
            return
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

    if isinstance(event, dict) and event.get("type") == "enemy":
        await message.answer(
            format_battle_intro(str(pet.get("name", "Енот")), location_id, str(event.get("enemy_id", "field_mouse"))),
            reply_markup=battle_menu_keyboard(),
        )
        return
    location_name = (location or {}).get("name", "Локация")
    spent = result or {}
    level_up_line = f"\n\n✨ Новый уровень! Енот достиг уровня {pet.get('level', 1)}." if levels_gained > 0 else ""
    text = (
        f"🌲 {location_name}\n\n"
        "Енот вернулся из прогулки, весь важный и немного в листьях.\n\n"
        "Потрачено:\n"
        f"• ⚡ Энергия: -{spent.get('energy', 0)}\n"
        f"• 🍽 Сытость: -{spent.get('satiety', 0)}\n"
        f"• 🧼 Чистота: -{spent.get('cleanliness', 0)}\n\n"
        "Награда:\n"
        f"• ✨ Опыт: +{spent.get('exp', 0)}\n"
        f"• 🪙 Монеты: +{spent.get('currency', 0)}\n\n"
        "Событие:\n"
        + _localize_event((event or {}).get("id") if isinstance(event, dict) else None)
        + level_up_line
    )
    await message.answer(
        text,
        reply_markup=travel_menu_keyboard(available),
    )


@router.message(F.text == BTN_BATTLE_ATTACK)
async def battle_attack(message: Message) -> None:
    if message.from_user is None:
        return
    ok, result = resolve_battle_attack(message.from_user.id)
    if not ok or not isinstance(result, dict):
        await message.answer("Сейчас рядом нет противника.", reply_markup=main_menu_keyboard())
        return
    enemy = result.get("enemy", {}) if isinstance(result.get("enemy"), dict) else {}
    if result.get("win"):
        lines = [
            f"{pet_name if (pet_name := str(result.get('pet_name', 'Енот'))) else 'Енот'} победил: {enemy.get('name', 'Неизвестный враг')}.",
            "Дополнительно:",
            f"• ✨ Опыт: +{result.get('extra_exp', 0)}",
            f"• 🪙 Монеты: +{result.get('extra_currency', 0)}",
        ]
        for item, amount in (result.get("drop_items", {}) if isinstance(result.get("drop_items"), dict) else {}).items():
            if item in ITEM_LABELS and isinstance(amount, int) and amount > 0:
                lines.append(f"• {ITEM_LABELS[item]} x{amount}")
        await message.answer(format_travel_result_after_battle(result.get("pet", {}), result.get("travel_context", {}), "⚔️ Бой:", lines), reply_markup=main_menu_keyboard())
        return
    penalties = result.get("penalties", {}) if isinstance(result.get("penalties"), dict) else {}
    await message.answer(
        format_travel_result_after_battle(
            result.get("pet", {}),
            result.get("travel_context", {}),
            "⚔️ Бой:",
            [
                f"{str(result.get('pet_name', 'Енот'))} проиграл: {enemy.get('name', 'Неизвестный враг')}.",
                f"Потери: ⚡ {penalties.get('energy', 0)}, 🧼 {penalties.get('cleanliness', 0)}, 💞 {penalties.get('love', 0)}, 🍽 {penalties.get('satiety', 0)}",
            ],
        ),
        reply_markup=main_menu_keyboard(),
    )


@router.message(F.text == BTN_BATTLE_RUN)
async def battle_run(message: Message) -> None:
    if message.from_user is None:
        return
    ok, result = resolve_battle_run(message.from_user.id)
    if not ok or not isinstance(result, dict):
        await message.answer("Сейчас рядом нет противника.", reply_markup=main_menu_keyboard())
        return
    penalties = result.get("penalties", {}) if isinstance(result.get("penalties"), dict) else {}
    enemy = result.get("enemy", {}) if isinstance(result.get("enemy"), dict) else {}
    if result.get("escaped"):
        await message.answer(
            format_travel_result_after_battle(
                result.get("pet", {}),
                result.get("travel_context", {}),
                "🏃 Побег:",
                [f"{str(result.get('pet_name', 'Енот'))} юркнул в кусты и ушёл от {enemy.get('name', 'Неизвестный враг')}.", f"Потери: ⚡ {penalties.get('energy', 0)}"],
            ),
            reply_markup=main_menu_keyboard(),
        )
        return
    await message.answer(
        format_travel_result_after_battle(
            result.get("pet", {}),
            result.get("travel_context", {}),
            "🏃 Побег:",
            [f"{str(result.get('pet_name', 'Енот'))} не смог сразу уйти от {enemy.get('name', 'Неизвестный враг')}.", f"Потери: ⚡ {penalties.get('energy', 0)}, 🧼 {penalties.get('cleanliness', 0)}, 💞 {penalties.get('love', 0)}"],
        ),
        reply_markup=main_menu_keyboard(),
    )


def _shop_category_text(category: dict, items: list[dict]) -> str:
    lines: list[str] = []
    for item in items:
        lines.extend(
            [
                f"{item.get('emoji', '🛒')} {item.get('name', 'Предмет')}",
                str(item.get("description", "Описание отсутствует.")),
                f"💰 {item.get('price', 0)} монет",
                "",
            ]
        )
    item_list = "\n".join(lines).strip() if lines else "Пока нет доступных товаров."
    return (
        f"{category.get('emoji', '🛒')} {category.get('title', 'Категория')}\n\n"
        f"{item_list}"
    )


def _resolve_shop_emoji(item_id: str, item_name: str) -> str:
    catalog = get_item_catalog()
    from_catalog = catalog.get(item_id, {}).get("emoji")
    if isinstance(from_catalog, str) and from_catalog:
        return from_catalog
    for value in ITEM_LABELS.values():
        if item_name in value:
            return value.split(" ")[0]
    return "🛒"

@router.message(F.text.in_(set(SHOP_BUTTON_TO_CATEGORY.keys())))
async def shop_open_category(message: Message) -> None:
    category_id = SHOP_BUTTON_TO_CATEGORY.get(message.text or "")
    if not category_id:
        return
    category = get_shop_categories().get(category_id)
    if not isinstance(category, dict):
        await message.answer("Категория недоступна.", reply_markup=build_shop_keyboard())
        return
    items = get_shop_items_by_category(category_id)
    prepared_items = [{**item, "emoji": _resolve_shop_emoji(str(item.get("id", "")), str(item.get("name", "")))} for item in items]
    await message.answer(
        _shop_category_text(category, prepared_items),
        reply_markup=build_shop_item_keyboard(category_id, prepared_items),
    )


@router.callback_query(F.data.startswith("shop_back:"))
async def shop_back_to_categories(callback: CallbackQuery) -> None:
    if callback.message is None:
        return
    await callback.message.answer("🛒 Магазин", reply_markup=build_shop_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("shop_buy:"))
async def shop_buy_item(callback: CallbackQuery) -> None:
    if callback.from_user is None:
        return
    item_id = (callback.data or "").split(":", maxsplit=1)[1] if ":" in (callback.data or "") else ""
    item = get_shop_item(item_id)
    if not isinstance(item, dict):
        await callback.answer("Товар недоступен.", show_alert=True)
        return
    success, price, _, count, _ = shop_purchase(callback.from_user.id, item_id)
    if not success:
        await callback.answer("Недостаточно монет.", show_alert=True)
        return
    emoji = _resolve_shop_emoji(item_id, str(item.get("name", "")))
    await callback.message.answer(
        "🛒 Покупка\n\n"
        "Вы купили:\n"
        f"{emoji} {item.get('name', 'Предмет')} x1\n\n"
        "Потрачено:\n"
        f"💰 {price} монет"
    )
    await callback.answer(f"В инвентаре: {count}")
