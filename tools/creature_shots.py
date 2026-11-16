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
ORDER = ["scarab", "cobra", "crocodile", "mummy", "royal_mummy", "tomb_guardian", "sun_pharaoh", "forgotten_pharaoh"]
CROP = {"crocodile": "440x495+187+60", "scarab": "260x293+297+140", "cobra": "250x281+302+90"}


def run(*a):
    subprocess.run(a, check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tiles = []
    for i in ORDER:
        for v in ("three-quarter", "face-side", "face"):
            shutil.copy(SRC / f"{i}-{v}.png", OUT / f"{i}-{v}.png")
        t = OUT / f".tile-{i}.png"
        run("convert", str(SRC / f"{i}-three-quarter.png"), "-crop", CROP.get(i, "250x281+302+50"), "+repage", "-filter", "point", "-resize", "213x240!", str(t))
        tiles.append(str(t))
    run("montage", *tiles, "-tile", "4x2", "-geometry", "213x240+0+0", "-background", "#d8c898", str(OUT / "creatures-all.png"))
    (OUT / "panels").mkdir(exist_ok=True)
    shutil.copy(OUT / "creatures-all.png", OUT / "panels/creatures-all.png")
    for t in tiles:
        Path(t).unlink()
    print("creature pictures written")


if __name__ == "__main__":
    main()
