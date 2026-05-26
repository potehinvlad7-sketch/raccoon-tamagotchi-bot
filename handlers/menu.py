import random
from datetime import timedelta

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest

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
    BTN_CARE_SLEEP,
    BTN_CARE_SMALL_ENERGY,
    BTN_CARE_SOAP,
    BTN_CARE_YARN_BALL,
    BTN_HELP,
    BTN_INVENTORY,
    BTN_CANCEL,
    BTN_CONTACT_ADMIN,
    BTN_LETTER_TO_RACCOON,
    BTN_MAGIC,
    BTN_MY_RACCOON,
    BTN_POTIONS,
    BTN_SHOP,
    BTN_SHOP_BACK,
    BTN_STATUS,
    BTN_SKILLS,
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
    pet_care_inline_keyboard,
    magic_and_sword_keyboard,
    magic_and_sword_inline_keyboard,
    training_menu_keyboard,
    TRAVEL_LOCATIONS,
    travel_menu_keyboard,
)
from config import ADMIN_IDS
from handlers.images import send_optional_screen
from storage import (
    calculate_enemy_win_chance,
    exp_to_next_level,
    LEGEND_LEVEL,
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
    refresh_user_metadata,
    touch_user_needs,
    train_skill,
    sleep_pet,
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


def _blocked_levelup_text(pet: dict) -> str:
    if pet.get("level_up_blocked"):
        return (
            "\n\n🔒 Енотик набрал достаточно опыта, но путь дальше закрыт.\n"
            "Победите босса следующей локации, чтобы открыть новый уровень."
        )
    return ""


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




def _select_travel_window(level: int, max_items: int = 3) -> list[tuple[str, dict]]:
    sorted_locations = sorted(get_travel_locations().items(), key=lambda item: item[1].get("min_level", 1))
    if not sorted_locations:
        return []

    safe_level = level if isinstance(level, int) and level > 0 else 1
    current_index = 0
    for idx, (_, location) in enumerate(sorted_locations):
        if safe_level >= int(location.get("min_level", 1)):
            current_index = idx
        else:
            break

    selected_indexes: list[int] = []
    for candidate in (current_index - 1, current_index, current_index + 1):
        if 0 <= candidate < len(sorted_locations) and candidate not in selected_indexes:
            selected_indexes.append(candidate)

    forward = current_index + 2
    backward = current_index - 2
    while len(selected_indexes) < max_items and (forward < len(sorted_locations) or backward >= 0):
        if forward < len(sorted_locations) and forward not in selected_indexes:
            selected_indexes.append(forward)
            if len(selected_indexes) >= max_items:
                break
        if backward >= 0 and backward not in selected_indexes:
            selected_indexes.insert(0, backward)
        forward += 1
        backward -= 1

    selected_indexes = sorted(selected_indexes)[:max_items]
    return [sorted_locations[i] for i in selected_indexes]


def _travel_buttons_for_level(level: int) -> list[str]:
    return [location.get("button", "🌲 Локация") for _, location in _select_travel_window(level)]


def _travel_location_ids_for_level(level: int) -> set[str]:
    return {location_id for location_id, _ in _select_travel_window(level)}
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


def _travel_event_line(event: dict | None) -> str:
    if not isinstance(event, dict):
        return "🌿 Событие: спокойная прогулка."
    if event.get("id") == "retreat_high_route":
        return "🌲 Енотик услышал тревожный шорох и с ужасом убежал обратно.\nПохоже, к этой дороге он пока не готов."
    if bool(event.get("is_boss")):
        return "👑 Хранитель пути преградил дорогу.\nПока он не побеждён, новая локация не откроется."
    if event.get("type") == "enemy":
        return "⚔️ Событие: встреча с противником."
    return "🌿 Событие: спокойная прогулка."


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
    is_legendary = safe_level >= LEGEND_LEVEL
    exp = pet.get("exp", 0)
    safe_exp = exp if isinstance(exp, int) and exp >= 0 else 0
    next_exp = exp_to_next_level(safe_level)
    exp_line = "✨ Опыт: максимум достигнут" if next_exp is None else f"✨ Опыт: {safe_exp} / {next_exp}"
    level_line = f"📌 Уровень: {safe_level} 👑 Легенда" if is_legendary else f"📌 Уровень: {safe_level}"
    max_needs = get_pet_max_needs(pet)
    return (
        f"🦝 {pet.get('name', '-')}\n\n"
        f"{level_line}\n"
        f"{exp_line}\n"
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
    is_legendary = safe_level >= LEGEND_LEVEL
    exp = pet.get("exp", 0)
    safe_exp = exp if isinstance(exp, int) and exp >= 0 else 0
    next_exp = exp_to_next_level(safe_level)
    exp_line = "✨ Опыт: максимум достигнут" if next_exp is None else f"✨ Опыт: {safe_exp} / {next_exp}"
    level_line = f"⭐ Уровень: {safe_level} 👑 Легенда" if is_legendary else f"⭐ Уровень: {safe_level}"
    max_needs = get_pet_max_needs(pet)
    name = str(pet.get("name", "Енот"))
    base = (
        f"🦝 {name}\n\n"
        f"{level_line}\n"
        f"{exp_line}\n\n"
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




def _reward_lines(exp: int, currency: int) -> list[str]:
    lines: list[str] = []
    if isinstance(exp, int) and exp > 0:
        lines.append(f"• ✨ Опыт: +{exp}")
    if isinstance(currency, int) and currency > 0:
        lines.append(f"• 🪙 Монеты: +{currency}")
    return lines


def _reward_block(exp: int, currency: int, empty_text: str | None = None) -> str:
    lines = _reward_lines(exp, currency)
    if lines:
        return "Награда:\n" + "\n".join(lines)
    return empty_text if empty_text else ""


def format_travel_result_after_battle(pet: dict, battle: dict, section_title: str, section_lines: list[str]) -> str:
    pet_name = str(pet.get("name", "Енот"))
    level_up_line = ""
    if int(battle.get("levels_gained", 0)) > 0:
        level_up_line = f"\n\n✨ Новый уровень! {pet_name} достиг уровня {pet.get('level', 1)}."
    event_line = "⚔️ Событие: встреча с противником."
    if battle.get("is_boss"):
        if battle.get("boss_failed") or battle.get("boss_blocked"):
            event_line = (
                "👑 Хранитель пути оказался сильнее.\n"
                "Енотик отступил, но запомнил дорогу."
            )
        elif battle.get("boss_defeated"):
            if battle.get("level_gained"):
                gained_exp = int(battle.get("boss_missing_exp_reward", battle.get("extra_exp", 0)))
                event_line = (
                    "👑 Хранитель пути повержен!\n"
                    "Енотик доказал, что готов идти дальше.\n"
                    "Победа закрыла недостающий опыт до нового уровня.\n\n"
                    f"✨ Получено опыта: +{gained_exp}\n"
                    f"📌 Новый уровень: {battle.get('level_after', pet.get('level', 1))}\n"
                    "🗺 Открыта новая локация."
                )
            else:
                event_line = (
                    "👑 Хранитель пути повержен!\n"
                    "Путь дальше открыт, но енотику ещё нужно немного опыта."
                )
    item_lines = [
        f"• {ITEM_LABELS[item]} x{amount}"
        for item, amount in (battle.get("items_delta", {}) if isinstance(battle.get("items_delta"), dict) else {}).items()
        if isinstance(amount, int) and amount > 0 and item in ITEM_LABELS
    ]
    reward_block = _reward_block(
        int(battle.get("base_exp", 0)),
        int(battle.get("base_currency", 0)),
        empty_text="Награды нет.",
    )
    return (
        f"{TRAVEL_LOCATIONS.get(battle.get('location_id', ''), {}).get('button', '🌲 Локация')}\n\n"
        f"{pet_name} вернулся из прогулки, весь важный и немного в листьях.\n\n"
        "Потрачено:\n"
        f"• ⚡ Энергия: -{battle.get('spent_energy', 0)}\n"
        f"• 🍽 Сытость: -{battle.get('spent_satiety', 0)}\n"
        f"• 🧼 Чистота: -{battle.get('spent_cleanliness', 0)}\n\n"
        + reward_block
        + "\n\n"
        f"{event_line}\n\n"
        f"{section_title}\n"
        + "\n".join(section_lines)
        + ("\n\nДополнительно из события:\n" + "\n".join(item_lines) if item_lines else "")
        + level_up_line
        + _blocked_levelup_text(pet)
    )

@router.message(F.text == BTN_STATUS)
async def show_status(message: Message) -> None:
    if message.from_user is None:
        return
    refresh_user_metadata(message.from_user.id, message.from_user)
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    if isinstance(pet.get("battle"), dict):
        battle = pet["battle"]
        enemy = get_enemy(str(battle.get("enemy_id", "field_mouse")))
        chance = max(15, min(90, int(battle.get("win_chance", calculate_enemy_win_chance(pet, enemy)))))
        await message.answer(
            "⚠️ У енота уже есть активная стычка.\n\n"
            f"Противник: {enemy.get('name', 'Неизвестный враг')} {enemy.get('emoji', '')}\n"
            f"Шанс победы: {chance}%\n\n"
            "Выбери действие:",
            reply_markup=battle_menu_keyboard(),
        )
        return
    await send_optional_screen(message, "pet", _status_text(pet), reply_markup=pet_care_inline_keyboard())


@router.message(F.text == BTN_MY_RACCOON)
async def show_raccoon(message: Message) -> None:
    if message.from_user is None:
        return
    refresh_user_metadata(message.from_user.id, message.from_user)
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    await send_optional_screen(message, "pet", _raccoon_profile_text(pet), reply_markup=pet_care_inline_keyboard())


@router.message(Command("мой_енот"))
async def show_raccoon_group_command(message: Message) -> None:
    if message.from_user is None:
        return
    refresh_user_metadata(message.from_user.id, message.from_user)
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У вас пока нет енотика.")
        return
    await message.answer(_group_raccoon_profile_text(pet))


@router.message(F.text == BTN_INVENTORY)
async def show_inventory(message: Message) -> None:
    if message.from_user is None:
        return
    refresh_user_metadata(message.from_user.id, message.from_user)
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    await send_optional_screen(message, "inventory", _inventory_text(pet), reply_markup=main_menu_keyboard())


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


@router.message(F.text.in_({BTN_CONTACT_ADMIN, BTN_LETTER_TO_RACCOON}))
async def contact_admin_entry(message: Message, state: FSMContext) -> None:
    await state.set_state(AdminMessageState.waiting_for_admin_message)
    await send_optional_screen(
        message,
        "letter",
        "💌 Напишите свое анонимное желание, и ваш енотик передаст его ArtRaccoon)))\n\nДля отмены нажмите:\n❌ Отмена",
        reply_markup=cancel_keyboard(),
    )


@router.message(AdminMessageState.waiting_for_admin_message, F.text == BTN_CANCEL)
async def contact_admin_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Отправка письма отменена.", reply_markup=main_menu_keyboard())


@router.message(AdminMessageState.waiting_for_admin_message, F.text)
async def contact_admin_send(message: Message, state: FSMContext) -> None:
    if message.from_user is None or message.text is None:
        return
    if not ADMIN_IDS:
        await state.clear()
        await message.answer("Администрация сейчас недоступна.", reply_markup=main_menu_keyboard())
        return

    refresh_user_metadata(message.from_user.id, message.from_user)
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    pet_name = str(pet.get("name", "без питомца")) if isinstance(pet, dict) else "без питомца"
    pet_level = int(pet.get("level", 1)) if isinstance(pet, dict) and isinstance(pet.get("level", 1), int) else 1
    username = f"@{message.from_user.username}" if message.from_user.username else "без username"
    sender_text = (
        "💌 Енотик принес новое письмо\n\n"
        "👤 Пользователь:\n"
        f"• ID: {message.from_user.id}\n"
        f"• Username: {username}\n"
        f"• Имя питомца: {pet_name}\n"
        f"• Уровень: {pet_level}"
    )
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
    await send_optional_screen(
        message,
        "magic_and_sword",
        "⚔️ Магия и меч\n\n"
        "Енотик разложил у костра свитки, зелья и маленький тренировочный меч.\n\n"
        "Здесь можно подготовиться к путешествиям:\n"
        "прокачать навыки, использовать зелья и позже изучить магию.\n\n"
        "Выберите действие:",
        reply_markup=magic_and_sword_inline_keyboard(),
    )


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


@router.message(F.text == BTN_POTIONS)
async def potion_menu(message: Message) -> None:
    if message.from_user is None:
        return
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    inventory = pet.get("inventory", {}) if isinstance(pet.get("inventory"), dict) else {}
    await send_optional_screen(
        message,
        "potions",
        "🧪 Зелья\n\n"
        "Доступные зелья в инвентаре:\n"
        f"• ⚡ Малое зелье: {inventory.get('energy_potion', 0)}\n"
        f"• 🔋 Большое зелье: {inventory.get('big_energy_potion', 0)}\n\n"
        "Чтобы использовать зелье, выберите его кнопкой ниже.",
        reply_markup=care_menu_keyboard(),
    )


@router.message(F.text == BTN_MAGIC)
async def magic_placeholder(message: Message) -> None:
    await send_optional_screen(
        message,
        "magic_placeholder",
        "✨ Магия\n\n"
        "Магические свитки пока покрыты енотовыми каракулями.\n"
        "Этот раздел откроется позже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🔙 Назад")]],
            resize_keyboard=True,
        ),
    )


