#!/usr/bin/env python3
"""Copy the creature photographs into the site and compose the group pictures (needs ImageMagick).

    python3 tools/creature_shots.py     playtest/models/<id>-*.png -> site/img/shots/, plus creatures-all.png and panels/creatures-all.png
"""
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "playtest/models"
OUT = ROOT / "site/img/shots"
ORDER = ["scarab", "cobra", "crocodile", "mummy", "royal_mummy", "tomb_guardian", "sun_pharaoh", "forgotten_pharaoh", "chariot"]
BOSSES = {"forgotten_pharaoh", "sun_pharaoh"}


def run(*a):
    subprocess.run(a, check=True)


def frame(src, dst, size="854x480", boss=False):
    """The cameras are aimed and set by tools/model_sheet.py; a boss's frame loses its top 40 pixels (the boss bar) and is trimmed back to 16:9."""
    if boss:
        run("convert", str(src), "-crop", "782x440+36+40", "+repage", "-filter", "point", "-resize", size + "!", str(dst))
    else:
        run("convert", str(src), "-filter", "point", "-resize", size + "!", str(dst))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tiles = []
    for i in ORDER:
        frame(SRC / f"{i}-three-quarter.png", OUT / f"{i}-three-quarter.png", boss=i in BOSSES)
        frame(SRC / f"{i}-side.png", OUT / f"{i}-side.png", boss=i in BOSSES)
        for v in ("face-side", "face"):
            shutil.copy(SRC / f"{i}-{v}.png", OUT / f"{i}-{v}.png")
        t = OUT / f".tile-{i}.png"
        frame(SRC / f"{i}-three-quarter.png", t, "427x240", boss=i in BOSSES)
        tiles.append(str(t))
    run("montage", *tiles, "-tile", "3x3", "-geometry", "427x240+0+0", "-background", "#d8c898", str(OUT / "creatures-all.png"))
    (OUT / "panels").mkdir(exist_ok=True)
    shutil.copy(OUT / "creatures-all.png", OUT / "panels/creatures-all.png")
    for t in tiles:
        Path(t).unlink()
    print("creature pictures written")


if __name__ == "__main__":
    main()
