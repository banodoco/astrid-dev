# Astrid Homepage Journey — Inputs

## Starting point and authority

This is a planning handoff for the Astrid homepage journey. It does not authorize product work. The accepted plan says work starts only after Hannah says go; Step 0 then confirms the live source and pointers.

- Product source: `banodoco/astrid-app`, route `/home` (`src/pages/Home/`).
- Baseline recorded by the accepted plan: `main` at `17e46de99` (20 Oct 2026). The start-here handoff records that `main` had moved to `bebadd0e1` when its zip was made; re-check every pointer at Step 0.
- Target working branch, if authorized: `feat/home-journey`, from `origin/main`; destination `main` only after R4 and the owner's go.
- Existing work recorded to preserve: none; hero remains as-is. Predecessor output: none.
- Existing assets: composition mockups in `mockups/`; the accepted requirements are in [design.md](design.md).
- At Step 0, copy this folder into `docs/strategy/projects/home-journey/` in astrid-app.

## Starting code facts

## 2. Code facts that shape the design (verified on `17e46de99`)

| Fact | Where | Consequence |
|---|---|---|
| The hero editor is the real editor: `EditorRuntimeProvider`, `RemotionPreview`, `TimelineEditorCoreBody` | `H/PublicAstridEditorProvider.tsx:39`; `H/PublicAstridEditorParts.tsx:61,80` | Drive the real editor, never a second one |
| **The hero is already a live 3D stack.** The stage has `perspective` (`H/PublicAstridShell.css:300`); `.astrid-editor-tilt` and `.astrid-editor-surfaces` are `preserve-3d` (`:394,403`); each surface has its own `translate3d(…, -175px…160px) rotateY()` per audience (`:870-953`); the assembly is `rotateX(5deg) rotateY(-8deg) scale(.9)` (`:891`). DOM: `H/PublicAstridMountedEditor.tsx:118-146` | as listed | The §2 stack is a third arrangement of the live surfaces. `overflow:hidden` on a surface only flattens that surface's own contents |
| The App/Agent switch animates `left/top/width/height` (reflowing the live editor every frame) with a 720 ms move | `H/PublicAstridShell.css:415-440`; `H/publicAstridMotion.ts:43` | Journey poses move with `transform` and `opacity` only, keeping each surface's hero box |
| Motion timing compares audience only (`sameExperience`, `routeMotionTiming`) | `H/PublicAstridShell.tsx:154`; `H/publicAstridMotion.ts:5,35` | Add the journey pose to the motion contract, or give the journey its own controller (T5 decides) |
| **Phones flatten the 3D**, and the phone hero is stacked (copy above, stage about 470–650 px tall below) | `H/PublicAstridShell.css:1497-1695,1581-1584` | Phones need a pin-and-scale handoff to a ~45svh sticky stage and an orthographic §2 stack [design.md](design.md#36-the-transitions-are-poses-of-the-live-panels) |
| The read-only guard and browse-only mode are on main (editability, element host, `enableMutationServices/LiveServices/RenderExport={false}`, `timelineOverlaysEnabled={false}`) | `H/PublicAstridEditorProvider.tsx:39-58`; `V/contexts/EditorRuntimeProvider.tsx:230,260,448` | No guard work. Keep the regression tests (`V/contexts/EditorRuntimeProvider.test.tsx:2661,2763`). Never enable services to show §2's examples |
| The page is hero-only: `.astrid-public-site` has `min-height: 100vh`, `overflow: clip` | `H/PublicAstridShell.css:28-33`; `H/PublicAstridShell.tsx:721` | Add real section height; clip deliberately (`overflow-x`) |
| Sticky is unverified for the new structure | `src/index.css:345,350`; `H/PublicAstridSite.css:14` | T5 audits body overflow and the retained-page wrapper |
| The showcase row is `clamp(520px, calc(100svh - 40px), 680px)` | `H/PublicAstridShell.css:295` | Override the 520 px minimum for short viewports and phones |
| The View Transition name sits on `.astrid-landing-grid` | `H/PublicAstridSite.css:42` | Move it to a hero-only wrapper so Vision doesn't snapshot the tall page |
| The public provider returns cloned fixed data and hard-codes `configVersion: 1`. Poll sync adopts with `save:false, skipHistory:true`; invalidation refetches at once; commit is a 0 ms `setTimeout`; a newer snapshot cancels a pending one; only drag or resize defers it | `H/publicAstridExample.tsx:127,142-160`; `V/hooks/useTimelineQueries.ts:8,42`; `V/hooks/usePollSync.ts:66-74,97-114,336-375` | A journey provider can feed scripted snapshots (S1, T2) |
| Adoption is blocked by stale versions, active interactions, unsaved work and canonical drafts. The public asset allowlist is captured at construction | `V/hooks/usePollSync.ts:66,112,299`; `H/publicAstridExample.tsx:133,153` | Strictly increasing versions; one **fixed registry** holding every journey asset from the start |
| `persistenceEnabled:false` does **not** stop draft writes on normal saved mutations; only poll adoption skips `scheduleSave` | `V/hooks/useTimelinePersistence.ts:973,1028,1040`; `V/hooks/useTimelineCommit.ts:337,398`; DB `astrid.timeline-drafts` (`V/data/timelineDraftIndexedDb.ts:13`) | S1 asserts zero `saveTimeline` calls and zero writes to `astrid.timeline-drafts` |
| The pure patch compiler supports `clip.move`, `clip.update`, `track.add`; split/slice are reserved no-ops | `V/lib/timeline-patch.ts:1012,1208,1309,1432`; `V/commands/media.ts:737` | Author endpoint snapshots as data with these ops; never rely on split |
| `clip.speed` and `clip.transition` render; a crossfade is an opacity ramp on the incoming clip, which already gets pre-roll | `V/compositions/VisualClip.tsx:307,557,640`; `V/effects/transitions.ts:6`; `V/transitions/catalog.ts:183` | 0.6× and the crossfade work as is. Don't subtract the transition from `at` |
| The video key includes playback rate | `V/compositions/ReadinessVideo.tsx:15`; `H/PublicAstridEditorParts.tsx:102` | A speed change remounts the preview video: the preview is paused from §2 on |
| Clip wrappers have stable ids and numeric `left`/`width`; no transition exists | `V/components/TimelineEditor/TrackListRenderer.tsx:285,292,296`; `ClipAction.tsx:555`; `V/lib/timeline-dom.ts:17,140` | A journey-scoped CSS transition animates moves (no FLIP) |
| Overlay positions are computable: `x = laneOrigin + t × scaleWidth/5`, `y = trackIndex × 52` | `V/components/TimelineEditor/TrackListRenderer.tsx:285`; `H/PublicAstridEditorParts.tsx:85` | No measuring loop. Measure the lane origin once per fit |
| **Zoom works** in the mounted editor (the no-op is only the initial fallback). px/s = `scaleWidth / 5` (default 160 → 32 px/s). Gutter 144 px desktop, 56 px touch. Prefs persist (debounced) under `video-editor:preferences:astrid-light-study`; the direct setter isn't clamped | `V/hooks/timelineStore.ts:404`; `V/hooks/useTimelineState.ts:575,583`; `V/hooks/useEditorPreferences.ts:30,78-93`; `V/lib/coordinate-utils.ts:6-16`; `V/settings/useEditorSettings.ts:17` | Fit-to-width with the real setter and gutter; clamp 40–1000; save and restore the hero zoom |
| A video clip with `volume > 0` fetches and decodes its whole file on the main thread to draw a waveform; the preview skips source-track clips | `V/hooks/useWaveformData.ts:38-44,54-104`; `V/components/PreviewPanel/RemotionPreview.tsx:205-207` | Lake clips: silent files, `volume: 0`, a `thumbnailUrl` each |
| Audio tracks exist; waveforms decode in the browser | `V/types/index.ts:57`; `V/hooks/useWaveformData.ts:29,106` | Music is a registry entry, an `A1` track and a clip |
| Source tracks (`role: 'source'`) stay authored and visible, excluded from output | `V/types/index.ts:82`; `V/data/timelineOutputProjection.ts:115`; `V/compositions/TimelineRenderer.tsx:1580` | The lake track is a labelled source track |
| The hero fixture forbids claiming live generation, named integrations or tool invocations | `H/content/light-study-v1/authored-script.ts:7-15`; `provenance.ts:28`; `provider-binding.ts:5`; `verified-result.ts:5` | Journey content is a **separate bundle** (`L/`). The hero fixture is untouched |
| `scriptedReplayReducer` is fixture-specific | `H/replay/scriptedReplay.ts:17,47,83,106,124` | A small journey reducer on the same pattern |
| `ConversationPresentation` takes items, pending state and scroll refs; `tool_group` exists; duplicate consecutive assistant messages are dropped; the hero's `column-reverse` is host CSS | `C/ConversationPresentation.tsx:14,86,103`; `C/contracts.ts:31,58,68`; `H/PublicAstridShell.css:732` | Chronological spine with a compact chip slot; don't loosen global dedupe |
| The mink: static poses on Home, a sprite overlay, the Vision juggler strip with `step-end`, and the `MinkRunner` run strip (81×44, 11 frames, 70 ms); reduced motion hides the overlay | `H/PublicAstridShell.tsx:223,260`; `H/PublicAstridSky.css:97,111,117`; `H/PublicAstridVision.css:73`; `src/shared/components/MinkRunner/astrid-mink-run.png` | New sprites follow the strip pattern; reduced motion shows chosen static frames |
| `three`, `@react-three/fiber`, `@remotion/three` are dependencies | `package.json:162-164` | Lazy `import()`; a vendor chunk only if a measured build says so (`config/vite/policy.ts:19`) |
| The sky is `position: fixed`; `setManualHours` notifies the controls listeners (a shell render). Raster, parallax and controls are separate channels; no journey claim/progress API | `H/PublicAstridSky.css:1`; `H/publicAstridSkySession.ts:192,324,340,511,576,580` | A scroll fast path (W10); never call `setManualHours` per frame |
| **Sky repaint cost.** The canvas is 1 px per 6 CSS px with no DPR; any change of hours invalidates the far, near and stars layers; `rows` comes from `innerHeight` and `resize` repaints with no debounce. iOS Safari's toolbar collapsing mid-scroll changes `innerHeight` | `H/PublicAstridSky.tsx:106-107,148`; `H/publicAstridSkyRenderer.ts:9-15,41-64` | Quantise progress to steps; size the canvas from a stable height |
| Drift saturates at 1400 px; the quiet field observes scroll | `H/publicAstridSkySession.ts:35,168`; `H/publicAstridSkyGeometry.ts:166` | Keep drift separate from time-of-day; gate the quiet field to the hero |
| `/art` is behind app routing | `src/app/routes.tsx:174` | No art link |
| Dynamic imports are excluded from the bundle budget | `config/vite/bundleBudget.ts:30-39,62` | Section code is dynamic imports; not a licence for unlimited deferred bytes |
| The build needs a selected or bundled Astrid source and a valid tool catalog | `config/vite/vite.config.ts:62`; `config/vite/astridSource.ts:67,132` | P1 proves a fresh-checkout build |
| **The app routes by pathname**: only `/`, `/home` and `/vision` mount the public site; any other path boots the full app. `renderPublicEntry()` mounts the public site directly | `src/app/entryClassification.ts:9-11,29-36`; `src/app/main.tsx:51-59`; `src/app/publicBootstrap.tsx:6-9` | The Artifact preview needs its own HTML entry calling `renderPublicEntry()` (a build artefact, not a runtime flag) |
| Root-absolute asset URLs (not `BASE_URL`): mink poses, psychic strip, Departure Mono, TT Gertika, Vision art. A service worker registers in `index.html`. `public/` is 215 MB | `H/PublicAstridShell.tsx:260`; `H/PublicAstridSky.css:113,127`; `src/index.css:8-10`; `H/PublicAstridVision.tsx:162`; `H/PublicAstridNorthStarArt.tsx:26`; `index.html:226` | P1 moves them to `BASE_URL`/imports and leaves the service worker out of the preview entry. Publish only emitted files |
| Editor settings write storage with no try/catch; Home ↔ Vision does an unguarded `pushState('/vision')` | `V/settings/useEditorSettings.ts:18-20`; `H/PublicAstridSite.tsx:78-83` | Wrap the storage write (one line). Test Vision round trips on the LAN preview, not the Artifact |
| Playwright boots its own Vite and a fake Runtime. The `chromium-condensed` and `chromium-mobile` projects use `devices['iPad Mini']`/`['iPhone 13']`, which default to **WebKit**; CI installs Chromium only | `playwright.config.ts:114,147,159-182`; `.github/workflows/slot-first-quality.yml:28` | CI must `npx playwright install webkit`, or the journey spec pins to what CI can launch (T26) |
| Phone breakpoint is 640 px | `H/publicAstridLifecycle.ts:12`; `H/publicAstridNavigation.ts:63` | Phone layouts key off it |


## Asset scope and provenance

## 6. Assets

### 6.1 Placeholders (in scope)

| ID | What | Route | Spec |
|---|---|---|---|
| A1 | Music, 28 s | Procedural loop at a fixed BPM (Astrid chiptune pack or a WebAudio offline render), quiet, so the beat list exists by construction | MP3 128 kbps + `L/journey-audio.json` (beats, downbeats); sha256 and duration pinned |
| A2 | Lake media | Five 16:9 stills by Codex image generation (`codex exec --enable image_generation`, 1280×720); 9:16 **crops** (720×1280); five 5 s **silent** clips by an FFmpeg slow pan/zoom over each still (720p, H.264, muted); posters and timeline thumbnails | Encoded at display size; `volume: 0` in the snapshots; sha256 and duration pinned |
| A5a | Mink placeholder kit | Existing art, no resampling except the exact ÷4 nearest-neighbour of `astrid-mink-front.png`: front, juggler crops, the run strip, spark and thought glyphs ([design.md](design.md#106-the-mink)) | One JSON per strip (frame size, count, feet anchor, ms) |
| A9 | Pixel icons | 16×16 grids in `H/PublicAstridPixelIcons.tsx` format: monitor (Local), cloud, wrench (chip) | Crisp at D and P, both palettes |

### 6.2 Deferred real assets (only on the user's word)

- **Real music** (original or licensed), with its beat list.
- **A real generation run** (Flux via ComfyUI, Wan 2.2 via Wan2GP, an LTX install) on rented GPUs, roughly $10–30, with receipts; then the readouts may print measured facts and drop "Example".
- **Final mink strips** A5b–A5h (7 strips, 27 frames: `sit`, `carry`, `push`, `snip`, `plug`, `lookup`, "!"), checked with Astrid's `pixel.strip`/`pixel.sprites`, then M1's second pass on them.

Because placeholders use the real registry format and dimensions, each swap is data only.


## Review boundary

[design.md](design.md) is the accepted design brief; [tasks.md](tasks.md) owns implementation proof and the PR will link actual checks. Mockups are visual guides, not pixel-by-pixel specifications. Historical planner transcripts are not a separate source of authority.
