Critic: Evidence (Cairo), R1

- Anchor used: Cairo, How Charts Lie. A printed figure is honest only if a reader can rebuild it from the source.
- Observed (Playwright, my run):
  - Landing wall bottom edge is 704 px of 800 at 1280 and 710 px of 812 at 375. scrollWidth equals the viewport at both sizes, and also on gods and creatures. One h1 on each.
  - Recomputed against content.json and potions.json: every blessing duration and tier on Gods (Ra and Anubis, 8 effects per god); the 3/10/25 thresholds; the offering favors; all 5 potions (Isis II 0:45, Horus Speed II 3:00, Bastet Luck II 5:00); Ankh (8.0 = 4 hearts, 600 ticks = 30 s); Khopesh (5 and -2.2 give 1.8 swings per second); sandstorm (200-tick check, 1 in 90 = about 15 min; 150 s = 2:30); mummy stats (Mummy.java, RoyalMummy.java); spawn weights 12 and 1 (KhemetEntities.java:47-48); structure spacing 32/34/30/20; guard counts; the chest-table item lists; the Weakness touch (200 ticks = 10 s); stonecutter sources.
  - Fixture: my Gods checker reported 0 misses on the real page. On a copy with Ra's Regeneration changed to 0:30 it reported 1 miss. The probe can fail.
- Findings:
  - F1 [defect] Creatures page, Royal Mummy row: "Also guards Anubis's shrine and the desert ruins." desert_ruin.json spawns only khemet:mummy (1-2). Only anubis_shrine.json lists royal_mummy (1-1). The royal mummy does not guard the ruins; the sentence is copied from the Mummy row.
  - F2 [claim] Home card "Structures: Found in deserts". Anubis's shrine also generates in badlands (its biome tag includes #minecraft:is_badlands). The Structures page says so; the home card omits it.
  - F3 [claim] "Spawns Deserts: 1 to 1 at a time" is true but reads as an error. Say "singly".
  - F4 [premise] No printed figure states the Royal Mummy's 4% Ankh drop chance, nor the Ankh chances of 30% in the Ra shrine and 4% from the royal mummy. "Small chance" and "rarely" hide a reproducible number.
- Verdict: OBJECT
- One change: correct the Royal Mummy guard sentence to "Also guards Anubis's shrine" (F1); fix F2 in the same pass.
