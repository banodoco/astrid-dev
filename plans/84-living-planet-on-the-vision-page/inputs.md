# Inputs — A living planet on the vision page

[Plan](plan.md) · [Tasks](tasks.md) · [Art direction](art-direction.md) · [References](assets/README.md)

## Planning evidence

**Scope decision:** **Chosen by the owner on 24 November 2026.** Create the fully spherical, tactile miniature Astrid planet for the Vision-page experience, with small 3D versions of the pixel mink, layered website pixel elements and discoverable community/cultural references. Keep a composed nonrotating starting view; the 3D authoring should allow later rotation. The owner asked for the existing Plan 84 folder to capture this complete project from first principles, with actual sequencing and benchmarks.

**Prior art and surfaces (observed 24 November 2026):** The public Vision page is in `banodoco/astrid-app` at `src/pages/Home/PublicAstridVision.tsx`, with existing Vision navigation, sky and content feed. The owner supplied page screenshots and conceptual images; exact copies and their roles are in [assets](assets/README.md). An experimental 3D planet exists in [banodoco/planet](https://github.com/banodoco/planet); code there may be consulted or selectively reused after checking its current provenance, suitability, runtime cost and rendering medium. No source code or images are assumed production-ready from their existence alone.

**Approach and alternatives:** We need a fully three-dimensional *authored world*, but a real-time 3D browser renderer is a distinct decision:
- **3D-authored still:** fastest and most accessible; no ambient movement or runtime turns. Suitable if visual quality and page clarity dominate.
- **3D-authored ambient loop plus poster:** gentle life without a large simulation; movement is authored rather than interactive. Likely efficient for the intended initial experience if compositing/codec/device tests pass.
- **Live browser 3D:** most flexible for future rotation and real-time light/interaction, but introduces GPU, canvas and mobile cost. Choose only if the prototype's distinctive value justifies it.

**Recommended route:** Create editable 3D content, perform a short LP-0 render-mode experiment using the actual Vision layout, then select the least complex shippable presentation. In all routes, preserve the possibility of reusing the world source for a later interactive version.

**Simplification challenge:** The dominant risk is scope expanding into a giant animation/simulation project before the first composition looks right. Bound the first result to three recognizable scenes, a small cast and limited ambient activity. Put the owner visual gate after one finished collaboration scene. Independent high-judgment design/engineering critique is **pending** and required before production implementation; do not report it as completed.

**Proof and limits:** The acceptance cases are in [plan.md](plan.md#completion) and evidence gates in [tasks.md](tasks.md). Visual quality is judged by the owner on the actual page and five device sizes, not an arbitrary model score. Benchmarks for speed are proposed until LP-0 records named device profiles and a production baseline. Still/video delivery will not receive spurious runtime-FPS claims.

**Review rounds:** One independent simplification review at RS0 before build, one art/experience critique after the LP-3 vertical slice, and one final integrated review; use targeted fixes and avoid open-ended polish. The owner can adjust the budget at run start.

**Run start:** **Not yet authorized for product implementation.** Owner's instruction authorizes this project rewrite and its planning PR. A fresh owner start message must name one accountable delivery owner, working repository/branch, budget and approvals; prior sessions and task boards do not grant execution authority.

## Owner decisions

- **D1 — The goal (decided 24 November):** One genuine miniature globe in the Vision hero; sufficiently physical and coherent to support multiple viewpoints, warm low-poly/diorama materials, Astrid pixel layering and tiny personal community references.
- **D2 — The opening state (decided 24 November):** Compose it to appear stationary; rotation need not run or be interactive in this delivery, although the underlying 3D content should support later turning.
- **D3 — Identity (decided 24 November):** 3D minks and Pixieminks coexist as two interpretations of one icon. The 3D form stays simplified; use the same anatomy and distinctive markings, not fur realism.
- **D4 — Personal discoveries (decided 24 November):** Include small, readable moments such as collaborating minks, a meditating elder and a cozy Comfy-inspired creator. Match their material/scale to the same world.
- **D5 — Rendering path (to decide during LP-0):** Still, pre-rendered loop or live 3D, based on visual quality, accessibility and benchmark evidence; owner reviews the recommendation if the tradeoff changes the visual outcome.
- **D6 — Art lock (to decide after LP-3):** Owner sees the first small complete scene in the real page and decides whether to proceed to full-world population or revise the look.

## Source identities

Observed, not execution pins: astrid-dev `main` at `0b1c9fd0e3bd063caa4b412e8bf3e90bf02ab2c4`; astrid-app `release/15/main` at `2e61a5dbdbeda503fdd70431bb556b7b4f5691b8`; its existing `release/15/plan-84` branch at `95a061b3ba24a0bdec598da449f04ee82c6acf5c`; and banodoco/planet `main` at `32f8dd63b9ffafcd18d2f1c34109f4c5e4b37b75`. These are investigation references, **not instructions to merge**. At LP-0 reread the exact live heads, inspect any open App work and record a non-destructive plan for the new implementation branch, then follow the active Release 15 integration rules. If Release 15 no longer has room, request an owner scheduling decision rather than forcing a late landing.

## References

- [Detailed art specification](art-direction.md) and [source/visual reference manifest](assets/README.md).
- [Astrid Vision page source](https://github.com/banodoco/astrid-app/blob/release/15/main/src/pages/Home/PublicAstridVision.tsx).
- [Planet authoring study](https://github.com/banodoco/planet).
- [Astrid app Vision checks](https://github.com/banodoco/astrid-app/blob/release/15/main/.github/workflows/public-vision.yml).
- [Release 15](../../releases/15.md), [run contract](../../skills/shared/run-contract.md), and [project-format rules](../../docs/project-format.md).
