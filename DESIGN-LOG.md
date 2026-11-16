# DESIGN LOG: the Khemet site (DADA run)

## Traversal Plan

**Brief, one sentence.** A deployable multi-page front end for Khemet, the Egyptian-mythology Minecraft mod, that shows what slice one
actually is (twelve stones, plants and potions, two gods with favor, four structures, mummies, sandstorms, two artifacts) with real
in-game photographs and honest status, as the sibling of the Asgard site and in an entirely different visual identity.

**Mode: Adaptive.** The site serves a public of players and builders; the brief says "design front end deployable", and the design
must be approachable to someone who has never seen the mod. The governing criterion is MAYA: the advanced pole and the acceptable pole
both have to hold.

**Run type: Full** (a new site from an empty `site/`), with the **Landing** rules applied to the home page (first screen, summary
graphic, legibility). No existing artifact, so R0 (premortem on an inherited artifact) is not applicable; the premortem is the
Asgard site's graded lessons, read below.

**Tooling inventory.** Panel: sub-agent tool (one agent per reference, at most three at a time, verdicts filed to a panel directory).
Panel choice: `skills/dada/scripts/pick_panel.py`. Graph: no graph tool; Mermaid text in this log. Workflow state: this log's
checklist. Measurement: headless Chromium via Playwright, ImageMagick for captures. Ledger import: `dada` repository not at hand for
`import_log.py` in this session (stated at close).

**Seed (exact labels from references/anchor-graph.md).**
- Stance: `Make It Bigger (Paula Scher)`
- Rules: `Visual Hierarchy (Arnheim, Dondis)`; `Grid Systems in Graphic Design (Josef Müller-Brockmann)`
- Breaker: `Learning from Las Vegas (Venturi, Scott Brown, Izenour)`
- Counterpoint (dotted edge from Stance): `Make It Bigger (Paula Scher)` -.->|contrasts with| `The Vignelli Canon (Massimo Vignelli)`

Chain: Make It Bigger -> (grounds) Visual Hierarchy -> (grounds) Grid Systems in Graphic Design; Learning from Las Vegas (the building
as its own sign) breaks the "headline over a hero image" convention; The Vignelli Canon is the restraint the bigness must answer to.

**Palette source (derived from the topic, not a house palette).** Egyptian painting worked with a canonical set of six colours:
white (gypsum), black (carbon), red (ochre), yellow (orpiment/ochre), blue (Egyptian blue) and green (malachite), and the country
itself was named by two of them: *Kemet*, the Black Land of the Nile's silt, and *Deshret*, the Red Land of the desert. The site takes
that system: the page ground is Kemet black; the signal colour (links, buttons, the argument) is gold-yellow; and each topic category
gets one of the others: Blocks = limestone white, Gods and shrines = Egyptian blue, Structures = red ochre, Plants and potions =
malachite green, Creatures = turquoise (faience, the sixth Egyptian pigment-material), Relics and weather = amethyst (a gem of Egyptian jewellery; first drafted as carnelian orange, which measured only delta-E 23.8 from the red ochre, so it was changed). Values and
the measured ΔE and contrast are printed by the build (it fails below ΔE 30, below 3:1 for marks, below 4.5:1 for text).

**Initial Frontier.**
| Candidate | Reached via | From anchor | Status |
|---|---|---|---|
| Landing as a register wall of six photo tiles (the front is the sign) | breaks, then grounded by Visual Hierarchy | Learning from Las Vegas | TAKEN (M2) |
| One hue per page category, measured | grounds | Visual Hierarchy | TAKEN (M1) |
| Eight pages on one grid with shared navigation | grounds | Grid Systems in Graphic Design | TAKEN (M3) |
| Restraint inside the tiles: two type sizes, one frame | dotted counterpoint | The Vignelli Canon | OPEN (answer after R1) |
| Status honesty bands: tested / not tested | follows from the mod's own rules | (project) | TAKEN (M4) |
| Light theme | deferred: dark only, as Asgard | (project) | DEFERRED (out of scope for slice one) |

