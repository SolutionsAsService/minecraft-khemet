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
