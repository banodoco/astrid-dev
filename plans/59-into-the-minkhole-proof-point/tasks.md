# Tasks — Into the Minkhole proof point

[Plan](plan.md) · [Inputs](inputs.md)

**Loop:** Take the next creative task; attempt it with Astrid's own tools; when blocked, find the cause, decide the properly engineered fix that prevents this and similar problems, land it, or file an astrid-dev issue if useful but too large for now; return to the creative task; record what was learned for the skill. No workarounds.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| C1 See the rough cut in Astrid (import, a clean frame, a short render). | X | — | Astrid import, visualize and render tools | Release 14 Agent `release/14/plan-59` at `509b09f94` imports the rough cut and reference; a single clean composed frame and one-second render are proven below. | [x] |
| C2 Fill the frame: the Matrix shots with no black bars. | X | C1 | Clip appearance contract, composition package, editor preview, export, composed visualize | Owner-approved shape (16 November): one composition-owned placement function called by export renderer, editor preview and editing handles, with their copies deleted; per-clip fit falls back to its track; old projects explicitly receive the existing implicit fit choice once on open. Exact 0.0.17 source is recovered and 0.0.18 builds from its owning repository (D3). The C2 candidate has one composition-owned placement function, independently reviewed; five must-fix findings are being fixed before the owner sees before/after Matrix frames. Show the owner a clean Matrix frame with no top/bottom bars. | [ ] |
| C3 Know what is said: the words and timings of each speaking clip, and the target lines from the machine-voice reference. | X | C1 | Astrid timeline and transcription tools | One line; refine from what C1/C2 teach us. |
| C4 First new line: one Morpheus shot says its new line, on a real GPU, trying the voice approaches (continuation from a voiced clip, a video reference, audio/video inpaint) and choosing with the owner. | X | C3 | Astrid H3 and generation tools | One line; keep within the authorized budget split. |
| C5 The remaining dialogue shots, one at a time. | X | C4 | Astrid H3 and timeline tools | One line; refine as each shot teaches us. |
| C6 Visual changes, one at a time. | X | C5 | Astrid visual editing tools | One line; refine as each change teaches us. |
| C7 Final render and owner review. | X | C5, C6 | Astrid render and review flow | One line; show the completed result to the owner. |
| C8 Write the skill and runbook from the log, then a fresh weaker agent repeats it on a different timeline. | X | C7 | Astrid skill and runbook | One line; retain the fresh agent's actions and outcome. |

## Blocker log

