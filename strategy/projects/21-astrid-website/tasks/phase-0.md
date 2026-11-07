# Astrid Homepage Journey — Phase 0 (parallel, after Step 0) Tasks

← [Task index](../tasks.md#task-index) · [Phase 1](phase-1.md)

##### Task T0

| Field | Accepted value |
|---|---|
| Tier | TASTE-HIGH |
| Goal · files | The Opus sheet: all copy (requests, replies, History lines, readout and install-log lines, Runtime labels, Replay and reduced-motion labels), section beats and timings, each section's ambient cycle at rest (contents, variation pool and cadence; [design.md](../design.md#101-principles), principle 8), and `J/journeyMotion.ts` tokens plus matching CSS custom properties, seeded from [design.md](../design.md#10-craft-details-t0s-starting-values-from-the-opus-craft-pass) (may tune any value ±20%) |
| Deps | — |
| Done when | Each token names its hero source line; a grep of `J/` finds no `ms` or `cubic-bezier` literal outside the tokens; §4's opening doesn't repeat the hero; the notes lineage file is seeded |

##### Task P1

| Field | Accepted value |
|---|---|
| Tier | NORMAL (+ coordinator) |
| Goal · files | **The Artifact preview, from today's hero**: a preview HTML entry calling `renderPublicEntry()`, a preview Vite config (`base: './'`, that HTML as `rollupOptions.input`, no service worker or manifest), root-absolute assets moved to `BASE_URL`/imports ([inputs.md](../inputs.md#starting-code-facts) list), the `useEditorSettings` storage write wrapped in try/catch, and `scripts/preview/build-artifact.sh` emitting `dist-preview/`. The coordinator publishes the emitted files plus referenced media (not `public/`) as a multi-file Artifact (two publishes if over 255 files) |
| Deps | — |
| Done when | Today's hero renders from the Artifact on desktop and the user's phone: both audiences, both palettes, editor, mink, fonts, sky; zero failed requests in the network log; file count and bytes recorded; one script rebuilds and the coordinator republishes to the same URL. If entry or CSP fails: the LAN `vite preview --host` fallback becomes the preview |

##### Task H0

| Field | Accepted value |
|---|---|
| Tier | NORMAL (run by a Claude session) |
| Goal · files | Capture harness: `scripts/capture/journey-capture.ts` + `playwright.capture.config.ts` (outside the default E2E match), `page.clock`, scroll profiles, all [tasks.md](../tasks.md#h0-capture-ids) ids at D and P, each also `-rm`; ids are added as their sections land (v0: `pull-app`, `pull-agent`, `pull-interrupt` for S2) |
| Deps | — |
| Done when | All existing ids record from one command; reruns give identical stills (seeded blinks) |

##### Task S1

| Field | Accepted value |
|---|---|
| Tier | XHARD |
| Goal · files | Snapshot publish and replay spike · `J/publication-spike.*`, provider test, E2E fixture |
| Deps | — |
| Done when | All versions adopted in order; same editor instance; zero history entries, zero `saveTimeline` calls, zero writes to `astrid.timeline-drafts`; a stale publish can't win |

##### Task S2

| Field | Accepted value |
|---|---|
| Tier | XHARD (+ Opus partner) |
| Goal · files | The live stack pose: `extend` pose on `.astrid-editor-surfaces` with per-surface depths, chat clip-path band, launcher growth (App), fold-down (Agent), sibling labels and pillars, a Runtime child, phone orthographic slabs, reduced-motion static stack plus dip. Values from [design.md](../design.md#103-transitions-beat-tables); the T8 Opus agent judges the captures in the same spike |
| Deps | H0 v0 |
| Done when | `pull-agent-D-480` shows no plane cutting another; `pull-interrupt-D` has no jump or blank frame; a WebKit run of `pull-app-D` matches Chromium; `pull-app-P-1320` shows the flat slabs; transforms and opacity only (no layout in the performance trace) |

##### Task S4

| Field | Accepted value |
|---|---|
| Tier | XHARD |
| Goal · files | Scroll-driven sky with ownership: the fast path, 1/48 quantisation, stable canvas height, held palette, claim/release |
| Deps | — |
| Done when | Scrub through dusk, midnight and twilight, open Vision, return: no React commit per scroll frame, no stale inline palette, same window restored; raster ms per paint reported at D (4× CPU throttle) and on an iPhone (LAN preview); RM stepping works |

##### Task A1

| Field | Accepted value |
|---|---|
| Tier | ASSET |
| Goal · files | Placeholder music + beat list |
| Deps | — |
| Done when | Digest, duration and beats verified; waveform legible at P |

##### Task A2

| Field | Accepted value |
|---|---|
| Tier | ASSET |
| Goal · files | Placeholder lake media |
| Deps | — |
| Done when | Five stills, crops, silent clips, posters, thumbnails at spec; contact sheet looks plausible at D and P |

##### Task A5a

| Field | Accepted value |
|---|---|
| Tier | ASSET |
| Goal · files | Mink placeholder kit ([inputs.md](../inputs.md#6-assets), [design.md](../design.md#106-the-mink)) |
| Deps | — |
| Done when | Every cue in [design.md](../design.md#106-the-mink) has a mapped placeholder that renders in H0 at D and P |

##### Task A9

| Field | Accepted value |
|---|---|
| Tier | ASSET |
| Goal · files | Pixel icons |
| Deps | — |
| Done when | Crisp at D and P in both palettes |

[Phase 1 →](phase-1.md) · [Back to task index](../tasks.md#task-index)
