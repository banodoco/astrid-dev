# W225 report: is the macOS Runtime shutdown race in R12's Runtime (42ae24af) or new in 6855dfa8?

## VERDICT: (a). The same race is present in R12's Runtime.

Every Runtime code path in the W224 chain (request server, stderr writers, claim route, SQLite transaction and connection settings, stop fence, grace/escalation, launchd plist and stop checks) is byte-identical between 42ae24aff8d2cb854f874ce134161077a3ba3641 (R12 pin) and 6855dfa8df65cf8ae4c002b57134d6505493c17c (R13 pin). The GitHub compare shows one commit ahead, touching two files:
- `runtime_protocol/service.py` (4 lines, output staging in `_stage_outputs`, not the claim or stop path).
- `tests/test_inline_output_proof.py` (added).

Defer the W224 failure as pre-existing R12 Runtime behaviour, not an R13 regression. The agent-side changes between R12 and R13 do not alter the claim-vs-stop ordering either (question 5).

Full SHAs: R12 Runtime is `42ae24aff8d2cb854f874ce134161077a3ba3641`, from `git -C /home/user/wt/agent-r12 show 0e1543e0:runtime.lock.json` (`source_commit`), and `astrid/resources/runtime.lock.json:71` carries the same value. R13 is `6855dfa8df65cf8ae4c002b57134d6505493c17c`.

## Method and scope

- `gh api repos/banodoco/astrid-runtime/compare/42ae24af...6855dfa8`: status ahead, 1 commit, 2 changed files (the full changed-file list, not truncated).
- `gh api repos/banodoco/astrid-runtime/contents/<path>?ref=<sha>` (raw) for 8 Runtime files at both SHAs. Fetched files: `astrid_runtime/{bootstrap,cli,runtime_boundary}.py`, `runtime_protocol/{server,store,service,services,daemon}.py`. Each one compared with `cmp`: all identical except `runtime_protocol/service.py`.
- Agent side: `git show` and `git diff` on `/home/user/wt/agent-r12` (read-only, nothing modified). R12 = `0e1543e0`, R13 = `8625a463`.
- Line numbers below are the same in both Runtime versions unless stated. The first cite is 42ae24af, the second 6855dfa8.
- Not checked: the rest of the Runtime tree outside the nine fetched files. The compare says it is identical, so this is covered by the compare, not by a grep.

## 1. `RuntimeHTTPServer` (runtime_protocol/server.py)

- `:113` `class RuntimeHTTPServer(ThreadingHTTPServer):` (42ae24af) / `:113` (6855dfa8). Same.
- `:114` `daemon_threads = True` / `:114`. Same.
- No `handle_error` override in either fetched server file. Its only `sys.stderr` writer is `_error`, below.

Identical.

## 2. `_error` and stderr from request threads

- `runtime_protocol/server.py:561-574` `_error`. For a non-`RuntimeErrorBase` exception it prints `Runtime internal error (request ...)` plus the traceback with `file=sys.stderr, flush=True` at `:573-574`. Same in both.
- `astrid_runtime/cli.py:406` `_run_foreground`. `contextlib.redirect_stdout(log), contextlib.redirect_stderr(log)` at `:421`, same in both. The redirect only covers the `with` block, so request threads that outlive it write to the real fd 2.
- `runtime_protocol/daemon.py:349,352` start `serve_forever` threads with `daemon=True`. `runtime_protocol/services.py:186,285` start the service and log-reader threads with `daemon=True`. Same in both.

Identical. The stderr path that matches the W224 traceback exists unchanged in both.

## 3. Claim path and SQLite settings

- Claim route: `runtime_protocol/server.py:1268` `if path == ["v1", "tasks", "claim"] and method == "POST":`, in both.
- `runtime_protocol/service.py:529` `with self.store._transaction():` wraps the command function, in both.
- `runtime_protocol/store.py:1198` `def _transaction`, `:1220` `self.conn.execute("BEGIN IMMEDIATE")`, in both. Identical file.
- Connection: `runtime_protocol/store.py:1514` `sqlite3.connect(self.db_path, timeout=10, isolation_level=None, check_same_thread=False)` and `:1519-1521` (same with a `file:` URI), in both.
- `:1525` `PRAGMA journal_mode=WAL`, in both.
- `:1535` `PRAGMA busy_timeout=10000`, in both. This is the existing retry-on-locked (10 s); there is no separate retry loop.
- The unrelated `store.py:1188` connection (`sqlite3.connect(sqlite_file_uri(...), uri=True, isolation_level=None)`, no timeout) is also unchanged.
- `service.py` in 6855dfa8 changes only `_stage_outputs` (`runtime_protocol/service.py:9308` in 6855dfa8, `if stage_path is None and (has_project_owner or not any(...` in place of `if has_project_owner or not any(...`). The claim route and `_transaction` are untouched.

Identical. Isolation, timeout, WAL and busy_timeout did not change.

## 4. Stop path (fence and grace)

- `astrid_runtime/bootstrap.py:1874` `def _fenced_stop_and_manager(`, in both. Fence at `:1886-1888` (`interruption_fence(realm_root)`, imported from `runtime_protocol.lifecycle` at `:33`). Identical.
- `astrid_runtime/runtime_boundary.py:53` `SERVICE_OWNER_STOP_GRACE_SECONDS = 20.0`, in both.
- `:429`, `:459`, `:968`: the grace is applied to `_runtime_stop_grace` and `shutdown_grace`, in both.
- `:854` TERM then KILL loop, `:1107` `custody.signal(platform.KILL, ...)` (escalation), `:1148` KILL signal, same line numbers in both. The brief's `~:1107` is correct.
- The fence is `interruption_fence` in `runtime_protocol/lifecycle.py`, which was not fetched. Its unchanged status is inferred from the identical compare, not read directly.

