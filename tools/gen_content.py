#!/usr/bin/env python3
"""Generate the textures, models, block states, item definitions and language entries for Khemet's blocks, items and creatures.

    python3 tools/gen_content.py && python3 tools/gen_assets.py

Everything is derived from this script; edit it, not the output. Stdlib only.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen_assets as ga  # noqa: E402  (write_png)

ROOT = HERE.parent
NS = "khemet"
ASSETS = ROOT / "src/main/resources/assets" / NS

GOLD, GOLD_D, GOLD_L = (236, 190, 60), (176, 130, 30), (255, 232, 140)
LAPIS, LAPIS_D = (38, 67, 155), (24, 44, 110)
TURQ = (40, 170, 160)
RED = (170, 60, 44)
INK = (11, 11, 13)
BROWN_D = (92, 68, 40)


def h(x, y, salt=0):
    return ((x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)) % 100


def shade(c, d):
    return tuple(max(0, min(255, v + d)) for v in c[:3])


class Pix:
    def __init__(self, w=16, hh=16):
        self.w, self.h = w, hh
        self.p = {}

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[(x, y)] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)

    def line(self, x0, y0, x1, y1, c, thick=1):
        n = max(abs(x1 - x0), abs(y1 - y0)) * 2 or 1
        for i in range(n + 1):
            x, y = round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)
            for dx in range(thick):
                for dy in range(thick):
                    self.put(x + dx, y + dy, c)

    def disc(self, cx, cy, r, c):
        for y in range(self.h):
            for x in range(self.w):
                if math.hypot(x - cx, y - cy) <= r:
                    self.put(x, y, c)

    def outline(self, c=INK):
        add = {}
        for (x, y) in self.p:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                k = (x + dx, y + dy)
                if k not in self.p and 0 <= k[0] < self.w and 0 <= k[1] < self.h:
                    add[k] = c
        self.p.update(add)

    def save(self, path):
        px = [(*self.p[(x, y)][:3], 255) if (x, y) in self.p else (0, 0, 0, 0) for y in range(self.h) for x in range(self.w)]
        path.parent.mkdir(parents=True, exist_ok=True)
        ga.write_png(path, self.w, self.h, px)


def tex(fn):
    p = Pix()
    for y in range(16):
        for x in range(16):
            p.put(x, y, fn(x, y))
    return p


# ---------- glyphs: 4 wide by 5 tall ----------
GLYPHS = {
    "ankh": ("#### ", "#..# ", "#### ", ".##. ", "#### "),
    "wave": ("#.#.", ".#.#", "#.#.", ".#.#", "#.#."),
    "eye": (".##.", "#..#", "#.##", ".##.", ".#.."),
    "bird": ("##..", ".###", "..##", ".#..", "#..."),
    "sun": (".##.", "#..#", "#..#", ".##.", "...."),
    "reed": ("..#.", ".#..", "..#.", ".#..", "..#."),
    "scarab": ("#..#", ".##.", "####", ".##.", "#..#"),
}
GLYPH_ORDER = list(GLYPHS)


def glyph(p, gx, gy, name, c):
    for j, row in enumerate(GLYPHS[name]):
        for i, ch in enumerate(row[:4]):
            if ch == "#":
                p.put(gx + i, gy + j, c)


def stone(base, salt, spread=7, seams=True, seam=None):
    def fn(x, y):
        c = shade(base, (h(x, y, salt) % (2 * spread + 1)) - spread)
        if seams and (y % 8 == 0 or (x + (4 if (y // 8) % 2 else 0)) % 8 == 0):
            c = shade(base, -22) if seam is None else seam
        return c
    return fn


def ancient_limestone(x, y):
    return stone((205, 196, 170), 1)(x, y)


def white_limestone(x, y):
    return stone((232, 228, 214), 2, 5)(x, y)


def golden_sandstone(x, y):
    c = shade((224, 184, 92), (h(x, y, 3) % 11) - 5)
    return shade((224, 184, 92), -24) if y % 5 == 0 else c


def black_basalt(x, y):
    c = shade((40, 40, 46), (h(x, y, 4) % 9) - 4)
    return (86, 86, 94) if h(x, y, 5) < 4 else c


def polished_pharaoh_stone(x, y):
    c = shade((190, 174, 134), (h(x, y, 6) % 5) - 2)
    return shade((190, 174, 134), -26) if x in (0, 15) or y in (0, 15) else c


def hieroglyph_stone(x, y):
    p = _glyph_tile((205, 196, 170), 7)
    return p[(x, y)]


def _glyph_tile(base, salt, order=0):
    p = Pix()
    for y in range(16):
        for x in range(16):
            p.put(x, y, shade(base, (h(x, y, salt) % 9) - 4))
    for row, gy in enumerate((1, 9)):
        for col, gx in enumerate((1, 6, 11)):
            glyph(p, gx, gy, GLYPH_ORDER[(row * 3 + col + order) % len(GLYPH_ORDER)], BROWN_D)
    return p.p


def cracked_temple_stone(x, y):
    c = stone((200, 190, 160), 8)(x, y)
    crack = {(3, 0), (3, 1), (4, 2), (5, 3), (5, 4), (6, 5), (7, 6), (7, 7), (8, 8), (9, 9), (9, 10), (10, 11), (11, 12), (11, 13), (12, 14), (12, 15)}
    return shade(c, -55) if (x, y) in crack else c


def weathered_pyramid_stone(x, y):
    c = stone((196, 184, 148), 9, 9)(x, y)
    return shade(c, -20) if h(x // 2, y // 2, 10) < 30 else c


def gold_inlaid_tile(x, y):
    c = shade((190, 174, 134), (h(x, y, 11) % 5) - 2)
    if x in (7, 8) or y in (7, 8):
        c = GOLD if (x + y) % 2 == 0 else GOLD_L
    if x in (0, 15) or y in (0, 15):
        c = shade((190, 174, 134), -28)
    return c


def painted_temple_wall(x, y):
    c = shade((222, 214, 188), (h(x, y, 12) % 5) - 2)
    if y in (2, 13):
        c = GOLD
    elif y in (3, 4, 11, 12):
        c = LAPIS if (x // 2) % 2 == 0 else TURQ
    elif y in (6, 7, 8, 9) and x % 4 in (1, 2):
        c = RED
    return c


def hieroglyph_bricks(x, y):
    p = _glyph_tile((214, 204, 176), 13, 3)
    c = p[(x, y)]
    if y % 8 == 0 or (x + (4 if (y // 8) % 2 else 0)) % 8 == 0:
        c = shade((214, 204, 176), -30)
    return c


def obelisk_block(x, y):
    c = shade((180, 168, 140), (h(x, y, 14) % 7) - 3)
    if x in (4, 5, 10, 11) and 1 <= y <= 14 and h(x, y // 3, 15) < 70:
        c = BROWN_D
    if y in (0, 15):
        c = GOLD_D
    return c


def golden_pillar_side(x, y):
    c = shade((224, 184, 92), -8 if x % 4 == 0 else (6 if x % 4 == 2 else 0))
    if y in (0, 1, 14, 15):
        c = GOLD
    elif y in (7, 8):
        c = GOLD_L if x % 2 == 0 else GOLD
    return c


def golden_pillar_top(x, y):
    d = math.hypot(x - 7.5, y - 7.5)
    return GOLD if d <= 7.2 and d > 5.2 else (GOLD_D if d <= 5.2 else shade((190, 160, 70), -10))


def lotus_column_side(x, y):
    c = shade((232, 228, 214), -6 if x % 4 == 0 else 0)
    if y <= 4:
        if abs(x - 7.5) <= (4 - y) * 1.6 + 1.4 and x % 4 != 0:
            c = TURQ if y % 2 else (60, 200, 190)
    if y in (14, 15):
        c = GOLD
    if y == 6:
        c = LAPIS
    return c


def lotus_column_top(x, y):
    d = math.hypot(x - 7.5, y - 7.5)
    ang = math.atan2(y - 7.5, x - 7.5)
    if d <= 7.2:
        return TURQ if int((ang + math.pi) / (math.pi / 4)) % 2 == 0 and d > 2 else (60, 200, 190) if d > 2 else GOLD
    return (200, 196, 180)


def brazier_side(x, y):
    c = shade((40, 40, 46), (h(x, y, 16) % 7) - 3)
    if y <= 2 or y >= 13:
        c = GOLD
    elif y in (7, 8):
        c = GOLD_D
    return c


def brazier_top(x, y):
    d = math.hypot(x - 7.5, y - 7.5)
    if d <= 5.5:
        n = h(x, y, 17)
        return (255, 140, 20) if n < 40 else ((255, 200, 60) if n < 75 else (255, 90, 20))
    return GOLD if d <= 7.2 else (40, 40, 46)


def altar_side(hue, dark):
    def fn(x, y):
        c = shade(dark, (h(x, y, 18) % 7) - 3)
        if x in (0, 15) or y in (0, 15):
            c = shade(dark, -22)
        if y in (5, 6, 9, 10) and 1 <= x <= 14:
            c = hue if y in (6, 9) else shade(hue, -50)
        return c
    return fn


def altar_top(hue, dark, kind):
    def fn(x, y):
        c = shade(dark, (h(x, y, 19) % 5) - 2)
        d = math.hypot(x - 7.5, y - 7.5)
        if kind == "ra":
            if 5.2 <= d <= 6.6:
                c = shade(hue, -30)
            if d <= 4.2:
                c = GOLD_L if d <= 1.6 else hue
        else:
            if abs(x - 7.5) + abs(y - 7.5) <= 6 and abs(x - 7.5) + abs(y - 7.5) >= 4.5:
                c = shade(hue, -30)
            if (x in (7, 8) and 3 <= y <= 12) or (y == 6 and 5 <= x <= 10) or (y in (6,) and x in (4, 11)):
                c = hue
        if x in (0, 15) or y in (0, 15):
            c = shade(dark, -22)
        return c
    return fn


def blue_lotus():
    p = Pix()
    for y in range(9, 16):
        p.put(7, y, (60, 120, 50)); p.put(8, y, (60, 120, 50))
    for x0, y0 in ((2, 12), (12, 12)):
        for dx in range(3):
            p.put(x0 + dx, y0 + (dx % 2), (70, 150, 60))
    petals = [(7, 4), (8, 4), (6, 5), (9, 5), (5, 6), (10, 6), (7, 6), (8, 6), (6, 7), (9, 7), (7, 8), (8, 8), (4, 7), (11, 7), (7, 3), (8, 3)]
    for x, y in petals:
        p.put(x, y, (80, 130, 245) if (x + y) % 2 == 0 else (120, 170, 255))
    p.put(7, 5, GOLD); p.put(8, 5, GOLD)
    return p


def papyrus():
    p = Pix()
    for x0 in (4, 8, 11):
        top = 3 + (x0 % 3)
        for y in range(top, 16):
            p.put(x0, y, (96, 150, 60) if y % 3 else (130, 180, 80))
        for dx, dy in ((-2, 0), (-1, -1), (0, -1), (1, -1), (2, 0), (-1, 0), (1, 0), (0, -2)):
            p.put(x0 + dx, top + dy + 1, (110, 165, 70))
    return p


# ---------- items ----------

def ankh():
    p = Pix()
    p.disc(7.5, 4.5, 3.6, GOLD)
    p.disc(7.5, 4.5, 1.8, (0, 0, 0, 0))
    for (x, y), c in list(p.p.items()):
        if c == (0, 0, 0, 0):
            del p.p[(x, y)]
    p.rect(7, 8, 8, 14, GOLD)
    p.rect(3, 9, 12, 10, GOLD)
    p.put(7, 3, GOLD_L); p.put(6, 4, GOLD_L); p.rect(7, 9, 7, 13, GOLD_L)
    p.outline()
    return p


def khopesh():
    p = Pix()
    p.line(2, 14, 4, 12, BROWN_D, 2)                    # grip
    p.rect(3, 11, 6, 12, GOLD)                          # guard
    blade = [(6, 10), (7, 9), (8, 8), (9, 6), (10, 4), (11, 3), (12, 2), (13, 2), (14, 3), (14, 4), (13, 5), (12, 4), (11, 5), (10, 7), (9, 9), (8, 10), (7, 11)]
    for i, (x, y) in enumerate(blade):
        p.put(x, y, (210, 215, 222) if i % 2 == 0 else (160, 168, 180))
    p.outline()
    return p


EGGS = {}   # spawn eggs belong to `shadw-mod mob gen` (mobs/*.json)

LANG = {
    "item.khemet.ankh": "Ankh of Life",
    "item.khemet.ankh.lore": "The key of life. Use it to heal at once; it wears out, and needs time between uses.",
    "item.khemet.khopesh": "Anubis's Khopesh",
    "item.khemet.khopesh.lore": "A curved sword of the dead's guide. It cuts the undead deeper.",
    "block.khemet.ancient_limestone": "Ancient Limestone", "block.khemet.white_limestone": "White Egyptian Limestone",
    "block.khemet.golden_sandstone": "Golden Sandstone", "block.khemet.black_basalt": "Black Basalt",
    "block.khemet.polished_pharaoh_stone": "Polished Pharaoh Stone", "block.khemet.hieroglyph_stone": "Carved Hieroglyphic Stone",
    "block.khemet.cracked_temple_stone": "Cracked Temple Stone", "block.khemet.weathered_pyramid_stone": "Weathered Pyramid Stone",
    "block.khemet.gold_inlaid_tile": "Gold-Inlaid Tile", "block.khemet.painted_temple_wall": "Painted Temple Wall",
    "block.khemet.hieroglyph_bricks": "Hieroglyphic Bricks", "block.khemet.obelisk_block": "Obelisk Block",
    "block.khemet.golden_pillar": "Golden Pillar", "block.khemet.lotus_column": "Lotus Column",
    "block.khemet.sacred_brazier": "Sacred Brazier", "block.khemet.blue_lotus": "Blue Lotus", "block.khemet.papyrus": "Papyrus",
    "block.khemet.ra_altar": "Altar of Ra", "block.khemet.anubis_altar": "Altar of Anubis",
    "entity.khemet.mummy": "Mummy", "entity.khemet.royal_mummy": "Royal Mummy",
    "item.khemet.mummy_spawn_egg": "Mummy Spawn Egg", "item.khemet.royal_mummy_spawn_egg": "Royal Mummy Spawn Egg",
}

STONE_FNS = {"ancient_limestone": ancient_limestone, "white_limestone": white_limestone, "golden_sandstone": golden_sandstone,
             "black_basalt": black_basalt, "polished_pharaoh_stone": polished_pharaoh_stone, "hieroglyph_stone": hieroglyph_stone,
             "cracked_temple_stone": cracked_temple_stone, "weathered_pyramid_stone": weathered_pyramid_stone,
             "gold_inlaid_tile": gold_inlaid_tile, "painted_temple_wall": painted_temple_wall, "hieroglyph_bricks": hieroglyph_bricks,
             "obelisk_block": obelisk_block}


def wj(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def item_def(name, model):
    wj(ASSETS / "items" / f"{name}.json", {"model": {"type": "minecraft:model", "model": model}})


# ---------- mummy skins (zombie model, 64 by 64) ----------

class Skin:
    def __init__(self):
        self.px = {}

    def fill(self, x0, y0, x1, y1, c, noise=0, salt=1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                d = ((h(x, y, salt) % (2 * noise + 1)) - noise) if noise else 0
                self.px[(x, y)] = shade(c, d)

    def put(self, x, y, c):
        self.px[(x, y)] = c

    def save(self, path):
        pix = [(*self.px[(x, y)], 255) if (x, y) in self.px else (0, 0, 0, 0) for y in range(64) for x in range(64)]
        path.parent.mkdir(parents=True, exist_ok=True)
        ga.write_png(path, 64, 64, pix)


HEAD = dict(top=(8, 0, 15, 7), bottom=(16, 0, 23, 7), right=(0, 8, 7, 15), front=(8, 8, 15, 15), left=(16, 8, 23, 15), back=(24, 8, 31, 15))
BODY = dict(top=(20, 16, 27, 19), bottom=(28, 16, 35, 19), right=(16, 20, 19, 31), front=(20, 20, 27, 31), left=(28, 20, 31, 31), back=(32, 20, 39, 31))
RARM = dict(top=(44, 16, 47, 19), bottom=(48, 16, 51, 19), right=(40, 20, 43, 31), front=(44, 20, 47, 31), left=(48, 20, 51, 31), back=(52, 20, 55, 31))
LARM = dict(top=(36, 48, 39, 51), bottom=(40, 48, 43, 51), right=(32, 52, 35, 63), front=(36, 52, 39, 63), left=(40, 52, 43, 63), back=(44, 52, 47, 63))
RLEG = dict(top=(4, 16, 7, 19), bottom=(8, 16, 11, 19), right=(0, 20, 3, 31), front=(4, 20, 7, 31), left=(8, 20, 11, 31), back=(12, 20, 15, 31))
LLEG = dict(top=(20, 48, 23, 51), bottom=(24, 48, 27, 51), right=(16, 52, 19, 63), front=(20, 52, 23, 63), left=(24, 52, 27, 63), back=(28, 52, 31, 63))
SIDES = ("right", "front", "left", "back")


def mummy(royal):
    s = Skin()
    wrap, shadow, skin = (212, 202, 168), (160, 148, 112), (110, 84, 58)
    parts = [HEAD, BODY, RARM, LARM, RLEG, LLEG]
    for part in parts:
        for name, (x0, y0, x1, y1) in part.items():
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    c = wrap if (y + (x // 3)) % 3 else shadow          # slanting bands of linen
                    c = shade(c, (h(x, y, 40) % 9) - 4)
                    if h(x, y, 41) < 4:
                        c = skin                                       # a gap in the wrappings
                    s.put(x, y, c)
    fx0, fy0, fx1, fy1 = HEAD["front"]
    for ex in (fx0 + 1, fx0 + 5):                                      # glowing eyes in the gap
        s.fill(ex, fy0 + 3, ex + 1, fy0 + 4, (30, 20, 14))
        s.put(ex, fy0 + 3, (255, 200, 60)); s.put(ex + 1, fy0 + 3, (255, 200, 60))
    for name in ("front", "left", "right", "back"):                    # trailing loose wraps at the hips
        x0, y0, x1, y1 = RLEG[name] if name != "front" else RLEG["front"]
    if royal:
        for f in ("top",):
            x0, y0, x1, y1 = HEAD[f]
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    s.put(x, y, GOLD if (x - x0) % 2 == 0 else LAPIS)
        for f in SIDES:                                                # the striped headdress
            x0, y0, x1, y1 = HEAD[f]
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    if y <= y0 + 3 or f in ("left", "right"):
                        s.put(x, y, GOLD if (x + y) % 3 else LAPIS)
        s.fill(fx0 + 1, fy0 + 1, fx0 + 6, fy0 + 1, GOLD)               # gold brow band
        for x in range(fx0 + 1, fx0 + 7):
            s.put(x, fy0 + 6, GOLD)                                    # a false beard line
        x0, y0, x1, y1 = BODY["front"]
        for y in range(y0, y0 + 3):                                    # the broad collar
            for x in range(x0, x1 + 1):
                s.put(x, y, GOLD if (x + y) % 2 == 0 else TURQ)
        for arm in (RARM, LARM):
            for name in SIDES:
                x0, y0, x1, y1 = arm[name]
                for x in range(x0, x1 + 1):
                    s.put(x, y1 - 3, GOLD); s.put(x, y1 - 2, GOLD_D)
    return s


def main():
    for name, fn in STONE_FNS.items():
        tex(fn).save(ASSETS / f"textures/block/{name}.png")
        wj(ASSETS / f"models/block/{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{name}"}})
        wj(ASSETS / f"blockstates/{name}.json", {"variants": {"": {"model": f"{NS}:block/{name}"}}})
        item_def(name, f"{NS}:block/{name}")
    for name, side, top in (("golden_pillar", golden_pillar_side, golden_pillar_top), ("lotus_column", lotus_column_side, lotus_column_top)):
        tex(side).save(ASSETS / f"textures/block/{name}.png")
        tex(top).save(ASSETS / f"textures/block/{name}_top.png")
        tx = {"end": f"{NS}:block/{name}_top", "side": f"{NS}:block/{name}"}
        wj(ASSETS / f"models/block/{name}.json", {"parent": "minecraft:block/cube_column", "textures": tx})
        wj(ASSETS / f"models/block/{name}_horizontal.json", {"parent": "minecraft:block/cube_column_horizontal", "textures": tx})
        wj(ASSETS / f"blockstates/{name}.json", {"variants": {"axis=y": {"model": f"{NS}:block/{name}"},
            "axis=x": {"model": f"{NS}:block/{name}_horizontal", "x": 90, "y": 90}, "axis=z": {"model": f"{NS}:block/{name}_horizontal", "x": 90}}})
        item_def(name, f"{NS}:block/{name}")
    tex(brazier_side).save(ASSETS / "textures/block/sacred_brazier_side.png")
    tex(brazier_top).save(ASSETS / "textures/block/sacred_brazier_top.png")
    wj(ASSETS / "models/block/sacred_brazier.json", {"parent": "minecraft:block/cube_bottom_top", "textures": {
        "top": f"{NS}:block/sacred_brazier_top", "bottom": f"{NS}:block/sacred_brazier_side", "side": f"{NS}:block/sacred_brazier_side"}})
    wj(ASSETS / "blockstates/sacred_brazier.json", {"variants": {"": {"model": f"{NS}:block/sacred_brazier"}}})
    item_def("sacred_brazier", f"{NS}:block/sacred_brazier")
    for god, hue, dark in (("ra", GOLD, (190, 150, 60)), ("anubis", GOLD, (40, 40, 46))):
        tex(altar_side(hue, dark)).save(ASSETS / f"textures/block/{god}_altar_side.png")
        tex(altar_top(GOLD_L if god == "ra" else GOLD, dark, god)).save(ASSETS / f"textures/block/{god}_altar_top.png")
        wj(ASSETS / f"models/block/{god}_altar.json", {"parent": "minecraft:block/cube_bottom_top", "textures": {
            "top": f"{NS}:block/{god}_altar_top", "bottom": f"{NS}:block/{god}_altar_side", "side": f"{NS}:block/{god}_altar_side"}})
        wj(ASSETS / f"blockstates/{god}_altar.json", {"variants": {"": {"model": f"{NS}:block/{god}_altar"}}})
        item_def(f"{god}_altar", f"{NS}:block/{god}_altar")
    for name, art in (("blue_lotus", blue_lotus()), ("papyrus", papyrus())):
        art.save(ASSETS / f"textures/block/{name}.png")
        wj(ASSETS / f"models/block/{name}.json", {"parent": "minecraft:block/cross", "textures": {"cross": f"{NS}:block/{name}"}})
        wj(ASSETS / f"blockstates/{name}.json", {"variants": {"": {"model": f"{NS}:block/{name}"}}})
        wj(ASSETS / f"models/item/{name}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:block/{name}"}})
        item_def(name, f"{NS}:item/{name}")
    for name, art, parent in (("ankh", ankh(), "minecraft:item/handheld"), ("khopesh", khopesh(), "minecraft:item/handheld")):
        art.save(ASSETS / f"textures/item/{name}.png")
        wj(ASSETS / f"models/item/{name}.json", {"parent": parent, "textures": {"layer0": f"{NS}:item/{name}"}})
        item_def(name, f"{NS}:item/{name}")
    for name, (a, b) in EGGS.items():
        tint = lambda c: c[0] * 65536 + c[1] * 256 + c[2]
        wj(ASSETS / f"models/item/{name}_spawn_egg.json", {"parent": "minecraft:item/template_spawn_egg"})
        wj(ASSETS / f"items/{name}_spawn_egg.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/{name}_spawn_egg",
            "tints": [{"type": "minecraft:constant", "value": tint(a)}, {"type": "minecraft:constant", "value": tint(b)}]}})
    # creature textures belong to `shadw-mod mob gen` (mobs/*.json)
    wj(HERE / "content_lang.json", LANG)
    print("content assets written")


if __name__ == "__main__":
    main()
