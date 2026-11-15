# W224 report: macOS Runtime "Fatal Python error: _enter_buffered_busy" at uninstall

VERDICT: (b). The Fatal line belongs to the Runtime daemon process (launchd job haus.astrid.runtime, pid 6464). Nothing the agent changed between 37bd5e06 and 8625a463 writes to that process's stderr. The new astrid.host_startup_timing print does not explain it. Cause: an existing Runtime shutdown race in the pinned Runtime 6855dfa8. A daemon HTTP request-handler thread writes to the real stderr while the interpreter finalizes. Remaining unproven: the exact request, and the abort versus Killed:9 timing (see "What is missing").

Paths: R = /home/user/wt/r13-tests/runs/w221/macos-fresh-43747941639. Agent code was read with `git show 8625a463:<path>`. Runtime code was read from the 6855dfa8 tarball, extracted to /tmp/w224/rt. No tracked file was changed.

## 1. Which process emitted the Fatal error

It was the Runtime daemon, not the pack host. The launchd job is:
- Label haus.astrid.runtime.
- Program `.../versions/8625a463-6855dfa8-b162bfde/py/bin/python -X utf8 -I -c <prelude> ... from astrid_runtime.cli import main; sys.exit(main(['run','--profile','astrid',...]))`.
- Source: `R/after-cleanup/unit-file-before-cleanup.txt:69-76` and the last lines of the prelude.
- StandardOutPath and StandardErrorPath are both `.../Library/Logs/Astrid Runtime/runtime-service.log` (`unit-file-before-cleanup.txt:309-312`, installer `astrid/installer/service.py:474`).

The file with the Fatal line:
- The harness copies runtime-service.log into three evidence names (see `scripts/ci_journey.py:797-800`). `runtime-service-native.log`, `...launchd-haus.astrid.runtime-stderr.log` and `...-stdout.log` are byte-identical (`cmp` says same, 387 bytes each).
- `R/after-cleanup/macos-file-listing.txt:68` shows runtime-service.log at 387 bytes.
- The log is 0 bytes in `R/before-cleanup/` (`runtime-service-native.log`). The Fatal was therefore written between the before-cleanup and after-cleanup captures, which is the final uninstall.

The full 387 bytes, with the first line exactly 40 dashes:
```
----------------------------------------
Fatal Python error: _enter_buffered_busy: could not acquire lock for <_io.BufferedWriter name='<stderr>'> at interpreter shutdown, possibly due to daemon threads
Python runtime state: finalizing (tstate=0x0000000104b5f7a8)

Current thread 0x000000020017a300 (most recent call first):
  <no Python frame>

Extension modules: yaml._yaml (total: 1)
```

Evidence for the Runtime daemon (pid 6464):
- The launchctl print in `R/before-cleanup/manager-state-before-cleanup.json` shows `state = running`, `pid = 6464`, `runs = 1`, `last exit code = (never exited)`.
- The same print after cleanup (`R/after-cleanup/manager-state-after-cleanup.json`, also `install.log:1878-1886`) shows `pid = 7992`, `runs = 2`, `immediate reason = semaphore` (KeepAlive respawn), `last terminating signal = Killed: 9`, `state = running`.
- So pid 6464 died by SIGKILL and launchd respawned it as 7992. That is what `service.py:828` reports as "did not remain stopped after Runtime exit" (the plist has `KeepAlive: {SuccessfulExit: False}`, `service.py:471-472`).
- The Runtime stops its owner with SIGTERM, waits 20 s (`SERVICE_OWNER_STOP_GRACE_SECONDS = 20.0`, Runtime `astrid_runtime/runtime_boundary.py:53`, `:968`), then SIGKILL (`:1107`, `:1148`). The "Killed: 9" fits that escalation. The respawn is the failure.

Why it is not the pack host:
- The pack host (`python -m astrid.core.execution.generic_host --service`, `astrid/services.py:140`) is spawned by the Runtime supervisor with `stdout=PIPE, stderr=STDOUT` (Runtime `runtime_protocol/services.py:268`). A reader thread copies it to service-pack-host.log (`:285`).
- So the host's fd 2 is a pipe and cannot reach runtime-service.log.
- `R/after-cleanup/service-pack-host.log` has no Fatal. It ends at line 455: `generic host shutdown requested: signal=15 reason=SIGTERM`. That is the second host, pid 6469, a child of 6464 (`service-pack-host.log:452`).
- The chat service is bun (service-chat.log, 82 bytes).

Runtime-side log lines (`R/after-cleanup/runtime-service-runtime.log`, which is runtime.log, 3795 bytes versus 2334 in before-cleanup):
- Second instance 3008db93..., source `...8625a463-6855dfa8-b162bfde`.
- Last item: `Runtime internal error (request request-ce68c07a08f54910bf53b06b727c7643, POST /v1/tasks/claim)`. The traceback runs `server.py:1555 _dispatch -> _route (1273) -> service.py:529 wrapped -> store._transaction (store.py:1220) self.conn.execute("BEGIN IMMEDIATE") -> sqlite3.OperationalError: database is locked`.
- before-cleanup has 0 "database is locked" lines and after-cleanup has 1, so it also happened during the final uninstall.
- It is a pack-host claim POST handled by a Runtime request thread. The SQLite fence taken by Runtime down (`bootstrap.py _fenced_stop_and_manager`) contends with it.
- The pack host got its second SIGTERM at the same time (`service-pack-host.log:455`).

