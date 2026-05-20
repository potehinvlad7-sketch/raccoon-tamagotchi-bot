from aiogram import F, Router
from aiogram.types import Message

from keyboards import main_menu_keyboard
from storage import get_user


router = Router()


@router.message(F.text == "Status")
async def show_status(message: Message) -> None:
    if message.from_user is None:
        return

    user = get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None

    if not isinstance(pet, dict):
        await message.answer("You do not have a raccoon yet. Send /start to create one.")
        return

    status_text = (
        "🐾 Raccoon Status\n"
        f"Name: {pet.get('name', '-') }\n"
        f"Gender: {pet.get('gender', '-') }\n"
        f"Level: {pet.get('level', 1)}\n"
        f"EXP: {pet.get('exp', 0)}\n"
        f"Currency: {pet.get('currency', 0)}\n"
        f"Mood: {pet.get('mood', 'normal')}"
    )
    await message.answer(status_text, reply_markup=main_menu_keyboard())


@router.message(F.text == "My Raccoon")
async def show_raccoon(message: Message) -> None:
    await show_status(message)


@router.message(F.text == "Help")
async def show_help(message: Message) -> None:
    await message.answer(
        "Use /start to create your raccoon.\n"
        "Use Status to view pet stats.\n"
        "Use My Raccoon to view the same status screen.",
        reply_markup=main_menu_keyboard(),
    )
