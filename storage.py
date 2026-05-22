import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"

DEFAULT_NEEDS = {
    "satiety": 80,
    "cleanliness": 80,
    "love": 80,
    "energy": 80,
}

DEFAULT_INVENTORY = {
    "food": 3,
    "soap": 2,
    "toy": 2,
    "energy_potion": 1,
    "hearty_snack": 0,
    "forest_honey": 0,
    "fluffy_shampoo": 0,
    "comb": 0,
    "yarn_ball": 0,
    "fun_toy": 0,
    "big_energy_potion": 0,
    "strength_scroll": 0,
    "agility_scroll": 0,
    "instinct_scroll": 0,
}
DEFAULT_SKILLS = {
    "strength": 0,
    "agility": 0,
    "instinct": 0,
}
DEFAULT_TRAVEL = {
    "total_travels": 0,
    "last_event": None,
}
DEFAULT_BATTLE = None
NEEDS_TICK_MINUTES = 30

MAX_LEVEL = 100
LEGEND_LEVEL = 100

TRAVEL_LOCATIONS = {
    "forest_clearing": {"button": "🌱 Лесная поляна", "name": "Лесная поляна", "min_level": 1, "costs": {'energy': 14, 'satiety': 7, 'cleanliness': 3}, "rewards": {'exp': 10, 'currency': 5}},
    "quiet_thicket": {"button": "🌿 Тихая чаща", "name": "Тихая чаща", "min_level": 2, "costs": {'energy': 16, 'satiety': 8, 'cleanliness': 4}, "rewards": {'exp': 14, 'currency': 7}},
    "mushroom_path": {"button": "🍄 Грибная тропа", "name": "Грибная тропа", "min_level": 3, "costs": {'energy': 18, 'satiety': 9, 'cleanliness': 5}, "rewards": {'exp': 18, 'currency': 9}},
    "old_deadfall": {"button": "🪵 Старый бурелом", "name": "Старый бурелом", "min_level": 4, "costs": {'energy': 20, 'satiety': 10, 'cleanliness': 6}, "rewards": {'exp': 22, 'currency': 11}},
    "misty_stream": {"button": "💧 Туманный ручей", "name": "Туманный ручей", "min_level": 5, "costs": {'energy': 22, 'satiety': 11, 'cleanliness': 7}, "rewards": {'exp': 27, 'currency': 13}},
    "stone_ravine": {"button": "🪨 Каменный овраг", "name": "Каменный овраг", "min_level": 6, "costs": {'energy': 24, 'satiety': 12, 'cleanliness': 8}, "rewards": {'exp': 31, 'currency': 15}},
    "forest_ruins": {"button": "🏚 Лесные руины", "name": "Лесные руины", "min_level": 7, "costs": {'energy': 26, 'satiety': 13, 'cleanliness': 9}, "rewards": {'exp': 35, 'currency': 17}},
    "abandoned_watchhut": {"button": "🌲 Заброшенная сторожка", "name": "Заброшенная сторожка", "min_level": 8, "costs": {'energy': 28, 'satiety': 14, 'cleanliness': 10}, "rewards": {'exp': 39, 'currency': 20}},
    "mossy_bridge": {"button": "🌉 Мшистый мост", "name": "Мшистый мост", "min_level": 9, "costs": {'energy': 30, 'satiety': 15, 'cleanliness': 11}, "rewards": {'exp': 43, 'currency': 22}},
    "foxglove_meadow": {"button": "🌸 Лисья поляна", "name": "Лисья поляна", "min_level": 10, "costs": {'energy': 32, 'satiety': 17, 'cleanliness': 12}, "rewards": {'exp': 48, 'currency': 24}},
    "hollow_stump_camp": {"button": "🪵 Лагерь в полом пне", "name": "Лагерь в полом пне", "min_level": 11, "costs": {'energy': 34, 'satiety': 18, 'cleanliness': 12}, "rewards": {'exp': 52, 'currency': 26}},
    "glowing_mushroom_grove": {"button": "🍄 Светящийся грибной бор", "name": "Светящийся грибной бор", "min_level": 12, "costs": {'energy': 36, 'satiety': 19, 'cleanliness': 13}, "rewards": {'exp': 56, 'currency': 28}},
    "silver_leaf_path": {"button": "🍃 Серебряная тропа", "name": "Серебряная тропа", "min_level": 13, "costs": {'energy': 38, 'satiety': 20, 'cleanliness': 14}, "rewards": {'exp': 60, 'currency': 30}},
    "raven_crossing": {"button": "🐦‍⬛ Вороний переход", "name": "Вороний переход", "min_level": 14, "costs": {'energy': 40, 'satiety': 21, 'cleanliness': 15}, "rewards": {'exp': 64, 'currency': 32}},
    "old_hunter_trail": {"button": "🏹 Старая охотничья тропа", "name": "Старая охотничья тропа", "min_level": 15, "costs": {'energy': 42, 'satiety': 22, 'cleanliness': 16}, "rewards": {'exp': 69, 'currency': 34}},
    "sleepy_pine_hill": {"button": "🌲 Сонный сосновый холм", "name": "Сонный сосновый холм", "min_level": 16, "costs": {'energy': 44, 'satiety': 23, 'cleanliness': 17}, "rewards": {'exp': 73, 'currency': 37}},
    "dewberry_lowland": {"button": "🫐 Ежевичная низина", "name": "Ежевичная низина", "min_level": 17, "costs": {'energy': 46, 'satiety': 24, 'cleanliness': 18}, "rewards": {'exp': 77, 'currency': 39}},
    "foggy_swamp": {"button": "🌫 Туманное болото", "name": "Туманное болото", "min_level": 18, "costs": {'energy': 48, 'satiety': 25, 'cleanliness': 19}, "rewards": {'exp': 81, 'currency': 41}},
    "frog_song_marsh": {"button": "🐸 Трясина жабьих песен", "name": "Трясина жабьих песен", "min_level": 19, "costs": {'energy': 50, 'satiety': 26, 'cleanliness': 20}, "rewards": {'exp': 85, 'currency': 43}},
    "reed_maze": {"button": "🌾 Камышовый лабиринт", "name": "Камышовый лабиринт", "min_level": 20, "costs": {'energy': 52, 'satiety': 28, 'cleanliness': 21}, "rewards": {'exp': 90, 'currency': 45}},
    "sunken_log_path": {"button": "🪵 Затонувшая тропа", "name": "Затонувшая тропа", "min_level": 21, "costs": {'energy': 54, 'satiety': 29, 'cleanliness': 21}, "rewards": {'exp': 94, 'currency': 47}},
    "firefly_pool": {"button": "✨ Пруд светляков", "name": "Пруд светляков", "min_level": 22, "costs": {'energy': 56, 'satiety': 30, 'cleanliness': 22}, "rewards": {'exp': 98, 'currency': 49}},
    "wet_root_tunnel": {"button": "🕳 Мокрый корневой лаз", "name": "Мокрый корневой лаз", "min_level": 23, "costs": {'energy': 58, 'satiety': 31, 'cleanliness': 23}, "rewards": {'exp': 102, 'currency': 51}},
    "heron_shallows": {"button": "🪶 Цаплиные отмели", "name": "Цаплиные отмели", "min_level": 24, "costs": {'energy': 60, 'satiety': 32, 'cleanliness': 24}, "rewards": {'exp': 106, 'currency': 54}},
    "stone_pass": {"button": "🪨 Каменный перевал", "name": "Каменный перевал", "min_level": 25, "costs": {'energy': 62, 'satiety': 33, 'cleanliness': 25}, "rewards": {'exp': 111, 'currency': 56}},
    "windy_cliff_path": {"button": "🌬 Ветреная тропа", "name": "Ветреная тропа", "min_level": 26, "costs": {'energy': 64, 'satiety': 34, 'cleanliness': 26}, "rewards": {'exp': 115, 'currency': 58}},
    "pebble_watch": {"button": "🪨 Галечный дозор", "name": "Галечный дозор", "min_level": 27, "costs": {'energy': 66, 'satiety': 35, 'cleanliness': 27}, "rewards": {'exp': 119, 'currency': 60}},
    "goat_grass_slope": {"button": "🐐 Склон козьей травы", "name": "Склон козьей травы", "min_level": 28, "costs": {'energy': 68, 'satiety': 36, 'cleanliness': 28}, "rewards": {'exp': 123, 'currency': 62}},
    "echoing_gully": {"button": "🔊 Эхо-лощина", "name": "Эхо-лощина", "min_level": 29, "costs": {'energy': 70, 'satiety': 37, 'cleanliness': 29}, "rewards": {'exp': 127, 'currency': 64}},
    "cracked_boulder_gate": {"button": "🪨 Треснувшие валуны", "name": "Треснувшие валуны", "min_level": 30, "costs": {'energy': 72, 'satiety': 39, 'cleanliness': 30}, "rewards": {'exp': 132, 'currency': 66}},
    "pine_needle_ridge": {"button": "🌲 Хребет хвойных игл", "name": "Хребет хвойных игл", "min_level": 31, "costs": {'energy': 74, 'satiety': 40, 'cleanliness': 30}, "rewards": {'exp': 136, 'currency': 68}},
    "cloudberry_shelf": {"button": "☁️ Морошковый уступ", "name": "Морошковый уступ", "min_level": 32, "costs": {'energy': 76, 'satiety': 41, 'cleanliness': 31}, "rewards": {'exp': 140, 'currency': 71}},
    "stormcrow_peak": {"button": "🐦‍⬛ Пик буревестников", "name": "Пик буревестников", "min_level": 33, "costs": {'energy': 78, 'satiety': 42, 'cleanliness': 32}, "rewards": {'exp': 144, 'currency': 73}},
    "dry_stream_bed": {"button": "🏜 Сухое русло", "name": "Сухое русло", "min_level": 34, "costs": {'energy': 80, 'satiety': 43, 'cleanliness': 33}, "rewards": {'exp': 148, 'currency': 75}},
    "old_settlement_ruins": {"button": "🏚 Руины старого поселения", "name": "Руины старого поселения", "min_level": 35, "costs": {'energy': 82, 'satiety': 44, 'cleanliness': 34}, "rewards": {'exp': 153, 'currency': 77}},
    "overgrown_well": {"button": "🕳 Заросший колодец", "name": "Заросший колодец", "min_level": 36, "costs": {'energy': 84, 'satiety': 45, 'cleanliness': 35}, "rewards": {'exp': 157, 'currency': 79}},
    "broken_cart_square": {"button": "🛞 Площадь сломанной телеги", "name": "Площадь сломанной телеги", "min_level": 37, "costs": {'energy': 86, 'satiety': 46, 'cleanliness': 36}, "rewards": {'exp': 161, 'currency': 81}},
    "moss_roof_houses": {"button": "🏚 Дома под мхом", "name": "Дома под мхом", "min_level": 38, "costs": {'energy': 88, 'satiety': 47, 'cleanliness': 37}, "rewards": {'exp': 165, 'currency': 83}},
    "forgotten_pantry": {"button": "🥫 Забытая кладовая", "name": "Забытая кладовая", "min_level": 39, "costs": {'energy': 90, 'satiety': 48, 'cleanliness': 38}, "rewards": {'exp': 169, 'currency': 85}},
    "chimney_crow_roost": {"button": "🐦‍⬛ Вороньи трубы", "name": "Вороньи трубы", "min_level": 40, "costs": {'energy': 92, 'satiety': 50, 'cleanliness': 39, 'love': 13}, "rewards": {'exp': 174, 'currency': 88}},
    "cracked_chapel_yard": {"button": "🕯 Двор треснувшей часовни", "name": "Двор треснувшей часовни", "min_level": 41, "costs": {'energy': 94, 'satiety': 51, 'cleanliness': 39, 'love': 13}, "rewards": {'exp': 178, 'currency': 90}},
    "cellar_of_whispers": {"button": "🕳 Подвал шёпотов", "name": "Подвал шёпотов", "min_level": 42, "costs": {'energy': 96, 'satiety': 52, 'cleanliness': 40, 'love': 14}, "rewards": {'exp': 182, 'currency': 92}},
    "ivy_clock_tower": {"button": "🕰 Башня в плюще", "name": "Башня в плюще", "min_level": 43, "costs": {'energy': 98, 'satiety': 53, 'cleanliness': 41, 'love': 14}, "rewards": {'exp': 186, 'currency': 94}},
    "moonlit_mill": {"button": "🌙 Лунная мельница", "name": "Лунная мельница", "min_level": 44, "costs": {'energy': 100, 'satiety': 54, 'cleanliness': 42, 'love': 14}, "rewards": {'exp': 190, 'currency': 96}},
    "starry_thicket": {"button": "🌌 Звёздная чаща", "name": "Звёздная чаща", "min_level": 45, "costs": {'energy': 102, 'satiety': 55, 'cleanliness': 43, 'love': 15}, "rewards": {'exp': 195, 'currency': 98}},
    "firefly_constellation_path": {"button": "✨ Тропа светлячных созвездий", "name": "Тропа светлячных созвездий", "min_level": 46, "costs": {'energy': 104, 'satiety': 56, 'cleanliness': 44, 'love': 15}, "rewards": {'exp': 199, 'currency': 100}},
    "silver_moth_glade": {"button": "🦋 Поляна серебряных мотыльков", "name": "Поляна серебряных мотыльков", "min_level": 47, "costs": {'energy': 106, 'satiety': 57, 'cleanliness': 45, 'love': 15}, "rewards": {'exp': 203, 'currency': 102}},
    "night_bloom_garden": {"button": "🌺 Ночной цветник", "name": "Ночной цветник", "min_level": 48, "costs": {'energy': 108, 'satiety': 58, 'cleanliness': 46, 'love': 16}, "rewards": {'exp': 207, 'currency': 105}},
    "owl_mirror_lake": {"button": "🦉 Зеркальное озеро сов", "name": "Зеркальное озеро сов", "min_level": 49, "costs": {'energy': 110, 'satiety': 59, 'cleanliness': 47, 'love': 16}, "rewards": {'exp': 211, 'currency': 107}},
    "comet_fallen_clearing": {"button": "☄️ Поляна упавшей кометы", "name": "Поляна упавшей кометы", "min_level": 50, "costs": {'energy': 112, 'satiety': 61, 'cleanliness': 48, 'love': 16}, "rewards": {'exp': 216, 'currency': 109}},
    "whispering_fern_field": {"button": "🌿 Поле шепчущих папоротников", "name": "Поле шепчущих папоротников", "min_level": 51, "costs": {'energy': 114, 'satiety': 62, 'cleanliness': 48, 'love': 17}, "rewards": {'exp': 220, 'currency': 111}},
    "blue_moon_copse": {"button": "🔵 Роща синей луны", "name": "Роща синей луны", "min_level": 52, "costs": {'energy': 116, 'satiety': 63, 'cleanliness': 49, 'love': 17}, "rewards": {'exp': 224, 'currency': 113}},
    "astral_burrow": {"button": "🌠 Звёздная нора", "name": "Звёздная нора", "min_level": 53, "costs": {'energy': 118, 'satiety': 64, 'cleanliness': 50, 'love': 17}, "rewards": {'exp': 228, 'currency': 115}},
    "lanternroot_path": {"button": "🏮 Тропа фонарных корней", "name": "Тропа фонарных корней", "min_level": 54, "costs": {'energy': 120, 'satiety': 65, 'cleanliness': 51, 'love': 18}, "rewards": {'exp': 232, 'currency': 117}},
    "underground_roots": {"button": "🕯 Подземные корни", "name": "Подземные корни", "min_level": 55, "costs": {'energy': 122, 'satiety': 66, 'cleanliness': 52, 'love': 18}, "rewards": {'exp': 237, 'currency': 119}},
    "root_cathedral": {"button": "⛪ Корневой собор", "name": "Корневой собор", "min_level": 56, "costs": {'energy': 124, 'satiety': 67, 'cleanliness': 53, 'love': 18}, "rewards": {'exp': 241, 'currency': 122}},
    "blind_mole_tunnels": {"button": "🕳 Тоннели слепых кротов", "name": "Тоннели слепых кротов", "min_level": 57, "costs": {'energy': 126, 'satiety': 68, 'cleanliness': 54, 'love': 19}, "rewards": {'exp': 245, 'currency': 124}},
    "amber_resin_caves": {"button": "🟠 Янтарные пещеры", "name": "Янтарные пещеры", "min_level": 58, "costs": {'energy': 128, 'satiety': 69, 'cleanliness': 55, 'love': 19}, "rewards": {'exp': 249, 'currency': 126}},
    "fossil_nest": {"button": "🦴 Ископаемое гнездо", "name": "Ископаемое гнездо", "min_level": 59, "costs": {'energy': 130, 'satiety': 70, 'cleanliness': 56, 'love': 19}, "rewards": {'exp': 253, 'currency': 128}},
    "deep_moss_chamber": {"button": "🌿 Глубокая моховая зала", "name": "Глубокая моховая зала", "min_level": 60, "costs": {'energy': 132, 'satiety': 72, 'cleanliness': 57, 'love': 20}, "rewards": {'exp': 258, 'currency': 130}},
    "echo_root_maze": {"button": "🔊 Лабиринт эхо-корней", "name": "Лабиринт эхо-корней", "min_level": 61, "costs": {'energy': 134, 'satiety': 73, 'cleanliness': 57, 'love': 20}, "rewards": {'exp': 262, 'currency': 132}},
    "buried_stream": {"button": "💧 Погребённый ручей", "name": "Погребённый ручей", "min_level": 62, "costs": {'energy': 136, 'satiety': 74, 'cleanliness': 58, 'love': 20}, "rewards": {'exp': 266, 'currency': 134}},
    "stone_seed_vault": {"button": "🪨 Хранилище каменных семян", "name": "Хранилище каменных семян", "min_level": 63, "costs": {'energy': 138, 'satiety': 75, 'cleanliness': 59, 'love': 21}, "rewards": {'exp': 270, 'currency': 136}},
    "sleeping_earth_heart": {"button": "🫀 Спящее сердце земли", "name": "Спящее сердце земли", "min_level": 64, "costs": {'energy': 140, 'satiety': 76, 'cleanliness': 60, 'love': 21}, "rewards": {'exp': 274, 'currency': 139}},
    "giants_graveyard": {"button": "🦴 Кладбище великанов", "name": "Кладбище великанов", "min_level": 65, "costs": {'energy': 142, 'satiety': 77, 'cleanliness': 61, 'love': 21}, "rewards": {'exp': 279, 'currency': 141}},
    "rib_bone_valley": {"button": "🦴 Долина рёбер", "name": "Долина рёбер", "min_level": 66, "costs": {'energy': 144, 'satiety': 78, 'cleanliness': 62, 'love': 22}, "rewards": {'exp': 283, 'currency': 143}},
    "skull_hill": {"button": "💀 Черепной холм", "name": "Черепной холм", "min_level": 67, "costs": {'energy': 146, 'satiety': 79, 'cleanliness': 63, 'love': 22}, "rewards": {'exp': 287, 'currency': 145}},
    "mammoth_moss_field": {"button": "🦣 Мамонтово моховое поле", "name": "Мамонтово моховое поле", "min_level": 68, "costs": {'energy': 148, 'satiety': 80, 'cleanliness': 64, 'love': 22}, "rewards": {'exp': 291, 'currency': 147}},
    "bone_wind_passage": {"button": "🌬 Костяной проход ветров", "name": "Костяной проход ветров", "min_level": 69, "costs": {'energy': 150, 'satiety': 81, 'cleanliness': 65, 'love': 23}, "rewards": {'exp': 295, 'currency': 149}},
    "giant_finger_bridge": {"button": "🦴 Мост пальца великана", "name": "Мост пальца великана", "min_level": 70, "costs": {'energy': 152, 'satiety': 83, 'cleanliness': 66, 'love': 23}, "rewards": {'exp': 300, 'currency': 151}},
    "ancient_battlefield": {"button": "⚔️ Древнее поле битвы", "name": "Древнее поле битвы", "min_level": 71, "costs": {'energy': 154, 'satiety': 84, 'cleanliness': 66, 'love': 23}, "rewards": {'exp': 304, 'currency': 153}},
    "white_antler_grove": {"button": "🦌 Роща белых рогов", "name": "Роща белых рогов", "min_level": 72, "costs": {'energy': 156, 'satiety': 85, 'cleanliness': 67, 'love': 24}, "rewards": {'exp': 308, 'currency': 156}},
    "hollow_bone_caves": {"button": "🦴 Полые костяные пещеры", "name": "Полые костяные пещеры", "min_level": 73, "costs": {'energy': 158, 'satiety': 86, 'cleanliness': 68, 'love': 24}, "rewards": {'exp': 312, 'currency': 158}},
    "last_giant_camp": {"button": "🔥 Последний лагерь великана", "name": "Последний лагерь великана", "min_level": 74, "costs": {'energy': 160, 'satiety': 87, 'cleanliness': 69, 'love': 24}, "rewards": {'exp': 316, 'currency': 160}},
    "forgotten_raccoon_castle": {"button": "🏰 Забытый енотовый замок", "name": "Забытый енотовый замок", "min_level": 75, "costs": {'energy': 162, 'satiety': 88, 'cleanliness': 70, 'love': 25}, "rewards": {'exp': 321, 'currency': 162}},
    "tailguard_gate": {"button": "🦝 Врата хвостатой стражи", "name": "Врата хвостатой стражи", "min_level": 76, "costs": {'energy': 164, 'satiety': 89, 'cleanliness': 71, 'love': 25}, "rewards": {'exp': 325, 'currency': 164}},
    "dusty_banner_hall": {"button": "🏳️ Пыльный зал знамён", "name": "Пыльный зал знамён", "min_level": 77, "costs": {'energy': 166, 'satiety': 90, 'cleanliness': 72, 'love': 25}, "rewards": {'exp': 329, 'currency': 166}},
    "moon_key_corridor": {"button": "🗝 Лунный коридор ключей", "name": "Лунный коридор ключей", "min_level": 78, "costs": {'energy': 168, 'satiety': 91, 'cleanliness': 73, 'love': 26}, "rewards": {'exp': 333, 'currency': 168}},
    "cracked_throne_room": {"button": "👑 Треснувший тронный зал", "name": "Треснувший тронный зал", "min_level": 79, "costs": {'energy': 170, 'satiety': 92, 'cleanliness': 74, 'love': 26}, "rewards": {'exp': 337, 'currency': 170}},
    "pantry_of_kings": {"button": "🍯 Королевская кладовая", "name": "Королевская кладовая", "min_level": 80, "costs": {'energy': 172, 'satiety': 94, 'cleanliness': 75, 'love': 26}, "rewards": {'exp': 342, 'currency': 173}},
    "armor_rat_barracks": {"button": "🛡 Казармы бронекрысов", "name": "Казармы бронекрысов", "min_level": 81, "costs": {'energy': 174, 'satiety': 95, 'cleanliness': 75, 'love': 27}, "rewards": {'exp': 346, 'currency': 175}},
    "knight_raccoon_gallery": {"button": "🖼 Галерея енотов-рыцарей", "name": "Галерея енотов-рыцарей", "min_level": 82, "costs": {'energy': 176, 'satiety': 96, 'cleanliness': 76, 'love': 27}, "rewards": {'exp': 350, 'currency': 177}},
    "silver_crown_tower": {"button": "👑 Башня серебряной короны", "name": "Башня серебряной короны", "min_level": 83, "costs": {'energy': 178, 'satiety': 97, 'cleanliness': 77, 'love': 27}, "rewards": {'exp': 354, 'currency': 179}},
    "royal_burrow_keep": {"button": "🏰 Королевская нора-крепость", "name": "Королевская нора-крепость", "min_level": 84, "costs": {'energy': 180, 'satiety': 98, 'cleanliness': 78, 'love': 28}, "rewards": {'exp': 358, 'currency': 181}},
    "black_grove": {"button": "🌑 Чёрная роща", "name": "Чёрная роща", "min_level": 85, "costs": {'energy': 182, 'satiety': 99, 'cleanliness': 79, 'love': 28}, "rewards": {'exp': 363, 'currency': 183}},
    "shadow_birch_path": {"button": "🌑 Тропа теневых берёз", "name": "Тропа теневых берёз", "min_level": 86, "costs": {'energy': 184, 'satiety': 100, 'cleanliness': 80, 'love': 28}, "rewards": {'exp': 367, 'currency': 185}},
    "cursed_acorn_field": {"button": "🌰 Поле проклятых желудей", "name": "Поле проклятых желудей", "min_level": 87, "costs": {'energy': 186, 'satiety': 101, 'cleanliness': 81, 'love': 29}, "rewards": {'exp': 371, 'currency': 187}},
    "silent_owl_court": {"button": "🦉 Суд безмолвных сов", "name": "Суд безмолвных сов", "min_level": 88, "costs": {'energy': 188, 'satiety': 102, 'cleanliness': 82, 'love': 29}, "rewards": {'exp': 375, 'currency': 190}},
    "thornmoon_thicket": {"button": "🌙 Терновая чаща луны", "name": "Терновая чаща луны", "min_level": 89, "costs": {'energy': 190, 'satiety': 103, 'cleanliness': 83, 'love': 29}, "rewards": {'exp': 379, 'currency': 192}},
    "black_sap_swamp": {"button": "🖤 Болото чёрной смолы", "name": "Болото чёрной смолы", "min_level": 90, "costs": {'energy': 192, 'satiety': 105, 'cleanliness': 84, 'love': 30}, "rewards": {'exp': 384, 'currency': 194}},
    "hollow_shadow_den": {"button": "🕳 Логово пустой тени", "name": "Логово пустой тени", "min_level": 91, "costs": {'energy': 194, 'satiety': 106, 'cleanliness': 84, 'love': 30}, "rewards": {'exp': 388, 'currency': 196}},
    "eclipse_root_circle": {"button": "🌘 Круг корней затмения", "name": "Круг корней затмения", "min_level": 92, "costs": {'energy': 196, 'satiety': 107, 'cleanliness': 85, 'love': 30}, "rewards": {'exp': 392, 'currency': 198}},
    "dead_star_clearing": {"button": "✴️ Поляна мёртвой звезды", "name": "Поляна мёртвой звезды", "min_level": 93, "costs": {'energy': 198, 'satiety': 108, 'cleanliness': 86, 'love': 31}, "rewards": {'exp': 396, 'currency': 200}},
    "night_crown_forest": {"button": "👑 Лес ночной короны", "name": "Лес ночной короны", "min_level": 94, "costs": {'energy': 200, 'satiety': 109, 'cleanliness': 87, 'love': 31}, "rewards": {'exp': 400, 'currency': 202}},
    "path_of_legends": {"button": "👑 Тропа легенд", "name": "Тропа легенд", "min_level": 95, "costs": {'energy': 202, 'satiety': 110, 'cleanliness': 88, 'love': 31}, "rewards": {'exp': 405, 'currency': 204}},
    "first_legend_step": {"button": "✨ Первый шаг легенды", "name": "Первый шаг легенды", "min_level": 96, "costs": {'energy': 204, 'satiety': 111, 'cleanliness': 89, 'love': 32}, "rewards": {'exp': 409, 'currency': 207}},
    "elder_tail_shrine": {"button": "🦝 Святилище старшего хвоста", "name": "Святилище старшего хвоста", "min_level": 97, "costs": {'energy': 206, 'satiety': 112, 'cleanliness': 90, 'love': 32}, "rewards": {'exp': 413, 'currency': 209}},
    "skyroot_summit": {"button": "🌌 Вершина небесных корней", "name": "Вершина небесных корней", "min_level": 98, "costs": {'energy': 208, 'satiety': 113, 'cleanliness': 91, 'love': 32}, "rewards": {'exp': 417, 'currency': 211}},
    "gate_before_legend": {"button": "🚪 Врата перед легендой", "name": "Врата перед легендой", "min_level": 99, "costs": {'energy': 210, 'satiety': 114, 'cleanliness': 92, 'love': 33}, "rewards": {'exp': 421, 'currency': 213}},
    "raccoon_legend_throne": {"button": "👑 Трон легендарного енота", "name": "Трон легендарного енота", "min_level": 100, "costs": {'energy': 212, 'satiety': 116, 'cleanliness': 93, 'love': 33}, "rewards": {'exp': 426, 'currency': 215}},
}


