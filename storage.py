import json
from datetime import UTC, datetime
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

    return user_data, changed


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


def has_pet(user_id: int) -> bool:
    user = get_user(user_id)
    return bool(user and isinstance(user.get("pet"), dict))


def create_pet(user_id: int, name: str, gender: str) -> dict[str, Any]:
    users = load_users()
    now = datetime.now(UTC).isoformat()
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
            "inventory": DEFAULT_INVENTORY.copy(),
            "created_at": now,
            "updated_at": now,
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

    user, changed = ensure_pet_defaults(user)
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
    pet["updated_at"] = datetime.now(UTC).isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True
