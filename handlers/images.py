from __future__ import annotations

from pathlib import Path

from aiogram.exceptions import TelegramAPIError, TelegramBadRequest
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InputMediaPhoto, Message, ReplyKeyboardMarkup

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


def _is_editable_error(exc: TelegramBadRequest) -> bool:
    lowered = str(exc).lower()
    return any(token in lowered for token in [
        "message is not modified",
        "there is no text in the message to edit",
        "message can't be edited",
        "message to edit not found",
    ])


async def edit_or_send_screen(
    source: CallbackQuery | Message,
    screen_key: str,
    text: str,
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
    parse_mode: str | None = None,
) -> None:
    message = source.message if isinstance(source, CallbackQuery) else source
    if message is None:
        return

    image_path = SCREEN_IMAGES.get(screen_key)
    image_file = Path(image_path) if image_path else None
    has_image = bool(image_file and image_file.exists() and image_file.is_file())

    try:
        if has_image and isinstance(reply_markup, InlineKeyboardMarkup):
            await message.edit_media(
                media=InputMediaPhoto(media=FSInputFile(image_file), caption=text, parse_mode=parse_mode),
                reply_markup=reply_markup,
            )
            return
        await message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        return
    except TelegramBadRequest as exc:
        if not _is_editable_error(exc):
            raise
    except TelegramAPIError:
        pass

    await send_optional_screen(message, screen_key, text, reply_markup=reply_markup)
