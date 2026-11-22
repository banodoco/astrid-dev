# Copied A/B tooling: current usage and limits

Run `./run-ab-installed.sh` from this copy for preparation, or add `--run` for the timed run. The script loads its driver, stand-in, media and default manifests from its own directory. `IB` selects the absolute live install root and defaults to `/root/codex/installed-baseline`; evidence defaults under that root and can be redirected with `EVIDENCE_DIR`. The default candidate manifest retains its historical absolute `agent.repo` path under `/root/codex/installed-baseline`; supply an appropriate `CANDIDATE_MANIFEST` if that source is unavailable or differs. Starting the wrapper can install or start processes and modify the selected install root.

Each round runs arms in fixed order (before, after, vc48), not randomized. The candidate arms use `--timings` for generation while before does not, so their measured wall times include different instrumentation. The after and vc48 builds also differ in Agent pin-generated files. Differences and the calculated ratios are descriptive comparisons, not proof of causal attribution. These CPU-container results use a stand-in ComfyUI and do not measure real ComfyUI node-info answers or GPU work.

The earlier `ab-run-2` driver did not pass the per-arm Runtime door ports into timed subprocesses; the effect, if any, on its saved results has not been established. The corrected wrapper and driver pass each arm's port explicitly. The historical evidence and narrative below remain records of those runs, not evidence that the corrected tooling was used for them.

---
# Installed-Astrid baseline (published Release 14, stand-in ComfyUI, CPU container)

Working evidence only (container seconds, shared 4-vCPU box); not a promise and not the owner's real-machine number.

## Re-run
    /root/codex/installed-baseline/run-installed-baseline.sh [--timings]
Env: `ASTRID_INSTALL_MANIFEST` (path or URL of an install manifest; used only if not installed yet, e.g. a candidate
build), `EVIDENCE_DIR` (default evidence/run-<UTC>), `LOAD_MAX` (1.0), `LOAD_WAIT_SECONDS` (600), `STANDIN_PORT` (18188),
`KEEP_RUNTIME=1` (do not stop the installed Runtime at the end).
It installs into the isolated HOME/XDG under this directory only if `program/run-astrid --version` does not answer, starts
the stand-in with the installed venv python, runs `us0-published.py` (unmodified copy) through `timed-astrid.py`, then
floor runs (`--version` x5, `generate defaults` x3), prints the summary and stops the stand-in and sampler when their recorded identities still match. Cleanup also attempts to stop Runtime processes that are still descendants of this invocation and whose executable or command-line path is inside an arm install root. Detached or reparented Runtime processes cannot be attributed reliably and may remain running; cleanup reports this limitation. Set `KEEP_RUNTIME=1` to leave Runtime processes alone. Cleanup uses pidfds and checks process start times, ancestry and paths before signaling, but a PID reused within the same start-time clock tick before the pidfd is opened cannot be distinguished by start time alone. Processes can also change after the checks. Cleanup sends SIGTERM and does not confirm that a process exits. If pidfds are unavailable, signaling fails closed.
`--timings`: only added to `generate` if `generate image --help` lists it; on Release 14 it does not (see below).
Launcher after a `--root` install: `program/run-astrid` (the `home/.local/bin/astrid` shim points at the same).
After teardown the first launcher call restarts the Runtime and may fail once (~8 s); the script retries.
To remove: `rm -rf` this directory's `program data home` (everything is under it).

## Parts
- Historical single-arm `timed-astrid.py`: ASTRID_CMD wrapper. Polls 1-min load < 1.0 (up to 600 s, then runs anyway and flags `load_gate_met:false`;
  later commands in the same run do not wait again), holds `/tmp/astrid-timing.lock` only while the command runs, logs the
  command's own wall time (wait excluded) to `timing.jsonl`. `summarize_timings.py` makes `timing-summary.json` from it.
  The current A/B driver instead fails closed if its load gate is not met.
  `us0-published.py`'s own `summary.json` times the wrapper process from outside, so it also contains the load/lock wait; use `timing.jsonl` / `timing-summary.json`.