TRAVEL_EVENTS = [
    {"id": "berry_cache", "type": "good", "text": "Енот нашёл под листьями горсть сладких ягод 🍓", "effects": {"currency": 2, "items": {"food": 1}}},
    {"id": "shiny_button", "type": "good", "text": "В мху блеснула старая пуговица. Енот решил, что это сокровище ✨", "effects": {"currency": 5}},
    {"id": "honey_smell", "type": "good", "text": "Енот учуял запах дикого мёда и принёс липкую добычу 🍯", "effects": {"items": {"forest_honey": 1}}},
    {"id": "clean_spring", "type": "good", "text": "У ручья енот умылся так важно, будто готовился к портрету 💧", "effects": {"needs": {"cleanliness": 15}}},
    {"id": "warm_sun_patch", "type": "good", "text": "На солнечной кочке енот немного отдохнул и снова приободрился ☀️", "effects": {"needs": {"energy": 10}}},
    {"id": "moss_inspection", "type": "neutral", "text": "Енот долго изучал мох. Научного вывода нет, но выглядело серьёзно 🌿", "effects": {}},
    {"id": "suspicious_stump", "type": "neutral", "text": "Енот поспорил с подозрительным пнём. Пень не ответил 🪵", "effects": {}},
    {"id": "owl_watched", "type": "neutral", "text": "С ветки за ним наблюдала сова. Енот сделал вид, что так и задумано 🦉", "effects": {}},
    {"id": "lost_tracks", "type": "neutral", "text": "Следы вывели к луже и внезапно закончились 🐾", "effects": {}},
    {"id": "rustle_in_bushes", "type": "neutral", "text": "В кустах что-то шуршало. Енот шуршал в ответ 🌲", "effects": {}},
    {"id": "muddy_paws", "type": "bad", "text": "Енот провалился лапами в мокрую землю 🐾", "effects": {"needs": {"cleanliness": -15}}},
    {"id": "thorny_bush", "type": "bad", "text": "Колючий куст оказался сильнее енотовой гордости 🌿", "effects": {"needs": {"love": -8, "energy": -5}}},
    {"id": "snack_lost", "type": "bad", "text": "Пока енот изучал корягу, перекус куда-то исчез 🍎", "effects": {"needs": {"satiety": -10}}},
    {"id": "loud_crack", "type": "bad", "text": "В лесу громко треснула ветка. Енот решил, что приключений достаточно 😳", "effects": {"needs": {"energy": -12}}},
    {"id": "rain_cloud", "type": "bad", "text": "Маленькая туча выбрала именно этого енота ☔", "effects": {"needs": {"cleanliness": -10, "love": -5}}},
    {"id": "strength_scroll_find", "type": "rare", "text": "Под корнем лежал старый свиток с грубым знаком лапы 📜", "effects": {"items": {"strength_scroll": 1}}},
    {"id": "agility_scroll_find", "type": "rare", "text": "Между камней енот нашёл тонкий свиток с рисунком бегущего хвоста 📜", "effects": {"items": {"agility_scroll": 1}}},
    {"id": "instinct_scroll_find", "type": "rare", "text": "На бересте проступали странные следы. Это оказался свиток инстинкта 📜", "effects": {"items": {"instinct_scroll": 1}}},
    {"id": "watchhut_floor_map", "type": "good", "text": "Старая карта под половицей привела енота к забытым припасам 🗺", "effects": {"currency": 18, "exp": 24}},
    {"id": "glow_spores", "type": "good", "text": "Светящиеся споры осели на шерсти и подсветили путь к находкам 🍄", "effects": {"currency": 20, "exp": 28}},
    {"id": "bog_light", "type": "bad", "text": "Болотный огонёк увёл енота в круги по топи 🌫", "effects": {"needs": {"energy": -24, "cleanliness": -18}}},
    {"id": "mountain_wind", "type": "bad", "text": "Горный ветер сбил темп и вымотал енота на подъёме 🌬", "effects": {"needs": {"energy": -26, "love": -12}}},
    {"id": "old_house_cache", "type": "good", "text": "Тайник старого дома хранил монеты и полезный свёрток 🏚", "effects": {"currency": 30, "exp": 36, "items": {"food": 1}}},
    {"id": "star_dust", "type": "rare", "text": "Звёздная пыль осыпала лапы, и енот стал двигаться увереннее ✨", "effects": {"currency": 42, "exp": 55}},
    {"id": "ancient_root_dream", "type": "rare", "text": "Сон древних корней подарил видение тайных троп 🕯", "effects": {"currency": 54, "exp": 70}},
    {"id": "giant_bone", "type": "good", "text": "Кость великана скрывала в трещине старые жетоны 🦴", "effects": {"currency": 46, "exp": 60}},
    {"id": "raccoon_knight_mark", "type": "rare", "text": "Рыцарский знак енота усилил решимость перед следующими боями 🏰", "effects": {"currency": 70, "exp": 90, "items": {"strength_scroll": 1}}},
    {"id": "black_branch", "type": "bad", "text": "Чёрная ветка цепко потянула хвост в тень 🌑", "effects": {"needs": {"energy": -32, "cleanliness": -22, "love": -14}}},
    {"id": "legend_trace", "type": "rare", "text": "След легенды вывел к тайнику на финальной тропе 👑", "effects": {"currency": 92, "exp": 120, "items": {"instinct_scroll": 1}}},
]

