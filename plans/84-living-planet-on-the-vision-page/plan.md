# A living planet on the vision page

**Project:** A living planet on the vision page

**Goal:** Visitors to Astrid's public Vision page encounter a beautiful, unmistakably spherical, miniature 3D world that feels inhabited by the open-source creative community, with sculptural orange mink, small discoveries, and an aesthetic that belongs to Astrid's editorial and pixel-art website.

**Status:** queued

**Owner:** Unassigned — one accountable delivery owner is appointed at run start.

**Estimate:** 12–20 engineering days for the seven delivery gates (first-principles estimate; calibrate after the first complete scene). Visual review and release waits are additional.

**Waiting on:** A fresh run start, a nominated delivery owner, a rendering approach chosen from the first prototype's evidence, and visual approval at the first complete-scene gate. No implementation starts from this plan alone.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md); its priority is its place in [priority.md](../../plans/priority.md).

**Vision gaps:** [CA-003 — Our vision and execution aren't yet fully connected](../../vision/gaps/CA-003-vision-experiments-progress.md) (primary). The page should *show* the shared creative ecosystem, not merely describe it.

## Outcome and scope

On `/vision`, a tactile little planet sits to the right of the editorial vision statement. It has a **genuine continuous sphere**, not a flat display island: rounded terrain, a coherent waterline, tiny paths and scenery that follow the curvature, landmarks that emerge around the horizon, and an authored far side. It feels as if it *could* rotate even when it does not.

The planet's physical language is restrained low-poly/sculpted 3D: warm directional sunlight, enough fill to preserve shape, local contact shadows, matte surfaces and very selective texture. Astrid orange minks are small three-dimensional interpretations of the pixel mascot, with its long body, simple face, cream underside and dark tail tip. Pixel clouds, authored mink markings, signs and little effect particles tie the 3D scene to the cream/peach, serif-led website. **Do not pixelate the entire image**.

The world feels lived in without becoming crowded. Compose two or three recognizable landmarks and three distinct small moments, connected by paths and quieter geography:
- **Collaboration:** two or three minks building, moving or discussing something at a little creative workshop.
- **Reflection:** a tiny meditating elder-like resident on a quiet rise; the reference is an affectionate Easter egg, not a literal copied character.
- **The cozy creative desk:** a small inhabitant at a workstation with a few node-like pixel accents, a subtle nod to creative AI tooling and ComfyUI culture without copying specific copyrighted designs.

A small bridge, tree, water feature, or observation point may connect these. Scale is important: use recognizable but modest landmarks, smaller mid-scale scenery and very small inhabitants and details. Preserve substantial quiet terrain; the whole composition must read at the actual hero size, not just enlarged in a renderer.

**Delivery form:** editable **3D source**, plus the lightest browser presentation that achieves the visual goal. The default page view is deliberately composed and **does not auto-rotate**. At LP-0, compare a high-quality still, a small pre-rendered ambient loop, and live Three.js; choose on demonstrated quality, speed and usefulness, not because an existing engine can do more. If the shipped experience is a still or rendered loop, it remains a genuinely 3D-authored planet. Build scene placements so a later interactive turn is possible, but rotation and user interaction are **not required to ship**.

**Included:** initial camera and terrain; one coherent 3D mink identity with a small pose library; three readable community vignettes with subtle activity where affordable; pixel/3D compositing; responsive Vision-page layout; an authored poster/still fallback; reduced-motion and no-WebGL behavior; and measurable performance and accessibility.

**Outside this project:** changing the Vision copy or the Pillars/Principles navigation and content; redesigning the homepage (`/`); a complex autonomous multi-agent simulation; dozens of scenes or famous-character replicas; click-to-control inhabitants; automatic planet rotation; a time-of-day control coupled to rotation; audio; extensive GPU effects; and engineering work solely to preserve a particular existing implementation.

## Existing work and decision

The public Vision page and its sky, typography, links and content feed already live in [astrid-app](https://github.com/banodoco/astrid-app), under `src/pages/Home/`. The working [planet study](https://github.com/banodoco/planet) provides optional reusable code and art evidence; [the checked-in references](assets/README.md) show the actual page language, mascot identity and spherical design. At LP-0, measure which pieces are useful and whether simpler 3D authoring plus a still/loop would produce a better result.

The preferred approach is **visual vertical slice first**: prove the sphere, the shared mink silhouette and one complete activity in the real page before populating the globe or investing in general-purpose runtime architecture. Do not require a large engine split unless the chosen runtime and measurements demonstrate a genuine need. See [inputs.md](inputs.md) for source identities, choices, review and authorization.

## Sequence and readiness

| Gate | Deliverable and go/no-go proof | Indicative effort |
| --- | --- | ---: |
| **LP-0 — Scene contract and baseline** | Named source SHAs; screenshots in five viewports; 3D-authoring/runtime choice supported by a small comparison; approved initial globe size, camera, palette and simple composition map | 1–2 d |
| **LP-1 — The globe** | Continuous 3D sphere, sculpted topography and clean light; gray-material and shaded 360° turntable; reads as a full planet from side and back and at actual page scale | 2–3 d |
| **LP-2 — The Astrid mink** | One scalable, fully volumetric mink, three poses and its restrained pixel identity; four-angle sheet plus small-size website comparison | 2–3 d |
| **LP-3 — One complete living scene** | Two minks collaborating in an art-directed area, with at least one coherent short activity and contact/shadows; a 20–30-second clip and real-page still approved by the owner | 2–3 d |
| **LP-4 — The whole miniature world** | The reflection and cozy-workstation scenes, connecting terrain, modest landmarks and quiet areas; full-turn inspection; three discoverable stories without visual clutter | 2–4 d |
| **LP-5 — The website experience** | The chosen poster/loop/live rendering mounted on `/vision`, responsive and correctly layered with existing pixel clouds and text; lazy loading, reduced-motion and still fallback | 2–3 d |
| **LP-6 — Final taste and technical proof** | Device, performance, regression and accessibility evidence; the owner approves the exact integrated preview; independent review and release handoff | 1–2 d |

**Critical decision:** LP-3 is the art-direction lock. If one small complete scene is not compelling at normal page size, correct it *before* adding more places. The LP-0 delivery-mode choice may eliminate substantial WebGL and simulation work.

Gate dependencies and checks are in [tasks.md](tasks.md). The project remains listed for Release 15; a fresh run must confirm a valid product branch and available release window before executing it. No change to this plan is a deployment or a release go.

## Interfaces and handoff

**Consumes:** the approved [art direction](art-direction.md), [versioned visual references](assets/README.md), existing `/vision` page and content feed, and the actual product source refs recorded at LP-0.

**Produces:** editable 3D project/source (code or authored models, with sufficient asset provenance), named terrain/inhabitant/scene composition, a hero-sized final render or renderer, a poster fallback, and the integration in the Vision page. If the live option wins, retain deterministic world setup, bounded resources and a contained renderer; if pre-rendered media wins, retain the 3D authoring scene and deterministic export recipe so the world is extendable.

**Compatibility:** preserve existing vision copy, links, sky session and content feed. Keep browser events and page scrolling available. The specific App branch and transfer path are selected from current observed heads at run start; do not merge an unreviewed prototype or change a published page outside the release process.

## Completion

The exact integrated candidate is accepted only when:

1. **A real planet:** an untextured 360° turntable proves a continuous globe with believable terrain and true far-side geography. The approved 3D source is retained.
2. **One aesthetic:** the site screenshot, 3D world, pixel clouds and mink read as a single Astrid design; no global pixel filter, generic toy-film character look or oversized forest of unrelated props.
3. **Recognizable mink:** a 4-angle character sheet and 3 poses match the pixel-mink identity, including orange, cream underside, dark-tipped tail and simple proportions.
4. **Three discoveries:** collaboration, reflection and cozy creation are recognizable in normal-size views; at least one vignette has meaningful, subtle motion if the approved delivery medium supports it. An edited render can substitute for runtime animation; interaction is not required.
5. **Hierarchical composition:** the sphere is clear in the hero, with two or three landmarks, small inhabitants, meaningful empty land and no collision with text. One static approved pose is sufficient.
6. **Responsive:** captures at 390×844, 844×390, 820×1180, 1440×900 and 1920×1080 show readable copy, a deliberate crop and reachable links. The planet is not simply hidden on phones.
7. **Accessible and resilient:** reduced-motion, media failure and unsupported WebGL show an authored still; scrolling, keyboard navigation, links and page contrast continue to work.
8. **Fast enough on real devices:** measure frame times only for live/animated modes; provisional targets are ≥30 FPS on a named mid-range phone and ≥50 FPS on a named laptop. Capture actual results and choose a cheaper medium if needed. No measurable layout shift caused by the planet and no material worsening of first/Largest Contentful Paint against the LP-0 baseline.
9. **Proved and landed:** focussed Vision-page tests and image comparisons pass without weakening existing assertions; source licences and asset provenance are known; the owner reviews the exact preview, an independent critic records findings, and release integration/publishing use their normal explicit authorization.

No criterion is satisfied solely by a generated mockup, a designer's isolated still, or a generic green build without the real Vision page.
