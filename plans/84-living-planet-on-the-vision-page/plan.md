# A living planet on the vision page

**Project:** A living planet on the vision page

**Goal:** Astrid's public Vision page presents a tactile, real-time rotatable 3D planet with expressive pixel-identity minks; its facing angle reflects the same local time as the existing sky, and horizontal turns move that sky and the site's palette forward or backward through the day.

**Status:** queued

**Owner:** Unassigned — one accountable delivery owner is appointed at run start.

**Estimate:** TBD after eight individually scoped scene briefs, four flight concepts and the two camera treatments are sized; the previous 18–28-day estimate only allowed for three scenes.

**Waiting on:** The owner to launch the fresh ChatGPT/Codex run with one accountable Lead and an authorized release base. Routine feedback never blocks; four major artistic direction gates and final publication require explicit decisions.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md); its priority is its place in [priority.md](../../plans/priority.md).

**Vision gaps:** [CA-003 — Our vision and execution aren't yet fully connected](../../vision/gaps/CA-003-vision-experiments-progress.md) (primary). The page should *show* the shared creative ecosystem, not merely describe it.

## Outcome and scope

On `/vision`, a tactile miniature planet sits in the hero alongside Astrid's editorial statement. It is **a genuine interactive three-dimensional sphere**: a continuous round horizon, sculpted hills and valleys, water and paths following its curvature, and inhabited places around the far side. The world feels like a small low-poly diorama built on a planet—not a floating island or decorative picture.

**The first view is stationary but time-dependent.** On entering Vision, the visible longitude is calculated from the effective hour in the website's existing shared `PublicAstridSkySession`. It should show a different side at 08:00, 14:00 and 21:00. It does not auto-spin when left alone.

**The planet is an interactive 24-hour dial.** A horizontal drag right advances time; dragging left rewinds time. One full horizontal turn equals exactly 24 hours, smoothly wrapping at midnight. The planet's longitude, sunlight, pixel sky, cloud/night appearance and page background and reading palette all stay synchronized with the existing time-of-day sky. Vertical drag, if enabled for limited pitch, **does not alter time or background**; on touch devices normal vertical page scrolling takes precedence. The direction requirement is expressed in screen-space, not as an ambiguous Three.js X/Y-axis name.

**One authoritative clock:** the existing sky session already knows the visitor's timezone and seasonal sunrise/sunset. Home and Vision share it. The planet receives session-driven effective hours (including real clock ticks, manual preview or replay) and follows them **without echoing a time change**. Only user-initiated horizontal rotation calls `setManualHours`. A clear “Live / return to now” action calls `setNow` and restores the correct hemisphere. The planet has no second clock or independent day/night formula.

The physical language is restrained, sculpted low-poly 3D: soft matte materials, warm sunlight and enough fill to maintain volume, appropriate local contact shadows, and subtle terrain texture. Pixel styling lives on the miniature characters' markings, signs, information effects and surrounding pixel clouds, rather than a full-frame resolution filter. The orange 3D mink is one interpretation of the same pixel mascot: elongated body, narrow neck, tiny face and ears, cream underside and dark-tipped tail.

**Eight distinct creative scene concepts** form the proposed story portfolio, distributed across the globe: collaborating minks, a tea clearing, a circling game, the solitary rose keeper, a mysterious object, the astronomer, a meditating elder and a cozy creative workstation. Every scene gets an individual art brief, implementation and aesthetic verdict, while the **whole world** gets a separate composition approval. This is not permission to crowd eight features onto the front hemisphere; see the [creative units](creative-units.md).

**Polish is a separately gated part of delivery:** once the world, time-scrubbing controls and page framing are stable, add a **camera fly-in with an arc** on Vision entry, a complementary camera pull-back/arc or thoughtful dissolve on exit, and **four individually art-directed flying elements** (proposed bird flock, tiny glider, balloon traveller and one original airborne oddity), each with its own approval. These are composed details, **not** giant attention-grabbing set pieces. Their animation must never change the selected clock hour or produce an unsolicited planet spin. Honour reduced-motion, navigation interruptions, loading and the site's existing page transitions.

**Included:** a lazy-loaded contained Three.js canvas; editable spherical terrain, the eight-scene creative portfolio, one canonical 3D mink and a small set of poses; the bidirectional sky-hour/longitude contract; drag/keyboard/time-reset interaction; responsive composition; a matching still for loading, reduced motion and WebGL failure; an authored entry and exit experience; a few carefully placed flying objects; and measured mobile/desktop performance.

**Not included:** rewriting Vision copy, Pillars/Principles behaviour or Home page; dozens of equally detailed destinations, complicated interactive character dialogues, persistent agent-memory simulation, auto-rotation at idle, a second clock, literal third-party character models, unrelated engine parity work, audio or independent product publication.

## Existing work and decision

The Astrid public site already owns a single time-of-day system. In `astrid-app/src/pages/Home/publicAstridSkySession.ts`, the sky session derives `hours` from the visitor's local timezone by default, keeps manual and replay modes, derives a sunrise/sunset-dependent palette, and exposes `getSnapshot`, `subscribe`, `subscribeControls`, `setManualHours` and `setNow`. `PublicAstridSite.tsx` creates that one session and passes it to Home and Vision. The actual sky's rendering and page colour tokens are derived in `publicAstridSkyRender.ts`. **Use these existing contracts; do not build new palettes or timekeeping for the planet.**

The optional [planet authoring study](https://github.com/banodoco/planet) contains useful 3D geometry and time hooks. Its `setTimeOfDay` setter currently calls `onTimeChange`, however; this would echo external changes if connected naively. Design separate external-time input and user-rotation output, and validate both directions with tests. The art target is defined by [art-direction.md](art-direction.md), with [versioned reference assets](assets/README.md).

The smallest sound approach is **one live vertical slice first**: real sphere + proven sky coupling and drag mapping; then a recognizable 3D mink; then one beautiful collaborative scene in the actual page. Only after that visual approval add more scenes, page integration and polish. A static/poster image is solely a fallback, not an alternative to interactive live 3D.

## Sequence and readiness

| Gate | Complete deliverable and proof | Indicative effort |
| --- | --- | ---: |
| **LP-0 — Time/interaction contract and baseline** | Exact App/planet SHAs and baseline captures at five viewports; mapped sky API, yaw sign, drag sensitivity, pitch/scroll rules, and clock-to-planet event boundaries; independent scope check | 1–2 d |
| **LP-1 — Live, clock-coupled globe** | Real Three.js spherical terrain, gray and shaded 360° turntable; orientation reads the effective sky hour on entry; right/left scrub changes the real page sky and colour, vertical does not | 3–5 d |
| **LP-2 — Definitive 3D mink** | Four-angle and three-pose mascot, proper volumetric proportions, selective pixel texture identity, web-scale render and lighting | 2–3 d |
| **LP-3 — One complete vignette** | Two collaborating minks with a coherent animated activity; 20–30-second recording and in-page visual approval; independent art critique | 2–3 d |
| **LP-4 — Creative scene portfolio and globe composition** | Seven independent scene art units after the workshop style lock, followed by an atlas/composition pass; each receives a distinct visual verdict | Sized per scene at art review |
| **LP-5 — Responsive live integration** | Shared-session controller, drag/keyboard, return-to-now, Home/Vision continuity, sun/sky/background synchronization, five responsive views, reliable still/reduced-motion fallbacks | 3–4 d |
| **LP-6 — Cinematic and flying-object portfolio** | Separately art-direct the entrance, exit and four flying concepts; then review the entire choreography for scale, silence, occlusion and motion | Sized per concept at art review |
| **LP-7 — Final quality, performance and release** | Exact integrated screenshot/video proof, device/CI/accessibility results, independent review, owner look, release handoff | 2–3 d |

**The first two internal quality checkpoints:** (1) LP-1: is the shared hour ↔ globe direction mathematically and interactively correct? (2) LP-3: is one complete little scene genuinely charming and visibly Astrid? The manager/reviewer establishes the style grammar, then requests explicit **VG-STORY** human approval before committing to all remaining character-driven scenes. Each later scene and flying object receives its own internal art verdict and optional human feedback; the whole-world and cinema direction have their own human VG gates. Do not compensate for a failed early gate by adding more objects or effects. Timing/visual taste for polish is judged after page framing, so the intro does not dictate the camera composition.

Use [tasks.md](tasks.md) for task/creative-unit milestones and the [ChatGPT orchestration and human feedback guide](chatgpt-orchestration.md) for actual Codex session dispatch. Share every meaningful creative outcome with a verified preview and optional questions; **the four human load-bearing style/story/world/motion gates do require explicit direction before dependent art progresses**. Technical and other unrelated work continues, and release approval is separate. Release 15 membership is retained, but a fresh run must confirm the available release window and the correct current product branch before execution.

## Interfaces and handoff

**Consumes:** [art-direction.md](art-direction.md), [assets/README.md](assets/README.md), the current `/vision` layout and content feed, and the **existing shared sky session** `getSnapshot`/`subscribe`/`subscribeControls`/`setManualHours`/`setNow` with timezone-aware sunrise/sunset and palette. Record exact App/planet/release heads at LP-0.

**Produces:** a real-time, lazy-loaded Three.js planet with editable 3D geometry, scenes, mink rig and subtle flying-object paths; pure tested hour↔yaw mapping; a sky-session adapter with **zero feedback loops**; bounded pitch and accessible input; an authored fallback; camera-only entry/exit sequences; responsive integration and evidence recordings.

**Compatibility:** the planet follows external sky-time changes and changes the shared session only in response to explicit user horizontal gestures. Existing Home replay, manual sky preview, “Live” reset, twilight readability, website copy, navigation and page scrolling remain. Entering/exiting Vision must not advance, reset or desynchronize the clock; changes to routing or deployment require their own release authority.

## Completion

The exact integrated candidate is accepted only when:

1. **Genuine shape and interaction:** neutral-material turntable proves a complete globe with far-side geography, and visitors can rotate it in the live site, not a still/video substitute. No idle auto-spin.
2. **A stable time-based opening:** at fixed test times (00:00, 06:00, 12:00, 18:00) the planet shows four distinct, repeatable longitudes on entry, with no blank frame or jump.
3. **Directional 24-hour mapping:** drag right = later, left = earlier, one full horizontal revolution = 24 hours; 23:30 + 2 hours = 01:30. Pure vertical dragging does not write any time; diagonal motion uses only its horizontal component for the clock.
4. **One site clock:** page colours, sky, globe orientation and its sunrise/sunset-aware lighting agree during drag, Home/Vision navigation, manual preview, replay, real-clock change and “Live / return to now”. External setting must never echo through the planet to the sky session.
5. **One visual identity:** sculptural mini-world, matte low-poly surfaces, small landmarks and ample quiet space; pixel clouds/accents and recognizable 3D Astrid minks match the editorial website from normal reading distance.
6. **Eight individually reviewed discoveries:** makers, tea, running game, rose, mystery, astronomer, meditation and cozy creator have recognizably different moods and on-page proof. The collaborating pair has a believable 20–30-second scene. The final globe preserves quiet geographic space.
7. **Responsive, readable and controllable:** actual page captures at 390×844, 844×390, 820×1180, 1440×900 and 1920×1080; links/text remain reachable, touch vertical scroll works, and accessible keyboard/reset controls exist.
8. **Cinematic entry and exit:** entry camera flies in and arcs into the *current-hour* pose; exit pulls away/arcs or dissolves deliberately in coordination with page transition. The movement changes camera view only, not the effective hour or the user's selected longitude. Interrupted navigation and loading show no jump, input lock, empty frame or layout shift. Reduced motion bypasses fly-through.
9. **Flying accents:** four individually art-directed aerial candidates each have a distinct silhouette, trajectory, realistic scale and acceptance record; the final orchestrated sky does not display everything at once. They do not overwhelm the scenes or change the time; pause when off screen and respect reduced motion.
10. **Measured technical quality:** named phone/laptop tests record frame times and visual degradation; provisional target ≥30 FPS midrange phone and ≥50 FPS laptop over 30 s, to be calibrated with device evidence. No material worsening of first/Largest Contentful Paint against baseline; no planet-caused layout shift, stable resource disposal and authored still on WebGL failure.
11. **Independent and owner acceptance:** focused existing Vision/sky tests pass without weakened assertions; exact final SHAs, screenshots, drag-through-dusk and intro/exit recordings, asset provenance and independent review are recorded; four load-bearing creative approvals are tied to exact proof, and final release go remains explicit.

No criterion is satisfied by a generated concept render or an isolated 3D beauty shot without the actual page and shared sky.

