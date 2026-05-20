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
