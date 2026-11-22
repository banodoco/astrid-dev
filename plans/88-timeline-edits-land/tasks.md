# Tasks — Timeline edits land and hold

[Plan](plan.md) · [Inputs](inputs.md)

These are proposed task cards, not dispatch authority. Every source path and symbol must be re-checked against the code at dispatch.

**Task ids:** `TE-n`. **Critical path:** TE-1 → TE-3 → TE-4 → TE-5.

**The rule for every task:** an edit is done when a fresh read-back shows exactly the intended change and nothing else, and a render from Plan 87's stack shows it.

**Test inventory:** `tests/timeline/test_occurrence_media_swap.py` (439 lines, from the donor commit), `tests/timeline/test_legacy_occurrence_timing_provenance.py`, the commit-boundary tests, and the sandbox repro scripts in [Plan 87's evidence](../87-render-works/evidence/edits/).

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| TE-1 Media on an existing shot-owned footage clip can be replaced with newly imported media; every other authored field, including a word anchor, is unchanged; SDK `swap_asset`, CLI `--swap-asset` and the document publisher share the route | X | Plan 87 RN-1 | Cherry-pick `24740fdf`: `astrid/sdk/timeline/media_swap.py`, `native_occurrence_media_commands.py`, `commit_session.py`, `timeline_media_replacement.py`, `astrid/packs/timeline/cli_native.py`, `timeline_document.py` | Donor tests, plus one real swap on the stack: a word-anchored footage clip, new media, read-back differs only in media. Closes [#1404](https://github.com/banodoco/astrid-dev/issues/1404), part of [#1405](https://github.com/banodoco/astrid-dev/issues/1405) | [ ] |
| TE-2 A clip whose legacy overrun is unchanged survives a pure start shift | N | TE-1 | Cherry-pick `ad10ff6d`: `_commit_timing_validation.py`, `validation.py` | Donor tests plus grown-bound, shrunk-bound and changed-source-window cases; one independent review | [ ] |
| TE-3 A timing-only edit to a word-anchored shot clip is accepted only when the clip's offset from its resolved word is unchanged within one frame; otherwise it is refused and the refusal names the supported form. Replaces `d4bf28e4` | S | TE-2 | `_commit_timing_validation.py`: `_BasisReader.signature`, `_signed_failures`, `_legacy_exemptions`; reads `reflow.py` and `_timing_evaluators.py` for the resolver | A test with a resolvable word: move the narration and the clip together (accepted), move the clip alone (refused), then a reflow moves nothing. Part of [#1403](https://github.com/banodoco/astrid-dev/issues/1403) | [ ] |
| TE-4 The edit loop on the heavy fixture (the standard variant Plan 87 renders): for each edit below, make it, read it back, render it, record the result | X | TE-1 to TE-3 | Fixes only where the cause is in TE-1 to TE-3's code; everything else is evidence on the owning issue | The loop log: one row per edit with command, outcome, read-back diff, render frame, and issue number if blocked | [ ] |
| TE-5 The film's workarounds are converted back: eleven overlay clips become in-place swaps, and the pause after "two million" loses 15 frames with everything after it moved | X | TE-4 | The film project only, from the undo list in [overlay evidence](../87-render-works/evidence/overlay/FRICTION.md) and the plan in [tighten evidence](../87-render-works/evidence/tighten/FRICTION.md) | Read-back: overlays gone, originals carry the new media; every clip after the cut is exactly 15 frames earlier; a dry-run reflow moves nothing; the film renders whole | [ ] |
| R One review round before the branch is offered to the Release 15 Lead | S | all | Read-only | Findings become rows `R.n` | [ ] |

## The edits in the loop (TE-4)

Each failed, or needed a workaround, on 22 November. In order:

1. Replace the media of a word-anchored footage clip with a newly imported still, and with a newly imported video.
2. Re-point a clip to an asset already in the registry (this worked; it is the control).
3. Change parameters on a project-pack element clip, and switch a clip to a newly admitted project element.
4. Move one clip without moving any other.
5. Remove a pause: move every clip after a cut by a fixed number of frames, with the narration.
6. Change about 250 clips in one commit, and find the size at which a commit is refused.
7. Remove a clip, then restore it exactly.
8. Add clips, then undo all of them in one change.
9. Run two edit sessions on different clips at once.

Edits 4, 6 and 9 are expected to meet Plan 77's and Plan 76's defects; edits 7 and 8 to meet [#1430](https://github.com/banodoco/astrid-dev/issues/1430). Record and continue.
