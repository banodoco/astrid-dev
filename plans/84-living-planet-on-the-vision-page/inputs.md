# Inputs — A living planet on the vision page

[Plan](plan.md) · [Tasks](tasks.md) · [Art direction](art-direction.md) · [References](assets/README.md)

## Planning evidence

**Scope decision:** **Chosen by the owner on 24 November 2026.** Create the fully spherical, tactile live 3D Astrid planet for Vision, with a composed non-spinning starting view selected from the website's existing local time; horizontally rotating the planet advances or rewinds the same site-wide sky and page colours, while vertical motion does not affect time. Retain sculptural pixel-identity minks. Distinct creative units are needed for roughly eight ground scenes, four flying concepts and separate entry/exit sequences, with art sign-off for each and a final whole-world composition gate; engineering infrastructure need not be subdivided the same way.

**Prior art and surfaces (observed 24 November 2026):** The public Vision page is in `banodoco/astrid-app` at `src/pages/Home/PublicAstridVision.tsx`, with existing Vision navigation, sky and content feed. The owner supplied page screenshots and conceptual images; exact copies and their roles are in [assets](assets/README.md). An experimental 3D planet exists in [banodoco/planet](https://github.com/banodoco/planet); code there may be consulted or selectively reused after checking its current provenance, suitability, runtime cost and rendering medium. No source code or images are assumed production-ready from their existence alone.

**Approach and alternatives:** A still, video and live renderer are not equivalent for this product: only **live 3D** permits a visitor to inspect the real far side and use the planet as a physical time scrubber. Three.js is therefore the required browser runtime. An authored still remains necessary for loading and WebGL/reduced-motion fallback; pre-rendered material may be used for screenshots, evidence or the poster, but **not as the primary delivery**. Orthographic or gently perspective projection is an artistic camera choice, not a restriction on interaction.

**Verified source contracts:** `PublicAstridSite.tsx` passes one `PublicAstridSkySession` to both Home and Vision. `publicAstridSkySession.ts` exposes `getSnapshot()` / `getControlsSnapshot()`, `subscribe` / `subscribeControls`, `setManualHours(hours)`, `setNow()`; defaults `hours: null` to the visitor's zoned wall-clock hour; computes sun times and seasonal palette; `publicAstridSkyRender.ts` owns the paper/ink dusk logic. Preserve these definitions and the Home replay/preview; don't duplicate them in the planet. The optional `banodoco/planet` study has `setTimeOfDay` and `onTimeChange`, but its external setter calls its own callback; adopt only with a non-echoing inbound path.

**Gesture contract:** define “right later / left earlier” in screen coordinates. Map horizontal yaw continuously to unwrapped hours at 24 h / 360°, with a configurable pixel-to-radian sensitivity; wrap only when displaying/publishing time. Pitch/vertical inspection is a separate bounded value, never used to derive time. Vertical touch movement scrolls the page; horizontal intent must be deliberate. Explicit horizontal rotation enters manual mode; a visible “Live” action returns the sky and planet to the current local hour. The sky session remains the source of truth in either mode.

**Polish contract:** after the functioning website and approved resting composition, author an approach/fly-in with a graceful camera arc, a matched retreat/exit on leaving Vision, and a few tiny independent flying objects (e.g. bird silhouettes, floating pixel particles or a small glider). The camera alone moves during transitions; do **not** edit selected time, yaw or site palette. Keep flying objects sparse and correctly lit/occluded. Stage performance testing and reduced-motion/nonblocking navigation with the polish.

**Simplification challenge:** The dominant risk is scope expanding into a giant animation/simulation project before the first composition looks right. Use one complete collaborative scene to lock the style before producing seven other individually directed scenes; the whole sphere needs deliberate geographic breathing room. Put the owner visual gate after one finished collaboration scene. Independent high-judgment design/engineering critique is **pending** and required before production implementation; do not report it as completed.

**Proof and limits:** [Plan completion](plan.md#completion) and [tasks](tasks.md) require mathematical and UI witnesses for clockwise/counterclockwise wrap, pure Y-screen drag with **zero** clock writes, no loop from external sky updates, four daypart entry positions, real site palette response through twilight, and correct “Live” restoration. Visual claims require the real Vision layout and deterministic 3D source, not generated concept stills. Performance budgets are provisional until named device tests and a production baseline exist.

**Review rounds:** One independent technical-scope critique before build (RS0), one art/experience critique after the first complete scene (RS1), and one integrated final review (R), with bounded rework. The owner can adjust the budget at run start.

**Run start:** **No product execution authority from this planning update.** Record a fresh owner start message, accountable session, exact App branch/source and integration owner before changing product code. The previous project queue is not a delegated run.

## Owner decisions

- **D1 — Full living sphere (decided 24 November):** One genuinely three-dimensional, rotatable miniature globe with curated low-poly terrain, pixel/3D layering and recognizable sculptural minks on the Vision page.
- **D2 — Default pose (decided 24 November):** On entry, the stationary globe faces the longitude defined by the site's *current effective local time*, not a fixed image and not auto-rotation.
- **D3 — Horizontal time mapping (decided 24 November):** Drag right moves later, drag left earlier; 360° is 24 hours. The **existing Home/Vision shared sky session** owns time, background and theme; a turn sets manual hours, while a clock/preview update only reorients the globe without an echo.
- **D4 — Vertical gesture (decided 24 November):** Vertical movement does not change time/background. Bounded pitch is optional; vertical touch scrolling must remain natural.
- **D5 — Return to present (derived implementation):** Offer a visible accessible “Live”/“Now” control to call the session's existing `setNow()` after a manual turn; the same sky contract handles seasonal sunrise/sunset and the page palette.
- **D6 — Resident identity and creative scene production:** The 3D minks remain sculptural versions of the pixel mascot. Plan eight individual scene art units based on the discussed ideas, with a workshop style lock, short per-scene art verdicts and small-batch owner looks. The final density is judged by the complete planet, not a scene count.
- **D7 — Cinematic/aerial creative units:** Entry camera fly-in, exit choreography and four candidate flying-object groups receive individual art briefs and acceptance. A shared airspace composition review prevents visual noise; none may change the site's hour.
- **D8 — Remaining tuning (delegated at run start):** Exact camera duration/easing, 360° drag sensitivity, bounded pitch range, flying-object selection and performance step-down are art/engineering judgments validated against screenshots, video, accessibility and user comfort.

## Source identities

Observed, not execution pins: astrid-dev `main` at `0b1c9fd0e3bd063caa4b412e8bf3e90bf02ab2c4`; astrid-app `release/15/main` at `2e61a5dbdbeda503fdd70431bb556b7b4f5691b8`; its existing `release/15/plan-84` branch at `95a061b3ba24a0bdec598da449f04ee82c6acf5c`; and banodoco/planet `main` at `32f8dd63b9ffafcd18d2f1c34109f4c5e4b37b75`. These are investigation references, **not instructions to merge**. At LP-0 reread the exact live heads, inspect any open App work and record a non-destructive plan for the new implementation branch, then follow the active Release 15 integration rules. If Release 15 no longer has room, request an owner scheduling decision rather than forcing a late landing.

## References

- [Detailed art specification](art-direction.md) and [source/visual reference manifest](assets/README.md).
- [Astrid Vision page source](https://github.com/banodoco/astrid-app/blob/release/15/main/src/pages/Home/PublicAstridVision.tsx).
- [Planet authoring study](https://github.com/banodoco/planet).
- [Astrid app Vision checks](https://github.com/banodoco/astrid-app/blob/release/15/main/.github/workflows/public-vision.yml).
- [Release 15](../../releases/15.md), [run contract](../../skills/shared/run-contract.md), and [project-format rules](../../docs/project-format.md).
