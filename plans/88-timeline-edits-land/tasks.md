# Tasks — Timeline edits land and hold

[Plan](plan.md) · [Inputs](inputs.md)

These are proposed task cards, not dispatch authority. Every source path and symbol must be re-checked against the code at dispatch.

**Task ids:** `TE-n`. **Critical path:** TE-1 → TE-3 → TE-4 → TE-5.

**The rule for every task:** an edit is done when a fresh read-back shows exactly the intended change and nothing else, and a render from Plan 87's stack shows it.

**Test inventory:** `tests/timeline/test_occurrence_media_swap.py` (439 lines, from the donor commit), `tests/timeline/test_legacy_occurrence_timing_provenance.py`, the commit-boundary tests, and the sandbox repro scripts in [Plan 87's evidence](../87-render-works/evidence/edits/).

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| TE-1 Media on an existing shot-owned footage clip can be replaced with newly imported media (cherry-picked here; Plan 87's branch does not carry it); every other authored field, including a word anchor, is unchanged; SDK `swap_asset`, CLI `--swap-asset` and the document publisher share the route | X | Plan 87 RN-6 | Cherry-pick `24740fdf`: `astrid/sdk/timeline/media_swap.py`, `native_occurrence_media_commands.py`, `commit_session.py`, `timeline_media_replacement.py`, `astrid/packs/timeline/cli_native.py`, `timeline_document.py` | Donor tests, plus one real swap on the stack: a word-anchored footage clip, new media, read-back differs only in media. Closes [#1404](https://github.com/banodoco/astrid-dev/issues/1404), part of [#1405](https://github.com/banodoco/astrid-dev/issues/1405) | [ ] |
| TE-2 A clip whose legacy overrun is unchanged survives a pure start shift | N | TE-1 | Cherry-pick `ad10ff6d`: `_commit_timing_validation.py`, `validation.py` | Donor tests plus grown-bound, shrunk-bound and changed-source-window cases; its review folds into R | [x] `95e29aab8` |
| TE-3 A timing-only edit to a word-anchored shot clip is accepted only when all of these hold: the clip had a valid resolved anchor before the edit; the word it resolves to is the same one after it, identified by transcript, source and word identity, and is unique (no nearest-match guess); the clip's offset from that word is unchanged within one frame at both its start and its end; its duration and source mapping are unchanged. Otherwise the edit is refused and the refusal names the supported cut-relative form. Replaces `d4bf28e4` | S | TE-2 | `_commit_timing_validation.py`: `_BasisReader.signature`, `_signed_failures`, `_legacy_exemptions` (the validator has no authenticated word binding today, about line 106); `reflow.py` (its nearest-word choice, about line 588, must not be what decides acceptance); `_timing_evaluators.py`. If a unique word identity cannot be established at commit time, TE-3 is delivered as the refusal alone and the ripple edit moves to [Plan 18](../18-timeline-editing/plan.md); say so within two days of starting | A test with a resolvable word: narration and clip moved together (accepted); clip moved alone (refused); an ambiguous word (refused); then a reflow moves nothing. Part of [#1403](https://github.com/banodoco/astrid-dev/issues/1403) | [ ] |
| TE-4 The edit loop on the heavy fixture (the standard variant Plan 87 renders): for each edit below, make it, read it back, render it, record the result | X | TE-1 to TE-3 | Fixes only where the cause is in TE-1 to TE-3's code; everything else is evidence on the owning issue | The loop log: one row per edit with command, outcome, read-back diff, render frame, and issue number if blocked | [ ] |
| TE-5 A film-shaped fixture variant exists in the App's builder and is proved on: the overlay workaround converts back to in-place media swaps, and cutting 15 frames after a word moves everything after it. It is a permanent regression test (replaces the real-film version, which the owner keeps: no card depends on her project) | X | TE-4 | `scripts/save-loop/build-fixture.mjs` in astrid-app: a `film-shaped` variant with the structures the film hit (shot-owned footage clips, word-anchored clips with word provenance from a generated transcript, a legacy overrun, and the overlay state: overlay clips over their originals), all generated media. Branch `release/15/plan-88` in astrid-app, cut from `release/15/main`. Then the proof, on that fixture, in Agent | Read-back: overlays gone and originals carry the new media; every clip after the cut is exactly 15 frames earlier; a dry-run reflow moves nothing; the film-shaped fixture renders whole on Plan 87's stack. The variant is built by a script any session can rebuild | [ ] |
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

- 23 Nov 2026: TE-1 independent review identified media type verification, selector/provenance and ordinary-edit grouping defects; candidate `4c6b9207d` addresses them with 31 focused tests passing, and the reviewer accepted the follow-up. Live swap, complete read-back and host gate remain; host owns integration of the host-authored fixture commit.
- 23 Nov 2026: TE-3 authenticated identity probe passed for a unique pinned transcript/source/word; ambiguity refused. Refusal increment `f601acfba` passed 37 tests; full-rule work remains uncommitted and its initial no-op reflow proof fails on an inherited unrelated fixture mismatch. Latest placement and retained-transcript changes are untested.
- 23 Nov 2026: Checkpoint requested for a revised run brief. TE-2 `9048fc12f` is pushed with 44 focused tests passing and reviewed correction; TE-1 and TE-3 branches are pushed, with uncommitted TE-3 work retained in its worktree. RN-6 remains outstanding. No tasks merged and no rented resources used.

- 2026-11-23: Superseding the earlier TE-1 fixture block, the host supplied the identity required by the new donor test fixture; its assertions are unchanged, and the revised run authority permits this adaptation and host commit.
- 2026-11-23: TE-1 `sync.py` is in scope because both submitted and interrupted CLI swaps must retain their provenance. Independent review of `0615e4e9..4c6b9207d` found three regressions (local-file verification, first asset assignment, and multi-swap ordering); fixes and follow-up review are required before live proof.
- 2026-11-23: TE-3’s no-op reflow failure includes an unrelated parent fixture with a 2-second hold and a 0.5-second authored duration; the new fixture may be made internally consistent while preserving the no-movement assertion.
- 2026-11-23: TE-5 uses generated media only, as the owner directed; the old film mapping request is withdrawn. Its builder needs a retained Runtime transcript and a separate fixture-specific check.

- 2026-11-23: TE-1 merged as `44b344d66` after 34 focused tests passed on `4943c7583` and the bounded independent review passed; its live word-anchored swap and render remain open pending RN-6, so TE-1 is not complete.
- 2026-11-23: TE-2 merged as `95e29aab8`; on `5409ced91`, `bash ../astrid-dev/env/agent-pytest.sh -q -rA tests/timeline/test_legacy_occurrence_timing_provenance.py tests/editing_conformance/test_commit_boundaries_d12.py` passed 44 tests. Prior review's provenance finding was fixed and independently checked; the host confirmed standing plan-branch merge authority.

- 2026-11-23: Native word vector `test_portable_native_captures[a]` and `[b]` also fail on the exact plan baseline `0615e4e9` (12 passed, 2 failed); treat them as pre-existing. TE-3 candidate `ce20c344` had 66 focused passes but four independent-review findings require repair.

- 2026-11-23: TE-5 is parked until RN-6; backup `8523400fe` preserves media preparation (10 focused tests), imported fade coercion and a legacy declaration import with an exact retained transcript pin; shot word retime, real pack admission, the full builder and render remain unproved.

- 2026-11-23: TE-3 merged as `cb14daac9`; on `6195c2c3b`, `bash ../astrid-dev/env/agent-pytest.sh -q -rA tests/editing_conformance/test_shot_word_retime_refusal.py tests/editing_conformance/test_commit_boundaries_d12.py tests/timeline/test_legacy_occurrence_timing_provenance.py` passed 76 tests, and 9 focused reflow golden tests passed; four final review regression cases failed before repair and passed after. Host authorized the bounded final repair without another review round; the live read-back and render remain pending RN-6, so TE-3 is not complete.

- 2026-11-23: TE-1 metadata follow-up merged as `850cae55e`; verified image/video dimensions now become registry resolution and audio/video duration is retained. Candidate `b762f41a8`: new still-swap test failed before the change; focused native/swap command passed 94 (`bash ../astrid-dev/env/agent-pytest.sh -q -rA tests/editing_conformance/test_imported_media_metadata.py tests/timeline/test_occurrence_media_swap.py tests/editing_conformance/test_recipe_occurrence_media.py`), new local Runtime PNG import passed separately, and audio binding passed a focused check. Three integration cases excluded by the repository default were run explicitly and failed identically on base `cb14daac9` and candidate, so they are pre-existing; live stack read-back/render remains pending.

- 2026-11-23 (Lead): Unpark TE-5’s film-shaped builder before TE-4 anchored work because the standard fixture lacks its required structures; use standard/large-shots for non-anchored swap, control and probes 5–9, and film-shaped for anchored swap, ripple and project-pack probe.

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
- 23 Nov 2026 (Lead, on the owner's direction): TE-5 no longer touches the owner's film project. It becomes a `film-shaped` variant of the App's save-loop fixture builder plus the same proof (overlays back to in-place swaps; 15 frames cut after a word) on generated media, kept as a permanent regression test. Cleaning up the real film is the owner's, after the fixes ship. Proofs run on inputs any session can rebuild. A branch `release/15/plan-88` in astrid-app is cut from `release/15/main` for the builder change (recorded for the Lead's branch table).
- 23 Nov 2026 (Lead, owner's review rule, astrid-dev PR #1699): a per-card high-judgment review runs only for an S card, a change to what is accepted, refused or published, or code already judged unsound. So: TE-1 keeps the review it has had (its repair gets one confirming check, then the PR); TE-2 drops its separate review and folds into R; TE-3 (S) keeps one review before TE-4 builds on it; TE-4 and TE-5 go to R. Every other card is proved by its own focused tests.
- 23 Nov 2026 (Lead): merging a task PR into the plan branch `release/15/plan-88` is the manager's, no gate needed; the Lead's gate is only for `release/15/main` and CI slots. TE-1 (PR #561) merged into the plan branch as `44b344d6` on that rule; its Progress box stays unticked until the live swap and render pass.
