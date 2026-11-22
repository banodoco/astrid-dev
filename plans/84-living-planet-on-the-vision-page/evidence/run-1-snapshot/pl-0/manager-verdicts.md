# Manager visual review — PL-0 donor, 22 November 2026

These are exploratory donor captures, not a fixed-pose acceptance baseline. Browser Chrome for Testing 153.0.8010.12; software GL (ANGLE/SwiftShader); DPR 2.

- `phone-portrait-dpr2.png` — OPENED. The low-poly globe is drawn, with a readable faceted silhouette, blue water and small orange mink. The planet overlaps the introductory paragraph and source attribution; the words lose contrast over its surface. The navigation exceeds the right edge. The world is placed centrally below the headline, which is a useful phone starting point, but the copy must have its own clear reading space in the product. The donor cards occupy a long separate opaque stack and do not demonstrate the requested shared translucent Foundations panel. Keep the world character, do not reproduce these layout defects. Image-viewing ability confirmed.

- `phone-landscape-dpr2.png` — OPENED. The globe becomes an enormous cropped foreground surface directly behind the entire headline and lead. Landmarks are legible, but the camera scale overwhelms the reading space; at the actual short viewport the controls consume valuable height. Product landscape framing needs a bounded right-side world or a lower separate stage, with clear words and scroll access.
- `tablet-dpr2.png` — OPENED. The same oversized globe fills the copy column and touches the navigation; a large amount of surface is cropped. The cast of mink and windmill are identifiable, but the text competes with them. Tablet must not inherit this desktop-width/short-camera mismatch. The floating controls cover pillar art farther down the page.
- `laptop-dpr2.png` — OPENED. The off-edge globe at the upper right gives the intended immersive world scale and carries below the hero. This is the strongest donor composition so far. Its left rim and stray mink still intrude into the last words of the headline and introduction; protect that boundary. The dark green surface, orange mink and blue lake form useful visual hierarchy. The separate cards below do not yet provide the requested continuous translucent panel.

- `wide-dpr2.png` — OPENED. The right-hand globe and generous sky give the desired scale and atmosphere. Its leftmost details still cross the headline; the upper crop is intentional-looking but needs more separation from the bar. The world barely carries into Pillars and none is visible behind Principles; the product stage must extend far enough for both sections without becoming an endless huge planet. The shared panel should read as one quiet surface rather than a set of unrelated opaque colour blocks.

## Supplemental crop review after restart — 22 November 2026
All ten crops opened individually by the manager with the image viewer. These are donor composition references, not fixed-pose acceptance baselines.

| Picture | Verdict |
| --- | --- |
| phone-portrait-hero-dpr2.png | Facets and landmark shapes read at phone width. Lead and attribution sit on the globe, weakening their contrast. Preserve the character; move/protect the reading space. |
| phone-landscape-hero-dpr2.png | Surface overwhelms the whole short viewport; controls compete with copy and landmarks. Needs a smaller, offset resting frame. |
| tablet-hero-dpr2.png | Globe is similarly oversized and behind almost every line of copy. The orange mink cross letters. Tablet must not simply inherit this desktop scale. |
| laptop-hero-dpr2.png | Upper-right crop is immersive and landmark detail is legible. Left rim and flying objects cross headline and body text; clear that boundary. |
| wide-hero-dpr2.png | Open left sky and off-edge planet establish scale well. Stray objects still intrude into the headline. Keep this balance with a protected reading column. |
| phone-portrait-pillars-dpr2.png | Cards and pixel art are readable. Floating controls cover the second card; planet disappears before the section rather than continuing behind one shared panel. |
| phone-landscape-pillars-dpr2.png | Two-column cards are readable, but controls cover the fourth illustration and the globe crowds section introduction. No shared panel yet. |
| tablet-pillars-dpr2.png | Card spacing is orderly. Globe details crowd the section copy; controls overlay the last card edge. Need one translucent foundation behind both sections. |
| laptop-pillars-dpr2.png | Four cards form a clear row with useful art and restrained colours. Planet barely persists above the section; panel composition still absent. |
| wide-pillars-dpr2.png | Same clear four-card row, no apparent text clipping. Broad sky remains separate from cards; carry the world behind the shared section wrapper. |

### Timing-run spin pairs
Previously opened each phone-portrait and laptop cpu1/cpu4/cpu6 spin-before.png and spin-after.png pair (12 images, DPR1). Landmarks and mink move between each pair: actual rotation is visible. Faceted form remains intact. Donor copy overlap persists. Stills establish changed orientation only; they are not evidence of smooth motion. Raw frame timing is in measurements.json.

### Motion clip keyframes — 22 November 2026
Reviewed the six sampled frames at DPR 1 on the SwiftShader diagnostic run. The spin frames show lake, windmill, and balloon positions changing while the world remains intact; copy overlap persists. These keyframes and clips are donor diagnostics, not owner visual-quality recordings. They provide no smoothness or native-GPU-performance evidence.

- `motion-phone-portrait-cpu1x.mp4` — 8.48 s. The script attempted wheel input, but did not record scroll offsets; page scroll movement is unproven. `recordings/phone-portrait/key-1-scroll.jpg` and `key-2-scroll.jpg` show the title in effectively the same position. `recordings/phone-portrait/key-3-spin.jpg` shows the spin-stage world pose; see the diagnostic caveat above.
- `motion-laptop-cpu1x.mp4` — 8.48 s. The script attempted wheel input, but did not record scroll offsets; page scroll movement is unproven. `recordings/laptop/key-1-scroll.jpg` and `key-2-scroll.jpg` show the title in effectively the same position. `recordings/laptop/key-3-spin.jpg` shows the spin-stage world pose; see the diagnostic caveat above.
