# Plan 39 K1 — E14 stale Runtime pin affects 85, not just 68, exact-head tests

**2026-11-17 UTC · N-class evidence extension only; no candidate execution or acceptance.**
This supplements [the original 68-occurrence diagnosis](k1a-e14-runtime-pin-drift-20261117.md), without replacing or modifying any frozen baseline. The **same full literal setup message** occurs in three completed CI jobs, not only unit shard 7.

## Exact-head evidence and reconciliation

Agent PR369 was merged **only** into `release/14/plan-39` at `6bbda788c1a62abcdda242f85c7a1cae86c57d3d` (reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`). Completed [CI 43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168), **attempt 1**, has the following 85 **error** occurrences across the same XML message group (SHA-256 `2e4afad1dcbbe9ae8dc51baed4c60a5a72503ffbdf0e65019d9a9063490e4af1`):

| Exact job | Count of same full XML message | Original JUnit artifact | ZIP SHA-256 | XML SHA-256 |
| --- | ---: | --- | --- | --- |
| [Darwin 133651924059](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924059) | **1 error** | [14277714424](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14277714424) | `06a2bac5da6c594ded3ca0f5dec3f0237fc6d02bff165cebd39d39450c386df0` | `07bd706c3faced716a9a421820e8da6a2bddf099af6fdc7d1347fa574483b984` |
| [Unit shard 4, 133651924745](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924745) | **16 errors** | [14282820153](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14282820153) | `2acb279263d68ae27adb9a008e0e0d610dc9bf4662c40fb2c6645cf7bdbe1cf7` | `63ea09f25b19ec3267f75f37d07a4fc0af9b122117fd956fa90a49e44b508008` |
| [Unit shard 7, 133651924616](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924616) | **68 errors** | [14281865130](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14281865130) | `3d208e420b35370e7b153a3f6349a64c415df126e87d3f5d97b7b1b9c8c0693a` | `3bd9218c3830caf27bc2502a50ebc7293c19012bad01a2e890b1f31c703b993b` |

**Identical full literal XML message** (verbatim, all three jobs):

```text
failed on setup with "AssertionError: assert '6855dfa8df65...4d6505493c17c' == '9ef808711a52...af6fdd7bc9550'
  
  - 9ef808711a5207f5be74dc5f267af6fdd7bc9550
  + 6855dfa8df65cf8ae4c002b57134d6505493c17c"
```

Concrete currently red **exact IDs** for the newly identified cohorts:
- Darwin: `tests.integrations.test_managed_media_saved_visualize::test_saved_revision_with_managed_media_visualizes_a_frame` (1 error).
- Unit 4: `tests.editing_conformance.test_reviewed_list_runtime_v3::test_disjoint_reviewed_doc_patch_list_merges`, `::test_reviewed_list_before_state_conflicts`, and `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_cli_retry_reports_accepted_part_from_durable_pending_state` (examples of 16 errors).
- Unit 7: `tests.sdk.test_timeline_clash_back_runtime::test_new_file_swap_recovery_reimports_after_saved_runtime_refusal` and related current exact IDs (68 errors, previously documented).

The previously produced **complete** local actual-XML/testcase JSON inventory was rehashed before this cross-job query: gzip SHA-256 `729e8a833061dc0b29c6cc345aef8b61d740ba83f004d969923398fc3a9c5426`. Its three message records each match the **same** full literal message and its 1+16+68 exact IDs. This continuation reuses the previously authenticated artifact ZIP/XML SHA-256 chain; it does **not** claim fresh network downloads of each artifact. The 85 are **already counted** in CI's original **882 failures / 398 errors**; never add 17 to those workflow totals. Neither [Lanes 43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160) nor its original **306 failures including 12 opt-in / 260 errors** has changed.

## Source and repair boundary

The three new cohorts **all consume the same `editing_case` fixture** in [`tests/sdk/test_timeline_editing_acceptance_runtime.py`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/sdk/test_timeline_editing_acceptance_runtime.py), directly (Darwin `test_managed_media_saved_visualize.py` and reviewed-list `test_reviewed_list_runtime_v3.py`) or as a registered pytest plugin (`test_timeline_clash_back_acceptance_runtime.py` and `test_timeline_clash_back_runtime.py`). The old fixture compares actual Runtime checkout `6855dfa8df65cf8ae4c002b57134d6505493c17c` with stale literal `9ef808711a5207f5be74dc5f267af6fdd7bc9550`, before running the substantive assertions.

Isolated [draft Agent PR377](https://github.com/banodoco/astrid-agent/pull/377) modifies **only that shared fixture's** `RUNTIME_COMMIT` source, using the committed Runtime lock helper, and leaves the checkout HEAD and imported-source assertions intact. Thus its **candidate reach is 85 measured setup errors**, not merely the originally documented 68. That is a **scope/reach forecast, not proof** that any of the 85 pass afterward. No product/runtime behavior, test conditions, skips or xfails should be weakened.

**Missing mandatory gates:** independently submitted N review with real reviewer/model provenance, focused execution in a genuine Agent worker environment, then independently reviewed integration into `release/14/plan-39` only and new exact-head hosted XML. Existing Plan38/55 ownership stays WAITING; Runtime clip 25P/2F replay-versus-CAS-integrity contract remains untouched; Release15 excluded; formal G1/G2 incomplete and **RS1 0/1**. No test-ID absent from an earlier snapshot is counted as a regression, and no attribution to PR369 is inferred. No CI cancellation/rerun/dispatch, authentication retry, other PR merge, `inputs.md`, task-checkbox, release-main or public-main changes.
