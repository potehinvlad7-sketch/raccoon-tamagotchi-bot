from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import is_admin
from keyboards import main_menu_keyboard
from storage import (
    ITEM_CATALOG,
    add_exp,
    admin_add_currency,
    admin_add_inventory_item,
    admin_clear_battle,
    admin_restore_needs,
    admin_update_pet_value,
    create_users_backup,
    ensure_pet_defaults,
    get_all_users,
    get_pet_max_needs,
    get_storage_stats,
    get_user_by_id,
)

router = Router()

ADMIN_ONLY_TEXT = "⛔ Команда доступна только администраторам."
USERS_PER_PAGE = 7

BROADCAST_TARGET_ALL = -1

broadcast_drafts: dict[int, dict] = {}


def _is_admin_message(message: Message) -> bool:
    return bool(message.from_user and is_admin(message.from_user.id))


def _is_admin_callback(callback: CallbackQuery) -> bool:
    return bool(callback.from_user and is_admin(callback.from_user.id))


def _admin_panel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin:stats")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin:users:0")],
        [InlineKeyboardButton(text="📣 Рассылка", callback_data="admin:broadcast")],
        [InlineKeyboardButton(text="💾 Backup JSON", callback_data="admin:backup")],
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="admin:main")],
    ])


def _users_keyboard(page: int, total_pages: int, users_slice: list[tuple[int, dict]]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for user_id, user in users_slice:
        pet = user.get("pet") if isinstance(user, dict) else None
        pet_name = pet.get("name") if isinstance(pet, dict) else "без питомца"
        rows.append([InlineKeyboardButton(text=f"👤 {user_id} · {pet_name}", callback_data=f"admin:user:{user_id}")])

    nav: list[InlineKeyboardButton] = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"admin:users:{page - 1}"))
    nav.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="admin:panel"))
    if page + 1 < total_pages:
        nav.append(InlineKeyboardButton(text="➡️", callback_data=f"admin:users:{page + 1}"))
    rows.append(nav)
    rows.append([InlineKeyboardButton(text="🛠 Админ-панель", callback_data="admin:panel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)




def _broadcast_audience_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Всем пользователям", callback_data="admin:broadcast:all")],
        [InlineKeyboardButton(text="👤 Выбрать пользователя", callback_data="admin:broadcast:select")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin:broadcast:cancel")],
    ])


def _broadcast_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Отправить", callback_data="admin:broadcast:send")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin:broadcast:cancel")],
    ])


def _broadcast_users_keyboard(page: int, total_pages: int, users_slice: list[tuple[int, dict]]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for user_id, user in users_slice:
        pet = user.get("pet") if isinstance(user, dict) else None
        pet_name = pet.get("name") if isinstance(pet, dict) else "без питомца"
        rows.append([InlineKeyboardButton(text=f"👤 {user_id} · {pet_name}", callback_data=f"admin:broadcast:pick:{user_id}")])

    nav: list[InlineKeyboardButton] = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"admin:broadcast:users:{page - 1}"))
    nav.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="admin:broadcast"))
    if page + 1 < total_pages:
        nav.append(InlineKeyboardButton(text="➡️", callback_data=f"admin:broadcast:users:{page + 1}"))
    rows.append(nav)
    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="admin:broadcast:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _user_actions_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🦝 Питомец", callback_data=f"admin:pet:{user_id}"), InlineKeyboardButton(text="✏️ Изменить питомца", callback_data=f"admin:edit:{user_id}")],
        [InlineKeyboardButton(text="🎒 Инвентарь", callback_data=f"admin:inv:{user_id}"), InlineKeyboardButton(text="💰 Монеты", callback_data=f"admin:currency_menu:{user_id}")],
        [InlineKeyboardButton(text="🔙 К списку пользователей", callback_data="admin:users:0")],
        [InlineKeyboardButton(text="🛠 Админ-панель", callback_data="admin:panel")],
    ])


