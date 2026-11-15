Critic: Inclusion (Holmes), R1

- Anchor used: Mismatch (Kat Holmes): exclusion is a mismatch between a person and a design; a fix for one extends to many.
- Observed: all 8 pages read (index, gods, blocks, install, relics in full; the screenshots were not opened). Skip link, `lang="en"`, `aria-current`, labelled ladder lists, `.sr` table captions and filled alt text on the content images are all present. Footer says "Dark theme only. English only." Evidence: no text under 12 px, 44 px tap targets, 6 panel JPEGs 169 KB total.
- Findings:
F1 [defect] "Black Land" appears once (blocks.html h1 and body) and is never glossed, and "Red Land" appears nowhere. The evidence file calls the ground "Kemet, the Black Land", but no page says what Khemet or Kemet means. Index h1 "Khemet" is unexplained to a newcomer. Egyptian terms (ankh, khopesh, cartouche, Sunstone, Myrrh) are not glossed.
F2 [claim] Gods are handled respectfully: Ra "God of the Sun", Anubis "God of the Dead", described as game mechanics ("takes offerings, gives a blessing") and not asserted as living belief. The "Stranger/Chosen" favor ladder and "worshipper" (gods.html) are game idiom. Nothing says Egyptian religion is being used as game content. One framing line would settle it.
F3 [defect] Reading level breaks on install and relics: "Fabric Loader 0.16", "Gradle 8", "gradle build", "jar", "operators", "/locate", "+5 attack damage (6 with a bare hand's 1)". Crafting grids such as "S·/·S·/·S; S = Golden Sandstone" are cryptic to a newcomer and read badly in a screen reader. A reader who has never played Minecraft is left out here.
F4 [defect] Index panel images have `alt=""`, which is fine because link text carries the name. The blocks.html screenshot alt text does not say what is shown beyond the count.
F5 [premise] "English only" is disclosed, but nothing is offered to a non-English reader, such as plain sentences that a translation tool can handle. Dark theme only leaves low-vision users who need a light page with no option.
- Verdict: OBJECT
- Requested change: add a short plain-language "New here?" glossary (Khemet = Egypt's own name for its land, Black Land = the fertile Nile soil, what a mod, jar and operator are), and put "Red Land" in the same place if it is meant to appear.
