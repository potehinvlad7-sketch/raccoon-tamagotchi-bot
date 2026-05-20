import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
PROXY_URL = os.getenv("PROXY_URL", "").strip()


def _parse_admin_ids(raw_value: str) -> set[int]:
    if not raw_value:
        return set()

    admin_ids: set[int] = set()
    for part in raw_value.split(","):
        value = part.strip()
        if not value:
            continue
        try:
            admin_ids.add(int(value))
        except ValueError:
            continue
    return admin_ids


ADMIN_IDS = _parse_admin_ids(os.getenv("ADMIN_IDS", "").strip())


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Please configure it in environment variables.")
