#!/usr/bin/env python3
"""Author Khemet's creature models (the "model" section of each mobs/<id>.json): Mummy, Royal Mummy, Scarab, Tomb Guardian, Forgotten Pharaoh.

    python3 tools/gen_models.py && shadw-mod mob . gen

Edit this script, not the JSON. Uses shadwlib.figure on the model system in shadw-modding's adapters/minecraft-fabric/mobmodel.py.
Coordinates are Minecraft model pixels: +y down, -z forward, root at the feet.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from shadwlib.figure import Rig, box, rect  # noqa: E402

LINEN = {"type": "cloth", "base": "#d4caa8", "trim": "#a89870"}
PAINTS = {
    "linen": LINEN, "linen_dark": {"type": "cloth", "base": "#b8aa84", "trim": "#8a7c58"}, "dry": {"type": "skin", "base": "#7a5c40", "shade": 6},
    "gold": {"type": "metal", "base": "#e0b838", "dark": "#8a6a14", "light": "#fff0a0"}, "lapis": {"type": "metal", "base": "#2a58b0", "dark": "#142c68", "light": "#6a98e8"},
    "turq": {"type": "metal", "base": "#2ab0a0", "dark": "#126058", "light": "#7ae8d8"}, "nemes": {"type": "cloth", "base": "#e0b838", "trim": "#2a58b0"},
    "stone": {"type": "ridged", "base": "#b8aa84", "dark": "#80724c", "light": "#d8ccaa"}, "basalt": {"type": "skin", "base": "#24242c", "shade": 4}, "black_gold": {"type": "scales", "base": "#2a2a32", "dark": "#101014", "light": "#4a4a56", "cell": 4},
    "white_crown": {"type": "cloth", "base": "#f0ece0", "trim": "#c8c0a8"}, "red_crown": {"type": "cloth", "base": "#b03028", "trim": "#701810"}, "wood": {"type": "ridged", "base": "#8a6a3a", "dark": "#4a3418", "light": "#b8924e"},
    "eye": {"type": "plain", "base": "#ffd040"}, "iron": {"type": "metal", "base": "#8a8e96", "dark": "#4a4e56", "light": "#d0d4dc"}, "shell": {"type": "scales", "base": "#1c6a78", "dark": "#0c3a48", "light": "#3fd0b8", "cell": 4},
    "shell_gold": {"type": "metal", "base": "#d8b030", "dark": "#80640e", "light": "#fff0a0"}, "bug": {"type": "skin", "base": "#14343c", "shade": 4}, "red": {"type": "plain", "base": "#d83020"},
}


def strip_chain(r, prefix, parent, pivot, n, paint, w=2, ln=3, amp=0.12, phase=0.0, rx=4):
    prev, pv = parent, pivot
    for i in range(n):
        nm = f"{prefix}{i}"
        r.part(nm, prev, pv, (rx, 0, 0), [box((-w / 2, 0, -0.4), (w, ln, 0.8), paint)])
        r.anim(nm, "sway", axis="x" if i % 2 == 0 else "z", amp=amp + 0.03 * i, freq=0.12 + 0.01 * i, phase=phase + i * 0.9, walk_amp=0.15)
        prev, pv = nm, (0, ln, 0)


def wrap_bands(r, which, paint="linen_dark", head=True):
    """Bands of bandage over limbs and torso: slightly fat thin boxes that break up the silhouette."""
    for p in r.parts:
        nm = p["name"]
        if nm.startswith(("arm_", "forearm_")) or nm.startswith(("leg_", "shin_")):
            p["boxes"].append(box((-2.2, 0.6, -2.2), (4.4, 1, 4.4), paint, 0.0))
            p["boxes"].append(box((-2.2, 3.4, -2.2), (4.4, 1, 4.4), paint, 0.0))
        if nm == "chest":
            for dy, off in ((-6, 0.5), (-3, 0.8), (-1, 0.5)):
                p["boxes"].append(box((-4.6, dy, -2.6), (9.2, 1, 5.2), paint, 0.0))
        if nm == "head" and head:
            p["boxes"].append(box((-4.5, -4.2, -4.5), (9, 1, 9), paint, 0.0))
            p["boxes"].append(box((-4.5, -1.8, -4.5), (9, 1, 9), paint, 0.0))


def mummy(royal=False):
    r = Rig(PAINTS)
    eyes = [rect("front", 1, 2, 2, 1, "#2a1a10"), rect("front", 5, 2, 2, 1, "#2a1a10"), rect("front", 1, 2, 1, 1, "#ffc840"), rect("front", 5, 2, 1, 1, "#ffc840"), rect("front", 0, 3, 8, 1, "#7a5c40")]
    n = r.biped("linen", cloth="linen_dark", head_paint="linen", head_decals=eyes, hip_y=-12, chest=(8, 7, 4), waist=(6, 5, 3), arm_len=(5, 5), stance=-62, swing_arm="r", arm_paint="linen",
                shin_paint="linen", body_paint="linen", hunch=6, feet=True, foot_paint="linen_dark")
    for p in r.parts:      # a gap in the wrappings: dry skin showing through at the ribs and one forearm
        if p["name"] == "chest":
            p["boxes"][0]["decals"] = [rect("front", 1, 2, 3, 2, "#7a5c40"), rect("front", 2, 3, 2, 3, "#5a4230")]
        if p["name"] == "forearm_l":
            p["boxes"][0]["decals"] = [rect("front", 0, 1, 3, 2, "#7a5c40")]
    wrap_bands(r, "all", head=not royal)
    strip_chain(r, "shroud_l", "forearm_l", (1, 5, 1), 3, "linen", 2, 3, phase=0)
    strip_chain(r, "shroud_r", "forearm_r", (-1, 5, 1), 3, "linen", 2, 3, phase=1.5)
    strip_chain(r, "hang_a", "chest", (-2, -1, 2.2), 3, "linen", 2, 4, rx=8, phase=0.7)
    strip_chain(r, "hang_b", "chest", (2, -1, 2.2), 3, "linen", 2, 4, rx=8, phase=2.1)
    strip_chain(r, "tag", "head", (-2, -4.5, 4.4), 3, "linen", 2, 3, rx=14, phase=1.1)
    if royal:
        # a striped nemes headdress with lappets, a uraeus cobra, a false beard, the broad collar, gold bands and a short golden khopesh
        r.part("nemes", "head", (0, -6, 0), (0, 0, 0), [box((-4.8, -2.5, -4.8), (9.6, 3, 9.6), "nemes"), box((-5, -0.5, -4.6), (1.4, 10, 3), "nemes"), box((3.6, -0.5, -4.6), (1.4, 10, 3), "nemes"),
                                                           box((-4.8, -0.5, 3.2), (9.6, 10, 1.6), "nemes"), box((-4.8, -3.6, -4.8), (9.6, 1.2, 9.6), "gold")])
        r.part("uraeus", "head", (0, -4.5, -4.8), (-10, 0, 0), [box((-0.8, -3, -0.8), (1.6, 3, 1.6), "gold"), box((-1.1, -4, -1.1), (2.2, 1.4, 1.6), "gold"), box((-0.5, -3.6, -1.4), (1, 1, 0.6), "red")])
        r.part("beard", "head", (0, 1.5, -4), (8, 0, 0), [box((-1, 0, -1), (2, 5, 2), "lapis"), box((-1.2, 4.6, -1.2), (2.4, 1, 2.4), "gold")])
        for p in r.parts:
            if p["name"] == "chest":
                p["boxes"] += [box((-5.4, -7, -3.2), (10.8, 1.5, 6.4), "gold"), box((-5, -5.8, -3), (10, 1.5, 6), "turq"), box((-4.6, -4.6, -2.8), (9.2, 1.5, 5.6), "lapis"), box((-4.2, -3.4, -2.6), (8.4, 1.2, 5.2), "gold")]
            if p["name"].startswith("forearm"):
                p["boxes"].append(box((-2, 0.5, -2), (4, 1.4, 4), "gold"))
        r.part("khopesh", "hand_r", (0, 1.5, -1), (-60, 0, 0), [box((-0.6, -2, -0.6), (1.2, 4, 1.2), "wood"), box((-1.5, -3, -0.6), (3, 1, 1.2), "gold"), box((-0.5, -9, -0.4), (1, 6, 0.8), "iron"),
                                                                  box((-0.5, -12, -2.2), (1, 3, 0.8), "iron")])
    return r.model(0.5)


def scarab():
    r = Rig(PAINTS)
    r.part("thorax", "root", (0, -4, 0), (0, 0, 0), [box((-3, -2, -3), (6, 4, 6), "bug"), box((-3.5, -2.5, -4), (7, 2, 3), "shell", 0.1)])
    r.part("abdomen", "thorax", (0, 0, 3), (-8, 0, 0), [box((-3.5, -2.5, 0), (7, 5, 8), "shell"), box((-0.4, -2.8, 0), (0.8, 1, 8), "shell_gold")])
    for side, sx in (("l", 1), ("r", -1)):
        # wing cases: two domed plates that part a little, gold-striped
        r.part(f"case_{side}", "thorax", (sx * 0.4, -2.6, -1), (0, sx * 4, sx * -4), [box((0 if sx > 0 else -3.2, 0, 0), (3.2, 1.6, 9), "shell", 0.1), box((0 if sx > 0 else -3.2, -0.3, 1), (3.2, 0.5, 1), "shell_gold"),
                                                                                  box((0 if sx > 0 else -3.2, -0.3, 4), (3.2, 0.5, 1), "shell_gold")])
        r.anim(f"case_{side}", "flap", axis="z", amp=0.05, freq=0.3, phase=0 if sx > 0 else math.pi)
        # antennae
        r.part(f"ant_{side}0", "head", (sx * 1, -1.5, -2), (-50, 0, sx * 20), [box((-0.4, -3, -0.4), (0.8, 3, 0.8), "bug")]) if False else None
    r.part("head", "thorax", (0, 0.5, -3.6), (0, 0, 0), [box((-2, -1.5, -3), (4, 3, 3), "bug", 0, [rect("front", 0, 0, 1, 1, "#d83020"), rect("front", 3, 0, 1, 1, "#d83020")]), box((-1.2, 0.5, -4.4), (2.4, 1, 1.4), "bug")])
    r.anim("head", "look", amount=0.6)
    for side, sx in (("l", 1), ("r", -1)):
        r.part(f"mand_{side}", "head", (sx * 1.2, 1, -3.2), (0, sx * 24, 0), [box((-0.4, -0.4, -2.2), (0.8, 0.8, 2.2), "shell_gold")])
        prev, pv = "head", (sx * 1, -1.5, -2.6)
        for i, (ln, rx) in enumerate(((3, -60), (3, 24))):
            nm = f"ant_{side}{i}"
            r.part(nm, prev, pv, (rx, 0, sx * 26 if i == 0 else sx * 8), [box((-0.4, -ln, -0.4), (0.8, ln, 0.8), "bug")])
            r.anim(nm, "sway", axis="x", amp=0.14, freq=0.18, phase=i + (0 if sx > 0 else 1.7))
            prev, pv = nm, (0, -ln, 0)
        # six legs: three on each side, each of three segments, in a tripod gait
        for k, (z, ph) in enumerate(((-2.6, 0.0), (0.0, math.pi), (2.8, 0.0))):
            ph2 = ph if sx > 0 else ph + math.pi
            nm = f"leg_{side}{k}"
            r.part(nm, "thorax", (sx * 2.8, 1.2, z), (0, sx * (28 - k * 28), sx * 40), [box((-0.5, 0, -0.5), (1, 3, 1), "bug")])
            r.part(f"{nm}b", nm, (0, 3, 0), (0, 0, sx * 58), [box((-0.5, 0, -0.5), (1, 3.4, 1), "bug")])
            r.part(f"{nm}c", f"{nm}b", (0, 3.4, 0), (0, 0, sx * -48), [box((-0.4, 0, -0.4), (0.8, 2.6, 0.8), "bug"), box((-0.8, 2.4, -0.8), (1.6, 0.6, 1.6), "shell_gold")])
            r.anim(nm, "walk", axis="y", amp=0.7, phase=ph2)
            r.anim(nm, "walk", axis="z", amp=0.4, phase=ph2 + 1.57)
    return r.model(0.4)


def tomb_guardian():
    r = Rig(PAINTS)
    eyes = [rect("front", 0, 1, 1, 1, "#40e0f0"), rect("front", 4, 1, 1, 1, "#40e0f0"), rect("front", 1, 0, 3, 1, "#101014")]
    n = r.biped("stone", cloth="gold", head_paint="basalt", head=None, head_decals=[], hip_y=-15, chest=(11, 8, 5), waist=(8, 6, 4), arm_len=(6, 6), leg_len=(8, 7), arm_w=4, leg_w=4,
                hunch=4, stance=-14, shin_paint="stone", thigh_paint="stone", body_paint="stone", arm_paint="stone", foot_paint="gold", swing_arm="r", foot_len=6, shoulder=True)
    # replace the human head with a jackal's: a long snout, black ears that stand tall, glowing cyan eyes, a gold collar
    for p in r.parts:
        if p["name"] == "head":
            p["boxes"] = [box((-3.5, -6, -3.5), (7, 6, 7), "basalt", 0, [rect("front", 0, 2, 2, 1, "#40e0f0"), rect("front", 5, 2, 2, 1, "#40e0f0"), rect("front", 0, 1, 3, 1, "#101014"), rect("front", 4, 1, 3, 1, "#101014")]),
                          box((-3, 0, -3), (6, 2, 6), "basalt")]
    r.part("snout", "head", (0, 0, 0), (6, 0, 0), [box((-1.8, -3.2, -9), (3.6, 3, 5.6), "basalt", 0, [rect("front", 0, 0, 1, 1, "#050508"), rect("front", 2, 0, 1, 1, "#050508")]), box((-1.2, -0.6, -9), (2.4, 1, 5), "black_gold")])
    r.part("nose", "snout", (0, -2, -9), (0, 0, 0), [box((-1.2, -0.8, -0.6), (2.4, 1.6, 1.2), "black_gold")])
    for side, sx in (("l", 1), ("r", -1)):
        r.part(f"ear_{side}", "head", (sx * 2, -5.5, 1), (-6, 0, sx * 8), [box((-1.5, -9, -0.6), (3, 9, 1.2), "basalt"), box((-0.8, -8, -0.8), (1.6, 6, 1.0), "gold")])
        r.anim(f"ear_{side}", "sway", axis="z", amp=0.05, freq=0.14, phase=0 if sx > 0 else 1.3)
    r.part("collar", "chest", (0, -8, 0), (0, 0, 0), [box((-6, 0, -3.4), (12, 1.5, 6.8), "gold"), box((-5.5, 1.3, -3.2), (11, 1.2, 6.4), "turq"), box((-5, 2.4, -3), (10, 1.2, 6), "lapis")])
    for p in r.parts:
        if p["name"] == "chest":
            p["boxes"][0]["decals"] = [rect("front", 4, 4, 3, 3, "#d8b030"), rect("front", 5, 3, 1, 5, "#d8b030"), rect("front", 4, 5, 3, 1, "#d8b030")]    # an ankh cut into the chest
        if p["name"].startswith("forearm"):
            p["boxes"].append(box((-2.2, 0.4, -2.2), (4.4, 2, 4.4), "gold"))
    # a pleated gold-and-lapis kilt (shendyt) and a was-sceptre with a jackal head in the right hand
    r.part("kilt", "body", (0, 0, 0), (0, 0, 0), [box((-5, -1, -2.8), (10, 9, 5.6), "nemes")])
    r.part("scepter", "hand_r", (0, 1, -1.5), (-20, 0, 0), [box((-0.7, -12, -0.7), (1.4, 32, 1.4), "gold"), box((-1.5, -17, -1.2), (3, 5, 2.4), "basalt"), box((-1, -15, -4), (2, 2, 4), "basalt"), box((-0.7, -19, -0.5), (1.4, 3, 1), "basalt")])
    return r.model(0.8)


def forgotten_pharaoh():
    r = Rig(PAINTS)
    mask = [rect("front", 0, 2, 3, 1, "#2a58b0"), rect("front", 5, 2, 3, 1, "#2a58b0"), rect("front", 1, 2, 2, 1, "#ffd040"), rect("front", 5, 2, 2, 1, "#ffd040"), rect("front", 0, 1, 3, 1, "#101014"), rect("front", 5, 1, 3, 1, "#101014"), rect("front", 3, 5, 2, 1, "#8a6a14")]
    n = r.biped("linen", cloth="gold", head_paint="gold", head_decals=mask, hip_y=-14, chest=(10, 8, 5), waist=(8, 6, 4), arm_len=(6, 6), leg_len=(7, 7), arm_w=3, leg_w=4, hunch=2, stance=-18,
                shin_paint="linen", thigh_paint="linen", body_paint="linen", arm_paint="linen", foot_paint="gold", swing_arm="r", foot_len=6)
    wrap_bands(r, "all", "linen_dark", head=False)
    # the double crown: a tall white hedjet inside a red deshret with a spiral, over a striped nemes with lappets
    r.part("nemes", "head", (0, -6, 0), (0, 0, 0), [box((-4.8, -2.5, -4.8), (9.6, 3, 9.6), "nemes"), box((-5, -0.5, -4.6), (1.4, 12, 3.4), "nemes"), box((3.6, -0.5, -4.6), (1.4, 12, 3.4), "nemes"), box((-4.8, -0.5, 3.2), (9.6, 12, 1.6), "nemes")])
    r.part("deshret", "head", (0, -8.5, 0), (0, 0, 0), [box((-4, -3, -4), (8, 3, 8), "red_crown"), box((-3.5, -5, -3.5), (7, 2, 7), "red_crown"), box((-3, -6.5, -3), (6, 1.5, 6), "red_crown")])
    r.part("hedjet", "deshret", (0, -6, 0), (0, 0, 0), [box((-3.4, -6, -3.4), (6.8, 6, 6.8), "white_crown"), box((-3, -9, -3), (6, 3, 6), "white_crown"), box((-2.4, -11.5, -2.4), (4.8, 2.5, 4.8), "white_crown"), box((-1.6, -13, -1.6), (3.2, 1.5, 3.2), "white_crown"), box((-1.2, -14, -1.2), (2.4, 1, 2.4), "gold")])
    r.part("curl", "deshret", (0, -4, -3), (0, 0, 0), [box((-0.5, -5, -2), (1, 1, 2), "red_crown"), box((-0.5, -6, -2.4), (1, 1, 1.4), "red_crown")])
    r.part("uraeus", "head", (0, -5, -4.8), (-10, 0, 0), [box((-0.8, -3, -0.8), (1.6, 3, 1.6), "gold"), box((-1.1, -4, -1.1), (2.2, 1.4, 1.6), "gold")])
    r.part("beard", "head", (0, 1.5, -4), (8, 0, 0), [box((-1, 0, -1), (2, 7, 2), "lapis"), box((-1.2, 6.6, -1.2), (2.4, 1, 2.4), "gold")])
    for p in r.parts:
        if p["name"] == "chest":
            p["boxes"] += [box((-6, -8, -3.6), (12, 1.5, 7.2), "gold"), box((-5.6, -6.8, -3.4), (11.2, 1.5, 6.8), "turq"), box((-5.2, -5.6, -3.2), (10.4, 1.5, 6.4), "lapis"), box((-4.8, -4.4, -3), (9.6, 1.4, 6), "gold"), box((-4.4, -3.2, -2.8), (8.8, 1.2, 5.6), "turq")]
        if p["name"].startswith("forearm"):
            p["boxes"].append(box((-2, 0.5, -2), (4, 1.4, 4), "gold"))
    r.part("kilt", "body", (0, 0, 0), (0, 0, 0), [box((-5, -1, -2.8), (10, 10, 5.6), "nemes")])
    # a tattered shroud streaming from the shoulders, and a crook and flail held crossed on the chest
    for i in range(7):
        x = -7.2 + i * 2.4
        strip_chain(r, f"cape{i}", "chest", (x, -7, 3.2), 4, "linen_dark", 2.2, 5, amp=0.10, phase=i * 0.8, rx=3)
    r.part("crook", "hand_l", (0, 1, -1.5), (-100, 0, 14), [box((-0.6, -10, -0.6), (1.2, 22, 1.2), "gold"), box((-0.6, -14, -0.6), (1.2, 5, 1.2), "lapis"), box((-2.8, -14.6, -0.6), (3.4, 1.2, 1.2), "gold"), box((-2.8, -16, -0.6), (1.2, 2, 1.2), "gold")])
    r.part("flail", "hand_r", (0, 1, -1.5), (-100, 0, -14), [box((-0.6, -10, -0.6), (1.2, 12, 1.2), "gold"), box((-0.8, -11, -0.8), (1.6, 2, 1.6), "lapis")])
    for j, dx in enumerate((-1.6, 0, 1.6)):
        prev, pv = "flail", (dx, -11, 0)
        for k in range(3):
            nm = f"fl{j}{k}"
            r.part(nm, prev, pv, (-14, 0, 0), [box((-0.4, -3, -0.4), (0.8, 3, 0.8), "gold"), box((-0.8, -4, -0.8), (1.6, 1, 1.6), "lapis") if k == 2 else box((-0.3, -3.2, -0.3), (0.6, 0.6, 0.6), "gold")])
            r.anim(nm, "sway", axis="x", amp=0.14, freq=0.15, phase=j + k * 0.8)
            prev, pv = nm, (0, -3, 0)
    return r.model(0.9)


SPECS = {
    "mummy": (mummy, {"id": "mummy", "name": "Mummy", "base": "zombie", "hostile": True, "attributes": {"health": 28, "damage": 4, "armor": 2, "speed": 0.19, "scale": 1.0},
                      "flags": {"sun_sensitive": False, "converts_in_water": False, "baby": False, "reinforcements": False}, "equipment": {},
                      "behaviours": [{"type": "on_hit_effect", "effect": "minecraft:weakness", "seconds": 10, "amplifier": 0}, {"type": "fire_vulnerable", "multiplier": 2.0}],
                      "spawn": {"biomes": ["minecraft:desert"], "weight": 12, "min": 1, "max": 3},
                      "drops": [{"item": "minecraft:bone", "min": 0, "max": 2}, {"item": "minecraft:string", "min": 1, "max": 3}, {"item": "minecraft:rotten_flesh", "min": 0, "max": 2},
                                {"item": "khemet:natron_salt", "min": 1, "max": 2, "chance": 0.3}, {"item": "minecraft:gold_nugget", "min": 1, "max": 4, "chance": 0.3}],
                      "skin": {"model": True}, "egg": ["#d6cdaa", "#ffbe32"], "tests": {"reach_distance": 12, "reach_max_seconds": 20}}),
    "royal_mummy": (lambda: mummy(True), {"id": "royal_mummy", "name": "Royal Mummy", "base": "zombie", "hostile": True, "attributes": {"health": 60, "damage": 7, "armor": 6, "speed": 0.19, "knockback_resistance": 0.4, "scale": 1.08},
                      "flags": {"sun_sensitive": False, "converts_in_water": False, "baby": False, "reinforcements": False}, "equipment": {},
                      "behaviours": [{"type": "on_hit_effect", "effect": "minecraft:weakness", "seconds": 10, "amplifier": 0}, {"type": "fire_vulnerable", "multiplier": 2.0}],
                      "spawn": {"biomes": ["minecraft:desert"], "weight": 1, "min": 1, "max": 1},
                      "drops": [{"item": "minecraft:bone", "min": 1, "max": 3}, {"item": "minecraft:string", "min": 2, "max": 4}, {"item": "minecraft:gold_nugget", "min": 3, "max": 8},
                                {"item": "minecraft:gold_ingot", "min": 1, "max": 3, "chance": 0.6}, {"item": "khemet:sunstone_powder", "min": 1, "max": 1, "chance": 0.35},
                                {"item": "khemet:sacred_myrrh", "min": 1, "max": 1, "chance": 0.25}, {"item": "khemet:ankh", "min": 1, "max": 1, "chance": 0.04}],
                      "skin": {"model": True}, "egg": ["#ecbe3c", "#2643a0"], "tests": {"reach_distance": 12, "reach_max_seconds": 20}}),
    "scarab": (scarab, None), "tomb_guardian": (tomb_guardian, None), "forgotten_pharaoh": (forgotten_pharaoh, None),
}


def main():
    for name, (fn, base) in SPECS.items():
        p = ROOT / "mobs" / f"{name}.json"
        spec = base if base else json.loads(p.read_text())
        spec["model"] = fn()
        spec["skin"] = {"model": True}
        if name == "scarab":
            spec["attributes"].pop("scale", None)
            spec["size"] = [0.9, 0.6]
        p.write_text(json.dumps(spec, indent=2) + "\n")
        print(name, len(spec["model"]["parts"]), "parts")


if __name__ == "__main__":
    main()
