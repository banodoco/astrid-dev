# Installed-Astrid baseline (published Release 14, stand-in ComfyUI, CPU container)

Working evidence only (container seconds, shared 4-vCPU box); not a promise and not the owner's real-machine number.

## Re-run
    /root/codex/installed-baseline/run-installed-baseline.sh [--timings]
Env: `ASTRID_INSTALL_MANIFEST` (path or URL of an install manifest; used only if not installed yet, e.g. a candidate
build), `EVIDENCE_DIR` (default evidence/run-<UTC>), `LOAD_MAX` (1.0), `LOAD_WAIT_SECONDS` (600), `STANDIN_PORT` (18188),
`KEEP_RUNTIME=1` (do not stop the installed Runtime at the end).
It installs into the isolated HOME/XDG under this directory only if `program/run-astrid --version` does not answer, starts
the stand-in with the installed venv python, runs `us0-published.py` (unmodified copy) through `timed-astrid.py`, then
floor runs (`--version` x5, `generate defaults` x3), prints the summary and stops the stand-in, sampler and the Runtime.
`--timings`: only added to `generate` if `generate image --help` lists it; on Release 14 it does not (see below).
Launcher after a `--root` install: `program/run-astrid` (the `home/.local/bin/astrid` shim points at the same).
After teardown the first launcher call restarts the Runtime and may fail once (~8 s); the script retries.
To remove: `rm -rf` this directory's `program data home` (everything is under it).

## Parts
- `timed-astrid.py`: ASTRID_CMD wrapper. Polls 1-min load < 1.0 (up to 600 s, then runs anyway and flags `load_gate_met:false`;
  later commands in the same run do not wait again), holds `/tmp/astrid-timing.lock` only while the command runs, logs the
  command's own wall time (wait excluded) to `timing.jsonl`. `summarize_timings.py` makes `timing-summary.json` from it.
  `us0-published.py`'s own `summary.json` times the wrapper process from outside, so it also contains the load/lock wait; use `timing.jsonl` / `timing-summary.json`.
- `standin/standin_comfy.py` + `standin/standin_lib.py`: stand-in ComfyUI adapted read-only from the managers'
  `runpod_slot_pod.py` / `_pinned_source.attached_comfy` (`*.managers-copy` are the untouched copies). It validates /prompt
  against the installed VibeComfy's packaged node schemas for the `image.t2i` default entry (qwen-image-2.1-turbo), fills loader
  menus with that entry's three model names, returns a 16x16 PNG. Only PIL was replaced by a hand-written PNG.
- `manifest-omp-npm.json` (+ `.diff`, `manifest-hashes.txt`): the manifest used for the install.
- `profile-generate.py`: one cProfile run of the installed `generate image` (evidence/run-1/profile-generate-top.txt).

## DEVIATION from the published install (owner-approved)
The session proxy blocks `github.com/banodoco/oh-my-pi` (the `omp` chat-engine source pin; 403, access request denied).
For this baseline only, `tools.omp.source` in the Release 14 manifest was changed to the npm form
`@oh-my-pi/pi-coding-agent@18.12.6`; nothing else differs (diff and sha256 recorded: published 8556f218..., override 43e2130d...).
The timed commands never call omp. Everything else (agent c0ad6b54, runtime 5120462d, vibecomfy 48b5fa9e, installer script
sha256 c268a5fa...) is the published release.

## Limits
Stand-in ComfyUI (no model load, no image generation; `--no-wait` times Astrid up to "task queued"); CPU container; the box is
shared with other managers' tests, so the load gate (< 1.0) was NOT met in run-1 (load 1.2 to 3.1; part of it is this
install's own Runtime/pack host executing the queued tasks against the stand-in). Treat medians as indicative.
