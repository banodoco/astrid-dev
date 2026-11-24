# How fast can a thin client queue `generate`? A floor experiment (24 November 2026)

For [Plan 82](../../plan.md), RA-1 (D1). The question: can `astrid generate` reach "task queued" in under 1 second on a warm, installed machine, if the command line is a thin client and a process that is already running holds everything that does not depend on the request? This was a measurement only. The client and host here are stubs, not product code, and nothing was pushed to a product repository.

## Answer

**Yes, on this box, with the stand-in ComfyUI. Median 0.32 s, with every per-request check today's command makes run in-line** (arm Cfull: 0.29 to 0.37 s, 5 samples). Today's command takes a median of 5.36 s (10 samples). The stub's bytes and approval digest are identical to an independent `astrid generate` process's. All 30 tasks the stub arms queued succeeded on the stand-in, as did the 12 from A. One of the ten real-work samples (arms Creal and Cfull) took 0.90 s, because one render took 0.80 s. Even that outlier stayed under 1 s.

**Confidence:** high for this box and the stand-in, with about 0.6 s of headroom. Medium for a person's machine. Four things were not exercised:

- a real ComfyUI's node list (the stand-in serves 13 classes);
- model-root hashing on a managed target;
- the per-command witness for a person's own and project packs;
- the rebuild when a template misses. That would add today's 0.58 s build and land near 0.9 s *est.*

Without the resident host's prepared graph, residency alone does not help much. Today's code held warm in one process (arm W) still takes 4.33 s.

**Recommendation for RA-1 (D1): resident first.** A thin client to the warm pack host is the only measured route under 1 s. The note's disk-only estimate stays near 2.0 s *est.*, because every command still pays interpreter start, imports (0.87 s under `-X importtime`), the launcher connection and host attachment. Disk caches should come second, to speed the first command after a host restart (today 5.4 to 5.8 s). RA-2's main target inside the host is the render: `emit_bundle` is 0.20 of the 0.31 s server time.

## Setup

- **Machine:** shared cloud container: 4 vCPU Intel Xeon @ 2.10 GHz, 15 GB, Linux 6.18. Every timed command was gated on a 1-minute load below 1.0; the load before each sample was 0.63 to 0.98. Each queued task was followed to a terminal state, untimed, before the next sample.
- **Code:** Agent `a09ea669` (release/15/main), Runtime `24e2c929` (release/15/main), VibeComfy `c0e910ca` (the commit Agent pins), lifecycle `9f88ef76`. Each came from a detached worktree under `/root/plan82-floor/src/`.
- **Install:** the published bootstrap, `install.sh` sha256 `c268a5fa…`, the same file Part 2b used. It was installed with `--root`, `--data-root`, `--autostart off`, `--command on` and `--skills off` into an isolated HOME. The manifest is [scripts/manifest.json](scripts/manifest.json), Part 2b's with the three SHAs and local repos swapped and `"release": 15`; omp comes from npm, as in Part 2b. It installed first time: [install.out](install.out), "Astrid installed: Release 15 (build a09ea669)".
- **Stand-in ComfyUI:** Plan 81's [standin_comfy.py](../../../81-once-per-command/evidence/installed-container-baseline/standin/standin_comfy.py) and its `standin_lib.py`, unchanged (sha256 `b00368ff…` and `f5c0f254…`). It runs on the installed venv, entry `image/qwen_image_2_1_turbo`, 13 classes.
- **Command:** Part 2b's, `run-astrid generate image "a red square on a plain background" --mode t2i --placement http://127.0.0.1:18388 --project floor --no-wait --json --timings`, to "task queued". Attestation was off.
- **Driver:** [scripts/floor_run.py](scripts/floor_run.py): one warm-up per arm, then 5 alternating rounds. It ran twice: run 1 had arms A, Cnaive, Creal, W and Cping; run 2 had A, Cfull, Cnaive and Cping. Records and medians are in [run1/](run1/) and [run2/](run2/); the per-occurrence stage tables are left out of the records, and the stage medians are in `summary.json`.

## The stub

