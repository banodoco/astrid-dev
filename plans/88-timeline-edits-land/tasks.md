# Tasks — Timeline edits land and hold

[Plan](plan.md) · [Inputs](inputs.md)

These are proposed task cards, not dispatch authority. Every source path and symbol must be re-checked against the code at dispatch.

**Task ids:** `TE-n`. **Critical path:** TE-1 → TE-3 → TE-4 → TE-5.

**The rule for every task:** an edit is done when a fresh read-back shows exactly the intended change and nothing else, and a render from Plan 87's stack shows it.

**Test inventory:** `tests/timeline/test_occurrence_media_swap.py` (439 lines, from the donor commit), `tests/timeline/test_legacy_occurrence_timing_provenance.py`, the commit-boundary tests, and the sandbox repro scripts in [Plan 87's evidence](../87-render-works/evidence/edits/).

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| TE-1 Media on an existing shot-owned footage clip can be replaced with newly imported media (cherry-picked here; Plan 87's branch does not carry it); every other authored field, including a word anchor, is unchanged; SDK `swap_asset`, CLI `--swap-asset` and the document publisher share the route | X | Plan 87 RN-6 | Cherry-pick `24740fdf`: `astrid/sdk/timeline/media_swap.py`, `native_occurrence_media_commands.py`, `commit_session.py`, `timeline_media_replacement.py`, `astrid/packs/timeline/cli_native.py`, `timeline_document.py` | Donor tests, plus one real swap on the stack: a word-anchored footage clip, new media, read-back differs only in media. Closes [#1404](https://github.com/banodoco/astrid-dev/issues/1404), part of [#1405](https://github.com/banodoco/astrid-dev/issues/1405) | [ ] |
| TE-2 A clip whose legacy overrun is unchanged survives a pure start shift | N | TE-1 | Cherry-pick `ad10ff6d`: `_commit_timing_validation.py`, `validation.py` | Donor tests plus grown-bound, shrunk-bound and changed-source-window cases; one independent review | [ ] |
| TE-3 A timing-only edit to a word-anchored shot clip is accepted only when all of these hold: the clip had a valid resolved anchor before the edit; the word it resolves to is the same one after it, identified by transcript, source and word identity, and is unique (no nearest-match guess); the clip's offset from that word is unchanged within one frame at both its start and its end; its duration and source mapping are unchanged. Otherwise the edit is refused and the refusal names the supported cut-relative form. Replaces `d4bf28e4` | S | TE-2 | `_commit_timing_validation.py`: `_BasisReader.signature`, `_signed_failures`, `_legacy_exemptions` (the validator has no authenticated word binding today, about line 106); `reflow.py` (its nearest-word choice, about line 588, must not be what decides acceptance); `_timing_evaluators.py`. If a unique word identity cannot be established at commit time, TE-3 is delivered as the refusal alone and the ripple edit moves to [Plan 18](../18-timeline-editing/plan.md); say so within two days of starting | A test with a resolvable word: narration and clip moved together (accepted); clip moved alone (refused); an ambiguous word (refused); then a reflow moves nothing. Part of [#1403](https://github.com/banodoco/astrid-dev/issues/1403) | [ ] |
| TE-4 The edit loop on the heavy fixture (the standard variant Plan 87 renders): for each edit below, make it, read it back, render it, record the result | X | TE-1 to TE-3 | Fixes only where the cause is in TE-1 to TE-3's code; everything else is evidence on the owning issue | The loop log: one row per edit with command, outcome, read-back diff, render frame, and issue number if blocked | [ ] |
| TE-5 The film's workarounds are converted back: eleven overlay clips become in-place swaps, and the pause after "two million" loses 15 frames with everything after it moved | X | TE-4 | The film project only, from the undo list in [overlay evidence](../87-render-works/evidence/overlay/FRICTION.md) and the plan in [tighten evidence](../87-render-works/evidence/tighten/FRICTION.md) | Read-back: overlays gone, originals carry the new media; every clip after the cut is exactly 15 frames earlier; a dry-run reflow moves nothing; the film renders whole | [ ] |
| R One review round before the branch is offered to the Release 15 Lead | S | all | Read-only | Findings become rows `R.n` | [ ] |

## Run decisions

- 2026-11-23: Start from the existing `release/15/plan-88` at `0615e4e9`, as the Run start directs; TE-2 and TE-3 start from TE-1's cherry-pick and merge forward without rewriting history.
- 2026-11-23: TE-1's donor candidate `93c02352e` also touches timing validation, omitted from the card's path list; host asked to confirm scope. Its donor SDK test fails on a session fixture missing `identity` on the current base; host asked for a permitted repair. Candidate with publisher coverage: `186c46904d` (18 passed, 1 failed; no live proof).
- 2026-11-23: Independent code review found no authenticated pre-edit shot word identity in the current commit path; sent the host the required TE-3 refusal-only gate. Refusal proof remains in progress.
- 2026-11-23: Baseline `0615e4e9`: commit-boundary test file 30 passed; both named timeline files are absent at base. TE-2 candidate `c71be97be` has three new provenance cases passing; donor boundary proof 38 passed. Independent review found a grown-bound provenance bypass; correction is in progress.
- 2026-11-23: TE-4 and TE-5 live work waits for RN-6. Evidence identifies eleven overlay IDs but not all original-to-media mappings; host asked for the undo list. No pods or paid resources used.

- 2026-11-23: Superseding the preliminary TE-3 ruling: a concrete authenticated-transcript probe found a unique stable word identity can be derived for bounded inputs; the host declined the refusal-only gate pending that probe, and full-rule implementation proceeds. Film applicability remains unverified.
- 2026-11-23: TE-2 candidate `9048fc12f` corrects the review's grown-bound provenance bypass; 44 focused tests pass and a separate bounded check accepted the correction. Integration waits on TE-1.
- 2026-11-23: TE-1 remains blocked: its donor SDK test fixture lacks base-required session identity. The host proposed changing that new fixture but the run's direct no-fixture-edit instruction is stricter; clarification requested. No existing assertion or fixture was changed.

## The edits in the loop (TE-4)

Each failed, or needed a workaround, on 22 November.

**Must pass.** These are what this plan lands; a block here is a failure of the plan, not evidence for another one.

1. Replace the media of a word-anchored footage clip with a newly imported still, and with a newly imported video.
2. Re-point a clip to an asset already in the registry (this worked on the day; it is the control).
3. Remove a pause: move every clip after a cut by a fixed number of frames, with the narration (accepted by TE-3), and try to move one anchored clip alone (refused by TE-3, naming the supported form).

**Probes.** Other plans own these. Make the edit, record how far it gets, and add the result to the owning issue. A block is an acceptable outcome.

4. Change parameters on a project-pack element clip, and switch a clip to a newly admitted project element (Plan 69).
5. Move one unanchored clip without moving any other (Plan 77, [#1401](https://github.com/banodoco/astrid-dev/issues/1401)).
6. Change about 250 clips in one commit, and find the size at which a commit is refused (Plan 77).
7. Remove a clip, then restore it exactly ([#1430](https://github.com/banodoco/astrid-dev/issues/1430)).
8. Add clips, then undo all of them in one change ([#1430](https://github.com/banodoco/astrid-dev/issues/1430)).
9. Run two edit sessions on different clips at once (Plan 76, [#1402](https://github.com/banodoco/astrid-dev/issues/1402)).

## Run decisions

One line per decision taken by the orchestrator during the run.

- 23 Nov 2026: `release/15/plan-88` cut from `release/15/main` at `0615e4e9` (owner's instruction), not from `release/15/plan-87`; the render-backed proofs build against Plan 87's stack once RN-6 lands.
- 23 Nov 2026: file order with Plan 89 agreed: Plan 89 touches only `_commit_patch.py` and `_doc_patch.py` in the Agent, so Plan 88 goes first on all its files; Plan 89 rebases onto Plan 88's merge SHAs.
- 23 Nov 2026: Codex manager started on route X at high effort; workers by card route (Luna, Terra, Sol for TE-3), reviews by Astra. The Lead gave a standing go for the manager's `tasks.md`-only progress PRs.
- 23 Nov 2026: render requests go to Plan 87's session one per message; TE-4's edits are batched into one request; Plan 87's RN-13 renders take priority.