ENEMY_CATALOG = {
    "field_mouse": {"id": "field_mouse", "name": "Полевая мышь", "emoji": "🐭", "difficulty": 2, "skills": {"agility": 2, "instinct": 1}},
    "angry_crow": {"id": "angry_crow", "name": "Сердитая ворона", "emoji": "🐦‍⬛", "difficulty": 3, "skills": {"agility": 1, "instinct": 2}},
    "watch_owl": {"id": "watch_owl", "name": "Сова-сторож", "emoji": "🦉", "difficulty": 4, "skills": {"instinct": 3, "agility": 2}},
    "house_spider": {"id": "house_spider", "name": "Паук-домовик", "emoji": "🕷", "difficulty": 4, "skills": {"agility": 2, "instinct": 2}},
    "mushroom_goblin": {"id": "mushroom_goblin", "name": "Грибной пакостник", "emoji": "🍄", "difficulty": 5, "skills": {"instinct": 2, "strength": 1}},
    "mushroom_shaman": {"id": "mushroom_shaman", "name": "Грибной шаман", "emoji": "🍄", "difficulty": 5, "skills": {"instinct": 3, "agility": 1}},
    "glowing_slime": {"id": "glowing_slime", "name": "Светящийся слизень", "emoji": "🟢", "difficulty": 5, "skills": {"instinct": 2, "strength": 2}},
    "swamp_snake": {"id": "swamp_snake", "name": "Болотный уж", "emoji": "🐍", "difficulty": 6, "skills": {"agility": 2, "instinct": 2}},
    "thorn_hog": {"id": "thorn_hog", "name": "Колючий хрюк", "emoji": "🦔", "difficulty": 7, "skills": {"strength": 2, "agility": 1}},
    "bog_predator": {"id": "bog_predator", "name": "Трясинный хищник", "emoji": "🐊", "difficulty": 7, "skills": {"strength": 2, "instinct": 2}},
    "mountain_marten": {"id": "mountain_marten", "name": "Горная куница", "emoji": "🐾", "difficulty": 8, "skills": {"agility": 3, "instinct": 1}},
    "stone_beetle": {"id": "stone_beetle", "name": "Каменный жук", "emoji": "🪲", "difficulty": 8, "skills": {"strength": 2, "instinct": 2}},
    "swamp_rat": {"id": "swamp_rat", "name": "Болотная крыса", "emoji": "🐀", "difficulty": 10, "skills": {"instinct": 2, "agility": 1}},
    "raider_rat": {"id": "raider_rat", "name": "Крыса-мародёр", "emoji": "🐀", "difficulty": 10, "skills": {"agility": 3, "instinct": 1}},
    "pantry_spirit": {"id": "pantry_spirit", "name": "Дух кладовой", "emoji": "👻", "difficulty": 10, "skills": {"instinct": 3, "agility": 1}},
    "star_owl": {"id": "star_owl", "name": "Звёздный филин", "emoji": "🦉", "difficulty": 12, "skills": {"instinct": 4, "agility": 2}},
    "stone_marten": {"id": "stone_marten", "name": "Каменная куница", "emoji": "🐾", "difficulty": 13, "skills": {"agility": 2, "strength": 1}},
    "night_badger": {"id": "night_badger", "name": "Ночной барсук", "emoji": "🦡", "difficulty": 13, "skills": {"strength": 3, "agility": 2}},
    "root_worm": {"id": "root_worm", "name": "Корневой червь", "emoji": "🪱", "difficulty": 15, "skills": {"strength": 3, "instinct": 2}},
    "moss_guardian": {"id": "moss_guardian", "name": "Мшистый страж", "emoji": "🗿", "difficulty": 16, "skills": {"strength": 4, "instinct": 2}},
    "ruin_owl": {"id": "ruin_owl", "name": "Руинная сова", "emoji": "🦉", "difficulty": 18, "skills": {"instinct": 2, "agility": 1}},
    "bone_weasel": {"id": "bone_weasel", "name": "Костяная ласка", "emoji": "🦴", "difficulty": 18, "skills": {"agility": 4, "strength": 2}},
    "skull_raven": {"id": "skull_raven", "name": "Черепной ворон", "emoji": "🐦‍⬛", "difficulty": 19, "skills": {"instinct": 4, "agility": 2}},
    "ghost_raccoon_knight": {"id": "ghost_raccoon_knight", "name": "Призрачный енот-рыцарь", "emoji": "👻", "difficulty": 22, "skills": {"strength": 5, "instinct": 2}},
    "armored_rat": {"id": "armored_rat", "name": "Бронекрыс", "emoji": "🐀", "difficulty": 22, "skills": {"agility": 4, "strength": 3}},
    "shadow_marten": {"id": "shadow_marten", "name": "Теневая куница", "emoji": "🌑", "difficulty": 25, "skills": {"agility": 5, "instinct": 3}},
    "cursed_owl": {"id": "cursed_owl", "name": "Проклятая сова", "emoji": "🦉", "difficulty": 26, "skills": {"instinct": 6, "agility": 3}},
    "legend_keeper": {"id": "legend_keeper", "name": "Хранитель легенды", "emoji": "👑", "difficulty": 30, "skills": {"strength": 6, "agility": 6, "instinct": 6}},
    "ancient_raccoon": {"id": "ancient_raccoon", "name": "Древний енот", "emoji": "🦝", "difficulty": 32, "skills": {"strength": 7, "agility": 7, "instinct": 7}},
}