def _pet_edit_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="+1 уровень", callback_data=f"admin:edit:{user_id}:level"), InlineKeyboardButton(text="+100 опыт", callback_data=f"admin:edit:{user_id}:exp")],
        [InlineKeyboardButton(text="+100 монет", callback_data=f"admin:edit:{user_id}:money"), InlineKeyboardButton(text="+1 сила", callback_data=f"admin:edit:{user_id}:strength")],
        [InlineKeyboardButton(text="+1 ловкость", callback_data=f"admin:edit:{user_id}:agility"), InlineKeyboardButton(text="+1 инстинкт", callback_data=f"admin:edit:{user_id}:instinct")],
        [InlineKeyboardButton(text="Полностью восстановить шкалы", callback_data=f"admin:edit:{user_id}:restore")],
        [InlineKeyboardButton(text="Очистить активный бой", callback_data=f"admin:edit:{user_id}:clear_battle")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"admin:user:{user_id}")],
    ])


def _inv_keyboard(user_id: int) -> InlineKeyboardMarkup:
    items = [
        ("food", "+1 яблоко"),
        ("soap", "+1 мыло"),
        ("toy", "+1 игрушка"),
        ("energy_potion", "+1 малое зелье"),
        ("strength_scroll", "+1 свиток силы"),
        ("agility_scroll", "+1 свиток ловкости"),
        ("instinct_scroll", "+1 свиток инстинкта"),
    ]
    rows = [[InlineKeyboardButton(text=label, callback_data=f"admin:inv_add:{user_id}:{key}")] for key, label in items]
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"admin:user:{user_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _currency_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="+10 монет", callback_data=f"admin:currency:{user_id}:10"), InlineKeyboardButton(text="+50 монет", callback_data=f"admin:currency:{user_id}:50")],
        [InlineKeyboardButton(text="+100 монет", callback_data=f"admin:currency:{user_id}:100"), InlineKeyboardButton(text="-10 монет", callback_data=f"admin:currency:{user_id}:-10")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"admin:user:{user_id}")],
    ])


def _format_stats() -> str:
    stats = get_storage_stats()
    backup_dir = "data/backups"
    return (
        "📊 <b>Статистика хранилища</b>\n\n"
        f"👥 Всего пользователей: <b>{stats['total_users']}</b>\n"
        f"🦝 Пользователей с питомцем: <b>{stats['users_with_pet']}</b>\n"
        f"🐾 Всего питомцев: <b>{stats['total_pets']}</b>\n"
        f"📈 Средний уровень: <b>{stats['average_level']}</b>\n"
        f"📂 Файл хранилища: <code>{stats['storage_path']}</code>\n"
        f"🗂 Каталог backup: <code>{backup_dir}</code>"
    )


def _format_user_line(user_id: int, user: dict) -> str:
    username = user.get("username") if isinstance(user.get("username"), str) and user.get("username") else "без username"
    pet = user.get("pet") if isinstance(user, dict) else None
    if not isinstance(pet, dict):
        return f"• <code>{user_id}</code> | @{username if username != 'без username' else username} | без питомца"
    level = pet.get("level", 1)
    pet_name = pet.get("name", "без имени")
    return f"• <code>{user_id}</code> | @{username if username != 'без username' else username} | {pet_name} (ур. {level})"


