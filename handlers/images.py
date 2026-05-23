from __future__ import annotations

from pathlib import Path

from aiogram.exceptions import TelegramAPIError
from aiogram.types import FSInputFile, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup

SCREEN_IMAGES: dict[str, str] = {
    "start": "assets/images/start.jpg",
    "main_menu": "assets/images/main_menu.jpg",
    "pet": "assets/images/pet.jpg",
    "inventory": "assets/images/inventory.jpg",
    "shop": "assets/images/shop.jpg",
    "travel": "assets/images/travel.jpg",
    "letter": "assets/images/letter.jpg",
    "admin": "assets/images/admin.jpg",
    "shop_food": "assets/images/shop_food.jpg",
    "shop_household": "assets/images/shop_household.jpg",
    "shop_toys": "assets/images/shop_toys.jpg",
    "shop_potions": "assets/images/shop_potions.jpg",
}


async def send_optional_screen(
    target: Message,
    screen_key: str,
    text: str,
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
) -> None:
    image_path = SCREEN_IMAGES.get(screen_key)
    if image_path:
        file_path = Path(image_path)
        if file_path.exists() and file_path.is_file():
            try:
                await target.answer_photo(
                    photo=FSInputFile(file_path),
                    caption=text,
                    reply_markup=reply_markup,
                )
                return
            except TelegramAPIError:
                pass
    await target.answer(text, reply_markup=reply_markup)