LOCATION_ENEMIES = {
    "forest_clearing": ['angry_crow', 'mushroom_goblin'],
    "quiet_thicket": ['mushroom_goblin', 'watch_owl'],
    "mushroom_path": ['watch_owl', 'field_mouse'],
    "old_deadfall": ['field_mouse', 'angry_crow'],
    "misty_stream": ['angry_crow', 'mushroom_goblin'],
    "stone_ravine": ['mushroom_goblin', 'watch_owl'],
    "forest_ruins": ['watch_owl', 'field_mouse'],
    "abandoned_watchhut": ['field_mouse', 'angry_crow'],
    "mossy_bridge": ['angry_crow', 'mushroom_goblin'],
    "foxglove_meadow": ['mushroom_goblin', 'watch_owl'],
    "hollow_stump_camp": ['watch_owl', 'field_mouse'],
    "glowing_mushroom_grove": ['field_mouse', 'angry_crow'],
    "silver_leaf_path": ['angry_crow', 'mushroom_goblin'],
    "raven_crossing": ['mushroom_goblin', 'watch_owl'],
    "old_hunter_trail": ['watch_owl', 'field_mouse'],
    "sleepy_pine_hill": ['glowing_slime', 'swamp_snake'],
    "dewberry_lowland": ['swamp_snake', 'thorn_hog'],
    "foggy_swamp": ['thorn_hog', 'stone_beetle'],
    "frog_song_marsh": ['stone_beetle', 'house_spider'],
    "reed_maze": ['house_spider', 'glowing_slime'],
    "sunken_log_path": ['glowing_slime', 'swamp_snake'],
    "firefly_pool": ['swamp_snake', 'thorn_hog'],
    "wet_root_tunnel": ['thorn_hog', 'stone_beetle'],
    "heron_shallows": ['stone_beetle', 'house_spider'],
    "stone_pass": ['house_spider', 'glowing_slime'],
    "windy_cliff_path": ['glowing_slime', 'swamp_snake'],
    "pebble_watch": ['swamp_snake', 'thorn_hog'],
    "goat_grass_slope": ['thorn_hog', 'stone_beetle'],
    "echoing_gully": ['stone_beetle', 'house_spider'],
    "cracked_boulder_gate": ['house_spider', 'glowing_slime'],
    "pine_needle_ridge": ['glowing_slime', 'swamp_snake'],
    "cloudberry_shelf": ['swamp_snake', 'thorn_hog'],
    "stormcrow_peak": ['thorn_hog', 'stone_beetle'],
    "dry_stream_bed": ['stone_beetle', 'house_spider'],
    "old_settlement_ruins": ['house_spider', 'glowing_slime'],
    "overgrown_well": ['bog_predator', 'mountain_marten'],
    "broken_cart_square": ['mountain_marten', 'swamp_rat'],
    "moss_roof_houses": ['swamp_rat', 'raider_rat'],
    "forgotten_pantry": ['raider_rat', 'pantry_spirit'],
    "chimney_crow_roost": ['pantry_spirit', 'ruin_owl'],
    "cracked_chapel_yard": ['ruin_owl', 'bog_predator'],
    "cellar_of_whispers": ['bog_predator', 'mountain_marten'],
    "ivy_clock_tower": ['mountain_marten', 'swamp_rat'],
    "moonlit_mill": ['swamp_rat', 'raider_rat'],
    "starry_thicket": ['raider_rat', 'pantry_spirit'],
    "firefly_constellation_path": ['pantry_spirit', 'ruin_owl'],
    "silver_moth_glade": ['ruin_owl', 'bog_predator'],
    "night_bloom_garden": ['bog_predator', 'mountain_marten'],
    "owl_mirror_lake": ['mountain_marten', 'swamp_rat'],
    "comet_fallen_clearing": ['swamp_rat', 'raider_rat'],
    "whispering_fern_field": ['raider_rat', 'pantry_spirit'],
    "blue_moon_copse": ['pantry_spirit', 'ruin_owl'],
    "astral_burrow": ['ruin_owl', 'bog_predator'],
    "lanternroot_path": ['bog_predator', 'mountain_marten'],
    "underground_roots": ['mountain_marten', 'swamp_rat'],
    "root_cathedral": ['stone_marten', 'night_badger'],
    "blind_mole_tunnels": ['night_badger', 'root_worm'],
    "amber_resin_caves": ['root_worm', 'moss_guardian'],
    "fossil_nest": ['moss_guardian', 'star_owl'],
    "deep_moss_chamber": ['star_owl', 'stone_marten'],
    "echo_root_maze": ['stone_marten', 'night_badger'],
    "buried_stream": ['night_badger', 'root_worm'],
    "stone_seed_vault": ['root_worm', 'moss_guardian'],
    "sleeping_earth_heart": ['moss_guardian', 'star_owl'],
    "giants_graveyard": ['star_owl', 'stone_marten'],
    "rib_bone_valley": ['stone_marten', 'night_badger'],
    "skull_hill": ['night_badger', 'root_worm'],
    "mammoth_moss_field": ['root_worm', 'moss_guardian'],
    "bone_wind_passage": ['moss_guardian', 'star_owl'],
    "giant_finger_bridge": ['star_owl', 'stone_marten'],
    "ancient_battlefield": ['stone_marten', 'night_badger'],
    "white_antler_grove": ['night_badger', 'root_worm'],
    "hollow_bone_caves": ['root_worm', 'moss_guardian'],
    "last_giant_camp": ['moss_guardian', 'star_owl'],
    "forgotten_raccoon_castle": ['star_owl', 'stone_marten'],
    "tailguard_gate": ['bone_weasel', 'skull_raven'],
    "dusty_banner_hall": ['skull_raven', 'ghost_raccoon_knight'],
    "moon_key_corridor": ['ghost_raccoon_knight', 'armored_rat'],
    "cracked_throne_room": ['armored_rat', 'bone_weasel'],
    "pantry_of_kings": ['bone_weasel', 'skull_raven'],
    "armor_rat_barracks": ['skull_raven', 'ghost_raccoon_knight'],
    "knight_raccoon_gallery": ['ghost_raccoon_knight', 'armored_rat'],
    "silver_crown_tower": ['armored_rat', 'bone_weasel'],
    "royal_burrow_keep": ['bone_weasel', 'skull_raven'],
    "black_grove": ['skull_raven', 'ghost_raccoon_knight'],
    "shadow_birch_path": ['ghost_raccoon_knight', 'armored_rat'],
    "cursed_acorn_field": ['armored_rat', 'bone_weasel'],
    "silent_owl_court": ['bone_weasel', 'skull_raven'],
    "thornmoon_thicket": ['skull_raven', 'ghost_raccoon_knight'],
    "black_sap_swamp": ['ghost_raccoon_knight', 'armored_rat'],
    "hollow_shadow_den": ['armored_rat', 'bone_weasel'],
    "eclipse_root_circle": ['bone_weasel', 'skull_raven'],
    "dead_star_clearing": ['skull_raven', 'ghost_raccoon_knight'],
    "night_crown_forest": ['ghost_raccoon_knight', 'armored_rat'],
    "path_of_legends": ['ancient_raccoon', 'shadow_marten'],
    "first_legend_step": ['shadow_marten', 'cursed_owl'],
    "elder_tail_shrine": ['cursed_owl', 'legend_keeper'],
    "skyroot_summit": ['legend_keeper', 'ancient_raccoon'],
    "gate_before_legend": ['ancient_raccoon', 'shadow_marten'],
    "raccoon_legend_throne": ['shadow_marten', 'cursed_owl'],
}


