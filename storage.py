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
NEEDS_TICK_MINUTES = 30


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


def ensure_pet_defaults(user_data: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    changed = False
    pet = user_data.get("pet")
    if not isinstance(pet, dict):
        return user_data, changed

    for key, default in DEFAULT_NEEDS.items():
        if not isinstance(pet.get(key), int):
            pet[key] = default
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

    updated_at = parse_datetime(pet.get("updated_at"))
    if updated_at is None:
        updated_at = utc_now()
        pet["updated_at"] = updated_at.isoformat()
        changed = True

    if parse_datetime(pet.get("last_needs_update_at")) is None:
        pet["last_needs_update_at"] = updated_at.isoformat()
        changed = True

    return user_data, changed


def apply_elapsed_need_ticks(pet: dict[str, Any], ticks: int) -> None:
    if ticks <= 0:
        return
    pet["satiety"] = clamp_need(int(pet.get("satiety", 0)) - (2 * ticks))
    pet["cleanliness"] = clamp_need(int(pet.get("cleanliness", 0)) - (1 * ticks))
    pet["love"] = clamp_need(int(pet.get("love", 0)) - (1 * ticks))
    pet["energy"] = clamp_need(int(pet.get("energy", 0)) + (3 * ticks))


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
        return changed

    apply_elapsed_need_ticks(pet, ticks)
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


def has_pet(user_id: int) -> bool:
    user = get_user(user_id)
    return bool(user and isinstance(user.get("pet"), dict))


def create_pet(user_id: int, name: str, gender: str) -> dict[str, Any]:
    users = load_users()
    now = utc_now().isoformat()
    users[str(user_id)] = {
        "pet": {
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
    }
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


def update_pet_need(user_id: int, need: str, amount: int, inventory_item: str) -> bool:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False

    changed = recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False

    if not consume_inventory_item(pet, inventory_item):
        if changed:
            users[str(user_id)] = user
            save_users(users)
        return False

    current_value = pet.get(need, 0)
    if not isinstance(current_value, int):
        current_value = 0

    pet[need] = clamp_need(current_value + amount)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True


def has_enough_energy(pet: dict[str, Any], amount: int) -> bool:
    energy = pet.get("energy", 0)
    return isinstance(energy, int) and energy >= amount


def train_skill(user_id: int, skill_name: str) -> tuple[bool, dict[str, Any] | None]:
    if skill_name not in DEFAULT_SKILLS:
        return False, None

    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, None

    recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, None

    if not has_enough_energy(pet, 15):
        users[str(user_id)] = user
        save_users(users)
        return False, user

    skills = pet.get("skills")
    if not isinstance(skills, dict):
        pet["skills"] = DEFAULT_SKILLS.copy()
        skills = pet["skills"]

    skill_value = skills.get(skill_name, 0)
    if not isinstance(skill_value, int):
        skill_value = 0

    skills[skill_name] = skill_value + 1
    pet["energy"] = clamp_need(int(pet.get("energy", 0)) - 15)
    exp = pet.get("exp", 0)
    pet["exp"] = (exp if isinstance(exp, int) else 0) + 5
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, user


def can_travel(pet: dict[str, Any]) -> tuple[bool, list[str]]:
    missing: list[str] = []
    energy = pet.get("energy", 0)
    satiety = pet.get("satiety", 0)
    cleanliness = pet.get("cleanliness", 0)

    if not isinstance(energy, int) or energy < 20:
        missing.append("energy >= 20")
    if not isinstance(satiety, int) or satiety < 20:
        missing.append("satiety >= 20")
    if not isinstance(cleanliness, int) or cleanliness < 15:
        missing.append("cleanliness >= 15")
    return len(missing) == 0, missing


def choose_travel_event(pet: dict[str, Any]) -> str:
    skills = pet.get("skills")
    instinct = skills.get("instinct", 0) if isinstance(skills, dict) else 0
    if isinstance(instinct, int) and instinct >= 3:
        weights = [35, 55, 10]
    else:
        weights = [30, 50, 20]
    return random.choices(["good", "neutral", "bad"], weights=weights, k=1)[0]


def apply_travel_event(pet: dict[str, Any], event_type: str) -> str:
    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        pet["inventory"] = DEFAULT_INVENTORY.copy()
        inventory = pet["inventory"]

    if event_type == "good":
        food = inventory.get("food", 0)
        inventory["food"] = (food if isinstance(food, int) else 0) + 1
        currency = pet.get("currency", 0)
        pet["currency"] = (currency if isinstance(currency, int) else 0) + 3
        return "Raccoon found extra berries."
    if event_type == "bad":
        pet["cleanliness"] = clamp_need(int(pet.get("cleanliness", 0)) - 10)
        return "Raccoon got muddy."
    return "Peaceful walk through the forest."


def perform_short_forest_trip(user_id: int) -> tuple[bool, list[str], dict[str, Any] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, ["pet is missing"], None

    recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, ["pet is missing"], None

    allowed, missing = can_travel(pet)
    if not allowed:
        users[str(user_id)] = user
        save_users(users)
        return False, missing, user

    pet["energy"] = clamp_need(int(pet.get("energy", 0)) - 20)
    pet["satiety"] = clamp_need(int(pet.get("satiety", 0)) - 10)
    pet["cleanliness"] = clamp_need(int(pet.get("cleanliness", 0)) - 5)
    pet["exp"] = int(pet.get("exp", 0)) + 10 if isinstance(pet.get("exp"), int) else 10
    pet["currency"] = int(pet.get("currency", 0)) + 5 if isinstance(pet.get("currency"), int) else 5

    travel = pet.get("travel")
    if not isinstance(travel, dict):
        pet["travel"] = DEFAULT_TRAVEL.copy()
        travel = pet["travel"]

    travels = travel.get("total_travels", 0)
    travel["total_travels"] = (travels if isinstance(travels, int) else 0) + 1

    event_type = choose_travel_event(pet)
    event_text = apply_travel_event(pet, event_type)
    travel["last_event"] = event_text

    pet["cleanliness"] = clamp_need(int(pet.get("cleanliness", 0)))
    pet["satiety"] = clamp_need(int(pet.get("satiety", 0)))
    pet["energy"] = clamp_need(int(pet.get("energy", 0)))
    pet["love"] = clamp_need(int(pet.get("love", 0)))
    pet["updated_at"] = utc_now().isoformat()

    users[str(user_id)] = user
    save_users(users)
    return True, [], user
