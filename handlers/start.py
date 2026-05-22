from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from keyboards import BTN_GENDER_FEMALE, BTN_GENDER_MALE, gender_keyboard, main_menu_keyboard
from handlers.images import send_optional_screen
from storage import create_pet, has_pet, refresh_user_metadata, touch_user_needs


router = Router()


class PetCreation(StatesGroup):
    choosing_gender = State()
    entering_name = State()


GENDER_TEXT_TO_INTERNAL = {
    BTN_GENDER_MALE: "male",
    BTN_GENDER_FEMALE: "female",
}


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    refresh_user_metadata(message.from_user.id, message.from_user)

    if has_pet(message.from_user.id):
        touch_user_needs(message.from_user.id)
        await state.clear()
        await send_optional_screen(message, "main_menu", "С возвращением! Главное меню:", reply_markup=main_menu_keyboard())
        return

    await state.set_state(PetCreation.choosing_gender)
    await send_optional_screen(message, "start", "Привет! Давай создадим твоего енота 🦝\n\nВыбери пол питомца:", reply_markup=gender_keyboard())


@router.message(PetCreation.choosing_gender, F.text.in_(set(GENDER_TEXT_TO_INTERNAL.keys())))
async def choose_gender(message: Message, state: FSMContext) -> None:
    if message.text is None:
        return

    await state.update_data(gender=GENDER_TEXT_TO_INTERNAL[message.text])
    await state.set_state(PetCreation.entering_name)
    await message.answer("Как назовём енота?")


@router.message(PetCreation.choosing_gender)
async def choose_gender_invalid(message: Message) -> None:
    await message.answer("Пожалуйста, выбери пол кнопками ниже.")


@router.message(PetCreation.entering_name)
async def enter_name(message: Message, state: FSMContext) -> None:
    if message.from_user is None or message.text is None:
        return

    name = message.text.strip()
    if not name:
        await message.answer("Имя не может быть пустым. Введи имя ещё раз.")
        return

    data = await state.get_data()
    gender = data.get("gender")
    if gender not in {"male", "female"}:
        await state.set_state(PetCreation.choosing_gender)
        await message.answer("Давай снова выберем пол питомца:", reply_markup=gender_keyboard())
        return

    refresh_user_metadata(message.from_user.id, message.from_user)
    create_pet(message.from_user.id, name=name, gender=gender)
    await state.clear()

    await message.answer(
        f"Готово! Теперь у тебя есть енот по имени {name} 🦝",
        reply_markup=main_menu_keyboard(),
    )
