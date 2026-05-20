import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Any


DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"


def _ensure_storage_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}", encoding="utf-8")


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
    return user if isinstance(user, dict) else None


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
            "created_at": now,
            "updated_at": now,
        }
    }
    save_users(users)
    return users[str(user_id)]
