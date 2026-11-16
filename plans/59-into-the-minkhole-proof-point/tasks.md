# Tasks — Into the Minkhole proof point

[Plan](plan.md) · [Inputs](inputs.md)

**Loop:** Take the next creative task; attempt it with Astrid's own tools; when blocked, find the cause, decide the properly engineered fix that prevents this and similar problems, land it, or file an astrid-dev issue if useful but too large for now; return to the creative task; record what was learned for the skill. No workarounds.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| C1 See the rough cut in Astrid (import, a clean frame, a short render). | X | — | Astrid import, visualize and render tools | Use the release build and Astrid CLI; record commands, source revisions, archive identities, errors, blocker decisions and proof below. Existing useful evidence: composed visualize failed with `worker Remotion readiness context is unavailable: runtime validation consumer context differs`; render refused asset key `height`; inputs-mode visualize returned success but exported nothing. Source bring-up requires pinned Node 20.19.4 and a source manifest that is not discoverable from the tool. Focused existing proofs: Agent `tests/packs/rendering/test_timeline_transfer_actions.py`, `tests/packs/rendering/test_managed_timeline_render.py`, `tests/packs/rendering/test_timeline_visualize_parity.py`; Runtime `tests/test_timeline_import.py`. | [ ] |
| C2 Fill the frame: the Matrix shots with no black bars. | X | C1 | Clip appearance contract, composition package, editor preview, export, composed visualize | Preview and export are separate renderers that disagree; fit exists only per track; crop is not editable on a clip. Candidate: composition package as the single source of truth for preview, export and composed visualize; size this now. Show the owner a clean Matrix frame with no top/bottom bars. | [ ] |
| C3 Know what is said: the words and timings of each speaking clip, and the target lines from the machine-voice reference. | X | C1 | Astrid timeline and transcription tools | One line; refine from what C1/C2 teach us. |
| C4 First new line: one Morpheus shot says its new line, on a real GPU, trying the voice approaches (continuation from a voiced clip, a video reference, audio/video inpaint) and choosing with the owner. | X | C3 | Astrid H3 and generation tools | One line; keep within the authorized budget split. |
| C5 The remaining dialogue shots, one at a time. | X | C4 | Astrid H3 and timeline tools | One line; refine as each shot teaches us. |
| C6 Visual changes, one at a time. | X | C5 | Astrid visual editing tools | One line; refine as each change teaches us. |
| C7 Final render and owner review. | X | C5, C6 | Astrid render and review flow | One line; show the completed result to the owner. |
| C8 Write the skill and runbook from the log, then a fresh weaker agent repeats it on a different timeline. | X | C7 | Astrid skill and runbook | One line; retain the fresh agent's actions and outcome. |

## Blocker log

| Blocker | Creative task | Cause | Decision | Where it landed | Proof |
| --- | --- | --- | --- | --- | --- |
| Release 14 refuses the rough-cut archive. | C1 | Release 14 import path rejects the supplied archive. | Fix now; existing fix is astrid-agent #346, closed unmerged on a Release 15 branch, being brought into `release/14/plan-59`. | Agent `release/14/plan-59` | Pending re-import through the release build. |
| Composed visualize fails with `worker Remotion readiness context is unavailable: runtime validation consumer context differs: this process's environment was not validated at launch (only the host and Remotion-capable capability workers are)`. | C1 | Readiness validation consumer context differs in the worker. | Fix at cause if required for a clean frame; otherwise file if too large. | Pending | Reproduce and capture a single clean frame. |
| Render refuses an asset key: `Asset registry.assets['occ-623427781ad940139658c54ff416184f-blue-pill-occurrence-2-20260928:old-man-neo-reaction-first'] has unknown key 'height'`. | C1 | Asset admission rejects the `height` field. | Find the schema/admission cause; preserve guards. | Pending | Short render through Astrid. |
| Inputs-mode visualize reports success and exports nothing. | C1 | The command's output path/result handling produces no files. | Fix at cause or file if broader than this task. | Pending | One command leaves a clean frame at the requested output and reports it. |
| Source bring-up requires pinned Node 20.19.4 and a source manifest users are not told about. | C1 | Bring-up prerequisites are undiscoverable. | Make the Astrid path understandable or file the broader setup issue. | Pending | Release build starts from documented prerequisites. |
| Preview and export disagree; fit is track-only; clip crop is not editable. | C2 | Appearance has separate rendering paths and no independent clip crop/fit authoring. | Fix through the composition package as shared source of truth; sizing underway. | Pending | Same authored Matrix frame in editor, export and composed visualize; clip Fit/Fill and crop independently editable. |

## Issues to file

- Broader `timelines visualize` command-surface redesign if the immediate C1 single-frame path is fixed but the CLI remains hard to understand.
- Full App renderer consolidation if composition-package single-source sizing shows it is useful but too large for this work loop.
- H3 documentation and alternate CLI drift beyond what blocks the creative work; make the documented route honest and keep stage links live.
- Intermittent black preview if measurement confirms a recurring defect after the correct media is ready.
- Any durable Astrid friction discovered in later creative tasks that is useful but too large to fix here; search for duplicates before filing. Existing issues #748, #745 and #736 were identified earlier; check their state and do not duplicate them.
