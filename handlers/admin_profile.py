from storage import ITEM_CATALOG, ensure_pet_defaults, get_pet_max_needs, get_user_by_id


def _username_value(raw_username: object) -> str:
    return f"@{raw_username}" if isinstance(raw_username, str) and raw_username else "без username"


def _inventory_summary(user: dict) -> str:
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


def _active_states(user: dict) -> str:
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
    ) + (f"\n• Enemy: {battle.get('enemy_id', 'неизвестно')}\n• Enemy status: active" if battle_active else "")


def format_admin_user_full(user_id: int) -> str:
    user_raw = get_user_by_id(user_id)
    if user_raw is None:
        return f"Пользователь <code>{user_id}</code> не найден."

    user, _ = ensure_pet_defaults(user_raw)
    first_name = user.get("first_name") if isinstance(user.get("first_name"), str) and user.get("first_name") else "неизвестно"
    last_name = user.get("last_name") if isinstance(user.get("last_name"), str) and user.get("last_name") else "неизвестно"
    language = user.get("language_code") if isinstance(user.get("language_code"), str) and user.get("language_code") else "неизвестно"
    is_bot = user.get("is_bot") if isinstance(user.get("is_bot"), bool) else "неизвестно"
    registration_time = user.get("created_at") if isinstance(user.get("created_at"), str) and user.get("created_at") else "неизвестно"
    username = _username_value(user.get("username"))

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
            "💰 <b>Экономика:</b>\n• Монеты: 0\n\n"
            "🎒 <b>Инвентарь:</b>\n• отсутствует\n\n"
            "⚔️ <b>Состояние:</b>\n• Active battle: no\n• Travel state: no\n• Current location: неизвестно"
        )

    max_needs = get_pet_max_needs(pet)
    skills = pet.get("skills", {}) if isinstance(pet.get("skills"), dict) else {}
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
        "💰 <b>Экономика:</b>\n"
        f"• Монеты: {pet.get('currency', 0)}\n\n"
        f"{_inventory_summary(user)}\n\n"
        f"{_active_states(user)}"
    )
