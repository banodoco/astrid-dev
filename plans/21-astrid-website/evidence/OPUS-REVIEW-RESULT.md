# Opus second opinion: homepage journey build plan (v2)

Reviewed: the v2 engineering guide (superseded by `PLAN.md`), `DEEP-PASS-RESULT.md`, the round 4 brief (in the owner's mockup workspace, not in this repo), the round 4 frames (`mockups/`), and astrid-app at `17e46de99`. Two decisions from 20 Oct are taken as already in the plan: **every asset is a placeholder for now**, and **the private preview is a multi-file Claude Artifact**. Paths use the guide's prefixes (`H/`, `V/`, `J/`).

## Verdict

1. The plan is buildable. The hard engineering is correctly identified and correctly tiered: the snapshot publisher, the director rules and the scroll-driven sky.
2. The biggest miss is that **the hero is already a live 3D stack.** Its four live surfaces sit in a `preserve-3d` parent with their own `translateZ`, and every App/Agent switch re-stacks them. The plates, captures, corner-matched handoff and plate-to-live crossfade (S2, A6, T7, half of T18) all solve a problem that doesn't exist. The exploded stack should be a third arrangement of the live surfaces.
3. Craft is under-owned. Copy, timings, the 3D view's look, §2 on phones, the tray motion and the finale sit with Luna or Sonnet, or with nobody. Taste arrives late, gets one session per moment, and has no shared motion tokens and no way to watch motion.
4. It is over-built in places (15 XHARD tasks, visitor GPU detection, IO plus reconciliation, measured overlays, two spikes on things that are already known, a five-viewport matrix on every task). It underrates phones: the stacked phone hero has to become a sticky stage, and the iOS toolbar resize repaints the sky.
5. Fix: re-pose the live editor, front-load one Opus sheet and a capture harness, cut the receipt and plate machinery, and make the Artifact preview a day-one spike with a LAN fallback. That gives about 29 tasks, 8 of them XHARD.

## 1. Difficulties

**Checked against astrid-app:**

| Claim | Status | Evidence |
|---|---|---|
| Live surfaces can't go into the 3D stack ("overflow clipping and 3D don't mix", W7) | **Wrong.** `overflow:hidden` only flattens each surface's own contents. The surfaces are already direct 3D children. | `.astrid-editor-tilt` and `.astrid-editor-surfaces` are `preserve-3d` (`H/PublicAstridShell.css:394,403`). Each surface has `translate3d(…, -175px…160px)` per audience (`:870-953`). Assembly is `rotateX(5deg) rotateY(-8deg) scale(.9)` (`:891`). DOM at `H/PublicAstridMountedEditor.tsx:118-146` |
| Poll adoption is viable for scripted snapshots | **True.** Invalidation refetches at once. Commit is a 0 ms `setTimeout`, and a newer snapshot cancels a pending one. Only drag or resize defers it, not playback. The public provider hard-codes `configVersion: 1`, so a journey provider is needed, as the guide says. | `V/hooks/usePollSync.ts:66-74,97-114,336-375`; `V/hooks/useTimelineQueries.ts:8` (30 s fallback poll); `H/publicAstridExample.tsx:142-160` |
| Clips keep keys; `left`/`width` are numeric; no existing transition | **True** | `V/components/TimelineEditor/TrackListRenderer.tsx:285,292,296` |
| Zoom persists | **True, and homepage-only.** The key is `video-editor:preferences:astrid-light-study`, so restoring it matters for the next visit's hero, not for the app | `V/hooks/useEditorPreferences.ts:78-93`; `H/content/light-study-v1/logical-ids.ts:6` |
| Timeline cost of five more clips | **Low.** One `<img>` thumbnail per clip, no frame decoding. The preview skips source-track clips. **But** a video clip with `volume > 0` fetches and decodes its whole file for a waveform on the main thread | `V/components/TimelineEditor/TimelineEditorCore.tsx:193-206,491-497`; `V/hooks/useWaveformData.ts:38-44,54-104`; `V/components/PreviewPanel/RemotionPreview.tsx:205-207` |
| "The desktop/iPad/iPhone projects are Chromium" | **Wrong.** `devices['iPhone 13']` and `devices['iPad Mini']` default to WebKit, and no project sets `browserName`. CI installs Chromium only | `playwright.config.ts:172-182`; Playwright's `browserName` defaults to `defaultBrowserType`; `.github/workflows/slot-first-quality.yml:28` |
| Sky repaint cost | **New risk.** The canvas is 1 px per 6 CSS px with no DPR (about 11k cells per layer on a phone, about 39k on a desktop). Any change of hours invalidates the far, near and stars layers, and sun or moon movement invalidates sky. `rows` comes from `innerHeight`, and `resize` repaints with no debounce | `H/PublicAstridSky.tsx:106-107,148`; `H/publicAstridSkyRenderer.ts:9-15,41-64` |
| Phone hero | **Underrated.** On phones the hero is stacked: copy above, stage below at about 470–650 px (more than the planned 45svh). It is flat, with no perspective | `H/PublicAstridShell.css:1497-1695,1581-1584,1761,1890` |

**Rated too hard:** S3 (the zoom setter works and the retime arithmetic is already in §5), S5 (a lazy `import()` plus dispose is routine), T4, T9, T10 and T26. None of them needs Sol at xhigh.

**Rated too easy, or missing:**
- **The phone hero becoming the journey.** The stage has to shrink from about 600 px to about 45svh and pin while the stacked hero copy leaves. §3.6 gives this one line, and T15 (Sonnet) owns "flat phone layers". On phones §2 needs an orthographic stack (a per-surface `rotateX/rotateZ` in a flat parent), because the phone hero deliberately removes perspective.
- **The iOS sky.** Today the hero barely scrolls. Scrolling five viewports collapses the Safari toolbar, `innerHeight` changes `rows`, and the canvas reallocates and repaints every layer mid-scroll. Continuous hours repaint three or four layers per frame. Quantise the sky to steps and size it from a stable height.
- **Headers against the spine.** §3.1 keeps headers in flow and makes the chat surface a pinned spine below them. The next section's header then scrolls up through the pinned spine at every boundary.
- **Copy and timing.** Both sit in T1 (Luna). They are taste.
- **Branch drift.** Over 14 days there were 511 commits repo-wide, 52 in `src/pages/Home` and 243 in `V/`. The plan's foundation (`usePollSync` gates, Shell CSS) is exactly what moves.
- **Real Safari.** Playwright WebKit isn't iOS Safari, and an Artifact iframe doesn't reproduce the toolbar or `svh` behaviour (see §7).

## 2. Strategy and approach

- **Spikes first:** yes, but three, not five: S1 publisher, S2 stack pose, S4 sky. Fold S3 into T9 and T1's tests, and S5 into T13.
- **Assets early:** with placeholders, they stop being the long pole. Make them the cheapest plausible versions in phase 0, at the real dimensions and durations, so a later swap is data only.
- **Sections in page order:** keep it for §2 and §3. **Start §4's edit beats (T19, T20) right after the foundation, in parallel with §2.** §4 is the payoff and is independent of §2 and §3 visuals: its base is a snapshot. In page order it gets the least refinement time.
- **Reviews at the end:** yes. The owner's look at the preview throughout replaces any mid-plan gate.

**Transitions: one mechanism instead of three.** Treat every transition as an arrangement (`data-journey` pose) of the same live surfaces. The hero already does this with staggered 600–720 ms transitions (`H/PublicAstridShell.css:415-430`, `H/publicAstridMotion.ts:43`):
- **Hero → §2:** freeze the tilt, pause the preview, hide the callouts, fade the stage card. Then switch to the `extend` pose: the assembly rotates to about `rotateX(55deg) rotateZ(-30deg)`, each surface gets its own `translateZ` with the existing stagger, and the chat surface collapses to its composer bar (the "Agent" layer). A new Runtime layer and the labels fade in. Interrupting retargets for free, as App/Agent does today. The music clip lands live on the timeline layer.
- **§2 → §3:** a pose change to `generate`. Nothing to crossfade and nothing to remount.
- **§3 → §4:** a pose change to `edit`, as the plan says.
- **Rule for the moving poses:** move with `transform` and `opacity` only, keeping each surface's hero `width`/`height` and scaling it. The App/Agent switch animates `width`/`height`, which reflows the live editor every frame. Here that would double the cost during the pull-apart.
- **What remains hard:** WebKit rendering of a `preserve-3d` stack that contains a live video, and the phone version. That is what S2 proves.

## 3. Over-engineering

| Cut or simplify | Instead |
|---|---|
| Plates: A6, T7, corner matching, plate-to-live crossfade, light and dark captures | Re-pose the live surfaces (§2). Keep one still: the three.js fallback, taken by T13 |
| Visitor GPU detection (T16): WebGPU or WebGL probe, three-browser parser fixtures, fingerprinting rules | Cut. It risks being misread as "ran on your machine", and with placeholders there are no run facts to sit beside it. The readout title stays "Your machine" as a scenario label |
| Receipts: T1e, served-bytes hash test, "Recorded example" binding | Cut for v1 (placeholders). Keep the existing registry format (sha256 and duration pinned, `H/content/light-study-v1/media.ts:9`) so real assets swap in as data |
| T4: an IntersectionObserver plus reconciliation for jumps and load | One passive, rAF-coalesced scroll reader computes the active section (cached section tops, hysteresis) **and** sky progress. Deterministic on load, hash or a scrollbar jump. Merge into T3 |
| T10: an anchored-overlay scheduler extracted from Callouts, plus a 2 px tracking test | Compute positions: `x = laneOrigin + t × scaleWidth/5` (the renderer's own formula, `TrackListRenderer.tsx:285`), `y = trackIndex × 52` (`H/PublicAstridEditorParts.tsx:85`). Measure the lane origin once per fit. Cursor and mink transition on the same tokens as the clips, so they stay together |
| sr-only transcripts in each section | The per-section spine (§7) is real flow DOM, so it is the transcript |
| A "copy and numbers agree" test that parses copy | One constant feeds both the copy template and the snapshot |
| D/P/N/S/RM on every task | D and P on every visual task. N, S and RM only in T6, T8 and R2 |
| A7 horizon strip, "optional" | Out of v1. R2 decides if the finale needs it |
| A5 new mink strips before choreography | Placeholders reuse existing art: `astrid-mink-front/focus/tinkering.png`, the psychic strip, the juggler strip (`public/`). New strips come only after the craft pass approves cues |

## 4. Tiering and model balance

The plan has 15 XHARD tasks against 7 taste tasks, and the craft-critical work leaks to Luna and Sonnet.

| Task | Plan | Proposed | Why |
|---|---|---|---|
| S1 | XHARD | XHARD | Subtle adoption and draft-write races |
| S2 | XHARD | XHARD **paired with Opus** | Becomes "live stack pose, App and Agent, interrupted, WebKit, phone flat variant". Opus sets the target pose and timing in the same spike |
| S3 | XHARD | cut | Known: zoom works, and the arithmetic is in §5. The 320 px legibility check moves to T6 |
| S4 | XHARD | XHARD | Add raster ms per paint and iOS resize behaviour |
| S5 | XHARD | → T13 | Routine |
| T0 (new) | — | TASTE-HIGH | Opus sheet: all copy (§4's first request, replies, History lines, readout and install-log lines, Runtime labels), section beat timings, motion tokens. Phase 0, before engineering |
| T1 | NORMAL | NORMAL | Snapshots and registry only, built to T0's numbers |
| T1e | NORMAL | cut | Placeholders |
| P1 | NORMAL | NORMAL, phase 0 | Now the Artifact preview spike (§7) |
| H0 (new) | — | NORMAL | Capture harness (§5) |
| T2, T3 | XHARD | XHARD | T3 absorbs T4 |
| T5 | XHARD | XHARD | Gains the sticky per-section left column, the phone stage handoff, and freezing tilt and callouts (from T7) |
| T6 | TASTE-HIGH | TASTE-HIGH | Also owns the phone composition of every section |
| T7 | XHARD | cut | No plates |
| T8 | TASTE-HIGH | TASTE-HIGH | Starts in S2. Owns the stack at D **and** P (takes "flat phone layers" from T15) |
| T9 | XHARD | NORMAL | Formula, setter, clamp, restore |
| T10 | XHARD | cut, or a NORMAL overlay layer | Computed, not measured |
| T11 | NORMAL | NORMAL | Per-section flow spine |
| T12 | TASTE-LOW | TASTE-LOW | Component styling from clear frames |
| T13 | NORMAL | NORMAL | Plumbing only. **Its look goes to T15.** The module must stay short and readable, because the code panel shows it |
| T14 | NORMAL | NORMAL | |
| T15 | TASTE-LOW | TASTE-LOW | Example panels, **including the 3D view's look** (camera, framing, material, orbit speed), the beat-sync card and the install log |
| T16 | NORMAL | cut | See §3 |
| T17 | NORMAL | NORMAL | Mechanism. Motion values come from tokens |
| T18 | TASTE-HIGH | TASTE-HIGH | Scope: **all** §3 motion (pose, stills in, reframe, animate, landing) |
| T19 | NORMAL | NORMAL | Moved earlier (parallel with §2) |
| T20 | TASTE-HIGH | TASTE-HIGH | Moved earlier |
| T21 | XHARD | XHARD | Adds quantised steps and a stable canvas height |
| T22 | TASTE-LOW | **TASTE-HIGH** | The sky reaching its opposite peak is the page's ending. Hand the shared reveal-module extraction to NORMAL inside the same brief |
| T23 | XHARD | XHARD | |
| T24 | NORMAL | NORMAL | Smaller: the spine is real DOM |
| T26 | XHARD | NORMAL | One spec with `page.clock`. The iPhone project is already WebKit |
| A1 | ASSET | ASSET | Placeholder: a procedural loop at a fixed BPM, so the beat list exists by construction. Astrid chiptune or WebAudio offline render |
| A2–A4 | ASSET ×3 | ASSET ×1 | Placeholder: five stills by image generation, 9:16 crops, 5 s silent clips by an FFmpeg pan or zoom, posters and timeline thumbnails, encoded at display size |
| A5, A6, A7 | ASSET | reuse, cut, cut | See §3 |

Result: 8 XHARD, 11 NORMAL, 6 TASTE-HIGH, 2 TASTE-LOW, 2 ASSET, 29 in all. **Opus vs Sonnet** is sensible once the moments sit with Opus (pull-apart, §3 motion, edit beats, finale, layouts and phones, copy and timing) and components sit with Sonnet (device, example panels). Nothing in Opus's tasks is engineering that should move, except T22's shared-module extraction.

## 5. Does the plan deliver craft?

Not reliably. Taste first touches the build at T6 and T8, at the end of a serial chain (T1→T2→T3→T4→T5→T7). Each moment gets one session. Engineering picks easings and durations ad hoc in T14, T17 and T19. The done-when is a "named visual check" with no named way to watch motion. The **smallest change that makes craft reliable**:

1. **T0, the Opus sheet (phase 0):** words, beats and `J/journeyMotion.ts` tokens: three easings taken from the hero (`--astrid-surface-ease` `cubic-bezier(.5,0,.15,1)`, the assembly ease `(.22,.61,.36,1)`, the entrance ease `(.16,1,.3,1)`) and four durations. Every engineering task reads timings, poses and offsets from the tokens and CSS custom properties, and never hard-codes them. Taste then tunes numbers without touching Sol's mechanism. A needed mechanism change goes back as a note.
2. **H0, the capture harness (phase 0, NORMAL):** a Playwright script that drives the director with `page.clock` and writes, per transition and per section demo, a video at the real D and P viewports plus 2× DPR stills at named beats. It is the done-when medium for every TASTE task and for R2.
3. **Opus inside S2.** The first pull-apart is decided when the mechanism is chosen, not after it is built.
4. **Two passes per TASTE-HIGH task:** build, then refine after the owner has looked at the preview on a phone.
5. **One Opus lineage** across T8, T18, T20 and T22 (a shared notes file), so the three transitions and the ending share a voice.

## 6. Reviews

The R1–R4 shape is right and light. Changes:
- **R1 (Astra) per section, at D and P:** (a) dropped frames and p95 frame time while scrolling through it, at 1× and 4× CPU throttle; (b) the longest main-thread task during its demo (snapshot adoption commits, three.js init, tray video start, waveform decode); (c) sky raster ms per paint and paints per second while scrolling; (d) idle cost 3 s after the demo (rAF callbacks per second should be about 0, apart from the 450 ms desktop star tick); (e) bytes fetched entering it.
- **R1 page-level:** hero LCP, TBT and JS bytes before the hero is interactive, **compared with `main`**, so the journey must not slow the hero. Also peak memory and live video and WebGL counts on an iPhone.
- **R1 real-phone pass:** one iPhone pass through Safari Web Inspector over the LAN preview (§7). Neither the Artifact iframe nor Playwright WebKit measures real phone Safari.
- **R1 output:** numbers compared with `main` and named regressions, not hard thresholds.
- **R2:** it works from H0's recordings and 2× stills plus the live preview, both audiences and both palettes. Fine as written.
- **R4:** make "may placeholder media ship to production?" an explicit owner decision in R4's done-when.

## 7. Anything else

- **Spine and header layout.** Make each section's left column (header plus its own spine) `position: sticky` within its section. Headers and spines then scroll in and out together, and only the stage spans sections. The chat surface stays in the stage as §2's Agent layer and is hidden after it. On phones this column simply sits below the 45svh stage. Reserve the spine's final height so arriving turns don't shift layout.
- **Mounting.** Before moving `.astrid-showcase` out of `.astrid-landing-grid` (§3.1), try making the existing showcase the sticky element in a taller grid. That keeps the editor's mount and the hero layout untouched, and moving it would be a large edit to a fast-changing 900-line Shell.
- **Lake placeholders:** set `volume: 0` and silent files, and give each a `thumbnailUrl`. Otherwise five full MP4 fetches and decodes feed waveforms.
- **Drift.** Merge `main` into `feat/home-journey` daily and re-run S1's adoption test after each merge.
- **Throughput.** Codex can't bind ports, so every Playwright run goes through the coordinator, one heavy job at a time. Give Codex tasks unit-test done-whens and batch E2E. Claude taste agents run their own dev server.
- **CI:** add `npx playwright install webkit` (or pin the journey spec to the projects CI can launch). Otherwise the iPhone and iPad projects can't run there.
- **Placeholder honesty.** Use no measured facts (no "RTX 4090 · 24 GB", timings or VRAM). Change the label to "Example". Mark the install log as illustrative. Keep the chat copy, which is a scenario.

### The Artifact preview (new decision)

**It is feasible. Make it P1, a day-one spike, built from today's `main` hero before any journey code exists.**

What the static build needs. All of it lives in a preview-only build config, apart from two small cleanups:
1. **Entry.** The app routes by pathname. Only `/`, `/home` and `/vision` mount the public site. Any other path, which is what an Artifact serves, boots the full app (`src/app/entryClassification.ts:9-11,29-36`; `src/app/main.tsx:51-59`). Add a preview HTML entry that calls `renderPublicEntry()` directly (`src/app/publicBootstrap.tsx:6-9`), plus a preview Vite config with `base: './'` and that HTML as `rollupOptions.input`. This is a build artefact, not a runtime flag.
2. **Root-absolute URLs.** Light-study media already use `BASE_URL` (`H/content/light-study-v1/media.ts:9`). These do not:
   - the mink poses (`H/PublicAstridShell.tsx:260`)
   - the psychic strip and Departure Mono (`H/PublicAstridSky.css:113,127`)
   - TT Gertika (`src/index.css:8-10`)
   - the Vision art (`H/PublicAstridVision.tsx:162`; `H/PublicAstridNorthStarArt.tsx:26`)

   They 404 unless the Artifact happens to be served at its origin root. Move them to `BASE_URL` or imports on the branch, which is harmless. Journey code uses `BASE_URL` from the start.
3. **Service worker.** Leave out the service worker registration (`index.html:226`) and the manifest.
4. **Publish only what the preview build emits plus the media it references.** Not `public/`: it is 215 MB, and its four files over 16 MB are legacy and unused by this page. The page's static import closure is about 1,180 source files. Built chunks plus the globbed fonts (`V/compositions/LocalFontFaces.tsx:12`) should sit well under 511 files and 256 MB; the spike records the real numbers. Over 255 files means two publishes per version.
5. **No backend.** The public page calls no API. Location comes from the `Intl` time zone plus a city table (`H/publicAstridLocation.ts:3-4,85`). Unconfirmed: whether anything under the editor reaches the auth health probe (`src/shared/auth/bridgeSession.ts:40`). The spike's network log answers it.

Known limits inside the Artifact (accept them and test these behaviours elsewhere):
- Home ↔ Vision does an unguarded `pushState('/vision')` (`H/PublicAstridSite.tsx:78-83`). In a sandboxed iframe it may throw, and a reload lands on a 404. Check T23's Vision round trip and hash restore on the LAN preview.
- `V/settings/useEditorSettings.ts:18-20` writes storage with no try/catch. If the iframe blocks storage, it throws after every zoom change. Wrap it (one line).
- An iframe in the claude.ai viewer never collapses Safari's toolbar or changes `svh`. So it can't show the sticky stage or the sky resize on an iPhone. It previews look and feel; it doesn't test phone Safari.
- The host's CSP for `blob:` workers or media and for module chunks is unknown. The spike finds out.

**Spike done when:**
- today's hero renders from the Artifact on desktop and on the owner's phone: both audiences, both palettes, the editor, mink, fonts and sky;
- the network log shows zero failed requests;
- the file count and bytes are recorded;
- one script rebuilds and republishes to the same URL.

A Claude agent runs it, because the Artifact tool is Claude-side and Codex can't publish.

**Fallback, which is also the real-Safari path:** `vite preview --host` on the coordinator's Mac, opened from the owner's iPhone on the same Wi-Fi at `/home` (or through a quick tunnel when off the LAN). It has real paths, the real toolbar, and Safari Web Inspector for R1. If the Artifact fails on entry or CSP, this becomes the preview. A second Railway service stays the last resort.

## Changes to the plan, most important first

1. **Build the exploded stack as a third arrangement of the live surfaces, and delete the plate pipeline.** Use a new `extend` pose on `.astrid-editor-surfaces` with per-surface `translateZ`, the chat surface collapsed to the Agent bar, and a fifth Runtime child in the same `preserve-3d` parent. Moving poses use `transform` and `opacity` only. §2→§3 and §3→§4 become pose changes. Rewrite W7, §3.6 and the §2 facts row. *S2 (re-scoped), A6 and T7 cut; T8 and T18.*
2. **Add T0, an Opus sheet in phase 0:** every line of copy, each section's beats and timings, and `J/journeyMotion.ts` tokens taken from the hero's easings. All engineering reads tokens and never hard-codes timing. T1 builds data to T0's numbers. *T0 (new); T1, T14, T17, T19, T8, T18, T20.*
3. **Add H0, a capture harness in phase 0:** Playwright plus `page.clock` records each transition and section demo as video at real D and P viewports, plus 2× stills at named beats. It is the done-when medium for every TASTE task and for R2. *H0 (new); T6, T8, T12, T15, T18, T20, T22, R2.*
4. **Make P1 the Artifact preview spike on day one.** It needs a preview-only entry calling `renderPublicEntry()`, `base: './'`, no service worker, only the emitted files published, and `BASE_URL` for the root-absolute assets. A Claude agent runs it. The fallback is a LAN or tunnel `vite preview`, which also serves R1's iPhone pass and T23's Vision checks. *P1, T23, R1.*
5. **Design phones explicitly:**
   - the stacked hero hands off to a sticky stage of about 45svh (T5 mechanism, T6 composition);
   - on phones §2 is an orthographic stack in a flat parent, owned by T8 at D and P;
   - remove "flat phone layers" from T15;
   - S2 proves the phone pose too.

   *S2, T5, T6, T8, T15.*
6. **Fix the layout model.** Each section gets a sticky left column (header plus its own flow spine), and only the stage spans sections. The spine is the transcript, so drop the sr-only copies. First try making the existing showcase sticky in a taller grid rather than moving it out of `.astrid-landing-grid`. *§3.1, T5, T6, T11, T24.*
7. **Make the sky cheap on scroll.** Quantise progress to visible steps rather than about one sky-minute, and size the canvas from a stable height, not a per-resize `innerHeight`. S4 reports raster ms per paint at D with 4× throttle and on an iPhone. *S4, T21, R1.*
8. **Rewrite for placeholders:**
   - procedural music with a beat list by construction, which removes T1's wait on the music pick (A1);
   - one lake-media task: stills, 9:16 crops, silent 5 s pan clips, posters and thumbnails, `volume: 0` (A2–A4 merged);
   - the existing mink art reused (A5);
   - A6, A7, T1e and T16 cut, and the served-bytes test cut;
   - readouts labelled "Example" with no measured facts, and the install log marked illustrative;
   - R4 asks whether placeholder media may ship.

   *A1–A7, T1, T1e, T16, T17, R4.*
9. **Cut or merge the over-tiered work:**
   - S3 goes into T9, T1's tests and T6;
   - S5 goes into T13;
   - T4 goes into T3 (one rAF scroll reader for section and sky progress);
   - T10 becomes computed overlay positions;
   - T9 and T26 drop to NORMAL.

   That gives 8 XHARD tasks out of about 29. *S3, S5, T3, T4, T9, T10, T13, T26.*
10. **Put taste where the feel is made:**
    - T22 becomes TASTE-HIGH;
    - T15 owns the 3D view's look;
    - T18 owns all §3 motion;
    - Opus pairs in S2;
    - each TASTE-HIGH task gets two passes, the second after the owner's phone look;
    - T8, T18, T20 and T22 share one Opus notes file.

    *S2, T8, T13, T15, T18, T20, T22.*
11. **Start §4's edit beats right after the foundation, in parallel with §2**, so the payoff gets the most refinement time. *Phase order; T19, T20.*
12. **Re-scope R1:**
    - per section: scroll frames at 1× and 4×, the longest task during the demo, sky ms per paint, idle callbacks, bytes;
    - page-level: hero LCP, TBT and initial JS compared with `main`;
    - one real-iPhone pass.

    Report numbers against `main`, not hard thresholds. *R1.*
13. **Keep the branch alive:**
    - merge `main` daily and re-run S1's adoption test after each merge;
    - CI installs WebKit, or the journey spec pins to what CI can launch;
    - Codex tasks get unit-level done-whens, and the coordinator batches E2E.

    *T2, T26, §9.*
14. **Correct the guide's stale facts:**
    - the plate rationale (W7, §2);
    - "iPhone and iPad projects are Chromium": they are WebKit (`playwright.config.ts:172-182`);
    - the sky cost and iOS resize row;
    - trim the visual-check matrix to D and P per task, with N, S and RM only in T6, T8 and R2.

    *§2, §7 header.*