def _format_user_detail(user_id: int, user: dict) -> str:
    user, _ = ensure_pet_defaults(user)
    username_raw = user.get("username")
    username = f"@{username_raw}" if isinstance(username_raw, str) and username_raw else "без username"
    first_name = user.get("first_name") if isinstance(user.get("first_name"), str) and user.get("first_name") else "неизвестно"
    last_name = user.get("last_name") if isinstance(user.get("last_name"), str) and user.get("last_name") else "неизвестно"
    language = user.get("language_code") if isinstance(user.get("language_code"), str) and user.get("language_code") else "неизвестно"
    is_bot = user.get("is_bot") if isinstance(user.get("is_bot"), bool) else "неизвестно"
    registration_time = user.get("created_at") if isinstance(user.get("created_at"), str) and user.get("created_at") else "неизвестно"

    pet = user.get("pet")
    if not isinstance(pet, dict):
        return (
            "👤 <b>Пользователь:</b>\n"
            f"• ID: <code>{user_id}</code>\n"
            f"• Username: {username}\n"
            f"• First name: {first_name}\n"
            f"• Last name: {last_name}\n"
            f"• Language: {language}\n"
            f"• Is bot: {is_bot}\n"
            f"• Registration time: {registration_time}\n\n"
            "🦝 <b>Питомец:</b>\n• отсутствует\n\n"
            "💰 <b>Экономика:</b>\n• Монеты: 0\n• Всего заработано: неизвестно\n• Всего потрачено: неизвестно"
        )

    max_needs = get_pet_max_needs(pet)
    skills = pet.get("skills", {}) if isinstance(pet.get("skills"), dict) else {}
    inv = pet.get("inventory", {}) if isinstance(pet.get("inventory"), dict) else {}
    travel = pet.get("travel", {}) if isinstance(pet.get("travel"), dict) else {}
    battle = pet.get("battle")
    total_earned = pet.get("total_earned") if isinstance(pet.get("total_earned"), int) else "неизвестно"
    total_spent = pet.get("total_spent") if isinstance(pet.get("total_spent"), int) else "неизвестно"
    return (
        "👤 <b>Пользователь:</b>\n"
        f"• ID: <code>{user_id}</code>\n"
        f"• Username: {username}\n"
        f"• First name: {first_name}\n"
        f"• Last name: {last_name}\n"
        f"• Language: {language}\n"
        f"• Is bot: {is_bot}\n"
        f"• Registration time: {registration_time}\n\n"
        "🦝 <b>Питомец:</b>\n"
        f"• Имя: {pet.get('name', 'неизвестно')}\n"
        f"• Пол: {pet.get('gender', 'неизвестно')}\n"
        f"• Уровень: {pet.get('level', 1)}\n"
        f"• Опыт: {pet.get('exp', 0)}\n"
        "• Навыки:\n"
        f"  - сила: {skills.get('strength', 0)}\n"
        f"  - ловкость: {skills.get('agility', 0)}\n"
        f"  - инстинкт: {skills.get('instinct', 0)}\n"
        "• Статы:\n"
        f"  - сытость: {pet.get('satiety', 0)}/{max_needs['satiety']}\n"
        f"  - чистота: {pet.get('cleanliness', 0)}/{max_needs['cleanliness']}\n"
        f"  - любовь: {pet.get('love', 0)}/{max_needs['love']}\n"
        f"  - энергия: {pet.get('energy', 0)}/{max_needs['energy']}\n\n"
        "🎮 <b>Прогресс:</b>\n"
        f"• Путешествий: {travel.get('total_travels', 0)}\n"
        f"• Последнее событие: {travel.get('last_event') or 'неизвестно'}\n\n"
        "💰 <b>Экономика:</b>\n"
        f"• Монеты: {pet.get('currency', 0)}\n"
        f"• Всего заработано: {total_earned}\n"
        f"• Всего потрачено: {total_spent}"
    )


def _format_inventory_summary(user: dict) -> str:
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return "🎒 <b>Инвентарь:</b>\n• отсутствует"
    inv = pet.get("inventory", {}) if isinstance(pet.get("inventory"), dict) else {}
    categories = {
        "food": ("🍖 Еда", []),
        "cleanliness": ("🧺 Хозмаг", []),
        "love": ("🧸 Игрушки", []),
        "energy": ("🧪 Зелья", []),
        "scrolls": ("📜 Свитки", []),
    }
    for key, amount in inv.items():
        if not isinstance(amount, int) or amount <= 0:
            continue
        meta = ITEM_CATALOG.get(key, {})
        name = meta.get("name", key)
        if key.endswith("_scroll"):
            categories["scrolls"][1].append(f"• {name} x{amount}")
            continue
        bucket = meta.get("category", "")
        if bucket in categories:
            categories[bucket][1].append(f"• {name} x{amount}")
    lines = ["🎒 <b>Инвентарь:</b>"]
    for title, entries in categories.values():
        if entries:
            lines.append(f"\n{title}:\n" + "\n".join(entries))
    if len(lines) == 1:
        lines.append("• пусто")
    return "\n".join(lines)