Strongest identification, the first line of the log:
- The 40-dash line is the first print of `socketserver.BaseServer.handle_error` (`print('-'*40, file=sys.stderr)`, then "Exception occurred during processing of request from ...", then the traceback, then another 40 dashes).
- Only the first line made it out. The next write never completed, and CPython then died finalizing with the stderr lock held.
- No Runtime class overrides `handle_error` (grep over 6855dfa8 finds none). The Runtime's request server is `RuntimeHTTPServer(ThreadingHTTPServer)` with `daemon_threads = True` (Runtime `runtime_protocol/server.py:113-114`).
- The process also loaded exactly one third-party extension module, `yaml._yaml`. The Runtime daemon loads it through `load_timeline_commit_provider` (`runtime_protocol/timeline_commit_provider.py:79`, called from `daemon.py:291`) importing `astrid.sdk.timeline.commit`.
- I confirmed with an import test against the 8625a463 source: `import astrid.sdk.timeline.commit` pulls in `yaml` through `astrid.core.pack.canonical`.
- Neutral `astrid_runtime`/`runtime_protocol` code never imports yaml itself.

## 2. Does the generic host's stderr go to the Runtime's launchd stderr file? No.

- The supervised service row is `astrid/services.py:140` (pack-host, `restart: always`, ready file generic-host.ready.json, timeout 300).
- The Runtime supervisor launches it with stdout=PIPE and stderr=STDOUT (Runtime `runtime_protocol/services.py:268`).
- The log file is `RotatingLog(self.logs / ("service-" + item.spec.name + ".log"))` (`services.py:394`), which is `Library/Logs/Astrid Runtime/service-pack-host.log`.
- The launchd plist (`astrid/installer/service.py:474`) points only the Runtime itself at runtime-service.log.
- Evidence: all 40 `astrid.host_startup_timing` rows are in `R/after-cleanup/service-pack-host.log` (grep count 40). They are absent from runtime-service.log, which holds only the Fatal.
- The host's own `_cli` runs in the same process as `--service` (`run_pack_host_foreground`, `astrid/sdk/host_bootstrap.py:2582-2594`, which calls `_cli()` after chdir). It never re-execs with an inherited stderr.
- The host launched by `ensure_pack_host` in a non-foreground SDK start uses `log_path = runtime_support/generic-host.log` (`host_bootstrap.py`, near the popen_owned_group call). That path is not used for the supervised service.

## 3. `_emit_startup_phase`

Location and enable logic (`astrid/core/execution/generic_host.py` at 8625a463):
- `_STARTUP_OBSERVATION_ENABLED` is set at `:78-80`: `__name__ == "__main__"` and `--ready-file` or `--service` in argv.
- `_emit_startup_phase` is `:99-134`. The new print is `:117-118`: `print(json.dumps({...}), file=sys.stderr, flush=True)`. It is guarded by `_STARTUP_TIMING_SEEN`, so each phase prints once per process.
- `_cli` also sets the flag if `--ready-file` is present (`:18144-18146`).
- `ensure_pack_host` sets the flag when `_foreground` (`astrid/sdk/host_bootstrap.py:2110-2111`). That is only reached from `run_pack_host_foreground`, which only runs in the `--service` pack-host process (`astrid/services.py:178-188`).

Call sites:
- All are linear startup checkpoints on the main thread: `:136`, `:18037`, `:18207`, `:18430`, `:18443`, `:18496`, `:18511`, `:18601`, `:18603`, `:18610`, `:18612`, `:18616`, `:18648`, `:18717`. The `bootstrap_*` ones are in `host_bootstrap.py` `ensure_pack_host`.
- `:8381-8386` (`preflight_begin`/`preflight_done`) are inside the registration function. The first call happens in the main thread through `host.register()` (`:18616`). The seen-set suppresses any later call from a renewal thread.
- None of these are invoked from a `threading.Thread(daemon=True)`. The daemon threads in generic_host.py are the heartbeat pump (`:12241`), publication owner, serve workers, host-control and native-engine threads. None emits a startup phase.
- No emission can occur at shutdown: after `ready_written` every phase is already in the seen set.

Runtime process: the emission never happens there.
- The Runtime daemon imports neither `astrid.core.execution.generic_host` nor `astrid.sdk.host_bootstrap`. Grep of Runtime 6855dfa8 finds generic_host only as argv strings for spawned subprocesses. Its only astrid import is `astrid.sdk.timeline.commit`, which does not import generic_host.
- A `down` process imports `astrid.services` via `selected_source.py:59`. That `down` CLI process does not touch `_STARTUP_OBSERVATION_ENABLED`, since `__name__` is not `__main__` and `_foreground` is never set.
- Passing receipts with the timing code show the same 40 rows and no Fatal. See question 5.

