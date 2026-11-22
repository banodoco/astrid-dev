# PL-1 manager visual review — 22 November 2026

Opened all ten isolated donor/App PNGs individually in pairs. These show the renderer port at fixed seed84, stopped localclock0, noon light and the donor initial orientation; they do not accept the final responsive page composition.

| Pair (both images opened) | Verdict |
| --- | --- |
| phone-donor.png / phone-app.png | Same globe outline, rim mink, lake, bridge and windmill. Faceted shading and orange silhouettes remain intact. No meaningful visible regression. |
| sideways-donor.png / sideways-app.png | Same top/bottom crop, landmark position and surface shading. No meaningful visible regression. Final landscape scale is PL-3. |
| tablet-donor.png / tablet-app.png | Same broad globe and landmark detail, with consistent low-poly edges and colour. No meaningful visible regression. Final tablet frame remains to set. |
| laptop-donor.png / laptop-app.png | Same strong right-side cropped globe, mink silhouettes, bridge and water contours. No meaningful visible regression. |
| wide-donor.png / wide-app.png | Same off-edge composition, surface features and shading across the enlarged crop. No meaningful visible regression. |

Raw diff-results.json reports 0.03985%, 0.02916%, 0.01196%, 0.01274%, 0.01164% pixels over16/255 respectively within nonempty alpha union bounds. All below the unchanged0.5% tolerance. Numerical evidence and capture/diff implementation still receive the separate verification check; this is visual acceptance of port fidelity only. Actual production page pictures remain pending.

## Actual production page comparisons
Opened both page-<size>-before.png and page-<size>.png at all five fixed sizes. Before is starting e3dbad64 production build; after is05f5ce4 with explicit fixed-pose diagnostic. Same pinnedfeed/date/DPR2/backend.

| Pair | Verdict and next owner |
| --- | --- |
| page-phone-before.png / page-phone.png | Headline/lead/attribution remain in their original geometry. Planet is drawn but the inherited illustration box clips it and introduces a large blank interval before the partial globe. This temporary integration composition is rejected as the final phone design; PL-2/PL-3 must replace the stage and camera frame. |
| page-sideways-before.png / page-sideways.png | Globe replaces the juggler clearly at right without crossing copy. Too small to carry the intended immersive world; PL-2/PL-3 enlarge and continue it behind the panel. |
| page-tablet-before.png / page-tablet.png | Copy and navigation remain readable and stationary; globe is a small isolated illustration. Needs its own world-scale resting frame and shared panel. |
| page-laptop-before.png / page-laptop.png | Renderer works in the existing right-hand illustration space and copy is preserved. Globe remains far too small for donor composition; PL-2/PL-3 own that next. |
| page-wide-before.png / page-wide.png | Same preserved copy/navigation with a tiny right-hand world. The planned off-edge planet and below-hero continuation have not yet been built. |

These accept only the PL-1 port boundary, subject to focused verification. They do not accept the finished layout. The task plan deliberately assigns stage/layout to PL-2 and camera/framing to PL-3; no owner preview should be requested from this intermediate candidate.

Opened page-still.png and page-home.png. Still Vision has a drawn globe in the illustration space with readable copy; full poster/fallback coverage remains PL-4. Home retains its normal page composition; network proof separately reports no engine request.
