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

---
# A/B installed run (Plan 81 release evidence): BEFORE = published Release 14, AFTER = candidate manifest

Setting, always: installed builds, CPU container, stand-in ComfyUI (not covered: a real ComfyUI's node-info answer, GPU work), shared 4-vCPU box.
Deviation in BOTH arms: `omp` from npm (`@oh-my-pi/pi-coding-agent@18.12.6`); the timed commands never call omp.

Commands (nothing else needed; installs are idempotent and isolated under this directory):
    /root/codex/installed-baseline/run-ab-installed.sh          # prepare + UNTIMED validation only
    /root/codex/installed-baseline/run-ab-installed.sh --run    # prepare, then the gated timed A/B (needs a quiet box)

Arms: before = `home/ program/ data/` (door port 17340, manifest-omp-npm.json); after = `home-after/ program-after/ data-after/`
(door port 17341, `CANDIDATE_MANIFEST`, default manifest-candidate.json). One stand-in ComfyUI (port 18188) is shared.
Timed run: per group (same-prompt generate, changed-prompt generate, timelines edit) 1 warm-up per arm then 5 measured per arm,
alternating before/after; each command waits for 1-min load < 1.0 (poll, up to 600 s, lock polled too), holds
/tmp/astrid-timing.lock only while it runs, records load before/after; if the gate is not met the run FAILS (exit 3,
`FAILED-load-gate.txt`) and nothing runs ungated. The after arm adds `--timings` (the before arm cannot; its overhead is part of the
after number). Outputs in the evidence dir: `summary-ab.json` (medians per arm per group, ratio after/before, % change, per-command
loads, after-arm stage table), `raw/`, `load-samples.txt` (30 s), `hashes.txt`, installed manifests, `astrid-version-*.txt`.

Pins (sha256 of files): installer https://astrid.haus/install sha256 c268a5fae7ff318414745cee7bfcec13b6d7a81434f7aaa10d218ffe28248fff;
published manifest 8556f218...; before manifest (omp npm) 43e2130d...; candidate manifest b25165b7...; fallback candidate-vc48 c1ecda6f....
BEFORE tuple: agent c0ad6b54aadd21630d98bb5039613e37efe92a8f, runtime 5120462d67479dc4719406d0d34440edb616ace1, vibecomfy 48b5fa9e45630e1bc502651975ec0ef3a5e74c4c, lifecycle 9f88ef7640bc664f697112d966ecefa123d44340.
CANDIDATE: agent 9c95c680e645335a4a2ea8091f02b88934a2492b (banodoco/astrid-agent release/15/plan-81), runtime 72b129e5a2296dc58360a9896cc65fab9db4ad0c
(banodoco/astrid-runtime release/15/plan-81; manifest `runtime.schema_digest` set to that Runtime's SCHEMA_DIGEST sha256:2c6a76e1...),
vibecomfy 36ea976ffa24ac3ab5b5e48b7b279af7565d5c41 (PR 182 head), lifecycle and omp unchanged. Diffs: `manifest-candidate-vs-published.diff`,
`manifest-candidate.diff` (vs the before manifest). The installer only pins by commit sha (archives from github.com/<repo>/archive/<sha>.tar.gz); no archive hashes exist.

## BLOCK: the candidate manifest as specified does not install
The installer refuses it (evidence/after-install-1): "The manifest VibeComfy pin does not match the staged Agent recipe." The installer requires
`manifest.vibecomfy.sha` to equal the Agent's own `astrid/packs/runpod/pins.json` -> sources.vibecomfy.revision, and Agent 9c95c680 still pins
48b5fa9e. The Agent release branch must carry the VibeComfy bump to 36ea976 in `astrid/packs/vibecomfy/pins.json`, `astrid/packs/runpod/pins.json`,
and the sha256-bound `recipe.windows-cu130.json` / `runpod/recipe.linux-cu130.json` (plus tests/test_windows_path_budget.py references 48b5fa9e).
Smallest fixes: (a) Plan 81 commits that pin bump on release/15/plan-81, then set manifest agent sha to the new head and re-run; or (b) the documented
developer-qualification route: a scratch clone of the Agent at 9c95c680 with one local commit bumping those files, manifest `agent.repo` = that clone.
Not done: neither is mine to choose (it changes what the Agent is).

## Validated so far (untimed, with the FALLBACK manifest-candidate-vc48.json = candidate agent + runtime, vibecomfy kept at 48b5fa9e)
Both installs answer `--version`; the candidate's `generate image --help` lists `--timings`; one untimed `generate image` per arm succeeds
against the stand-in (candidate prints its stage table; evidence/ab-prepare-vc48, ab-prepare-vc48b). The candidate's stage list does include
"pack host source identity" (~0.15 s) and "Runtime launcher connection" (~0.2 s) (untimed observation, loaded box). Stale installs are caught:
the script refuses if the installed pins differ from the requested manifest. NOT validated: the timed `--run` (ab_run.py has only been syntax checked),
and the true candidate manifest (blocked above). NOTE: the after install currently on disk is the vc48 fallback; to use the true candidate,
remove `program-after data-after home-after` first (or the script's pin check will stop the run).

## UPDATE: true candidate route (scratch Agent clone with one LOCAL pin-bump commit; nothing pushed)
`agent-candidate/` = clone of banodoco/astrid-agent `release/15/plan-81` (head 9c95c680e645335a4a2ea8091f02b88934a2492b, unchanged when checked)
plus ONE local commit bc75d6c592e16582fffc5f1ca1a6aa35508c9ddf (origin remote removed; never pushed). It was made with the repo's own
generator `python scripts/vibecomfy_pin.py 36ea976ffa24ac3ab5b5e48b7b279af7565d5c41 --checkout <VibeComfy at 36ea976>`, which rewrote six
files (the two pins.json, the two sha256-bound recipes, environment.windows-nvidia.json and the generation.engine comfyui.yaml recipe digests);
diff in `evidence/candidate-pin/pin-bump.diff`. The test literal tests/test_windows_path_budget.py was not touched (not used by the installer).
`manifest-candidate.json` now has agent {sha: bc75d6c5..., repo: /root/codex/installed-baseline/agent-candidate} (documented local-source route),
runtime 72b129e5, vibecomfy 36ea976 (sha256 3f0ec9db...); the real pin bump goes to the owner with Plan 81's landing.
Before installing the true candidate, remove the fallback arm: `rm -rf home-after program-after data-after` (then `run-ab-installed.sh` installs it).
