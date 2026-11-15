- Anchor used: Bringhurst, The Elements of Typographic Style: one family chosen and kept (3.1); figures suited to their setting, tabular in tables, lining with capitals (4.2); rules and ornament must not outshout the text.
- Observed: kh-desktop-home.png and kh-phone-home.png, plus site/style.css. The frieze is one gold ruled band. The cartouche is a plain gold oval around KHEMET. On the phone all six panel names are one word with an arrow, and they line up. In style.css line 83 `.panel .name` and line 68 `.ladder b` still set `font-family: Georgia`, while line 10 defines `--serif` and line 21 applies it to h1, brand and h3.
- Findings:
 F1 [defect] Closes R1 "six-hue frieze": the single-hue ruled band is quiet and serves as a rule.
 F2 [defect] Closes R1 "cartouche bar read as a cursor": the bar is gone, only the oval remains.
 F3 [defect] Closes R1 "uneven panel names on the phone": one word each, same size, arrows aligned.
 F4 [defect] REOPENS R1 "Georgia hard-coded beside the serif stack": lines 68 and 83 remain. On a machine with Iowan or Palatino, the heading and the panel label beside it (h1 and panel name, h3 and ladder numeral) are two different faces. The evidence line "one serif variable" is false for these two rules.
 F5 [claim] Partly closes R1 "untabular figures": tabular lining figures are set in `table.data td` and `.ladder b`. The `.panel .fig` lines ("19 blocks", "5 potions") are proportional, but they are not stacked in columns, so this is minor.
- Verdict: OBJECT. Requested change: replace both `Georgia` declarations (lines 68 and 83) with `var(--serif)`.
