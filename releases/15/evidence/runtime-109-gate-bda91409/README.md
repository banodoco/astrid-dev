# Runtime #109 gate: save branch into Runtime `release/15/main`

Date: 23 November 2026. Gate by the Release 15 Lead.

- **Candidate:** astrid-runtime `release/15/plan-77-save` at `bda914099d670b60ee8dc51ac26891daed81874f` (Plan 89 SV-2d, SV-2b, SV-2, SV-2f and SV-2g), CI run [45253631980](https://github.com/banodoco/astrid-runtime/actions/runs/45253631980).
- **Base:** `737843e9cb92c565c266452dde540832ee2c745b`, CI run [45158253276](https://github.com/banodoco/astrid-runtime/actions/runs/45158253276) attempt 2 ([baseline](../runtime-ci-baseline-737843e9/)).
- **Method:** each job's full log fetched, then the failing and erroring ids from its last short test summary were extracted with [cmp.py](cmp.py) and compared as sets. Per job, failed plus errors on the totals line equals the id count.

| Job | Base ids | Candidate ids | New | Gone | Candidate totals |
|---|---:|---:|---:|---:|---|
| unit (ubuntu) | 478 | 478 | 0 | 0 | 111 failed, 9348 passed, 26 skipped, 13 xfailed, 367 errors |
| unit (macOS) | 477 | 477 | 0 | 0 | 110 failed, 9245 passed, 130 skipped, 13 xfailed, 367 errors |
| sandbox-process-control | 495 | 495 | 0 | 0 | 124 failed, 9255 passed, 26 skipped, 13 xfailed, 371 errors |
| portability-lifecycle (ubuntu) | 7 | 7 | 0 | 0 | 7 failed, 610 passed, 45 skipped |
| portability-lifecycle (macOS) | 8 | 8 | 0 | 0 | 8 failed, 595 passed, 59 skipped |

The other jobs (typescript-client, boundary, windows-realm-publication, darwin-native) succeed on both runs. Landing reference succeeds on the candidate; it was skipped on the base.

**History.** An earlier head failed `tests/test_timeline_headless_overwrite_refused.py::test_original_trackless_authored_payload_with_verified_media_is_invalid_untouched` in the sandbox job, twice, while the base passed it on a re-run. The save run bisected the failure to SV-2f (#106). SV-2g (#111) fixes it and was merged into the candidate as `bda91409`; the test passes here.

**Verdict:** gate confirmed. No failing id is new or gone in any job.