**Panel (from `pick_panel.py --mode adaptive --run-type full --project khemet`).** Debord, Shklovsky (Provocateur, dotted with Krug),
Holmes, Mace (Inclusion), Cairo (Evidence, measurement seat), Krug (Usability), Bringhurst (Craft), Garland (rotation). The run is
seated with the first six for round R1 (a bounded run: the session has hit agent rate limits on earlier DADA runs, so seats are
launched three at a time and any seat that does not file is recorded NOT REPORTED, not reconstructed).

## Decision Records

### Move M1: Palette from the six canonical colours of Egyptian art  (KEEP-THE-RULE)
Depends on: none
Anchors: Stance Make It Bigger (Paula Scher) | Rule Visual Hierarchy (Arnheim, Dondis) | Counterpoint The Vignelli Canon (dotted edge from Make It Bigger)
Intent: black ground, gold for action, one hue per category, so a visitor tells the parts apart by colour as well as by label.
Formal argument: claim, the six-colour system is the topic's own; grounds, a canonical set with a documented history (white, black, red,
yellow, blue, green) plus faience turquoise and carnelian; warrant, Visual Hierarchy needs a value-and-hue ladder where the signal
colour is the strongest thing on the page, so gold is reserved for the argument.
Alternatives rejected: (1) papyrus-and-ink "parchment" ground: the cliché, and light-ground gold fails contrast; (2) Minecraft dye
colours as Asgard did: ties Khemet to its sibling's identity, which the brief asks it not to share.
Consequence: six hues on near-black means pairwise ΔE and 4.5:1 text contrast must be checked; "red ochre" on black is the risky pair.
Fence: do not let a meaning ride on hue alone (every category also has a name, a glyph and a page).
Frontier effect: opens "glyph per category" (taken in M2) and a contrast fix if red ochre fails.
Advanced pole: a topic-derived six-colour register on black. Acceptable pole: black ground, light text, one gold link colour.

