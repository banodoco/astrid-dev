# Group 015: read-only diagnosis and continuation proposal

## Evidence and limits

The four clean-host exact-selector runs all failed `test_instantly_exiting_launches_are_a_known_outcome_not_a_custody_error` with `CustodyError: initial custody observer census timed out`; elapsed pytest times were R10 3.68s, R11 52.01s, base 146.53s, candidate 5.90s. Each ran with a 600s pytest timeout and 300s faulthandler timer, which did not fire. Evidence and hashes: `/workspace/r12-a2-evidence-015-diagnostic/`. Earlier full-group R10 ran 692.57s with six failures including a pytest timeout (>600s) on that test, while other pytest processes overlapped; `/workspace/r12-a2-resume/sharded/history/015/r10-overlap-075841/` is excluded pending disposition. It cannot show whether overlap caused the timeout. A single test loops up to 40 owned-shell launches, so whole-test duration is not the duration of an individual 1s observer wait.

On Linux, `popen_owned_process` binds and observes a child, then `start_observer` starts a thread. `start_observer` waits for the monitor's ready event; for the Linux no-launch-broker path `prepare_launch` leaves `_launch_broker` unset, so the wait is 1.0s. The monitor calls `observe_tree`, takes the custody RLock, runs `_observe_tree` and its census, then sets ready or records an exception. `_process_snapshot` launches `/bin/ps` or `/usr/bin/ps` with a 5s per-attempt subprocess timeout and up to three attempts; it parses output and reads `/proc/<pid>/stat` and zombie identity for entries. Thus the 1s parent wait can expire while the worker has not completed census/locking/error reporting. All four custody broker, process-group and test files have identical hashes as recorded in the diagnostic trace.

At 2026-11-11 09:19 UTC, read-only current host inventory showed 8,800 visible processes of which 8,777 were zombies, all parented to PID 1; cgroup `cpu.max` was `400000 100000` (4 CPU quota), `pids.current` 8,863 and `pids.max` unlimited. This is a current snapshot, not a count at the earlier runs. A large census is a plausible cost source but these observations do not prove why the observer missed its deadline. The logs have only line-level failure traces and no thread stack during the 1s wait. Do not kill, reap, or otherwise change unrelated processes; the host process population is a possible comparability limitation.

## Bounded distinctions, requiring an exclusive host lease

1. One diagnostic-only R10 exact-selector rerun with the same environment, `-vv --tb=line -rA`, `timeout=600`, fresh log/basetemp, and `-o faulthandler_timeout=0.75` instead of 300. Pytest's installed faulthandler uses a one-shot `dump_traceback_later` for each test; a dump before the 1s readiness gate may show the observer in `_process_snapshot`/`subprocess.run`, waiting for its custody lock, or not yet started. It is a sample, not complete timing: a no-dump or an already-unwinding thread remains inconclusive. Record all thread stacks, exit and hashes as diagnostic only; lower traceback timer does not change test timeout, but stack dumping can affect scheduling. Stop after this single run and inspect before any follow-up.
2. If stacks leave the distinction unresolved and separately authorized, a single `strace -ff -tt -T` of that same selector, limited to `futex,clone,clone3,execve,wait4,openat` and written to restricted local files, can time lock waits, `ps` launch/wait, and `/proc` reads. It cannot by itself prove thread scheduling delay, and tracing can alter the behavior. Do not put raw traces in a shared evidence bundle without review: pathnames can be sensitive. Compare pre/post host process counts and cgroup throttling deltas; do not treat them as proof of causation. No source or product change is needed for either diagnostic.

## Clean continuation of the approved comparison, after disposition and a lease

Group 015 is one intact module, `tests/core/execution/test_process_group.py`, 91 selected IDs on every side; manifest SHA-256 `885b264862a0e6e90698ed8a76a6b5b30e2dbeb1f3846ea96b356913b1a9e771`. The isolated test results do not replace the 91-ID group. Obtain an exclusive lease and manager/orchestrator disposition on the overlapping R10 timeout and on whether this high-zombie host is comparable enough for the evidence. If not, use a fresh isolated host with the same frozen pins/toolchain and record the host/environment difference; no assumption that a replacement host exists.

