**Verdict: BLOCK.** A slow optional log fetch can still delay a completed generation past its execution or paid deadline, or delay cancellation, before normal release and reset. The success fetch has no per-log or aggregate deadline and does not use the cancellable transport scope. The independent paid-expiry timer can initiate release, so this does not establish indefinite billing; expiry can nevertheless race the post-fetch custody checkpoint and fail the completed generation.

The fetched candidate is one commit on A′. The full diff contains:

- `astrid/packs/runpod/machine.py`: optional staged success-log fetches.
- `astrid/core/execution/generic_host.py`: copies `logs_unavailable` into machine metadata.
- `tests/packs/runpod/test_success_logs.py`: eight new tests.

No existing tests or assertions changed.

**Code read**

- **Outputs and classification.** `machine.py:1190–1233` verifies the manifest digest, then fetches non-`logs` members first, checking each downloaded digest and size and propagating failures. Classification is solely the first path component being exactly `logs`: an actual generated output under `logs/` is treated as optional. A local probe confirmed that a failed `logs/render.png` fetch returns success from the fetch helper. Later host validation can still reject a missing required artifact; that probe did not establish an end-to-end successful task with a missing artifact.
- **Paths and symlinks.** `logs/../x` reaches the path check at `machine.py:1203–1206`, but its `DigestMismatch` is caught as an unavailable log at `1220–1230`, so it does not fail the manifest. The remote manifest generator skips symlink files (`remote_placement.py:391–401`). The local destination check does not reject symlinked parent directories: a probe with an existing symlinked `logs` directory installed a verified log outside the destination. This requires a pre-existing local symlink.
- **Partial logs, time and cancellation.** Logs stage under `TemporaryDirectory` and are digest- and size-checked before `replace` (`machine.py:1223–1227`). Normal cleanup removes partial staged files. A successful replace overwrites an existing destination; a failed fetch leaves any old destination file in place. Cleanup or cross-filesystem replacement can itself fail and is recorded as unavailable. The deadline is checked only before collection (`machine.py:1082–1086`); release follows fetch (`machine_run.py:121–137`). The underlying HTTPS client uses 1 MiB chunks, a 20-second request timeout and retries, but no total download bound. A stalled or slowly progressing 256 MiB log has no finite overall bound before normal release. Poll uses a cancellable scope (`machine.py:951–956`); fetch does not. The independent paid-expiry timer is at `worker_owner.py:1372–1405`.
- **Failure path.** The failure-path collection call and its behavior are unchanged in the diff (`machine.py:1056–1064`, `1146–1173`). Its shared verifier is called without the new optional-log argument, so it retains fail-closed handling.
- **Manifest and size checks.** Non-log members still receive path, digest and size checks (`machine.py:1190–1212`). Log members receive the same checks before installation, but failures—including unsafe paths—are suppressed into metadata. The 256 MiB cap applies during log collection (`run_logs.py:26`, `190–259`); the success fetch does not enforce that cap against manifest entries before downloading.
- **Metadata and consumers.** Values contain exception type names, not exception messages, but keys are unsanitized manifest paths and can contain user names or other sensitive text (`machine.py:1229–1230`). `generic_host.py:7570–7573` attaches the mapping to machine metadata, which is copied into the receipt and task result (`11514–11515`, `13632–13633`); `tasks show` displays the task response (`domain_tasks.py:228–233`). Failure receipts separately use a `logs_unavailable` field for a single failure reason (`failure_receipt.py:296–305`).

**Tests**

Counts are A′ / candidate. Each invocation ran sequentially with the worker environment. The requested `tests/core/execution/test_generic_host_result_json.py` path is absent on both sides; the actual `tests/test_generic_host_result_json.py` was tested instead.

| File | A′ | Candidate |
|---|---:|---:|
| `test_success_logs.py` | absent | 8 passed |
| `test_machine.py` | 135 passed | 135 passed |
| `test_job_on_claimed_machine.py` | 53 passed | 53 passed |
| `test_exact_release.py` | 53 passed | 53 passed |
| `test_failure_logs.py` | 6 passed | 6 passed |
| `test_declared_logs_e2e.py` | 3 passed | 3 passed |
| `test_failure_diagnostics.py` | 66 passed | 66 passed |
| `test_remote_placement.py` | 16 passed | 16 passed |
| `test_host_log_outputs.py` | 11 passed | 11 passed |
| `tests/test_generic_host_result_json.py` | 26 passed, 1 failed | 26 passed, 1 failed |
| `test_job_logs_script.py` | 4 passed | 4 passed |
| `test_host_checkpoint_evidence.py` | 21 passed | 21 passed |
| `test_job_logs_fetch.py` | 4 passed | 4 passed |
| `test_remote_machine_cpu.py`, requested default invocation | 24 deselected | 24 deselected |
| Same integration file, two selected local-double journeys | 2 passed, 22 deselected | 2 passed, 22 deselected |

The common failure was `test_request_digest_does_not_depend_on_attempt_or_materialized_paths`: its delegated-child fixture lacks the required admitted source digest. **Candidate-only failing IDs: none. Weakened assertions: none.** An additional full integration-lane attempt was interrupted after six baseline cases passed; it was not a completed suite.

Fail-first against a scratch A′ copy produced **5 failed, 3 passed**. The failing IDs were `test_completed_job_log_fetch_budget` with `timeout`, `digest`, `size`, and `None`, plus `test_host_records_successful_job_logs_unavailable`. All three `test_completed_job_output_failure_still_fails` cases passed.

**Fault simulations**

These exercised the fetch helper locally, with one valid output and no provider calls; metadata below is the helper’s returned mapping, not a full task receipt.

| Fault | Outcome | Files left | `logs_unavailable` |
|---|---|---|---|
| Log timeout after partial write | Success | Verified output and scratch manifest; no log | `{"logs/engine.log": "TimeoutError"}` |
| Wrong log digest | Success | Verified output and scratch manifest; no log | `{"logs/engine.log": "DigestMismatch"}` |
| ENOSPC during staged log write | Success | Verified output and scratch manifest; no log | `{"logs/engine.log": "OSError"}` |
| Output timeout after partial write | `TimeoutError` | Partial output and scratch manifest | Empty; no successful result returned |

The detached worktrees, scratch copy, environments and basetemps created for this review were removed. No provider calls or pushes were made.