# Declared run logs (owner-requested; reconciled design)

The owner's rule: getting a run's full logs must be really simple. There is NO REDACTION: the user's own machines produce the user's own logs.

## The shape (one, at every layer)
```python
@dataclass(frozen=True)
class LogDecl:
    name: str            # unique in the run: "engine", "run", "job.stdout", "job.stderr", "attempt"
    role: str            # "engine" | "run" | "stdout" | "stderr" | "install" | "attempt"
    path: str            # absolute on the declaring machine, or relative to the declaration file
    start: int = 0       # first byte belonging to this run (slices a shared session log)
    end: int | None = None  # None = still being written
```
- It is serialised as JSON `{"schema": "run-logs.v1", "logs": [ {name, role, path, start, end} ]}`.
- It is written when the run STARTS and updated (`end` set) when it ends, so a crashed run has still declared its logs.
- The parent assigns the run root, so nothing searches for files.

## Who declares what
- **VibeComfy:** `RunContext` gains `declare_log(...)`. `begin()` writes the `logs` list into `attempt.json`.
  - A per-run managed server declares `run_dir/comfy.log` (`run.py` ~479).
  - A session-owned server declares its session log (`session.py` `_captured_process_log_path()` ~2114-2120) with `start` = the file size when the run begins.
  - An attached endpoint declares whatever `capture_log` fetched.
  - On a node failure, `attempt.json` keeps ComfyUI's FULL `execution_error` message and traceback. Today VibeComfy drops them: `session.py` ~3977-4031 allowlists them away. Remove that filtering for the stored record; there is no redaction.
- **Pod job wrapper (Astrid RunPod):** declares its own `job.stdout` and `job.stderr` (the agent job dir).
- **Host:** reads the child's declaration at the path it assigned.

## One collector
New module `astrid/core/_shared/run_logs.py`, standard library only:
- `read_declared(path) -> list[LogDecl]`;
- `collect(decls, dest, *, cap_bytes=8 MiB) -> list[row]` writes `dest/<name>.log` = bytes [start:end], keeping the tail over the cap and marking it truncated. Each row is `{name, role, path, size, sha256, truncated, missing}`. A declared but unreadable log gives `missing: true`.

## Transport
- Logs are ordinary outputs with role `log`. The Runtime already associates outputs on failed tasks (`store.py` ~6808) and lists them (`list_managed_outputs`).
- Local placement: the files are already there, so only collect is needed.
- RunPod: the pod-side code collects into the job's `out/logs/`. The job script runs the manifest on failure too, and the controller fetches through the existing `_fetch_verified` on failure.
- One command: `astrid tasks logs <task> [--name engine]`. `astrid generate failure` lists them.

## Delete
- `failure_logs_command`, the stopgap scrape at `r13/failure-logs` `43993b6f`.
- The 4 KB frame-only failure read, as the sole fetch.
- `tail -c 4000` / `stderr[-800:]` in `remote_placement._run_job`.
- The redactor and the secrecy allowlists.