Before launch, check no foreign tests, actual process state and host load; rerun `/workspace/r12-a2-resume/recovery-run/preflight.py`, verify manifest and Node/esbuild binary hashes/versions, and confirm each `shard-015-clean-<unique>` basetemp and `receipts/015/<side>` is absent. Run R10, R11, base, candidate serially with the identical module, existing `run-batch.sh`, unchanged 600s timeout and a unique `A2_BASETEMP_SUFFIX`, for example:

```sh
A2_BASETEMP_SUFFIX=-clean-unique /workspace/r12-a2-resume/sharded/run-batch.sh r10 015 tests/core/execution/test_process_group.py
python /workspace/r12-a2-resume/sharded/verify.py r10 015
```

Repeat the two commands for `r11`, `base`, and `candidate` only after verifying prior side's summary, exit, exact ID coverage, SHA/pins/toolchain and no competing workload. Store the exact command/session, monitor PID and log at least every 30–60 seconds and stop after a side if contention appears. Preserve any interrupted or overlapped output under history and use another unique log/basetemp; never splice it into the clean side. Do not overwrite the retained prior R10 history. After all four complete, continue remaining batches with approved manifest and final cross-side ID/message/coverage comparison. Keep grouped session-fixture/cross-module-order limitations explicit.

Duration estimate: current evidence spans 3.68–146.53s for the isolated case, while the prior overlapped R10 full module took 692.57s. Allow roughly 10–50 minutes for four serial complete module receipts, but this is a planning range, not a bound: the timeout is per test, not per group, and slow teardown or repeated long tests can exceed it. If a case hits 600s, preserve the complete failure and report it; do not widen or silently stop it. Trace work and any host migration add time.

## Suggested noninvasive census-cost measurement after lease

Do not run while Track B owns the host. After a separate exclusive lease, first record process/zombie counts, `cpu.max`, `pids.current`, and cumulative `cpu.stat`. A single sanitized timing probe can execute the exact `ps` shape used by `_process_snapshot`, retain its output only in memory, and separately time the real `_parse_census` (which reads `/proc` and zombie identity); print only counts, return code and elapsed times, never raw process rows. A hard 30s outer `timeout` bounds the probe; it makes no product edits and is not pytest or comparison evidence, but still consumes host resources and may perturb measurements. Example from the R10 checkout, after inspecting the command and checking the lease:

```sh
cd /workspace/r12-a2-resume/r10
/usr/bin/timeout 30s env -i PATH=/workspace/r12-a2-resume/r10.env/venv/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /workspace/r12-a2-resume/r10.env/venv/bin/python - <<'PY'
import subprocess, time
from astrid.core.execution.process_group import _parse_census
start = time.monotonic()
p = subprocess.run(['/bin/ps', '-axo', 'pid=,ppid=,pgid=,lstart='], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=5, check=False)
ps_done = time.monotonic()
if p.returncode:
    raise SystemExit('ps failed; return code=' + str(p.returncode))
snapshot = _parse_census(p.stdout)
end = time.monotonic()
print('ps_seconds=%.6f parse_seconds=%.6f live_entries=%d exited_entries=%d' % (ps_done-start, end-ps_done, len(snapshot), len(snapshot.exited)))
PY
```

Record result/exit, elapsed time, host counts and `cpu.stat` again. A slow `ps` versus slow parsing of `/proc` suggests different census costs, but the separate one-shot probe neither measures the observer thread's lock wait/scheduling nor proves the failing execution followed the same timing. A one-second faulthandler stack or syscall trace, separately approved, remains necessary to distinguish where the observer actually was. The probe itself runs one `ps` and one census parse, not the full 40-launch test; allow 30 seconds maximum plus setup and verification. Do not kill or alter unrelated processes.
