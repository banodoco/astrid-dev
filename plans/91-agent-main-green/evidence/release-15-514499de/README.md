# AG-0 re-measure — `release/15/main` at `514499de`

[Evidence](../README.md) · [Tasks](../../tasks.md) · [Inputs](../../inputs.md)

Taken 24 November 2026 by the Plan 91 orchestrator (`session_011EzfW1yUojAfWkGcaZNRph`) for AG-0.

## The cut

astrid-agent `release/15/plan-91` was cut at `514499debc902643a03aee3f0ed68b710c5d3ead`, the `release/15/main` head of the day ("Merge pull request #612 from banodoco/release/15/plan-88"). Plan 88 has landed, so its two failing test files no longer stack ([base choice](../../inputs.md#source-identities)); Plan 77 still does. Later the same day the owner moved Plan 91 to Release 16 (D1), and the plan branch became `release/16/plan-91`, cut at the same commit; `release/15/plan-91` is superseded.

## Runs read

| Workflow | Run | Result |
| --- | --- | --- |
| CI | [45351510784](https://github.com/banodoco/astrid-agent/actions/runs/45351510784) | eight `unit` shards red; `darwin native` **timed out** at its 120-minute limit inside pytest with no result line (it took 10–18 minutes on the three heads before); the rest green |
| Lanes | [45351510868](https://github.com/banodoco/astrid-agent/actions/runs/45351510868) | four `integration` shards and `opt-in` red; `installed wheel` green |
| CI, unchanged tree, dispatched | [45375336008](https://github.com/banodoco/astrid-agent/actions/runs/45375336008) on `release/15/plan-91` (`514499de`) | `darwin native` ran to an outcome in 17 minutes: 15 failed. The 120-minute hang was a one-off on the same tree. The `darwin native` rows here come from this run |

## Totals, each equal to the job's pytest result line

| Job | pytest result line | Rows here |
| --- | --- | --- |
| unit shard 1 | 47 failed, 54 errors | 47 FAILED, 54 ERROR |
| unit shard 2 | 77 failed, 51 errors | 77, 51 |
| unit shard 3 | 31 failed | 31, 0 |
| unit shard 4 | 32 failed, 19 errors | 32, 19 |
| unit shard 5 | 28 failed, 33 errors | 28, 33 |
| unit shard 6 | 261 failed, 25 errors (33 of the failures are subtests) | 261, 25 |
| unit shard 7 | 225 failed, 142 errors | 225, 142 |
| unit shard 8 | 74 failed, 4 errors | 74, 4 |
| darwin native | 15 failed (run 45375336008) | 15, 0 |
| integration shard 1 | 44 failed | 44, 0 |
| integration shard 2 | 120 failed, 292 errors | 120, 292 |
| integration shard 3 | 123 failed, 117 errors | 123, 117 |
| integration shard 4 | 93 failed, 26 errors | 93, 26 |
| opt-in | 12 failed | 12, 0 |

**CI: 1,118 (job, id) rows in 276 test files, 428 clusters (the unit shards of run 45351510784 and `darwin native` of run 45375336008). Lanes: 827 rows in 128 files, 106 clusters. 1,945 in all.** `cluster_failures.py` now prints this check for every log it reads and marks any job whose rows differ from its result line, or that has no result line.

## The parser, fixed

The first measurement at `b324d7c1` undercounted: re-run on the same `b324d7c1` logs, the fixed script finds 1,122 CI rows (published 1,087) and 827 Lanes rows (published 787). Three causes, all fixed in `cluster_failures.py`:
- **IDs with spaces were dropped.** A parametrized ID such as `test_param_map_parity[z-image-i2i-local-{'prompt': ...}]` holds spaces, and the summary pattern stopped at the first one. The ID now ends at the first ` - ` outside its brackets.
- **Failed subtests were not counted.** pytest counts each failed subtest in "N failed" but gives it no summary row. They are now taken from their `SUBFAILED(...)` progress line and keyed `<nodeid> SUBFAILED(<params>)` (33 in unit shard 6).
- **Inner pytest output was counted.** Tests that run pytest themselves print its rows (for example `test_case.py::test_x`). Only the job's own last `= short test summary info =` section, before its final result line, is read now.

`env/baseline-diff.py`, which AG-1 reuses, should be checked for the same three cases before it gates anything.

## What changed since `b324d7c1`

[changed-since-b324d7c1.tsv](changed-since-b324d7c1.tsv), both runs read with the fixed parser, keyed by job family (see below):
- **No longer failing (5):** four `tests/core/generation/test_readiness_missing_models.py` and two `tests/test_pinokio_platform_adapter.py` IDs, both groups the [Release 15 baseline](../../../../releases/15/evidence/agent-ci-baseline-8807f820/README.md) records as moving between runs; and `tests/integrations/test_command_count_capture.py::test_fresh_process_command_counts`.
- **Newly failing (1):** `tests/core/execution/test_generic_host_child_bridge_d18.py::test_host_bridge_outer_send_diagnostic_preserves_revoke_close[False]` (integration), in the child-bridge file AG-B11 owns, whose writers the baseline already names as racing.
- **`darwin native`:** all 13 of `b324d7c1`'s still fail, and 2 more fail: `tests/packs/test_audio_render.py` and `tests/packs/test_text_card_render.py`, each "candidate reconciliation budget ran out after 1.1–1.6 s". That is the macOS render deadline group the Release 15 baseline names as moving (D14), so they go to AG-B22 (ci:C93).

Nothing else moved. Plan 88's landing changed no failing ID outside the groups that move.

## Two findings for AG-1

- **Tests move between shard numbers.** The same two `tests/sdk/test_timeline_clip_scalar_provider.py` IDs failed in `unit shard 7` at `b324d7c1` and in `unit shard 6` here, and `test_native_word_anchor.py::...[missing-version]` moved from integration shard 2 to shard 3. Keyed by (shard, id), each would read as one lost and one new failure. The ceiling and the comparison key by job family: `unit`, `darwin native`, `integration`, `opt-in`, and the single jobs by name.
- **Log file names carry a number that changes between runs** (`9_unit shard 6 …` here, `1_unit shard 6 …` at `b324d7c1`). The job column now drops it.

## Cluster numbers

Cluster numbers moved, so [assignment.json](assignment.json) was remapped from `b324d7c1` by grouping key. Three keys moved line because the code moved and were mapped by hand: lanes C1 (`service.py:3400` → `:3421`), C11 (`sync.py:1220` → `:1245`) and C19 (`timeline_address.py:520` → `:524`, now C20). [wave-c-cards.md](wave-c-cards.md) and [prune-candidates.md](prune-candidates.md) are regenerated: **Wave C 432 IDs in 235 files; prune candidates 392 IDs in 94 files.** Each card's IDs are in [cards/](cards/), written by `make_wave_c.py`; `cards/AG-A8.tsv` is a first reading by refusal message, split from AG-A7's clusters. The card counts are at the end of `wave-c-cards.md`. From AG-0 on, `ci:C<n>` and `lanes:C<n>` in new packets mean this folder's rows.

## What cancels started runs on `release/15/main`

**People's sessions do, by hand, through the shared account.** Every one of the 18 cancelled runs among the last 30 CI and Lanes runs on `release/15/main` (21 to 23 November) carries the check annotation "The run was canceled by @AstridPseudon" (one "canceled forcefully"). `@AstridPseudon` is the account every Release 15 session uses. No workflow rule cancels them: both workflows set `cancel-in-progress` false for `release/*/main` (`ci.yml:16-18`, `lanes.yml:18-20`), and none of the cancelled jobs carries GitHub's concurrency message ("Canceling since a higher priority waiting request … exists").

The pattern fits the release's CI-capacity rulings (one Agent run at a time, later two): a landing merge starts a push run of CI and Lanes, and the landing lane or the Lead cancels it seconds later to keep the slot for its own dispatched run (for example `0615e4e9` at 17:09 and `045064b6` at 18:25 on 23 November, each cancelled within 25 seconds alongside a plan branch's pull-request run), or later, when a newer landing follows (`8fdf6615`, after 27 minutes).

Consequences for this plan: D7's comparison of every completed `release/15/main` run gets few runs to compare, and AG-10 does not rely on push runs (D15). The orchestrator asks the Release 15 Lead for a standing ruling that a `release/15/main` push run is not cancelled, or that the landing lane names, at landing, the run that stands in for it.
