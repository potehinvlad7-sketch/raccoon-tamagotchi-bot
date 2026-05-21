import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"

DEFAULT_NEEDS = {
    "satiety": 80,
    "cleanliness": 80,
    "love": 80,
    "energy": 80,
}

DEFAULT_INVENTORY = {
    "food": 3,
    "soap": 2,
    "toy": 2,
    "energy_potion": 1,
    "hearty_snack": 0,
    "forest_honey": 0,
    "fluffy_shampoo": 0,
    "comb": 0,
    "yarn_ball": 0,
    "fun_toy": 0,
    "big_energy_potion": 0,
    "strength_scroll": 0,
    "agility_scroll": 0,
    "instinct_scroll": 0,
}
DEFAULT_SKILLS = {
    "strength": 0,
    "agility": 0,
    "instinct": 0,
}
DEFAULT_TRAVEL = {
    "total_travels": 0,
    "last_event": None,
}
DEFAULT_BATTLE = None
NEEDS_TICK_MINUTES = 30

TRAVEL_LOCATIONS = {
    "forest_clearing": {"button": "🌿 Лесная поляна", "name": "Лесная поляна", "min_level": 1, "costs": {"energy": 15, "satiety": 8, "cleanliness": 4}, "rewards": {"exp": 8, "currency": 4}},
    "quiet_thicket": {"button": "🌲 Тихая чаща", "name": "Тихая чаща", "min_level": 1, "costs": {"energy": 20, "satiety": 10, "cleanliness": 5}, "rewards": {"exp": 10, "currency": 5}},
    "mushroom_path": {"button": "🍄 Грибная тропа", "name": "Грибная тропа", "min_level": 2, "costs": {"energy": 23, "satiety": 12, "cleanliness": 6}, "rewards": {"exp": 12, "currency": 6}},
    "old_deadfall": {"button": "🪵 Старый бурелом", "name": "Старый бурелом", "min_level": 3, "costs": {"energy": 26, "satiety": 14, "cleanliness": 8}, "rewards": {"exp": 15, "currency": 8}},
    "misty_stream": {"button": "💧 Туманный ручей", "name": "Туманный ручей", "min_level": 5, "costs": {"energy": 30, "satiety": 16, "cleanliness": 10}, "rewards": {"exp": 20, "currency": 10}},
    "stone_ravine": {"button": "🪨 Каменный овраг", "name": "Каменный овраг", "min_level": 7, "costs": {"energy": 35, "satiety": 18, "cleanliness": 12}, "rewards": {"exp": 25, "currency": 13}},
    "forest_ruins": {"button": "🏚 Лесные руины", "name": "Лесные руины", "min_level": 10, "costs": {"energy": 42, "satiety": 22, "cleanliness": 16}, "rewards": {"exp": 35, "currency": 18}},
}

TRAVEL_EVENTS = [
    {"id": "berry_cache", "type": "good", "text": "Енот нашёл под листьями горсть сладких ягод 🍓", "effects": {"currency": 2, "items": {"food": 1}}},
    {"id": "shiny_button", "type": "good", "text": "В мху блеснула старая пуговица. Енот решил, что это сокровище ✨", "effects": {"currency": 5}},
    {"id": "honey_smell", "type": "good", "text": "Енот учуял запах дикого мёда и принёс липкую добычу 🍯", "effects": {"items": {"forest_honey": 1}}},
    {"id": "clean_spring", "type": "good", "text": "У ручья енот умылся так важно, будто готовился к портрету 💧", "effects": {"needs": {"cleanliness": 15}}},
    {"id": "warm_sun_patch", "type": "good", "text": "На солнечной кочке енот немного отдохнул и снова приободрился ☀️", "effects": {"needs": {"energy": 10}}},
    {"id": "moss_inspection", "type": "neutral", "text": "Енот долго изучал мох. Научного вывода нет, но выглядело серьёзно 🌿", "effects": {}},
    {"id": "suspicious_stump", "type": "neutral", "text": "Енот поспорил с подозрительным пнём. Пень не ответил 🪵", "effects": {}},
    {"id": "owl_watched", "type": "neutral", "text": "С ветки за ним наблюдала сова. Енот сделал вид, что так и задумано 🦉", "effects": {}},
    {"id": "lost_tracks", "type": "neutral", "text": "Следы вывели к луже и внезапно закончились 🐾", "effects": {}},
    {"id": "rustle_in_bushes", "type": "neutral", "text": "В кустах что-то шуршало. Енот шуршал в ответ 🌲", "effects": {}},
    {"id": "muddy_paws", "type": "bad", "text": "Енот провалился лапами в мокрую землю 🐾", "effects": {"needs": {"cleanliness": -15}}},
    {"id": "thorny_bush", "type": "bad", "text": "Колючий куст оказался сильнее енотовой гордости 🌿", "effects": {"needs": {"love": -8, "energy": -5}}},
    {"id": "snack_lost", "type": "bad", "text": "Пока енот изучал корягу, перекус куда-то исчез 🍎", "effects": {"needs": {"satiety": -10}}},
    {"id": "loud_crack", "type": "bad", "text": "В лесу громко треснула ветка. Енот решил, что приключений достаточно 😳", "effects": {"needs": {"energy": -12}}},
    {"id": "rain_cloud", "type": "bad", "text": "Маленькая туча выбрала именно этого енота ☔", "effects": {"needs": {"cleanliness": -10, "love": -5}}},
    {"id": "strength_scroll_find", "type": "rare", "text": "Под корнем лежал старый свиток с грубым знаком лапы 📜", "effects": {"items": {"strength_scroll": 1}}},
    {"id": "agility_scroll_find", "type": "rare", "text": "Между камней енот нашёл тонкий свиток с рисунком бегущего хвоста 📜", "effects": {"items": {"agility_scroll": 1}}},
    {"id": "instinct_scroll_find", "type": "rare", "text": "На бересте проступали странные следы. Это оказался свиток инстинкта 📜", "effects": {"items": {"instinct_scroll": 1}}},
]

