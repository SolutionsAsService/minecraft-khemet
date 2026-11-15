#!/usr/bin/env python3
"""Generate Khemet's structures as Minecraft structure files (data/khemet/structure/*.nbt).

    python3 tools/gen_structures.py

The shrines of Ra and Anubis, an obelisk field and a desert ruin. Everything is deterministic: the same run writes
the same bytes. The structures are placed in the world by the worldgen data (structure, structure set, template pool,
biome tags) in src/main/resources/data/asgard/. Stdlib only.
"""

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nbt  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "src/main/resources/data/khemet/structure"
DATA_VERSION = 4189  # Minecraft 1.21.4

AIR = ("minecraft:air", ())


def state(name, **props):
    return (name, tuple(sorted(props.items())))


class Structure:
    def __init__(self, sx, sy, sz):
        self.size = (sx, sy, sz)
        self.blocks = {}
        self.nbt = {}

    def put(self, x, y, z, block, tag=None):
        sx, sy, sz = self.size
        if 0 <= x < sx and 0 <= y < sy and 0 <= z < sz:
            self.blocks[(x, y, z)] = block
            if tag:
                self.nbt[(x, y, z)] = tag

    def fill(self, x0, y0, z0, x1, y1, z1, block):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                for x in range(x0, x1 + 1):
                    self.put(x, y, z, block)

    def remove(self, x, y, z):
        self.blocks.pop((x, y, z), None)

    def dumps(self):
        palette, index = [], {}
        for blk in self.blocks.values():
            if blk not in index:
                index[blk] = len(palette)
                palette.append(blk)
        pal = []
        for name, props in palette:
            c = {"Name": (nbt.STRING, name)}
            if props:
                c["Properties"] = (nbt.COMPOUND, {k: (nbt.STRING, v) for k, v in props})
            pal.append(c)
        blocks = []
        for (x, y, z), blk in sorted(self.blocks.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
            c = {"pos": (nbt.LIST, (nbt.INT, [x, y, z])), "state": (nbt.INT, index[blk])}
            tag = self.nbt.get((x, y, z))
            if tag:
                c["nbt"] = (nbt.COMPOUND, {k: (nbt.STRING, v) for k, v in tag.items()})
            blocks.append(c)
        root = {
            "DataVersion": (nbt.INT, DATA_VERSION),
            "size": (nbt.LIST, (nbt.INT, list(self.size))),
            "palette": (nbt.LIST, (nbt.COMPOUND, pal)),
            "blocks": (nbt.LIST, (nbt.COMPOUND, blocks)),
            "entities": (nbt.LIST, (nbt.COMPOUND, [])),
        }
        return nbt.dumps(root)




def chest(facing, loot):
    return state("minecraft:chest", facing=facing, type="single", waterlogged="false"), {
        "id": "minecraft:chest", "LootTable": loot}


def hole(x, y, z):
    """Deterministic scatter in [0, 100)."""
    return ((x * 73856093) ^ (y * 19349663) ^ (z * 83492791)) % 100


K = lambda name, **props: state(f"khemet:{name}", **props)
ALTAR_RA, ALTAR_ANUBIS = K("ra_altar"), K("anubis_altar")
SAND = state("minecraft:sand")
SANDSTONE = state("minecraft:sandstone")
GOLDBLK = state("minecraft:gold_block")
BRAZIER = K("sacred_brazier")


def pillar(axis="y", name="golden_pillar"):
    return K(name, axis=axis)


def weather(seed, x, y, z, fresh="ancient_limestone"):
    """Limestone that has stood a few thousand years: some cracked, some weathered."""
    r = hole(x + seed * 5, y, z)
    if r < 12:
        return K("cracked_temple_stone")
    if r < 26:
        return K("weathered_pyramid_stone")
    return K(fresh)


# ---------- the shrine of Ra: a golden obelisk and a sun disc ----------

def ra_shrine(seed):
    rnd = random.Random(seed * 7919 + 101)
    N, c = 21, 10
    s = Structure(N, 26, N)
    for z in range(N):
        for x in range(N):
            dx, dz = abs(x - c), abs(z - c)
            m = max(dx, dz)
            s.put(x, 0, z, weather(seed, x, 0, z))
            if m <= 8:
                s.put(x, 1, z, K("golden_sandstone") if m == 8 else K("white_limestone"))
            if m <= 6:
                s.put(x, 2, z, K("gold_inlaid_tile") if m == 6 or (dx == 0 or dz == 0) else K("polished_pharaoh_stone"))
    for y in range(3, 21):                                              # the obelisk, tapering as it rises
        r = 1 if y < 7 else 0
        for dz in range(-r, r + 1):
            for dx in range(-r, r + 1):
                block = GOLDBLK if y in (8, 13, 18) else K("obelisk_block")
                s.put(c + dx, y, c - 2 + dz, block)
    s.put(c, 21, c - 2, GOLDBLK); s.put(c, 22, c - 2, state("minecraft:light", level="15", waterlogged="false"))
    for yy in range(-4, 5):                                             # the sun disc behind it
        for xx in range(-4, 5):
            d = math.hypot(xx, yy)
            if 3.2 <= d <= 4.4:
                s.put(c + xx, 14 + yy, c - 4, GOLDBLK)
            elif d < 3.2:
                s.put(c + xx, 14 + yy, c - 4, state("minecraft:orange_stained_glass") if d > 1.6 else state("minecraft:glowstone"))
    for px, pz in ((c - 6, c - 6), (c + 6, c - 6), (c - 6, c + 6), (c + 6, c + 6)):   # four golden pillars
        for y in range(3, 10):
            s.put(px, y, pz, pillar("y"))
        s.put(px, 10, pz, K("polished_pharaoh_stone"))
        s.put(px, 11, pz, BRAZIER)
    for bx, bz in ((c - 4, c + 1), (c + 4, c + 1)):
        s.put(bx, 3, bz, BRAZIER)
    s.put(c, 3, c + 4, ALTAR_RA)
    blk, tag = chest("south", "khemet:chests/ra_shrine")
    s.put(c + 2, 3, c + 4, blk, tag)
    for k in range(6):                                                  # drifted sand
        s.put(rnd.randint(2, 18), 1, rnd.randint(2, 18), SAND) if (c, 1, c) != (0, 0, 0) else None
    return s


# ---------- the shrine of Anubis: black basalt, jackals and canopic jars ----------

JARS = ("minecraft:brown_terracotta", "minecraft:terracotta", "minecraft:orange_terracotta", "minecraft:yellow_terracotta")


def anubis_shrine(seed):
    rnd = random.Random(seed * 6271 + 29)
    N, c = 19, 9
    s = Structure(N, 14, N)
    for z in range(N):
        for x in range(N):
            m = max(abs(x - c), abs(z - c))
            if m <= 9:
                s.put(x, 0, z, K("black_basalt"))
            if m <= 7:
                s.put(x, 1, z, K("polished_pharaoh_stone") if m == 7 else K("black_basalt"))
            if m == 7 and (x + z) % 2 == 0:
                s.put(x, 1, z, GOLDBLK)
    for i in range(-5, 6):
        s.put(c + i, 1, c, K("gold_inlaid_tile")); s.put(c, 1, c + i, K("gold_inlaid_tile"))

    def jackal(jx, jz, face):
        s.put(jx, 2, jz, K("black_basalt")); s.put(jx, 3, jz, K("black_basalt")); s.put(jx, 4, jz, K("black_basalt"))
        s.put(jx, 3, jz + face, state("minecraft:polished_blackstone_slab", type="bottom", waterlogged="false"))   # snout
        s.put(jx, 4, jz + face, state("minecraft:polished_blackstone_slab", type="bottom", waterlogged="false"))
        s.put(jx, 5, jz, state("minecraft:polished_blackstone_wall", east="none", north="none", south="none", west="none", up="true", waterlogged="false"))   # ears
        s.put(jx, 3, jz - face, K("black_basalt")); s.put(jx, 2, jz + face, K("polished_pharaoh_stone"))
        s.put(jx, 3, jz, GOLDBLK)                                       # the gold collar
    jackal(c - 4, c + 3, 1); jackal(c + 4, c + 3, 1)
    for k, (jx, jz) in enumerate(((c - 6, c - 5), (c + 6, c - 5), (c - 6, c - 1), (c + 6, c - 1))):   # canopic jars
        s.put(jx, 2, jz, state(JARS[(k + seed) % 4])); s.put(jx, 3, jz, state(JARS[(k + seed) % 4]))
        s.put(jx, 4, jz, state("minecraft:smooth_stone_slab", type="bottom", waterlogged="false"))
    for sx in range(c - 2, c + 3):                                      # a sarcophagus
        s.put(sx, 2, c - 5, state("minecraft:polished_blackstone_slab", type="bottom", waterlogged="false"))
        s.put(sx, 2, c - 4, state("minecraft:polished_blackstone_slab", type="bottom", waterlogged="false"))
    s.put(c - 2, 2, c - 5, GOLDBLK); s.put(c + 2, 2, c - 5, GOLDBLK)
    for bx, bz in ((c - 7, c + 7), (c + 7, c + 7), (c - 7, c - 7), (c + 7, c - 7)):
        s.put(bx, 2, bz, state("minecraft:soul_campfire", facing="north", lit="true", signal_fire="false", waterlogged="false"))
        for y in (3, 4):
            s.put(bx, y, bz, state("minecraft:polished_blackstone_wall", east="none", north="none", south="none", west="none", up="true", waterlogged="false"))
    s.put(c, 2, c + 5, ALTAR_ANUBIS)
    blk, tag = chest("north", "khemet:chests/anubis_shrine")
    s.put(c + 2, 2, c + 5, blk, tag)
    return s


# ---------- the obelisk field ----------

def obelisk_field(seed):
    rnd = random.Random(seed * 3571 + 7)
    N, c = 25, 12
    s = Structure(N, 18, N)
    for z in range(N):
        for x in range(N):
            d = math.hypot(x - c, z - c)
            if d <= 12:
                s.put(x, 0, z, weather(seed, x, 0, z, "polished_pharaoh_stone") if hole(x, 1, z) < 55 else SAND)
    spots = [(c, c)] + [(c + round(math.cos(k * 1.26 + seed) * 8), c + round(math.sin(k * 1.26 + seed) * 8)) for k in range(4)]
    for k, (ox, oz) in enumerate(spots):
        height = rnd.randint(11, 16) if k else 16
        for dz in (-1, 0, 1):
            for dx in (-1, 0, 1):
                s.put(ox + dx, 1, oz + dz, K("polished_pharaoh_stone")); s.put(ox + dx, 2, oz + dz, K("white_limestone"))
        for y in range(3, height):
            s.put(ox, y, oz, GOLDBLK if (y - 3) % 5 == 4 else K("obelisk_block"))
        s.put(ox, height, oz, GOLDBLK)
        s.put(ox, height + 1, oz, state("minecraft:light", level="12", waterlogged="false"))
    blk, tag = chest("south", "khemet:chests/obelisk_field")
    s.put(c + 2, 1, c + 2, blk, tag)
    for _ in range(14):
        s.put(rnd.randint(1, 23), 1, rnd.randint(1, 23), SAND) if not any(abs(x - ox) <= 1 and abs(z - oz) <= 1 for ox, oz in spots for x, z in [(0, 0)]) else None
    return s


# ---------- the desert ruin ----------

def desert_ruin(seed):
    rnd = random.Random(seed * 9109 + 5)
    N, c = 15, 7
    s = Structure(N, 10, N)
    for z in range(N):
        for x in range(N):
            if max(abs(x - c), abs(z - c)) <= 6:
                s.put(x, 0, z, weather(seed, x, 0, z, "polished_pharaoh_stone"))
    for z in range(N):
        for x in range(N):
            m = max(abs(x - c), abs(z - c))
            if m == 6:
                top = rnd.randint(1, 5)
                for y in range(1, top + 1):
                    if not (z == c + 6 and abs(x - c) <= 1):             # a doorway to the south
                        s.put(x, y, z, weather(seed, x, y, z))
    for px, pz in ((c - 3, c - 3), (c + 3, c - 3), (c - 3, c + 3), (c + 3, c + 3)):
        full = rnd.random() < 0.45
        for y in range(1, (7 if full else rnd.randint(2, 4)) + 1):
            s.put(px, y, pz, pillar("y", "lotus_column" if (px + pz) % 2 == 0 else "golden_pillar"))
        if not full:
            s.put(px + rnd.choice((-1, 1)), 1, pz, K("cracked_temple_stone"))
    s.put(c, 1, c - 4, K("painted_temple_wall")); s.put(c - 1, 1, c - 4, K("hieroglyph_stone")); s.put(c + 1, 1, c - 4, K("hieroglyph_stone"))
    s.put(c, 2, c - 4, K("hieroglyph_bricks"))
    blk, tag = chest("south", "khemet:chests/desert_ruin")
    s.put(c, 1, c - 2, blk, tag)
    s.put(c - 2, 1, c + 1, BRAZIER) if seed % 2 == 0 else s.put(c + 2, 1, c + 1, state("minecraft:suspicious_sand"))
    for _ in range(36):
        sx, sz = rnd.randint(1, 13), rnd.randint(1, 13)
        if (sx, 1, sz) not in s.blocks:
            s.put(sx, 1, sz, SAND)
    return s


STRUCTURES = {"ra_shrine": (ra_shrine, 2), "anubis_shrine": (anubis_shrine, 2), "obelisk_field": (obelisk_field, 2), "desert_ruin": (desert_ruin, 3)}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.nbt"):
        old.unlink()
    for name, (fn, n) in STRUCTURES.items():
        for i in range(n):
            st = fn(i)
            data = st.dumps()
            (OUT / f"{name}_{i}.nbt").write_bytes(data)
            back = nbt.loads(data)
            assert len(back["blocks"][1][1]) == len(st.blocks), name
            print(f"{name}_{i}: size {st.size}, {len(st.blocks)} blocks, {len(back['palette'][1][1])} states, {len(data)} bytes")
