from aiogram import F, Router
from aiogram.types import Message

from keyboards import care_menu_keyboard, main_menu_keyboard
from storage import get_user, update_pet_need


router = Router()


def _status_text(pet: dict) -> str:
    inventory = pet.get("inventory", {}) if isinstance(pet.get("inventory"), dict) else {}
    return (
        "🐾 Raccoon Status\n"
        f"Name: {pet.get('name', '-')}\n"
        f"Gender: {pet.get('gender', '-')}\n"
        f"Level: {pet.get('level', 1)}\n"
        f"EXP: {pet.get('exp', 0)}\n"
        f"Currency: {pet.get('currency', 0)}\n"
        f"Mood: {pet.get('mood', 'normal')}\n"
        f"Satiety: {pet.get('satiety', 80)}/100\n"
        f"Cleanliness: {pet.get('cleanliness', 80)}/100\n"
        f"Love: {pet.get('love', 80)}/100\n"
        f"Energy: {pet.get('energy', 80)}/100\n\n"
        "🎒 Inventory\n"
        f"Food: {inventory.get('food', 0)}\n"
        f"Soap: {inventory.get('soap', 0)}\n"
        f"Toy: {inventory.get('toy', 0)}\n"
        f"Energy potion: {inventory.get('energy_potion', 0)}"
    )


@router.message(F.text == "Status")
async def show_status(message: Message) -> None:
    if message.from_user is None:
        return

    user = get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None

    if not isinstance(pet, dict):
        await message.answer("You do not have a raccoon yet. Send /start to create one.")
        return

    await message.answer(_status_text(pet), reply_markup=main_menu_keyboard())


@router.message(F.text == "My Raccoon")
async def show_raccoon(message: Message) -> None:
    await show_status(message)


@router.message(F.text == "Help")
async def show_help(message: Message) -> None:
    await message.answer(
        "Use /start to create your raccoon.\n"
        "Use Status to view full pet stats and inventory.\n"
        "Use Care to feed, clean, play, or restore energy.",
        reply_markup=main_menu_keyboard(),
    )


@router.message(F.text == "Care")
async def care_menu(message: Message) -> None:
    await message.answer("Choose a care action:", reply_markup=care_menu_keyboard())


@router.message(F.text == "Back to main menu")
async def back_to_main(message: Message) -> None:
    await message.answer("Main menu:", reply_markup=main_menu_keyboard())


async def _perform_care_action(
    message: Message,
    need: str,
    amount: int,
    item: str,
    action_name: str,
    missing_message: str,
) -> None:
    if message.from_user is None:
        return

    success = update_pet_need(message.from_user.id, need=need, amount=amount, inventory_item=item)
    if not success:
        await message.answer(missing_message, reply_markup=care_menu_keyboard())
        return

    user = get_user(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("Action completed.", reply_markup=care_menu_keyboard())
        return

    await message.answer(
        f"{action_name} completed!\n\n{_status_text(pet)}",
        reply_markup=care_menu_keyboard(),
    )


@router.message(F.text == "Feed")
async def care_feed(message: Message) -> None:
    await _perform_care_action(
        message,
        need="satiety",
        amount=20,
        item="food",
        action_name="Feeding",
        missing_message="No food left right now. Let's find some food later!",
    )


@router.message(F.text == "Clean")
async def care_clean(message: Message) -> None:
    await _perform_care_action(
        message,
        need="cleanliness",
        amount=20,
        item="soap",
        action_name="Cleaning",
        missing_message="No soap available now. Time to restock soon!",
    )


@router.message(F.text == "Play")
async def care_play(message: Message) -> None:
    await _perform_care_action(
        message,
        need="love",
        amount=20,
        item="toy",
        action_name="Playtime",
        missing_message="No toy available right now. Your raccoon still loves you!",
    )


@router.message(F.text == "Energy potion")
async def care_energy(message: Message) -> None:
    await _perform_care_action(
        message,
        need="energy",
        amount=30,
        item="energy_potion",
        action_name="Energy boost",
        missing_message="No energy potions left. Save one for next time!",
    )
