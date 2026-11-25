# Proposal — one-day packets and satellite development for Plan 84

**Date:** 23 November 2026  
**Status:** Execution proposal, not an approved new run or an update of task completion.  
**Parent records:** [Plan 84](plan.md) · [Task register](tasks.md) · [Inputs and decisions](inputs.md)  
**Purpose:** Keep the accepted living-planet product outcome intact while replacing oversized implementation tasks with bounded, verifiable work and a low-friction external development workflow.

## Summary / decision

**Propose** preparing portable planet-engine work in an independent satellite workspace (working name: **planet-lab**) and landing it into **astrid-app** through a repeatable, allowlisted source-transfer and qualification process. Do not turn the planet into a second production package, introduce a separately hosted iframe, or duplicate the site's Vision, sky or navigation code.

**Propose** breaking each large Plan 84 task into reviewable packets expected to fit at most one engineering day. The matrix below deliberately separates the roughly 9,000-line engine's systems and **one authored ground scene at a time**. Some packets are only hours; packet count is not a day count. After the first real import and one measured scene extraction, replace the original estimate with observed effort and a dependency-based schedule.

**Preserve** the existing scope, Release 15 route, manager's taste responsibility, owner look, independent review, tests, approved phone ruling and explicit authority boundaries. The Plan 84 run was stopped on 22 November 2026. This document does **not** restart it, authorize product writes, or reassign the existing manager.

If the owner accepts this execution change, the manager should translate these candidate IDs into the canonical [tasks.md](tasks.md) under the existing PL task IDs and record the decision in [inputs.md](inputs.md), **rather than maintain two competing progress registers**.

## Current source and recovered work

