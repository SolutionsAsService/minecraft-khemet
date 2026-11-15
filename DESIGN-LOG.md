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
malachite green, Creatures = turquoise (faience, the sixth Egyptian pigment-material), Relics and weather = carnelian orange. Values and
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
