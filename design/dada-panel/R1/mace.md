Critic: Inclusion (Mace), R1

- Anchor used: Principles of Universal Design (Mace et al.): perceptible information, equitable use, size and space for approach.
- Observed: style.css line 16 `a:focus-visible, .btn:focus-visible` = 3px solid #F2EBD6, offset 3px, on a #14110F ground (strong). Skip link (.skip, line 17-18) is first in every page, jumps to `main#main[tabindex=-1]`. Source order is skip, brand, nav, main; no positive tabindex. Nav and buttons min-height 44px; nav gap 2px but 44px height clears 2.5.8. Every content img has alt; the six home panel images and 22px icons are alt="" beside link text (correct). Muted/hue text is claimed >=4.5:1 by the evidence file (not independently measured by me). Home panels carry hue plus a name, a figure and a thumbnail, so hue is never the only channel; current page is marked by a 4px border plus aria-current. I saw kh-desktop-home.png only; I did not press Tab.
- Findings:
F1 [defect] structures.html: day and dusk images share identical alt ("The shrine of Ra in a desert" x2, same for Anubis); the difference is lost to screen-reader users (gods.html distinguishes them).
F2 [defect] No `@media (forced-colors: active)` anywhere in style.css; the .frieze gradient, signal-coloured buttons (.btn-quiet is transparent with a signal border) and the aria-current border-bottom are unverified in forced colours.
F3 [claim] The evidence file's contrast figures are build-printed numbers; the focus ring's contrast on .skip (#EDBE3A background) is unstated.
F4 [premise] The evidence says no text under 12px and 44px targets, but nothing states a real Tab-press check was run; ring visibility on .panel (3px hue border, 3px offset) is unobserved.
F5 [claim] Dark theme only is disclosed; fine for this slice.
- Verdict: OBJECT
- Requested change: add a `forced-colors: active` block (explicit borders on .btn-quiet and aria-current, ring in CanvasText), and give the dusk images distinct alt text.