def _format_active_states(user: dict) -> str:
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return "⚔️ <b>Состояние:</b>\n• Active battle: no\n• Travel state: no\n• Current location: неизвестно"
    battle = pet.get("battle")
    travel = pet.get("travel", {}) if isinstance(pet.get("travel"), dict) else {}
    battle_active = isinstance(battle, dict)
    travel_active = isinstance(travel, dict) and bool(travel.get("current_location"))
    location = travel.get("current_location") if isinstance(travel.get("current_location"), str) and travel.get("current_location") else "неизвестно"
    return (
        "⚔️ <b>Состояние:</b>\n"
        f"• Active battle: {'yes' if battle_active else 'no'}\n"
        f"• Travel state: {'yes' if travel_active else 'no'}\n"
        f"• Current location: {location}"
    ) + (
        f"\n• Enemy: {battle.get('enemy_id', 'неизвестно')}\n• Enemy status: active"
        if battle_active else ""
    )


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if not _is_admin_message(message):
        await message.answer(ADMIN_ONLY_TEXT)
        return
    await message.answer("🛠 <b>Админ-панель</b>\nВыберите действие:", reply_markup=_admin_panel_keyboard())


@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: Message) -> None:
    if not _is_admin_message(message):
        await message.answer(ADMIN_ONLY_TEXT)
        return
    await message.answer(_format_stats())


@router.message(Command("backup"))
async def cmd_backup(message: Message) -> None:
    if not _is_admin_message(message):
        await message.answer(ADMIN_ONLY_TEXT)
        return
    success, backup_path = create_users_backup()
    if not success:
        await message.answer(backup_path)
        return
    await message.answer(f"✅ Backup создан: <code>{backup_path}</code>")
    await message.answer_document(document=FSInputFile(backup_path))




@router.message()
async def handle_broadcast_content(message: Message) -> None:
    if not _is_admin_message(message):
        return
    admin_id = message.from_user.id
    draft = broadcast_drafts.get(admin_id)
    if not draft or not draft.get("awaiting_content"):
        return

    if not message.text and not message.photo:
        await message.answer("✉️ Отправьте текст, фото или фото с подписью для рассылки.")
        return

    draft["content_chat_id"] = message.chat.id
    draft["content_message_id"] = message.message_id
    draft["awaiting_content"] = False

    await message.answer("📣 Предпросмотр рассылки\n\nПроверьте сообщение перед отправкой.")
    await message.bot.copy_message(chat_id=admin_id, from_chat_id=message.chat.id, message_id=message.message_id)
    await message.answer("Отправить рассылку?", reply_markup=_broadcast_confirm_keyboard())

