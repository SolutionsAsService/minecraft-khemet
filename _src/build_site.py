#!/usr/bin/env python3
"""Build the Khemet site (site/) from the mod's own files.

Every figure, table row and colour check on the site is computed here from the mod's data: block states and language entries,
potions.json, content.json (gods, favor, artifacts, sandstorm), the structure NBT and worldgen JSON, the loot tables, and the
entity classes. In-game photographs are read from site/img/shots/ and a page never refers to a capture that does not exist.

    python3 _src/build_site.py

The output (site/) is committed. The deploy serves it as static files and never runs this script. The build fails when the
palette or the Shadw/Vercel deploy files do not hold (see check_palette and check_deploy).
"""

import html
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"
SITE_URL = "https://minecraft-khemet.shadw.app"
ASSETS = REPO / "src/main/resources/assets/khemet"
DATA = REPO / "src/main/resources/data/khemet"
JAVA = REPO / "src/main/java/dev/shadw/khemet"
sys.path.insert(0, str(REPO / "tools"))
from shadwlib import nbt  # noqa: E402

# ---------- palette: the six canonical colours of Egyptian painting, plus faience and carnelian ----------
# Kemet ("the Black Land", the Nile's silt) is the page ground; Deshret ("the Red Land") is the desert. Gold is reserved for the
# argument (links, buttons). Each topic category has one hue; none of them is the signal.
GROUND = "#14110F"        # Kemet, the Black Land
CARD = "#201B16"
TEXT = "#F2EBD6"          # gypsum white
MUTED = "#BDB29A"
SIGNAL = "#EDBE3A"        # orpiment yellow, the argument
HUES = {                  # category -> (hue, name of the pigment or material)
    "blocks": ("#D8CCAA", "limestone white"),
    "gods": ("#6A9BEA", "Egyptian blue"),
    "structures": ("#E4685F", "red ochre, Deshret"),
    "potions": ("#86C24F", "malachite green"),
    "creatures": ("#35C4B6", "faience turquoise"),
    "relics": ("#DE86C6", "amethyst"),
}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def mix(a, b, t):
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(rgb(a), rgb(b)))


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    r, g, b = rgb(h)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def lab(h):
    r, g, b = (_lin(v) for v in rgb(h))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def delta_e(a, b):
    return math.dist(lab(a), lab(b))


def check_palette():
    """Measured, not asserted: the build fails below delta-E 30 between any two hues, below 3:1 for marks, or below 4.5:1 for text."""
    hues = {k: v[0] for k, v in HUES.items()}
    hues["signal"] = SIGNAL
    pairs = [(a, b) for i, a in enumerate(hues) for b in list(hues)[i + 1:]]
    worst = min(pairs, key=lambda p: delta_e(hues[p[0]], hues[p[1]]))
    de = delta_e(hues[worst[0]], hues[worst[1]])
    errors = []
    if de < 30:
        errors.append(f"hues {worst[0]} / {worst[1]} are only delta-E {de:.1f} apart (need 30)")
    for k, h in hues.items():
        band = mix(h, GROUND, 0.82)       # the dark panel band the hue sits on
        for ground, what in ((GROUND, "page ground"), (CARD, "card"), (band, "panel band")):
            c = contrast(h, ground)
            if c < 4.5:
                errors.append(f"{k} text on {what} is {c:.2f}:1 (need 4.5)")
    for what, fg, bg in (("body text", TEXT, GROUND), ("body text on card", TEXT, CARD), ("muted text", MUTED, GROUND), ("muted on card", MUTED, CARD)):
        if contrast(fg, bg) < 4.5:
            errors.append(f"{what} is {contrast(fg, bg):.2f}:1 (need 4.5)")
    if errors:
        raise SystemExit("palette check failed:\n  " + "\n  ".join(errors))
    return {"min_delta_e": round(de, 1), "min_pair": f"{worst[0]} / {worst[1]}",
            "min_contrast": round(min(contrast(h, band_) for h in hues.values() for band_ in (GROUND, CARD)), 2)}


def check_deploy():
    """The Shadw/Vercel guarantee, checked rather than remembered."""
    need = {}
    for rel, expect in (("vercel.json", "site"), ("site/vercel.json", ".")):
        d = json.loads((REPO / rel).read_text())
        for k, v in (("framework", None), ("installCommand", ""), ("buildCommand", ""), ("outputDirectory", expect), ("cleanUrls", True), ("fluid", True)):
            if d.get(k, "MISSING") != v:
                need[f"{rel}: {k}"] = f"expected {v!r}, found {d.get(k, 'MISSING')!r}"
    f = json.loads((REPO / "fluid.json").read_text())
    if f.get("project") != "minecraft-khemet" or f.get("static_dir") != "site" or f.get("routes") != [{"pattern": "/", "target": "static"}]:
        need["fluid.json"] = "needs project minecraft-khemet, static_dir site, and routes [{pattern: /, target: static}] only"
    if "site/index.html" not in (REPO / "index.html").read_text():
        need["index.html"] = "the root redirect must point at site/index.html"
    ignore = (REPO / ".vercelignore").read_text().split()
    if "/_src/" not in ignore or any(not e.startswith("/") for e in ignore):
        need[".vercelignore"] = "entries must be anchored at the root (/_src/)"
    if need:
        raise SystemExit("deploy files check failed:\n  " + "\n  ".join(f"{k}: {v}" for k, v in need.items()))


# ---------- reading the mod ----------

