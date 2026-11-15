Anchor used: Cairo, How Charts Lie: every printed figure must be reproducible from its source, and omission misleads like a wrong number.

Observed: Wall bottom (caption inside, seen in 375 shot) 733.8 of 800 at 1280 and 752.1 of 812 at 375; scrollWidth equals clientWidth at both, so no sideways scroll. Fixture (1400px by 600px div at 375) reads bottom 1408, scrollWidth 608 over 375, so the probe does fail on a bad page. Recomputed from content.json, loot_table, structure, structure_set and the .nbt sizes: all stats, drops, weights (12 and 1), counts (2-3, 1, 1-2), spacings, sizes, variants, card counts (19, 5, 4 stages), sandstorm (1/90 per 200 ticks, 150 s, Slowness I) and Ankh numbers (8 hp, 10 s, 30 s, 32, 30%, 4%) match.

Findings:
F1 [claim] Home Structures card says "Found in deserts and badlands"; only Anubis (tag has #is_badlands) does. Ra, obelisk and ruin are desert-only. Reopens R1 badlands finding as an overcorrection.
F2 [claim] Relics: Khopesh "Also found in Anubis's shrine" hides its 30% chest chance (anubis_shrine.json), the same omission as R1 Ankh.
F3 [claim] Ankh "does nothing at full health" is false when poisoned or withered (AnkhItem.java:22): it cures and spends a use.
F4 [closed] Royal Mummy guards the shrine only; "1 to 3 at a time" is correct; Ankh chances shown.

Verdict: OBJECT

One change: reword the home card to "Four sites; one reaches badlands", and give the Khopesh its 30%.
