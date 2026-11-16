#!/usr/bin/env python3
"""The chariot's item definition, model, sprite and crafting recipe.

    python3 tools/gen_vehicles.py

The entity's model, texture, loot and language come from mobs/chariot.json (tools/gen_models.py + `shadw-mod mob gen`); this writes the item.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from shadwlib.png import write_png  # noqa: E402

ASSETS = ROOT / "src/main/resources/assets/khemet"
DATA = ROOT / "src/main/resources/data/khemet"


def wj(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sprite():
    """A 16 by 16 chariot seen from the side: a gilded wheel, a lapis guard with a gold rim, a pole to a horse's head."""
    px = {}
    gold, gold_d, gold_l, wood, wood_d, lap, lap_d, red, horse, horse_d = ((224, 184, 56), (138, 106, 20), (255, 240, 160), (138, 106, 58), (74, 52, 24), (42, 88, 176), (20, 44, 104), (208, 58, 24), (138, 90, 52), (74, 44, 20))
    for y in range(16):
        for x in range(16):
            px[(x, y)] = (0, 0, 0, 0)
    def put(x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            px[(x, y)] = (*c, 255)
    for x in range(5, 15):                                   # the carriage: a lapis guard over a wooden floor
        for y in range(4, 10):
            put(x, y, lap if (x + y) % 5 else lap_d)
        put(x, 3, gold); put(x, 10, wood); put(x, 11, wood_d)
    for y in range(3, 11):
        put(5, y, gold_d)
    put(10, 6, red); put(11, 6, red); put(10, 7, red); put(11, 7, red)   # the sun disc
    cx, cy, r = 8, 11, 4                                     # the wheel
    for a in range(0, 360, 12):
        put(round(cx + r * math.cos(math.radians(a))), round(cy + r * math.sin(math.radians(a))), gold if (a // 12) % 2 else gold_l)
    for d in range(-3, 4):
        put(cx + d, cy, wood); put(cx, cy + d, wood)
    put(cx, cy, gold_d)
    for x in range(0, 6):                                    # the pole and a horse's head
        put(x, 8, wood)
    for x, y in ((0, 5), (1, 5), (2, 5), (0, 6), (1, 6), (2, 6), (2, 4), (1, 7)):
        put(x, y, horse if (x + y) % 3 else horse_d)
    out = [px[(x, y)] for y in range(16) for x in range(16)]
    write_png(ASSETS / "textures/item/chariot.png", 16, 16, out)


def main():
    sprite()
    wj(ASSETS / "items/chariot.json", {"model": {"type": "minecraft:model", "model": "khemet:item/chariot"}})
    wj(ASSETS / "models/item/chariot.json", {"parent": "minecraft:item/generated", "textures": {"layer0": "khemet:item/chariot"}})
    wj(DATA / "recipe/chariot.json", {
        "type": "minecraft:crafting_shaped", "category": "misc",
        "pattern": [" L ", "PGP", "SPS"],
        "key": {"L": "minecraft:leather", "P": "minecraft:acacia_planks", "G": "minecraft:gold_ingot", "S": "minecraft:stick"},
        "result": {"id": "khemet:chariot", "count": 1}})
    print("chariot item, sprite and recipe written")


if __name__ == "__main__":
    main()