def jread(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def esc(v):
    return html.escape(str(v), quote=True)


def label(rid):
    return rid.split(":")[-1].replace("_", " ").title()


def dur(s):
    return f"{s // 60}:{s % 60:02d}"


def roman(n):
    return ["", "I", "II", "III", "IV", "V"][n]


LANG = jread(ASSETS / "lang/en_us.json")
CONTENT = jread(ASSETS / "content.json")
POTIONS = jread(ASSETS / "potions.json")["potions"]
EFFECT = {"minecraft:strength": "Strength", "minecraft:fire_resistance": "Fire Resistance", "minecraft:regeneration": "Regeneration",
          "minecraft:speed": "Speed", "minecraft:slow_falling": "Slow Falling", "minecraft:invisibility": "Invisibility", "minecraft:luck": "Luck",
          "minecraft:resistance": "Resistance", "minecraft:night_vision": "Night Vision", "minecraft:absorption": "Absorption"}


def fx(e):
    return f"{EFFECT.get(e['effect'], label(e['effect']))} {roman(e['amplifier'] + 1)} for {dur(e['seconds'])}"


def block_ids():
    return sorted(p.stem for p in (ASSETS / "blockstates").glob("*.json"))


def stone_order():
    m = re.search(r"STONES\s*=\s*\{(.*?)\}", (JAVA / "KhemetBlocks.java").read_text(), re.S)
    return re.findall(r'"([a-z_]+)"', m.group(1))


def shot(name):
    return f"/img/shots/{name}.png" if (SITE / "img/shots" / f"{name}.png").exists() else None


def nbt_size(name):
    root = nbt.loads((DATA / "structure" / f"{name}.nbt").read_bytes())
    return tuple(root["size"][1][1]), len(root["blocks"][1][1])


def variants(slug):
    return len(list((DATA / "structure").glob(f"{slug}_*.nbt")))


def chest_items(slug):
    d = jread(DATA / "loot_table/chests" / f"{slug}.json")
    out = []
    for pool in d["pools"]:
        for e in pool["entries"]:
            if e.get("type") == "minecraft:item":
                n = e["name"]
                if n == "minecraft:potion":
                    pid = e["functions"][0]["id"].split(":")[-1]
                    n = "Potion of " + next((p["name"] for p in POTIONS if p["id"] == pid), label(pid))
                else:
                    n = label(n)
                if n not in out:
                    out.append(n)
    return out


def java_attrs(cls):
    src = (JAVA / f"{cls}.java").read_text()
    out = {}
    for key, name in (("MAX_HEALTH", "health"), ("ATTACK_DAMAGE", "damage"), ("ARMOR", "armour"), ("MOVEMENT_SPEED", "speed"), ("KNOCKBACK_RESISTANCE", "knockback")):
        m = re.search(rf"Attributes\.{key},\s*([0-9.]+)", src)
        if m:
            out[name] = float(m.group(1))
    return out


def spawn_rules():
    src = (JAVA / "KhemetEntities.java").read_text()
    return {m.group(2): dict(weight=int(m.group(3)), lo=int(m.group(4)), hi=int(m.group(5)))
            for m in re.finditer(r"addSpawn\(.*?MobCategory\.MONSTER,\s*(\w+),?\s*(\d+),\s*(\d+),\s*(\d+)\)", src, re.S)} if False else {
        m.group(1): dict(weight=int(m.group(2)), lo=int(m.group(3)), hi=int(m.group(4)))
        for m in re.finditer(r"MobCategory\.MONSTER,\s*(\w+),\s*(\d+),\s*(\d+),\s*(\d+)\)", src)}


# ---------- page shell ----------

NAV = [("index.html", "Home", "home"), ("blocks.html", "Blocks", "blocks"), ("potions.html", "Potions", "potions"),
       ("gods.html", "Gods", "gods"), ("structures.html", "Structures", "structures"), ("creatures.html", "Creatures", "creatures"),
       ("relics.html", "Relics", "relics"), ("install.html", "Install", "install")]


def typo(markup):
    """Real apostrophes in prose; <pre> and <code> keep straight ones."""
    out = []
    for part in re.split(r"(<pre.*?</pre>|<code>.*?</code>|<style.*?</style>)", markup, flags=re.S):
        out.append(part if part.startswith(("<pre", "<code>", "<style")) else part.replace("&#x27;", "’").replace("'", "’"))
    return "".join(out)


def css():
    hv = "\n".join(f"  --{k}: {v[0]};" for k, v in HUES.items())
    return f""":root {{
  --ground: {GROUND}; --card: {CARD}; --text: {TEXT}; --muted: {MUTED}; --signal: {SIGNAL};
{hv}
  --hue: var(--signal);
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
}}
* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{ margin: 0; background: var(--ground); color: var(--text); font: 16px/1.55 "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif; }}
img {{ max-width: 100%; height: auto; }}
a {{ color: var(--signal); }}
a:focus-visible, .btn:focus-visible {{ outline: 3px solid var(--text); outline-offset: 3px; }}
.skip {{ position: absolute; left: 12px; top: -60px; background: var(--signal); color: #000; padding: 10px 14px; z-index: 9; }}
.skip:focus {{ top: 10px; }}
.skip:focus-visible {{ outline: 3px solid #000; outline-offset: 2px; }}
.serif, h1, h2, h3, .brand, .panel .name, .ladder b {{ font-family: var(--serif); }}
.frieze {{ height: 12px; background:
  linear-gradient(var(--signal), var(--signal)) 0 0 / 100% 2px no-repeat,
  linear-gradient(var(--signal), var(--signal)) 0 100% / 100% 2px no-repeat,
  repeating-linear-gradient(90deg, var(--signal) 0 6px, transparent 6px 12px) 0 50% / 100% 4px no-repeat; }}
.top {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 2px 14px; padding: 6px 16px; background: #0c0a08; }}
.brand {{ font-weight: 800; letter-spacing: .22em; color: var(--text); text-decoration: none; display: inline-flex; align-items: center; min-height: 44px; }}
.top nav {{ display: flex; flex-wrap: wrap; gap: 0 2px; }}
.top nav a {{ display: inline-flex; align-items: center; min-height: 44px; padding: 6px 10px; color: var(--text); text-decoration: none; font-size: 15px; }}
.top nav a[aria-current="page"] {{ border-bottom: 4px solid var(--signal); }}
@media (hover: hover) {{ .top nav a:hover {{ background: var(--card); }} }}
main {{ display: block; }}
.eyebrow {{ text-transform: uppercase; letter-spacing: .16em; font-size: 13px; color: var(--hue); margin: 0 0 4px; font-weight: 700; }}
h1 {{ font-size: clamp(30px, 6vw, 52px); line-height: 1.08; margin: 0 0 10px; letter-spacing: .06em; text-transform: uppercase; }}
h2 {{ font-size: 28px; margin: 34px 0 8px; line-height: 1.2; }}
h3 {{ font-size: 20px; margin: 0 0 4px; }}
.page {{ max-width: 980px; margin: 0 auto; padding: 26px 16px 56px; }}
.page p, .page li, .band p {{ max-width: 38em; text-wrap: pretty; }}
.lede {{ color: var(--muted); font-size: 18px; max-width: 34em; }}
.meta {{ color: var(--muted); font-size: 14px; max-width: 38em; }}
.page .rule {{ border-top: 4px solid var(--hue); margin: 4px 0 18px; width: 90px; }}
.btn {{ display: inline-flex; align-items: center; min-height: 44px; padding: 8px 20px; font-weight: 800; text-decoration: none; background: var(--signal); color: #000; border: 3px solid #000; }}
.btn-alt {{ background: var(--text); }}
.btn-quiet {{ background: transparent; color: var(--signal); border-color: var(--signal); }}
.action {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 16px 0 0; }}
.shots {{ display: grid; grid-template-columns: 1fr; gap: 14px; margin: 14px 0; }}
.shot {{ margin: 0; }}
.shot img {{ display: block; width: 100%; border: 3px solid var(--hue); }}
.shot figcaption {{ color: var(--muted); font-size: 14px; margin-top: 6px; }}
@media (min-width: 760px) {{ .shots.two {{ grid-template-columns: 1fr 1fr; }} }}
table.data {{ width: 100%; border-collapse: collapse; background: var(--card); margin: 12px 0 8px; font-size: 15px; }}
table.data td, .ladder b {{ font-variant-numeric: lining-nums tabular-nums; }}
table.data th, table.data td {{ text-align: left; vertical-align: top; padding: 9px 12px; border-bottom: 1px solid #3a322a; overflow-wrap: anywhere; }}
table.data th {{ width: 8.5em; color: var(--hue); font-weight: 700; }}
.sr {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
.cards {{ display: grid; grid-template-columns: 1fr; gap: 10px; margin: 12px 0; padding: 0; list-style: none; }}
@media (min-width: 720px) {{ .cards {{ grid-template-columns: 1fr 1fr; }} }}
.card {{ display: flex; gap: 14px; align-items: flex-start; background: var(--card); border: 3px solid #000; border-left: 6px solid var(--hue); padding: 12px; }}
.card img.px {{ flex: none; width: 64px; height: 64px; image-rendering: pixelated; background: #000; padding: 4px; border: 2px solid #3a322a; }}
.card h3 {{ margin: 0; }} .card p {{ margin: 2px 0 0; font-size: 15px; color: var(--muted); }}
.wallnote {{ margin: 8px 0 0; font-size: 13px; }}
.gloss {{ max-width: 44em; }} .gloss dt {{ font-family: var(--serif); font-weight: 700; color: var(--signal); margin-top: 10px; }} .gloss dd {{ margin: 2px 0 0; color: var(--text); }}
.status {{ border: 3px solid var(--hue); background: var(--card); padding: 12px 16px; margin: 26px 0 0; }}
.status h2 {{ font-size: 20px; margin: 0 0 6px; }} .status p, .status li {{ font-size: 15px; max-width: 46em; }} .status ul {{ margin: 6px 0; padding-left: 20px; }}
.ladder {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: 14px 0; padding: 0; list-style: none; max-width: 640px; }}
.ladder li {{ background: var(--card); border-top: 6px solid var(--gods); padding: 8px 8px 10px; text-align: center; }}
.ladder li:nth-child(2) {{ border-top-width: 10px; }} .ladder li:nth-child(3) {{ border-top-width: 14px; }} .ladder li:nth-child(4) {{ border-top-width: 18px; }}
.ladder b {{ display: block; font-size: 24px; font-family: Georgia, serif; }} .ladder span {{ font-size: 13px; color: var(--muted); }}
.sec {{ margin-top: 40px; scroll-margin-top: 12px; }}
/* the landing: a register wall of six photograph panels under a cartouche */
.wall {{ max-width: 1060px; margin: 0 auto; padding: 14px 14px 10px; }}
.cartouche {{ display: flex; flex-wrap: wrap; align-items: center; gap: 4px 24px; margin: 4px 0 14px; }}
.cartouche h1 {{ margin: 0; border: 3px solid var(--signal); border-radius: 999px; padding: 4px 30px 4px 26px; position: relative; font-size: clamp(30px, 5.4vw, 58px); }}
.cartouche .dot {{ display: none; }}
.cartouche .btn {{ margin-left: 4px; }}
.cartouche .sub {{ margin: 0; color: var(--muted); font-size: 16px; max-width: 28em; }}
.panels {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 0; padding: 0; list-style: none; }}
.panel {{ display: block; text-decoration: none; color: var(--text); background: color-mix(in srgb, var(--hue) 18%, var(--ground)); border: 3px solid var(--hue); height: 100%; }}
.panel .ph {{ display: block; width: 100%; aspect-ratio: 2 / 1; object-fit: cover; background: #000; }}
.panel .ph.art {{ display: flex; align-items: center; justify-content: center; gap: 14px; }}
.panel .ph.art img {{ width: 56px; height: 56px; image-rendering: pixelated; }}
.panel .pn {{ display: block; padding: 7px 10px 9px; }}
.panel .name {{ display: flex; align-items: center; gap: 8px; font-family: Georgia, serif; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: var(--hue); font-size: 15px; line-height: 1.15; }}
.panel .name img {{ width: 22px; height: 22px; image-rendering: pixelated; flex: none; }}
.panel .name::after {{ content: "\\2192"; margin-left: auto; color: var(--text); }}
.panel .fig {{ display: block; font-size: 14px; font-weight: 700; margin-top: 2px; }}
.panel .claim {{ display: none; font-size: 13px; color: var(--muted); margin-top: 1px; }}
@media (hover: hover) {{ .panel:hover {{ background: color-mix(in srgb, var(--hue) 30%, var(--ground)); }} }}
@media (min-width: 1100px) {{ .panel .ph {{ aspect-ratio: 7 / 4; }} }}
@media (min-width: 720px) {{ .panel .claim {{ display: block; }} .panel .name {{ font-size: 16px; }} }}
@media (max-width: 719px) {{ .cartouche .dot {{ display: inline; }} .panels {{ grid-template-columns: repeat(2, 1fr); gap: 8px; }} .cartouche {{ margin-bottom: 10px; }} .cartouche .sub {{ font-size: 15px; }} .cartouche .sub .more {{ display: none; }}
  .top nav a {{ font-size: 14px; padding: 6px 8px; }} .panel .ph {{ aspect-ratio: 5 / 2; }} .panel .name img {{ display: none; }} .panel .name {{ font-size: 13px; }} .panel .fig {{ font-size: 13px; }} .panel .pn {{ padding: 6px 8px 8px; }} }}
code, pre {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 14px; overflow-wrap: anywhere; }}
pre {{ white-space: pre-wrap; background: var(--card); border-left: 4px solid var(--hue); padding: 10px 12px; margin: 10px 0; }}
.foot {{ border-top: 0; padding: 18px 16px 30px; color: var(--muted); font-size: 14px; max-width: 980px; margin: 0 auto; }}
.foot p {{ max-width: 46em; }} .foot a {{ display: inline-block; padding: 3px 0; }}
@media (forced-colors: active) {{
  .btn, .btn-quiet {{ border: 2px solid ButtonText; }}
  .top nav a[aria-current="page"] {{ border-bottom: 4px solid Highlight; }}
  a:focus-visible, .btn:focus-visible {{ outline: 3px solid CanvasText; }}
  .panel {{ border: 3px solid CanvasText; }}
  .frieze {{ background: none; border-top: 2px solid CanvasText; border-bottom: 2px solid CanvasText; }}
}}
@media (prefers-reduced-motion: no-preference) {{ html {{ scroll-behavior: smooth; }} }}
"""


def page(title, desc, body, active, path, hue=None, image="/img/og.png"):
    nav = "".join(f'<a href="/{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for h, t, k in NAV)
    style = f' style="--hue:var(--{hue})"' if hue else ""
    return typo(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{esc(SITE_URL + '/' + path)}">
<meta property="og:image" content="{SITE_URL}{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{GROUND}">
<link rel="icon" href="/img/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
</head>
<body{style}>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="brand" href="/index.html">KHEMET</a>
  <nav aria-label="Primary">{nav}</nav>
</header>
<div class="frieze" aria-hidden="true"></div>
<main id="main" tabindex="-1">
{body}
</main>
<div class="frieze" aria-hidden="true"></div>
<footer class="foot">
  <p>A Minecraft mod for Fabric 1.21.4, the Egyptian sibling of <a href="https://github.com/SolutionsAsService/minecraft-asgard">Asgard</a>. Source: <a href="https://github.com/SolutionsAsService/minecraft-khemet">minecraft-khemet</a>. Built with <a href="https://github.com/SolutionsAsService/shadw-modding">shadw-modding</a>. Credit: SolutionsAsService. Dark theme only. English only.</p>
</footer>
</body>
</html>
""")


def status(tested, untested, hue=None):
    t = "".join(f"<li>{esc(x)}</li>" for x in tested)
    u = "".join(f"<li>{esc(x)}</li>" for x in untested)
    return (f'<section class="status"><h2>Status</h2><p><b>Seen in a running Minecraft 1.21.4 game:</b></p><ul>{t}</ul>'
            f'<p><b>Not yet tested:</b></p><ul>{u}</ul></section>')


def fig(name, caption, alt):
    return (f'<figure class="shot"><img src="{shot(name)}" alt="{esc(alt)}" width="854" height="480" loading="lazy"><figcaption>{esc(caption)}</figcaption></figure>'
            if shot(name) else "")


def sprite(rel, size=64, alt=""):
    return f'<img class="px" src="/img/tex/{rel}.png" width="{size}" height="{size}" alt="{esc(alt)}">'


RECIPE_TEXT = {
    "golden_pillar": "Crafting: three Golden Sandstone in a column make three pillars",
    "lotus_column": "Crafting: White Limestone above and below a Blue Lotus makes two columns",
    "sacred_brazier": "Crafting: Black Basalt across the bottom row and both sides of the middle row, Coal in the middle, a Gold Ingot in each top corner",
    "khopesh": "Crafting: Gold Ingots in a curve (two on top, one below on the right) over a Stick",
}


def recipe_text(name):
    p = DATA / "recipe" / f"{name}.json"
    if not p.exists():
        return ""
    d = jread(p)
    names = lambda i: label(i if isinstance(i, str) else i.get("item", ""))
    if d["type"] == "minecraft:stonecutting":
        return f"Stonecutter, from {names(d['ingredient'])}"
    if d["type"] == "minecraft:crafting_shapeless":
        from collections import Counter
        c = Counter(names(i) for i in d["ingredients"])
        return "Shapeless: " + ", ".join(f"{n} ×{k}" if k > 1 else n for n, k in c.items())
    if name in RECIPE_TEXT:
        return RECIPE_TEXT[name]
    key = {k: names(v) for k, v in d.get("key", {}).items()}
    return "Crafting: " + " / ".join("".join(r) for r in d["pattern"]).replace(" ", "·") + "; " + ", ".join(f"{k} = {v}" for k, v in key.items())


# ---------- the data every page draws on ----------

def spawn_rules():
    src = (JAVA / "KhemetEntities.java").read_text()
    return {m.group(1): dict(weight=int(m.group(2)), lo=int(m.group(3)), hi=int(m.group(4)))
            for m in re.finditer(r"MobCategory\.MONSTER,\s*(\w+),\s*(\d+),\s*(\d+),\s*(\d+)\)", src)}


STAGES = CONTENT["favor"]["stages"]
GODS = [("ra", "ra_shrine", "Ra", "God of the Sun", "gods"), ("anubis", "anubis_shrine", "Anubis", "God of the Dead", "gods")]
STRUCTS = [
    ("ra_shrine", "The shrine of Ra", "A stepped limestone and golden-sandstone dais under a golden obelisk, with a gold-rimmed sun disc standing behind it, four golden pillars with braziers on top, and the altar of Ra in front.", ("ra-shrine", "ra-shrine-dusk")),
    ("anubis_shrine", "The shrine of Anubis", "A black-basalt court with a gold trim: two jackal statues in gold collars, four canopic jars, a sarcophagus of dark slabs, soul campfires at the corners, and the altar of Anubis. Mummies guard it.", ("anubis-shrine", "anubis-shrine-dusk")),
    ("obelisk_field", "The obelisk field", "Five obelisks of different heights on a pharaoh-stone floor drifted with sand: slender shafts of carved stone banded in gold, each capped with a golden pyramidion that gives light, and a small chest.", ("obelisk-field",)),
    ("desert_ruin", "The desert ruin", "A broken temple court: walls of weathered and cracked stone worn to different heights, lotus columns and golden pillars (some fallen), a painted wall of glyphs, a chest, and sand drifted in. Mummies haunt it.", ("desert-ruin",)),
]
CHEST_LABEL = {"ra_shrine": "Ra's shrine", "anubis_shrine": "Anubis's shrine", "obelisk_field": "an obelisk field", "desert_ruin": "a desert ruin"}
STONE_NOTES = {
    "ancient_limestone": "The everyday wall block: pale, seamed, a little worn.",
    "white_limestone": "Brighter limestone for temple faces and columns.",
    "golden_sandstone": "Banded gold sandstone for sun shrines and trim.",
    "black_basalt": "Dark flecked stone for the Black Land: tombs, and the jackal god's court.",
    "polished_pharaoh_stone": "Smooth, even stone with a worn edge, for floors and plinths.",
    "hieroglyph_stone": "Two rows of carved glyphs: ankh, wave, eye, bird, sun, reed, scarab.",
    "cracked_temple_stone": "Limestone split by one long crack, for ruins.",
    "weathered_pyramid_stone": "Mottled, eroded blocks for old pyramid faces.",
    "gold_inlaid_tile": "A pharaoh-stone tile with a gold cross inlaid.",
    "painted_temple_wall": "A painted band: gold, lapis and turquoise above, red bars below.",
    "hieroglyph_bricks": "Glyphs on bricks, offset like a real wall.",
    "obelisk_block": "Shaft stone with vertical inscriptions and gold ends.",
}


def n_structs():
    return len(list((DATA / "worldgen/structure_set").glob("*.json")))


def home_wall():
    panels = [
        ("gods", "Gods", "Ra & Anubis · " + str(len(STAGES)) + " stages", "Make an offering. Be named Chosen.", "gods.html", "panels/ra-shrine", "ra_altar"),
        ("structures", "Structures", f"{n_structs()} structures", "Found in deserts; one also in badlands.", "structures.html", "panels/anubis-shrine", "obelisk_block"),
        ("creatures", "Creatures", "2 mummies", "Wrapped in linen, with glowing eyes.", "creatures.html", "panels/mummies", "mummy-face"),
        ("blocks", "Blocks", f"{len(block_ids())} blocks", "Limestone, gold, basalt and glyphs.", "blocks.html", "panels/blocks", "hieroglyph_stone"),
        ("potions", "Potions", f"{len(POTIONS)} potions · 2 plants", "Lotus, papyrus and five brews.", "potions.html", "panels/plants", "blue_lotus"),
        ("relics", "Relics", "2 relics · sandstorms", "An ankh and a khopesh, shown large.", "relics.html", "panels/relics", "ankh"),
    ]
    items = ""
    for hue, name, figure, claim, href, img, icon in panels:
        items += (f'<li><a class="panel" style="--hue:var(--{hue})" href="/{href}"><img class="ph" src="/img/{img}.jpg" width="640" height="320" alt="" loading="eager">'
                  f'<span class="pn"><span class="name"><img src="/img/tex/{icon}.png" alt="" width="22" height="22">{esc(name)}</span>'
                  f'<span class="fig">{esc(figure)}</span><span class="claim">{esc(claim)}</span></span></a></li>')
    return f"""
<section class="wall" aria-labelledby="h1">
  <div class="cartouche"><h1 id="h1">Khemet</h1><p class="sub">Sands of the ancient gods. A Minecraft mod<span class="more">: shrines, mummies, obelisks, and the favor of Ra and Anubis</span><span class="dot">.</span></p><a class="btn" href="/install.html">Build &amp; install</a></div>
  <ul class="panels">{items}</ul>
  <p class="meta wallnote">Real in-game photos from a flat test world; the sand and sky are vanilla.</p>
</section>"""


def favor_ladder():
    li = "".join(f"<li><b>{s['at']}</b><span>{esc(s['name'])}</span></li>" for s in STAGES)
    return f'<ol class="ladder" aria-label="Divine favor stages by points">{li}</ol>'


def build_index():
    tested = len(list((SITE / "img/shots").glob("*.png")))
    body = home_wall() + f"""
<section class="page">
  <p class="lede">Khemet is the Egyptian sibling of the Asgard mod: the same stack and the same ideas (shrines, offerings, relics, creatures, ancient structures), with a different land. This is slice one of a much larger <a href="https://github.com/SolutionsAsService/minecraft-khemet/blob/main/design/master-prompt.md">design</a>.</p>
  <p class="action"><a class="btn" href="/gods.html">Meet the gods</a> <a class="btn btn-alt" href="/install.html">Install</a> <a class="btn btn-quiet" href="/structures.html">Find a shrine</a></p>
  <h2>New here?</h2>
  <dl class="gloss">
    <dt>Khemet</dt><dd>Kemet, \u201cthe Black Land\u201d, is what the ancient Egyptians called their own country: the dark, fertile silt the Nile left each year. The desert beyond it was Deshret, \u201cthe Red Land\u201d.</dd>
    <dt>A Minecraft mod</dt><dd>An add-on that changes the game. This one adds new blocks, plants, potions, creatures and buildings.</dd>
    <dt>A shrine and an altar</dt><dd>A shrine is a building for a god. Its altar is a block: you hold an offering (say, a gold ingot) and use it, and the god gives you a blessing.</dd>
    <dt>Favor</dt><dd>A score each god keeps for you. More offerings, more favor, stronger blessings.</dd>
  </dl>
  <h2>Divine favor</h2>
  <p>Each god takes offerings at its altar. Every offering adds favor, and favor moves you up four stages; each stage adds a blessing.</p>
  {favor_ladder()}
  <p class="meta">The points are the thresholds in the mod's own data file.</p>
  {status(["The mod loads on a Fabric server with no data errors.", "All four structures generate on their own in a desert world, and the game's /locate finds them.",
           "Favor, the stage thresholds and the blessings work through the same code the altars use.", "The sandstorm slows a player in the open and not under a roof."],
          ["Using an altar by hand (the same code path was tested through a command).", "Brewing the potions.", "The Ankh and the Khopesh in play.", "A sandstorm starting on its own.", "Mummies spawning on their own."])}
</section>"""
    return page("Khemet: Egyptian gods, shrines and mummies for Minecraft", "A Minecraft mod: Egyptian stone and plants, five divine potions, the shrines of Ra and Anubis with offerings and divine favor, four desert structures, mummies and sandstorms.", body, "home", "index.html", None)


def build_blocks():
    cards = ""
    for n in stone_order():
        cards += f'<li class="card">{sprite(n, 64, LANG["block.khemet." + n])}<div><h3>{esc(LANG["block.khemet." + n])}</h3><p>{esc(STONE_NOTES[n])}</p><p>{esc(recipe_text(n + "_from_stonecutting"))}</p></div></li>'
    others = [("golden_pillar", "A pillar: place it upright or on its side. Gold bands and a gold ring on the end."), ("lotus_column", "A white column with a turquoise lotus capital and a lapis band."),
              ("sacred_brazier", "A bowl of fire in a black-and-gold stand. Light level 14, with flame and smoke.")]
    oc = "".join(f'<li class="card">{sprite(n, 64, LANG["block." + "khemet." + n])}<div><h3>{esc(LANG["block.khemet." + n])}</h3><p>{esc(t)}</p><p>{esc(recipe_text(n))}</p></div></li>' for n, t in others)
    body = f"""
<section class="page">
  <p class="eyebrow">Blocks</p><h1>Stone for the Black Land</h1><div class="rule"></div>
  <p class="lede">Twelve building stones, two pillars and a brazier, all drawn for the mod. Every stone can be cut from sandstone at a stonecutter (the table below says from what).</p>
  <div class="shots two">{fig("blocks", "The twelve stones in a row, with the pillars, the brazier and the two altars behind.", "Twelve Egyptian building blocks in a row on desert sand: cream, white, gold, black, patterned and hieroglyph-carved stones")}{fig("blocks-dusk", "The same row at dusk.", "The same twelve blocks at dusk under a darkening sky")}</div>
  <h2>The twelve stones</h2><ul class="cards">{cards}</ul>
  <h2>Pillars and the brazier</h2><ul class="cards">{oc}</ul>
  <p class="meta">The two altars (Ra and Anubis) are on the <a href="/gods.html">Gods</a> page.</p>
  {status(["Every block loads, shows its own texture, and its item shows in the inventory and tab.", "The blocks in these photographs were placed in the game and photographed from a client."],
          ["Mining speeds and tool requirements.", "The stonecutter and crafting recipes were checked by the generator's linter, not by crafting them in play."])}
</section>"""
    return page("Blocks: Egyptian limestone, gold and basalt", "The twelve Egyptian building stones, the Golden Pillar, the Lotus Column and the Sacred Brazier in the Khemet mod.", body, "blocks", "blocks.html", "blocks")


def build_potions():
    where = {}
    for slug in ("ra_shrine", "anubis_shrine", "obelisk_field", "desert_ruin"):
        for it in chest_items(slug):
            where.setdefault(it, []).append(CHEST_LABEL[slug])
    rows = ""
    for p in POTIONS:
        ing = p["ingredient"].replace("_", " ").title()
        found = ", ".join(where.get(ing, [])) or "only by crafting or other drops"
        rows += (f'<li class="card">{sprite("item-" + p["ingredient"], 64, ing)}<div><h3>{esc(p["name"])}</h3><p>{esc(p["god"])}, {esc(p["epithet"])}. '
                 f'{" ".join(esc(fx(e)) + "." for e in p["effects"])}</p><p>Brew an Awkward Potion with {esc(ing)}. Found in {esc(found)}.</p><p>{esc(p["lore"])}</p></div></li>')
    plants = (f'<li class="card">{sprite("blue_lotus", 64, "Blue Lotus")}<div><h3>Blue Lotus</h3><p>A river flower that glows faintly (light level 3). Grows on sand, dirt, clay or sandstone. Craft two Lotus Columns from it and two white limestone.</p></div></li>'
              f'<li class="card">{sprite("papyrus", 64, "Papyrus")}<div><h3>Papyrus</h3><p>A tall reed with a feathered head, for river banks and oases. Grows on sand, dirt, clay or sandstone. A stand of papyrus turns up in the desert ruins’ chests.</p></div></li>')
    body = f"""
<section class="page">
  <p class="eyebrow">Plants &amp; potions</p><h1>Lotus, papyrus and five brews</h1><div class="rule"></div>
  <p class="lede">Two river plants and five divine potions, each brewed from an Awkward Potion and one ingredient found in the desert structures.</p>
  <div class="shots two">{fig("plants", "Blue lotus and papyrus on sand, in front of the altars of Ra and Anubis, a brazier and a lotus column.", "Blue lotus and papyrus plants on desert sand")}{fig("relics", "Blood of Ra, held large, beside the Ankh and the Khopesh.", "A Blood of Ra potion shown large beside two relics")}</div>
  <h2>Plants</h2><ul class="cards">{plants}</ul>
  <h2>The five potions</h2><ul class="cards">{rows}</ul>
  <p class="meta">The potions use the same data format as Asgard's: one entry in <code>potions.json</code> adds an ingredient, a potion and a brewing recipe.</p>
  {status(["The five potions and their ingredient items load, with names and lore, and the recipes register.", "The plants render with transparent backgrounds after a cutout fix, and are placed in the photograph."],
          ["Brewing, drinking or splashing the potions in play.", "Planting the lotus and papyrus by hand (the placement rule is in the code)."])}
</section>"""
    return page("Plants & potions: lotus, papyrus and five brews", "Blue lotus, papyrus and the five divine potions of the Khemet mod: Blood of Ra, Tears of Isis, Breath of Horus, Anubis's Veil and Bastet's Grace.", body, "potions", "potions.html", "potions")


def blessing_rows(god):
    rows = ""
    for b in CONTENT["gods"][god]["blessings"]:
        eff = ", ".join(f"{EFFECT.get(e[0], label(e[0]))} {roman(e[2] + 1)} for {dur(e[1])}" for e in b["effects"])
        rows += f'<tr><th scope="row">{esc(STAGES[b["stage"]]["name"])}</th><td>{esc(eff)}</td></tr>'
    return rows


def build_gods():
    secs = ""
    for god, slug, name, title, hue in GODS:
        g = CONTENT["gods"][god]
        off = "".join(f"<tr><th scope=\"row\">{esc(label(o['item']))}</th><td>{o['favor']} favor</td></tr>" for o in g["offerings"])
        secs += f"""<section class="sec" id="{god}"><p class="eyebrow">{esc(title)}</p><h2>{esc(name)}</h2>
  <div class="shots two">{fig(slug.replace('_', '-'), name + "'s shrine by day.", name + "'s shrine in a desert")}{fig(slug.replace('_', '-') + "-dusk", name + "'s shrine at dusk.", name + "'s shrine at dusk")}</div>
  <table class="data"><caption class="sr">{esc(name)}: offerings</caption><tbody>{off}</tbody></table>
  <p>Blessings: each stage adds to the ones before it, so a Chosen worshipper gets all of them.</p>
  <table class="data"><caption class="sr">{esc(name)}: blessings by stage</caption><tbody>{blessing_rows(god)}</tbody></table></section>"""
    body = f"""
<section class="page">
  <p class="eyebrow">Gods</p><h1>Ra and Anubis</h1><div class="rule"></div>
  <p class="meta">The gods here are game material: a simplified retelling for a Minecraft mod, made with respect for the ancient Egyptian world it draws on, and not a statement about religion.</p>
  <p class="lede">Each god has a shrine and an altar. Hold an offering, use the altar, and the god takes one item, adds to your favor, and gives you a blessing. Favor is saved with you, and kept through death.</p>
  <h2>Favor</h2>{favor_ladder()}
  <p>Use an altar with an empty hand to see your favor and what the god wants. <code>/khemet favor</code> lists your standing with every god.</p>
  {secs}
  <p class="meta">Seven more gods are in the design (Horus, Isis, Osiris, Set, Bastet, Thoth, Khonsu); slice one has two.</p>
  {status(["Offering, refusal of the wrong item, favor kept per god, and all four stage names (Ra reached Chosen at 25 favor), through the command that runs the same code as the altar.", "The blessings stack by stage: at Recognized, Ra gave Fire Resistance and Strength; at Favored, Regeneration and Resistance joined them; at Chosen (28 favor) Regeneration II, Fire Resistance and a longer Strength were active.", "Both shrines generate on their own and are photographed."],
          ["Using an altar block with a held item (the click path).", "Favor kept across a server restart (it is saved with the player; not yet restarted to check).", "Anubis's blessings and his stages beyond Stranger were not individually inspected."])}
</section>"""
    return page("Gods: the shrines and favor of Ra and Anubis", "Ra and Anubis in the Khemet mod: their altars, offerings, four stages of divine favor and the blessings each stage gives.", body, "gods", "gods.html", "gods")


def build_structures():
    secs = ""
    for slug, title, blurb, shots in STRUCTS:
        (sx, sy, sz), nblocks = nbt_size(slug + "_0")
        sset = jread(DATA / "worldgen/structure_set" / f"{slug}.json")["placement"]
        biomes = ", ".join(b.replace("#minecraft:is_", "").replace("minecraft:", "") for b in jread(DATA / "tags/worldgen/biome/has_structure" / f"{slug}.json")["values"])
        spawns = jread(DATA / "worldgen/structure" / f"{slug}.json").get("spawn_overrides", {})
        sp = ", ".join(f"{label(s['type'])} ({s['minCount'] if s['minCount'] == s['maxCount'] else str(s['minCount']) + ' to ' + str(s['maxCount'])})" for c in spawns.values() for s in c["spawns"]) or "none"
        sp = (sp + ". Set in the structure's data; not yet watched in play.") if sp != "none" else sp
        figs = "".join(fig(n, title + (" at dusk." if n.endswith("dusk") else " by day."), title + (" at dusk, under an orange sky" if n.endswith("dusk") else " by day, on desert sand")) for n in shots)
        secs += f"""<section class="sec" id="{slug}"><h2>{esc(title)}</h2><p>{esc(blurb)}</p><div class="shots two">{figs}</div>
  <table class="data"><caption class="sr">{esc(title)}: facts</caption><tbody>
  <tr><th scope="row">Size</th><td>{sx} by {sz} blocks, {sy} high; {variants(slug)} variants</td></tr>
  <tr><th scope="row">Spacing</th><td>One in every {sset['spacing']} by {sset['spacing']} chunks</td></tr>
  <tr><th scope="row">Biomes</th><td>{esc(biomes)}</td></tr>
  <tr><th scope="row">Guardians</th><td>{esc(sp)}</td></tr>
  <tr><th scope="row">Chest</th><td>{esc(", ".join(chest_items(slug)))}</td></tr></tbody></table></section>"""
    body = f"""
<section class="page">
  <p class="eyebrow">Structures</p><h1>Four things in the sand</h1><div class="rule"></div>
  <p class="lede">The desert hides two shrines, an obelisk field and a ruin. Each is a template with a few variants, generated by the game where the biome allows, with a chest of themed loot.</p>
  {secs}
  {status(["All four generate on their own in a desert world: the game's /locate found each one, from 16 to 417 blocks away.", "All four were also placed with the template command and photographed from a client."],
          ["How they sit among vanilla desert structures (a flat test world has none).", "Pyramids, the Sphinx and temples are not in this slice."])}
</section>"""
    return page("Structures: shrines, obelisks and ruins in the desert", "The four desert structures of the Khemet mod: the shrines of Ra and Anubis, the obelisk field and the desert ruin.", body, "structures", "structures.html", "structures")


def guard_list(key):
    out = []
    for slug, title, *_ in STRUCTS:
        spawns = jread(DATA / "worldgen/structure" / f"{slug}.json").get("spawn_overrides", {})
        if any(s["type"] == f"khemet:{key}" for c in spawns.values() for s in c["spawns"]):
            out.append(title.replace("The ", "the ", 1))
    return out


def chance_of(path, item):
    for pool in jread(path)["pools"]:
        for e in pool["entries"]:
            if e.get("name") == item:
                for c in pool.get("conditions", []):
                    if c.get("condition") == "minecraft:random_chance":
                        return round(c["chance"] * 100)
    return None


ANKH_RA = chance_of(DATA / "loot_table/chests/ra_shrine.json", "khemet:ankh")
ANKH_ROY = chance_of(DATA / "loot_table/entities/royal_mummy.json", "khemet:ankh")
KHOP = chance_of(DATA / "loot_table/chests/anubis_shrine.json", "khemet:khopesh")


def build_creatures():
    m = java_attrs("Mummy")
    r = {**m, **java_attrs("RoyalMummy")}
    sp = spawn_rules()
    cards = ""
    for key, name, a, blurb, shotn in (("mummy", "Mummy", m, "A tomb guardian wrapped in linen with glowing amber eyes. As written in the code (not yet seen in a fight): slow and durable, its touch leaves a 10-second Weakness, and dry linen burns twice as hard, so fire does double damage. It does not burn in sunlight.", "mummies"),
                                       ("royal_mummy", "Royal Mummy", r, "An elite mummy from a royal burial, in a striped headdress, a collar of gold and turquoise and gold armour. More health, harder hits, and better drops, including a {ANKH_ROY}% chance at an Ankh (from the loot table).".replace("{ANKH_ROY}", str(ANKH_ROY)) + "", None)):
        rule = sp.get(key.upper())
        guards = guard_list(key)
        count = "singly" if rule and rule["lo"] == rule["hi"] else (f"{rule['lo']} to {rule['hi']} at a time" if rule else "")
        spawn = (f"Deserts: {count}, spawn weight {rule['weight']}. Set to guard " + (" and ".join(guards) if guards else "nothing else") + " (in the data; not yet watched).") if rule else ""
        loot = ", ".join(label(e["name"]) for pool in jread(DATA / "loot_table/entities" / f"{key}.json")["pools"] for e in pool["entries"] if e.get("type") == "minecraft:item")
        cards += f"""<section class="sec" id="{key}"><h2>{name}</h2><p>{esc(blurb)}</p>{fig(shotn, "A pair of mummies and a royal mummy, in a desert test world with their AI off for the photograph.", "Two mummies and a royal mummy standing on desert sand") if shotn else ""}
  <table class="data"><caption class="sr">{name}: facts</caption><tbody>
  <tr><th scope="row">Stats</th><td>{a['health']:g} health ({a['health'] / 2:g} hearts), {a['damage']:g} attack damage, {a['armour']:g} armour{(', knockback resistance ' + format(a['knockback'], 'g')) if 'knockback' in a else ''}</td></tr>
  <tr><th scope="row">Spawns</th><td>{esc(spawn)}</td></tr>
  <tr><th scope="row">Drops</th><td>{esc(loot)}</td></tr>
  <tr><th scope="row">Spawn egg</th><td>In the Spawn Eggs tab, and <code>/summon khemet:{key}</code></td></tr></tbody></table></section>"""
    body = f"""
<section class="page">
  <p class="eyebrow">Creatures</p><h1>The wrapped guardians</h1><div class="rule"></div>
  <p class="lede">The first two creatures of the design's Phase 3. They use the zombie model with skins painted for the mod.</p>
  {cards}
  {status(["Both load, render with their skins (wrapped linen, glowing eyes; the royal mummy in gold) and are summoned and photographed.", "The stats are the ones in the code, read at build time."],
          ["Mummies spawning on their own over a night in a desert.", "The Weakness touch and the double fire damage in a fight.", "Their drops (the table is written, not yet watched).", "Custom models and animations: they reuse the zombie's."])}
</section>"""
    return page("Creatures: mummies and royal mummies", "The mummy and the royal mummy of the Khemet mod: stats, spawns, drops and what they do.", body, "creatures", "creatures.html", "creatures")


def build_relics():
    a, k, s = CONTENT["ankh"], CONTENT["khopesh"], CONTENT["sandstorm"]
    per_min = s["chance_in"] * 10 / 60
    body = f"""
<section class="page">
  <p class="eyebrow">Relics &amp; weather</p><h1>An ankh, a khopesh, and a storm</h1><div class="rule"></div>
  <div class="shots two">{fig("relics", "The Ankh of Life and Anubis's Khopesh, shown large with a Blood of Ra potion.", "The ankh, the khopesh and a potion shown at display size")}{fig("sandstorm", "A sandstorm at the edge of the desert: wind-blown sand (this capture shows only a few particles).", "A few blown sand particles over a desert")}</div>
  <h2>Relics</h2>
  <p class="meta">The numbers here are as written in the code; neither relic has been used in play yet.</p>
  <ul class="cards"><li class="card">{sprite("ankh", 64, "Ankh of Life")}<div><h3>Ankh of Life</h3><p>Use it to heal {a['heal'] / 2:g} hearts at once and then regenerate ({roman(a['regen_amplifier'] + 1)}, {a['regen_seconds']} seconds). It also clears poison and wither. It wears out after {a['durability']} uses and needs {a['cooldown_ticks'] // 20} seconds between uses. At full health it does nothing, unless you are poisoned or withered.</p><p>{esc(recipe_text('ankh'))}. Found in {ANKH_RA}% of Ra's shrine chests, and dropped by {ANKH_ROY}% of royal mummies.</p></div></li>
  <li class="card">{sprite("khopesh", 64, "Anubis's Khopesh")}<div><h3>Anubis's Khopesh</h3><p>A curved sword: +{k['damage']:g} attack damage ({k['damage'] + 1:g} with a bare hand's 1) at {4 + k['attack_speed_modifier']:g} swings per second, {k['durability']} durability, and {k['undead_bonus']:g} extra magic damage to the undead.</p><p>{esc(recipe_text('khopesh'))}. Found in {KHOP}% of Anubis's shrine chests.</p></div></li></ul>
  <h2>Sandstorms</h2>
  <p>As written in the code (a sandstorm has been started with the command, but not yet seen to start by itself): in daytime, in clear weather, there is a 1 in {s['chance_in']} chance every 10 seconds (about once every {per_min:.0f} minutes) that a sandstorm starts if any player is in a desert. It lasts {s['duration_seconds'] // 60}:{s['duration_seconds'] % 60:02d}. Anyone in a desert or badlands under open sky is slowed ({'Slowness ' + roman(s['slowness_amplifier'] + 1)}) and blown with sand; stand under a roof and nothing happens. Operators can start and stop one with <code>/khemet sandstorm start</code> and <code>stop</code>.</p>
  {status(["The Ankh and the Khopesh load, show their icons, and are photographed at display size.", "A sandstorm applied Slowness to a player in the open, and none under a roof (measured on the player's effects)."],
          ["Using the Ankh, and the Khopesh's undead bonus, in play.", "A sandstorm starting on its own (it has been started with the command).", "Sandstorm visuals: the particles are sparse, as the photograph shows, and the sky does not darken."])}
</section>"""
    return page("Relics & weather: the Ankh, the Khopesh and sandstorms", "The Ankh of Life, Anubis's Khopesh and the desert sandstorm of the Khemet mod, with their numbers.", body, "relics", "relics.html", "relics")


def build_install():
    mf = jread(REPO / "shadw.mod.json")
    body = f"""
<section class="page">
  <p class="eyebrow">Install</p><h1>Install Khemet</h1><div class="rule"></div>
  <p class="lede">Khemet is a Fabric mod for Minecraft {esc(mf['game_versions'][0])}. No release jar is published yet, so you build it.</p>
  <p class="meta">Words used here: a <b>mod</b> is an add-on for the game; a <b>jar</b> is the mod\u2019s file; <b>Fabric</b> is the program that loads mods; an <b>operator</b> is a player allowed to use admin commands.</p>
  <h2>You need</h2><ul><li>Minecraft Java Edition {esc(mf['game_versions'][0])} (not Bedrock)</li><li><a href="https://fabricmc.net">Fabric</a> Loader 0.16 or later, and Fabric API</li><li>Java 21 and Gradle 8 (the repository has no Gradle wrapper)</li></ul>
  <h2>Build</h2>
  <pre><code>git clone https://github.com/SolutionsAsService/minecraft-khemet
cd minecraft-khemet
gradle build
# the jar is in build/libs/khemet-{esc(mf['version'])}.jar</code></pre>
  <p>Copy the jar into your <code>mods</code> folder and start the game. The server log line <code>Khemet loaded: 5 potions, 5 brewing recipes, 0 unknown effects skipped; {len(block_ids())} blocks, 2 gods, 2 creatures</code> confirms the registration.</p>
  <h2>Commands</h2>
  <table class="data"><caption class="sr">Commands</caption><tbody><tr><th scope="row"><code>/khemet favor</code></th><td>Your favor and stage with each god.</td></tr>
  <tr><th scope="row"><code>/khemet offer &lt;god&gt;</code></th><td>Operators: offer the item in your hand to a god (the same code the altar runs).</td></tr>
  <tr><th scope="row"><code>/khemet sandstorm start|stop</code></th><td>Operators: start or stop a sandstorm.</td></tr></tbody></table>
  {status(["Builds on Fabric Loom 1.11.8 and Gradle 8, and loads on a Fabric 1.21.4 dedicated server; a client joined and rendered every page of photographs here."],
          ["Other platforms and mods: it is built and tried only on Fabric 1.21.4 with Fabric API.", "A published release jar."])}
</section>"""
    return page("Install Khemet", "How to build and install the Khemet Minecraft mod.", body, "install", "install.html", None)


# ---------- assets and the build ----------

def convert(*args):
    return subprocess.run(["convert", *map(str, args)], capture_output=True).returncode == 0


def prepare_assets():
    tex = SITE / "img/tex"
    shutil.rmtree(tex, ignore_errors=True)
    tex.mkdir(parents=True, exist_ok=True)
    pick = {"sacred_brazier": "sacred_brazier_top", "ra_altar": "ra_altar_top", "anubis_altar": "anubis_altar_top"}
    for n in block_ids():
        src = ASSETS / "textures/block" / f"{pick.get(n, n)}.png"
        if src.exists():
            shutil.copyfile(src, tex / f"{n}.png")
    for p in POTIONS:
        shutil.copyfile(ASSETS / "textures/item" / f"{p['ingredient']}.png", tex / f"item-{p['ingredient']}.png")
    for n in ("ankh", "khopesh"):
        shutil.copyfile(ASSETS / "textures/item" / f"{n}.png", tex / f"{n}.png")
    convert(ASSETS / "textures/entity/mummy.png", "-crop", "8x8+8+8", "+repage", "-filter", "point", "-resize", "88x88", tex / "mummy-face.png")
    panels = SITE / "img/panels"
    shutil.rmtree(panels, ignore_errors=True)
    panels.mkdir(parents=True, exist_ok=True)
    for name in ("ra-shrine", "anubis-shrine", "mummies", "blocks", "plants", "relics"):
        src = SITE / "img/shots" / f"{name}.png"
        if src.exists():
            convert(src, "-resize", "640x320^", "-gravity", "center", "-extent", "640x320", "-quality", "80", panels / f"{name}.jpg")
        else:
            raise SystemExit(f"missing photograph for the landing: {src}")
    og = SITE / "img/og.png"
    ok = convert(SITE / "img/shots/ra-shrine.png", "-resize", "1200x630^", "-gravity", "center", "-extent", "1200x630", "-fill", "#14110FD0",
                 "-draw", "rectangle 0,430 1200,630", "-fill", TEXT, "-pointsize", "92", "-gravity", "southwest", "-annotate", "+48+86", "KHEMET",
                 "-fill", SIGNAL, "-pointsize", "34", "-annotate", "+52+36", "Sands of the ancient gods · a Minecraft mod", og)
    if not ok:
        shutil.copyfile(SITE / "img/shots/ra-shrine.png", og)
    (SITE / "img/icon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect width="16" height="16" fill="{GROUND}"/>'
                                       f'<circle cx="8" cy="4.6" r="2.9" fill="none" stroke="{SIGNAL}" stroke-width="1.6"/><rect x="7" y="7.5" width="2" height="7.5" fill="{SIGNAL}"/>'
                                       f'<rect x="3" y="9" width="10" height="1.8" fill="{SIGNAL}"/></svg>\n')


def write(rel, text):
    path = SITE / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    palette = check_palette()
    check_deploy()
    prepare_assets()
    write("style.css", css())
    for rel, fn in (("index.html", build_index), ("blocks.html", build_blocks), ("potions.html", build_potions), ("gods.html", build_gods),
                    ("structures.html", build_structures), ("creatures.html", build_creatures), ("relics.html", build_relics), ("install.html", build_install)):
        write(rel, fn())
    weight = {p.name: p.stat().st_size for p in (SITE / "img/panels").glob("*.jpg")}
    print(f"site written: {len(list(SITE.glob('*.html')))} pages; palette min delta-E {palette['min_delta_e']} ({palette['min_pair']}); "
          f"min hue contrast {palette['min_contrast']}; first-screen images {sum(weight.values()) // 1024} KB over {len(weight)} files, largest {max(weight.values()) // 1024} KB")


if __name__ == "__main__":
    main()