[scripts/warm_host_stub.py](scripts/warm_host_stub.py) is the resident stand-in for the pack host. At start it runs one `generate` through the full product path in-process (`astrid.console.main`, an embedded invocation) and keeps four things: the Runtime requests it sent, the emitted `workflow.py` and `workflow.vibe.json`, a deep copy of the graph handed to `emit_bundle`, and the arguments of the node-list and model-resolution call. It then opens its own Runtime session with the product's `AstridClient.open_from_launcher()`; product code reads the launcher-issued credential, and the stub never does. It serves one-line JSON on a Unix socket.

[scripts/thin_client.py](scripts/thin_client.py) runs as `python -I -S`. It imports `sys` and `_socket` only, writes the JSON by hand, sends the prompt and seed, and prints `task queued: <id>`. Under `-X importtime` it loads 16 modules in 4 ms.

Modes:

- **naive:** a literal substitution of the prompt string and `DEFAULT_SEED = …` into the kept `workflow.py`, with `workflow_inputs` rewritten and the digests swapped in the kept task body. Then 2 object POSTs and `POST /v1/tasks`, the admission call the command makes.
- **real:** the real per-request work, warm: a node-list fetch, Runtime liveness (`GET /v1/health`), the slot checks (`resolve_entry_inputs` on a held registry), a deep copy of the kept graph with `set_input` for prompt and seed, the render (`emit_bundle`), 3 object POSTs as the command makes them, the product's admission preflight (`_vibecomfy_invocation_preflight`, which sets the approval digests), a capability lookup and `POST /v1/tasks`.
- **realfull:** real, plus the product's target node list and model resolution (`_capture_model_resolution`, `TargetSchemaProvider.from_object_info`, `require_workflow_assets`) and the approval compile (`load_bundle`, `require_canonical_authority`, `compile`).
- **product:** today's `astrid.console.main(["generate", …])`, run inside the warm process.

**Validation.** For the warm-up's own prompt and seed, the real path's `workflow.py`, companion and `invocation_preflight` receipt are byte-identical to what the warm-up sent. For an independent `astrid generate` process, with the prompt "a blue circle, variation 7" and seed 12345 ([capture/](capture/)), realfull gives the same `workflow.py` sha256 `87b1b8aa…`, the same companion `59d7b1e5…` and the same `api_digest` `0547ea2b…` ([capture/host-validation.log](capture/host-validation.log)).

## A/B/C/D

| Arm | What | Median (s) | Samples (s) |
| --- | --- | ---: | --- |
| **A** | installed `astrid generate --timings` to queued | **5.357** (run 1: 5.802, run 2: 5.201) | 5.599, 6.383, 6.070, 5.802, 5.405; 5.209, 5.093, 5.310, 5.201, 5.168 |
| W | today's code held warm in one process (thin client to `console.main`) | 4.333 | 4.333, 4.378, 4.501, 4.137, 4.261 |
| **C, naive stub** | thin client, literal substitution, admission | **0.036** | 0.031, 0.034, 0.036, 0.040, 0.041; 0.035, 0.036, 0.036, 0.035, 0.038 |
| C, real | the naive stub plus the real per-request render, approval digests and checks | 0.387 | 0.341, 0.408, 0.387, 0.359, 0.902 |
| **C, real, full** | real plus the target node list, model resolution and approval compile | **0.320** | 0.309, 0.374, 0.320, 0.344, 0.292 |
| C, ping | the thin client round trip with no request work | 0.011 | 0.014, 0.013, 0.011, 0.016, 0.011; 0.011, 0.012, 0.011, 0.009, 0.040 |

**A is near Part 2b's 5.83 s.** Run 1 matched it at 5.80 s. Run 2 was 0.6 s faster across the board, on the same build at a similar load, so it is box variance. Its stage medians over the 10 samples are close to Part 2b's: pack discovery 2.19, workflow build 0.58, emission 0.43, other command work 0.41, pack host attachment 0.40, approval compile 0.31, launcher connection 0.18, source identity 0.15 and interpreter start 0.12 s. The collector's span is 5.14 s.