| Blocker | Creative task | Cause | Decision | Where it landed | Proof |
| --- | --- | --- | --- | --- | --- |
| Release 14 refuses the rough-cut archive. | C1 | `astrid/core/timeline/authoring_bundle.py:1140-1164` treated archive history as competing selected media because the import carried no trusted media baseline; descriptor ownership and legacy internal assets also needed normalization. | Fixed at cause in Agent #346 commits (`a17104dc9`, `d039f4ce9`, `07da9e768`, `49e50b9be`) and import follow-up `4baabb4b3`; integrated into Agent `release/14/plan-59` at `509b09f94`. | Agent `release/14/plan-59` | Import prep: 26 passed; archive guard tests passed. `astrid timelines import` imported both archives on fresh isolated Runtime (rough cut 68 media objects, reference 3). See import-fix report. |
| Composed capture rejected source-worker readiness context. | C1 | Launch projected CLI pack roots/dependency path while execution used host-resolved pack roots and Runtime dependency root; validated consumer context therefore differed. | Fixed in Agent `p59/see-the-timeline` commit `d88a22ae`, merged to `release/14/plan-59`; mismatch diagnostic names fields without values and guards remain. | Agent `release/14/plan-59` | Focused startup/context checks: 5 passed, 38 deselected. Composed visualize captured a clean raw frame at 6.5s, 1280x720. See see-it-2 report. |
| Inputs-mode visualize reported success without exporting declared artifacts. | C1 | Output path handling did not materialize managed PNG/Markdown artifacts, and command suggestions dropped the invoked launcher. | Fixed in `a340ec7e` on `p59/see-the-timeline`, merged to `release/14/plan-59`. | Agent `release/14/plan-59` | Astrid CLI exit 0; both reported files exist, and output says inputs mode produced no picture. Focused test: 5 passed; expanded selection: 9 passed. See see-it report. |
| Visualize did not provide a clearly identified single clean composed frame. | C1 | `--at` selected a frame but the default PNG was a decorated review page; clean frame export was not identified by the CLI. | Fixed in `eb0fc0c0` on `p59/see-the-timeline`, merged to `release/14/plan-59`; recipe documented in `astrid/packs/rendering/docs/references/render-inspect-transfer.md`. | Agent `release/14/plan-59` | CLI produced `frames/frame-000000156.png` at 6.5s, 1280x720, explicitly labelled clean composed frame. `test_visualize_export.py`: 7 passed. See see-it-2 report. |
| Rough-cut render rejected legacy internal asset `height`. | C1 | Internal child assets retained numeric `width`/`height`, while the closed render registry schema correctly disallows those keys; stored data had to be normalized at trusted boundaries. | Fixed in Agent `asset_dimensions.py`, commits `7e407e84` and `d01155ec`; canonicalize detached import, migration and renderer projections, preserving stored source and strict validator. | Agent `release/14/plan-59` | Focused checks: 36 passed plus 6 subtests; unchanged schema contract passed. Fresh import had zero numeric dimensions in 788 registry entries. Astrid rendered one second; ffprobe: H.264 1280x720, 24 fps, AAC, duration 1.000000s. See render-dimensions report. |
| Asset records can admit and store open data that the renderer rejects later. | C1 | Import/save accept asset records in an open form, then render enforces a closed list; malformed or unsupported fields can be persisted and discovered late (the original `width`/`height` case). | Open decision: enforce one asset contract at admission while retaining provenance and validation guards. | Pending owner/contract decision | Render-time canonicalization made this archive render, but does not establish one admission contract. See render-dimensions report and `tests/test_schema_contract.py:135`; no schema assertion or guard was weakened. |
| Preview and export disagree; fit is track-only; clip crop is not editable. | C2 | Appearance has separate rendering paths and no independent clip crop/fit authoring. | Owner approved one placement function owned by the composition package, called by export, preview and editing handles with their copies removed; per-clip fit with track fallback; write the old implicit fit choice once when opening an old project. Package source is recovered and build ownership resolved. The independently reviewed candidate has five must-fix findings in progress; owner sample follows those fixes. | `banodoco/timeline-composition` `release/14/plan-59` at `2c0740a` contains recovered source merged with staging as 0.0.18; composition source report. | Placement oracle compared against 0.0.17; package `npm test`: 91 passed; two packs have identical SHA-256; package smoke passed. No Matrix Fill parity/owner sample yet. |
| `astrid hivemind search` failed from a source install. | C1 | Pack-relative script paths were resolved against the working directory instead of selected pack root; network broker rejected CONNECT to a declared `https://host` destination. | Both causes fixed on Agent task branch `p59/hivemind-source-cli`, pushed and under independent review; `astrid hivemind item` was added for one message or resource. File the remaining search limitation: six noisy rows, no thread view. | `p59/hivemind-source-cli` | Source CLI and network reports; review pending. |

## Issues to file

Filed in `banodoco/astrid-dev`:

- #757 — Seven tests fail on untouched Release 14; covers former drafts 1–4.
- #758 — Source bring-up prerequisites and status/collision guidance.
- #759 — Runtime identity mismatch and stale pack-host registration.
- #760 — Browser download TLS cause hidden by renderer lease error.
- #761 — `timelines visualize` has an unwieldy flat flag surface.

Still held:

- H3 docs and alternate CLI: Plan 60 is now the owning plan and removes the alternate command.
- Composition licence: needs the owner's licensing decision.
- Renderer consolidation: App consolidation is larger than the current crop/placement fix.
- Intermittent black preview: needs a measured, repeatable reproduction before filing.

## Parallel track

The H3 manager's shot inventory is complete (9 shots, 19 cuts); the Morpheus source is 81.05–84.30s. Automatic source conform now exists on task branch `p59/h3-conform`; integration remains in Plan 60 RH-1. Rental is held until the creation-time lifetime bound is independently reviewed. Spend is $0 of the $3 pilot. Plan 60, “Refining H3_AV,” is the H3 record.