@router.callback_query(F.data.startswith("admin:"))
async def admin_callbacks(callback: CallbackQuery) -> None:
    if not _is_admin_callback(callback):
        await callback.answer("Нет доступа", show_alert=True)
        return

    data = callback.data or ""
    parts = data.split(":")

    try:
        if data == "admin:panel":
            await callback.message.edit_text("🛠 <b>Админ-панель</b>\nВыберите действие:", reply_markup=_admin_panel_keyboard())
        elif data == "admin:stats":
            await callback.message.edit_text(_format_stats(), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="admin:panel")]]))
        elif data == "admin:backup":
            success, backup_path = create_users_backup()
            if success:
                await callback.message.answer(f"✅ Backup создан: <code>{backup_path}</code>")
                await callback.message.answer_document(document=FSInputFile(backup_path))
            else:
                await callback.message.answer(f"❌ {backup_path}")
        elif data == "admin:broadcast":
            broadcast_drafts.pop(callback.from_user.id, None)
            await callback.message.edit_text("📣 Рассылка\n\nКому отправляем сообщение?", reply_markup=_broadcast_audience_keyboard())
        elif data == "admin:broadcast:all":
            broadcast_drafts[callback.from_user.id] = {"target": BROADCAST_TARGET_ALL, "awaiting_content": True}
            await callback.message.edit_text("✉️ Отправьте текст, фото или фото с подписью для рассылки.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="admin:broadcast:cancel")]]))
        elif data == "admin:broadcast:select":
            users = get_all_users()
            if not users:
                await callback.message.edit_text("Пользователи не найдены.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="admin:broadcast")]]))
            else:
                page = 0
                start = page * USERS_PER_PAGE
                total_pages = (len(users) + USERS_PER_PAGE - 1) // USERS_PER_PAGE
                users_slice = users[start:start + USERS_PER_PAGE]
                text = "👥 Выберите пользователя для рассылки\n\n" + "\n".join(_format_user_line(uid, user) for uid, user in users_slice)
                await callback.message.edit_text(text, reply_markup=_broadcast_users_keyboard(page, total_pages, users_slice))
        elif data == "admin:broadcast:cancel":
            broadcast_drafts.pop(callback.from_user.id, None)
            await callback.message.edit_text("❌ Рассылка отменена.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛠 Админ-панель", callback_data="admin:panel")]]))
        elif data == "admin:broadcast:send":
            draft = broadcast_drafts.get(callback.from_user.id)
            if not draft or draft.get("awaiting_content"):
                await callback.message.answer("Нет сообщения для рассылки.")
            else:
                target = draft.get("target")
                if target == BROADCAST_TARGET_ALL:
                    recipients = [uid for uid, _ in get_all_users() if isinstance(uid, int) and uid > 0]
                elif isinstance(target, int) and target > 0:
                    recipients = [target]
                else:
                    recipients = []
                sent = 0
                failed = 0
                for recipient_id in recipients:
                    try:
                        await callback.bot.copy_message(chat_id=recipient_id, from_chat_id=draft["content_chat_id"], message_id=draft["content_message_id"])
                        sent += 1
                    except Exception:
                        failed += 1
                broadcast_drafts.pop(callback.from_user.id, None)
                await callback.message.answer(
                    "📣 Рассылка завершена\n\n"
                    f"✅ Отправлено: {sent}\n"
                    f"⚠️ Ошибок: {failed}\n"
                    f"👥 Получателей: {len(recipients)}"
                )
        elif len(parts) == 4 and parts[1] == "broadcast" and parts[2] == "users":
            page = max(0, int(parts[3]))
            users = get_all_users()
            if not users:
                await callback.message.edit_text("Пользователи не найдены.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="admin:broadcast")]]))
            else:
                start = page * USERS_PER_PAGE
                total_pages = (len(users) + USERS_PER_PAGE - 1) // USERS_PER_PAGE
                if page >= total_pages:
                    page = total_pages - 1
                    start = page * USERS_PER_PAGE
                users_slice = users[start:start + USERS_PER_PAGE]
                text = "👥 Выберите пользователя для рассылки\n\n" + "\n".join(_format_user_line(uid, user) for uid, user in users_slice)
                await callback.message.edit_text(text, reply_markup=_broadcast_users_keyboard(page, total_pages, users_slice))
        elif len(parts) == 4 and parts[1] == "broadcast" and parts[2] == "pick":
            user_id = int(parts[3])
            if get_user_by_id(user_id) is None:
                await callback.message.answer("Пользователь не найден.")
            else:
                broadcast_drafts[callback.from_user.id] = {"target": user_id, "awaiting_content": True}
                await callback.message.edit_text("✉️ Отправьте текст, фото или фото с подписью для рассылки.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="admin:broadcast:cancel")]]))
        elif data == "admin:main":
            await callback.message.answer("Возврат в главное меню.", reply_markup=main_menu_keyboard())
        elif len(parts) == 3 and parts[1] == "users":
            page = max(0, int(parts[2]))
            users = get_all_users()
            if not users:
                await callback.message.edit_text("Пользователи не найдены.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="admin:panel")]]))
            else:
                start = page * USERS_PER_PAGE
                total_pages = (len(users) + USERS_PER_PAGE - 1) // USERS_PER_PAGE
                if page >= total_pages:
                    page = total_pages - 1
                    start = page * USERS_PER_PAGE
                users_slice = users[start:start + USERS_PER_PAGE]
                text = "👥 <b>Пользователи</b>\n\n" + "\n".join(_format_user_line(uid, user) for uid, user in users_slice)
                await callback.message.edit_text(text, reply_markup=_users_keyboard(page, total_pages, users_slice))
        elif len(parts) == 3 and parts[1] == "user":
            user_id = int(parts[2])
            user = get_user_by_id(user_id)
            if user is None:
                await callback.message.answer("Пользователь не найден.")
            else:
                profile_text = _format_user_detail(user_id, user)
                extra_text = _format_inventory_summary(user) + "\n\n" + _format_active_states(user)
                if len(profile_text) + len(extra_text) > 3600:
                    await callback.message.edit_text(profile_text, reply_markup=_user_actions_keyboard(user_id))
                    await callback.message.answer(extra_text)
                else:
                    await callback.message.edit_text(profile_text + "\n\n" + extra_text, reply_markup=_user_actions_keyboard(user_id))
        elif len(parts) == 3 and parts[1] == "pet":
            user_id = int(parts[2])
            user = get_user_by_id(user_id)
            if user is None:
                await callback.message.answer("Пользователь не найден.")
            else:
                await callback.message.edit_text(_format_user_detail(user_id, user), reply_markup=_user_actions_keyboard(user_id))
        elif len(parts) == 3 and parts[1] == "edit":
            user_id = int(parts[2])
            await callback.message.edit_text("✏️ Выберите действие для редактирования питомца:", reply_markup=_pet_edit_keyboard(user_id))
        elif len(parts) == 4 and parts[1] == "edit":
            user_id = int(parts[2])
            action = parts[3]
            text = ""
            if action == "level":
                ok, before, after = admin_update_pet_value(user_id, "level", 1)
                text = f"✅ Уровень: {before} → {after}" if ok else "❌ Не удалось изменить уровень."
            elif action == "exp":
                ok, before, after = admin_update_pet_value(user_id, "exp", 100)
                text = f"✅ Опыт: {before} → {after}" if ok else "❌ Не удалось изменить опыт."
            elif action == "money":
                ok, before, after = admin_add_currency(user_id, 100)
                text = f"✅ Монеты: {before} → {after}" if ok else "❌ Не удалось изменить монеты."
            elif action in {"strength", "agility", "instinct"}:
                ok, before, after = admin_update_pet_value(user_id, f"skills.{action}", 1)
                text = f"✅ {action}: {before} → {after}" if ok else "❌ Не удалось изменить навык."
            elif action == "restore":
                ok = admin_restore_needs(user_id)
                text = "✅ Шкалы полностью восстановлены." if ok else "❌ Не удалось восстановить шкалы."
            elif action == "clear_battle":
                ok = admin_clear_battle(user_id)
                text = "✅ Активный бой очищен." if ok else "❌ Активный бой не найден."
            await callback.message.answer(text)
        elif len(parts) == 3 and parts[1] == "inv":
            user_id = int(parts[2])
            user = get_user_by_id(user_id)
            if not user or not isinstance(user.get("pet"), dict):
                await callback.message.answer("У пользователя нет питомца.")
            else:
                inv = user["pet"].get("inventory", {})
                categories = {"food": [], "cleanliness": [], "love": [], "energy": [], "other": []}
                for key, amount in inv.items():
                    if not isinstance(amount, int) or amount <= 0:
                        continue
                    meta = ITEM_CATALOG.get(key, {})
                    bucket = meta.get("category", "other")
                    name = meta.get("name", key)
                    categories[bucket if bucket in categories else "other"].append(f"• {name}: {amount}")
                lines = ["🎒 <b>Инвентарь</b>"]
                for title, bucket in (("Еда", "food"), ("Гигиена", "cleanliness"), ("Игра", "love"), ("Энергия", "energy"), ("Прочее", "other")):
                    if categories[bucket]:
                        lines.append(f"\n<b>{title}</b>\n" + "\n".join(categories[bucket]))
                await callback.message.edit_text("\n".join(lines), reply_markup=_inv_keyboard(user_id))
        elif len(parts) == 4 and parts[1] == "inv_add":
            user_id = int(parts[2])
            key = parts[3]
            ok, before, after = admin_add_inventory_item(user_id, key, 1)
            if ok:
                await callback.message.answer(f"✅ {key}: {before} → {after}")
            else:
                await callback.message.answer("❌ Не удалось обновить инвентарь.")
        elif len(parts) == 3 and parts[1] == "currency_menu":
            user_id = int(parts[2])
            await callback.message.edit_text("💰 Управление монетами:", reply_markup=_currency_keyboard(user_id))
        elif len(parts) == 4 and parts[1] == "currency":
            user_id = int(parts[2])
            amount = int(parts[3])
            ok, before, after = admin_add_currency(user_id, amount)
            if ok:
                await callback.message.answer(f"✅ Монеты: {before} → {after}")
            else:
                await callback.message.answer("❌ Не удалось изменить монеты.")
    except (ValueError, IndexError):
        await callback.message.answer("Некорректная команда админ-панели.")

    await callback.answer()