**B, start-up and imports** ([startup/](startup/), 7 samples each, installed venv Python 3.11.13):

| Measure | Median (s) |
| --- | ---: |
| `python -I -S -c pass` | 0.0109 |
| `python -I -c pass` | 0.0167 |
| `python -X utf8 -I -c pass` | 0.0144 |
| `run-astrid --version` (`sh`, then `run_astrid.py`, then an `exec` of the second interpreter) | 0.130 |
| `python -X utf8 -I -m astrid.omp_agent --version` (the second process only) | 0.099 |
| the thin client's whole round trip, ping mode | 0.0108 |
| `-X importtime` of the real `generate` (3 runs) | **0.866 total, 1,284 modules** |

The import self-time splits about evenly: astrid 0.26 s, vibecomfy 0.25 s, the standard library and other third-party packages 0.23 s, and numpy 0.07 s. The largest top-level imports are `astrid.core.execution.generic_host` 0.19 s, `vibecomfy.porting.emit.ui` 0.17 s and `astrid.core.generation.backends.comfy_schema` 0.11 s. `-X importtime` overstates the cost, and the command's own collector spreads these imports across its stages. The launcher hop adds about 0.03 s: the second interpreter's start, beyond `sh` and the first.

**D, where the 0.32 s of Cfull goes** (medians of server steps, run 2):

| Part | Seconds |
| --- | ---: |
| client interpreter start (`-I -S`) | 0.011 |
| client imports, Unix-socket connect and IPC (the ping minus a bare interpreter) | about 0.001 |
| **render: `emit_bundle` of the filled graph** | **0.203** |
| approval digests (`_vibecomfy_invocation_preflight`: three GETs of the objects, then a compile of the projection) | 0.025 |
| approval compile (`load_bundle` and `compile` against the target schema) | 0.025 |
| object POSTs ×3 (source, `workflow.py`, companion) | 0.017 |
| Runtime admission: `POST /v1/tasks`, round trip including the server's handling | 0.009 |
| capability lookup, `GET /v1/capabilities` | 0.008 |
| target node list and model resolution (product), plus the stub's own `/object_info` fetch | 0.005 + 0.002 |
| Runtime liveness, `GET /v1/health` | 0.004 |
| copy and slot fill, slot checks | 0.002 |
| server total / unattributed | 0.306 / about 0.003 |

The Runtime's own share is small: an object POST takes about 6 ms and the task admission 9 ms. Almost all of the floor is the render.

**What the render is made of.** From [render-profile.json](render-profile.json), cProfile on one warm `emit_bundle` (0.55 s profiled, against 0.20 s unprofiled): object-info class lookups take about a third (556 `_class_entry` lookups, which re-witness the files with 9,411 `stat` calls); `copy.deepcopy` takes about a quarter (68,150 calls); and canonicalisation and the sidecar take the rest. Holding a validated object-info generation in the host's memory, and making fewer copies, would probably bring the render under 0.1 s *est.*, but that is not measured. In the ten real-work samples the render's time varied: 0.20 to 0.29 s typically, and 0.80 s once.

## What the naive stub skips, and what each costs

| Skipped by the naive stub | What the product must keep | Measured, warm (s) |
| --- | --- | ---: |
| Re-rendering the graph. The companion's `generation_id` and the `source_bundle` line in `workflow.py` stay those of the warm-up graph | Render the current literals; RA-2's fill-then-render | 0.203 |
| The approval digests: `api_digest`, `semantic_digest`, `revision_id` and `workflow_content_digest` stay the warm-up's | Recompute them from the projection of the exact admitted bytes | 0.025 |
| The approval compile (pins, provenance, the capability fence, the target schema) | Its structural part can be cached; the slot values are checked per request | 0.025 |
| Slot checks (`resolve_entry_inputs`, `set_input`) | Every request | 0.002 |
| Target node-list fetch and model resolution | Every request until a real ComfyUI is measured (D3a) | 0.005 on the stand-in; **not measured on a real ComfyUI** |
| The source object POST, the capability lookup and Runtime liveness | Every request | 0.006 + 0.008 + 0.004 |
| The private output prefix | Not on the path to "queued": the worker scopes `filename_prefix` per attempt (`local_server_engine.py:240-255`) | 0 |