ENEMY_TEXTS = {
    "field_mouse": {"event": "🐭 Полевая мышь выскочила из травы и попыталась утащить находку.", "win": "Енот распушил хвост, сделал важный выпад и победил.", "lose": "Мышь юркнула в кусты, а енот остался озадаченно шуршать листвой."},
    "angry_crow": {"event": "🐦‍⬛ Сердитая ворона налетела сверху и громко потребовала всё блестящее.", "win": "Енот ловко отскочил, шикнул на ворону и отстоял добычу.", "lose": "Енот героически сделал вид, что это была тактическая прогулка назад."},
    "mushroom_goblin": {"event": "🍄 Грибной пакостник вынырнул из пней и начал дразнить енота.", "win": "Енот перехитрил пакостника и прогнал его в чащу.", "lose": "Пакостник насыпал спор в нос, и енот отступил, чихая."},
    "thorn_hog": {"event": "🦔 Колючий хрюк преградил тропу и упрямо засопел.", "win": "Енот обошёл колючки, сделал рывок и победил.", "lose": "Хрюк боднул воздух так грозно, что енот решил не спорить."},
    "swamp_rat": {"event": "🐀 Болотная крыса устроила грязную засаду у воды.", "win": "Енот увернулся от брызг и выгнал крысу с берега.", "lose": "Крыса обдала енота болотной жижей, и бой сорвался."},
    "stone_marten": {"event": "🐾 Каменная куница скользнула по камням и бросилась в атаку.", "win": "Енот точно рассчитал момент и перехватил инициативу.", "lose": "Куница оказалась слишком быстрой, енот едва ушёл от погони."},
    "ruin_owl": {"event": "🦉 Руинная сова бесшумно спикировала из древних арок.", "win": "Енот выдержал жуткий взгляд и заставил сову отступить.", "lose": "Сова кругами нагнала страху, и енот спешно ретировался."},
}


ITEM_CATALOG = {
    "food": {"name": "Яблоко", "emoji": "🍎", "category": "food", "need": "satiety", "restore": 50, "price": 5},
    "hearty_snack": {"name": "Сытный перекус", "emoji": "🥪", "category": "food", "need": "satiety", "restore": 90, "price": 12},
    "forest_honey": {"name": "Лесной мёд", "emoji": "🍯", "category": "food", "need": "satiety", "restore": 140, "price": 22},
    "soap": {"name": "Мыло", "emoji": "🧼", "category": "cleanliness", "need": "cleanliness", "restore": 50, "price": 7},
    "fluffy_shampoo": {"name": "Пушистый шампунь", "emoji": "🫧", "category": "cleanliness", "need": "cleanliness", "restore": 90, "price": 14},
    "comb": {"name": "Гребень", "emoji": "🪮", "category": "cleanliness", "need": "cleanliness", "restore": 35, "price": 4},
    "toy": {"name": "Мячик", "emoji": "🎾", "category": "love", "need": "love", "restore": 50, "price": 8},
    "yarn_ball": {"name": "Клубок", "emoji": "🧶", "category": "love", "need": "love", "restore": 80, "price": 14},
    "fun_toy": {"name": "Забавная игрушка", "emoji": "🪀", "category": "love", "need": "love", "restore": 120, "price": 24},
    "energy_potion": {"name": "Малое зелье энергии", "emoji": "⚡", "category": "energy", "need": "energy", "restore": 50, "price": 12},
    "big_energy_potion": {"name": "Большое зелье энергии", "emoji": "🔋", "category": "energy", "need": "energy", "restore": 100, "price": 25},
}

SHOP_CATEGORIES = {
    "food": {"id": "food", "title": "Еда", "emoji": "🍖", "description": "Что-то вкусное для голодного енота."},
    "household": {"id": "household", "title": "Быт", "emoji": "🧺", "description": "Полезные вещи для чистоты и уюта."},
    "toys": {"id": "toys", "title": "Игрушки", "emoji": "🧸", "description": "Предметы для игр и хорошего настроения."},
    "potions": {"id": "potions", "title": "Зелья", "emoji": "🧪", "description": "Зелья для восстановления сил."},
    "weapons": {"id": "weapons", "title": "Оружие", "emoji": "🗡️", "description": "Будущий раздел боевого снаряжения."},
    "armor": {"id": "armor", "title": "Броня", "emoji": "🛡️", "description": "Будущий раздел защитного снаряжения."},
    "accessories": {"id": "accessories", "title": "Аксессуары", "emoji": "💍", "description": "Будущий раздел редких аксессуаров."},
    "materials": {"id": "materials", "title": "Материалы", "emoji": "🪵", "description": "Будущий раздел ресурсов для крафта."},
}

SHOP_ITEMS = {
    "food": {"id": "food", "category": "food", "name": "Яблоко", "description": "Сочное лесное яблоко.", "price": 5, "effects": {"satiety": 50}},
    "hearty_snack": {"id": "hearty_snack", "category": "food", "name": "Сытный перекус", "description": "Плотный перекус для долгих прогулок.", "price": 12, "effects": {"satiety": 90}},
    "forest_honey": {"id": "forest_honey", "category": "food", "name": "Лесной мёд", "description": "Сладкий мёд, найденный в чаще.", "price": 22, "effects": {"satiety": 140}},
    "soap": {"id": "soap", "category": "household", "name": "Мыло", "description": "Помогает быстро отмыть лапки и хвост.", "price": 7, "effects": {"cleanliness": 50}},
    "fluffy_shampoo": {"id": "fluffy_shampoo", "category": "household", "name": "Пушистый шампунь", "description": "Ароматный шампунь для идеальной шерсти.", "price": 14, "effects": {"cleanliness": 90}},
    "comb": {"id": "comb", "category": "household", "name": "Гребень", "description": "Простой гребень для быстрой укладки.", "price": 4, "effects": {"cleanliness": 35}},
    "toy": {"id": "toy", "category": "toys", "name": "Мячик", "description": "Любимая игрушка для весёлой игры.", "price": 8, "effects": {"love": 50}},
    "yarn_ball": {"id": "yarn_ball", "category": "toys", "name": "Клубок", "description": "Мягкий клубок для долгих игр.", "price": 14, "effects": {"love": 80}},
    "fun_toy": {"id": "fun_toy", "category": "toys", "name": "Забавная игрушка", "description": "Яркая игрушка, поднимающая настроение.", "price": 24, "effects": {"love": 120}},
    "energy_potion": {"id": "energy_potion", "category": "potions", "name": "Малое зелье энергии", "description": "Быстро возвращает силы после дел.", "price": 12, "effects": {"energy": 50}},
    "big_energy_potion": {"id": "big_energy_potion", "category": "potions", "name": "Большое зелье энергии", "description": "Мощное зелье для полного заряда.", "price": 25, "effects": {"energy": 100}},
}