Identical.

## 5. Pack host claim loop and shutdown (R12 `0e1543e0` vs R13 `8625a463`, `astrid/core/execution/generic_host.py`)

The brief's grep (`git diff 0e1543e0 8625a463 -- generic_host.py | grep -n claim`) shows many claim-related hunks, but none changes the claim gate or the SIGTERM ordering:
- Claim gate `_handoff_enter_claim_rpc`: `:6847` (R12) / `:7080` (R13). Same body (returns False when `_handoff_claim_gate_closed` or observation unknown; otherwise increments the in-flight counter).
- Claim-loop entry: the claim function checks `self._shutdown.is_set()` at `:13781` (R12) / `:14130` (R13), and the `claim_next(...)` call is at `:13819` (R12) / `:14168` (R13). The serve loop guard `while not self._shutdown.is_set()` is at `:14027` (R12) / `:14684` (R13), and the inner `while not self._shutdown.is_set():` at `:14219` (R12) / `:14878` (R13), same semantics.
- Host shutdown `def shutdown` at `:7195` (R12) / `:7423` (R13). It sets `self._shutdown` first, closes warm holds, and fences all claim slots before releasing sessions, in both. R13 adds one line, `:7435 self._local_engine_idle.close()` (when this host owns the accounting), before slot shutdown. This does not touch the claim gate or the Runtime fence.
- SIGTERM handler `_handle_host_shutdown_signal`: `:17376` (R12) / `:18040` (R13), same body, logs `generic host shutdown requested: signal=%d`, then calls `host.shutdown()`. `_ManagedStdinShutdown` at `:17399` / `:18063`, same.
- Other claim-hunk changes (blocked-claim reporting `_reported_blocked_claims`, RunPod claim recorder, `_CLAIM_HEAD_OF_LINE_SKIPS = 8` at `:4438` in R12) do not change when a host stops claiming.

Answer: the claim loop's behaviour at shutdown did not change. R13's host still sets `_shutdown` and stops claiming before the Runtime fence, as R12's does.

## 6. launchd side (`astrid/installer/service.py`)

- `git diff --stat 0e1543e0 8625a463 -- astrid/installer/service.py` is empty. The file is identical.
- `:470-472` `KeepAlive: {SuccessfulExit: False}`, `ExitTimeOut: 90` (R12 and R13).
- `:596` and `:828` `The launchd service did not remain stopped after Runtime exit.` (R12 and R13).
- `:1194-1222` bootout, gated on the Runtime C1 stop callback (R12 and R13).

Identical.

## Compare summary

| item | 42ae24af (R12 Runtime) | 6855dfa8 (R13 Runtime) | changed? |
|---|---|---|---|
| RuntimeHTTPServer bases / daemon_threads | server.py:113-114 | server.py:113-114 | no |
| _error stderr print | server.py:561-574 | server.py:561-574 | no |
| cli redirect | cli.py:406, 421 | cli.py:406, 421 | no |
| claim route | server.py:1268 | server.py:1268 | no |
| _transaction BEGIN IMMEDIATE | store.py:1198, 1220 | store.py:1198, 1220 | no |
| sqlite connect / busy_timeout | store.py:1514-1521, 1525, 1535 | same | no |
| stop fence | bootstrap.py:1874, 1886-1888 | same | no |
| stop grace / KILL | runtime_boundary.py:53, 429, 459, 854, 968, 1107, 1148 | same | no |
| service.py (the one changed file) | not on claim or stop path; `_stage_outputs` at service.py:9308 | changed hunk | yes, output staging only |

## Did anything between the two Runtimes make the stop fence or the claim-vs-fence contention more likely?

No evidence in the code I read. The only Runtime change is in output staging (`_stage_outputs`, `runtime_protocol/service.py:9308` in 6855dfa8), which is not the claim transaction or the fence. The new condition skips the authorization query when `stage_path` is set, so it does less work on that path. Whether the settle path holds `BEGIN IMMEDIATE` longer or runs more often at shutdown was not measured, so that is unproven and does not change the verdict.

## What is still missing (not changed by this compare)

- The exact request that raised the `handle_error` traceback in the W224 run is still unknown.
- The `interruption_fence` implementation (`runtime_protocol/lifecycle.py`) was not fetched.
- Repo-wide grep for `handle_error` and extra stderr writers was limited to the nine fetched files. The compare shows nothing else changed.
- No R12 macOS run of the same uninstall exists in this session. The race is shown present in the code, not reproduced in R12.

Mitigations from W224 apply to both Runtime pins: join or quiesce request threads before the redirect exits, make `_error` safe at finalization, or make the installer retry a respawn after `down`. These are Runtime-side changes, not an R13 regression fix.

Scratchpad copies of the fetched files: `/tmp/claude-0/-home-user/b383ba57-32bc-5b5c-97e8-e4e7807998d3/scratchpad/w225/a/` (42ae24af) and `/tmp/claude-0/-home-user/b383ba57-32bc-5b5c-97e8-e4e7807998d3/scratchpad/w225/b/` (6855dfa8). Agent-side copies: `.../w225/gh_0e1543e0.py` and `.../w225/gh_8625a463.py`.