@router.message(F.text == "🔙 Назад")
async def magic_back(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await care_menu(message)


@router.message(F.text == BTN_SKILLS)
async def skills_menu(message: Message) -> None:
    if message.from_user is None:
        return
    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    await send_optional_screen(
        message,
        "skills",
        "📊 Навыки\n\n"
        f"💪 Сила: {pet.get('strength', 1)}\n"
        f"🤸 Ловкость: {pet.get('agility', 1)}\n"
        f"🧠 Инстинкт: {pet.get('instinct', 1)}\n\n"
        "Навыки помогают чаще побеждать в боях и увереннее встречать хранителей пути.",
        reply_markup=magic_and_sword_keyboard(),
    )


@router.callback_query(F.data == "magic_sword:train")
async def magic_sword_train_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message is None:
        return
    if callback.from_user is None or not _has_pet(callback.from_user.id):
        await callback.message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    await training_menu(callback.message)


@router.callback_query(F.data == "magic_sword:potions")
async def magic_sword_potions_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message is None:
        return
    await potion_menu(callback.message)


@router.callback_query(F.data == "magic_sword:magic")
async def magic_sword_magic_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message is None:
        return
    if callback.from_user is None or not _has_pet(callback.from_user.id):
        await callback.message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return
    await magic_placeholder(callback.message)


@router.callback_query(F.data == "magic_sword:skills")
async def magic_sword_skills_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message is None:
        return
    await skills_menu(callback.message)


@router.callback_query(F.data == "magic_sword:main")
async def magic_sword_main_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message is None:
        return
    if callback.from_user is not None:
        touch_user_needs(callback.from_user.id)
    await callback.message.answer("Главное меню", reply_markup=main_menu_keyboard())


def _has_pet(user_id: int) -> bool:
    user = get_user(user_id)
    return isinstance(user, dict) and isinstance(user.get("pet"), dict)


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
    level = pet.get("level", 1) if isinstance(pet.get("level"), int) else 1
    travel_buttons = _travel_buttons_for_level(level)
    await send_optional_screen(
        message,
        "travel",
        "🗺️ Путешествие\n\n"
        "Енотик принюхался к ветру и выбрал три тропы:\n"
        "одна спокойнее, одна по силам, а одна явно пахнет приключениями.\n\n"
        "Выберите маршрут:",
        reply_markup=travel_menu_keyboard(travel_buttons),
    )


@router.message(F.text == BTN_SHOP)
async def shop_menu(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await send_optional_screen(message, "shop", "🛒 Магазин", reply_markup=build_shop_keyboard())


@router.message(F.text == BTN_BACK)
async def back_to_main(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await send_optional_screen(message, "main_menu", "Главное меню:", reply_markup=main_menu_keyboard())


@router.message(F.text == BTN_SHOP_BACK)
async def back_from_shop(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await send_optional_screen(message, "main_menu", "Главное меню:", reply_markup=main_menu_keyboard())


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


async def _perform_care_action_for_user(user_id: int, item_key: str) -> tuple[bool, str]:
    catalog = get_item_catalog()
    item = catalog.get(item_key, {})
    success, _ = update_pet_need(user_id, inventory_item=item_key)
    if not success:
        return False, "Такого предмета нет в инвентаре. Загляни в магазин 🛒"
    if item_key == "toy":
        return True, f"Енот немного поиграл. Любовь +{item.get('restore', 0)}."
    return (
        True,
        f"Енот использовал {item.get('name', 'предмет').lower()} {item.get('emoji', '')}\n"
        f"{_need_label(item.get('need', ''))} +{item.get('restore', 0)}.",
    )


def _need_label(need: str) -> str:
    return {"satiety": "Сытость", "cleanliness": "Чистота", "love": "Любовь", "energy": "Энергия"}.get(need, "Параметр")


def _format_time_left(time_left: timedelta) -> str:
    total_seconds = max(0, int(time_left.total_seconds()))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours} ч {minutes} мин"


async def _refresh_pet_care_card(callback: CallbackQuery, pet: dict, result_text: str) -> None:
    message = callback.message
    if message is None:
        return

    updated_text = f"{result_text}\n\n{_status_text(pet)}"
    try:
        if message.photo:
            await message.edit_caption(caption=updated_text, reply_markup=pet_care_inline_keyboard())
            return
        await message.edit_text(updated_text, reply_markup=pet_care_inline_keyboard())
        return
    except TelegramBadRequest as exc:
        if "message is not modified" in str(exc).lower():
            return
    except TelegramAPIError:
        pass

    await message.answer(updated_text, reply_markup=pet_care_inline_keyboard())



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


@router.message(F.text == BTN_CARE_SLEEP)
async def care_sleep(message: Message) -> None:
    if message.from_user is None:
        return
    result = sleep_pet(message.from_user.id)
    if result.get("available"):
        await message.answer(
            "🌙 Енотик сладко поспал и восстановил силы.\n"
            "⚡ Энергия полностью восстановлена.",
            reply_markup=care_menu_keyboard(),
        )
        return
    time_left = result.get("time_left")
    formatted = _format_time_left(time_left) if isinstance(time_left, timedelta) else "неизвестно"
    await message.answer(
        "🌙 Енотик уже отдыхал сегодня.\n\n"
        f"Бесплатный сон будет доступен через: {formatted}.\n"
        "⚡ Энергия постепенно восстановится в течение дня.\n"
        "Также можно использовать зелья энергии.",
        reply_markup=care_menu_keyboard(),
    )


async def _handle_pet_care_callback_action(callback: CallbackQuery, action: str) -> None:
    if callback.from_user is None:
        await callback.answer()
        return
    user = touch_user_needs(callback.from_user.id) or get_user(callback.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await callback.message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        await callback.answer()
        return

    action_to_item = {"feed": "food", "clean": "soap", "play": "toy"}
    if action in action_to_item:
        _, text = await _perform_care_action_for_user(callback.from_user.id, action_to_item[action])
        pet_state = (touch_user_needs(callback.from_user.id) or get_user(callback.from_user.id) or {}).get("pet", pet)
        await _refresh_pet_care_card(callback, pet_state if isinstance(pet_state, dict) else pet, f"✅ {text}")
        await callback.answer()
        return
    if action == "sleep":
        result = sleep_pet(callback.from_user.id)
        if result.get("available"):
            pet_state = (touch_user_needs(callback.from_user.id) or get_user(callback.from_user.id) or {}).get("pet", pet)
            await _refresh_pet_care_card(
                callback,
                pet_state if isinstance(pet_state, dict) else pet,
                "😴 Енотик сладко поспал.\nЭнергия восстановлена.",
            )
            await callback.answer()
            return
        time_left = result.get("time_left")
        formatted = _format_time_left(time_left) if isinstance(time_left, timedelta) else "неизвестно"
        pet_state = (touch_user_needs(callback.from_user.id) or get_user(callback.from_user.id) or {}).get("pet", pet)
        await _refresh_pet_care_card(
            callback,
            pet_state if isinstance(pet_state, dict) else pet,
            "😴 Сон пока недоступен.\n"
            f"Бесплатный сон будет доступен через: {formatted}.\n"
            "Энергия также постепенно восстановится в течение дня, или можно использовать зелья.",
        )
        await callback.answer()
        return
    if action == "menu":
        await send_optional_screen(callback.message, "main_menu", "Главное меню:", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("pet_care:"))
async def pet_care_inline_action(callback: CallbackQuery) -> None:
    action = callback.data.split(":", 1)[1] if callback.data else ""
    await _handle_pet_care_callback_action(callback, action)


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

    user = touch_user_needs(message.from_user.id) or get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return

    level = pet.get("level", 1) if isinstance(pet.get("level"), int) else 1
    available = _travel_buttons_for_level(level)
    allowed_ids = _travel_location_ids_for_level(level)
    if location_id not in allowed_ids:
        await message.answer("Этот маршрут уже недоступен. Откройте путешествия заново.", reply_markup=travel_menu_keyboard(available))
        return

    success, levels_gained, missing, user, location, event, result = perform_travel(message.from_user.id, location_id, allow_above_level=True)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("У тебя пока нет енота. Нажми /start, чтобы создать питомца.")
        return

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
    reward_block = _reward_block(int(spent.get("exp", 0)), int(spent.get("currency", 0)))
    text = (
        f"🌲 {location_name}\n\n"
        "Енот вернулся из прогулки, весь важный и немного в листьях.\n\n"
        "Потрачено:\n"
        f"• ⚡ Энергия: -{spent.get('energy', 0)}\n"
        f"• 🍽 Сытость: -{spent.get('satiety', 0)}\n"
        f"• 🧼 Чистота: -{spent.get('cleanliness', 0)}"
        + (f"\n\n{reward_block}" if reward_block else "")
        + "\n\n"
        + _travel_event_line(event if isinstance(event, dict) else None)
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
        await send_optional_screen(message, "shop", "Категория недоступна.", reply_markup=build_shop_keyboard())
        return
    items = get_shop_items_by_category(category_id)
    prepared_items = [{**item, "emoji": _resolve_shop_emoji(str(item.get("id", "")), str(item.get("name", "")))} for item in items]
    screen_key = f"shop_{category_id}"
    await send_optional_screen(
        message,
        screen_key,
        _shop_category_text(category, prepared_items),
        reply_markup=build_shop_item_keyboard(category_id, prepared_items),
    )


@router.callback_query(F.data.startswith("shop_back:"))
async def shop_back_to_categories(callback: CallbackQuery) -> None:
    if callback.message is None:
        return
    await send_optional_screen(callback.message, "shop", "🛒 Магазин", reply_markup=build_shop_keyboard())
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
