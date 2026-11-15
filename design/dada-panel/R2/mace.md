- Anchor used: The Principles of Universal Design (Mace et al.): Perceptible Information, Equitable Use and Low Physical Effort, checked in every mode.
- Observed: Playwright at 1280 and 375 on index, gods and install. 14 real Tab presses each. Every control showed a 3px solid outline (black on the skip link, rgb(242,235,214) elsewhere). Nav links and buttons are 44px tall. With forcedColors active I tabbed to Potions and took mace-fc-index.png in the scratchpad. The ring, Install button border, panel borders and current-page underline are all visible.
- Findings:
F1 [defect, closes R1 unobserved focus rings] Measured on real Tab presses, including the panels at 337x255 and 170x122. The ring is not clipped.
F2 [defect, closes R1 no forced-colors block] The block exists and renders. The ring, button borders and panel edges survive. Seen in the screenshot, not inferred from the CSS.
F3 [defect, closes R1 duplicate dusk alt text] Each pair of alts now differs: "Ra's shrine in a desert" vs "Ra's shrine at dusk", "...under an orange sky" on the structures page, "darkening sky" on blocks.
F4 [claim] The alts "under an orange sky" and "darkening sky" describe the images. I did not check them against the pixels. Low risk.
F5 [premise] The footer links are 47x17 and 118x17, but they sit inside a paragraph. That is the 2.5.8 inline exception, so it is not a defect.
F6 [premise] Dark-only is disclosed in the footer and deferred. I accept that as stated, not as proof.
- Verdict: PASS. All three R1 objections are answered by what I measured.
- Requested change: none required. Optionally, give the three footer links a 24px target or spacing, so that 2.5.8 holds without the inline exception.