- `standin/standin_comfy.py` + `standin/standin_lib.py`: stand-in ComfyUI adapted read-only from the managers'
  `runpod_slot_pod.py` / `_pinned_source.attached_comfy` (`*.managers-copy` are the untouched copies). It validates /prompt
  against the installed VibeComfy's packaged node schemas for the `image.t2i` default entry, fills loader
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
    ./run-ab-installed.sh          # prepare + UNTIMED validation only
    ./run-ab-installed.sh --run    # prepare, then the gated timed A/B (needs a quiet box)

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

---
# A/B/C run (three arms) and its artifacts

Setting, always: installed builds, CPU container, stand-in ComfyUI (not covered: a real ComfyUI's node-info answer, GPU work), shared 4-vCPU box,
`--no-wait` (times Astrid up to "task queued"). Both candidate arms run `generate` with `--timings`; the published Release 14 build has no such flag, so only
the candidate arms include its overhead and the wall comparison includes this instrumentation difference. omp comes from npm in every arm (owner-approved); the timed commands never call omp.

Arms (installed in isolated dirs; door ports differ so all three Runtimes can run at once):
| arm | dirs | manifest (sha256 prefix) | tuple |
|---|---|---|---|
| before | home/ program/ data/ (17340) | manifest-omp-npm.json (43e2130d3f4e) | published Release 14: agent c0ad6b54, runtime 5120462d, vibecomfy 48b5fa9e, lifecycle 9f88ef76 |
| after | home-after/ program-after/ data-after/ (17341) | manifest-candidate.json (3f0ec9db1e60) | agent bc75d6c5 (local pin-bump commit on release/15/plan-81 9c95c680, in agent-candidate/, never pushed), runtime 72b129e5, vibecomfy 36ea976f |
| vc48 | home-vc48/ program-vc48/ data-vc48/ (17342) | manifest-candidate-vc48.json (c1ecda6f1f2d) | agent 9c95c680, runtime 72b129e5, vibecomfy 48b5fa9e |
`vc48` is the candidate without the VibeComfy change. It uses Agent 9c95c680, not bc75d6c5: the installer refuses an Agent whose own pin (36ea976f in bc75d6c5)
differs from the manifest's VibeComfy sha, and bc75d6c5 differs from 9c95c680 only in the six generator-written pin files (evidence/candidate-pin/pin-bump.diff), so the code is the same.
Installer sha256 c268a5fae7ff318414745cee7bfcec13b6d7a81434f7aaa10d218ffe28248fff. Published manifest 8556f2183dfc... Candidate commit bc75d6c592e16582fffc5f1ca1a6aa35508c9ddf.

Commands (exact):
    cd /path/to/this/copied/tooling
    python3 test_ab_summary.py                  # pure-file test of the summary code (no process started); reproduces ab-run-1's medians
    ./run-ab-installed.sh                       # install missing arms (idempotent) + UNTIMED validation of every arm
    ./run-ab-installed.sh --run                 # prepare, then the gated, timed run
    ARMS="before after" ./run-ab-installed.sh --run     # the earlier two-arm run
The timed run needs a quiet box (nothing else heavy; 1-min load under 1.0 before and between commands). One round = before, after, vc48 (in that order); per group
(same-prompt generate, changed-prompt generate, timelines edit) 1 warm-up round and 5 measured rounds. Every command waits for load < 1.0 (poll, 600 s cap, lock polled too),
holds /tmp/astrid-timing.lock only while it runs, and the whole run FAILS (exit 3, FAILED-load-gate.txt) rather than running ungated.

Output (summary is produced by the run itself): three-column medians, ratios vs before, % change, and descriptive median-difference ratios
((vc48 - after) / (before - after) and (before - vc48) / (before - after)), plus a stage table for each candidate arm. Fixed order,
differing instrumentation, and differences in Agent pin-generated files prevent exact attribution of those ratios to individual changes.

Where each artifact lives (evidence dir, e.g. evidence/ab-run-N/):
- `records.jsonl`: one line per command, appended + flushed + fsynced as it finishes (args, started_at, wall_seconds, exit code, 1-min and 5/15-min loads before/after,
  gate wait, timings), then a final `{"records_complete": true}` line. If the summary step ever fails the run exits 4 and
  `python3 ab_summary.py <evidence dir>` rebuilds `summary-ab.json` from it.
- `summary-ab.json` / console output: medians, ratios, shares, stage tables, all records. `raw/<group>-<arm>-<k>.stdout|.stderr`: full command output.
- `load-samples.txt` (30 s sampler), `hashes.txt`, `manifest-<arm>.json` (requested) and `installed-manifest-<arm>.json` (what the installer recorded), `astrid-version-<arm>.txt`, `standin.log`, `install.sh`.
- `console.log`: the run's printed output (the wrapper's `evidence/<run>.console.log` is the same).

