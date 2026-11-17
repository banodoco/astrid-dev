# Plan 39 K1 prerequisite — E14 Runtime fixture tests stale revision, not locked checkout (2026-11-17 UTC)

**N-class source/actual-XML diagnosis and isolated draft candidate. No accepted repair.** Agent exact reviewed head `6bbda788c1a62abcdda242f85c7a1cae86c57d3d` (tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`), CI [43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168) attempt **1** completed failure; Lanes [43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160) attempt **1** completed failure. Historical totals **CI 882 failures / 398 errors** and **Lanes 306 failures (including 12 log-only opt-in) / 260 errors** are unchanged. These 68 CI failures are **already included**, not additive.

## Original actual JUnit and literal message

[CI unit shard 7 job 133651924616](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924616), [JUnit artifact 14281865130](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14281865130), original verified archive **ZIP SHA-256 `3d208e420b35370e7b153a3f6349a64c415df126e87d3f5d97b7b1b9c8c0693a`**, inner **XML SHA-256 `3bd9218c3830caf27bc2502a50ebc7293c19012bad01a2e890b1f31c703b993b`**. Actual XML aggregate: **6,163 tests, 250 failures, 160 errors, 4 skipped**; **110 distinct per-job literal XML-message groups**. The complete previous full-message/testcase-index inventory remains unchanged, SHA-256 `729e8a833061dc0b29c6cc345aef8b61d740ba83f004d969923398fc3a9c5426`.

One exact full literal XML message, **68 occurrences**, message SHA-256 `2e4afad1dcbbe9ae8dc51baed4c60a5a72503ffbdf0e65019d9a9063490e4af1`:

```text
failed on setup with "AssertionError: assert '6855dfa8df65...4d6505493c17c' == '9ef808711a52...af6fdd7bc9550'
  
  - 9ef808711a5207f5be74dc5f267af6fdd7bc9550
  + 6855dfa8df65cf8ae4c002b57134d6505493c17c"
```

Actual XML includes exact red examples `tests.sdk.test_timeline_clash_back_runtime::test_new_file_swap_recovery_reimports_after_saved_runtime_refusal`, `::test_new_file_swap_recovers_after_same_actor_default_outbox_race` and `::test_reviewed_new_file_swap_runtime_conflict_is_saved_and_explicit_retry_recovers`. The 68 are **message occurrences**, not 68 distinct independently proven downstream root causes. We do **not** infer regression from absent old IDs. Prior exact-ID comparisons remain separately preserved; no new comparable-baseline check was performed for this group.

## Source and installation provenance

At the tested commit:

1. [Agent `runtime.lock.json`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/runtime.lock.json) selects **`source_commit: 6855dfa8df65cf8ae4c002b57134d6505493c17c`**.
2. [`.github/workflows/ci.yml`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/.github/workflows/ci.yml) unit-shard checks out exactly `steps.runtime-pin.outputs.commit` to `astrid-runtime`, sets `ASTRID_RUNTIME_CHECKOUT`, and executes `python scripts/ci_install_runtime.py`. The installer reads the **same lock** and installs that Runtime/client.
3. [`tests/sdk/test_timeline_editing_acceptance_runtime.py`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/sdk/test_timeline_editing_acceptance_runtime.py) instead hard-codes `RUNTIME_COMMIT = "9ef808711a5207f5be74dc5f267af6fdd7bc9550"` and its `editing_case` fixture asserts the checked-out HEAD equals that constant *before* running E14 SDK behavior. The fixture advertises acceptance **against the locked Runtime**, making the mismatch a stale test-provenance expectation, not evidence that the product operation is wrong.
4. [`tests/helpers/runtime.py`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/helpers/runtime.py) already exposes `vendored_runtime_commit()`, reading the committed lock. Reusing it preserves an exact-SHA verification of source checkout identity.

## Isolated candidate, not accepted

[Agent **draft PR377**](https://github.com/banodoco/astrid-agent/pull/377), task branch `p39/k1a-e14-runtime-pin-20261117`, exact base `6bbda788`, commit **`5b9db95c84f863c0eee63c238bdeb4583b49d7c7`**, modifies **one file only**, 4 insertions and 2 deletions. It imports `vendored_runtime_commit` and defines `RUNTIME_COMMIT = vendored_runtime_commit()`. It keeps both `assert actual == RUNTIME_COMMIT` and the independent `timeline_commit_store.__file__` source-path assertion, leaving all functional expectations, provenance verification, skip/xfail, and product code intact. The browser/read-back and Git comparison verify exactly one isolated change, but **no focused execution, independent reviewer, or hosted candidate XML** exists. This is not a passing-fix claim.

**Independent N-class review** must confirm following the current locked Runtime is intended, including the revision shift from `9ef808...` to `6855dfa...`, and no Plan38/55 ownership conflict. Then perform worker focused tests and prove exact-ID outcomes on reviewed integration into `release/14/plan-39` only. If downstream SDK failures emerge, classify them independently; do not weaken assertions or label missing IDs as regressions.

**Separate unruled failure cluster:** unit shard 7 includes another **92** setup occurrences whose literal error expects `runtime_protocol` to import from the source checkout but finds `site-packages` instead, and unit shard 6 includes **3** occurrences with that message. Those **95 existing occurrences** are not fixed by PR377. The ordering of `sys.modules`, installed package, source helper, and per-test import checks requires independent source/provenance triage before any change. Keep security and source authority assertions. The 95 are *also included* in the unchanged CI total.

Other draft Agent PR373–376 remain independently unreviewed/unmerged with no candidate hosted proof at this poll. Plan38/55 **WAITING**, Release15 excluded, Runtime clip patch **uncommitted 25 passed / 2 failed** on owner replay/history-integrity hold. Formal **G1/G2 incomplete, RS1 0/1**. No workflow cancellation, rerun, dispatch or authentication retry; no changes to `release/14/main`, public `main`, `inputs.md` or plan task checkboxes.