def update_pet_mood(pet: dict[str, Any]) -> str:
    max_needs = get_pet_max_needs(pet)
    satiety = int(pet.get("satiety", DEFAULT_NEEDS["satiety"]))
    cleanliness = int(pet.get("cleanliness", DEFAULT_NEEDS["cleanliness"]))
    love = int(pet.get("love", DEFAULT_NEEDS["love"]))
    energy = int(pet.get("energy", DEFAULT_NEEDS["energy"]))

    if satiety < max_needs["satiety"] * 0.2 or cleanliness < max_needs["cleanliness"] * 0.2 or love < max_needs["love"] * 0.2:
        mood = "distressed"
    elif satiety < max_needs["satiety"] * 0.4 or cleanliness < max_needs["cleanliness"] * 0.4 or love < max_needs["love"] * 0.4 or energy < max_needs["energy"] * 0.2:
        mood = "tired"
    elif satiety >= max_needs["satiety"] * 0.8 and cleanliness >= max_needs["cleanliness"] * 0.8 and love >= max_needs["love"] * 0.8 and energy >= max_needs["energy"] * 0.6:
        mood = "happy"
    else:
        mood = "normal"

    pet["mood"] = mood
    return mood


def get_runaway_risk(pet: dict[str, Any]) -> str:
    love = int(pet.get("love", DEFAULT_NEEDS["love"]))
    love_max = get_pet_max_needs(pet)["love"]
    if love < love_max * 0.15:
        return "high"
    if love < love_max * 0.30:
        return "medium"
    if love < love_max * 0.45:
        return "low"
    return "none"


def utc_now() -> datetime:
    return datetime.now(UTC)


def parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _ensure_storage_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}", encoding="utf-8")


def clamp_need(value: int) -> int:
    return max(0, min(100, value))


def get_max_need_value(level: int) -> int:
    safe_level = level if isinstance(level, int) and level > 0 else 1
    safe_level = max(1, min(MAX_LEVEL, safe_level))
    # Stage 13 foundation: higher levels require more attention and maintenance.
    return 100 + (safe_level - 1) * 12 + max(0, safe_level - 30) * 8 + max(0, safe_level - 70) * 15


def get_pet_max_needs(pet: dict[str, Any]) -> dict[str, int]:
    level = pet.get("level", 1) if isinstance(pet, dict) else 1
    max_value = get_max_need_value(level if isinstance(level, int) else 1)
    return {"satiety": max_value, "cleanliness": max_value, "love": max_value, "energy": max_value}


def clamp_need_by_level(pet: dict[str, Any], need: str, value: int) -> int:
    need_max = get_pet_max_needs(pet).get(need, 100)
    return max(0, min(need_max, value))


