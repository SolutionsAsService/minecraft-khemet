- Anchor used: Bringhurst, The Elements of Typographic Style: choose faces that suit the text and each other; set a humane measure (about 45-75 characters); letterspace only capitals and small caps; use true punctuation; let the rag fall naturally.
- Observed: kh-desktop-home.png, kh-phone-home.png, kh-wide-1280-gods.png, kh-phone-375-relics.png, style.css. Uppercase letterspaced serif h1 inside a gold pill cartouche; Inter-like sans body at 16/1.55; body paragraphs capped at 38em; lede 34em; the frieze is a 10px repeating stripe of six flat colours.
- Findings:
F1 [claim] The uppercase serif (h1 .06em, panel names .08em) is correctly letterspaced capitals, and the 38em measure with text-wrap: pretty gives a calm rag (gods page lede, Status box). The lowercase h2/h3 are unspaced, as they should be.
F2 [defect] The cartouche's serif KHEMET is well made, but its inner bar (::after, 3px) sits hard against the right stroke and reads as a stray cursor on the phone (kh-phone-home.png). It is ornament that performs.
F3 [defect] Panel names on the phone wrap awkwardly ("RELICS & / WEATHER", 13px caps with tracking), while the sibling panels stay on one line. The panel set is uneven.
F4 [defect] The frieze is crude: six saturated hues in 14px blocks with 2px gaps, a rainbow bar in kh-desktop-home.png. It matches no Egyptian pattern and competes with the panel colours. It repeats above the footer, so it is a gimmick, not a rule.
F5 [defect] The serif/sans pairing is the wrong way round: Georgia is hard-coded in .panel .name and .ladder b, but the stack elsewhere starts with Iowan/Palatino. Faces drift between components, and Georgia's old-style figures in .ladder (0, 3, 10, 25) bounce on the baseline.
F6 [defect] Tables: label column set in bold coloured sans, no figure alignment; "0:20" and "2:00" durations are not tabular-aligned. Fine for scanning, plain in craft.
F7 [premise] Apostrophes in captions ("Ra’s shrine", "Anubis’s") appear curly in the screenshots; I did not verify every page's source.
- Verdict: OBJECT. Requested change: replace the six-hue frieze with a single-hue (gold) ruled band, and set the panel and ladder faces from the same serif stack variable.