ENEMY_CATALOG = {
    "field_mouse": {"id": "field_mouse", "name": "Полевая мышь", "emoji": "🐭", "difficulty": 2, "skills": {"agility": 2, "instinct": 1}},
    "angry_crow": {"id": "angry_crow", "name": "Сердитая ворона", "emoji": "🐦‍⬛", "difficulty": 3, "skills": {"agility": 1, "instinct": 2}},
    "mushroom_goblin": {"id": "mushroom_goblin", "name": "Грибной пакостник", "emoji": "🍄", "difficulty": 5, "skills": {"instinct": 2, "strength": 1}},
    "thorn_hog": {"id": "thorn_hog", "name": "Колючий хрюк", "emoji": "🦔", "difficulty": 7, "skills": {"strength": 2, "agility": 1}},
    "swamp_rat": {"id": "swamp_rat", "name": "Болотная крыса", "emoji": "🐀", "difficulty": 10, "skills": {"instinct": 2, "agility": 1}},
    "stone_marten": {"id": "stone_marten", "name": "Каменная куница", "emoji": "🐾", "difficulty": 13, "skills": {"agility": 2, "strength": 1}},
    "ruin_owl": {"id": "ruin_owl", "name": "Руинная сова", "emoji": "🦉", "difficulty": 18, "skills": {"instinct": 2, "agility": 1}},
}

LOCATION_ENEMIES = {
    "forest_clearing": ["field_mouse", "angry_crow"],
    "quiet_thicket": ["field_mouse", "angry_crow", "mushroom_goblin"],
    "mushroom_path": ["mushroom_goblin", "thorn_hog"],
    "old_deadfall": ["thorn_hog", "swamp_rat"],
    "misty_stream": ["swamp_rat", "stone_marten"],
    "stone_ravine": ["stone_marten", "ruin_owl"],
    "forest_ruins": ["ruin_owl"],
}

ENEMY_TEXTS = {
    "field_mouse": {"event": "🐭 Полевая мышь выскочила из травы и попыталась утащить находку.", "win": "Енот распушил хвост, сделал важный выпад и победил.", "lose": "Мышь юркнула в кусты, а енот остался озадаченно шуршать листвой."},
    "angry_crow": {"event": "🐦‍⬛ Сердитая ворона налетела сверху и громко потребовала всё блестящее.", "win": "Енот ловко отскочил, шикнул на ворону и отстоял добычу.", "lose": "Енот героически сделал вид, что это была тактическая прогулка назад."},
    "mushroom_goblin": {"event": "🍄 Грибной пакостник вынырнул из пней и начал дразнить енота.", "win": "Енот перехитрил пакостника и прогнал его в чащу.", "lose": "Пакостник насыпал спор в нос, и енот отступил, чихая."},
    "thorn_hog": {"event": "🦔 Колючий хрюк преградил тропу и упрямо засопел.", "win": "Енот обошёл колючки, сделал рывок и победил.", "lose": "Хрюк боднул воздух так грозно, что енот решил не спорить."},
    "swamp_rat": {"event": "🐀 Болотная крыса устроила грязную засаду у воды.", "win": "Енот увернулся от брызг и выгнал крысу с берега.", "lose": "Крыса обдала енота болотной жижей, и бой сорвался."},
    "stone_marten": {"event": "🐾 Каменная куница скользнула по камням и бросилась в атаку.", "win": "Енот точно рассчитал момент и перехватил инициативу.", "lose": "Куница оказалась слишком быстрой, енот едва ушёл от погони."},
    "ruin_owl": {"event": "🦉 Руинная сова бесшумно спикировала из древних арок.", "win": "Енот выдержал жуткий взгляд и заставил сову отступить.", "lose": "Сова кругами нагнала страху, и енот спешно ретировался."},
}


ITEM_CATALOG = {
    "food": {"name": "Яблоко", "emoji": "🍎", "category": "food", "need": "satiety", "restore": 50, "price": 5},
    "hearty_snack": {"name": "Сытный перекус", "emoji": "🥪", "category": "food", "need": "satiety", "restore": 90, "price": 12},
    "forest_honey": {"name": "Лесной мёд", "emoji": "🍯", "category": "food", "need": "satiety", "restore": 140, "price": 22},
    "soap": {"name": "Мыло", "emoji": "🧼", "category": "cleanliness", "need": "cleanliness", "restore": 50, "price": 7},
    "fluffy_shampoo": {"name": "Пушистый шампунь", "emoji": "🫧", "category": "cleanliness", "need": "cleanliness", "restore": 90, "price": 14},
    "comb": {"name": "Гребень", "emoji": "🪮", "category": "cleanliness", "need": "cleanliness", "restore": 35, "price": 4},
    "toy": {"name": "Мячик", "emoji": "🎾", "category": "love", "need": "love", "restore": 50, "price": 8},
    "yarn_ball": {"name": "Клубок", "emoji": "🧶", "category": "love", "need": "love", "restore": 80, "price": 14},
    "fun_toy": {"name": "Забавная игрушка", "emoji": "🪀", "category": "love", "need": "love", "restore": 120, "price": 24},
    "energy_potion": {"name": "Малое зелье энергии", "emoji": "⚡", "category": "energy", "need": "energy", "restore": 50, "price": 12},
    "big_energy_potion": {"name": "Большое зелье энергии", "emoji": "🔋", "category": "energy", "need": "energy", "restore": 100, "price": 25},
}

