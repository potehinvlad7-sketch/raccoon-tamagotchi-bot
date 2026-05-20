from aiogram import F, Router
from aiogram.types import Message

from keyboards import care_menu_keyboard, main_menu_keyboard, shop_menu_keyboard, training_menu_keyboard, travel_menu_keyboard
from storage import (
    exp_to_next_level,
    get_runaway_risk,
    get_shop_items,
    get_user,
    perform_short_forest_trip,
    shop_purchase,
    touch_user_needs,
    train_skill,
    update_pet_mood,
    update_pet_need,
)


router = Router()


def _status_text(pet: dict) -> str:
    mood = update_pet_mood(pet)
    runaway_risk = get_runaway_risk(pet)
    warning_line = "⚠️ Your raccoon needs more love.\n" if runaway_risk in {"medium", "high"} else ""
    inventory = pet.get("inventory", {}) if isinstance(pet.get("inventory"), dict) else {}
    skills = pet.get("skills", {}) if isinstance(pet.get("skills"), dict) else {}
    travel = pet.get("travel", {}) if isinstance(pet.get("travel"), dict) else {}
    last_event = travel.get("last_event")
    last_event_line = f"Last travel: {last_event}\n" if isinstance(last_event, str) and last_event else ""
    level = pet.get("level", 1)
    safe_level = level if isinstance(level, int) and level > 0 else 1
    exp = pet.get("exp", 0)
    safe_exp = exp if isinstance(exp, int) and exp >= 0 else 0
    need_exp = exp_to_next_level(safe_level)
    return (
        "🐾 Raccoon Status\n"
        f"Name: {pet.get('name', '-')}\n"
        f"Gender: {pet.get('gender', '-')}\n"
        f"Level: {safe_level}\n"
        f"EXP: {safe_exp} / {need_exp}\n"
        f"Currency: {pet.get('currency', 0)}\n"
        f"Mood: {mood}\n"
        f"Runaway risk: {runaway_risk}\n"
        f"{warning_line}"
        f"Satiety: {pet.get('satiety', 80)}/100\n"
        f"Cleanliness: {pet.get('cleanliness', 80)}/100\n"
        f"Love: {pet.get('love', 80)}/100\n"
        f"Energy: {pet.get('energy', 80)}/100\n\n"
        "💪 Skills\n"
        f"Strength: {skills.get('strength', 0)}  "
        f"Agility: {skills.get('agility', 0)}  "
        f"Instinct: {skills.get('instinct', 0)}\n"
        f"Travels: {travel.get('total_travels', 0)}\n"
        f"{last_event_line}\n"
        "Needs update automatically over elapsed time.\n\n"
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
    user = touch_user_needs(message.from_user.id) or user
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
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await message.answer("Choose a care action:", reply_markup=care_menu_keyboard())


@router.message(F.text == "Training")
async def training_menu(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await message.answer("Choose a training:", reply_markup=training_menu_keyboard())


@router.message(F.text == "Travel")
async def travel_menu(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await message.answer("Choose travel:", reply_markup=travel_menu_keyboard())


@router.message(F.text == "Shop")
async def shop_menu(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
    await message.answer("Choose an item to buy:", reply_markup=shop_menu_keyboard())


@router.message(F.text == "Back to main menu")
async def back_to_main(message: Message) -> None:
    if message.from_user is not None:
        touch_user_needs(message.from_user.id)
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


async def _train(message: Message, skill_name: str, label: str) -> None:
    if message.from_user is None:
        return

    trained, levels_gained, user = train_skill(message.from_user.id, skill_name)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("You do not have a raccoon yet. Send /start to create one.")
        return

    if not trained:
        await message.answer(
            "Your raccoon is too tired for training now. Let it rest a little!",
            reply_markup=training_menu_keyboard(),
        )
        return

    level_up_line = f"\nLevel up! Your raccoon reached level {pet.get('level', 1)}." if levels_gained > 0 else ""
    await message.answer(
        f"{label} training completed! (+1 {label}, +5 EXP, -15 energy){level_up_line}\n\n{_status_text(pet)}",
        reply_markup=training_menu_keyboard(),
    )


@router.message(F.text == "Train Strength")
async def train_strength(message: Message) -> None:
    await _train(message, "strength", "Strength")


@router.message(F.text == "Train Agility")
async def train_agility(message: Message) -> None:
    await _train(message, "agility", "Agility")


@router.message(F.text == "Train Instinct")
async def train_instinct(message: Message) -> None:
    await _train(message, "instinct", "Instinct")


@router.message(F.text == "Short Forest Trip")
async def short_forest_trip(message: Message) -> None:
    if message.from_user is None:
        return

    success, levels_gained, missing, user = perform_short_forest_trip(message.from_user.id)
    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("You do not have a raccoon yet. Send /start to create one.")
        return

    if not success:
        await message.answer(
            "Your raccoon is not ready for travel yet.\nNeeded: " + ", ".join(missing),
            reply_markup=travel_menu_keyboard(),
        )
        return

    last_event = pet.get("travel", {}).get("last_event", "Travel completed!")
    level_up_line = f"\nLevel up! Your raccoon reached level {pet.get('level', 1)}." if levels_gained > 0 else ""
    await message.answer(
        "Short forest trip completed!\n"
        "Costs: -20 energy, -10 satiety, -5 cleanliness\n"
        "Rewards: +10 EXP, +5 currency\n"
        f"{level_up_line}\n"
        f"Event: {last_event}\n\n"
        f"{_status_text(pet)}",
        reply_markup=travel_menu_keyboard(),
    )


async def _buy_item_action(message: Message, item_key: str, item_label: str) -> None:
    if message.from_user is None:
        return

    prices = get_shop_items()
    price = prices.get(item_key, 0)
    success, _, balance, count, user = shop_purchase(message.from_user.id, item_key)

    if not success:
        await message.answer(
            f"Not enough currency for {item_label}. Price: {price}. Your balance: {balance}.",
            reply_markup=shop_menu_keyboard(),
        )
        return

    pet = (user or {}).get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        await message.answer("Purchase completed.", reply_markup=shop_menu_keyboard())
        return

    await message.answer(
        f"Bought {item_label} for {price} currency!\n"
        f"Balance: {balance}\n"
        f"{item_label} in inventory: {count}",
        reply_markup=shop_menu_keyboard(),
    )


@router.message(F.text == "Buy Food")
async def buy_food(message: Message) -> None:
    await _buy_item_action(message, "food", "Food")


@router.message(F.text == "Buy Soap")
async def buy_soap(message: Message) -> None:
    await _buy_item_action(message, "soap", "Soap")


@router.message(F.text == "Buy Toy")
async def buy_toy(message: Message) -> None:
    await _buy_item_action(message, "toy", "Toy")


@router.message(F.text == "Buy Energy Potion")
async def buy_energy_potion(message: Message) -> None:
    await _buy_item_action(message, "energy_potion", "Energy potion")
