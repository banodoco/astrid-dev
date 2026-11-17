# Plan 39 K1a — macOS 15 failure-mode provenance: 40 exact red IDs and isolated repair

**Status:** Source-evidenced N-route prerequisite fix candidate; **not accepted**. Agent exact merged/reviewed head `6bbda788c1a62abcdda242f85c7a1cae86c57d3d` / tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`. This note does **not** revise the frozen G1 baseline or the existing exact-head totals.

## Hosted evidence, unchanged test counts

Exact-head [Agent CI 43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168), attempt 1, completed failure: **31,351 tests; 882 failures, 398 errors, 55 skipped** across nine failing JUnit jobs. In its **actual XML** two jobs share exactly the full literal message `KeyError: 'macos-15'` (SHA-256 of literal message `7e50c076d42ec2a2cb14b3b73dd06c0f522bacac69d765b4992447a318c5bbc6`).

| Job | XML failure occurrences with this *exact* message | Actual XML source | Original artifact ZIP SHA-256 | Inner XML SHA-256 |
| --- | ---: | --- | --- | --- |
| Unit shard 7, job [133651924616](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924616) | **25** | [JUnit artifact 14281865130](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14281865130) | `3d208e420b35370e7b153a3f6349a64c415df126e87d3f5d97b7b1b9c8c0693a` | `3bd9218c3830caf27bc2502a50ebc7293c19012bad01a2e890b1f31c703b993b` |
| Unit shard 8, job [133651924880](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924880) | **15** | [JUnit artifact 14278249808](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14278249808) | `035eb0316e0ca3b3294b4eeb5ac205d78bdd0ce754b86628d090fd253ca7d891` | `adb00f44093c9f0656c1b050b4e712e83a5e31203fd72f89224af0d598885c42` |

There are **40 XML failure occurrences**, 40 distinct direct testcase IDs across those two jobs. Unit 7's 25 are `tests.test_failure_receipts::` IDs. Unit 8's 15 are `tests.test_journey_failure_modes::`, `tests.test_journey_predicates::` and `tests.test_native_service_adapter::` IDs. The full exact-ID and complete literal-message inventory is retained separately as the compressed complete Agent XML inventory: SHA-256 `729e8a833061dc0b29c6cc345aef8b61d740ba83f004d969923398fc3a9c5426`. These **40 are already inside the CI total of 882 failures**. They are not new additional failures, and no comparison against prior-plan *same testcase IDs* was undertaken in this bounded diagnosis; no regression attribution is made.

## Source-proven deterministic wiring failure

At this exact Agent head:
- `scripts/journey_matrix.py` defines `M4_6_MATRIX` from three direct plus six deferred Pinokio failure-mode slots; the macOS direct/Pinokio slots name hosted runner `macos-15`.
- `scripts/journey_failure_modes.py:RUNNER_PROVENANCE` maps `macos-14`, `ubuntu-24.04`, and `windows-2022` but **not `macos-15`**. The actual implementation `_runner_errors` looks up `RUNNER_PROVENANCE[runner]`; `tests/failure_mode_fixtures.py:valid_observation` likewise looks up `RUNNER_PROVENANCE[contract["runner"]]`. Either raises the observed `KeyError` for the macOS-15 rows.
- The intended `ImageOS` value `macos15` is independently present in `scripts/check_journey_evidence.py` and `scripts/pinokio_platform_adapter.py`. This is a missing compatible provenance mapping, **not** evidence that the M4-6 receipt semantics should be relaxed. Existing old `macos-14` mapping remains valid.

## Isolated candidate and review/proof hold

[Agent **draft PR375**](https://github.com/banodoco/astrid-agent/pull/375), branch `p39/k1a-failure-mode-macos15-20261117`, base `6bbda788c1a62abcdda242f85c7a1cae86c57d3d`, candidate commit `58219a6360df541fabb6f04280ebbc62b0be5aad`, adds exactly one mapping line in `scripts/journey_failure_modes.py`:

```python
"macos-15": ("macos", "macOS", "macos15"),
```

No other source or tests change. This preserves the old key; no skip, xfail, test assertion, receipt validation, historical pin or product contract is loosened. The change is limited to the existing Plan 39 test/harness prerequisites. Route is **N (source diagnosis/mechanical correction)**. Actual worker model provenance was not available in this tool session and is **not invented**; the persisted run's N-role mapping remains configured but is not proof of this invocation. **No separate independent N reviewer submission or local/hosted candidate test execution exists yet; PR is deliberately draft and unmerged.**

Review must inspect M4-6 exact slot admission, whether accepting macOS 15 in the runner map unintentionally broadens a receipt (it should not alter slot-ID or hash checks), and the unchanged failure-mode security assertions. In a genuine Agent worker checkout, run the focused existing wrapper against `tests/test_journey_failure_modes.py` and `tests/test_failure_receipts.py`, capture exact candidate outcomes and any new reached assertions. After review and integration **into `release/14/plan-39` only**, re-measure actual CI unit shard 7/8 on the integrated head with XML: all 40 exact IDs must be collected, and the `KeyError` must disappear; they are **not promised to pass**. No manual workflow was dispatched, and other sessions' workflows were not cancelled or rerun.

Separate unmerged draft [PR373](https://github.com/banodoco/astrid-agent/pull/373) still requires native Windows exact-ID execution, and [PR374](https://github.com/banodoco/astrid-agent/pull/374) requires independent historic Git archive/tree proof; neither has review submissions. Separate source/ownership holds remain on Plan 38 and Plan 55 tests, the pod-bootstrap legacy-entrypoint/noneditable-vs-editable contract and the Runtime clip replay-vs-history-integrity conflict. **Plan 38/55 WAITING, Release 15 excluded; G1/G2 incomplete; RS1 0/1.** Do not edit `inputs.md` or plan task checkboxes, or promote `release/14/main` or public `main`.
