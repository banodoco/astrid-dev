**Verdict: MERGE-READY**, with a Windows durability limitation and a separate later worker-path issue noted below. No candidate-only test failures were found. The security API and crash behavior were reviewed in code but were not exercised on native Windows.

The full diff from A′ `f709407cb` to C `a08cdd7c8` contains:

- `astrid/core/execution/generic_host.py`: 4 lines changed.
- `astrid/packs/runpod/provider.py`: 7 lines changed.
- `astrid/packs/runpod/release_control.py`: 9 lines changed.
- `tests/packs/runpod/test_windows_claim_state.py`: 196 lines added.

No existing test assertions were changed or weakened.

**Code read**

- Windows `owner_only(fd)` calls `windows_security.restrict` (`runtime_protocol/platform.py:98`; `windows_security.py:230`). It reopens the handle with `READ_CONTROL | WRITE_DAC`, checks ownership, and uses `SetSecurityInfo` to install a protected DACL granting full access to the current token user and SYSTEM (`windows_security.py:130`, `:136`, `:218`). A valid descriptor can still raise, including if reopening, ownership validation, or setting the DACL fails. After a successful restriction, validation is run on the same handle; `is_owner_only` should accept it when subsequently opened with sufficient rights (`platform.py:114`; `windows_security.py:166`). This was not verified with native Windows APIs. `msvcrt` and Win32 library loading are inside functions; the helper has no top-level Windows-only module import that prevents POSIX import.
- POSIX release control remains private: `owner_only` applies `0600` (`platform.py:104`), while `request_release` retains the UID and regular-file checks and uses `O_NOFOLLOW` where available (`release_control.py:174`). The descriptor is closed on the relevant failure paths (`release_control.py:112`, `:192`). The generic-host replacement likewise applies `0600` on POSIX (`generic_host.py:317`).
- Gate publication still flushes the file, calls `os.replace`, then syncs the directory on POSIX (`provider.py:184`; `platform.py:184`). On Windows the directory sync is a no-op; `os.replace` also lacks `durable_replace`’s write-through move and sharing-violation retry (`platform.py:159`, `:173`, `:195`). A crash can leave an older valid gate or alias record and bypass a newer pacing interval or Retry-After cooldown; an unreadable or missing initialized record instead gets a 60-second recovery cooldown (`provider.py:254`, `:295`, `:320`). This is a pacing limitation, not a spending-ceiling check: paid authority, hourly ceiling and USD cap are separately checked in `target_selection.py:352` and `:381`. A transient sharing violation can also make publication fail.
- The by-name import keeps the intent-flush test meaningful. The test patches `worker_preparation.platform.fsync_directory`, and exclusive intent creation calls that attribute after flushing the intent (`test_target_selection.py:414`; `worker_preparation.py:168`). The gate uses its independently bound name (`provider.py:10`, `:197`), so it does not consume the injected failure first. The test passed on both sides.
- The search found **no other unguarded POSIX-only calls on the traced local claim construction and account-gate binding path**. The watchdog’s `fcntl` and directory fsync execute in the transported pod program (`pod_watchdog.py:22`, `:142`, `:260`). Separately, the later managed remote-worker activation path has an unguarded `os.O_NOFOLLOW` in `_read_credential` (`worker_owner.py:1540`, called at `:2351` and `:3179`); it would fail on Windows if that path is used. I did not establish that it is reached by the claim operation reviewed here.

**Tests**

Each side used its setup script and one pytest process at a time. Counts below are A′ / C.

| Test file | A′ | C |
|---|---:|---:|
| `test_target_selection.py` | 101 passed | 101 passed |
| `test_provider_gate.py` | 11 passed | 11 passed |
| `test_provider_gate_durability.py` | 13 passed | 13 passed |
| `test_provider_gate_entrypoints.py` | 9 passed | 9 passed |
| `test_provider_gate_release.py` | 6 passed | 6 passed |
| `test_provider_gate_review.py` | 9 passed | 9 passed |
| `test_provider_gate_selection_binding.py` | 2 passed | 2 passed |
| `test_acquisition_gates_provider_fields.py` | 33 passed | 33 passed |
| `test_release_control.py` | 6 passed | 6 passed |
| `tests/test_generic_host_result_json.py` | 26 passed, 1 failed | 26 passed, 1 failed |
| `tests/test_generic_host.py -k 'terminal or request'` | 18 passed, 292 deselected | 18 passed, 292 deselected |
| New Windows claim-state test | 3 passed, 7 failed | 10 passed |

The common failure is `test_request_digest_does_not_depend_on_attempt_or_materialized_paths`; it failed on both sides. No test passed on A′ and failed on C.

For fail-first, C’s new test file was copied to scratch and run against A′ product files. The failures were both `[zero]` and `[absent]` variants of `test_windows_lease_owner_setup_budget`, `test_windows_account_binding_and_pacing_budget`, and `test_windows_unbound_pacing_state`, plus `test_windows_terminal_request_persistence_needs_no_fchmod`. All seven pass on C.

The standalone Linux simulation deleted `os.fchmod`, forced `O_DIRECTORY` to zero, denied directory opens, and created a release server and fresh gate state successfully. It stubbed Windows DACL restriction, so it proves the simulated control flow rather than actual Windows permissions. No provider call was made.

The detached worktrees, environments, scratch files and basetemps were removed. No tracked files were edited and nothing was pushed.