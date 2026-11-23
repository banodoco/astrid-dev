# Installed render and lease source trace

Read-only inspection of installed release `5bf20639e293` under `~/astrid-release/release-14-plan-69`; source checkout files were not modified and no Runtime request or process launch was made.

## Lease timing and request bounds

- Generic Runtime task claim lease is **30 s**: `r/runtime_protocol/store.py:457,4434`; heartbeat renewals default to that same `LEASE_SECONDS` at `:6252` (and deadline computation at `:6269`). The default `ExecutionGuardPolicy.authority_window_seconds` is **300 s** (`a/astrid/core/execution/guards.py:201`), so the host's default lease poll interval is **5 s** (`generic_host.py:555,12016-12020`). The per-attempt pump starts at `:12266-12270` and polls task/lease state in its own thread (`:12035-12039`).
- Heartbeat call is separately fenced and guarded in `a/astrid/core/execution/generic_host.py:5658-5688`; it uses a per-call client copy and caps RPC time to **2 s** by default (300/150; `guards.py:201`, `generic_host.py:5646-5656,5668-5686`). Generated loopback client default request timeout is **30 s** (`a/astrid_runtime_client/generated.py:643-649,667-672`), but the guarded heartbeat path shortens it. The corresponding 30 s attempt lease means a delayed RPC/pump can outrun lease expiry.
- These are runtime/source defaults, not exposed render environment settings. Host concurrency is a host launch/registration parameter (`generic_host.py:18206` CLI `--max-concurrency`, default 1; accepted launch bounds at `:16785-16787`). Remotion itself is explicitly launched with `--concurrency=1` at `a/astrid/packs/rendering/rendering/renderers/remotion/run.py:1239-1263`.

## Renderer isolation and possible contention

The Remotion renderer runs as a subprocess from `run.py` (see subprocess setup around `:1280-1330`); its Chromium worker concurrency is one. The parent pack host runs a distinct daemon heartbeat/poll thread (`generic_host.py:12266-12270`) while the executor owns and monitors the render subprocess. Parallel generic host slots, if configured above one, are also separate `threading.Thread` workers (`generic_host.py:14884-14899,14914-14981`). Thus rendering does not synchronously occupy the heartbeat thread. However, heartbeat and renderer/preview requests share the same Runtime door/process and local state; this source trace alone does not prove contention or event-loop starvation. Runtime uses its service/door threads (daemon shutdown/thread lifecycle in `r/runtime_protocol/daemon.py:234-257,1595-1606`); local lease state uses the Runtime store.

## Render ranges/chunks and documented tuning

Remotion render invocation supports a native window via `--frames=start-end` (`run.py:998-1054,1265-1266`) and selected-frame PNG mode (`:1267-1272`). I found no user-facing documented env setting to tune heartbeat cadence, task lease duration, or Remotion worker count; those are source/launch-level controls. The installed renderer hardcodes one Chromium worker. Host-level concurrent task execution is configurable via `--max-concurrency`, independent of Remotion frame/window selection.

## As-built stop/start facts

`start-2400.sh:13-21` starts the editor as a detached new session and records its PID; it then discovers Runtime PID from `data/runtime/discovery.json` and appends that PID (`:23-30`). Current `state/processes.tsv` records editor PID **5654** and Runtime PID **5671**. Read-only `ps` shows both currently have PPID 1 and each is its own process group/session leader. Therefore stopping only the editor PID does not stop Runtime. Stop the editor and Runtime owners individually through their respective graceful stop paths; do not signal the shared parent group or assume a child relationship. `program/run_runtime.py` launches Runtime via `exec` on POSIX (`:445-449`), so its recorded PID is the Runtime owner. Runtime has a guarded owner-stop implementation with TERM/grace/escalation (`r/astrid_runtime/runtime_boundary.py:945-968,982-983,1091-1107`); use the supported Runtime owner stop path for PID 5671, then stop editor PID 5654 gracefully. Verify both PIDs exit before relaunching with `start-2400.sh`.

No credentials or environment values were inspected or copied into this report.
