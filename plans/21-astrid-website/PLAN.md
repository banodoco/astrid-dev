# Astrid homepage journey: build plan (v3, round 4)

## Executor brief (read this first)

**Goal.** Build the scroll journey below the hero of the Astrid homepage (`banodoco/astrid-app`, route `/home`), as specified in this plan, on the existing code. Hero → §2 "A creative suite your agent can extend" → §3 "Open models, without the setup pain" → §4 "A creative partner with deep tools" → §5 finale. The approved look is in `mockups/` (composition guides, not specs; where they disagree with this plan, follow the plan).

**What matters most.** The mockups are only a guide to composition and tone; don't chase them pixel for pixel. Two things decide whether this succeeds, and every other choice serves them:
1. **Each section feels alive while you rest on it.** Stop scrolling anywhere and things keep happening: messages come through, the agent works, the timeline changes, clips play, the mink gets on with a job. A section is never a dead screenshot (part 10.1, principle 8).
2. **The transitions between sections are really nice.** Each one is the same live objects moving into a new arrangement, continuous and unhurried, never a cut or a fade to a new scene (part 3.6, part 10.3).

When time is short, spend it on these two. R2 judges them first.

**Bound by the experience, free in the implementation.**
- **Binding (what the visitor gets):**
  - the two priorities above;
  - part 1 (what we're building and the ground rules);
  - part 5 (the copy);
  - part 10 (the craft direction: beats, motion vocabulary, the mink, phones and reduced motion), with numbers tunable by ±20% in T0;
  - the mockups, as composition and tone;
  - every done-when phrased as what a visitor sees at desktop or phone size;
  - R1's performance bar.
- **Also binding (they protect the live site and editor):**
  - scripted publishes never save, write drafts or add history;
  - one editor instance;
  - no per-frame React work;
  - no flags;
  - placeholders claim nothing real.
- **Flexible (the recommended route, not a contract):**
  - parts 3 and 4 (architecture and workstreams);
  - file and module names;
  - the suggested mechanisms;
  - how tasks are split.

  Any agent may take a different mechanism, layout or split when it delivers the same experience more simply or more robustly; it records the deviation and why in its report. Done-whens that name files or greps are guardrails; the visible result is what's binding.

**Definition of done.** Every task in part 7 is merged into `feat/home-journey`; the journey E2E spec is green; the bundle budget is green; R1 (performance) and R2 (taste) have run and R3 has fixed or explicitly dropped their findings; the user has seen the preview on desktop and phone. Then **stop and ask the user** two things: may the placeholder media ship, or should real assets be made first; and may `feat/home-journey` merge to `main` (which deploys production). Nothing reaches `main` before that.

**Who coordinates.** Prefer a **Claude Code session** as coordinator. Only Claude can publish the preview Artifact, and Codex workers can't bind ports (no dev server, no Playwright), send signals or nest sandboxes. If a Codex session coordinates, one Claude Sonnet agent owns P1 and every preview republish, and a Claude session runs Playwright and H0.

**Phase order** (detail in part 8): Step 0 → phase 0 (T0 motion sheet, P1 preview, H0 capture harness, spikes S1/S2/S4, placeholder assets, all in parallel) → phase 1 foundation (T1 → T2 → T3 → T5; then T9, T10, T28) → phase 2 (§2 and §4 in parallel, the sky, the mink) → phase 3 (§3) → phase 4 (finale, navigation, accessibility, E2E) → review (R1 Astra performance ∥ R2-D desktop and R2-P phone iteration passes → R3) → ask the user → R4 merge.

**Briefing.** Use the templates in part 9.6. Every brief names the task id, its row from part 7, the plan parts to read, the worktree and branch, the files it may touch, the done-when, and the fan-out rule.

**The fan-out rule.** This applies to every senior agent, whether it's building, fixing or reviewing.
- Opus, Sonnet, Sol and Astra direct and judge. They hand the hands-on work to parallel subagents from their own family: reading, searching, captures, running tests, and the edits themselves.
- **Claude agents (Opus, Sonnet) deploy Haiku subagents** (Agent tool, `model: "haiku"`).
- **Codex agents (Sol, Astra) deploy Luna subagents** (`spawn_agent` with `model: "gpt-6-luna"`).
- The senior agent checks each subagent's result before accepting it, and keeps the decisions: taste with Opus or Sonnet, mechanism with Sol.
- Plumbing that's bigger than a fix stays in its own NORMAL or XHARD task. Engineering never writes a millisecond or an easing curve: they come from `J/journeyMotion.ts` (T0).

**Practical limits.**
- App unit tests run on **Node 20.19.4**: `export PATH=<path to Node 20.19.4>/bin:$PATH` (Node 26 fakes hundreds of localStorage failures). vitest with `--maxWorkers=2..4`.
- **One heavy Codex job at a time** on this Mac (parallel Codex test runs have exhausted memory before). Light Codex work (writing code, no test suites) can overlap. Let GitHub CI run big suites.
- Codex workers commit in their own worktree with `--add-dir <repo>/.git`; they can't run Playwright or a dev server, so their done-whens are unit-level plus a list of visual/E2E checks for the coordinator.
- Claude taste agents run their own dev server on their own port (2223+), never the coordinator's.
- **Test and capture agents never write to anything the user views.** Only the coordinator republishes the preview Artifact.
- Merge `main` into `feat/home-journey` daily and re-run S1's adoption test after each merge (the editor's poll-sync code moves fast).

**Where results go.** Each task: branch `hj/<id>` in worktree `../hj-<id>`, merged by the coordinator into `feat/home-journey`; a short report at `docs/plans/home-journey/reports/<id>.md` (what changed, tests run, open notes). Captures (H0): `h0/` at the repo root, git-ignored. The Opus craft notes lineage: `docs/plans/home-journey/notes/opus-craft.md`, appended by T0, T8, T18, T20, T22 and M1.

**When to ask the user.** Only for: shipping placeholder media, and merging to `main`. Everything else: decide, record the decision in the task report, carry on. The user may look at the preview and send notes at any time; fold them into the next pass, but never wait for them.

> **34 tasks:** 8 XHARD (Sol) · 13 NORMAL (Luna) · 7 TASTE-HIGH (Opus) · 2 TASTE-LOW (Sonnet) · 4 ASSET (placeholders), then R1–R4. Real assets are deferred (part 6.2).
> **Day one:** P1 Artifact preview · S1 snapshot publishing without writes · S2 the live stack pose (App, Agent, interrupted, WebKit, phone) · S4 the scroll-driven sky.

## Step 0, on "go"

1. `git fetch origin && git switch -c feat/home-journey origin/main`.
2. **Pointer re-check (Luna, read-only, ~1 session).** This plan is pinned to `main` at `17e46de99` (20 Oct 2026). Re-check every `path:line` in it against the new branch point; update moved pointers in `PLAN.md`; list any fact in part 2 that is no longer true. The coordinator decides what a changed fact means before phase 0 starts.
3. Commit this folder (`PLAN.md`, `mockups/`, `evidence/`) to `docs/plans/home-journey/` on `feat/home-journey`. Create `reports/` and `notes/opus-craft.md` (seeded with part 10).
4. Add `h0/` to `.gitignore`.

---

**Status (20 Oct 2026):** plan only; nothing is built until the user says go. Supersedes v1 (12 Oct, round 3 order) and v2 (20 Oct). Code facts come from an Astra deep pass and an Opus review against `main` at `17e46de99`; the evidence is in `evidence/` (`DEEP-PASS-RESULT.md`, `OPUS-REVIEW-RESULT.md`, `OPUS-CRAFT-RESULT.md`). Where evidence and this plan differ, this plan wins.

Paths are relative to the app repo. Prefixes: `H/` = `src/pages/Home/`, `V/` = `src/tools/video-editor/`, `C/` = `src/shared/components/conversation/`, `J/` = `src/pages/Home/journey/` (new), `L/` = `src/pages/Home/content/journey-v1/` (new), `P/` = `public/astrid/journey/` (new). Line numbers drift; treat them as pointers. Guide parts are written "part 3.4"; page sections are §2–§5.

## 0. Decisions

