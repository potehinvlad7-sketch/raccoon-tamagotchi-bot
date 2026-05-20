# RPG Tamagotchi Raccoon Bot

Telegram RPG tamagotchi bot where users create a raccoon pet, care for it, train it, travel, earn currency, buy items, gain levels, and monitor mood/risk.

## Current features

- Pet creation
- Gender selection
- Name input
- JSON storage
- Needs: satiety, cleanliness, love, energy
- Inventory
- Care actions
- Real-time needs recalculation by timestamp without background loop
- Skills: strength, agility, instinct
- Training
- Instant short forest travel
- Rewards and simple random events
- Shop
- EXP and leveling
- Mood and runaway risk warning
- Need maximums scale with level
- Basic care items restore fixed values, so their relative impact decreases at higher levels

## Local run

1. Create `.env` in project root.
2. Required:
   - `BOT_TOKEN=your_telegram_bot_token`
3. Optional:
   - `PROXY_URL=socks5://127.0.0.1:1080`
4. Install:
   - `python -m pip install -r requirements.txt`
5. Run:
   - `python main.py`

## Notes

- `.env` must not be committed.
- JSON data is stored in `data/users.json`.
- No database is used yet.
- No background loop is used for needs recalculation.
- `PROXY_URL` is read from environment and used only when present.


## Admin (Stage 11)

- Optional env: `ADMIN_IDS=123456789,987654321` (доступ только этим Telegram ID)
- `/admin` — русская админ-панель с кнопками (статистика, пользователи, backup, возврат в меню)
- `/admin_stats` — статистика JSON-хранилища
- `/backup` — создание и отправка backup `data/users.json` из `data/backups/`
- В панели администратора доступны просмотр пользователей, профиль/питомец, редактирование питомца, инвентарь и монеты


## Stage 10.3
- Путешествия получили локации с требованиями по уровню и расширенный каталог событий.
- Во время путешествий могут редко выпадать свитки для будущих механик тренировок.
