# Tasks — A living planet on the vision page

[Plan](plan.md) · [Inputs](inputs.md) · [Art direction](art-direction.md) · [References](assets/README.md)

**Task ids:** `LP-0`–`LP-6`, `RS1`, `R`. **Critical path:** LP-0 → LP-1 and LP-2 → LP-3 → RS1 → LP-4 → LP-5 → LP-6 → R. **Estimates:** 12–19 engineering days, excluding owner/independent review and release waits. The owner chooses the runtime after LP-0; don't build unused rendering modes.

**Test inventory (reverify on exact product base):** App `.github/workflows/public-vision.yml`; `tests/e2e/public-astrid-vision-captures.spec.ts`; `tests/e2e/public-astrid-vision-entry.spec.ts`; page/sky tests under `src/pages/Home/`; existing mobile layout, social/nav and contrast specs. Capture fixed screenshots at **390×844, 844×390, 820×1180, 1440×900 and 1920×1080**. Pin source SHA, seed/pose, content feed, sky hour, viewport, DPR, renderer and device profile on every comparison. Compare to LP-0 baseline, not to an isolated art canvas.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **LP-0 — Ground truth and rendering choice (1–2 d).** Inspect exact App/planet heads and existing assets; produce a page-composition sheet, performance/capture baseline and tiny still-vs-loop-vs-live comparison; choose and document one format. | N | — | Read-only App/planet source; planning evidence under this plan; scratch prototype only, no product edits until run authority | Baseline report with SHA/5 viewports/current loading and comparison of quality, file size, runtime cost and fallback; one approved delivery-mode decision | [ ] |
| **LP-1 — The sphere and material language (2–3 d).** Full 3D globe, gentle relief, terrain/water/paths, a few draft trees, key/fill/contact shading and fixed camera; no detailed vignette population. | X | LP-0 | Planet scene/geometry/material/camera sources, chosen authoring medium and its focused tests | Gray and shaded 360° turntables; 1440 and 390 width page-composition stills; silhouette clearly spherical from any side and no terrain appearing as a flat platform | [ ] |
| **LP-2 — One canonical 3D mink (2–3 d).** Build a small sculptural mascot consistent with the 2D icon, with idle, walk/turn and sitting or forepaw-use poses; authored square-marking accents. | X | LP-0 | Mink model, source textures, rig/poses and any renderer adapter; no changing site copy | Front, back, side and elevated character sheet; wireframe/plain-material and styled stills; small-size preview on the actual hero; markings stay attached through pose changes | [ ] |
| **LP-3 — One living collaboration vignette (2–3 d).** Attach one mini workshop to the sphere with two minks, an object they work with and a concise believable 20–30 s ambient sequence (or authored frames for a static route). | X | LP-1, LP-2 | One scene, props, clips, layout preview and focused deterministic/export checks | In-page 1440/390 stills; recorded activity with grounded props and no sliding/teleporting; owner says yes to scale, light, identity and charm before adding regions | [ ] |
| **RS1 — Early artistic and simplification review.** Independent high-judgment critic reviews the real page, 360° proof, 3D mink identity and the selected medium; owner accepts the visual vertical slice. | S | LP-3 | Read-only; findings and disposition recorded in project PR/evidence | Review exposes any failed criteria or unnecessary architecture; blocking findings repaired before LP-4, no silent broadening | [ ] |
| **LP-4 — Whole-world composition (2–4 d).** Add a quiet meditating-elder moment and a cozy node-creator station, plus connecting paths, small water/trees and a restrained large landmark. Author the far side with quiet zones. | X | RS1 | Planet scene composition, two vignette configs and shared assets; no unrelated site sections | Eight-angle or full-turn recording and actual page-size stills: 3 identifiable moments, readable hierarchy and quiet surface; all objects obey curvature and shared lighting/material rules | [ ] |
| **LP-5 — Vision-page delivery and fallbacks (2–3 d).** Integrate only the selected medium at `/vision`; keep site text, nav and sky; blend pixel clouds carefully; mobile sizing, lazy loads, still poster and reduced-motion behavior. | N | LP-4 | `src/pages/Home/PublicAstridVision.tsx`, local layout/styles, one small 3D/media adapter, poster assets, corresponding tests | Five real-size views, no text/controls clipped; browser scroll and links work; still visible for media error/reduced motion/no WebGL; no empty canvas on load or CLS | [ ] |
| **LP-6 — Device proof, polish and handoff (1–2 d).** Measure before/after in production mode, trim costly effects/media, fix contrast and composition, capture exact final candidate. | N/T | LP-5 | Planet/media resources, Vision tests, workflow path filters and evidence; only scoped aesthetic polish | Focused unit/E2E and build checks; LCP/first paint/CLS versus LP-0; video/live frame samples on named devices, plus phone/laptop owner preview; no regressions | [ ] |
| **R — Final independent review (one review round).** Inspect exact App candidate, user-visible captures, provenance, performance and release scope. | S | LP-6 | Read-only review and bounded repairs as findings | Record exact candidate SHA, test selectors/results, independent verdict, owner art approval and release-owner integration decision | [ ] |

## Art acceptance at each gate

**LP-1 / shape:** A neutral-material rendering alone conveys a globe with depth. Eight views or a smooth full rotation reveal curved water, land and props, not a single façade. Shadows identify form rather than making half the planet black.

**LP-2 / identity:** The avatar's silhouette, orange hue, cream underside, small dark face and dark tail tip are still readable in a 24–48 px-ish on-page character view. Avoid requiring realistic fur, tiny facial features or a global chunky resolution pass.

**LP-3 / decisive vertical slice:** Show the actual serif headline and backdrop, not a blank studio. The activity reads as cooperation even without labels. Slow/human-looking idle is better than constant motion. This is an explicit go/no-go checkpoint; if it's merely technically functional, improve it before LP-4.

**LP-4 / world:** Fewer, stronger details. A familiar workshop, a meditative pause and a cozy creator are separated by hills, sky and quiet regions. Their characters and props are from one coherent physical style. Small Easter eggs are rewards for looking, not signs filling the composition.

**LP-5 / responsive:** Real mobile gets an intentionally cropped but recognizable planet rather than a hidden desktop illustration. The primary headline and call to action are unobscured; content still works with JS media failures.

**LP-6 / measurable:** Frame targets are provisional and apply only to animated/live routes: ≥30 FPS on a named mid-range phone and ≥50 FPS on a named laptop in a 30-second trial. For a still or video, judge decode/scroll smoothness and page performance instead. Record baseline and candidate network/memory costs; no planet-induced CLS; the failed-media and reduced-motion stills render correctly. First/Largest Contentful Paint should show no material regression relative to LP-0.

## Delivery rules

- One accountable owner carries all gates. Small implementation packets may be delegated within the gate, but no extra queue becomes the plan's authority.
- LP-0's rendering choice is binding for this release; do not build a live simulation just because the 3D source supports it.
- Capture at each gate with fixed camera, seed, site feed and source SHA. Include a short annotated verdict: **accepted / needs rework**, and the owner-facing image or clip.
- Preserve the current website's tests and copy. Do not suppress, rewrite or weaken an assertion to make the new illustration pass.
- Every implemented scene and its art/animation source must remain editable and distributable with known rights. Retain source, not merely a generated flattened picture.
- Product implementation, integration and publication require separate explicit authority and the current release's branch discipline.
