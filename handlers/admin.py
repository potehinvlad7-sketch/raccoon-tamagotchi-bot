from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from config import is_admin
from storage import create_users_backup, get_storage_stats

router = Router()

ADMIN_ONLY_TEXT = "Эта команда доступна только администратору."


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if message.from_user is None or not is_admin(message.from_user.id):
        await message.answer(ADMIN_ONLY_TEXT)
        return

    await message.answer(
        "🛠 Админ-панель\n\n"
        "Доступные команды:\n"
        "• /admin_stats — статистика\n"
        "• /backup — backup JSON"
    )


@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: Message) -> None:
    if message.from_user is None or not is_admin(message.from_user.id):
        await message.answer(ADMIN_ONLY_TEXT)
        return

    stats = get_storage_stats()
    await message.answer(
        "🛠 Статистика\n\n"
        f"Пользователей: {stats['total_users']}\n"
        f"С пользователями-питомцами: {stats['users_with_pet']}\n"
        f"Питомцев: {stats['total_pets']}\n"
        f"Средний уровень: {stats['average_level']}\n"
        f"Хранилище: {stats['storage_path']}"
    )


@router.message(Command("backup"))
async def cmd_backup(message: Message) -> None:
    if message.from_user is None or not is_admin(message.from_user.id):
        await message.answer(ADMIN_ONLY_TEXT)
        return

    success, backup_path = create_users_backup()
    if not success:
        await message.answer(backup_path)
        return

    await message.answer(f"✅ Backup создан: {backup_path}")
    document = FSInputFile(backup_path)
    await message.answer_document(document=document)