| Question | Decision |
|---|---|
| Page order | Hero → §2 extend → §3 generate → §4 edit → §5 finale |
| The exploded stack | **The live editor panels in a third pose**, not still plates. The hero is already a live 3D stack (part 2). §2→§3 and §3→§4 are pose changes of the same live panels |
| §4 edit scope | The three light studies and the music only. The five lake clips from §3 sit on a labelled source track (`role: 'source'`), unchanged and silent |
| Flags | **None.** No `?journey=1`, no hidden modes. One branch, `feat/home-journey`, merged to `main` only at R4 with the user's go |
| Preview | **A Claude Artifact** of the branch's public entry (P1), republished by the coordinator. Fallback and real-Safari path: `vite preview --host` on the coordinator's Mac, opened from the user's iPhone on the same Wi-Fi (or a quick tunnel) |
| Assets | **Placeholders for everything** (music, lake stills and clips, mink strips). Registered in the real registry format (sha256, duration) so real assets swap in as data later (part 6.2) |
| Readout honesty | Placeholders claim nothing real: readouts carry an **"Example"** label, no GPU specs, VRAM, timings or usage counts; the install log is marked illustrative; no visitor GPU detection |
| Reviews | At the back end and light: R1 Astra performance pass, R2 two or three Opus taste checks, R3 one fix round. Mid-plan TASTE tasks judge their own result from H0 captures; no mid-plan gates |
| Craft ownership | T0 (Opus) fixes copy, beats and motion tokens before engineering. TASTE-HIGH tasks get two passes. One Opus notes lineage across the moments |
| Sky window | The visitor's real time to the opposite peak (night → solar noon, day → solar midnight); polar day/night runs +12 h |
| Moon | Real phase, no visibility floor |
| Art link | Left out; the finale has one link, to Vision |
| §2 3D view | Live three.js, lazy-loaded (`three` is already a dependency) |
| Phones | In v1, designed explicitly (part 3.6, part 10.5) |
| Clip labels | Real names: "First light", "Passing shapes", "A quiet finish" (not the mockups' "final-frame") |

## 1. What we're building

The hero stays as it is. Below it, three sections and a finale re-say the hero's six notes in new ways, using the objects the hero already shows (the four editor panels, the conversation, the mink). One repeated device shows **what your agent did**.

| § | Eyebrow · headline · sub | Hero notes | On screen | Agent-action device |
|---|---|---|---|---|
| §2 | `02 / MAKE IT YOURS` · **A creative suite your agent can extend.** · Any view, tool or model, from the canvas down to the runtime. | 4, 5 | The live panels tip back and fan out into an exploded stack over a new Runtime layer. Three examples: a 3D view (Panels), a beat-sync tool (Agent), a new model (Runtime). After the first cycle they keep cycling with live activity (the ambient cycle) | `built by your agent` stamps (`installed by your agent` for the model); the layer each example extends lights up (text plus dot) |
| §3 | `03 / GENERATE ANYWHERE` · **Open models, without the setup pain.** · Your agent installs and runs them, on your machine or in the cloud. | 2, 3 | The stack folds back into the live timeline (bottom strip). Five stills develop, reframe to 9:16, play once and drop onto a new "Lake at dawn" source track | `set up by your agent` under each readout title |
| §4 | `04 / CREATE TOGETHER` · **A creative partner with deep tools.** · It edits beside you, with tools you build and workflows the community shares. | 1, 5 | The timeline grows to fill the stage. You (a cursor) and Astrid (the mink) both edit the three light studies; a History panel interleaves the edits | Tool-call chips under Astrid's replies: `arrange · 3 clips`, `beat-sync · 3 downbeats` (stronger fill: the tool built in §2), `retime · crossfade` |
| §5 | `THE VISION` · Unlocking the creative potential of the open-source ecosystem. | 6 | The stage scrolls away; the sky, turning since §2, reaches the opposite peak; the mink looks up. One link to Vision | — |

**Ground rules**
1. Scroll is never blocked or hijacked. Scroll decides *where* the visitor is; *time* plays each moment. Only the sky follows the scroll.
2. Arriving in a section plays its demo once, then its ambient cycle keeps it alive while the visitor stays. Leaving early fast-forwards to its endpoint. Scrolling back up shows that section's own endpoint with ↺ Replay.
3. No App/Agent toggle below the hero. The first scroll leaves from whichever side the visitor was on.
4. All copy is real DOM text. The stage is decorative and never the only carrier of meaning.
5. Nothing claims the visitor's machine did anything. The demo is an example and says so.

## 2. Code facts that shape the design (verified on `17e46de99`)

| Fact | Where | Consequence |
|---|---|---|
| The hero editor is the real editor: `EditorRuntimeProvider`, `RemotionPreview`, `TimelineEditorCoreBody` | `H/PublicAstridEditorProvider.tsx:39`; `H/PublicAstridEditorParts.tsx:61,80` | Drive the real editor, never a second one |
| **The hero is already a live 3D stack.** The stage has `perspective` (`H/PublicAstridShell.css:300`); `.astrid-editor-tilt` and `.astrid-editor-surfaces` are `preserve-3d` (`:394,403`); each surface has its own `translate3d(…, -175px…160px) rotateY()` per audience (`:870-953`); the assembly is `rotateX(5deg) rotateY(-8deg) scale(.9)` (`:891`). DOM: `H/PublicAstridMountedEditor.tsx:118-146` | as listed | The §2 stack is a third arrangement of the live surfaces. `overflow:hidden` on a surface only flattens that surface's own contents |
| The App/Agent switch animates `left/top/width/height` (reflowing the live editor every frame) with a 720 ms move | `H/PublicAstridShell.css:415-440`; `H/publicAstridMotion.ts:43` | Journey poses move with `transform` and `opacity` only, keeping each surface's hero box |
| Motion timing compares audience only (`sameExperience`, `routeMotionTiming`) | `H/PublicAstridShell.tsx:154`; `H/publicAstridMotion.ts:5,35` | Add the journey pose to the motion contract, or give the journey its own controller (T5 decides) |
| **Phones flatten the 3D**, and the phone hero is stacked (copy above, stage about 470–650 px tall below) | `H/PublicAstridShell.css:1497-1695,1581-1584` | Phones need a pin-and-scale handoff to a ~45svh sticky stage and an orthographic §2 stack (part 3.6) |
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

## 3. Architecture

### 3.1 Page structure

**First try** making the existing showcase the sticky element inside a taller landing grid. That keeps the editor's mount and the hero layout untouched (moving `.astrid-showcase` would be a large edit to a fast-changing 900-line Shell). Only if that fails, T5 falls back to a separate sticky track, and records why.

```html
<main class="astrid-public-site" data-audience="app|agent" data-journey="hero|extend|generate|edit|vision">
  <div class="astrid-landing-grid">                      <!-- existing grid, now tall -->
    <section class="astrid-showcase">                    <!-- position: sticky; top: 0; spans hero..§4 -->
      …existing stage…
      <div class="astrid-editor-surfaces">                <!-- preserve-3d -->
        four live surfaces · Runtime layer (HTML) · layer labels · conduit pillars   <!-- siblings, not children -->
      </div>
      <div class="astrid-journey-overlays" aria-hidden="true">mink, cursor, markers, flashes (flat)</div>
      <div class="astrid-journey-extras" aria-hidden="true">History, readouts, tray, example panels</div>
    </section>
    <div>…hero copy (in flow)…</div>
    <section data-journey-section="extend" id="extend">   <!-- left column: header + its own spine + tabs, sticky within the section -->
    <section data-journey-section="generate" id="generate">
    <section data-journey-section="edit" id="edit">
  </div>
  <section data-journey-section="vision" id="vision">finale (in flow, over the sky)</section>
</main>
```

- **Per-section left column.** Each section's header and its own flow spine sit in one column that is `position: sticky` within that section, so header and spine scroll in and out together and only the stage spans sections. The spine is real DOM and is the section's transcript (no sr-only copies). Reserve the spine's final height so arriving turns never shift layout.
- The chat surface stays in the stage as §2's Agent layer and is hidden after §2.
- The finale sits outside the sticky range, so the stage scrolls away before §5.
- Mount the journey from `H/PublicAstridSite.tsx`; add only mount points and attributes to `PublicAstridShell.tsx` and `PublicAstridCallouts.tsx`; each new journey component stays under 300 lines. Don't name a folder `sections/`.

### 3.2 State lineage (section projections)

Order is explicit: `hero → extend → generate → edit → vision`.

| Projection | Timeline | Presentation |
|---|---|---|
| Hero | `V1` "Light study": `light-study-01` 0–8, `-02` 8–20, `-03` 20–28 (`H/content/light-study-v1/timeline.ts:4`) | Existing hero contract, App or Agent |
| §2 end | Hero + music clip on `A1` | Three examples complete; spine ends "Run LTX-Video locally on my GPU." / "LTX-Video is ready on your GPU." No lake media |
| §3 end | §2 + `V2` "Lake at dawn" (`role: 'source'`, silent, `volume: 0`) with `lake-01`…`lake-05` | Tray and readouts complete |
| §4 end | §3 with edits to `V1` and the music level only; `V2` unchanged | History complete; three chips |
| Finale | §4 retained | Editor presentation inactive |

Scrolling back up restores that section's own projection (§2 shows no lakes).

### 3.3 The publisher (`J/publicAstridJourneyData.ts`)

- One journey session per mounted public editor, not a module singleton. The hero example stays immutable.
- A **fixed registry** with every journey asset URL from the start (registering doesn't fetch).
- One stable provider and `QueryClient` (`H/PublicAstridEditorProvider.tsx:23,37`). Publish copies the config with a strictly increasing version, invalidates through the timeline key helper (`V/hooks/useTimeline.ts:12`; suffixed keys at `V/hooks/useTimelineQueries.ts:49` match a prefix invalidation unless `exact: true`), and resolves an acknowledgement when that version is adopted.
- Replaying older content publishes it with a **new, higher** version.
- Skipped steps coalesce to the final snapshot; stale callbacks die by operation id.

### 3.4 The scroll reader and the director (`J/publicAstridDirector.ts`, pure)

**One passive, rAF-coalesced scroll reader** (cached section tops, hysteresis) computes both the active section and sky progress. It is deterministic on load, hash navigation and scrollbar jumps. Trigger lines (part 10.2): desktop/tablet activate at 66% of viewport height (back at 72%); phone 78% (back 83%); "leave hero" at scroll ≥ 10% of the viewport (back at 4%).

| Situation | Behaviour |
|---|---|
| Enter a section the first time | Pose change, then the demo once the base snapshot is adopted |
| Leave downward early | Fast-forward within 600 ms: overlays pop out, the endpoint publishes, clips glide once, History/chips/tags/readouts appear complete without stamps |
| Jump over sections | Commit skipped endpoints in order; render only the destination. Poses retarget, never queue |
| Scroll back up into a finished section | That section's projection plus ↺ Replay |
| Replay | Reset the section's presentation; publish its base with a new version |
| §2 tabs | Selection is separate from completion |
| Tab hidden / `visualActive` false | Pause; resume without one giant tick |
| Reduced motion | Never play. Endpoints at once; manual tabs; "Show the steps" (part 10.5) |
| Secondary effects | Start ≥ 120 ms after a pose begins (the floor rule), so a replaced pose never flashes its extras |

Gate on the shell's `visualActive` (`H/PublicAstridShell.tsx:166`); generation ids as the sky does (`H/publicAstridSkySession.ts:379`). Integer ticks. Unit-test every row with a manual rAF queue.

### 3.5 Data flow

```
scroll ─► scroll reader ─► active section ─► data-journey (CSS pose, transforms only)
                       │                └─► director.enter / leave / skip
                       └─► sky progress (quantised) ─► sky fast path (raster channel)
director clock (rAF, gated) ─► step i
   ├─ snapshot i ─► publisher.publish(v+1) ─► invalidate ─► poll adoption ─► ack
   ├─ chat turns ≤ i ─► section spine
   └─ cues ─► mink / cursor / markers / stamps / chips (DOM + CSS, token timings; no React render per frame)
```

### 3.6 The transitions are poses of the live panels

- **Hero → §2 (pull-apart, ~1.3 s):** freeze the pointer tilt (eased to 0 first), pause the preview, retract the callouts, dissolve the stage frame. The assembly tips to the stack pose; each surface travels to its own depth; the chat surface folds (App: grows out of the launcher; Agent: folds down) into the Agent band; a Runtime layer (new HTML, a fifth child of `.astrid-editor-surfaces`) rises from below; labels fade in. The music clip is published under the motion. Interrupting retargets, as App/Agent does today.
- **§2 → §3 (fold, ~0.84 s):** a pose change to `generate`; the timeline leads and lands flat as the bottom strip at `scale(.84)`; the frame re-forms. Nothing remounts.
- **§3 → §4 (grow, ~0.72 s):** a pose change to `edit`: the timeline scales `.84 → 1` and rises (a dolly-in; no zoom change, so no reflow).
- **Rules:** transforms and opacity only (the App chat growing out of its launcher reuses today's geometry move, its content hidden meanwhile); identical transform function lists across poses; keep `transform-origin: 35% 42%` and re-centre through `translate: var(--astrid-centre-x)` plus a y term; labels and pillars are siblings of the surfaces; nothing measured per frame.
- **Phones (≤640 px):** the stacked hero's stage pins at the top and scales into ~45svh (top-centre origin, no jump of the text below). §2 is an **orthographic** stack: each surface `rotateX(58deg) rotateZ(-10deg)` in a flat parent, 40 px apart, ~260 px wide, top 60% of the stage; the selected example sits as one compact card in the bottom 40%. Section text and spine sit below the stage. Tablet (641–1099) uses desktop poses with the phone's pin-and-scale handoff.

Exact beats, values and the reverse paths: part 10.

## 4. Workstreams

### W1. Scroll and the sticky stage (T5)
1. `.astrid-public-site`: `overflow: clip` → `overflow-x: clip`; `100vh` → `100svh` (`H/PublicAstridShell.css:28-33`). If the tilted editor stretches the document, clip only the hero row.
2. Make the showcase sticky in the taller grid (part 3.1); the stage row never exceeds the viewport: `min(clamp(…), 100svh - 40px)`, with a short-viewport override (`:295`).
3. Move `view-transition-name` off `.astrid-landing-grid` (`H/PublicAstridSite.css:42`).
4. Callouts: retract with today's vacuum on leaving the hero, unmount after the tilt has eased to 0 (mount `H/PublicAstridShell.tsx:890`; listeners `H/PublicAstridCallouts.tsx:908`; tilt `:458`).
5. Re-point the layout-glide selectors (`H/usePublicAstridLayoutGlide.ts:3`).
6. Phones: pin-and-scale handoff (part 3.6).

### W2. Poses (`data-journey`) (S2, T5, T8)
- `data-journey` next to `data-audience` (`H/PublicAstridShell.tsx:672`) and on the stage (`:770`).
- One CSS block per surface per pose, after the audience blocks (`H/PublicAstridShell.css:863,883,1079`), values from tokens and CSS custom properties. Assembly poses share one function list: `rotateX() rotateY() rotateZ() scale()`.
- `useInactiveSurface` (`H/PublicAstridShell.tsx:108,282`) and surface `aria-hidden` (`H/PublicAstridMountedEditor.tsx:120,150`) take the journey into account; keep the conversation loaded through §2 (`:94`).
- Reduced-motion equivalents of `H/PublicAstridShell.css:1715,1757,1793`.

### W3. The scroll reader and director (T3)
Part 3.4. Pure reducer, unit-tested; one scroll reader for section and sky progress.

### W4. The demo timeline (S1, T1, T2, T9)
- **Publisher:** part 3.3; spike S1 first.
- **Snapshots as data** (`L/journey-snapshots.ts`): precomputed from `LIGHT_STUDY_TIMELINE` with tiny immutable helpers over the pure patch ops. A unit test validates every snapshot; every §4 snapshot asserts `V2` is unchanged. **One constant** feeds both a number in the copy and its snapshot (e.g. "It runs N seconds now").
- **Clip motion** (journey-scoped): `transition: left, width` on `[data-action-id]` in `.astrid-timeline-surface`, duration and easing from tokens; a new clip id fades in.
- **Fit-to-width** (`J/useJourneyTimelineFit.ts`): `scaleWidth = (laneWidth - gutter) * 5 / 28`, real gutter (144 / 56), clamped 40–1000; save the hero zoom on leaving the hero, restore it on return. `pointer-events: none` on the timeline in journey poses.

### W5. The spine and the agent-action device (T11, T12, T28)
- `J/PublicAstridJourneySpine.tsx` on `ConversationPresentation`, chronological, one per section in its left column, all turns in DOM; older turns recede to .55; phones show the latest two visually.
- **Carry-over:** §2 starts its own thread; §3 opens with §2's LTX pair faded; §4 opens with §3's last pair faded; §4's first request never repeats the hero's.
- **Pending:** "Thinking" with a pixel ellipsis replacing the spinner (host CSS) for 600 ms before each reply.
- **Chips** sit directly under their reply and land when the edit finishes (narrow render slot; `tool_group` gives structure).
- **The device** (`J/JourneyAgentAction.*`): one vocabulary, three variants (stamp pill, `set up by your agent` line, tool-call chip with a pixel wrench). Lit layer = text plus dot. All DOM text.

### W6. Overlays and the mink (T10, M1)
- **One flat overlay layer** with computed positions (part 2): mink, cursor, beat markers, flash rectangles, the §2 cable. Anything pointing into the 3D stack reads one 1 px anchor inside its layer **once after settle** and on resize, never per frame.
- **`PixelSprite`**: strips, a 70 ms tick, one-shot/loop/hold, `--px = devicePx / devicePixelRatio`, rest positions snapped to device pixels, hop arc, pop in/out, reduced-motion frame, glyphs. The mink never sits inside a scaled or 3D-transformed element.
- **The "You" cursor:** inline SVG pointer plus pill label on the same layer.
- **Beat markers:** at `x = laneOrigin + t × scaleWidth / 5`. Don't turn on the extension overlay host (`H/PublicAstridEditorProvider.tsx:53`).

### W7. §2 The extendable creative suite (S2, T8, T13, T14, T15)
- **The stack** is the live surfaces in the `extend` pose plus the Runtime layer (part 3.6, part 10.3). The Agent layer is the chat surface clipped to its composer band (`clip-path: inset(calc(100% - 64px) 0 0 0 round 10px)`).
- **The Runtime layer** is real HTML: model runners, workflows, tools, workers, packs, chips for ComfyUI, Wan2GP and Flux. Call it `backendLayer` in code; the label says "Runtime".
- **Conduits:** 2 px pillars rotated 90° about X between layers, drawn with `scaleY 0→1`; on phones, plain 2D lines.
- **Examples are real `<button>`s** (a 3-segment control, tablist semantics), one auto-cycle of 6 s per tab resting on New model; the first click stops cycling; never under reduced motion.
  - **3D view (Panels):** live three.js in its own panel, `import()`ed when §2 is a section away (watch hero load cost in R1). Scene from the hero timeline plus music: one textured plane per clip from the light-study thumbnails, a waveform strip, a time axis; camera sways ±18° yaw on an 8 s sine (no full orbit); DPR ≤ 2; render only while active; dispose on tab change or exit. The code panel shows the **actual** module source, so the module stays short and readable. Reduced motion and no-WebGL: one still frame of the same view (captured by T13).
  - **Beat-sync (Agent):** a workflow card ("music-video cut", "Community workflow · adapted by your agent", saved for reuse) and a waveform using the same beat list §4 uses; the mink plugs a cable into an "audio analysis" block.
  - **New model (Runtime):** an install log (marked illustrative); the mink pushes an LTX-Video block into its Runtime slot; its conduit lights through the layers to a new option on the Panels layer. No separate 3D LTX box beside the stack.
- Leaving §2 always produces the canonical LTX-ready handoff.

### W8. §3 Open models, without the setup pain (T17, T18)
- **The tray** (`J/PublicAstridGenerationTray.tsx`, lazy, loaded one section ahead): five cards. Stills develop; reframe animates explicit `width`/`height` and crossfades to the 9:16 file; each card plays its clip **once**, then a dashed drop line draws to its `V2` slot and the clip appears there with a "changed" flash. Cards stay in the tray (no flying clones). One video plays at a time; offscreen videos stop; a failed video keeps its poster. A skipped section publishes the five-clip endpoint once.
- **Readouts:** "Your machine" (a scenario title, no detection) and "Cloud", each with `set up by your agent` and the **"Example"** label; lines type out (part 10.4). Model and tool names are fine; no GPU specs, VRAM, timings or counts.
- **Media** follow the light-study convention (`H/content/light-study-v1/media.ts:9`): files in `P/`, pinned `sha256` and `duration`, `origin: 'immutable-public'`, URLs via `BASE_URL`.

### W9. §4 A creative partner with deep tools (T19, T20)
- Fit-to-width, History (journey presentation data, separate from editor undo), cursor and mink cues, beat markers from A1's beat list, chips under replies.
- Edits touch `V1` and the music volume only; `V2` recedes to .55 and becomes the mink's stage.
- The preview stays paused (the speed change would remount it).

### W10. §5 and the scroll-driven sky (S4, T21, T22)

**Why not `setManualHours`:** it (`H/publicAstridSkySession.ts:511`) notifies the controls listeners, re-rendering the shell; in twilight the palette changes nearly every tick.

**A fast path on the session:**

```ts
// session state, set by claim/release
let scroll: { from: number; span: number; progress: number } | null = null;

// effectiveHours (:192): use scroll when set; cloud hours stay on the real clock
const base = settings.hours ?? (scroll ? wrapHours(scroll.from + scroll.progress * scroll.span)
                                       : zonedHours(date, location.timeZone));

const setScrollProgress = (progress: number) => {           // progress already quantised to 1/48
  if (destroyed || !scroll || settings.hours !== null || replay || reviewPlaying) return;
  if (progress === scroll.progress) return;
  scroll = { ...scroll, progress };
  // re-derive scene and snapshot as emit() does, then:
  writePalette(paletteTarget?.element ?? null, snapshot.palette);  // only at section boundaries (held palette)
  if (themeOrInkChanged) controlListeners.forEach((l) => l());    // rare: one shell render
  listeners.forEach((l) => l());                                   // raster repaint next rAF
};
```

- **Quantise** progress to 1/48 steps (visible pixel steps of the sky); **size the canvas from a stable height** (not a per-resize `innerHeight`), debounce resize. S4 reports raster ms per paint.
- Manual sky controls stay authoritative. Keep `controlsSnapshot.palette` consistent with what was written (`H/PublicAstridShell.tsx:695`). Cache `Intl.DateTimeFormat` per time zone (`H/publicAstridLocation.ts:52,66`).
- **Window:** the visitor's time to the opposite peak (`H/publicAstridSkyRender.ts:322,366`): peak sun = `(sunrise + sunset) / 2`; peak moon = `(sunset + sunrise + 24) / 2` (the private `MOON_TWILIGHT_HOURS`, `:45`, cancels out).

```ts
const forward = (from: number, to: number) => wrapHours(to - from);
function scrollWindow(date: Date, location: PublicAstridLocation) {
  const from = zonedHours(date, location.timeZone);
  const { sunrise, sunset } = sunTimes(date, location);
  const isDay = skyState(from, { sunrise, sunset }).body === 'sun';
  const target = isDay ? wrapHours((sunset + sunrise + 24) / 2) : wrapHours((sunrise + sunset) / 2);
  return { from, span: forward(from, target) };
}
```

- Twilight band (`body: 'none'`): night after sunset, else day. Polar day/night (`:336`): +12 h. Capture the window once per visit; keep it through Vision and tab hiding. `progress` runs 0 at the top of §2 to 1 at the finale.
- **Hold the UI palette per section** (theme switch `DUSK_SWITCH.at = 0.46`, hard ink, `H/publicAstridSkyRender.ts:75,120`): commit the new palette at section boundaries with a 720 ms `settle` colour transition on journey text and panels (no view transition during scroll). The sky picture keeps moving.
- **Ownership:** claim/release from the journey keyed on `visualActive`; Vision registers into the same slot (`H/PublicAstridVision.tsx:339`; session `:567`): release on Vision. Phones and reduced motion use the same claim, stepping once per section.
- **Finale** (`J/PublicAstridJourneyFinale.tsx`): eyebrow, headline, one line, one link ("Read the full vision →", `href="/vision"` plus the in-page follow, `H/PublicAstridShell.tsx:741`; `H/publicAstridLinks.ts:11`). Reveal with the Vision `[data-reveal]` values (`H/PublicAstridVision.css:554`), moved to a shared module. No horizon lights in v1.

### W11. Phone, reduced motion, accessibility, deep links (T23, T24)
- Phone: part 3.6 and part 10.5. Reduced motion: part 10.5.
- Accessibility: `<section aria-labelledby>` with real `h2`s; the spines are the transcripts; stage overlays `aria-hidden="true"`; the tab control and Replay labelled; hidden surfaces `inert`. Tests for heading order, tab keys, Replay and "Show the steps" focus, and inertness (`H/PublicAstridShell.accessibility.test.tsx:107`).
- Deep links `id="extend|generate|edit|vision"`. Same-page hashes must not start a room transition (`H/PublicAstridSite.tsx:68`; `H/PublicAstridShell.tsx:608`). Vision saves the full Home URL and back restores it (`H/PublicAstridSite.tsx:78,85`); extend to scroll position and section.

### W12. Tests, captures, the preview (P1, H0, T26, R1)
- **Unit (vitest, Node 20):** director rules (manual rAF queue, `H/PublicAstridCallouts.scheduling.test.tsx:59`; fake timers, `H/PublicAstridSite.lifecycle.test.tsx:98`); snapshot validity; publisher versioning and replay; the scroll reader with a stubbed layout (the setup's IO is a no-op, `src/test/setup.ts:10`); reduced-motion flips (`H/PublicAstridShell.accessibility.test.tsx:79`); motion primitives' step counts.
- **H0 captures** (part 9.4): the medium every TASTE task and R2 judge from.
- **E2E:** `tests/e2e/public-astrid-journey.spec.ts` (collected by default, `playwright.config.ts:92`), driven with `page.clock`: section end states (clip `left`/`width`, track count, spine turns), flick, back up with Replay, Vision round trip, reduced motion, the phone project.
- **Performance** is measured once, in R1.

## 5. Section content (copy and data)

Clip ids: `light-study-01` "First light" (0–8), `-02` "Passing shapes" (8–20), `-03` "A quiet finish" (20–28), on `V1`. Timings for every beat are in part 10.4; T0 owns final copy and timing.

### §2
| Tab | Request | Lit layer | Panel | Stamp |
|---|---|---|---|---|
| 3D view | "Add a 3D view of the edit." | Panels | Code panel (`structure-view.ts`, real source) + live view | `built by your agent` |
| Beat-sync | "Build me a beat-sync tool." | Agent → Runtime ("audio analysis") | Workflow card + waveform with markers | `built by your agent` |
| New model | "Run LTX-Video locally on my GPU." | Runtime → all layers | Install log (illustrative); LTX-Video block in Runtime | `installed by your agent` |

Endpoint: all three complete; music on `A1`; spine ends "Run LTX-Video locally on my GPU." / "LTX-Video is ready on your GPU."

### §3
Requests: "Make five stills of the lake at dawn with Flux, on my GPU." · "Make them vertical." · "Animate them in the cloud with Wan." Replies: "Reframed to 9:16." · "Five stills, reframed and set in motion." Route pills: `Local · Flux · ComfyUI`, `Cloud · Wan · Wan2GP`. Readouts (T0 finalises; no specs or timings): *Your machine*: "✓ Flux.1 dev, via ComfyUI" · "✓ running on your GPU" · "✓ reframed to 9:16 · Flux Fill". *Cloud*: "✓ Wan 2.2, via Wan2GP" · "✓ 5 clips · 5 s each". Snapshot: `track.add` `V2` "Lake at dawn" (`role: 'source'`), then `lake-01`…`lake-05`, one per landing.

### §4
| Step | Chat | Snapshot change | History · chip |
|---|---|---|---|
| 1 | User: "I'll shorten the opening. Close the gap behind me." | `-01` trimmed by the cursor | "You · trimmed First light" |
| 2 | Astrid: "Closed the gap. It runs N seconds now." (N from the snapshot constant) | `-02`, `-03` moved | "Astrid · moved Passing shapes" · `arrange · 3 clips` |
| 3 | User: "Cut every clip on the downbeat." → Astrid: "Done. Every cut lands on a beat." | Cut points snapped to the nearest downbeats from A1 | "Astrid · cut on 3 downbeats" · `beat-sync · 3 downbeats` (strong fill) |
| 4 | — | `A1` `volume: 0.6` (cursor) | "You · lowered the music" |
| 5 | User: "Slow the middle scene and crossfade into the last frame." → Astrid: "Slowed to 0.6× with a 1.5s crossfade." | `-02` `speed: 0.6`; `-03` `transition: {type: 'crossfade', duration: 1.5}` | "Astrid · slowed Passing shapes" · `retime · crossfade` |
| 6 | — | `-03` extended (cursor) | "You · extended A quiet finish" |

`V2` is asserted unchanged at every step.

**Retime arithmetic.** Duration applies speed once; the incoming transition already adds pre-roll (`V/lib/config-utils.ts:98`; `V/compositions/VisualClip.tsx:640`), so don't subtract 1.5 s from `at`. A feasible shape from the 8/12/8 cut: middle at 8, source 0…8.4 at 0.6 → 14 s; final at 22, source 2…8 → 6 s; total 28 s. T1 authors the exact numbers once A1's beat list exists.

### §5
No script: the sky runs to its end over the scroll, the finale text reveals, the mink looks up at the peak.

## 6. Assets

### 6.1 Placeholders (in scope)

| ID | What | Route | Spec |
|---|---|---|---|
| A1 | Music, 28 s | Procedural loop at a fixed BPM (Astrid chiptune pack or a WebAudio offline render), quiet, so the beat list exists by construction | MP3 128 kbps + `L/journey-audio.json` (beats, downbeats); sha256 and duration pinned |
| A2 | Lake media | Five 16:9 stills by Codex image generation (`codex exec --enable image_generation`, 1280×720); 9:16 **crops** (720×1280); five 5 s **silent** clips by an FFmpeg slow pan/zoom over each still (720p, H.264, muted); posters and timeline thumbnails | Encoded at display size; `volume: 0` in the snapshots; sha256 and duration pinned |
| A5a | Mink placeholder kit | Existing art, no resampling except the exact ÷4 nearest-neighbour of `astrid-mink-front.png`: front, juggler crops, the run strip, spark and thought glyphs (part 10.6) | One JSON per strip (frame size, count, feet anchor, ms) |
| A9 | Pixel icons | 16×16 grids in `H/PublicAstridPixelIcons.tsx` format: monitor (Local), cloud, wrench (chip) | Crisp at D and P, both palettes |

### 6.2 Deferred real assets (only on the user's word)

- **Real music** (original or licensed), with its beat list.
- **A real generation run** (Flux via ComfyUI, Wan 2.2 via Wan2GP, an LTX install) on rented GPUs, roughly $10–30, with receipts; then the readouts may print measured facts and drop "Example".
- **Final mink strips** A5b–A5h (7 strips, 27 frames: `sit`, `carry`, `push`, `snip`, `plug`, `lookup`, "!"), checked with Astrid's `pixel.strip`/`pixel.sprites`, then M1's second pass on them.

Because placeholders use the real registry format and dimensions, each swap is data only.

## 7. Tasks

**Tiers:** NORMAL = Codex Luna (`gpt-6-luna`) · XHARD = Codex Sol (`gpt-6.1-sol`, reasoning xhigh) · TASTE-HIGH = Claude Opus 5.5 · TASTE-LOW = Claude Sonnet 5.5 · ASSET = generation or capture (placeholders). Every senior agent fans legwork out within its family (executor brief).

**Visual checks:** **D** 1586×992 light and dark · **P** 390×844 light and dark on every visual task. **N** 320×693, **S** 1440×700 and **RM** reduced motion only in T6, T8 and R2. H0 ids name the evidence (part 9.4). A TASTE task's done-when is its named stills and recordings, judged at 2× against the named mockup, not "tests pass". **Every TASTE-HIGH task has two passes:** pass 2 runs once its moment is on the preview, folding in any notes the user has sent (never waiting for them).

### Phase 0 (parallel, after Step 0)

| ID | Tier | Goal · files | Deps | Done when |
|---|---|---|---|---|
| T0 | TASTE-HIGH | The Opus sheet: all copy (requests, replies, History lines, readout and install-log lines, Runtime labels, Replay and reduced-motion labels), section beats and timings, each section's ambient cycle at rest (contents, variation pool and cadence; part 10.1, principle 8), and `J/journeyMotion.ts` tokens plus matching CSS custom properties, seeded from part 10 (may tune any value ±20%) | — | Each token names its hero source line; a grep of `J/` finds no `ms` or `cubic-bezier` literal outside the tokens; §4's opening doesn't repeat the hero; the notes lineage file is seeded |
| P1 | NORMAL (+ coordinator) | **The Artifact preview, from today's hero**: a preview HTML entry calling `renderPublicEntry()`, a preview Vite config (`base: './'`, that HTML as `rollupOptions.input`, no service worker or manifest), root-absolute assets moved to `BASE_URL`/imports (part 2 list), the `useEditorSettings` storage write wrapped in try/catch, and `scripts/preview/build-artifact.sh` emitting `dist-preview/`. The coordinator publishes the emitted files plus referenced media (not `public/`) as a multi-file Artifact (two publishes if over 255 files) | — | Today's hero renders from the Artifact on desktop and the user's phone: both audiences, both palettes, editor, mink, fonts, sky; zero failed requests in the network log; file count and bytes recorded; one script rebuilds and the coordinator republishes to the same URL. If entry or CSP fails: the LAN `vite preview --host` fallback becomes the preview |
| H0 | NORMAL (run by a Claude session) | Capture harness: `scripts/capture/journey-capture.ts` + `playwright.capture.config.ts` (outside the default E2E match), `page.clock`, scroll profiles, all part 9.4 ids at D and P, each also `-rm`; ids are added as their sections land (v0: `pull-app`, `pull-agent`, `pull-interrupt` for S2) | — | All existing ids record from one command; reruns give identical stills (seeded blinks) |
| S1 | XHARD | Publish three visibly different snapshots through a journey provider, then replay the first with a higher version · `J/publication-spike.*`, provider test, E2E fixture | — | All versions adopted in order; same editor instance; zero history entries, zero `saveTimeline` calls, zero writes to `astrid.timeline-drafts`; a stale publish can't win |
| S2 | XHARD (+ Opus partner) | The live stack pose: `extend` pose on `.astrid-editor-surfaces` with per-surface depths, chat clip-path band, launcher growth (App), fold-down (Agent), sibling labels and pillars, a Runtime child, phone orthographic slabs, reduced-motion static stack plus dip. Values from part 10.3; the T8 Opus agent judges the captures in the same spike | H0 v0 | `pull-agent-D-480` shows no plane cutting another; `pull-interrupt-D` has no jump or blank frame; a WebKit run of `pull-app-D` matches Chromium; `pull-app-P-1320` shows the flat slabs; transforms and opacity only (no layout in the performance trace) |
| S4 | XHARD | Scroll-driven sky with ownership: the fast path, 1/48 quantisation, stable canvas height, held palette, claim/release | — | Scrub through dusk, midnight and twilight, open Vision, return: no React commit per scroll frame, no stale inline palette, same window restored; raster ms per paint reported at D (4× CPU throttle) and on an iPhone (LAN preview); RM stepping works |
| A1 | ASSET | Placeholder music + beat list (part 6.1) | — | Digest, duration and beats verified; waveform legible at P |
| A2 | ASSET | Placeholder lake media (part 6.1) | — | Five stills, crops, silent clips, posters, thumbnails at spec; contact sheet looks plausible at D and P |
| A5a | ASSET | Mink placeholder kit (part 6.1, part 10.6) | — | Every cue in part 10.6 has a mapped placeholder that renders in H0 at D and P |
| A9 | ASSET | Pixel icons (part 6.1) | — | Crisp at D and P in both palettes |

### Phase 1: foundation

| ID | Tier | Goal · files | Deps | Done when |
|---|---|---|---|---|
| T1 | NORMAL | Scripts, snapshots and registry to T0's numbers · `L/journey-script.ts`, `journey-snapshots.ts`, `journey-media.ts` | S1, T0, A1, A2 | Every snapshot validates; projections follow part 3.2; §4 never changes `V2`; copy numbers come from the same constants |
| T2 | XHARD | Session-owned publisher and adoption bridge · `J/publicAstridJourneyData.ts`, `H/PublicAstridEditorProvider.tsx`, `H/PublicAstridMountedEditor.tsx` | S1, T1 | Publish, replay and race tests pass; one provider instance; hero bundle immutable |
| T3 | XHARD | Scroll reader, pure director, projections and clock (trigger lines, retarget-never-queue, 120 ms floor, fast-forward, "Show the steps" mode, and an **ambient phase** after each demo that plays T0's ambient beats with variation, pauses off-screen or when hidden, and is skipped under reduced motion) · `J/publicAstridDirector.ts`, `J/usePublicAstridDirector.ts`, `J/publicAstridScrollReader.ts`, tests | T0, T1, T2 | Every part 3.4 row is a passing test; initial `#edit`, scrollbar jumps and boundary oscillation pick the right section without flicker; `flick-D`/`flick-P` show no stack, tray or label flash |
| T5 | XHARD | Sticky showcase in the tall grid (or the recorded fallback), per-section sticky left columns, leave-hero beat (vacuum retract, tilt eased to 0 before unmount, preview playing at rest), frame dissolve/re-form hooks, phone pin-and-scale · `J/PublicAstridJourney.tsx`, `H/PublicAstridSite.tsx`, Shell mount points, CSS | S2, T3 | One editor; no doubled scroll height; sticky ends before the finale; `pull-app-P` shows no jump of stage or text; between 10% and the trigger the hero rests, still playing |
| T9 | NORMAL | Fit controller and hero zoom restore · `J/useJourneyTimelineFit.ts` | T2, T5 | D/P/N fits use the real gutter; stable on resize; clamped; hero zoom restored; `V1+A1+V2` fits at 320 px |
| T10 | NORMAL | Flat overlay layer with computed positions + `PixelSprite` (part W6) · `J/JourneyOverlay.tsx`, `J/PixelSprite.tsx` | T0, T5, A5a | `s4-demo-D`/`-P` stills at DPR 2: every sprite pixel is a uniform k×k block in the mink palette (pixel check); the mink stays with a gliding clip |
| T28 | NORMAL | Shared motion primitives reading only tokens: typed line, stamp, chip receipt, flash, History row, pixel ellipsis, Replay, the reduced-motion slideshow · `J/motion/*` | T0 | Unit tests for step counts, timings and reduced-motion paths |

### Phase 2: §2 and §4 in parallel, the sky, the mink

| ID | Tier | Goal · files | Deps | Done when |
|---|---|---|---|---|
| T6 | TASTE-HIGH | Section layouts: headers (eyebrow types on; headline and sub never animate), section scroll lengths, the composition of every section at D, P, N and S, including phones · `J/PublicAstridJourney.css`, section wrappers | T5, H0 | `pull-app-D-1320` and `-P-1320`: header readable and sticky beside the settled stack; no title or spine collision at D, P, N, S |
| T8 | TASTE-HIGH | The pull-apart and its reverse, from App and Agent, at D and P, plus the RM dip (owns the phone stack) · pose CSS, `J/PublicAstridExtendStack.tsx` | S2, T6, H0 | Signs off `pull-app-D-0/240/600/1320`, `pull-agent-D-0/300/600/1320`, `pull-app-P-1320`, `back-2-1-D`, `pull-app-D-rm` against `mockups/night/02a` and `day/02b` at 2×: the hero coming apart, not a cut to a new scene |
| T11 | NORMAL | Section spines with chip slot, pending ellipsis, reserved height · `J/PublicAstridJourneySpine.tsx` | T1, T3, T28 | Carry-over exact; chips attach to the right reply; replay makes no duplicate turns; `s4-demo-P` shows no spinner and no layout shift |
| T12 | TASTE-LOW | The look of every primitive: stamp, lit layer, chip and flood, typed line and check, History row, tabs, Replay, Departure Mono 11 px | T11, T28, H0 | `s2-demo-D` at the stamp peak, `s4-demo-D` at the flood, and `-P` equivalents legible in both palettes; highlight is text plus dot |
| T13 | NORMAL | Three.js structure view (plumbing; lazy import, dispose, still-frame fallback captured from the scene) · `J/structure-view.ts`, `J/PublicAstridStructureView.tsx` | T1, T8 | No three.js request at hero load; planes match the snapshot; code panel shows the real module; repeated entry doesn't grow canvases; fallback works at D and P |
| T14 | NORMAL | §2 example states and tabs: the first cycle, then T0's ambient cycling with live activity in each example; a click pins one example, progress line, pillar conduits, the cable from an anchor measured once · `J/extendExamples.ts`, `J/PublicAstridExtendExamples.tsx` | T3, T8, T28 | `s2-demo-D` plays the first cycle and `rest-2-D` shows it still alive 20 s later; leaving gives the LTX handoff; resize re-anchors the cable once; keyboard tests pass |
| T15 | TASTE-LOW | Example panels, **including the 3D view's look** (camera, framing, material, sway), the workflow card, waveform reveal, install log, tab-swap motion, cause → light → stamp order | T12, T13, T14 | `s2-demo-D` and `-P`, one still per tab at +2600, against `mockups/*/02a`, `02b`, `02c` at 2× |
| T19 | NORMAL | §4 mechanics: cursor states, History append/shift/tint and phone ticker, the ambient exchanges from T0's pool (snapshot publishes at beat boundaries), beat markers, flash rectangles, wedge/level/dimension strokes · `J/PublicAstridJourneyHistory.tsx`, edit cues | T1, T3, T9, T10, T11, T28 | Each History row matches its snapshot in `s4-demo-D`/`-P`; the ticker shows one row at a time; `V2` unchanged |
| T20 | TASTE-HIGH | The grow and the §4 beats (starts right after the foundation; the grow is finished after T18's fold exists) | T9, T19 | Signs off `grow-D-0/420/840`, `s4-demo-D` stills (trim, mid-carry, 2nd snip, flood, mid-retime, end) and `s4-demo-P` against `mockups/*/04a`, `04b`, `04c` at 2× |
| T21 | XHARD | Sky in the journey: progress from the scroll reader, quantised steps, held palette with the 720 ms boundary transition, quiet field gated to the hero, RM stepping · sky session/geometry, `J/useJourneySky.ts` | S4, T3, T5 | `finale-D` shows visible steps and no colour pop at boundaries; `finale-D-rm` steps per section; Vision return deterministic |
| M1 | TASTE-HIGH | Every mink cue and glyph (part 10.6): placement, frame choice and holding back at D and P, on the A5a placeholders | T10, A5a; cue slots from T15, T18, T20 | One still per cue in `s2/s3/s4-demo-D`/`-P` and `finale-D`: charming, never covering a label, chip or cursor; "!" and the sparkle appear once each across the full recordings |

### Phase 3: §3

| ID | Tier | Goal · files | Deps | Done when |
|---|---|---|---|---|
| T17 | NORMAL | Tray mechanics: develop, reframe (explicit width/height), play once, then the ambient cycle (one clip at a time, in turn), drop line, clip appears; one video at a time; offscreen stop; poster fallback · `J/PublicAstridGenerationTray.tsx`, media controller | T1, T3, T28, A2 | `s3-demo-D-9200` shows drop lines and no clones; only one video plays at a time; landing ids match snapshots |
| T18 | TASTE-HIGH | The fold and every §3 beat at D and P (readout layout included) | T8, T10, T15, T17 | Signs off `fold-D-0/420/840/1200`, `s3-demo-D` stills (3rd still in, mid-reframe, 3rd landing, mink on clip) and `fold-P` against `mockups/*/03a`, `03c` at 2× |

### Phase 4: finale, navigation, accessibility, E2E

| ID | Tier | Goal · files | Deps | Done when |
|---|---|---|---|---|
| T22 | TASTE-HIGH | The finale: shared reveal module (its extraction is a NORMAL sub-step inside this brief), the mink at the horizon, look-up at progress ≥ .98 · `J/PublicAstridJourneyFinale.tsx`, CSS | T6, T21, M1 | Signs off `finale-D` and `-P` at the peak and the look-up frame against `mockups/*/05-finale` at 2×; one Vision link |
| T23 | XHARD | Navigation, lifecycle and hash restore | T3, T5, T22 | Repeated Vision/back restores exact scroll, hash and section (checked on the LAN preview in real Safari); hidden work stops; same-page hashes don't start room transitions |
| T24 | NORMAL | Semantics and keyboard: headings, the tab control's keys, Replay and "Show the steps"/"Pause" focus, inertness | T3, T11, T14, T17, T19, T28 | a11y tests pass; `s4-demo-P-rm` shows the stepped story with opacity changes only; keyboard order checked in a recording |
| T26 | NORMAL | The journey E2E spec with `page.clock` (forward, flick, back, Replay, Vision, RM, phone project); CI installs WebKit or the spec pins to what CI can launch | T23, T24 | The default projects pass locally and in CI |

### Review phase (back end, light)

| ID | Who | What | Done when |
|---|---|---|---|
| R1 | Astra (`gpt-6-astra`, xhigh, legwork to Luna; the coordinator runs the browsers) | **Per section at D and P:** dropped frames and p95 frame time while scrolling (1× and 4× CPU throttle); the longest main-thread task during its demo (adoption commits, three.js init, tray video start, waveform decode); sky raster ms per paint and paints per second; the cost of the ambient cycle at rest (compositor and CSS motion only; no per-frame React; paused off-screen and in hidden tabs); bytes fetched entering it. **Page-level:** hero LCP, TBT and initial JS compared with `main`; peak memory and live video/WebGL counts on an iPhone. **One real-iPhone pass** via Safari Web Inspector on the LAN preview | A short report with numbers against `main`, named regressions and a ranked, tiered fix list |
| R2-D | Opus, **desktop iteration pass** (deploys Haiku subagents for captures and edits) | Iterates on the running page at D and S (1440×700), both audiences and both palettes, from H0 recordings, 2× stills and the live preview. It judges the two priorities first: each section alive at rest (`rest-*`) and every transition really nice (`pull-*`, `fold`, `grow`, `back-*`, `flick`). Then it checks the rest of the journey against part 10 and the mockups, and that every cut-list item (part 10.7) is absent. Each loop: judge → fix taste issues directly (Haiku subagents make the edits; Opus checks them) → send mechanism issues to the coordinator as tiered fix tasks → re-capture. Up to 3 loops | Both priorities pass at D and S on a fresh capture; any remaining findings are tiered for R3 |
| R2-P | Opus, **phone iteration pass** (deploys Haiku subagents for captures and edits) | The same loop at P (390×844) and N (320×693), plus reduced motion and "Show the steps". It includes one look on a real iPhone in Safari via the LAN preview (toolbar collapse, sticky stage, sky), with the coordinator driving the device or the user sending notes. Runs in parallel with R2-D on its own port; layout changes that could affect desktop are checked against D before they're kept | Both priorities pass at P and N on a fresh capture and on the real iPhone; remaining findings tiered for R3 |
| R3 | Tiered like everything else; each fixer follows the fan-out rule (Opus → Haiku, Sol/Astra → Luna) | One fix round over R1's findings and anything R2-D or R2-P couldn't close in its loops | Findings fixed or explicitly dropped; R1's numbers and the R2 priorities still pass on a re-capture |
| R4 | Coordinator, **after asking the user** | (a) May placeholder media ship, or make real assets first (part 6.2)? (b) Merge `feat/home-journey` into `main` | E2E green, budget green, R3 done, the user has seen the preview, the user said go |

## 8. Phase order

| Phase | Runs in parallel | Notes |
|---|---|---|
| Step 0 | branch · Luna pointer re-check · commit the folder | Coordinator |
| 0 | T0 · P1 · H0 · S1 · S2 (with the T8 Opus agent) · S4 · A1 · A2 · A5a · A9 | One heavy Codex test job at a time; S2 waits only for H0 v0 |
| 1 | T1 → T2 → T3 → T5 · T28 (after T0) · then T9, T10 | A short serial chain |
| 2 | §2: T6, T8, T11, T12, T13, T14, T15 · §4: T19, T20 · T21 · M1 as cue slots land | §4 starts with §2 so the payoff gets the most refinement time |
| 3 | §3: T17, T18 · T20's grow after T18 | |
| 4 | T22 · T23 · T24 · T26 | |
| Review | R1 ∥ R2-D ∥ R2-P → R3 → ask the user → R4 | The only review gates; R2-D and R2-P iterate, they don't just report |

TASTE-HIGH pass 2s run as each moment reaches the preview, before R2-D and R2-P.

## 9. How to run it

### 9.1 Repo, branches, worktrees
`banodoco/astrid-app`, branch `feat/home-journey` off `main`. One worktree per parallel task: `git worktree add ../hj-<id> -b hj/<id> feat/home-journey`. The coordinator merges `hj/<id>` into `feat/home-journey`, merges `main` in daily, and re-runs S1's adoption test after each merge.

### 9.2 Agents
- **Codex:** `codex exec -m <model> --skip-git-repo-check -C ../hj-<id> -s workspace-write --add-dir <repo>/.git -o reports/<id>.last.txt "<brief>" < /dev/null`, in the background; Sol adds `-c model_reasoning_effort='"xhigh"'`. No ports, signals or nested sandboxes.
- **Claude:** Agent tool with `model: "opus"` or `"sonnet"`; they deploy Haiku subagents (`model: "haiku"`) for the hands-on work, fixes included.
- **Fan-out:** Sol and Astra deploy Luna subagents (`spawn_agent`, `model: "gpt-6-luna"`) for the hands-on work, fixes included. Every brief says this explicitly (part 9.6).
- **Preview:** only the coordinator republishes the Artifact (P1's script, then the Artifact publish with the same file path/URL). Fallback: `vite preview --host` from `dist-preview/`, opened at the Mac's LAN address `/home` on the iPhone (or a quick tunnel).

### 9.3 Dev server, tests, rules
- `npm run dev` serves port 2222 (`config/vite/policy.ts:1`); taste agents use 2223+. Open `/home`. The public path needs no backend; Supabase vars can be placeholders. The build needs the selected or bundled Astrid source and a valid tool catalog (`config/vite/astridSource.ts:67`).
- vitest on Node 20.19.4 (executor brief), `--maxWorkers=2..4`; don't use `vitest.public-host.config.ts`.
- E2E: `npx playwright test --config playwright.config.ts tests/e2e/public-astrid-journey.spec.ts` (boots its own Vite and fake Runtime; `chromium-condensed`/`chromium-mobile` are WebKit).
- `npm run lint` allows zero warnings; `react-hooks/exhaustive-deps` is an error. No `@/integrations/supabase/client` in journey code. Palette tokens (`--astrid-*`), never hard-coded colours. Lint and debt allowlists only shrink. `npm test` rejects placeholder smoke tests. No `ms`/`cubic-bezier` literals in `J/` outside the tokens.

### 9.4 H0 capture ids
Recordings `h0/<id>-<D|P>.webm`; stills `h0/<id>-<D|P>-<ms>.png` at 2× DPR. Scroll profiles: **slow** 400 px/s, **flick** 3000 px/s, **back** 600 px/s. Ids: `pull-app`, `pull-agent`, `pull-interrupt` (App→Agent switch, then scroll at 300 ms), `back-2-1`, `fold`, `back-3-2`, `grow`, `back-4-3`, `flick` (hero→§4), `s2-demo`, `s3-demo`, `s4-demo`, `rest-2`, `rest-3`, `rest-4` (20 s resting in each section after its demo, to judge that it feels alive), `finale`, each also `-rm`. Seeded blinks keep reruns identical. Judge at 2× against the named mockup, not from contact sheets.

### 9.5 Reports
`docs/plans/home-journey/reports/<id>.md`: what changed, decisions made (with one-line reasons), tests run, checks left for the coordinator.

### 9.6 Brief templates

Fix tasks (hand-offs from R2-D or R2-P, and R3) use the same template for their tier, with the finding and its capture in place of the task row. Every senior fixer follows the fan-out rule: Opus and Sonnet deploy Haiku, Sol and Astra deploy Luna.

**NORMAL (Luna)**
> Task `<id>` (NORMAL) for the Astrid homepage journey. Read `docs/plans/home-journey/PLAN.md` parts `<…>` and the `<id>` row in part 7. Work in `../hj-<id>` on branch `hj/<id>`; touch only `<files>`. Timings and easings come from `J/journeyMotion.ts`; never write `ms` or `cubic-bezier` literals. For any legwork that splits, including fixes, spawn parallel `gpt-6-luna` subagents. Run vitest on Node 20 (`export PATH=<path to Node 20.19.4>/bin:$PATH`, `--maxWorkers=2`). You can't run a dev server or Playwright: list the visual and E2E checks the coordinator should run. Done when: `<row>`. Commit to `hj/<id>` and write `reports/<id>.md`.

**XHARD (Sol 6.1, xhigh)**
> Task `<id>` (XHARD) … *(as NORMAL, plus:)* You own the mechanism and its correctness. Write the tests that pin the behaviour rules first. Deploy parallel `gpt-6-luna` subagents (`spawn_agent`) for the hands-on work (reading, searching, edits, running unit tests), including when you're fixing; keep the design decisions yourself and check what they return. You're bound by the experience, not the suggested implementation: prefer the simplest mechanism that meets the done-when, and record any deviation and anything you chose not to build.

**TASTE-HIGH (Opus)**
> You own the feel of `<moment>` (task `<id>`, TASTE-HIGH). Read PLAN parts `<…>`, part 10, and `notes/opus-craft.md`. Run your own dev server on port `<2223+>` and H0 for `<ids>`; judge at 2× against `mockups/<frames>`. Decide the tuning of tokens, CSS custom properties and choreography yourself. Deploy parallel Haiku subagents (`model: "haiku"`) to make the edits, run captures and read code, and check every result before keeping it. If the mechanism needs changing, write a note for the coordinator rather than rebuilding it. You're bound by the experience (the executor brief), not the suggested implementation. Two passes: pass 2 once it's on the preview, folding in any user notes. Done when: you sign off `<named stills/recordings>`. Append your decisions to `notes/opus-craft.md` and write `reports/<id>.md`.

**TASTE-LOW (Sonnet)**
> You own the look of `<components>` (task `<id>`, TASTE-LOW). Read PLAN parts `<…>` and part 10. Use your own dev server (`<port>`) and H0 for `<ids>`; judge at 2× against `mockups/<frames>` in both palettes at D and P. Change only styling and token use in `<files>`; mechanism changes go back as a note. Deploy parallel Haiku subagents (`model: "haiku"`) for the edits, captures and legwork, and check their results. Done when: `<row>`. Write `reports/<id>.md`.

**ASSET (placeholder)**
> Make placeholder `<asset>` (task `<id>`): `<spec from part 6.1>`. Use `<Codex image generation | FFmpeg | the Astrid chiptune pack | existing art>`. Write files to `P/…` at the given dimensions and durations, compute sha256 and duration, and register them in `L/journey-media.ts` in the light-study format. Placeholders claim nothing real. Done when: `<row>`. Write `reports/<id>.md` with the commands used, so the real asset can replace it as data later.

## 10. Craft details (T0's starting values, from the Opus craft pass)

T0 may tune any number here by ±20% without reopening the design.

### 10.1 Principles
1. **One set of objects.** Everything that moves is the hero's own panels, re-posed. Anything new comes from somewhere: the Agent layer opens out of the launcher or the conversation, the Runtime rises from below, a stamp is put there by the agent.
2. **One motion vocabulary, all from the hero** (10.2). Nothing in `J/` writes its own millisecond or curve.
3. **Scroll picks the place; time plays the moment.** Poses are timed transitions fired at a line; only the sky follows the scroll. Poses retarget, never queue.
4. **One lead at a time:** one primary motion, at most one secondary, and the mink, who leads only when she is the agent doing the edit.
5. **The agent is pixel, the human is vector.** The mink and her glyphs step in whole device pixels on a 70 ms tick; the cursor and the UI glide.
6. **Cause, then receipt:** request → action → the system lights up → the stamp. The stamp is the only thing that overshoots.
7. **Every end state is a composed frame** (phones, reduced motion, flicks, scrolling back).
8. **Alive at rest** (the user's priority, 20 Oct; it replaces the craft pass's "then stillness"). While the visitor is in a section it keeps living. Once the scripted demo ends, the section moves into an **ambient cycle**, so resting there never shows a frozen frame:
   - **§2:** the examples keep cycling, with real activity inside each one: the 3D view sways and follows the playhead, beat-sync marks pulse with the music, and the install log ticks on.
   - **§3:** one lake clip plays at a time, in turn; a readout line occasionally refreshes; the mink checks on a card.
   - **§4:** a short new exchange arrives every so often (a request, Astrid's reply with its tool chip, a small visible edit and a History row), drawn from a small pool of variations so it never repeats mechanically.
   - **Restraint still holds:** one lead at a time; breathing room between beats (part 10.4); nothing frantic; pause when off-screen or the tab is hidden.
   - **Reduced motion:** no ambient cycle; the composed end state.
   - T0 designs each section's ambient cycle (contents, pool and cadence). The cycle is CSS and compositor motion plus snapshot publishes at beat boundaries, never per-frame React work.

### 10.2 Motion tokens and mechanics

| Token | Value | Hero source | Used for |
|---|---|---|---|
| `ease.pose` | `cubic-bezier(.5,0,.15,1)` | `--astrid-surface-ease`, `H/PublicAstridShell.css:418` | Surface, clip, cursor moves; conduit draws |
| `ease.settle` | `cubic-bezier(.22,.61,.36,1)` | assembly transition `:411`; layout glide `H/usePublicAstridLayoutGlide.ts:18` | Assembly tilt, frame fade, colour/opacity, small lifts |
| `ease.enter` | `cubic-bezier(.16,1,.3,1)` | `astrid-callout-in` `:1194`; `astrid-surface-in` `:1902` | Anything appearing |
| `ease.land` (accent) | `cubic-bezier(.34,1.5,.64,1)` | connector end-dot land `:1211` | **Only** the agent stamp and the lit-layer dot |
| `ms.quick` | 260 | composer note `:818`; mink hop `PublicAstridSky.css:97` | Fades out, stamps, chip slides, tab swaps |
| `ms.enter` | 520 | callout text and connector draw `:1196,1203` | Entrances, clip moves, conduit draws |
| `ms.travel` | 720 | `publicAstridMotion.ts:43` | Every pose change, assembly tilt, palette crossfade |
| `ms.ping` | 900 | `astrid-dot-ping` `:1219` | Stamp ping, "changed" flash |
| derived | stagger 60 · floor 120 · fade 360 · label point 0.7 · sprite tick 70 · pending 600 · receded opacity .55 | phone callout stagger `:1826`; retarget floor `publicAstridMotion.ts:80`; MinkRunner 770 ms/11 frames; Agent backdrop `:1369` | — |
| `linear` / `steps(n)` | — | — | The sky / sprites and typed text |

**Mechanics.** Trigger lines: desktop 66% (back 72%), phone 78% (back 83%), leave hero at scroll ≥ 10% (back 4%). Assembly function list everywhere: hero `rotateX(5deg) rotateY(-8deg) rotateZ(0) scale(.9)`, stack `rotateX(58deg) rotateY(0) rotateZ(-8deg) scale(.84)`. Keep `transform-origin: 35% 42%`. Labels counter-rotated (`rotateZ(8deg) rotateX(-58deg)`); if the 2× still shows soft label text, fall back to flat labels measured once after settle. Floor rule: secondary effects start ≥ 120 ms after a pose begins.

### 10.3 Transitions (beat tables)

**Leaving the hero (scroll ≥ 10%).** 0 ms: callouts retract with today's vacuum (connectors 450 ms; cards fade 360 ease-in, −4 px, scale .94, last-in first, 60 ms apart); pointer tilt eases to 0 over 480 `settle`, then the loop stops (never unmount mid-tilt). The preview keeps playing; the frame stays. Back above 4%: today's reconnect (extend 380, 140 stagger, 900 ping).

**The pull-apart (~1.3 s).** Stack at D: layer depths Preview +250, Panels +125, Timeline 0, Agent −125, Runtime −250 (≈ 89 px screen separation), all on one axis; scales player 1.0, inspector 1.2, timeline .8, Agent band 1.0, Runtime laid out at 72% × 30% of the stage.

*From App* (the editor tips back and fans out; Agent opens out of the launcher):

| t (ms) | Beat |
|---|---|
| 0 | Preview pauses on its frame. Assembly tips (720 `settle`). Launcher fades (260) |
| 120 | Frame dissolves (border, fill, shadow → transparent; 520 `settle`). Music clip publishes and fades onto the timeline (360) |
| 180 / 240 / 300 | Preview, Panels, Timeline travel to their depths (720 `pose`), top-down |
| 360 | Chat grows out of the launcher into the Agent band (today's App→Agent geometry, 720 `pose`); content fades in 160 after settle |
| 600 | Runtime rises from −420 to −250, opacity 0→1 (720 `pose`) |
| 684, 744, 804, 864, 1104 | Each label fades in at 0.7 of its layer's travel (260 `enter`, 6 px from the left) |
| 1320 | Settled; 200 ms of nothing, then the §2 demo |

*From Agent* (the conversation leads):

| t (ms) | Beat |
|---|---|
| 0 | Assembly tips. The conversation's clip closes top-down to the composer band (520 `pose`) |
| 120 | Frame dissolves; the three backdrop panels brighten .55 → 1 (520 `settle`) |
| 180 / 240 / 300 | Preview, Panels, Timeline rise to their depths (720 `pose`), above the band on screen before they pass it in depth |
| 420 | The band sinks from +70 to −125 (720 `pose`), only once its clip is mostly closed |
| 600 → 1320 | Runtime and labels as from App |

*Headline:* the §2 header scrolls in normally; at the trigger the eyebrow types on (`steps`, 16 ms a character, ≈ 290 ms, once per visit); headline and sub never animate. *Slow scroll:* the hero rests after the callouts leave; the stack settles about when the header pins. *Flick:* retargeted at once; the floor stops flashes; §2's endpoint is committed in data only. *Back up:* reverse bottom-up — Runtime sinks and fades (360); the band returns to the launcher (App) or reopens into the conversation (Agent: clip 520, rise to +70); Timeline, Panels, Preview follow 60 ms apart (720 `pose`); the assembly tips forward (720 `settle`); the frame re-forms at 480 (360); callouts reconnect after settle; playback resumes after they land; the music clip fades out.

**The fold §2 → §3 (~0.84 s).**

| t (ms) | Beat |
|---|---|
| 0 | Example panels, cable, tabs, labels fade (260 `settle`, drift 8 px right); the mink pops out (160). Runtime sinks to −420 and fades (520 `pose`); the Agent band sinks and fades (360 `settle`, from 60) |
| 120 / 180 | Preview, then Panels, lift 120 px more depth and fade (520 `pose`) |
| 120 | **The timeline leads:** assembly un-tips to `rotateX(0) rotateY(0) rotateZ(0) scale(1)` (720 `pose`); the timeline lands flat as the bottom strip at `scale(.84)`, keeping its hero box |
| 840 | Frame re-forms (360 `settle`); a changed fit glides clips (520 `pose`) |
| 1200 | §3 demo |

*Flick into §4:* straight to the edit pose; the tray never appears; lake clips are on `V2` on landing (260 fade). *Back up:* tray fades (260), `V2` fades (260), frame dissolves (360), the timeline tips back (720 `pose`), the others return from where they left, 60 ms apart; the examples show the last tab's end state with Replay.

**The grow §3 → §4 (~0.72 s, a dolly-in).**

| t (ms) | Beat |
|---|---|
| 0 | Readouts lift 8 px and fade; route pills, machine icons and the tray fade (260); the mink pops out (160) |
| 120 | Timeline `scale(.84) → scale(1)` and rises to centre-low (720 `pose`); no zoom change. `V2` recedes to .55 (520 `settle`) |
| 600 | History enters top-right with only its header (−8 px, 520 `enter`) |
| 840 | The mink pops back in on `V2` above First light (3-step hop, 210 ms) |
| 1100 | §4 demo |

*Flick:* endpoint state; History rows and chips without stamps. *Back up:* History fades (260), `V2` returns to 1 (360), the timeline shrinks to the strip (720 `pose`), the tray shows its end state.

**§4 → finale.** The stage scrolls away; nothing animates. The finale reveals with the Vision `[data-reveal]` values (opacity, 14 px, 560 ms `settle`, stagger 0/90/180/270 ms).

### 10.4 Micro-animations and beat sheets

| Moment | Behaviour | Timing | Avoid |
|---|---|---|---|
| Agent stamp | Departure Mono 11 px, orange; 120 ms after the thing it labels settles: scale 1.12→1, opacity 0→1, then a 1 px ring expands 6 px and fades | 260 `land`; ring 900 (`(.2,.7,.3,1)`) | Shimmer, glow, typing the tag, re-stamping on revisits |
| Lit layer | Label → orange (260 `settle`); dot fills from a ring (.4→1, 260 `land`); plane rim `0 0 0 1.5px` + 28 px glow at 35% (360 `settle`) | as given | Pulsing; more than one lit layer except "Runtime → all layers" |
| Conduits | Pillars draw layer to layer (`scaleY`), one hop after another; end dot lands; one 4 px packet travels **once** | 520 `pose`, 120 per hop; dot 380 `land`; packet 600 | Looping packets, marching dashes |
| Typed readout / log | Monospace 11 px / 16 px line, `steps(chars)` at 18 ms a character; the pixel check pops in 2 steps at line end; next line after 120; a 1ch orange caret blinks twice at the end, then goes | 18 ms/char | Spinners or bars implying compute; re-typing on scroll-back; measured numbers |
| Code panel | First 4 lines type at 12 ms a character; static "● live" dot | ≈ 600 ms | A pulsing live dot |
| Thinking | "Thinking" + a 3-square pixel ellipsis replacing the spinner (host CSS) | `steps(4)` 960 loop, for 600 | The round spinner |
| Spine bubble | `astrid-rise` (14 px, 500 ease); the previous turn recedes to .55 | 500; recede 360 | Layout shift |
| Tool-call chip | Lands when its edit **finishes**: slides 6 px down from under its reply; the 16 px wrench turns −30°→0 in 2 steps; `beat-sync` floods its fill left to right | 260 `enter`; flood 360 `settle` | Chips before the change |
| Clips settling | `left`/`width` glide; on arrival an overlay rectangle draws a 1.5 px orange outline that fades; moved clips lift 4 px with a shadow, then drop | 520 `pose`; flash 900; lift/drop 120 | Bounce, blur, several clips in one beat (stagger 120) |
| Stills develop | Opacity 0→1, scale .96→1, image sharpens from `blur(6px) saturate(.4)` | 520 `enter`; image 720 `settle`; 400 apart | Loading bars, skeletons |
| Reframe | Explicit width/height to 9:16; crossfade to the 9:16 file at the midpoint | 720 `pose`, 60 ms left to right; crossfade 260 | Stretching the 16:9 image |
| Card → clip | Play glyph pops (2 steps); video fades over the poster and plays once; a dashed drop line draws to the `V2` slot; the clip appears with a flash | glyph 2×70; fade 260; line 520; 600 apart | Flying clones; five videos at once |
| Beat markers | Three orange lines grow from `A1` to the top of `V1`, each topped by a dot | 360 `enter`, 90 apart; dot 260 `land` | Pulsing to the music |
| "You" cursor | Glides; press scale .9 for 80; drags on the same curve; release 120 `settle`; fades to .55 after 1.5 s idle | 720 long / 520 short | Jitter, wandering, teleporting |
| Level line, wedge, 0.6× dimension | Strokes draw (`stroke-dashoffset`); the wedge grows to 1.5 s | 520 `pose` | Labels before their stroke |
| History row | Appends at the bottom (four visible); icon (cursor, or 16 px mink head from `astrid-favicon.svg`) pops in 2 steps; text whole; new row tints orange 10% → 0; a fifth row shifts the list up | 260 `enter` from +6 px; tint 1200 linear; shift 360 | Typing, counters, two tinted rows |
| Example tabs | 3-segment control. Hover: fill ink 6% (dark: white 8%), icon up 1 px, 120 ease. Press: .97 for 80, release 160. One orange pill slides between segments; text colour swaps at its midpoint. A 2 px line fills under the selected tab while cycling; the first click stops it (fade 260). Focus: 2 px `#ed6b23`, offset 2 | pill 360 `pose` | Layout change on hover; progress lines under RM |
| Tab swap | Outgoing panel, cable and mink out (260, 8 px toward the old side); layer unlights; new tab starts at +260 | 260 | Two examples crossfading on top of each other |
| Replay | `↺ Replay`, bottom-right of the stage (under the spine on phones); fades in 800 after a demo ends, or at once on scroll-back; hover turns ↺ −180°; press fades the section to its base (260), replays after 360 | glyph 520 `pose` | Showing it during play |

**Page rhythm.**

| Section | Arrives with | First key beat | Demo | Scroll length (T6 tunes) |
|---|---|---|---|---|
| Hero | — | — | live | 100svh |
| §2 | 1.3 s pull-apart | stack 1.3 s; first stamp 3.5 s | 3 tabs × 6 s, one cycle, rests on New model | 220svh |
| §3 | 0.84 s fold | first still 2.5 s | ≈ 12 s | 180svh |
| §4 | 0.72 s grow | trim 2.7 s | ≈ 12.6 s | 180svh |
| Finale | the stage leaves | the sky at its peak | — | 120svh |

**§2 per tab** (tab k starts at k × 6000): +0 request rises · +150 layer lit · +300 "Thinking" (600) · +900 reply, example panel enters (520 `enter`, from 12 px right) and builds (≤ 800: 3D view — code types, canvas fades in 360, ±18° sway on 8 s; Beat-sync — card, waveform reveals 720 `pose`, 5 markers 90 apart; New model — log types) · +1400 mink cue · +1750 conduits light · +2300 stamp · +2600–6000 still.

**§3** (s): 0.0 carried LTX pair at .55 · 0.3 "Make five stills…", machine icon and `Local · Flux · ComfyUI` enter (260), mink pops in · 0.7 "Your machine" readout, stamp at +260 · 1.0–2.6 lines type · 1.3–2.9 five stills develop, 400 apart · 3.8 "Make them vertical." · 4.2 Thinking · 4.8–5.9 reframe; "reframed to 9:16" types · 5.9 "Reframed to 9:16." · 6.8 "Animate them in the cloud with Wan.", cloud icon, `Cloud · Wan · Wan2GP`, a dashed Local→Cloud line (520) · 7.2 Cloud readout · 7.8 `V2` fades in (260) · 8.0 + 0.6k card k plays once and drops · 10.1 the mink rides down · 11.2 "Five stills, reframed and set in motion." · 12.0 end; Replay at 12.8.

**§4** (s): 0.4 request · 0.9 cursor enters from the right (720 `pose`) · 1.6 press, drag First light's handle, release; "!" · 2.2 History "You · trimmed First light" · 2.4 Thinking · 3.0 reply · 3.1 Passing shapes then A quiet finish (+120) lift, slide, drop; the mink carries · 3.9 History + `arrange · 3 clips` · 4.6 "Cut every clip on the downbeat."; markers rise · 5.2 Thinking · 5.8 "Done. Every cut lands on a beat." · 5.9–7.3 three snips and snaps · 7.4 History + `beat-sync · 3 downbeats` with its flood · 7.9 cursor drags the music level to 0.6 · 8.6 History · 9.2 "Slow the middle scene…" · 9.8 Thinking · 10.4 "Slowed to 0.6× with a 1.5s crossfade."; stretch, dimension line, wedge; the mink pushes · 11.2 History + `retime · crossfade` · 11.6 cursor extends A quiet finish · 12.2 History (the list shifts) · 12.6 end; Replay at 13.4; cursor dims at 14.1.

**Breathe:** 200 ms after each pose settles; ≥ 2.7 s of stillness after each §2 example; 0.9 s between the last still and "Make them vertical"; 0.8 s at every demo's end before Replay; no demo in the finale.

### 10.5 Phones and reduced motion

**Phones (390 px).** The handoff: the stacked hero's stage pins at the top and scales into 45svh (`transform: scale`, top-centre, 720 `pose`); the text below never jumps. §2: orthographic slabs (part 3.6) with the same 720 `pose`, 60 ms stagger and Agent clip-fold as desktop, settled ≈ 1.3 s; labels left of the slabs (Departure Mono 11 px); conduits as 2D lines; the selected example as one compact card in the bottom 40%; tabs ("3D view", "Beat-sync", "New model") in the text below. §3: five cards 62 px wide (16:9 at 35 px, reframed to 110 px) above the strip at .84; readouts move into the flow text under the spine (title, stamp, first line typed, the rest whole, 120 apart). §4: the timeline only (`V2` at .55) with the 56 px gutter; History as a one-line ticker at the stage top (crossfade 260); the latest two turns below, chips under them. The mink on phones: only §3's ride, §4 and the finale, at 2 device px.

**Reduced motion.**

| Item | Behaviour |
|---|---|
| Leaving the hero | Callouts disappear (today); no tilt |
| Pose changes | Geometry switches in one frame inside a 200 ms opacity dip (to .2 over 100, back over 100, `settle`). The stack keeps its static 3D |
| Demos | Never auto-play; endpoints at once (stamps, complete readouts, History full, chips, eyebrow already typed) |
| Tabs | Manual only; no progress line; 150 ms opacity crossfade |
| Mink | One static frame per section: §2 `sit` by the LTX block; §3 `sit` on lake-05; §4 `sit` on `V2` by the crossfade; finale `lookup` f1. No glyphs |
| Sky | One step per section boundary |
| Replay | Replaced by **"Show the steps"**: the beat sheet's endpoints as a slideshow, 1.6 s each, 200 ms opacity crossfades, no transforms, pausable ("Pause"), only on request |

### 10.6 The mink

**Rules.** Density matches the run cycle (81×44, 11 frames) and the juggler (47×77). One art pixel = a whole number of device pixels: desktop 3 at DPR ≥ 2, 2 at DPR 1; phone 2; finale 2 everywhere ("small mink, big sky"). Palette exactly `#FF7A2E`, `#D9531E`, `#F7E6CF`, `#151311`; props from the tinkerer's set (`#A5B2B2`, `#7E989F`, `#3C5F66`, `#F3D27D`, `#B46D30`); 1 art px outline in `#151311`; no partial alpha. Sprites advance on 70 ms (slow loops 140). Moves are attached to a gliding UI object (same curve and duration) or a hop (3 steps at 70 ms, rising 4 then 6 art px). Pop in = the existing `astrid-mink-hop` (1 art px, 260 ms `steps(2)`); pop out drops 1 art px over 2 steps (160 ms). She appears and disappears between spots; she never runs across 3D layers.

**Cue sheet.**

| Where | Beat | Pose | What she does | Glyph |
|---|---|---|---|---|
| Hero | — | — | Nothing new | — |
| §2 · 3D view | tab +1400 | `sit` f0, clipped by the panel's top edge | Peeks over the 3D panel; blinks at +3600 | — |
| §2 · Beat-sync | +1400 | `plug` | At the Agent band's right end with the cable's plug; 5-frame push-in (350) as the cable reaches the socket; holds | — |
| §2 · New model | +1400 | `push` | Pushes the LTX-Video block into its Runtime slot along its path (720 `pose`); hops on arrival | **sparkle** (the page's only one) |
| §3 | 0.3 s | `sit` + 1 art px bob (2 × 140) | Beside the Local machine icon, "typing" while the readout types | thought dots on "Thinking" |
| §3 | 10.1 s | `sit` → hop | Onto lake-05's card, down its drop line in a 3-step hop, onto the new `lake-05` clip (where §4 finds her) | — |
| §4 | 1.6 s | `sit` | Notices the cursor trimming | **"!"** (the page's only one) |
| §4 · arrange | 3.1 s | `carry` (6 f, 420 loop) | Rides Passing shapes as it slides, matched to its glide | thought dots before |
| §4 · beat | 5.9 s | `run` → `snip` (4 f, 280) ×3 | Scampers to each cut and snips as the edge snaps, 500 apart | thought dots before |
| §4 · retime | 10.4 s | `push` (4 f, 560 loop) | Pushes the stretching clip until it lands | thought dots before |
| §4 end | 12.6 s | `sit` | Sits on `V2` near the crossfade; blinks | — |
| Finale | always | `lookup` f0 → f1 | Small at the horizon, ~72% across; at sky progress ≥ .98 lifts her head (2 frames, 140) and blinks 1.2 s later; below .9 swaps back without animation | — |

**Holding back.** One mink at a time, never during a pose change (out at its start, back after settle). She never covers a clip label, stamp, chip, the cursor or History. She watches while the cursor edits. She reacts to beats, never to scroll; on fast-forward she is placed at the section's end spot. Idle is a blink every 3.6/4.4/4.0/4.8 s (seeded). Thought dots only while "Thinking" shows. Motion and snip lines are baked into frames.

**Strips (placeholders now, A5a; finals deferred, part 6.2).**

| Strip | Frame (art px) | Frames | Playback | Placeholder now |
|---|---|---|---|---|
| `run` | 81×44 | 11 | 70 loop | **Final:** the MinkRunner strip |
| `sit` | 40×56 | 2 | blink 140 | `astrid-mink-front.png` ÷4 nearest-neighbour to its 32×32 grid |
| `carry` | 80×56 | 6 | 70 loop | `run` at 70 |
| `push` | 81×44 | 4 | 140 loop | `run` frames 6–9 at 140 |
| `snip` | 56×56 | 4 | 70 one-shot | `sit` + the `astrid-north-star-adapt-snap` glyph |
| `plug` | 48×64 | 5 | 70 one-shot, hold f4 | juggler frame 1 + an SVG plug |
| `lookup` | 48×80 | 3 | on cue | juggler frames 1 and 2 |
| `!` | 5×12 | 3 | 3 × 70, hold 490 | Departure Mono "!" 11 px `#FF7A2E` |
| sparkle | 7×7 / 5×5 | 3 | 100 each, once | **Final:** `astrid-north-star-knowledge-spark0/1/2` |
| thought dots | 3, 4, 6 px | 3 | 140 apart | **Final:** `astrid-north-star-adapt-thought0/1/2` |

### 10.7 Cut list (R2 confirms each is absent)
1. The orange page rail and the dots on bubbles. 2. The brand repeated at the top of each section. 3. Connectors from spine bubbles to the stage. 4. Mechanical repetition: an ambient cycle that replays the same beat identically (vary it from a pool). 5. Looping conduit packets. 6. A mink that fidgets constantly; between jobs she rests or watches. 7. A full 3D orbit (sway ±18°). 8. Several lake videos playing at once (in the ambient cycle they play one at a time, in turn). 9. The big 3D LTX box beside the stack (mockup 02c). 10. Pointer tilt and callouts below the hero. 11. Horizon lights. 12. More than one sparkle or one "!". 13. GPU specs, VRAM, timings and usage counts ("2.4k uses") anywhere.

## 11. What changed from v2, and how conflicts were resolved

- **Plates → live panels** (Opus review): S2 re-scoped; A6, T7 and the plate handoff cut; T18 becomes a pose change.
- **Cut or merged:** S3 → T9, T1's tests and T6; S5 → T13; T4 → T3 (one scroll reader); T16 (visitor GPU detection) cut; T1e and receipts cut (placeholders); A7 horizon cut; A2–A4 merged into A2; sr-only transcripts cut (the spines are the transcripts); T9 and T26 drop to NORMAL; T10 restored as a NORMAL computed overlay layer plus `PixelSprite`.
- **Added:** T0 (Opus sheet), H0 (capture harness), T28 (motion primitives), M1 (mink direction), A5a (mink placeholder kit), A9 (pixel icons). T22 rises to TASTE-HIGH; T15 owns the 3D view's look; T18 owns all §3 motion; T8 owns the phone stack.
- **Resolved between the review and the craft pass:**
  - *Mink strips:* the review wanted existing art until cues are approved; the craft pass specified seven new strips. Resolved by the user's placeholder decision: A5a (placeholders from existing art) is in scope; A5b–A5h and M1's second pass are deferred real assets.
  - *Two passes vs. no mid-plan gates:* TASTE-HIGH pass 2 runs once the moment is on the preview and folds in any user notes, but never waits for the user, so no gate appears mid-plan.
  - *H0 dependency:* the craft pass hung H0 on P1; H0 runs against Playwright's own dev server, so it doesn't wait for the preview.
  - *Readout label:* v2's "Recorded example" becomes "Example" (both reviews), with no specs or timings.
  - *Tab cycling:* v2's 5 s endless cycle becomes one 6 s cycle resting on New model (craft).
  - *§4 opening copy:* the craft pass's "I'll shorten the opening. Close the gap behind me." replaces v2's proposal; T0 confirms.
  - *Phone stage height:* both sources agree on ~45svh with pin-and-scale; the craft pass's trigger lines (78/83%) are adopted.
  - *Sky steps:* the review's "quantise" is the craft pass's 1/48.

## 12. Questions for the user

Only at R4: (a) may the placeholder media ship, or should the real assets (part 6.2) be made first? (b) may `feat/home-journey` merge to `main`? Nothing else needs the user before then.