- Original donor: [banodoco/planet at 037293de](https://github.com/banodoco/planet/tree/037293dedf932cd12eb7ef2568017b9196b76c32), read only under the accepted Plan 84 approach.
- Already-ported production candidate: [App PR #371](https://github.com/banodoco/astrid-app/pull/371) was merged into **release/15/plan-84** at **95a061b3ba24a0bdec598da449f04ee82c6acf5c**. It brought the engine behind **PublicAstridPlanet.tsx**, with deferred loading, deterministic capture and resource tracking. Do not repeat PL-1.
- Part-complete PL-2 layout: recorded branch **plan-84/pl-2** at **0e290681**. Entry/startup repair: [App PR #372](https://github.com/banodoco/astrid-app/pull/372), recorded head **54998927** and open. Both require exact-head reconciliation and the existing acceptance route.
- Snapshot of run-1 captures/verdicts: [evidence branch](https://github.com/banodoco/astrid-dev/tree/plan-84/evidence-snapshot/plans/84-living-planet-on-the-vision-page/evidence/run-1-snapshot). The large raw capture files were not retained, so recreate any baseline needed for actual proof.
- The imported [planetEngine.ts](https://github.com/banodoco/astrid-app/blob/release/15/plan-84/src/pages/Home/planet/planetEngine.ts) has **about 9,147 lines** as inspected on 23 November; nearly all are inside **initPlanetEngine**. **createSceneControllers** occupies roughly lines **2,632–6,708**, with additional floating scenes, render loop, lighting, gesture state and cleanup in the remainder. Simple file slicing is insufficient.
- Current **setTimeOfDay** emits **onTimeChange**. A naïve Astrid-session-to-engine update would echo back to the session. The adapter needs explicit **user rotation vs applied session hour** semantics.
- The hosted unmodified Release 15 baseline passed the stated public-Vision checks, but the port's plan branch exhibited failures; not all causes were proven. Keep original assertions, isolate inherited TypeScript diagnostics from new ones, and report unknowns as unknowns.
- PL-0's SwiftShader / CPU figures are not evidence of native-phone speed or heat. The accepted phone path is lighter live by default, adaptive quality, then still poster if the device struggles.

The planned target remains astrid-app/src/pages/Home/planet/, on the App's own three.js (**0.185.1** at planning time; re-verify when dispatched). No new independent package release.

## Two codebases, one production source

| Surface | Owner | What it contains | What must not drift |
| --- | --- | --- | --- |
| **Satellite planet-lab** (proposed) | One engine writer per seam | Portable engine modules, authored scenes, engine assets, test fixtures, deterministic preview and export tooling | Built from the accepted **ported** App source, not the old donor; no App layout or fake “production” sky |
| **astrid-app integration branch** | Plan 84 App writer / manager | PublicAstridPlanet.tsx adapter, Vision layout/CSS, sky-session connection, page/navigation tests, release build | Existing content feed, headings, anchors, dialogs, page route and test contracts |
| **astrid-dev** | Existing Plan 84 management route | Accepted plan/inputs/tasks, execution decisions, evidence references | Only one status and authority record; this proposal is not a second plan |

In the satellite, use a small preview, pinned camera/clock/feed/renderer fixtures, focused tests and an export utility. A suggested nonproduction layout is **src/planet/**, **preview/**, **fixtures/**, **tests/**, **evidence/** and **scripts/export-to-app**. Do not export the preview, mock sky, third-party boilerplate or any test shortcuts into Astrid.

**Proposed interface principle:** evolve the existing **PlanetEngineAPI** and **initPlanetEngine** callbacks. Let Astrid's existing **PublicAstridSkySession** remain the sole hour owner; engine receives its hour, while a genuine user-initiated rotation reports a change outward. Distinguish the two directions without changing the hour inside an echo loop. Keep rendering, pointer input, camera, scheduling, resource registry and scene construction as separately owned modules, not a new 2,000-line “Context” object shared by every scene.

**Source-of-truth rule:** during satellite development, a portable-engine packet originates from the lab and is imported into an isolated App branch. No independent competing writer changes that portable module in App. If an urgent App-side fix does touch it, reconcile the exact patch into the lab before the next export. The App remains the final production source; the lab is a staging environment, not a separately released artifact.

## What qualifies as a one-day packet

Before a worker starts, a packet must identify the exact base SHA and exclusive writer, its target module/function and non-goals, the smallest independent outcome, dependencies, focused tests, reproducible visual/interaction evidence where relevant, and an import receipt for engine changes. The manager judges the visual output: the worker does not self-approve. **If a task cannot reasonably be built, tested and handed off in a working day, split it again before dispatch.** Several short cards may complete in one day.

**Fixed visual contract:** preserve the existing five sizes **390×844, 844×390, 820×1180, 1440×900, 1920×1080**, seed **84**, frozen pose, sky hour, browser date, content feed, drawing backend and pixel ratio. Use the existing port comparison's tolerance: at most **0.5% differing pixels above 16/255 per channel in the meaningful crop**. Investigate a difference; do not enlarge tolerance to turn failure into green. A moved scene additionally needs a frame turned to **its landmark**, because default-hero screenshots can miss damage to the far hemisphere.

### Preparation and recovery

| Packet | Independently deliverable outcome | Dependency / proof |
| --- | --- | --- |
| P-01 | Reconcile live refs, ownership, stopped-run evidence and unresolved CI failures | Read-only; record exact App plan/PL-2/PR #372 heads and custody; no product write until resumed |
| P-02 | Establish reproducible parity fixtures (five viewports, scene orientations, lifecycle counts) | P-01; pinned browser/backend/date/seed/hour/feed; nonempty real rendering |
| P-03 | Provision satellite lab seeded from the already-ported App engine | P-01; same Three version, live and still previews, no donor modifications |
| P-04 | Implement manifest-based export dry-run and isolated App import smoke | P-02/P-03; clean whitelist diff, production compile and no App-owned file collisions |
| P-05 | Qualify and integrate existing PL-2 and entry repair via the Plan 84 route | Separate authorized run; unchanged focused checks, five-size/contrast verdict, no competing writer |

### Shared engine extraction

**All C cards are parity-only.** First establish narrow explicit dependencies and resource ownership; no visual embellishment or behaviour change while moving code.

| Packet | Extract just this seam | Dependency / proof |
| --- | --- | --- |
| C-01 | Public engine types, deterministic random/clock and resource-ownership context | P-02/P-04; ten-mount lifetime proof, no all-powerful shared context |
| C-02 | World config, landmark directions, terrain masks, height/normal/walkability | C-01; sampled values and landmark positions identical |
| C-03 | Terrain mesh, surface colouring, water mesh and shader | C-02; default and landmark pixel parity, identical resource accounting |
| C-04 | Mink pixel textures, geometry and shared shadow resources | C-01; texture, geometry and resource snapshot parity |
| C-05 | Mink rigs, poses and skeletal animation functions | C-04; frozen-frame and transition parity |
| C-06 | MinkAgent traversal, movement and behaviour | C-02/C-05; deterministic motion trajectories and interaction parity |
| C-07 | Shared prop builders and surface placement (bridge, trees, cups, rocks, tools) | C-01/C-02; fixed geometry and resource parity |

### Individual authored ground scenes

**One card per scene.** Each card moves just the scene's geometry/material construction, local mutable state, update controller and hit/tap behavior into an independently callable builder. Preserve the existing landmark identifiers and animation update order. The world bridge belongs to shared props/terrain, not a fabricated additional scene. Use **C-01–C-07** as needed, calibrate one scene before dispatching many, then permit parallel independent file ownership.

| Packet | Specific landmark / scene |
| --- | --- |
| S-01 | Tea clearing |
| S-02 | Running meadow |
| S-03 | Desert rose |
| S-04 | Mystery box |
| S-05 | Astronomer |
| S-06 | Ball clearing |
| S-07 | Oil derrick |
| S-08 | Monolith |
| S-09 | Dune thumper |
| S-10 | Fargo |
| S-11 | Comfy fennec |
| S-12 | Six-fingered hand |
| S-13 | Lascaux |
| S-14 | David |
| S-15 | Painter / pillar 1 |
| S-16 | Tinkerer / pillar 2 |
| S-17 | Garden library / pillar 3 |
| S-18 | Helping hand / pillar 4 |
| S-19 | Hobbit hole |
| S-20 | Thinker |
| S-21 | Iron Giant |

**Acceptance for every S card:** fixed default + landmark-facing screenshots within established tolerance; unchanged local animation and tap result; no resource leak; safe export dry-run. A complicated scene may be split further into geometry and controller cards. The source comments duplicate the number “SCENE 19”; these S IDs intentionally avoid relying on that numbering.

### Floating set pieces and independent special cases

| Packet | One set piece | Focused proof |
| --- | --- | --- |
| A-01 | Balloon house, pops, fall and cleanup | Keyframe, interactions, detached GPU resource parity |
| A-02 | Moving castle, its legs, smoke and interactions | Construction and motion parity; split further if >1 day |
| A-03 | Little Prince and migrating birds | Keyframe and orbit parity |
| A-04 | Wright brothers' biplane, pilot and propellers | Keyframe and animation parity |
| A-05 | Bullet character, its taps and burst effects | Hit targets, animation and effect cleanup |

### Runtime, input, rendering and lifecycle

| Packet | Small structural/behavioral change | Dependency / proof |
| --- | --- | --- |
| R-01 | Assemble world from extracted scene/controller modules | Relevant C/S/A done; same scene inventory and controller update order |
| R-02 | Isolate renderer initialization, shadow policy and pixel postprocessing | C-03; mode/render target and production import parity |
| R-03 | Extract camera projection/resize without yet redesigning framing | R-02; camera values and five-size pixel parity |
| R-04 | Extract pointer/gesture/raycast behaviour | R-03; tap, drag, scroll pass-through, event cleanup |
| R-05 | Extract pure rotation↔24-hour math and user-vs-programmatic events | R-04; wrap cases, full rotation, no callback echo |
| R-06 | Extract animation scheduler, pause and offscreen/tab visibility | R-01/R-02; fake scheduler forbids hidden draws and proves resume |
| R-07 | Extract light palette and hourly shading from engine time state | R-05; identical fixed-hour darkness/brightness images |
| R-08 | Extract disposal/context-loss and complete lifecycle ownership | R-06; 10 mounts, loss/restoration, zero leaked listeners/timers/fences |
| R-09 | Module integration and parity qualification | All structural packets; no file over 1,200 lines, no new App type/lint failures |

### Astrid website and visitor features

**W packets are App-owned**, except a separately imported portable change explicitly required by the card. Do not rebuild the real Vision page in the lab.

| Packet | Visitor-visible outcome | Dependency / proof |
| --- | --- | --- |
| W-01 | Finish Foundations wrapper, hero stage, transparency, clipped-edge treatment | P-05; five-size layout, cards, links/dialogs and unchanged page tests |
| W-02 | Final camera composition and finger-scroll rules at all five sizes | W-01/R-03/R-04; viewport pictures and touch recording |
| W-03 | Wire planet and Astrid sky session as one time-of-day authority | R-05/R-07; spin updates session once, external hour does not echo |
| W-04 | Day replay, real-time reset and reduced-motion time behaviour | W-03; full-day recording and existing sky tests unchanged |
| W-05 | Poster, still/failure states and accessible controls | W-01/R-08; no blank frame or layout jump, keyboard/ARIA checks |
| W-06 | Production measurements, adaptive phone quality and still fallback | W-05/R-06; matched FCP/LCP/CLS/transfer and measured frame-time guard |
| W-07 | Late camera fly-in/arc, timed with existing 1.8-second sky reveal | W-02–W-06; five entrance recordings, first content readable, no CLS |
| W-08 | Five-size visual regression/CI path triggers and functional tests | W-01–W-07; planet-only change runs capture; WebKit/sky/links unchanged |

**Important sequencing:** Build the deterministic screenshot harness at **P-02** rather than leaving visual reproducibility until **W-08**. Finish the camera entrance **late**, after framing/time/fallbacks are stable, following the accepted owner decision.

### Taste, owner preview and release qualification

| Packet | Reviewable result | Acceptance |
| --- | --- | --- |
| Q-01 | Compare candidate with unmodified production App baseline | Matched transfer/paint/shift, functional checks and qualified infrastructure caveats |
| Q-02 | Taste round 1 with pinpoint visual correction cards | Manager opens real five-size captures; each finding gets a narrow task |
| Q-03 | Taste round 2/3 only if manager finds worthwhile remaining issues | Stop when satisfactory or at accepted round cap; no hidden scope |
| Q-04 | Owner preview of the exact final candidate on own phone and laptop | Record device, SHA, approval or follow-up; real GPU/heat limits visible |
| Q-05 | Independent review and authorized Release 15 handoff | Code/tests/metrics/source SHAs and original assertions; no merge without gates |

## Parallelism and first-week sequence

The likely critical path is **P-01 → P-02/P-03 → P-04 → C-01/C-02/C-07 → first scene calibration → scene/A extractions → R-01/R-09 → W/Q integration**. The App lane **P-05 → W-01** may run alongside lab engine work *only after the paused run is explicitly restarted* and with separate nonoverlapping writers. Serialize the camera/gesture/time seam at R-04/R-05/W-03.

**Proposed first five working days (capacity targets, not promises):**

1. Recover the actual App branch and existing PRs (P-01), fix the source identity, and start the baseline fixture (P-02). No blind write to old branches.
2. Stand up a lab from the accepted App-port revision (P-03). Complete an **unchanged-code dry-run import** into an isolated App branch (P-04), proving the transfer before feature development.
3. Move the smallest explicit construction/resource context seam (C-01); verify fixed image, resource and mount parity.
4. Extract world config/terrain functions or shared props (C-02/C-07) as the dependency graph dictates. Record actual elapsed effort and unexpected coupling.
5. Extract **one** scene, suggested **S-01 Tea**, with landmark-facing picture, interaction trace and import receipt. Use its measured cost to re-estimate the other scenes and judge whether parallel extraction is safe.

This is an execution **proposal**, not a fabricated delivery forecast. Some scene extractions may be automated and several can finish in a day; others (monolith, castle, complex mink state) may need more than one card. Re-estimate the **original approximately 16 engineering-day allowance** after the first real import and sample extraction; record engineering effort separately from calendar elapsed time and worker parallelism.

## Mandatory transfer receipt for every portable change

1. **Identity:** packet ID, exact satellite base/head commit, target App base/head, engine version, resource/scene manifest, sole writer and touched paths.
2. **Native proof:** focused unit/interaction tests; deterministic default and landmark shots; note pixel delta and accepted tolerance; lifecycle counts and frame-time measurements for affected systems.
3. **Import:** exporter runs dry first; it rejects unknown destination paths, unexpected deletion/rename and collisions, and only writes a predeclared whitelist into **src/pages/Home/planet/** on a **fresh isolated App integration branch**.
4. **App proof:** compile/production build and scoped lint/typecheck; do not claim the inherited eight TypeScript errors are caused or fixed by the packet. Run relevant existing page/sky tests unchanged, real lazy-loading test (Home and still-only Vision download no engine), screenshot/contrast tests and matched production metrics when relevant.
5. **Disposition:** accept the isolated import, send it back with specific failing evidence, or mark blocked with exact reason. **An accepted import does not authorize merge to release/main or publication.**

A successful result is a **mechanical import operation** with a map of exact satellite commits to App candidate commits and artifacts, not a final-week manual copy/paste campaign.

## Explicit constraints and decisions

- **Run remains paused.** Publishing this proposal is not permission to resume the old manager, dispatch agents, move old branches, merge product PRs, rent hardware, or ship Release 15. Resumption and landing require the established owner/Lead authorization.
- **Recover, don't overwrite:** qualify [App PR #372](https://github.com/banodoco/astrid-app/pull/372) and **plan-84/pl-2** with exact-head evidence and original tests. Keep any historical failing outcomes visible.
- **Satellite remote choice:** a new repository/workspace (provisionally planet-lab) must have its location, writer permissions and source pin chosen on resume. **banodoco/planet remains read-only** under the accepted plan.
- **No App duplicate:** don't introduce a second three.js version, a publishable npm package, an iframe, a duplicated sky clock, different Vision copy or separate content feed.
- **No reduced gates:** protect the existing 760-pixel responsive rule, all section headings/links and dialogs, reduced motion, phone lighter-live+fallback ruling, no first-paint regression, no offscreen GPU work, ten-mount cleanup, original browser assertions and five-size visual review.
- **No scope substitution:** the engine split's **1,200-line maximum per file** still applies; don't merely move the giant closure into a helper. Independently review the new architecture and the App integration.
- **Taste and approval:** manager judges screenshots, owner reviews the exact final candidate on real devices, independent reviewer judges the code/proof, Release 15 Lead/owner retains release integration control.
- **Canonical update:** after accepted, record the change in **inputs.md** and put true dispatch cards under the relevant PL IDs in **tasks.md**; remove neither completed history nor accepted owner decisions. Do not treat this proposal's candidate IDs as actual assigned statuses.

## Acceptance of the proposed execution method

The proposal earns its complexity if the first few packets show all of the following: (1) a no-op external-to-App import produces the same artifact with no hand edits; (2) a small engine extraction passes deterministic default and rotated-scene visual parity; (3) an App-specific layout or sky improvement can proceed without touching the satellite's source; (4) no competing writer or second clock is introduced; and (5) remaining effort can be re-estimated from measured task sizes rather than a large “split the engine” promise.

**Recommended next action once authorized:** verify refs/custody, establish an isolated lab from the integrated port, prove **P-04** before changing the engine, and then turn the candidate matrix into appropriately sized, evidence-backed tasks inside the existing Plan 84 register.
