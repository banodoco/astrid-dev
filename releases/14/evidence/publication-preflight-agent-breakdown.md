# Provisional Agent 434-ID investigation

This examines the [original per-job ledger](publication-preflight-agent-20261121.md), using its linked existing R13 and pre-freeze candidate logs and the [source diff](https://github.com/banodoco/astrid-agent/compare/959da7326c982a9197b5d6e2a4489f45e1deef0e...0020c2e8d7f5d6051db2964a235b97f4ba002a72). No tests were run. Counts are original job/ID occurrences, not a frozen release verdict. Candidate pytest progress lines were checked as well as `-rA` summaries.

| Original job | Passing in another candidate job | Passing in same job, omitted by provisional parser | Changed test names/behavior | Changed parameter ID | Total |
|---|---:|---:|---:|---:|---:|
| unit 1 | 12 | 0 | 1 | 0 | 13 |
| unit 2 | 0 | 0 | 0 | 0 | 0 |
| unit 3 | 19 | 1 | 0 | 0 | 20 |
| unit 4 | 1 | 0 | 6 | 0 | 7 |
| unit 5 | 0 | 0 | 0 | 0 | 0 |
| unit 6 | 1 | 0 | 5 | 1 | 7 |
| unit 7 | 102 | 0 | 0 | 0 | 102 |
| unit 8 | 283 | 0 | 0 | 0 | 283 |
| integration 1 | 0 | 0 | 0 | 0 | 0 |
| integration 2 | 2 | 0 | 0 | 0 | 2 |
| integration 3–4 | 0 | 0 | 0 | 0 | 0 |
| **Total** | **420** | **1** | **12** | **1** | **434** |

- Shard movement: e.g. `tests/test_installer_update_end_to_end.py::test_refused_launch_is_reported_with_its_reason_not_as_an_os_rejection` passed in candidate unit 7 instead of R13 unit 8. The candidate progress line establishes the pass even where the summary reader missed it.
- Same-job parser omission: `tests/editing_conformance/test_native_sheet_current.py::test_explicit_clear_restores_tagged_value[None-asset]` appears as passed in candidate unit 3 progress. The original summary does not establish an omission.
- Changed tests: unit 1's interrupted download test was renamed to `test_an_interrupted_download_keeps_only_its_resumable_part`; unit 4's six TLS cases were replaced by revised verified-policy tests (e.g. `test_certificate_failure_retries_once_with_verified_context[direct]` became a one-attempt policy test); unit 6 contains one VibeComfy scan case and four baseline/structure cases with changed names and expectations. These are source changes, **not proof of equivalent coverage**; the Lead must review their intended behavior and reconcile destinations individually.
- Parameter ID: unit 6 `tests/reshape/test_compare_baselines.py::test_file_code_ratchet[1-2-0-Ratchet down available]` changed its message parameter to `IMPROVEMENT (ratchet down available)`; review its changed expectation.
- Job not run/cancelled: **0 identified**; file deleted: **0 identified**; new skip/xfail: **0 identified** among these 434. All 13 IDs not observed as passing are in files present on both revisions; the source diff accounts for their changed names or parameter. These counts do not assert that other tests or the final tuple have no such issues.
