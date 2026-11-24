# Runtime cards: C3, C7 and the legacy_authority tests (read-only, Plan 39 rebuild on release/15/main)

Heads checked: astrid-runtime release/15/main = 24e2c929 (23 Nov 2026); astrid-agent pin = 0e1543e0; Agent release/15/main = 514499de; astrid-dev main for plans. Nothing changed, pushed or dispatched.

## Verdict in one line
The default V1/A1 tracks are seeded by the Runtime, not the Agent. The three test files still expect the pre-seed empty track list. Kind: **stale-test**, with one open owner question (issue #1507) that could flip it to product-bug.

## Card RT-C3C7-1: update the starter-track expectations in the inverse, forward and legacy authority tests

- Repo: astrid-runtime. Clusters: C3 (28 distinct IDs), C7 (8), C32 (1), C34 (1), C35 (1). Total 39 distinct IDs, 117 rows across the three CI jobs (unit ubuntu, unit macos, sandbox). Source: `failing-ids.tsv` (84 + 24 + 3 + 3 + 3 rows).
- Files and failing IDs:
  - `tests/test_timeline_inverse_sequential_authority.py`: 28 IDs (`test_inverse_sequential_scope_round_trip[legacy|v2 x native-delete|whole-restore]`, `test_restore_inverse_refuses_inexact_sequential_authority[...]`, and others in the file).
  - `tests/test_timeline_forward_created_authority.py`: 8 IDs in C7 (`test_real_forward_omission_keeps_exact_allocations[...]`, 8 parametrizations; `test_declared_allocation_and_retired_reservation_remain_exact` is also listed under C7/C32 in the TSV, so C7 is 8 IDs and C32 is the 1 listed at :124).
  - `tests/test_timeline_legacy_authority.py`: 2 IDs (C34, C35).
- Kind: **stale-test**.
  - Product side (verified in code): a new timeline is created with the canonical starter tracks. `runtime_protocol/timeline_commit_store.py:2603-2625` calls `default_bootstrap_document`; `runtime_protocol/timeline_commit_baseline.py:426-433` builds V1 and A1 rows. Each of these tests creates its timeline through `service.create_timeline(...)` (the forward fixture at `tests/test_timeline_forward_created_authority.py:26`), so the empty-track baseline the tests assume never exists.
  - Test side (verified in code): the expectations are the empty list or a one-track list. `tests/test_timeline_inverse_sequential_authority.py:30` asserts `tracks == []`. `tests/test_timeline_forward_created_authority.py:82` asserts `tracks == [call["args"]["row"]]`, and `:124` asserts `tracks == []`. `tests/test_timeline_legacy_authority.py:476` asserts `[{"id":"video",...}]` and `:522` asserts `[{"id":"audio",...}]`. The log diffs show actual = `[V1, A1, <row>]`.
  - Source that states the new behaviour and postdates the test's last change (the Plan 91 rule):
    - `astrid-dev` `plans/77-saving-holds-on-a-heavy-timeline/rounds.md:449` (committed 23 Nov 2026, `868b216`): "The Runtime bootstrap already has its canonical V1 and A1 rows."
    - `astrid-dev` `plans/77-saving-holds-on-a-heavy-timeline/tasks.md:79`: the same starter-track mismatch is "pre-existing".
    - `astrid-runtime` commit `b2b514b` (27 Oct 2026, 16:56 UTC, "test(runtime): align fixtures with canonical timeline bootstrap") changed `tests/test_shot_composition_runtime.py` to expect V1/A1. It did not touch these three files, which is the gap.
    - `tests/test_timeline_commit_baseline.py:324-328` (`test_default_bootstrap_tracks_are_valid_and_detached`) pins the V1/A1 rows.
  - Date caveat: the release branch history is squashed to 27 Oct. The seed and the three tests all show as introduced in merge `f232693` (27 Oct 12:12 UTC), so I cannot date from git when the expectations last matched behaviour. The expectation is older than the 23 Nov plan text by weeks.
- Fix (by the allowed kind, no product change): replace the literal empty or one-track expectations with the canonical starter rows, for example by importing `default_bootstrap_document` from `runtime_protocol.timeline_commit_baseline` and taking its `config.tracks`, then appending the created row. Do not add a skip, deselect or retry.
- Scope, by path:symbol:
  - `tests/test_timeline_inverse_sequential_authority.py:test_inverse_sequential_scope_round_trip` (line 30 only; the later `canonical_document == created` checks are already relative and need no change).
  - `tests/test_timeline_forward_created_authority.py:test_real_forward_omission_keeps_exact_allocations` (line 82) and `:test_declared_allocation_and_retired_reservation_remain_exact` (line 124).
  - `tests/test_timeline_legacy_authority.py:test_service_actual_bootstrap_command_restore_and_exact_retries` (line 476) and `:test_http_actual_create_command_restore_rename_and_ordinary_artifact_metadata` (line 522).
  - No product file changes.
- Focused proof: `pytest -q tests/test_timeline_inverse_sequential_authority.py tests/test_timeline_forward_created_authority.py tests/test_timeline_legacy_authority.py`, plus `tests/test_timeline_commit_baseline.py` (covering test for the seed). Runs in the same CI jobs as the failures.
- Route: N. Size: 0.5 engineering day.
- Dependencies: none on other cards. Blocked in part by owner question Q1.
- Confidence: verified in code (seed site, expectations, log diffs from failing-ids and REPORT). Inferred: that the test side is the stale one. That inference rests on Plan 77's statement, which is written from the App's point of view.
- Open questions:
  - **Q1 (blocking the reading, not the edit):** astrid-dev issue #1507, "native starter-track semantics", is still open (plans/77 tasks.md:79 and rounds.md:449 say it "goes through a separate owner decision"). App capture requires the empty-track shape (rounds.md:447-449; App guard link in that paragraph). If the owner decides native timelines should start empty, the seed at `timeline_commit_baseline.py:426-433` is the product bug and these expectations are right. Then this card becomes product-bug. Ask the owner before merging the expectation change.

## Legacy_authority tests and the support line

- `tests/test_timeline_legacy_authority.py` is misnamed. Its refusal tests (410 `retired_route` / `RetiredRouteError`, e.g. lines 143-242, 249-305, 374-428; `reject_retired_timeline_writer` at `runtime_protocol/service.py:462-475`) are the D5 refusal tests and pass. Keep them.
- The two failing IDs (C34, C35) test current behaviour: create, commit and restore through the supported provider. Under the support line ("tests of what users do today are never deleted") they are **not retired**. They are part of Card RT-C3C7-1.
- `tests/test_timeline_inverse_sequential_authority.py` and `tests/test_timeline_forward_created_authority.py` run a `v2=False` ("legacy") body shape. The current Runtime accepts that shape (the test passes it to `commit`), so it is current behaviour and is not retired today. Open question Q2: if the owner retires the v1 body shape under D5, those parametrizations need a 410-style refusal test instead. Not decided by any source I found.
- No card deletes a test for these files.

## Agent pin: would bumping to Agent release/15/main change these?

- No evidence it would, for C3/C7/C32/C34/C35.
- Neither the pin (`0e1543e0`) nor Agent release/15/main (`514499de`) seeds V1/A1 tracks: `git grep` for `'V1'`/`"V1"` in `astrid/sdk` and `astrid/core` finds only `astrid/sdk/timeline/media_add.py:95,111,114` (suggestions for a media add) in both, at `media_add.py:95` (pin) and `:98` (release). The seed is only in the Runtime.
- Agent pin to release/15/main changes 137 commits touching `astrid/sdk/timeline` and `astrid/core/timeline`. These could change other clusters (for example C4 `video_editing` pack, C5, C6), but I did not read them for the track-create path. Inferred, not run: no change to C3/C7/C34/C35. A bump needs a dispatch to confirm.

## What I could not verify

- I did not run any test. The conclusion that the expectations are stale rests on reading the seed and expectations and on the logged actual values.
- release/15/main history is squashed or shallow to 27 Oct, so git cannot date the first commit that seeded V1/A1 or the last commit that matched the tests.
- Whether the App needs the empty shape to stay (Q1) is outside this repo.
- Whether bumping the Agent pin changes anything (inferred only).
- Cluster counts: `clusters.md` lists C7 as 24 rows and the brief as 8 IDs. These are the same thing (24 rows = 8 IDs x 3 jobs). I used the ID counts.

## Owner questions
- Q1: Starter tracks. Is issue #1507's answer "native timelines start with V1/A1" (then these tests are stale) or "start empty" (then the seed is a product bug and these expectations are right)?
- Q2: Does the v1 ("legacy") body shape stay supported under the support line? If not, those parametrizations become refusal tests.