ab-run-1 (two arms) was run by the first driver, which crashed in the summary step (a stage row without `total_seconds`) and had not yet been taught to keep records.jsonl,
so that directory has NO original `records.jsonl`. `evidence/ab-run-1/records-recovered.jsonl` was written afterwards by `recover_records.py` from the console log and raw/ and is labelled
`"recovered": true` on every line: wall/exit/1-min load are exact (2 decimals), args are reconstructed from the driver templates, started_at is the raw file's mtime, gate waits are not recoverable.
`evidence/ab-run-1/summary-ab.json` was rebuilt by `rebuild_ab_summary.py` (same numbers; `test_ab_summary.py` re-derives them).

For historical `ab-run-2` records, rebuild a copy of the evidence directory with
`python3 ab_summary.py DIR --legacy-records --arms before after vc48 --samples 5`.
This explicit historical mode validates timing rows but permits the missing collector spans
and labels them unverified; it does not manufacture values. Current timed records require
the timing receipt schema and collector spans.
## Run 2 and evidence boundaries

Run 2's 54 command outputs are preserved in `ab-run-2/raw/`; run 1's raw outputs are in `ab-run-1/raw/`. The two installed A/B raw trees total 1,568,180 bytes. Run 2's original records omit C despite the raw outputs containing it; `ab-run-2/collector-spans.json` is derived from those raw outputs and records source provenance. The summary tables are descriptive; the candidate tuples differ in Agent pin, nested stages overlap, and these measurements do not provide a causal share or an occurrence-count oracle.

The A-5 observer draft and A-6 harness source are stored in sibling evidence directories under `plans/81-once-per-command/evidence/`; hash/witness probes remain in the existing attribution bundle. The A-5 code is explicitly unqualified. The US-2 runner and its referenced fixture files are retained under `evidence/us2-post69/`; this copy does not claim a new gate result.

The unrelated full A-4 raw attribution archive is intentionally not committed: `/root/codex/plan-81m/run/attribution-evidence-2026-11-22-full-raw.tar.gz`, 20,246,866 bytes, SHA-256 `6a690c4afe10be2bce3f49d0b372b2fe1a2ab20db209e095746fc1721421e58a`. Kept on the machine that made it; reproducible by rerunning the [source fixture](../2026-11-22-attribution-bundle/README.md#full-raw-archive), although a new measurement will not reproduce the original bytes. The included failed witness-attempt archive is `../witness-attempts-2026-11-22.tar.gz`, 77,570 bytes, SHA-256 `36200a120eb9178077c88266007082395075b782500f385c47819425ec8b5171`; a targeted scan found no credential-pattern matches, and `.env` files were not read or included. These are failed/diagnostic attempts, not a passing attribution result, and cannot be reproduced byte-for-byte by rerunning.

Focused proof on the packaged files: `test_ab_summary.py` passed all four tests on 22 November 2026. Its historical fixture layout expects `evidence/ab-run-1` and `evidence/ab-run-1.console.log` beside the test. For the proof, unchanged test and Python modules were copied into a temporary directory, with those two paths linked respectively to this package's `ab-run-1/` and `ab-run-1/console.log`. The original cleanup-focused tests also passed eight tests and the shell syntax check; no installed command or timing run was made for these proofs.

The test files are preserved but not run as part of this evidence-only documentation update. Current tooling fixes postdate the recorded run 2 results, so the recorded measurements predate those fixes. Historical source-only paths may point at a removed scratch checkout; installed trees and live checkout trees were distinct. The earlier broad cleanup could match unrelated processes. The current `run-ab-installed.sh` uses `process_ownership.py` to verify process ancestry and install-root paths before signaling; `load_sampler.py` is tracked as a child process, and the decoy-path matcher tests are preserved in `test_process_ownership.py` and `test_cleanup_children.py`.
