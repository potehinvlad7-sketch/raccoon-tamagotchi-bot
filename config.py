import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
PROXY_URL = os.getenv("PROXY_URL", "").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Please configure it in environment variables.")
