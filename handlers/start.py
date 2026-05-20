from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from keyboards import gender_keyboard, main_menu_keyboard
from storage import create_pet, has_pet


router = Router()


class PetCreation(StatesGroup):
    choosing_gender = State()
    entering_name = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    if has_pet(message.from_user.id):
        await state.clear()
        await message.answer("Welcome back! Main menu:", reply_markup=main_menu_keyboard())
        return

    await state.set_state(PetCreation.choosing_gender)
    await message.answer("Choose your raccoon gender:", reply_markup=gender_keyboard())


@router.message(PetCreation.choosing_gender, F.text.in_({"male", "female"}))
async def choose_gender(message: Message, state: FSMContext) -> None:
    if message.text is None:
        return

    await state.update_data(gender=message.text)
    await state.set_state(PetCreation.entering_name)
    await message.answer("Great! Now enter your raccoon's name:")


@router.message(PetCreation.choosing_gender)
async def choose_gender_invalid(message: Message) -> None:
    await message.answer("Please choose gender using buttons: male or female.")


@router.message(PetCreation.entering_name)
async def enter_name(message: Message, state: FSMContext) -> None:
    if message.from_user is None or message.text is None:
        return

    name = message.text.strip()
    if not name:
        await message.answer("Name cannot be empty. Please enter a valid name.")
        return

    data = await state.get_data()
    gender = data.get("gender")
    if gender not in {"male", "female"}:
        await state.set_state(PetCreation.choosing_gender)
        await message.answer("Let's choose gender again:", reply_markup=gender_keyboard())
        return

    create_pet(message.from_user.id, name=name, gender=gender)
    await state.clear()

    await message.answer(
        f"Your raccoon {name} ({gender}) has been created!",
        reply_markup=main_menu_keyboard(),
    )
    await message.answer("Main menu:", reply_markup=main_menu_keyboard())