## 4. Other stderr writers between 37bd5e06 and 8625a463

`git diff --stat 37bd5e06 8625a463` shows 62 files, +4519/-164. I grepped the added lines of the non-test diff for `sys.stderr`, `print(`, `faulthandler`, `StreamHandler`, `atexit`, `daemon=` and `threading.Thread`.

Only one new stderr writer in runtime code:
- The `astrid.host_startup_timing` print (`generic_host.py:117`).

Other hits:
- `astrid/installer/cli.py`: `print(f"{type(failure).__name__}: {failure}")` goes to stdout, in the installer CLI process.
- `scripts/ci_windows_install_guard.py` prints `::error ...`, CI-only on Windows.

No added faulthandler, StreamHandler, atexit or daemon thread anywhere. No changes to `astrid/installer/service.py`, `astrid/services.py`, `network_broker.py` or `installer/core.py` (empty diffstat). The `backend.py`/`cli.py` diffs only add `require_git` and error-text changes, not stop or launchd logic.

37bd5e06 already had the private-fd diagnostic. It wrote only via `os.write(2, ...)` when fd 2 is an owner-only regular file, so it was a no-op under a pipe. The Windows-merge change added only the extra `print(..., file=sys.stderr)` to the pack host's pipe.

Pinned Runtime shutdown behavior (all in 6855dfa8, unchanged by the agent):
- `astrid_runtime/cli.py:406-440` (`_run_foreground`): `contextlib.redirect_stderr(log)` only wraps the run. sys.stderr reverts to the real fd-2 BufferedWriter after the with block, then the process exits.
- `runtime_protocol/server.py:113-114` (`RuntimeHTTPServer`, `daemon_threads = True`) means request threads are not joined. `server.py:561-574` (`_error`) prints the traceback with `file=sys.stderr, flush=True` from those daemon threads. The default `socketserver.handle_error` prints to stderr too. `server.py:145` and `services.py:186` start daemon reaper and service threads as well.
- A handler thread that calls `print(..., flush=True)` on the real stderr during `Py_FinalizeEx` can be frozen while holding the BufferedWriter lock. The main thread's final stderr flush then aborts with exactly the `_enter_buffered_busy` message.

## 5. Verdict and supporting comparison

Verdict is (b): an old Runtime shutdown race.
- Writer: a daemon request-handler thread of `RuntimeHTTPServer` in the Runtime process (named `Thread-N`, a ThreadingMixIn per-request thread). It was inside `socketserver.BaseServer.handle_error` after an exception escaped `RuntimeHandler._dispatch`, probably the POST /v1/tasks/claim request that failed with "database is locked".
- It wrote to the real sys.stderr after `_run_foreground` restored it. The traceback from `_error` (`server.py:574`) landed in runtime.log while the redirect was still active.

Comparison of macos-fresh receipts, all with Runtime 6855dfa8:

| receipt | agent | timing rows | "database is locked" | Fatal | result |
|---|---|---|---|---|---|
| 43725021701 | 91b60416 | 0 | 0 | 0 | passes |
| 43728710873 | 37bd5e06 | 0 | 0 | 0 | passes |
| 43729191295 | 37bd5e06 | 0 | 0 | 0 | passes |
| 43751138054 | 8625a463 (rerun) | 40 | 0 | 0 | passes |
| 43751148361 | 8625a463 | 40 | 0 | 0 | passes |
| 43753381312 | 36f04678 | 40 | 0 | 0 | passes |
| 43747941639 | 8625a463 (the failure) | 40 | 1 | yes | fails |

- Rows 43751138054, 43751148361 and 43753381312 carry the same 40 timing rows as the failure and pass. Their runtime-service.log is empty.
- The failing run differs from them by the extra claim-vs-fence "database is locked" traceback. The pack host's shutdown request timing hit the Runtime's SQLite fence.
- So the failure is a timing coincidence at Runtime shutdown. The new print adds no stderr writes to that process.

## What is missing (gaps)

- No pids, timestamps or crash report for the Fatal line (the Python message has no pid). The mapping to pid 6464 rests on the launchd bookkeeping and that the Fatal lies in the launchd-owned log, not on a printed pid.
- "Killed: 9" versus abort(): a Fatal Python error normally ends in SIGABRT, but launchd reports Killed:9. I infer the Runtime hung in abort and crash-report handling, then got SIGKILL from the 20 s escalation. This is not proven.
- The exact request that hit `handle_error` is unknown (only the dash line survived). A `launchctl print` right after the stop, or a ReportCrash entry, would settle it.
- Mitigation options, none in the agent: join or quiesce request threads before the redirect exits and finalization, make stderr writes in `_error`/`handle_error` safe at shutdown (Runtime change), or have the installer treat a respawn after `down` as retry-able. The agent-side print needs no change for this failure.