def ensure_pet_defaults(user_data: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    changed = False
    pet = user_data.get("pet")
    if not isinstance(pet, dict):
        return user_data, changed

    for key, default in DEFAULT_NEEDS.items():
        if not isinstance(pet.get(key), int):
            pet[key] = default
            changed = True

    if not isinstance(pet.get("level"), int) or int(pet.get("level", 0)) < 1:
        pet["level"] = 1
        changed = True
    elif pet["level"] > MAX_LEVEL:
        pet["level"] = MAX_LEVEL
        changed = True
    if not isinstance(pet.get("exp"), int) or int(pet.get("exp", 0)) < 0:
        pet["exp"] = 0
        changed = True
    if not isinstance(pet.get("currency"), int) or int(pet.get("currency", 0)) < 0:
        pet["currency"] = 0
        changed = True

    is_legendary = int(pet.get("level", 1)) >= LEGEND_LEVEL
    if pet.get("legendary") is not is_legendary:
        pet["legendary"] = is_legendary
        changed = True

    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        pet["inventory"] = DEFAULT_INVENTORY.copy()
        changed = True
    else:
        for item, default in DEFAULT_INVENTORY.items():
            if not isinstance(inventory.get(item), int):
                inventory[item] = default
                changed = True

    skills = pet.get("skills")
    if not isinstance(skills, dict):
        pet["skills"] = DEFAULT_SKILLS.copy()
        changed = True
    else:
        for skill, default in DEFAULT_SKILLS.items():
            if not isinstance(skills.get(skill), int):
                skills[skill] = default
                changed = True

    travel = pet.get("travel")
    if not isinstance(travel, dict):
        pet["travel"] = DEFAULT_TRAVEL.copy()
        changed = True
    else:
        if not isinstance(travel.get("total_travels"), int):
            travel["total_travels"] = DEFAULT_TRAVEL["total_travels"]
            changed = True
        if not (isinstance(travel.get("last_event"), str) or travel.get("last_event") is None):
            travel["last_event"] = DEFAULT_TRAVEL["last_event"]
            changed = True
    if "battle" not in pet:
        pet["battle"] = DEFAULT_BATTLE
        changed = True

    updated_at = parse_datetime(pet.get("updated_at"))
    if updated_at is None:
        updated_at = utc_now()
        pet["updated_at"] = updated_at.isoformat()
        changed = True

    if parse_datetime(pet.get("last_needs_update_at")) is None:
        pet["last_needs_update_at"] = updated_at.isoformat()
        changed = True
    if not isinstance(pet.get("mood"), str):
        pet["mood"] = "normal"
        changed = True

    for need in DEFAULT_NEEDS:
        current = pet.get(need, DEFAULT_NEEDS[need])
        if isinstance(current, int):
            clamped = clamp_need_by_level(pet, need, current)
            if clamped != current:
                pet[need] = clamped
                changed = True

    return user_data, changed


def apply_elapsed_need_ticks(pet: dict[str, Any], ticks: int) -> None:
    if ticks <= 0:
        return
    pet["satiety"] = clamp_need_by_level(pet, "satiety", int(pet.get("satiety", 0)) - (2 * ticks))
    pet["cleanliness"] = clamp_need_by_level(pet, "cleanliness", int(pet.get("cleanliness", 0)) - (1 * ticks))
    pet["love"] = clamp_need_by_level(pet, "love", int(pet.get("love", 0)) - (1 * ticks))
    pet["energy"] = clamp_need_by_level(pet, "energy", int(pet.get("energy", 0)) + (3 * ticks))


def recalculate_needs(user_data: dict[str, Any]) -> bool:
    user_data, changed = ensure_pet_defaults(user_data)
    pet = user_data.get("pet")
    if not isinstance(pet, dict):
        return changed

    last_update = parse_datetime(pet.get("last_needs_update_at"))
    if last_update is None:
        last_update = utc_now()
        pet["last_needs_update_at"] = last_update.isoformat()
        return True

    now = utc_now()
    elapsed = now - last_update
    tick_seconds = NEEDS_TICK_MINUTES * 60
    ticks = int(elapsed.total_seconds() // tick_seconds)
    if ticks <= 0:
        update_pet_mood(pet)
        return changed

    apply_elapsed_need_ticks(pet, ticks)
    update_pet_mood(pet)
    pet["last_needs_update_at"] = (last_update + timedelta(seconds=ticks * tick_seconds)).isoformat()
    return True


def load_users() -> dict[str, Any]:
    _ensure_storage_file()

    raw = USERS_FILE.read_text(encoding="utf-8").strip()
    if not raw:
        return {}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        return {}

    return data


def save_users(users: dict[str, Any]) -> None:
    _ensure_storage_file()
    USERS_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")


def get_user(user_id: int) -> dict[str, Any] | None:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return None

    user, changed = ensure_pet_defaults(user)
    if changed:
        users[str(user_id)] = user
        save_users(users)

    return user


def touch_user_needs(user_id: int) -> dict[str, Any] | None:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return None

    needs_changed = recalculate_needs(user)
    if needs_changed:
        users[str(user_id)] = user
        save_users(users)
    return user




def refresh_user_metadata_from_chat(user_id: int, chat: Any) -> dict[str, Any]:
    users = load_users()
    key = str(user_id)
    user = users.get(key)
    if not isinstance(user, dict):
        user = {}

    username = getattr(chat, "username", None)
    first_name = getattr(chat, "first_name", None)
    last_name = getattr(chat, "last_name", None)
    is_bot = getattr(chat, "is_bot", None)

    user["username"] = username if isinstance(username, str) else None
    user["first_name"] = first_name if isinstance(first_name, str) else None
    user["last_name"] = last_name if isinstance(last_name, str) else None
    if isinstance(is_bot, bool):
        user["is_bot"] = is_bot

    language_code = getattr(chat, "language_code", None)
    if isinstance(language_code, str):
        user["language_code"] = language_code

    user["last_seen_at"] = utc_now().isoformat()

    users[key] = user
    save_users(users)
    return user


def refresh_user_metadata(user_id: int, telegram_user: Any) -> dict[str, Any]:
    return refresh_user_metadata_from_chat(user_id, telegram_user)

def has_pet(user_id: int) -> bool:
    user = get_user(user_id)
    return bool(user and isinstance(user.get("pet"), dict))


def create_pet(user_id: int, name: str, gender: str) -> dict[str, Any]:
    users = load_users()
    now = utc_now().isoformat()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        user = {}
    user["pet"] = {
            "name": name,
            "gender": gender,
            "level": 1,
            "exp": 0,
            "currency": 0,
            "mood": "normal",
            "satiety": DEFAULT_NEEDS["satiety"],
            "cleanliness": DEFAULT_NEEDS["cleanliness"],
            "love": DEFAULT_NEEDS["love"],
            "energy": DEFAULT_NEEDS["energy"],
            "skills": DEFAULT_SKILLS.copy(),
            "inventory": DEFAULT_INVENTORY.copy(),
            "travel": DEFAULT_TRAVEL.copy(),
            "created_at": now,
            "updated_at": now,
            "last_needs_update_at": now,
        }
    users[str(user_id)] = user
    save_users(users)
    return users[str(user_id)]


def consume_inventory_item(pet: dict[str, Any], item: str) -> bool:
    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        return False

    count = inventory.get(item)
    if not isinstance(count, int) or count <= 0:
        return False

    inventory[item] = count - 1
    return True


def get_item_catalog() -> dict[str, dict[str, Any]]:
    return {key: value.copy() for key, value in ITEM_CATALOG.items()}


def get_shop_items() -> dict[str, int]:
    return {key: item["price"] for key, item in SHOP_ITEMS.items()}


def get_shop_categories() -> dict[str, dict[str, Any]]:
    return {key: value.copy() for key, value in SHOP_CATEGORIES.items() if key in {"food", "household", "toys", "potions"}}


def get_shop_items_by_category(category_id: str) -> list[dict[str, Any]]:
    return [item.copy() for item in SHOP_ITEMS.values() if item.get("category") == category_id]


def get_shop_item(item_id: str) -> dict[str, Any] | None:
    item = SHOP_ITEMS.get(item_id)
    return item.copy() if isinstance(item, dict) else None


def can_afford(currency: int, price: int) -> bool:
    return currency >= price


def add_inventory_item(pet: dict[str, Any], item: str, amount: int = 1) -> int:
    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        pet["inventory"] = DEFAULT_INVENTORY.copy()
        inventory = pet["inventory"]

    current = inventory.get(item, 0)
    current_count = current if isinstance(current, int) and current >= 0 else 0
    inventory[item] = current_count + amount
    return inventory[item]


def buy_item(user_data: dict[str, Any], item_key: str) -> tuple[bool, int, int]:
    user_data, _ = ensure_pet_defaults(user_data)
    recalculate_needs(user_data)
    pet = user_data.get("pet")
    if not isinstance(pet, dict):
        return False, 0, 0

    price = SHOP_ITEMS.get(item_key, {}).get("price")
    if not isinstance(price, int):
        return False, 0, 0

    currency = pet.get("currency", 0)
    currency_value = currency if isinstance(currency, int) and currency >= 0 else 0
    pet["currency"] = currency_value

    if not can_afford(currency_value, price):
        count = int(pet.get("inventory", {}).get(item_key, 0)) if isinstance(pet.get("inventory"), dict) else 0
        return False, currency_value, count

    pet["currency"] = currency_value - price
    new_count = add_inventory_item(pet, item_key, amount=1)
    pet["updated_at"] = utc_now().isoformat()
    return True, pet["currency"], new_count


def shop_purchase(user_id: int, item_key: str) -> tuple[bool, int, int, int, dict[str, Any] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, 0, 0, None

    items = get_shop_items()
    price = items.get(item_key, 0)
    success, balance, count = buy_item(user, item_key)

    users[str(user_id)] = user
    save_users(users)
    return success, price, balance, count, user


def update_pet_need(user_id: int, need: str | None = None, amount: int | None = None, inventory_item: str = "") -> tuple[bool, dict[str, Any] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, None

    changed = recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, None

    item_data = ITEM_CATALOG.get(inventory_item)
    resolved_need = item_data.get("need") if isinstance(item_data, dict) else need
    resolved_amount = item_data.get("restore") if isinstance(item_data, dict) else amount

    if not isinstance(resolved_need, str) or not isinstance(resolved_amount, int):
        if changed:
            users[str(user_id)] = user
            save_users(users)
        return False, None

    if not consume_inventory_item(pet, inventory_item):
        if changed:
            users[str(user_id)] = user
            save_users(users)
        return False, user

    current_value = pet.get(resolved_need, 0)
    if not isinstance(current_value, int):
        current_value = 0

    pet[resolved_need] = clamp_need_by_level(pet, resolved_need, current_value + resolved_amount)
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, user


def has_enough_energy(pet: dict[str, Any], amount: int) -> bool:
    energy = pet.get("energy", 0)
    return isinstance(energy, int) and energy >= amount


def exp_to_next_level(level: int) -> int | None:
    safe_level = level if isinstance(level, int) and level > 0 else 1
    safe_level = max(1, safe_level)
    if safe_level >= MAX_LEVEL:
        return None
    if safe_level < 20:
        return 50 + (safe_level - 1) * 35
    if safe_level < 50:
        return 900 + (safe_level - 20) * 120
    if safe_level < 80:
        return 4500 + (safe_level - 50) * 350
    return 15000 + (safe_level - 80) * 1200


def apply_level_ups(pet: dict[str, Any]) -> int:
    level = pet.get("level", 1)
    exp = pet.get("exp", 0)
    currency = pet.get("currency", 0)

    pet["level"] = level if isinstance(level, int) and level > 0 else 1
    pet["level"] = min(MAX_LEVEL, pet["level"])
    pet["exp"] = exp if isinstance(exp, int) and exp >= 0 else 0
    pet["currency"] = currency if isinstance(currency, int) and currency >= 0 else 0

    levels_gained = 0
    while pet["level"] < MAX_LEVEL:
        required = exp_to_next_level(pet["level"])
        if required is None or pet["exp"] < required:
            break
        pet["exp"] -= required
        pet["level"] += 1
        pet["currency"] += 10
        levels_gained += 1

    if pet["level"] >= MAX_LEVEL:
        pet["level"] = MAX_LEVEL
        pet["exp"] = 0

    pet["legendary"] = pet["level"] >= LEGEND_LEVEL
    return levels_gained


def add_exp(pet: dict[str, Any], amount: int) -> int:
    safe_amount = amount if isinstance(amount, int) and amount > 0 else 0
    current_exp = pet.get("exp", 0)
    pet["exp"] = (current_exp if isinstance(current_exp, int) and current_exp >= 0 else 0) + safe_amount
    return apply_level_ups(pet)


def train_skill(user_id: int, skill_name: str) -> tuple[bool, int, dict[str, Any] | None, str | None]:
    if skill_name not in DEFAULT_SKILLS:
        return False, 0, None, None

    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, None, None

    recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, 0, None, None

    if not has_enough_energy(pet, 15):
        users[str(user_id)] = user
        save_users(users)
        return False, 0, user, None

    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        inventory = DEFAULT_INVENTORY.copy()
        pet["inventory"] = inventory

    scroll_by_skill = {"strength": "strength_scroll", "agility": "agility_scroll", "instinct": "instinct_scroll"}
    scroll_key = scroll_by_skill[skill_name]
    scroll_count = inventory.get(scroll_key, 0)
    if not isinstance(scroll_count, int) or scroll_count < 1:
        users[str(user_id)] = user
        save_users(users)
        return False, 0, user, scroll_key

    skills = pet.get("skills")
    if not isinstance(skills, dict):
        pet["skills"] = DEFAULT_SKILLS.copy()
        skills = pet["skills"]

    skill_value = skills.get(skill_name, 0)
    if not isinstance(skill_value, int):
        skill_value = 0

    skills[skill_name] = skill_value + 1
    pet["energy"] = clamp_need_by_level(pet, "energy", int(pet.get("energy", 0)) - 15)
    inventory[scroll_key] = scroll_count - 1
    levels_gained = add_exp(pet, 5)
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, levels_gained, user, scroll_key


def get_travel_locations() -> dict[str, dict[str, Any]]:
    return TRAVEL_LOCATIONS


def get_travel_event(event_id: str) -> dict[str, Any] | None:
    for event in TRAVEL_EVENTS:
        if event.get("id") == event_id:
            return event
    return None


def calculate_enemy_win_chance(pet: dict[str, Any], enemy: dict[str, Any]) -> int:
    skills = pet.get("skills", {}) if isinstance(pet.get("skills"), dict) else {}
    strength = skills.get("strength", 0) if isinstance(skills.get("strength"), int) else 0
    agility = skills.get("agility", 0) if isinstance(skills.get("agility"), int) else 0
    instinct = skills.get("instinct", 0) if isinstance(skills.get("instinct"), int) else 0
    pet_level = pet.get("level", 1) if isinstance(pet.get("level"), int) else 1
    difficulty = enemy.get("difficulty", 1) if isinstance(enemy.get("difficulty"), int) else 1

    base = 50
    skill_score = int(strength * 2 + agility * 1.5 + instinct * 1.5)
    difficulty_penalty = difficulty * 4
    level_bonus = pet_level * 2
    chance = base + skill_score + level_bonus - difficulty_penalty
    return max(15, min(90, chance))


def choose_travel_event(pet: dict[str, Any], location_id: str) -> dict[str, Any]:
    skills = pet.get("skills")
    instinct = skills.get("instinct", 0) if isinstance(skills, dict) else 0
    weights = {"good": 24, "neutral": 28, "bad": 14, "rare": 4, "enemy": 30}
    if isinstance(instinct, int) and instinct >= 7:
        weights = {"good": 30, "neutral": 33, "bad": 12, "rare": 5, "enemy": 20}
    elif isinstance(instinct, int) and instinct >= 3:
        weights = {"good": 27, "neutral": 31, "bad": 13, "rare": 4, "enemy": 25}

    event_types = list(weights.keys())
    chosen_type = random.choices(event_types, weights=[weights[t] for t in event_types], k=1)[0]
    if chosen_type == "enemy":
        available = LOCATION_ENEMIES.get(location_id, [])
        enemy_id = random.choice(available) if available else "field_mouse"
        enemy = ENEMY_CATALOG.get(enemy_id, ENEMY_CATALOG["field_mouse"])
        texts = ENEMY_TEXTS.get(enemy_id, ENEMY_TEXTS["field_mouse"])
        return {
            "id": f"enemy_{enemy_id}",
            "type": "enemy",
            "enemy_id": enemy_id,
            "text": texts["event"],
            "enemy": enemy,
            "win_text": texts["win"],
            "lose_text": texts["lose"],
        }

    pool = [event for event in TRAVEL_EVENTS if event.get("type") == chosen_type]
    return random.choice(pool)


def perform_travel(user_id: int, location_id: str, allow_above_level: bool = False) -> tuple[bool, int, list[str], dict[str, Any] | None, dict[str, Any] | None, dict[str, Any] | None, dict[str, int] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, ["pet is missing"], None, None, None, None

    recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, 0, ["pet is missing"], None, None, None, None
    if isinstance(pet.get("battle"), dict):
        return False, 0, ["battle_pending"], user, None, None, None

    location = TRAVEL_LOCATIONS.get(location_id)
    if not isinstance(location, dict):
        return False, 0, ["unknown location"], user, None, None, None

    level = pet.get("level", 1) if isinstance(pet.get("level"), int) else 1
    if not allow_above_level and level < location.get("min_level", 1):
        return False, 0, [f"level >= {location.get('min_level', 1)}"], user, location, None, None

    costs = location.get("costs", {})
    missing = []
    for need in ("energy", "satiety", "cleanliness"):
        required = int(costs.get(need, 0))
        current = pet.get(need, 0)
        if not isinstance(current, int) or current < required:
            missing.append(f"{need} >= {required}")
    if missing:
        users[str(user_id)] = user
        save_users(users)
        return False, 0, missing, user, location, None, None

    spent = {k: int(v) for k, v in costs.items() if isinstance(v, int)}
    for need, value in spent.items():
        pet[need] = clamp_need_by_level(pet, need, int(pet.get(need, 0)) - value)

    rewards = location.get("rewards", {})
    base_exp = int(rewards.get("exp", 0))
    base_currency = int(rewards.get("currency", 0))
    pet["currency"] = int(pet.get("currency", 0)) + base_currency if isinstance(pet.get("currency"), int) else base_currency
    levels_gained = add_exp(pet, base_exp)

    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        pet["inventory"] = DEFAULT_INVENTORY.copy()
        inventory = pet["inventory"]

    event = choose_travel_event(pet, location_id)
    effects = event.get("effects", {}) if isinstance(event.get("effects"), dict) else {}
    event_exp = int(effects.get("exp", 0)) if isinstance(effects.get("exp", 0), int) else 0
    event_currency = int(effects.get("currency", 0)) if isinstance(effects.get("currency", 0), int) else 0
    if event_exp:
        levels_gained += add_exp(pet, event_exp)
    if event_currency:
        pet["currency"] = int(pet.get("currency", 0)) + event_currency if isinstance(pet.get("currency"), int) else event_currency

    for need, delta in (effects.get("needs", {}) if isinstance(effects.get("needs"), dict) else {}).items():
        if isinstance(delta, int):
            pet[need] = clamp_need_by_level(pet, need, int(pet.get(need, 0)) + delta)

    items_delta = {}
    for item, amount in (effects.get("items", {}) if isinstance(effects.get("items"), dict) else {}).items():
        if isinstance(amount, int):
            current = inventory.get(item, 0)
            inventory[item] = (current if isinstance(current, int) else 0) + amount
            items_delta[item] = amount

    enemy_result = {"win": False, "chance": 0, "roll": 0, "extra_exp": 0, "extra_currency": 0, "penalties": {}, "drop_items": {}}
    if event.get("type") == "enemy":
        enemy = event.get("enemy", {}) if isinstance(event.get("enemy"), dict) else {}
        chance = calculate_enemy_win_chance(pet, enemy)
        pet["battle"] = {
            "enemy_id": event.get("enemy_id", "field_mouse"),
            "location_id": location_id,
            "win_chance": chance,
            "travel_context": {
                "location_id": location_id,
                "base_exp": base_exp,
                "base_currency": base_currency,
                "event_id": None,
                "spent_energy": spent.get("energy", 0),
                "spent_satiety": spent.get("satiety", 0),
                "spent_cleanliness": spent.get("cleanliness", 0),
                "items_delta": items_delta,
                "levels_gained": levels_gained,
            },
            "created_at": utc_now().isoformat(),
        }
        enemy_result["pending"] = True
        enemy_result["chance"] = chance

    travel = pet.get("travel")
    if not isinstance(travel, dict):
        pet["travel"] = DEFAULT_TRAVEL.copy()
        travel = pet["travel"]
    travel["total_travels"] = int(travel.get("total_travels", 0)) + 1
    travel["last_event"] = f"Встреча: {event.get('enemy', {}).get('name', 'Неизвестный враг')}" if event.get("type") == "enemy" else event.get("id")

    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, levels_gained, [], user, location, event, {"exp": base_exp, "currency": base_currency, "event_exp": event_exp, "event_currency": event_currency, "enemy_result": enemy_result, **spent, **items_delta}


def get_enemy(enemy_id: str) -> dict[str, Any]:
    return ENEMY_CATALOG.get(enemy_id, ENEMY_CATALOG["field_mouse"])


def resolve_battle_attack(user_id: int) -> tuple[bool, dict[str, Any] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, None
    recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, None
    battle = pet.get("battle")
    if not isinstance(battle, dict):
        users[str(user_id)] = user
        save_users(users)
        return False, user
    enemy = get_enemy(str(battle.get("enemy_id", "field_mouse")))
    chance = max(15, min(90, int(battle.get("win_chance", calculate_enemy_win_chance(pet, enemy)))))
    win = random.randint(1, 100) <= chance
    difficulty = enemy.get("difficulty", 1) if isinstance(enemy.get("difficulty"), int) else 1
    inventory = pet.get("inventory") if isinstance(pet.get("inventory"), dict) else DEFAULT_INVENTORY.copy()
    pet["inventory"] = inventory
    travel_context = battle.get("travel_context", {}) if isinstance(battle.get("travel_context"), dict) else {}
    result = {"win": win, "chance": chance, "enemy": enemy, "drop_items": {}, "levels_gained": 0, "travel_context": travel_context, "pet": pet, "pet_name": pet.get("name", "Енот")}
    if win:
        extra_exp = difficulty + 2
        extra_currency = max(2, difficulty)
        result["levels_gained"] = add_exp(pet, extra_exp)
        result["travel_context"]["levels_gained"] = int(result["travel_context"].get("levels_gained", 0)) + result["levels_gained"]
        pet["currency"] = int(pet.get("currency", 0)) + extra_currency if isinstance(pet.get("currency"), int) else extra_currency
        result["extra_exp"] = extra_exp
        result["extra_currency"] = extra_currency
        if random.random() < 0.22:
            drop_item = random.choice(["food", "soap", "toy", "energy_potion", "hearty_snack", "comb"])
            inventory[drop_item] = int(inventory.get(drop_item, 0)) + 1
            result["drop_items"][drop_item] = 1
        if random.random() < 0.10:
            scroll = random.choice(["strength_scroll", "agility_scroll", "instinct_scroll"])
            inventory[scroll] = int(inventory.get(scroll, 0)) + 1
            result["drop_items"][scroll] = result["drop_items"].get(scroll, 0) + 1
    else:
        extra = difficulty // 3
        penalties = {"energy": -(10 + extra), "cleanliness": -(8 + extra), "love": -(6 + extra), "satiety": -(4 + extra)}
        for need, delta in penalties.items():
            pet[need] = clamp_need_by_level(pet, need, int(pet.get(need, 0)) + delta)
        result["penalties"] = penalties
    pet["battle"] = None
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, result


def resolve_battle_run(user_id: int) -> tuple[bool, dict[str, Any] | None]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, None
    recalculate_needs(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, None
    battle = pet.get("battle")
    if not isinstance(battle, dict):
        users[str(user_id)] = user
        save_users(users)
        return False, user
    enemy = get_enemy(str(battle.get("enemy_id", "field_mouse")))
    difficulty = enemy.get("difficulty", 1) if isinstance(enemy.get("difficulty"), int) else 1
    skills = pet.get("skills", {}) if isinstance(pet.get("skills"), dict) else {}
    agility = skills.get("agility", 0) if isinstance(skills.get("agility"), int) else 0
    instinct = skills.get("instinct", 0) if isinstance(skills.get("instinct"), int) else 0
    flee_chance = max(20, min(90, 55 + agility * 3 + instinct - difficulty * 7))
    escaped = random.randint(1, 100) <= flee_chance
    penalties = {"energy": -8} if escaped else {"energy": -14, "cleanliness": -7, "love": -5}
    for need, delta in penalties.items():
        pet[need] = clamp_need_by_level(pet, need, int(pet.get(need, 0)) + delta)
    pet["battle"] = None
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    travel_context = battle.get("travel_context", {}) if isinstance(battle.get("travel_context"), dict) else {}
    return True, {"escaped": escaped, "enemy": enemy, "flee_chance": flee_chance, "penalties": penalties, "travel_context": travel_context, "pet": pet, "pet_name": pet.get("name", "Енот")}


def get_storage_stats() -> dict[str, float | int | str]:
    users = load_users()
    total_users = len(users)
    users_with_pet = 0
    total_pets = 0
    levels_sum = 0

    for user_data in users.values():
        if not isinstance(user_data, dict):
            continue
        pet = user_data.get("pet")
        if not isinstance(pet, dict):
            continue

        users_with_pet += 1
        total_pets += 1
        level = pet.get("level", 1)
        safe_level = level if isinstance(level, int) and level > 0 else 1
        levels_sum += safe_level

    average_level = (levels_sum / total_pets) if total_pets else 0.0
    return {
        "total_users": total_users,
        "users_with_pet": users_with_pet,
        "total_pets": total_pets,
        "average_level": round(average_level, 1),
        "storage_path": str(USERS_FILE),
    }


def create_users_backup() -> tuple[bool, str]:
    _ensure_storage_file()
    backups_dir = DATA_DIR / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)

    source = USERS_FILE
    if not source.exists():
        return False, "Файл хранилища не найден."

    timestamp = utc_now().strftime("%Y%m%d_%H%M%S")
    backup_path = backups_dir / f"users_{timestamp}.json"
    backup_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return True, str(backup_path)


def get_all_users() -> list[tuple[int, dict[str, Any]]]:
    users = load_users()
    rows: list[tuple[int, dict[str, Any]]] = []
    changed = False
    for key, value in users.items():
        try:
            user_id = int(key)
        except (ValueError, TypeError):
            continue
        if not isinstance(value, dict):
            continue
        value, user_changed = ensure_pet_defaults(value)
        if user_changed:
            users[key] = value
            changed = True
        rows.append((user_id, value))
    if changed:
        save_users(users)
    rows.sort(key=lambda item: item[0])
    return rows


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    return get_user(user_id)


def admin_update_pet_value(user_id: int, field: str, delta: int) -> tuple[bool, int, int]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, 0
    user, _ = ensure_pet_defaults(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, 0, 0

    target = pet
    key = field
    if "." in field:
        prefix, key = field.split(".", 1)
        nested = pet.get(prefix)
        if not isinstance(nested, dict):
            nested = {}
            pet[prefix] = nested
        target = nested

    current = target.get(key, 0)
    before = current if isinstance(current, int) else 0
    if field == "exp":
        before = int(pet.get("exp", 0)) if isinstance(pet.get("exp"), int) else 0
        add_exp(pet, delta)
        after = int(pet.get("exp", 0)) if isinstance(pet.get("exp"), int) else 0
    elif field == "level":
        before = int(pet.get("level", 1)) if isinstance(pet.get("level"), int) else 1
        pet["level"] = max(1, min(MAX_LEVEL, before + delta))
        if pet["level"] >= MAX_LEVEL:
            pet["exp"] = 0
        pet["legendary"] = pet["level"] >= LEGEND_LEVEL
        after = pet["level"]
    else:
        target[key] = before + delta
        after = target[key]

    for need in DEFAULT_NEEDS:
        pet[need] = clamp_need_by_level(pet, need, int(pet.get(need, DEFAULT_NEEDS[need])))
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, before, after


def admin_add_currency(user_id: int, amount: int) -> tuple[bool, int, int]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, 0
    user, _ = ensure_pet_defaults(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, 0, 0
    before = int(pet.get("currency", 0)) if isinstance(pet.get("currency"), int) else 0
    pet["currency"] = max(0, before + amount)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, before, pet["currency"]


def admin_add_inventory_item(user_id: int, item_key: str, amount: int = 1) -> tuple[bool, int, int]:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False, 0, 0
    user, _ = ensure_pet_defaults(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False, 0, 0
    inventory = pet.get("inventory")
    if not isinstance(inventory, dict):
        pet["inventory"] = DEFAULT_INVENTORY.copy()
        inventory = pet["inventory"]
    before = inventory.get(item_key, 0) if isinstance(inventory.get(item_key), int) else 0
    inventory[item_key] = max(0, before + amount)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True, before, inventory[item_key]


def admin_restore_needs(user_id: int) -> bool:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False
    user, _ = ensure_pet_defaults(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False
    max_needs = get_pet_max_needs(pet)
    for need, max_value in max_needs.items():
        pet[need] = max_value
    update_pet_mood(pet)
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True


def admin_clear_battle(user_id: int) -> bool:
    users = load_users()
    user = users.get(str(user_id))
    if not isinstance(user, dict):
        return False
    user, _ = ensure_pet_defaults(user)
    pet = user.get("pet")
    if not isinstance(pet, dict):
        return False
    if not isinstance(pet.get("battle"), dict):
        return False
    pet["battle"] = None
    pet["updated_at"] = utc_now().isoformat()
    users[str(user_id)] = user
    save_users(users)
    return True