SHOP_CATEGORIES = {
    "food": {"id": "food", "title": "Еда", "emoji": "🍖", "description": "Что-то вкусное для голодного енота."},
    "household": {"id": "household", "title": "Быт", "emoji": "🧺", "description": "Полезные вещи для чистоты и уюта."},
    "toys": {"id": "toys", "title": "Игрушки", "emoji": "🧸", "description": "Предметы для игр и хорошего настроения."},
    "potions": {"id": "potions", "title": "Зелья", "emoji": "🧪", "description": "Зелья для восстановления сил."},
    "weapons": {"id": "weapons", "title": "Оружие", "emoji": "🗡️", "description": "Будущий раздел боевого снаряжения."},
    "armor": {"id": "armor", "title": "Броня", "emoji": "🛡️", "description": "Будущий раздел защитного снаряжения."},
    "accessories": {"id": "accessories", "title": "Аксессуары", "emoji": "💍", "description": "Будущий раздел редких аксессуаров."},
    "materials": {"id": "materials", "title": "Материалы", "emoji": "🪵", "description": "Будущий раздел ресурсов для крафта."},
}

SHOP_ITEMS = {
    "food": {"id": "food", "category": "food", "name": "Яблоко", "description": "Сочное лесное яблоко.", "price": 5, "effects": {"satiety": 50}},
    "hearty_snack": {"id": "hearty_snack", "category": "food", "name": "Сытный перекус", "description": "Плотный перекус для долгих прогулок.", "price": 12, "effects": {"satiety": 90}},
    "forest_honey": {"id": "forest_honey", "category": "food", "name": "Лесной мёд", "description": "Сладкий мёд, найденный в чаще.", "price": 22, "effects": {"satiety": 140}},
    "soap": {"id": "soap", "category": "household", "name": "Мыло", "description": "Помогает быстро отмыть лапки и хвост.", "price": 7, "effects": {"cleanliness": 50}},
    "fluffy_shampoo": {"id": "fluffy_shampoo", "category": "household", "name": "Пушистый шампунь", "description": "Ароматный шампунь для идеальной шерсти.", "price": 14, "effects": {"cleanliness": 90}},
    "comb": {"id": "comb", "category": "household", "name": "Гребень", "description": "Простой гребень для быстрой укладки.", "price": 4, "effects": {"cleanliness": 35}},
    "toy": {"id": "toy", "category": "toys", "name": "Мячик", "description": "Любимая игрушка для весёлой игры.", "price": 8, "effects": {"love": 50}},
    "yarn_ball": {"id": "yarn_ball", "category": "toys", "name": "Клубок", "description": "Мягкий клубок для долгих игр.", "price": 14, "effects": {"love": 80}},
    "fun_toy": {"id": "fun_toy", "category": "toys", "name": "Забавная игрушка", "description": "Яркая игрушка, поднимающая настроение.", "price": 24, "effects": {"love": 120}},
    "energy_potion": {"id": "energy_potion", "category": "potions", "name": "Малое зелье энергии", "description": "Быстро возвращает силы после дел.", "price": 12, "effects": {"energy": 50}},
    "big_energy_potion": {"id": "big_energy_potion", "category": "potions", "name": "Большое зелье энергии", "description": "Мощное зелье для полного заряда.", "price": 25, "effects": {"energy": 100}},
}


def update_pet_mood(pet: dict[str, Any]) -> str:
    max_needs = get_pet_max_needs(pet)
    satiety = int(pet.get("satiety", DEFAULT_NEEDS["satiety"]))
    cleanliness = int(pet.get("cleanliness", DEFAULT_NEEDS["cleanliness"]))
    love = int(pet.get("love", DEFAULT_NEEDS["love"]))
    energy = int(pet.get("energy", DEFAULT_NEEDS["energy"]))

    if satiety < max_needs["satiety"] * 0.2 or cleanliness < max_needs["cleanliness"] * 0.2 or love < max_needs["love"] * 0.2:
        mood = "distressed"
    elif satiety < max_needs["satiety"] * 0.4 or cleanliness < max_needs["cleanliness"] * 0.4 or love < max_needs["love"] * 0.4 or energy < max_needs["energy"] * 0.2:
        mood = "tired"
    elif satiety >= max_needs["satiety"] * 0.8 and cleanliness >= max_needs["cleanliness"] * 0.8 and love >= max_needs["love"] * 0.8 and energy >= max_needs["energy"] * 0.6:
        mood = "happy"
    else:
        mood = "normal"

    pet["mood"] = mood
    return mood


def get_runaway_risk(pet: dict[str, Any]) -> str:
    love = int(pet.get("love", DEFAULT_NEEDS["love"]))
    love_max = get_pet_max_needs(pet)["love"]
    if love < love_max * 0.15:
        return "high"
    if love < love_max * 0.30:
        return "medium"
    if love < love_max * 0.45:
        return "low"
    return "none"


def utc_now() -> datetime:
    return datetime.now(UTC)


def parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _ensure_storage_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}", encoding="utf-8")


def clamp_need(value: int) -> int:
    return max(0, min(100, value))


def get_max_need_value(level: int) -> int:
    safe_level = level if isinstance(level, int) and level > 0 else 1
    return 100 + (safe_level - 1) * 17


def get_pet_max_needs(pet: dict[str, Any]) -> dict[str, int]:
    level = pet.get("level", 1) if isinstance(pet, dict) else 1
    max_value = get_max_need_value(level if isinstance(level, int) else 1)
    return {"satiety": max_value, "cleanliness": max_value, "love": max_value, "energy": max_value}


def clamp_need_by_level(pet: dict[str, Any], need: str, value: int) -> int:
    need_max = get_pet_max_needs(pet).get(need, 100)
    return max(0, min(need_max, value))


