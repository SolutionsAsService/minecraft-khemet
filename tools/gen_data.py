#!/usr/bin/env python3
"""Generate Khemet's loot tables, recipes, block tags, advancements and worldgen data.

    python3 tools/gen_data.py

The structures themselves come from tools/gen_structures.py. Everything here is derived from this script. Stdlib only.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "src/main/resources/data"
K = D / "khemet"
STONES = ["ancient_limestone", "white_limestone", "golden_sandstone", "black_basalt", "polished_pharaoh_stone", "hieroglyph_stone",
          "cracked_temple_stone", "weathered_pyramid_stone", "gold_inlaid_tile", "painted_temple_wall", "hieroglyph_bricks", "obelisk_block"]
BLOCKS = STONES + ["golden_pillar", "lotus_column", "sacred_brazier", "ra_altar", "anubis_altar", "blue_lotus", "papyrus"]


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def item(name, weight, lo=None, hi=None):
    e = {"type": "minecraft:item", "name": name, "weight": weight}
    if lo is not None:
        e["functions"] = [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]
    return e


def pool(entries, lo, hi):
    return {"rolls": {"type": "minecraft:uniform", "min": lo, "max": hi}, "entries": entries}


def chance(entries, c):
    return {"rolls": 1, "bonus_rolls": 0, "conditions": [{"condition": "minecraft:random_chance", "chance": c}], "entries": entries}


def potion_item(pid, weight):
    return {"type": "minecraft:item", "name": "minecraft:potion", "weight": weight, "functions": [{"function": "minecraft:set_potion", "id": pid}]}


def drops_self(name):
    return {"type": "minecraft:block", "random_sequence": f"khemet:blocks/{name}", "pools": [{
        "rolls": 1, "bonus_rolls": 0, "conditions": [{"condition": "minecraft:survives_explosion"}],
        "entries": [{"type": "minecraft:item", "name": f"khemet:{name}"}]}]}


# structure name: (spacing, separation, salt, biomes, spawn overrides)
STRUCTS = {
    "ra_shrine": (32, 10, 8123401, ["minecraft:desert"], {}),
    "anubis_shrine": (34, 10, 8123402, ["minecraft:desert", "#minecraft:is_badlands"],
                      {"monster": {"bounding_box": "piece", "spawns": [{"type": "khemet:mummy", "weight": 10, "minCount": 2, "maxCount": 3},
                                                                       {"type": "khemet:royal_mummy", "weight": 1, "minCount": 1, "maxCount": 1}]}}),
    "obelisk_field": (30, 10, 8123403, ["minecraft:desert"], {}),
    "desert_ruin": (20, 8, 8123404, ["minecraft:desert"],
                    {"monster": {"bounding_box": "piece", "spawns": [{"type": "khemet:mummy", "weight": 10, "minCount": 1, "maxCount": 2}]}}),
}
VARIANTS = {"ra_shrine": 2, "anubis_shrine": 2, "obelisk_field": 2, "desert_ruin": 3}


def main():
    for n in BLOCKS:
        write(K / "loot_table/blocks" / f"{n}.json", drops_self(n))
    # chests
    chests = {
        "ra_shrine": [pool([item("khemet:sunstone_powder", 5, 1, 3), item("minecraft:gold_ingot", 6, 2, 6), item("minecraft:golden_apple", 2),
                            item("khemet:golden_date", 4, 1, 3), item("khemet:sacred_myrrh", 3, 1, 2), item("minecraft:sunflower", 4, 2, 5),
                            item("minecraft:lapis_lazuli", 4, 3, 8), potion_item("khemet:blood_of_ra", 2)], 4, 6),
                      chance([item("khemet:ankh", 1)], 0.3)],
        "anubis_shrine": [pool([item("khemet:natron_salt", 5, 1, 3), item("minecraft:bone", 6, 3, 8), item("minecraft:gold_ingot", 4, 2, 5),
                                item("minecraft:soul_sand", 3, 2, 6), item("khemet:falcon_feather", 2, 1, 2), item("minecraft:lapis_lazuli", 3, 2, 6),
                                potion_item("khemet:anubis_veil", 2)], 4, 6),
                          chance([item("khemet:khopesh", 1)], 0.3)],
        "obelisk_field": [pool([item("minecraft:gold_nugget", 6, 4, 12), item("minecraft:lapis_lazuli", 5, 3, 8), item("khemet:hieroglyph_stone", 4, 2, 6),
                                item("khemet:falcon_feather", 3, 1, 2), item("khemet:golden_sandstone", 3, 3, 8), item("khemet:sunstone_powder", 2, 1, 2)], 3, 5)],
        "desert_ruin": [pool([item("minecraft:gold_nugget", 6, 2, 8), item("khemet:natron_salt", 4, 1, 3), item("khemet:golden_date", 4, 1, 3),
                              item("minecraft:bone", 4, 2, 5), item("khemet:papyrus", 3, 1, 3),
                              item("minecraft:emerald", 2, 1, 2), item("khemet:sacred_myrrh", 2, 1, 1)], 2, 4)],
    }
    for name, pools in chests.items():
        write(K / "loot_table/chests" / f"{name}.json", {"type": "minecraft:chest", "pools": pools})
    write(K / "loot_table/entities/mummy.json", {"type": "minecraft:entity", "pools": [
        pool([item("minecraft:bone", 4, 0, 2), item("minecraft:string", 4, 1, 3), item("minecraft:rotten_flesh", 4, 0, 2)], 1, 2),
        chance([item("khemet:natron_salt", 1, 1, 2)], 0.3), chance([item("minecraft:gold_nugget", 1, 1, 4)], 0.3)]})
    write(K / "loot_table/entities/royal_mummy.json", {"type": "minecraft:entity", "pools": [
        pool([item("minecraft:bone", 4, 1, 3), item("minecraft:string", 4, 2, 4), item("minecraft:gold_nugget", 5, 3, 8)], 2, 3),
        chance([item("minecraft:gold_ingot", 1, 1, 3)], 0.6), chance([item("khemet:sunstone_powder", 1)], 0.35),
        chance([item("khemet:sacred_myrrh", 1)], 0.25), chance([item("khemet:ankh", 1)], 0.04)]})
    # recipes
    rec = K / "recipe"
    for n, src in (("ancient_limestone", "minecraft:sandstone"), ("weathered_pyramid_stone", "minecraft:sandstone"), ("hieroglyph_stone", "minecraft:sandstone"),
                   ("cracked_temple_stone", "minecraft:sandstone"), ("hieroglyph_bricks", "minecraft:sandstone"), ("polished_pharaoh_stone", "minecraft:sandstone"),
                   ("white_limestone", "minecraft:calcite"), ("black_basalt", "minecraft:smooth_basalt"), ("golden_sandstone", "minecraft:cut_sandstone"),
                   ("gold_inlaid_tile", "khemet:polished_pharaoh_stone"), ("painted_temple_wall", "khemet:polished_pharaoh_stone"),
                   ("obelisk_block", "khemet:polished_pharaoh_stone")):
        write(rec / f"{n}_from_stonecutting.json", {"type": "minecraft:stonecutting", "ingredient": src, "result": {"id": f"khemet:{n}", "count": 1}})
    write(rec / "golden_pillar.json", {"type": "minecraft:crafting_shaped", "category": "building", "pattern": ["S", "S", "S"],
          "key": {"S": "khemet:golden_sandstone"}, "result": {"id": "khemet:golden_pillar", "count": 3}})
    write(rec / "lotus_column.json", {"type": "minecraft:crafting_shaped", "category": "building", "pattern": ["W", "L", "W"],
          "key": {"W": "khemet:white_limestone", "L": "khemet:blue_lotus"}, "result": {"id": "khemet:lotus_column", "count": 2}})
    write(rec / "sacred_brazier.json", {"type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["G G", "BCB", "BBB"],
          "key": {"G": "minecraft:gold_ingot", "B": "khemet:black_basalt", "C": "minecraft:coal"}, "result": {"id": "khemet:sacred_brazier", "count": 1}})
    write(rec / "ankh.json", {"type": "minecraft:crafting_shapeless", "category": "equipment", "ingredients": [
        "minecraft:gold_ingot", "minecraft:gold_ingot", "khemet:sunstone_powder", "khemet:sacred_myrrh"], "result": {"id": "khemet:ankh", "count": 1}})
    write(rec / "khopesh.json", {"type": "minecraft:crafting_shaped", "category": "equipment", "pattern": ["GG", " G", " S"],
          "key": {"G": "minecraft:gold_ingot", "S": "minecraft:stick"}, "result": {"id": "khemet:khopesh", "count": 1}})
    # tags
    tag = D / "minecraft/tags/block"
    write(tag / "mineable/pickaxe.json", {"replace": False, "values": [f"khemet:{n}" for n in STONES + ["golden_pillar", "lotus_column", "sacred_brazier", "ra_altar", "anubis_altar"]]})
    write(tag / "small_flowers.json", {"replace": False, "values": ["khemet:blue_lotus"]})
    # worldgen
    for name, (spacing, sep, salt, biomes, spawns) in STRUCTS.items():
        write(K / "worldgen/structure" / f"{name}.json", {
            "type": "minecraft:jigsaw", "biomes": f"#khemet:has_structure/{name}", "step": "surface_structures", "spawn_overrides": spawns,
            "terrain_adaptation": "beard_thin", "start_pool": f"khemet:{name}", "size": 1, "start_height": {"absolute": 0},
            "project_start_to_heightmap": "WORLD_SURFACE_WG", "max_distance_from_center": 40, "use_expansion_hack": False})
        write(K / "worldgen/template_pool" / f"{name}.json", {"fallback": "minecraft:empty", "elements": [
            {"weight": 1, "element": {"element_type": "minecraft:single_pool_element", "location": f"khemet:{name}_{i}",
                                      "processors": "minecraft:empty", "projection": "rigid"}} for i in range(VARIANTS[name])]})
        write(K / "worldgen/structure_set" / f"{name}.json", {"structures": [{"structure": f"khemet:{name}", "weight": 1}],
              "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": sep, "salt": salt}})
        write(K / "tags/worldgen/biome/has_structure" / f"{name}.json", {"values": biomes})
    # advancements
    def adv(name, parent, icon, title, desc, trigger, conditions, frame="task", root=False):
        disp = {"icon": {"id": icon}, "title": {"text": title}, "description": {"text": desc}, "frame": frame,
                "show_toast": not root, "announce_to_chat": not root, "hidden": False}
        if root:
            disp["background"] = "minecraft:textures/gui/advancements/backgrounds/stone.png"
        d = {"display": disp, "criteria": {"c": {"trigger": trigger, "conditions": conditions}}}
        if parent:
            d["parent"] = f"khemet:{parent}"
        write(K / "advancement" / f"{name}.json", d)

    def loc(s):
        return {"player": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"location": {"structures": f"khemet:{s}"}}}]}

    def kind(t):
        return {"entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": f"khemet:{t}"}}]}

    def have(i):
        return {"items": [{"items": i}]}
    adv("root", None, "khemet:golden_sandstone", "Khemet", "Sands of the ancient gods.", "minecraft:tick", {}, root=True)
    adv("desert_ruin", "root", "khemet:cracked_temple_stone", "Under the Dunes", "Find a ruin in the desert.", "minecraft:location", loc("desert_ruin"))
    adv("obelisk_field", "root", "khemet:obelisk_block", "A Field of Needles", "Find an obelisk field.", "minecraft:location", loc("obelisk_field"))
    adv("ra_shrine", "obelisk_field", "khemet:ra_altar", "Where the Sun Stands", "Find the shrine of Ra.", "minecraft:location", loc("ra_shrine"))
    adv("anubis_shrine", "desert_ruin", "khemet:anubis_altar", "The Jackal's Court", "Find the shrine of Anubis.", "minecraft:location", loc("anubis_shrine"))
    adv("mummy", "desert_ruin", "minecraft:bone", "Unwrapped", "Defeat a mummy.", "minecraft:player_killed_entity", kind("mummy"))
    adv("royal_mummy", "anubis_shrine", "minecraft:golden_helmet", "A Crown Taken", "Defeat a royal mummy.", "minecraft:player_killed_entity", kind("royal_mummy"), "challenge")
    adv("ankh", "ra_shrine", "khemet:ankh", "The Key of Life", "Hold an Ankh of Life.", "minecraft:inventory_changed", have("khemet:ankh"), "challenge")
    adv("khopesh", "anubis_shrine", "khemet:khopesh", "A Curved Blade", "Hold Anubis's Khopesh.", "minecraft:inventory_changed", have("khemet:khopesh"), "challenge")
    print("khemet data written")


if __name__ == "__main__":
    main()
