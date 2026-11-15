# Evidence file, Khemet site, round R2 (the artifact after move M5, which answered round R1)

Artifact: /home/user/minecraft-khemet/site (8 pages), served at http://127.0.0.1:8098/<page>.html. Screenshots (open them, they are fresh):
/tmp/claude-0/-home-user/43a5318b-9e73-5f11-bea4-51a56a726ae4/scratchpad/ kh-desktop-home.png, kh-phone-home.png, kh-phone-375-<page>.png, kh-wide-1280-<page>.png.
Round R1's six reports and the resolutions table are in /home/user/minecraft-khemet/DESIGN-LOG.md ("Panel Reports", "Resolutions, round R1").

## What changed in M5 (every row answers an R1 finding)
Nav labels shortened (two rows on phone); one-word panel names with an arrow each; Gods figure now "Ra & Anubis . 4 stages"; a gold Install button beside the title;
"A Minecraft mod" kept on the phone tagline; a one-line caption under the wall (real in-game photos from a flat test world, sand and sky vanilla);
a "New here?" glossary (Khemet, mod, shrine and altar, favor); a respect line on the Gods page; Install page glossary line; recipes as sentences;
untested behaviour now worded "as written in the code (not yet tried / seen in play)"; the Royal Mummy guard list, Ankh chances (30% of Ra chests, 4% royal mummy) and
mummy counts are computed from the data/loot files; Anubis shrine biomes stated (deserts and badlands); distinct dusk alt texts; one serif variable, lining and tabular figures;
the six-hue frieze replaced by a single-hue gold ruled band; the cartouche bar removed; a forced-colors block; a visible focus ring on every control.

## Measured after M5 (Playwright)
- First-screen rule, with the caption inside the wall: desktop wall bottom 734 of 800 (panels end 696); phone 752 of 812 (panels end 694); no sideways scroll at either size.
- Mobile floor, 8 pages x 375 and 1280 = 16 rows: all clean (no horizontal scroll, no text under 12 px, smallest standalone target 44 px, no broken image, one h1). check_floor.py could not run here (its tools/measure.py is missing).
- Real Tab presses on the home page: skip link, brand, each nav link, the Install button and the first panel each show a 3px solid outline (black on the gold skip link, limestone elsewhere).
- Straight apostrophes between letters in prose (outside code/pre/style): 0 across the 8 pages.
- Palette unchanged: min delta-E 44.9 (gods/relics), every hue >= 5.24:1 on ground and card.
- Install facts: fabric.mod.json depends on fabricloader >=0.16.0 and fabric-api; gradle.properties has loom_version=1.11.8, minecraft 1.21.4, mod_version=0.1.0 (jar name khemet-0.1.0.jar).

## Measured in the game since R1
- Ra's favor reached 28 "Chosen" through the command that runs the altar's code; active_effects then listed Regeneration II, Fire Resistance and a longer Strength.
- Natural generation of all four structures by /locate in a desert world (earlier).

## Still true and disclosed
Not tested in play: using an altar by hand, brewing, the Ankh and Khopesh, a sandstorm starting on its own, mummies spawning or fighting, favor across a restart. The sandstorm photograph is sparse and the Relics page says so.
DEFERRED with reasons: a light theme; translations (both out of scope for slice one; the footer says "Dark theme only. English only.").

## Added after the first R2 batch (move M6 and the S4 push), measured
- M6 answers Krug's and Cairo's R2 findings: the button reads "Build & install"; the home Structures card says "Found in deserts; one also in badlands." (only Anubis's tag includes badlands); the Khopesh's 30% chest chance (anubis_shrine loot table) is printed; the Ankh text now matches AnkhItem.java (it cures poison and wither, so it works at full health if you are poisoned or withered).
- S4 push (escalating the landing wall): desktop panel photographs 166 px -> 189 px tall (+14%), wall bottom edge 734 -> 781 of 800; phone unchanged, wall bottom 752 of 812; no sideways scroll at either size; floor 16 of 16 clean after M6.
- Round R2 verdicts so far: Mace PASS; Krug and Cairo OBJECT with the findings M6 answers. Debord and Bringhurst are seated now on this final state.