The stub plus these checks comes to 0.036 + 0.28 ≈ 0.32 s, which matches the measured Cfull median of 0.320 s.

**Not covered by any arm:**

- the per-command witness for a person's own and project packs, including the PB-7c refusal order (duplicate name before managed inventory, the pending transaction on a warm hit). The installed box has no own packs;
- model-root hashing on a managed target (`verify_files=True`);
- a real ComfyUI's `/object_info`, which can be several MB;
- checking the prepared graph's structure key on each hit;
- the rebuild on a miss (about 0.58 s);
- the claimed-machine refusal, which does not apply to an attached placement.

## Surprises

1. **A task with a stale approval receipt and a stale companion was admitted and succeeded.** In all 10 naive samples, `invocation_preflight` carried the warm-up graph's `api_digest` and `revision_id`, and the companion carried the warm-up's `generation_id`. The Runtime queued every task, and the worker ran the new prompt and seed. The stand-in's `/history` shows "variation k" and seeds 7011 to 7051 for run 1's naive arm, and every task ended `succeeded`. The worker's `_approve_live` recompiles from the admitted bytes, so what runs is what is in the bytes. But nothing downstream compares the receipt or the companion binding with those bytes, so a stale cache would produce a wrong record without any refusal. RA-2's differential test, and its rule that approval is derived from the admitted bytes, is therefore the only guard. It should not be relaxed on the assumption that the worker will catch a mismatch.
2. **Residency alone saves only about 1 s** (A 5.36 s against W 4.33 s). Run warm, today's code still repeats discovery (2.39 s), the build (0.51 s), attachment (0.21 s) and the launcher connection (0.20 s) on every call. Only the first-use costs fall: the approval compile from 0.31 to 0.02 s and the emission from 0.43 to 0.21 s. The gain comes from the host holding the prepared graph and the discovery results, not from the process staying alive.
3. **The command's session cannot read executors.** The stub's `GET /v1/executors/astrid-pack-host` was refused with "credential lacks required scope". The command reads it earlier, during attachment, under another identity. RA-1 must decide whose session the host admits the person's task with. The stub used a client-scoped session opened at the launcher boundary, as the command does; the pack host's executor session is a different thing.
4. **Today's command runs the invocation preflight three times:** the SDK, Workspace and Remote admission preflights, about 0.025 s each warm and 0.15 s on first use. A host needs it once.

## Recommendation for RA-1

Choose **resident first** (D1): the thin command line hands the request to the warm pack host, which holds the pack-host identity, the discovery and registry results, object-info trust and a prepared graph per structure key, and renders, checks and admits per request.

- It is the only route measured under 1 s (0.32 s with today's per-request checks), and the disk route's floor is still about 2.0 s *est.*
- Invalidation inside the host's lifetime is simpler than proving a cross-process disk hit current. Two checks are still needed on every command: the own-pack witness, with PB-7c's refusal order, and host liveness and compatibility. A client and host of different versions must refuse or fall back.
- Make RA-2's first target the render inside the host (0.20 s of 0.31). Make RA-4's first step a real ComfyUI's node-list cost, the largest unmeasured term.
- Fund disk caches afterwards, and only for the first command after a host restart.

## Files

- [scripts/](scripts/): the stub host, thin client, driver, Runtime request capture, B script, import-time parser, environment files and the install manifest.
- [run1/](run1/), [run2/](run2/): `records.jsonl`, `summary.json` and `console.log`.
- [startup/](startup/): interpreter and launcher timings, one `-X importtime` log of `generate`, the thin client's import log and the summary.
- [capture/](capture/): every Runtime request of two `generate` runs, as method, path, size and status, without bodies or credentials; and the host's validation lines.
- [render-profile.json](render-profile.json): the cProfile of one warm render.

The run folder `/root/plan82-floor/` (a 4.3 GB install) is left in place for re-runs. The stub host, the stand-in and the install's Runtime and pack host were stopped.
