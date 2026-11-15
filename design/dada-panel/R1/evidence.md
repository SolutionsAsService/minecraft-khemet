# Evidence file, Khemet site, round R1 (whole artifact, rendered)

Artifact: /home/user/minecraft-khemet/site (8 static pages, built by _src/build_site.py), served at http://127.0.0.1:8098/<page>.html.
Pages: index, blocks, potions, gods, structures, creatures, relics, install. Mode Adaptive, run type Full with Landing rules.
Screenshots (open them): /tmp/claude-0/-home-user/43a5318b-9e73-5f11-bea4-51a56a726ae4/scratchpad/
  kh-desktop-home.png (1280x800 first screen), kh-phone-home.png (375x812 first screen),
  kh-phone-375-<page>.png and kh-wide-1280-<page>.png (full-page, for blocks potions gods structures creatures relics install).
In-game photographs the site uses: /home/user/minecraft-khemet/site/img/shots/*.png (real captures from a Minecraft 1.21.4 client in a flat desert test world).

## Measured (Playwright, after the last build)
- First-screen rule: desktop wall (the landing figure) bottom edge 704 px of 800; phone 710 px of 812; no sideways scroll at either size.
- Mobile floor, all 8 pages at 375 and 1280: no horizontal scroll; no text under 12 px; smallest standalone tap target 44 px; no broken image; one h1 per page.
  (DADA's check_floor.py could not run: its tools/measure.py is not installed here. Playwright measurements stand in.)
- Palette (printed by the build, which fails below these): minimum pairwise CIE76 delta-E 44.9 (gods/relics) over 6 category hues + the gold signal; every hue >= 5.24:1 on the page ground and card; body text >= 4.5:1. Hues: blocks #D8CCAA limestone, gods #6A9BEA Egyptian blue, structures #E4685F red ochre, potions #86C24F malachite, creatures #35C4B6 faience, relics #DE86C6 amethyst; signal #EDBE3A; ground #14110F (Kemet, the Black Land).
- First-screen weight: six panel JPEGs 169 KB total, largest 34 KB.
- Deploy files (root and inner vercel.json, fluid.json, root redirect, anchored .vercelignore) are checked by the build, which passed.

## What the mod verifiably did (source: scratchpad/pt-khemet.out and the retests; the project log)
- Loaded on a Fabric 1.21.4 dedicated server: "Khemet loaded: 5 potions, 5 brewing recipes, 0 unknown effects skipped; 19 blocks, 2 gods, 2 creatures"; log check: no data errors.
- Natural generation: in a desert flat world /locate found all four structures (nearest 16, 229, 417, 257 blocks in one run; 164, 323, 164, 288 in another).
- Favor through `/khemet offer` (same code as the altar): 3 gold ingots to Ra -> favor 3 "Recognized"; a stick was refused; bones to Anubis -> favor 1; 13 favor -> "Favored".
- Blessings (data get entity active_effects): at Recognized Fire Resistance + Strength; at Favored Regeneration + Resistance added.
- Sandstorm: started by command, Slowness applied to a player in the open; none under a stone roof.
- NOT tested: using an altar by hand; brewing; the Ankh and Khopesh in play; a sandstorm starting on its own; mummy fire/weakness in a fight; favor across a restart.

## Known weaknesses the conductor already sees (disclosed, not hidden)
- The sandstorm photograph shows only a few sand particles; the sky does not darken. The Relics page says so.
- Dark theme only; no light theme (out of scope for slice one).
- The landing wall puts six photographs on one 3x2 grid (2x3 on phones). Gold is reserved for links and buttons.
- The panel is bounded: six of the eight picked seats (Shklovsky and Garland not seated), because earlier runs in this session hit agent rate limits.
