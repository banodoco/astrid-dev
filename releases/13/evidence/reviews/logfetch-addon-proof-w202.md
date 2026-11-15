**Verdict: findings.** The requested tests show no candidate-only regression, and the fixes close the reproduced pre-existing nested-symlink and malformed-size cases. Three limitations remain: a symlinked destination root loses its logs, a concurrent directory swap can redirect an installation, and an ownerless adapter without a bounded transport can exceed the calculated deadline. These are not classified as BLOCK under the card’s stated threshold.

The diff from `51971b0e2` to `4eb67605d` changes two files, with **95 insertions and 10 deletions**:

- `astrid/packs/runpod/machine.py`: ownerless adapter handling, size validation, and destination checks.
- `tests/packs/runpod/test_success_logs.py`: eight new parametrized test cases. **No existing assertion changed.**

`git merge-tree --write-tree 3d8c1d8d9 4eb67605d` was clean, producing tree `089c815b8f4ffe84ae51700d8a90d136b2af8e74`. A scratch merge also completed cleanly.

**Code read**

- **Deadline and owner:** [`machine.py:1111–1129`](https://github.com/banodoco/astrid-agent/blob/4eb67605d36b2f2975f6ee29230055161df46cb8/astrid/packs/runpod/machine.py#L1111-L1129) uses `getattr` for the owner. With a bounded transport, the deadline is the earliest applicable paid, job, or existing transport deadline, less the 15-second margin, capped at 60 seconds. If the owner and `bounded()` are both absent, the computed deadline is not applied to the transport. The success-log scope has no other unguarded owner read, but the wider fetch path still has unguarded reads in `_checkpoint`, `_checkpoint_installed`, and failure-log collection at lines 1778, 1361, and 1141. The ownerless acceptance double stubs the checkpoint methods.
- **Destination:** [`machine.py:1293–1318`](https://github.com/banodoco/astrid-agent/blob/4eb67605d36b2f2975f6ee29230055161df46cb8/astrid/packs/runpod/machine.py#L1293-L1318) checks the destination itself and each component through the log’s parent with `lstat`, then compares the resolved parent with the resolved destination. The root is the fetch destination, normally the attempt’s `outputs` directory. A symlink at that root is refused, even if it is a legitimate user output directory. Checks and `replace` are separate operations; a concurrent swap can redirect the final write.
- **Windows:** The diff adds no `O_NOFOLLOW`, `fchmod`, `fcntl`, or other POSIX-only primitive. It checks only `S_ISLNK`, not Windows reparse tags. Python’s `lstat` opens name-surrogate reparse points without following them, but junctions are not identified by `S_ISLNK`; the resolved-parent containment check can refuse a junction leading outside the root. A junction resolving inside it can pass. This was a code and documentation assessment, not a Windows execution test. [Python filesystem documentation](https://docs.python.org/3.13/library/os.html), [Python reparse-point behavior](https://github.com/python/cpython/blob/main/Doc/whatsnew/3.8.rst).
- **Size:** [`machine.py:1285–1291`](https://github.com/banodoco/astrid-agent/blob/4eb67605d36b2f2975f6ee29230055161df46cb8/astrid/packs/runpod/machine.py#L1285-L1291) accepts only exact integers from zero through 256 MiB. It excludes `True`, floats, strings, `None`, missing values, and negatives. Zero permits a downloaded, digest-verified empty log. After download, both digest and actual size must match the manifest at lines 1243–1254. The pre-request rule does **not** limit actual streamed bytes if a manifest understates the size; the mismatch is detected afterward.

**Local simulations**

| Case | Result |
|---|---|
| Symlink at `logs/a` or deeper at `logs/a/b` | `unsafe_destination`; log requested and staged first; nothing written outside |
| Top-level `logs` symlink | `unsafe_destination`; no log request |
| Destination root symlink | `unsafe_destination`; log requested, then refused |
| Directory swapped to a symlink after the resolved-parent check | Verified log installed outside the destination |
| Missing, `None`, `-1`, `"12"`, `1.5`, `True` | `invalid_size`; no log request |
| `0` | Requested and empty verified log installed |
| 256 MiB | Requested; deliberately short response rejected as `DigestMismatch` |
| 256 MiB + 1 | `too_large`; no log request |
| Stalled bounded transfer | Candidate test passed: deadline enforced, child reaped, release and reset observed |
| Cancellation during transfer | Candidate test passed: cancellation propagated and no staged partial remained |
| Ownerless transport without `bounded()` | A 0.3-second transfer completed despite a calculated approximately 0.05-second budget |

**Paired tests**

Each requested file ran separately using the worker setup and pytest wrapper, with the checkout added to `PYTHONPATH` and no more than two pytest processes.

| File | B | C |
|---|---:|---:|
| `test_success_logs.py` | 22 passed | 30 passed |
| `test_declared_logs_e2e.py` | 2 passed, 1 failed | 3 passed |
| `test_machine.py` | 135 passed | 135 passed |
| `test_job_on_claimed_machine.py` | 53 passed | 53 passed |
| `test_exact_release.py` | 53 passed | 53 passed |
| `test_failure_logs.py` | 6 passed | 6 passed |
| `test_failure_diagnostics.py` | 66 passed | 66 passed |
| `test_remote_placement.py` | 16 passed | 16 passed |
| `test_host_log_outputs.py` | 11 passed | 11 passed |
| `test_generic_host_result_json.py` | 26 passed, 1 failed | 26 passed, 1 failed |
| `test_job_logs_script.py` | 4 passed | 4 passed |
| `test_job_logs_fetch.py` | 4 passed | 4 passed |
| `test_host_checkpoint_evidence.py` | 21 passed | 21 passed |
| **Total** | **419 passed, 2 failed** | **428 passed, 1 failed** |

There were **no IDs failing on C that passed on B**. The shared failure was `test_request_digest_does_not_depend_on_attempt_or_materialized_paths`, whose fixture is rejected for missing `admitted_source_digest`. B alone failed the declared-log success acceptance case.

Fail-first, using C’s success-log test file against B product files, produced **8 failed, 22 passed**. The failures were:

- `test_success_logs_refuse_nested_symlink_destination`
- `test_success_logs_invalid_size_request_budget[missing]`, `[negative]`, `[string]`, `[float]`, and `[bool]`
- `test_success_log_deadline_without_lease_owner[20-1005]` and `[300-1060]`

`make cycles` passed on C and the scratch compose merge; `ruff check` passed on both changed files. The requested worktrees, environments, and basetemps were removed. No provider call or push was made.