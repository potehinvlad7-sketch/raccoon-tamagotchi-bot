# Audit Report — RPG Tamagotchi Raccoon Bot (current state)

Date: 2026-05-26 (UTC)
Scope: full repository inspection, no gameplay/formula/schema changes.

## 1) Summary
Project is **feature-rich but monolithic in handlers/menu.py and storage.py**. Core loops (pet creation, needs, care, travel, shop, training, admin panel) are implemented and generally coherent. Main cleanup need is **structural decomposition**, callback/message flow consistency, and UX text polish.

## 2) Implemented systems (✅)
- `/start` flow with metadata refresh and existing-pet shortcut to main menu.
- Pet creation with gender + name FSM.
- Main menu with status/care/training/travel/shop/inventory/profile/help/letter entries.
- Needs status rendering with bars, mood phrase, runaway risk display.
- Inventory display and category counts used in status/profile.
- Shop categories + item purchase via inline buy buttons.
- Training skills (strength/agility/instinct), potions usage.
- Travel with level-window location selection, events and enemy encounters.
- Battle actions (attack/run) via reply keyboard flow.
- Admin panel: stats, users list/detail, pet edits, inventory/coins adjustment, backups, notifications section, broadcast flow.
- Opportunistic low-needs notifications + logging.

## 3) Partial systems / rough areas (⚠️)
- `handlers/menu.py` overload: many unrelated concerns in one module (status rendering, care logic, travel, battles, shop, help, admin-contact messaging).
- Duplicated mapping data for travel locations in both `storage.py` and `keyboards.py` (risk of drift).
- Mixed UI paradigms for related domains: ReplyKeyboard entry + Inline submenus; some flows edit messages in-place, others send new messages.
- Magic/sword section mostly wrapper around existing training/potions and placeholder block.
- Some broad `except` fallback behavior hides exact Telegram API failure causes from maintainers.

## 4) Placeholders / stubs (🧪)
- Magic section explicit placeholder text (`Этот раздел откроется позже.`) with back callback.
- README explicitly states no equipment/step-by-step combat expansion from earlier stages.

## 5) Potential bugs / risks
- **Single-file complexity risk**: menu handler size increases regression probability when touching any flow.
- **Data source duplication**: travel map duplicated between `storage.py` and `keyboards.py`; inconsistency can silently break location resolution.
- **Callback drift risk**: large callback namespace spread across modules without centralized registry/type-safe callback data.
- **Silent exception swallowing** (`pass` in Telegram send/edit fallbacks) may hide operational issues.
- **Admin callback mega-handler** (`admin_callbacks`) is large and branch-heavy.

## 6) UX/text issues
- Mixed wording style (formal/informal, technical/user-facing tone) across menus and system replies.
- Placeholder text appears in user journey (magic block) without roadmap context.
- Some responses can feel repetitive when returning to menu after actions.
- Status/profile readability good overall, but long screens in dense sections (skills/shop admin details) can be chunked better.

## 7) Cleanup roadmap (small safe PRs)
1. **PR-1: Module split for menu domain**
   - Extract pure render/text helpers from `handlers/menu.py` into `handlers/menu_views.py`.
   - No behavior changes.
2. **PR-2: Travel source unification**
   - Keep travel location catalog in one module, import where needed.
   - Add assertion/test that keyboard location ids exactly match storage ids.
3. **PR-3: Callback naming registry**
   - Introduce constants/enums for callback prefixes.
   - Replace raw string literals incrementally.
4. **PR-4: Notification/admin logging polish**
   - Replace silent `pass` with debug-safe structured logs.
   - Keep user UX unchanged.
5. **PR-5: UX text cleanup batch**
   - Only copy edits and consistency improvements (no logic).
6. **PR-6: Magic placeholder hardening**
   - Keep placeholder behavior but make dedicated lightweight screen with clear “coming soon” positioning and return path.

## 8) Files inspected
- `main.py`
- `config.py`
- `storage.py`
- `keyboards.py`
- `handlers/__init__.py`
- `handlers/start.py`
- `handlers/menu.py`
- `handlers/admin.py`
- `handlers/images.py`
- `README.md`

## 9) Validation (commands and results)
- `python -m py_compile main.py config.py storage.py keyboards.py handlers/__init__.py handlers/start.py handlers/menu.py handlers/admin.py handlers/images.py`
  - Result: success (`PY_COMPILE_EXIT=0`)
- `git status --short`
  - Result before report file creation: clean
- `git diff --name-only`
  - Result before report file creation: empty
- `rg -n "edit_or_send_screen" .`
  - Result: no matches
- `rg -n "BOT_TOKEN\s*=|PROXY_URL\s*=|ADMIN_IDS\s*=" -g "*.py" .`
  - Result: matches only in `config.py` env-loading declarations
- `rg -n "TODO|FIXME|placeholder|заглуш|позже|откроется позже|pass" .`
  - Result: placeholder/pass occurrences found primarily in `handlers/menu.py`, `handlers/images.py`
- `rg -n "callback_data=|data ==|F.data|CallbackQuery" handlers keyboards.py`
  - Result: extensive callback map in `handlers/menu.py`, `handlers/admin.py`, and inline builders in `keyboards.py`

## Requested action
No gameplay/storage-schema changes were made. This commit adds only this audit report markdown for review.
