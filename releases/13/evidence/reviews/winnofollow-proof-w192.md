**Verdict: MERGE-READY for the reviewed delta**, with one shared test failure left unresolved. The merge into A″ is clean, and the completed comparisons found no test failing on C that passed on A′. This is not a native Windows or provider end-to-end validation.

The diff from A′ to C contains five files: `failure_diagnostics.py`, `pod_reset.py`, `worker_owner.py`, and the new `test_windows_controller.py` and `test_windows_credential_read.py`—194 insertions and 3 deletions. No existing test assertions changed, so none were weakened. The merge-tree check against A″ was clean; the two branches touch **no common files**.

The code read found:

- **Reset and imports.** `pod_reset.py:80` now imports `fcntl` inside `reset_lock`. The pod receives the Agent source tree in an archive (`remote_placement.py:363`) and invokes the module with `python -m` (`machine.py:248`). The reset source is **not byte-identical**: its digest changes, and import timing changes. The lock operation itself is unchanged on a Linux pod with `fcntl`. The source-digest test computes the expected digest dynamically; it does not pin a fixed `pod_reset.py` digest, and it passed on both sides. An independent import guard passed for all 21 listed controller modules with `fcntl`, `pwd`, `grp`, and `termios` unavailable. A scan of the 78 project modules loaded by that guard found no unconditional top-level imports of those modules or `resource`, and no top-level `os.fork` calls. That scan does not establish coverage of every possible lazy import.

- **Graph facts.** `failure_diagnostics.py:283` uses the portable filesystem open with no-follow and nonblocking flags. On POSIX, `runtime_protocol/dirfd.py:641` selects ordinary `os`, preserving the previous flags. A FIFO probe returned empty facts immediately. On Windows, `dirfd.py:54–56,223–273,290–318,370–372` defines nonblocking as zero, opens components without following reparse points, and rejects them. The diagnostic source is shipped to the pod as `python -c` source (`machine.py:452–454`); `failure_diagnostics.py:15–19` selects stdlib `os` when `__package__` is empty. It does **not** catch `ImportError`, so a Runtime import error during a normal packaged controller import is not hidden. The other two opens remain unchanged at `failure_diagnostics.py:333,348`.

- **Credential read.** `worker_owner.py:1543–1565` retains the early symlink refusal, no-follow open, descriptor regular-file, single-link and owner checks, and before/after and path identity checks. The path-based precheck still precedes the open, but the no-follow open protects that interval; there is no new check-to-open weakness relative to A′. A′ already imported the same portable filesystem object as `os`, so C’s final explicit `filesystem` spelling is behaviorally equivalent to A′ for this read on both platforms.

Test counts below are **A′ / C**. Counts for the interrupted machine run combine its completed cases with the resumed run, which deselected those cases.

| Test file | A′ | C |
|---|---:|---:|
| `test_windows_controller.py` | 0 passed, 4 failed | 4 passed |
| `test_windows_credential_read.py` | 2 passed, 2 failed | 4 passed |
| `test_machine.py` | 135 passed | 135 passed |
| `test_pod_reset_runtime.py` | 9 passed, 1 failed | 9 passed, 1 failed |
| `test_failure_diagnostics.py` | 66 passed after retry | 66 passed after retry |
| `test_job_on_claimed_machine.py` | 53 passed | 53 passed |
| `test_exact_release.py` | 53 passed | 53 passed |
| `test_remote_placement.py` | 16 passed | 16 passed |
| `test_pod_source_install.py` | 2 passed | 2 passed |
| `test_reset_diagnostics.py` | 27 passed | 27 passed |
| `test_generation_preparation.py` | 22 passed | 22 passed |
| `test_worker_preparation.py` | 48 passed | 48 passed |
| `test_worker_release.py` | 20 passed | 20 passed |

The integration-marked `test_remote_machine_cpu.py` cases were deselected by the wrapper’s default marker expression.

Fail-first was confirmed using scratch copies of C’s new tests against A′ product files: **6 failed, 2 passed**, versus **8 passed** on C. Four failures exercise the controller import and graph defects. The two credential-test failures are a limitation of the POSIX simulation: it patches the new `filesystem` name, while A′ uses the same adapter under its `os` alias.

Four diagnostic cases initially failed on both sides because spawned children resolved the dependency’s `tests` package. All four passed on both sides when rerun with the checkout first on `PYTHONPATH`. The remaining shared failure is `test_fresh_reset_uses_launcher_owner_authority_and_preserves_scoped_connection`: it failed on both sides, including retries, while masking the underlying `ResetError`. Its cause is unconfirmed.

The readiness budget test passed on C with **one readiness exec and zero reset starts**. Temporary worktrees, environments, and basetemps were removed; no provider call or push was made.