### Move M2: The landing is a register wall of six photograph panels  (BREAK)
Depends on: M1
Anchors: Stance Make It Bigger (Paula Scher) | Rule Visual Hierarchy (Arnheim, Dondis) | Rule Grid Systems in Graphic Design (Josef Müller-Brockmann) | Breaker Learning from Las Vegas (Venturi, Scott Brown, Izenour) | Counterpoint The Vignelli Canon (dotted edge from Make It Bigger)
Intent: the first screen is one composed object, like the painted register of a temple wall: a cartouche title over six panels in two
rows, each a real in-game photograph with its category hue as the band, its computed figure, and a link; the whole site read at once.
Formal argument: claim, the front of the building should be its own sign; grounds, the mod is visual (structures, blocks, creatures),
so the proof is the photographs, and a wall of panels states every topic on the first screen; warrant, Make It Bigger (scale and
confidence) with the grid keeping the panels on one 3 by 2 module (2 by 3 on a phone).
Alternatives rejected: (1) a single hero photograph of the Ra shrine: beautiful, but it summarises one topic of six (the First-screen
rule's own failure case); (2) a card row with icons: six cards in a row is not a form.
Consequence: six photographs on the first screen cost bytes; the images are PNG captures, so the build records the weight of the
first screen and the largest request, and reduces them if heavy. Panels must stay legible at 375 px.
Fence: the convention broken is "headline, subhead, button over a hero"; the fence is that a visitor must still be able to name the
site and three topics in five seconds, so each panel carries its name and one figure.
Reception dial / poles: Advanced: the page is a wall, not a hero. Acceptable: tiles with images and labels are a pattern everyone reads.
Frontier effect: opens "chip per panel for the stat", "panel order", and the Vignelli counterpoint (restraint).

### Move M3: Eight pages on one grid  (KEEP-THE-RULE)
Depends on: M1, M2
Anchors: Rule Grid Systems in Graphic Design (Josef Müller-Brockmann) | Rule Visual Hierarchy (Arnheim, Dondis)
Intent: Home; Blocks; Plants and potions; Gods and shrines; Structures; Creatures; Relics and weather; Install. Shared header, one
column measure, tables for every computed fact.
Formal argument: a page per topic (the skill's multi-page rule), each page's colour is its category hue; facts are computed from the
mod's own data (blocks from block states, structures from the NBT and structure sets, favor stages from content.json, stats from the
entity classes), so a number cannot drift from the mod.
Alternatives rejected: one long page (hides the sections, fails the multi-page rule); a page per block (twenty thin pages).
Consequence: the build must read the mod's files and fail if a figure cannot be computed.
Fence: grids exist to make reading predictable; the one break is the landing wall.

### Move M4: Honest status on every page  (KEEP-THE-RULE)
Depends on: M3
Anchors: Rule Visual Hierarchy (Arnheim, Dondis)
Intent: each page ends with "Status": what was verified in a running game (loaded, natural generation by /locate, favor and blessings
through the command path, the sandstorm slowing players in the open and not under a roof, creature rendering) and what was not (using an
altar by hand, brewing, the Ankh and Khopesh in combat, plant placement, a natural sandstorm).
Alternatives rejected: a single status page (nobody reads it); no status (the mod is a slice).
Consequence: the status text is a list of claims the panel can check against the project's own log.

## Panel Reports

### Panel, WHOLE, round R1  (artifact examined: site/ at the build `site written: 8 pages; palette min delta-E 44.9`, with rendered screenshots at 1280x800 and 375x812)
Seated from `pick_panel.py` (8 picked, 6 sat; Shklovsky and Garland not seated: bounded run). One agent per seat, three at a time, each filing to `panel/R1/<seat>.md` (all six filed; none NOT REPORTED). Evidence file: `panel/R1/evidence.md`.
| Critic | Anchor used | Observed in the work | Verdict | Requested change |
|---|---|---|---|---|
| Debord | The Society of the Spectacle, thesis 1 | Status boxes are a counter-spectacle; body copy above them states untested behaviour flatly | OBJECT | qualifier in the sentence; swap the storm card photo or drop "a storm" |
| Mace | Principles of Universal Design | focus ring and skip link present; dusk alt text duplicates; no forced-colors block | OBJECT | forced-colors block, distinct dusk alts |
| Cairo | How Charts Lie | recomputed every figure on Gods, Creatures, Relics against the source; landing 704/800 and 710/812; probe fails on a corrupted fixture | OBJECT | correct the Royal Mummy guard sentence |
| Krug | Don't Make Me Think | phone first screen does not say "Minecraft mod"; legibility probe fails on phone; no first action | OBJECT | full tagline on phone, an Install button |
| Holmes | Mismatch | "Black Land" unglossed; install page reading level; respect framing absent | OBJECT | a "New here?" glossary |
| Bringhurst | The Elements of Typographic Style | six-hue frieze crude; cartouche bar reads as a cursor; panel names wrap unevenly; Georgia hard-coded | OBJECT | single-hue frieze; one serif variable |
Statements of meaning (round): the wall reads as a sign for the mod; the honest Status boxes read as the site's real voice. Andon pulled: no.

#### Resolutions, round R1
| Seat: finding | Resolution |
|---|---|
| Debord: F1 storm card photo has no storm | ADAPT (M5): the tile's claim now says what the photo shows |
| Debord: F2 + F3 untested numbers stated flatly | ADAPT (M5): "as written in the code, not yet tried in play" in the sentence |
| Debord: F4 "Be named Chosen" never reached | OVERRULE (premise refuted: Ra favor 28 "Chosen" measured through the command path, with Regeneration II, Fire Resistance and Strength II active) |
| Debord: F5 mummy guards and the 15-minute sandstorm untested | ADAPT (M5): worded as set in the data, not yet watched |
| Debord: F6 install facts not in the evidence file | OVERRULE (premise refuted: Loader 0.16 is in fabric.mod.json, Loom 1.11.8 and the version in gradle.properties; the evidence file omitted them, R2 file adds them) |
| Debord: F7 the wall sells a world, the mod shows a lab | ADAPT (M5): a caption under the wall says the photographs are flat-world test captures |
| Mace: F1 duplicate dusk alt | ADAPT (M5) |
| Mace: F2 no forced-colors block | ADAPT (M5) |
| Mace: F3 + F4 focus ring on panel and skip link unobserved | ADAPT (M5): measure a real Tab press on both |
| Mace: F5 dark theme only | DEFERRED: light theme, out of scope for slice one, disclosed in the footer |
| Cairo: F1 Royal Mummy "also guards the ruins" is false | ADAPT (M5): the guard list is computed from the structure data per creature |
| Cairo: F2 "Found in deserts" omits badlands | ADAPT (M5) |
| Cairo: F3 "1 to 1 at a time" | ADAPT (M5): "singly" |
| Cairo: F4 drop chances hidden as "small chance" | ADAPT (M5): the Ankh chances are computed from the loot tables and printed |
| Krug: F1 phone does not say Minecraft mod | ADAPT (M5) |
| Krug: F2 phone legibility probe fails | ADAPT (M5): the figure names the gods ("Ra & Anubis") |
| Krug: F3 no first action | ADAPT (M5): a gold Install button beside the title |
| Krug: F4 nav costs three rows on phone | ADAPT (M5): shorter labels, two rows |
| Krug: F5 tiles not marked as links | ADAPT (M5): an arrow on each panel |
| Holmes: F1 + F3 unglossed terms and reading level | ADAPT (M5): a "New here?" glossary, and recipes written as sentences |
| Holmes: F2 respect framing | ADAPT (M5): one framing line on the Gods page |
| Holmes: F4 weak alt on the blocks photo | ADAPT (M5) |
| Holmes: F5 no translation, no light page | DEFERRED: same reason as Mace F5 |
| Bringhurst: F2 cartouche bar reads as a cursor | ADAPT (M5): removed |
| Bringhurst: F3 uneven panel names on phone | ADAPT (M5): one-word panel names |
| Bringhurst: F4 six-hue frieze is crude | ADAPT (M5): a single-hue gold ruled band |
| Bringhurst: F5 + F6 faces drift, figures not tabular | ADAPT (M5): one serif variable, lining and tabular figures |
| Bringhurst: F7 apostrophes unverified | ADAPT (M5): verified in the build output |

### Panel, WHOLE (reconvened seats), round R2  (artifact examined: site/ after move M5, rendered; evidence file `panel/R2/evidence.md`)
| Critic | Anchor used | Observed in the work | Verdict | Requested change |
|---|---|---|---|---|
| Mace | Principles of Universal Design | 14 real Tab presses per page, every control a 3px solid outline, not clipped; forced-colors screenshot keeps ring, button borders, panel edges, current-page underline; dusk alts differ | PASS | none required (optional: footer link targets) |
| Krug | Don't Make Me Think | both first screens show title, "A Minecraft mod", an Install button and six arrowed panels; probe traced Gods to the favor ladder | OBJECT (narrow) | the button says "Install" but the page is build-from-source |
| Cairo | How Charts Lie | wall bottom 733.8 of 800 and 752.1 of 812 with the caption; a corrupted fixture fails the probe; recomputed every stat, drop, weight, spacing, size and the Ankh numbers | OBJECT | home card says badlands for all structures; Khopesh chest chance omitted; Ankh "does nothing at full health" false when poisoned |

#### Resolutions, round R2
| Seat: finding | Resolution |
|---|---|
| Krug: "Install" over-promises a download | ADAPT (M6): the button reads "Build & install" |
| Cairo: home card "deserts and badlands" is true only of Anubis's shrine | ADAPT (M6): "Found in deserts; one also in badlands." |
| Cairo: Khopesh chest chance omitted | ADAPT (M6): computed from the loot table and printed (30%) |
| Cairo: Ankh "does nothing at full health" false when poisoned or withered | ADAPT (M6): reworded to match AnkhItem.java |
| Mace: optional footer link targets | ADAPT (M6): footer links padded to a larger target |

(R2, second batch, on the state after M6 and the S4 push)
| Critic | Anchor used | Observed in the work | Verdict | Requested change |
|---|---|---|---|---|
| Debord | The Society of the Spectacle, thesis 1 | caption on both viewports; Relics discloses the sparse photo and the untested sandstorm start; Gods states Chosen reached through the command; lead sentences on Gods, Structures, Blocks and Potions still state design as fact | OBJECT | apply "as written, not yet seen in play" to those leads; cut "kept through death" until tested |
| Bringhurst | The Elements of Typographic Style | gold ruled band, plain oval cartouche, one-word panel names aligned; `font-family: Georgia` still set on `.panel .name` and `.ladder b` beside the `--serif` variable | OBJECT | replace both with `var(--serif)` |

#### Resolutions, round R2 (second batch)
| Seat: finding | Resolution |
|---|---|
| Debord: lead sentences state design as fact (Gods, Structures, Blocks, Potions) | ADAPT (M7): reworded as set / written / not yet tried |
| Debord: "kept through death" untested | OVERRULE (premise refuted: Ra favor was 28 "Chosen" before the player was killed and 28 after the respawn, measured), and the measurement is added to the Gods status |
| Bringhurst: Georgia overrides the serif variable | ADAPT (M7): both declarations removed; the computed font-family of h1, h2, `.panel .name` and `.ladder b` is "Iowan Old Style" at 1280 (the stack's first family) |
| Bringhurst: panel figures are proportional | DEFERRED: they are single short lines, not stacked in columns; the tables and ladder use tabular lining figures |

## Move M5 / M6 / M7 and the S4 push (what was done, after the fact, with the measurements)
- **M5 (ADAPT of R1):** every R1 finding with its resolution above: nav labels and panel names shortened, figure names the gods, an Install button, a glossary, plain recipes, claims qualified or computed from the data, one-hue frieze, cartouche bar removed, forced-colors block, focus ring. Depends on M1-M4. Measured after: landing 734/800 and 752/812 with the caption (a first version of the caption pushed the phone wall to 819 of 812 and was shortened), floor 16 of 16 clean, 0 straight apostrophes, real Tab presses show a 3px ring on every control.
- **M6 (ADAPT of R2):** "Build & install", badlands stated for the one structure that has it, the Khopesh chest chance computed and printed (30%), the Ankh's full-health rule matched to the code.
- **S4 ambition push (the wall's photographs taller):** desktop photographs 166 -> 189 px (+14%), wall bottom 734 -> 781 of 800, phone unchanged at 752 of 812, no sideways scroll. Judged in round R2's second batch (no objection to it).
- **M7 (ADAPT of R2, second batch):** Georgia overrides removed (computed value checked), lead sentences reworded, the death test added to the Status.

## Frontier (final)
| Candidate | Reached via | From anchor | Status |
|---|---|---|---|
| Landing as a register wall | breaks | Learning from Las Vegas | TAKEN (M2) |
| One hue per category, measured | grounds | Visual Hierarchy | TAKEN (M1, changed to amethyst after a measured delta-E of 23.8) |
| Eight pages on one grid | grounds | Grid Systems in Graphic Design | TAKEN (M3) |
| Restraint inside the tiles (the Vignelli Canon counterpoint) | dotted edge from Make It Bigger | The Vignelli Canon | TAKEN (applied in M5: one-word panel names, a single-hue rule, no ornament bar) |
| Honest status bands | project | none | TAKEN (M4; widened in M5 and M7) |
| Light theme | project | none | DEFERRED (out of scope for slice one; the footer says dark only) |
| Translations | Holmes F5 | Mismatch | DEFERRED (English only, disclosed) |

## Stop test
- **S1** Frontier has no OPEN items: met (taken or deferred with reasons).
- **S2** a WHOLE round with PASS from every required critic: **not met.** Mace passed in R2; Krug, Cairo, Debord and Bringhurst objected in R2 and their findings were answered by M6 and M7, which were applied and measured but not re-judged by those seats. Shklovsky and Garland (picked by the picker) were not seated.
- **S3** two consecutive quiet WHOLE rounds: **not met.**
- **S4** ambition push, measured: met (above).
- **S5** every dotted edge leaving a used anchor applied or declined: met (Make It Bigger to The Vignelli Canon applied in M5).
**The run is incomplete under the bound.** Resume point: reconvene Krug, Cairo, Debord and Bringhurst (and seat Shklovsky and Garland) on the state after M7 (commit `main`, site/), then run a second quiet WHOLE round.

## Anchor Ledger
| Anchor | Role | Status | Evidence | Note |
|---|---|---|---|---|
| Make It Bigger (Paula Scher) | Stance | KEEP | survived Krug's R1 "does not say it is a mod" objection by gaining a tagline and a button without shrinking the wall | the wall grew 14% in S4 |
| Visual Hierarchy (Arnheim, Dondis) | Rule | KEEP | survived R1's "no first action" and "unlinked tiles" | arrows, a button, a gold signal |
| Grid Systems in Graphic Design (Josef Müller-Brockmann) | Rule | KEEP | survived Bringhurst's R1 untidy-names finding | one-word names on one grid |
| Learning from Las Vegas (Venturi, Scott Brown, Izenour) | Breaker | KEEP | survived Debord's R1 "the wall sells a world" | answered with a caption, not by dropping the wall |
| The Vignelli Canon (Massimo Vignelli) | Counterpoint | ADAPT | applied as restraint in M5 | frieze reduced to one hue, ornament bar removed |

## Double loop
The criterion (MAYA) held, and the graph held. The panel's most productive seats were the measurement and claims seats, and every one of their strongest findings was something I wrote carelessly, not something the design got wrong: a Royal Mummy guard sentence copied from the Mummy row, a "one serif variable" claim made from the source and not the computed value, a caption that broke the fold. The process rule "assert on the computed value" already says this; I did not follow it for the font claim. Graph amendment: none to the nodes. Process amendment: for any site that prints facts, the build should compute every sentence that names a source (done for most; the font and the fold are now measured), and Cairo should sit from R0, not R1, because his findings cost the least to fix early.

## Carry-forward Ledger (facts about the medium, read before a later run on this site)
- A later same-specificity CSS rule beats an earlier one, even if the earlier one uses `var()`: `.panel .name { font-family: Georgia }` defined after the `--serif` rule won, shown only by the computed `font-family` (M7).
- In a Python f-string or plain string that emits CSS, `"\2192"` is an octal escape and renders a control character plus "92"; write `"\\2192"` (the arrow rendered as "DC1 92" until the built CSS was inspected).
- Measure the figure including its caption: a one-line caption inside the measured container moved the phone wall's bottom from 752 to 819 against an 812 fold (M5).
- A CIE76 gate caught carnelian at delta-E 23.8 from red ochre; amethyst `#DE86C6` passed at 44.9 (M1).
- 640x320 JPEG panels at quality 80 weigh about 28-34 KB each against 100-300 KB for the PNG captures; six together are 169 KB (M2).
- `page.emulateMedia({ forcedColors: 'active' })` in Playwright shows whether rings, borders and underlines survive forced colours.
- `check_floor.py` needs `/root/.claude/tools/measure.py`, which is not installed in this environment; Playwright probes stood in.

## Compliance Check
- [x] Tooling inventory: sub-agent tool for the panel; `pick_panel.py` for the seats; no graph tool (Mermaid text and tables in this log); Playwright and ImageMagick for measurement; `import_log.py` not run (below).
- [x] Mode stated with the reason (Adaptive: a public of players and builders).
- [~] Panel seated from `pick_panel.py`: 8 picked, 6 sat in R1 (Shklovsky and Garland not seated, a bounded run because earlier runs in this session hit agent rate limits); every seat briefed from its `seats/` file. The bound was my own, not the person's words.
- [x] Seed with exact labels, one dotted-edge counterpoint, a living Frontier (above).
- [x] Run type stated (Full, with Landing rules), no freeze broken.
- [~] Mobile Floor measured (16 rows, Playwright) at the final state; `check_floor.py` could not run. What needs a phone: nothing measured on a real phone.
- [x] Shadw- and Vercel-configured: root and inner `vercel.json`, `fluid.json`, root redirect, root-anchored `.vercelignore`, absolute `og:image` on the shadw.app address; checked by the build, which passed.
- [x] Palette derived from the topic (six canonical colours of Egyptian art), min delta-E 44.9, contrast >= 5.24:1 on ground and card; the palette is dark only, and light mode was not checked; no meaning rests on hue alone (each category has a name, a figure and an icon).
- [x] Landing leads with one bold graphic summarising every topic (the wall), measured complete at both sizes (781/800 and 752/812).
- [x] At least one BREAK move taken (M2).
- [x] A Decision Record before each of M1-M4; M5-M7 are recorded after the fact in this log (not before), which is a deviation, stated here.
- [x] A Panel Report per round, each critic citing something observable.
- [x] Every OBJECT resolved as ADAPT, OVERRULE or DEFERRED, with a reason.
- [ ] WHOLE rounds run to the stop conditions: S2 and S3 not met (above).
- [x] Every figure the artifact displays re-measured at the final state (landing, floor, fonts, text figures against the data by Cairo in R2 and by the build).
- [x] Anchor Ledger complete; the live graph is the table above (no graph tool).
- [x] Double-loop paragraph written.
- [ ] Run recorded in the ledger (`import_log.py`, `rate_seats.py` not run: the dada repository's ledger was not updated in this session).
- [x] Final reply states the mode, the tools, the stop conditions and everything skipped.


## Run: Polish and extend (2.0: faces, and a cobra, a crocodile and the Sun Pharaoh)

**Brief:** revamp and polish the Khemet models; keep going from the design. Mode: Adaptive. Run type: Polish for the five existing creatures, Extend for the new ones.

**Found by the close-ups:** the mummies' head wraps lay over their eye rows (blank faces), the royal mummy's face was the same linen as its wrappings, the
jackal's eyes were one pixel at the edge of its head, and the scarab and the guardian's face cameras pointed at nothing (a small or long-snouted mob needs its
head position given). **Fixed:** `face()` on every head, bands moved above the eyes and under the mouth, a gold mask, eyes on the side faces of the jackal,
thicker mummy arms. **New, from the design's lists** (the Serpent Pharaoh's venomous creatures, "crocodile-infested waters", the Sun Pharaoh): a Cobra (17
parts), a Crocodile (42) and The Sun Pharaoh (47 parts, a boss). Measured once each in a running game: cobra reached a player in 3 s and hit for 2.5 with
Poison; crocodile 4 s, 4.5; Sun Pharaoh 3 s, 6.5.
**Not done:** the Serpent Pharaoh, the Golden Pharaoh and the mounts (a rideable scarab, falcon, camel) are not built; the cobra's head reads small from the
front; the crocodile does not swim; the Sun Pharaoh spawns rarely in deserts and nothing else places it; no panel; animation in stills only.


## Run: Extend (a craftable chariot)

**Built:** the war **Chariot**: an item (sprite, model, recipe: leather, three acacia planks, a gold ingot and two sticks) that sets a chariot down; a `Mob` with the riding hooks (use it to board, the first rider drives by look direction, forward and back, sprint for a burst, a second rider can sit behind; it climbs one block, takes no fall damage, and when broken drops the item); a 76-part model (a gilded carriage with a lapis guard and sun disc, two spoked wheels that turn as it moves, a pole and yoke, two harnessed ponies scaled down from the horse builder). **Checked:** builds, loads; the recipe unlocks (`recipe give`), the item is given, the entity summons and the player can be seated by command; photographed from six angles. **Not checked:** crafting by hand, driving, the second seat, the wheels turning in motion, and how the team overhangs the hitbox (the ponies are drawn ahead of a 2-block footprint).