def ensure_pet_defaults(user_data: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    changed = False
    pet = user_data.get("pet")
    if not isinstance(pet, dict):
        return user_data, changed

    for key, default in DEFAULT_NEEDS.items():
        if not isinstance(pet.get(key), int):
            pet[key] = default
            changed = True

    if not isinstance(pet.get("level"), int) or int(pet.get("level", 0)) < 1:
        pet["level"] = 1
        changed = True
    if not isinstance(pet.get("exp"), int) or int(pet.get("exp", 0)) < 0:
        pet["exp"] = 0
        changed = True
    if not isinstance(pet.get("currency"), int) or int(pet.get("currency", 0)) < 0:
        pet["currency"] = 0
        changed = True

    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        pet["inventory"] = DEFAULT_INVENTORY.copy()
        changed = True
    else:
        for item, default in DEFAULT_INVENTORY.items():
            if not isinstance(inventory.get(item), int):
                inventory[item] = default
                changed = True

    skills = pet.get("skills")
    if not isinstance(skills, dict):
        pet["skills"] = DEFAULT_SKILLS.copy()
        changed = True
    else:
        for skill, default in DEFAULT_SKILLS.items():
            if not isinstance(skills.get(skill), int):
                skills[skill] = default
                changed = True

    travel = pet.get("travel")
    if not isinstance(travel, dict):
        pet["travel"] = DEFAULT_TRAVEL.copy()
        changed = True
    else:
        if not isinstance(travel.get("total_travels"), int):
            travel["total_travels"] = DEFAULT_TRAVEL["total_travels"]
            changed = True
        if not (isinstance(travel.get("last_event"), str) or travel.get("last_event") is None):
            travel["last_event"] = DEFAULT_TRAVEL["last_event"]
            changed = True
    if "battle" not in pet:
        pet["battle"] = DEFAULT_BATTLE
        changed = True

    updated_at = parse_datetime(pet.get("updated_at"))
    if updated_at is None:
        updated_at = utc_now()
        pet["updated_at"] = updated_at.isoformat()
        changed = True

    if parse_datetime(pet.get("last_needs_update_at")) is None:
        pet["last_needs_update_at"] = updated_at.isoformat()
        changed = True
    if not isinstance(pet.get("mood"), str):
        pet["mood"] = "normal"
        changed = True

    for need in DEFAULT_NEEDS:
        current = pet.get(need, DEFAULT_NEEDS[need])
        if isinstance(current, int):
            clamped = clamp_need_by_level(pet, need, current)
            if clamped != current:
                pet[need] = clamped
                changed = True

    return user_data, changed


def apply_elapsed_need_ticks(pet: dict[str, Any], ticks: int) -> None:
    if ticks <= 0:
        return
    pet["satiety"] = clamp_need_by_level(pet, "satiety", int(pet.get("satiety", 0)) - (2 * ticks))
    pet["cleanliness"] = clamp_need_by_level(pet, "cleanliness", int(pet.get("cleanliness", 0)) - (1 * ticks))
    pet["love"] = clamp_need_by_level(pet, "love", int(pet.get("love", 0)) - (1 * ticks))
    pet["energy"] = clamp_need_by_level(pet, "energy", int(pet.get("energy", 0)) + (3 * ticks))


def recalculate_needs(user_data: dict[str, Any]) -> bool:
    user_data, changed = ensure_pet_defaults(user_data)
    pet = user_data.get("pet")
    if not isinstance(pet, dict):
        return changed

    last_update = parse_datetime(pet.get("last_needs_update_at"))
    if last_update is None:
        last_update = utc_now()
        pet["last_needs_update_at"] = last_update.isoformat()
        return True

    now = utc_now()
    elapsed = now - last_update
    tick_seconds = NEEDS_TICK_MINUTES * 60
    ticks = int(elapsed.total_seconds() // tick_seconds)
    if ticks <= 0:
        update_pet_mood(pet)
        return changed

    apply_elapsed_need_ticks(pet, ticks)
    update_pet_mood(pet)
    pet["last_needs_update_at"] = (last_update + timedelta(seconds=ticks * tick_seconds)).isoformat()
    return True


def load_users() -> dict[str, Any]:
    _ensure_storage_file()

    raw = USERS_FILE.read_text(encoding="utf-8").strip()
    if not raw:
        return {}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        return {}

    return data


def save_users(users: dict[str, Any]) -> None:
    _ensure_storage_file()
    USERS_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")


def get_user(user_id: int) -> dict[str, Any] | None:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return None

    user, changed = ensure_pet_defaults(user)
    if changed:
        users[str(user_id)] = user
        save_users(users)

    return user


def touch_user_needs(user_id: int) -> dict[str, Any] | None:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return None

    needs_changed = recalculate_needs(user)
    if needs_changed:
        users[str(user_id)] = user
        save_users(users)
    return user




def refresh_user_metadata_from_chat(user_id: int, chat: Any) -> dict[str, Any]:
    users = load_users()
    key = str(user_id)
    user = users.get(key)
    if not isinstance(user, dict):
        user = {}

    username = getattr(chat, "username", None)
    first_name = getattr(chat, "first_name", None)
    last_name = getattr(chat, "last_name", None)
    is_bot = getattr(chat, "is_bot", None)

    user["username"] = username if isinstance(username, str) else None
    user["first_name"] = first_name if isinstance(first_name, str) else None
    user["last_name"] = last_name if isinstance(last_name, str) else None
    if isinstance(is_bot, bool):
        user["is_bot"] = is_bot

    language_code = getattr(chat, "language_code", None)
    if isinstance(language_code, str):
        user["language_code"] = language_code

    user["last_seen_at"] = utc_now().isoformat()

    users[key] = user
    save_users(users)
    return user


def refresh_user_metadata(user_id: int, telegram_user: Any) -> dict[str, Any]:
    return refresh_user_metadata_from_chat(user_id, telegram_user)

def has_pet(user_id: int) -> bool:
    user = get_user(user_id)
    return bool(user and isinstance(user.get("pet"), dict))


def create_pet(user_id: int, name: str, gender: str) -> dict[str, Any]:
    users = load_users()
    now = utc_now().isoformat()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        user = {}
    user["pet"] = {
            "name": name,
            "gender": gender,
            "level": 1,
            "exp": 0,
            "currency": 0,
            "mood": "normal",
            "satiety": DEFAULT_NEEDS["satiety"],
            "cleanliness": DEFAULT_NEEDS["cleanliness"],
            "love": DEFAULT_NEEDS["love"],
            "energy": DEFAULT_NEEDS["energy"],
            "skills": DEFAULT_SKILLS.copy(),
            "inventory": DEFAULT_INVENTORY.copy(),
            "travel": DEFAULT_TRAVEL.copy(),
            "created_at": now,
            "updated_at": now,
            "last_needs_update_at": now,
        }
    users[str(user_id)] = user
    save_users(users)
    return users[str(user_id)]


def consume_inventory_item(pet: dict[str, Any], item: str) -> bool:
    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        return False

    count = inventory.get(item)
    if not isinstance(count, int) or count <= 0:
        return False

    inventory[item] = count - 1
    return True


def get_item_catalog() -> dict[str, dict[str, Any]]:
    return {key: value.copy() for key, value in ITEM_CATALOG.items()}


def get_shop_items() -> dict[str, int]:
    return {key: item["price"] for key, item in SHOP_ITEMS.items()}


def get_shop_categories() -> dict[str, dict[str, Any]]:
    return {key: value.copy() for key, value in SHOP_CATEGORIES.items() if key in {"food", "household", "toys", "potions"}}


def get_shop_items_by_category(category_id: str) -> list[dict[str, Any]]:
    return [item.copy() for item in SHOP_ITEMS.values() if item.get("category") == category_id]


def get_shop_item(item_id: str) -> dict[str, Any] | None:
    item = SHOP_ITEMS.get(item_id)
    return item.copy() if isinstance(item, dict) else None


def can_afford(currency: int, price: int) -> bool:
    return currency >= price


def add_inventory_item(pet: dict[str, Any], item: str, amount: int = 1) -> int:
    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        pet["inventory"] = DEFAULT_INVENTORY.copy()
        inventory = pet["inventory"]

    current = inventory.get(item, 0)
    current_count = current if isinstance(current, int) and current >= 0 else 0
    inventory[item] = current_count + amount
    return inventory[item]


def buy_item(user_data: dict[str, Any], item_key: str) -> tuple[bool, int, int]:
    user_data, _ = ensure_pet_defaults(user_data)
    recalculate_needs(user_data)
    pet = user_data.get("pet")
    if not isinstance(pet, dict):
        return False, 0, 0

    price = SHOP_ITEMS.get(item_key, {}).get("price")
    if not isinstance(price, int):
        return False, 0, 0

    currency = pet.get("currency", 0)
    currency_value = currency if isinstance(currency, int) and currency >= 0 else 0
    pet["currency"] = currency_value

    if not can_afford(currency_value, price):
        count = int(pet.get("inventory", {}).get(item_key, 0)) if isinstance(pet.get("inventory"), dict) else 0
        return False, currency_value, count

    pet["currency"] = currency_value - price
    new_count = add_inventory_item(pet, item_key, amount=1)
    pet["updated_at"] = utc_now().isoformat()
    return True, pet["currency"], new_count


def shop_purchase(user_id: int, item_key: str) -> tuple[bool, int, int, int, dict[str, Any] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, 0, 0, None

    items = get_shop_items()
    price = items.get(item_key, 0)
    success, balance, count = buy_item(user, item_key)

    users[str(user_id)] = user
    save_users(users)
    return success, price, balance, count, user


def update_pet_need(user_id: int, need: str | None = None, amount: int | None = None, inventory_item: str = "") -> tuple[bool, dict[str, Any] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, None

    changed = recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, None

    item_data = ITEM_CATALOG.get(inventory_item)
    resolved_need = item_data.get("need") if isinstance(item_data, dict) else need
    resolved_amount = item_data.get("restore") if isinstance(item_data, dict) else amount

    if not isinstance(resolved_need, str) or not isinstance(resolved_amount, int):
        if changed:
            users[str(user_id)] = user
            save_users(users)
        return False, None

    if not consume_inventory_item(pet, inventory_item):
        if changed:
            users[str(user_id)] = user
            save_users(users)
        return False, user

    current_value = pet.get(resolved_need, 0)
    if not isinstance(current_value, int):
        current_value = 0

    pet[resolved_need] = clamp_need_by_level(pet, resolved_need, current_value + resolved_amount)
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, user


def has_enough_energy(pet: dict[str, Any], amount: int) -> bool:
    energy = pet.get("energy", 0)
    return isinstance(energy, int) and energy >= amount


def exp_to_next_level(level: int) -> int:
    safe_level = level if isinstance(level, int) and level > 0 else 1
    return 50 + (safe_level - 1) * 25


def apply_level_ups(pet: dict[str, Any]) -> int:
    level = pet.get("level", 1)
    exp = pet.get("exp", 0)
    currency = pet.get("currency", 0)

    pet["level"] = level if isinstance(level, int) and level > 0 else 1
    pet["exp"] = exp if isinstance(exp, int) and exp >= 0 else 0
    pet["currency"] = currency if isinstance(currency, int) and currency >= 0 else 0

    levels_gained = 0
    while pet["exp"] >= exp_to_next_level(pet["level"]):
        required = exp_to_next_level(pet["level"])
        pet["exp"] -= required
        pet["level"] += 1
        pet["currency"] += 10
        levels_gained += 1

    return levels_gained


def add_exp(pet: dict[str, Any], amount: int) -> int:
    safe_amount = amount if isinstance(amount, int) and amount > 0 else 0
    current_exp = pet.get("exp", 0)
    pet["exp"] = (current_exp if isinstance(current_exp, int) and current_exp >= 0 else 0) + safe_amount
    return apply_level_ups(pet)


def train_skill(user_id: int, skill_name: str) -> tuple[bool, int, dict[str, Any] | None, str | None]:
    if skill_name not in DEFAULT_SKILLS:
        return False, 0, None, None

    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, None, None

    recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, 0, None, None

    if not has_enough_energy(pet, 15):
        users[str(user_id)] = user
        save_users(users)
        return False, 0, user, None

    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        inventory = DEFAULT_INVENTORY.copy()
        pet["inventory"] = inventory

    scroll_by_skill = {"strength": "strength_scroll", "agility": "agility_scroll", "instinct": "instinct_scroll"}
    scroll_key = scroll_by_skill[skill_name]
    scroll_count = inventory.get(scroll_key, 0)
    if not isinstance(scroll_count, int) or scroll_count < 1:
        users[str(user_id)] = user
        save_users(users)
        return False, 0, user, scroll_key

    skills = pet.get("skills")
    if not isinstance(skills, dict):
        pet["skills"] = DEFAULT_SKILLS.copy()
        skills = pet["skills"]

    skill_value = skills.get(skill_name, 0)
    if not isinstance(skill_value, int):
        skill_value = 0

    skills[skill_name] = skill_value + 1
    pet["energy"] = clamp_need_by_level(pet, "energy", int(pet.get("energy", 0)) - 15)
    inventory[scroll_key] = scroll_count - 1
    levels_gained = add_exp(pet, 5)
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, levels_gained, user, scroll_key


def get_travel_locations() -> dict[str, dict[str, Any]]:
    return TRAVEL_LOCATIONS


def get_travel_event(event_id: str) -> dict[str, Any] | None:
    for event in TRAVEL_EVENTS:
        if event.get("id") == event_id:
            return event
    return None


def calculate_enemy_win_chance(pet: dict[str, Any], enemy: dict[str, Any]) -> int:
    skills = pet.get("skills", {}) if isinstance(pet.get("skills"), dict) else {}
    strength = skills.get("strength", 0) if isinstance(skills.get("strength"), int) else 0
    agility = skills.get("agility", 0) if isinstance(skills.get("agility"), int) else 0
    instinct = skills.get("instinct", 0) if isinstance(skills.get("instinct"), int) else 0
    pet_level = pet.get("level", 1) if isinstance(pet.get("level"), int) else 1
    difficulty = enemy.get("difficulty", 1) if isinstance(enemy.get("difficulty"), int) else 1

    base = 50
    skill_score = int(strength * 2 + agility * 1.5 + instinct * 1.5)
    difficulty_penalty = difficulty * 4
    level_bonus = pet_level * 2
    chance = base + skill_score + level_bonus - difficulty_penalty
    return max(15, min(90, chance))


def choose_travel_event(pet: dict[str, Any], location_id: str) -> dict[str, Any]:
    skills = pet.get("skills")
    instinct = skills.get("instinct", 0) if isinstance(skills, dict) else 0
    weights = {"good": 24, "neutral": 28, "bad": 14, "rare": 4, "enemy": 30}
    if isinstance(instinct, int) and instinct >= 7:
        weights = {"good": 30, "neutral": 33, "bad": 12, "rare": 5, "enemy": 20}
    elif isinstance(instinct, int) and instinct >= 3:
        weights = {"good": 27, "neutral": 31, "bad": 13, "rare": 4, "enemy": 25}

    event_types = list(weights.keys())
    chosen_type = random.choices(event_types, weights=[weights[t] for t in event_types], k=1)[0]
    if chosen_type == "enemy":
        available = LOCATION_ENEMIES.get(location_id, [])
        enemy_id = random.choice(available) if available else "field_mouse"
        enemy = ENEMY_CATALOG.get(enemy_id, ENEMY_CATALOG["field_mouse"])
        texts = ENEMY_TEXTS.get(enemy_id, ENEMY_TEXTS["field_mouse"])
        return {
            "id": f"enemy_{enemy_id}",
            "type": "enemy",
            "enemy_id": enemy_id,
            "text": texts["event"],
            "enemy": enemy,
            "win_text": texts["win"],
            "lose_text": texts["lose"],
        }

    pool = [event for event in TRAVEL_EVENTS if event.get("type") == chosen_type]
    return random.choice(pool)


def perform_travel(user_id: int, location_id: str) -> tuple[bool, int, list[str], dict[str, Any] | None, dict[str, Any] | None, dict[str, Any] | None, dict[str, int] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, ["pet is missing"], None, None, None, None

    recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, 0, ["pet is missing"], None, None, None, None
    if isinstance(pet.get("battle"), dict):
        return False, 0, ["battle_pending"], user, None, None, None

    location = TRAVEL_LOCATIONS.get(location_id)
    if not isinstance(location, dict):
        return False, 0, ["unknown location"], user, None, None, None

    level = pet.get("level", 1) if isinstance(pet.get("level"), int) else 1
    if level < location.get("min_level", 1):
        return False, 0, [f"level >= {location.get('min_level', 1)}"], user, location, None, None

    costs = location.get("costs", {})
    missing = []
    for need in ("energy", "satiety", "cleanliness"):
        required = int(costs.get(need, 0))
        current = pet.get(need, 0)
        if not isinstance(current, int) or current < required:
            missing.append(f"{need} >= {required}")
    if missing:
        users[str(user_id)] = user
        save_users(users)
        return False, 0, missing, user, location, None, None

    spent = {k: int(v) for k, v in costs.items() if isinstance(v, int)}
    for need, value in spent.items():
        pet[need] = clamp_need_by_level(pet, need, int(pet.get(need, 0)) - value)

    rewards = location.get("rewards", {})
    base_exp = int(rewards.get("exp", 0))
    base_currency = int(rewards.get("currency", 0))
    pet["currency"] = int(pet.get("currency", 0)) + base_currency if isinstance(pet.get("currency"), int) else base_currency
    levels_gained = add_exp(pet, base_exp)

    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        pet["inventory"] = DEFAULT_INVENTORY.copy()
        inventory = pet["inventory"]

    event = choose_travel_event(pet, location_id)
    effects = event.get("effects", {}) if isinstance(event.get("effects"), dict) else {}
    event_exp = int(effects.get("exp", 0)) if isinstance(effects.get("exp", 0), int) else 0
    event_currency = int(effects.get("currency", 0)) if isinstance(effects.get("currency", 0), int) else 0
    if event_exp:
        levels_gained += add_exp(pet, event_exp)
    if event_currency:
        pet["currency"] = int(pet.get("currency", 0)) + event_currency if isinstance(pet.get("currency"), int) else event_currency

    for need, delta in (effects.get("needs", {}) if isinstance(effects.get("needs"), dict) else {}).items():
        if isinstance(delta, int):
            pet[need] = clamp_need_by_level(pet, need, int(pet.get(need, 0)) + delta)

    items_delta = {}
    for item, amount in (effects.get("items", {}) if isinstance(effects.get("items"), dict) else {}).items():
        if isinstance(amount, int):
            current = inventory.get(item, 0)
            inventory[item] = (current if isinstance(current, int) else 0) + amount
            items_delta[item] = amount

    enemy_result = {"win": False, "chance": 0, "roll": 0, "extra_exp": 0, "extra_currency": 0, "penalties": {}, "drop_items": {}}
    if event.get("type") == "enemy":
        enemy = event.get("enemy", {}) if isinstance(event.get("enemy"), dict) else {}
        chance = calculate_enemy_win_chance(pet, enemy)
        pet["battle"] = {
            "enemy_id": event.get("enemy_id", "field_mouse"),
            "location_id": location_id,
            "win_chance": chance,
            "travel_context": {
                "location_id": location_id,
                "base_exp": base_exp,
                "base_currency": base_currency,
                "event_id": None,
                "spent_energy": spent.get("energy", 0),
                "spent_satiety": spent.get("satiety", 0),
                "spent_cleanliness": spent.get("cleanliness", 0),
                "items_delta": items_delta,
                "levels_gained": levels_gained,
            },
            "created_at": utc_now().isoformat(),
        }
        enemy_result["pending"] = True
        enemy_result["chance"] = chance

    travel = pet.get("travel")
    if not isinstance(travel, dict):
        pet["travel"] = DEFAULT_TRAVEL.copy()
        travel = pet["travel"]
    travel["total_travels"] = int(travel.get("total_travels", 0)) + 1
    travel["last_event"] = f"Встреча: {event.get('enemy', {}).get('name', 'Неизвестный враг')}" if event.get("type") == "enemy" else event.get("id")

    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, levels_gained, [], user, location, event, {"exp": base_exp, "currency": base_currency, "event_exp": event_exp, "event_currency": event_currency, "enemy_result": enemy_result, **spent, **items_delta}


def get_enemy(enemy_id: str) -> dict[str, Any]:
    return ENEMY_CATALOG.get(enemy_id, ENEMY_CATALOG["field_mouse"])


def resolve_battle_attack(user_id: int) -> tuple[bool, dict[str, Any] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, None
    recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, None
    battle = pet.get("battle")
    if not isinstance(battle, dict):
        users[str(user_id)] = user
        save_users(users)
        return False, user
    enemy = get_enemy(str(battle.get("enemy_id", "field_mouse")))
    chance = max(15, min(90, int(battle.get("win_chance", calculate_enemy_win_chance(pet, enemy)))))
    win = random.randint(1, 100) <= chance
    difficulty = enemy.get("difficulty", 1) if isinstance(enemy.get("difficulty"), int) else 1
    inventory = pet.get("inventory") if isinstance(pet.get("inventory"), dict) else DEFAULT_INVENTORY.copy()
    pet["inventory"] = inventory
    travel_context = battle.get("travel_context", {}) if isinstance(battle.get("travel_context"), dict) else {}
    result = {"win": win, "chance": chance, "enemy": enemy, "drop_items": {}, "levels_gained": 0, "travel_context": travel_context, "pet": pet, "pet_name": pet.get("name", "Енот")}
    if win:
        extra_exp = difficulty + 2
        extra_currency = max(2, difficulty)
        result["levels_gained"] = add_exp(pet, extra_exp)
        result["travel_context"]["levels_gained"] = int(result["travel_context"].get("levels_gained", 0)) + result["levels_gained"]
        pet["currency"] = int(pet.get("currency", 0)) + extra_currency if isinstance(pet.get("currency"), int) else extra_currency
        result["extra_exp"] = extra_exp
        result["extra_currency"] = extra_currency
        if random.random() < 0.22:
            drop_item = random.choice(["food", "soap", "toy", "energy_potion", "hearty_snack", "comb"])
            inventory[drop_item] = int(inventory.get(drop_item, 0)) + 1
            result["drop_items"][drop_item] = 1
        if random.random() < 0.10:
            scroll = random.choice(["strength_scroll", "agility_scroll", "instinct_scroll"])
            inventory[scroll] = int(inventory.get(scroll, 0)) + 1
            result["drop_items"][scroll] = result["drop_items"].get(scroll, 0) + 1
    else:
        extra = difficulty // 3
        penalties = {"energy": -(10 + extra), "cleanliness": -(8 + extra), "love": -(6 + extra), "satiety": -(4 + extra)}
        for need, delta in penalties.items():
            pet[need] = clamp_need_by_level(pet, need, int(pet.get(need, 0)) + delta)
        result["penalties"] = penalties
    pet["battle"] = None
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, result


def resolve_battle_run(user_id: int) -> tuple[bool, dict[str, Any] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, None
    recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, None
    battle = pet.get("battle")
    if not isinstance(battle, dict):
        users[str(user_id)] = user
        save_users(users)
        return False, user
    enemy = get_enemy(str(battle.get("enemy_id", "field_mouse")))
    difficulty = enemy.get("difficulty", 1) if isinstance(enemy.get("difficulty"), int) else 1
    skills = pet.get("skills", {}) if isinstance(pet.get("skills"), dict) else {}
    agility = skills.get("agility", 0) if isinstance(skills.get("agility"), int) else 0
    instinct = skills.get("instinct", 0) if isinstance(skills.get("instinct"), int) else 0
    flee_chance = max(20, min(90, 55 + agility * 3 + instinct - difficulty * 7))
    escaped = random.randint(1, 100) <= flee_chance
    penalties = {"energy": -8} if escaped else {"energy": -14, "cleanliness": -7, "love": -5}
    for need, delta in penalties.items():
        pet[need] = clamp_need_by_level(pet, need, int(pet.get(need, 0)) + delta)
    pet["battle"] = None
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    travel_context = battle.get("travel_context", {}) if isinstance(battle.get("travel_context"), dict) else {}
    return True, {"escaped": escaped, "enemy": enemy, "flee_chance": flee_chance, "penalties": penalties, "travel_context": travel_context, "pet": pet, "pet_name": pet.get("name", "Енот")}


def get_storage_stats() -> dict[str, float | int | str]:
    users = load_users()
    total_users = len(users)
    users_with_pet = 0
    total_pets = 0
    levels_sum = 0

    for user_data in users.values():
        if not isinstance(user_data, dict):
            continue
        pet = user_data.get("pet")
        if not isinstance(pet, dict):
            continue

        users_with_pet += 1
        total_pets += 1
        level = pet.get("level", 1)
        safe_level = level if isinstance(level, int) and level > 0 else 1
        levels_sum += safe_level

    average_level = (levels_sum / total_pets) if total_pets else 0.0
    return {
        "total_users": total_users,
        "users_with_pet": users_with_pet,
        "total_pets": total_pets,
        "average_level": round(average_level, 1),
        "storage_path": str(USERS_FILE),
    }


def create_users_backup() -> tuple[bool, str]:
    _ensure_storage_file()
    backups_dir = DATA_DIR / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)

    source = USERS_FILE
    if not source.exists():
        return False, "Файл хранилища не найден."

    timestamp = utc_now().strftime("%Y%m%d_%H%M%S")
    backup_path = backups_dir / f"users_{timestamp}.json"
    backup_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return True, str(backup_path)


def get_all_users() -> list[tuple[int, dict[str, Any]]]:
    users = load_users()
    rows: list[tuple[int, dict[str, Any]]] = []
    changed = False
    for key, value in users.items():
        try:
            user_id = int(key)
        except (ValueError, TypeError):
            continue
        if not isinstance(value, dict):
            continue
        value, user_changed = ensure_pet_defaults(value)
        if user_changed:
            users[key] = value
            changed = True
        rows.append((user_id, value))
    if changed:
        save_users(users)
    rows.sort(key=lambda item: item[0])
    return rows


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    return get_user(user_id)


def admin_update_pet_value(user_id: int, field: str, delta: int) -> tuple[bool, int, int]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, 0
    user, _ = ensure_pet_defaults(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, 0, 0

    target = pet
    key = field
    if "." in field:
        prefix, key = field.split(".", 1)
        nested = pet.get(prefix)
        if not isinstance(nested, dict):
            nested = {}
            pet[prefix] = nested
        target = nested

    current = target.get(key, 0)
    before = current if isinstance(current, int) else 0
    if field == "exp":
        before = int(pet.get("exp", 0)) if isinstance(pet.get("exp"), int) else 0
        add_exp(pet, delta)
        after = int(pet.get("exp", 0)) if isinstance(pet.get("exp"), int) else 0
    elif field == "level":
        before = int(pet.get("level", 1)) if isinstance(pet.get("level"), int) else 1
        pet["level"] = max(1, before + delta)
        after = pet["level"]
    else:
        target[key] = before + delta
        after = target[key]

    for need in DEFAULT_NEEDS:
        pet[need] = clamp_need_by_level(pet, need, int(pet.get(need, DEFAULT_NEEDS[need])))
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, before, after


def admin_add_currency(user_id: int, amount: int) -> tuple[bool, int, int]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, 0
    user, _ = ensure_pet_defaults(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, 0, 0
    before = int(pet.get("currency", 0)) if isinstance(pet.get("currency"), int) else 0
    pet["currency"] = max(0, before + amount)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, before, pet["currency"]


def admin_add_inventory_item(user_id: int, item_key: str, amount: int = 1) -> tuple[bool, int, int]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, 0
    user, _ = ensure_pet_defaults(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, 0, 0
    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        pet["inventory"] = DEFAULT_INVENTORY.copy()
        inventory = pet["inventory"]
    before = inventory.get(item_key, 0) if isinstance(inventory.get(item_key), int) else 0
    inventory[item_key] = max(0, before + amount)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, before, inventory[item_key]


def admin_restore_needs(user_id: int) -> bool:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False
    user, _ = ensure_pet_defaults(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False
    max_needs = get_pet_max_needs(pet)
    for need, max_value in max_needs.items():
        pet[need] = max_value
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True


def admin_clear_battle(user_id: int) -> bool:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False
    user, _ = ensure_pet_defaults(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False
    if not isinstance(pet.get("battle"), dict):
        return False
    pet["battle"] = None
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True
