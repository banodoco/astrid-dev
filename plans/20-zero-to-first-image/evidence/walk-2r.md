[Plan](../plan.md) · [Tasks](../tasks.md) · [Inputs](../inputs.md) · [Walk 1](walk-1.md) · [Walk 2](walk-2.md)

Committed by the planning session from the phase 4 manager's message of 14 Nov 2026 (`session_011EzfW4R5yz8EETVbzZaLCF`). The walker's text follows unchanged, except that HTML entities from the message transport are decoded (`&gt;` → `>`).

---

# P4.9r: short re-walk of Runs A and B on the R13 candidate

Evidence folder: `/home/user/wt/p4-9-evidence/rewalk/`. `cmdlog.txt` has each command's start and end time (UTC, 2026-11-14). `out-LABEL.txt` holds each command's full output, with stdout and stderr kept apart (`out-LABEL.stdout`, `out-LABEL.stderr`). The fake's request log is `fake/requests.jsonl`, with a timestamp on every request and the body of every POST except `/prompt`. Posted prompt bodies are in `fake/prompts.jsonl`.
`L` = `rewalk/launcher.sh`. `RT` = `rewalk/rt.sh`, which runs `astrid-runtime` with the same environment as `L`.

## 1. Versions
- Candidate SHA `bea57349a4c1c364c9f88ff614956dd07b52cc1c` (`/home/user/wt/p4-9`, detached). Clean before and after the walk (`git status --short` was empty).
- Environment `/home/user/wt/p4-9.env`, unchanged: VibeComfy `dba38f86`, Runtime `6855dfa8`, Python 3.13.18.
- `HOME=/home/user/wt/p4-9r-home`. It was new and empty, so "My first project" was created again.

## Deviations (setup rows, not counted)
- R-D0. Same as walk 2: D1 (launcher instead of `run-astrid`), D2 (door port 17341, because walk 1's Runtime pid 9143 still holds 17340) and D6 (each "ask" was answered with the recommended option). The P4.9.1 temp-folder wedge was avoided as in D5: `TMPDIR` is set to `rewalk/tmp`, a new empty folder.
- R-D1. **Launcher cwd.** The first `defaults`, `targets` and `scan` (16:32:16-16:32:30) ran from cwd `/home/user/astrid-agent`. `python -m astrid` puts the cwd first on `sys.path`, so those three calls imported `/home/user/astrid-agent/astrid` (cb91903a) and not the candidate. In that code `generate scan` exits 2 with `astrid generate: error: argument command: invalid choice: 'scan' (choose from 'list')`, and `defaults` has no `ready` field. Those outputs are kept as `out-A{1,2,3}-*-WRONGCWD.*`. I added `-P` to the launcher's `python -m astrid` and ran the three again. Walk 1's and walk 2's launchers have the same weakness; walk 2 got away with it because it ran from the evidence folder. The real launcher (`astrid/installer/launcher.py:190`) uses `-I`, so this does not affect users.
- R-D2. Fake: walk 2's corrected fake, copied to `rewalk/fake/fake_comfyui.py`. It writes its logs under `rewalk/fake/`, puts a timestamp on each request, logs the body of each non-`/prompt` POST (for check 11), answers `POST /interrupt` with 200 like `/queue`, and logs any DELETE/PUT/PATCH. The full diff is in `rewalk/fake/fake-diff-vs-walk2.txt`. The model folders started empty, and `/object_info` loader choices follow the folder contents. I cleared the request log after two startup probes of my own (`/models/vae`, `/internal/folder_paths`), so it holds only the walk's requests.
- R-D3. No fake file server. `fetch-models` has no CLI option for another source. Its only source guard (`_token_safe_source`, `asset_gaps.py:208`) runs when the plan is built, and all three declared sources are `https://huggingface.co/...`, so the guard lets them through. The skill's path cannot be pointed at a local server, and `--apply` with the real digest would start a 16.10 GiB download from huggingface.co, which the brief forbids. **`--apply` was not run.** No refusal text exists to quote. See P4.9r.3.
- R-D4. Check 7's inputs. The brief's `{"prompt": ...}` is refused by this workflow, which has no `prompt` input (B3, below). I ran it again with walk 2's `{"model": "tiny-cpu-test.safetensors"}`, which also has no seed (B3b), and used the same base for check 8: `{"model": ..., "seed": 11}`.

## 2. Setup
| # | Command | Start | Outcome |
|---|---|---|---|
| F | fake on 127.0.0.1:8188 (`python3 -I rewalk/fake/fake_comfyui.py 8188`) | 16:31:56 | up; the three model folders empty (`/models/vae` -> `[]`) |
| S1 | `RT workspace create --source-manifest rewalk/runtime-profile/astrid.json --realm-root /home/user/wt/p4-9r-home/astrid-realm --door-port 17341 --json` | 16:32:04 | exit 0, `configured_create`, realm `75765088...` |
| S2 | `RT up --wait --door-port 17341 --json` | 16:32:08 | exit 0 (3 s), `started`, door `http://127.0.0.1:17341`, origin `https://astrid.haus` |

## 3. Run A (the default, `qwen-image-2.1-turbo`, slot `image.t2i`)
First skill step (valid code): 16:33:26 (`runA-skillstart.txt`). The first, wrong-cwd attempt started at 16:32:16 (R-D1).

| # | Command | Start | Outcome |
|---|---|---|---|
| (x) | `L generate defaults/targets/scan --json`, wrong cwd | 16:32:16 | not the candidate (R-D1); scan exit 2 `invalid choice: 'scan'` |
| A1 | `L generate defaults --json` | 16:33:26 | exit 0, 16 s. `image.t2i`: `"entry": "qwen-image-2.1-turbo"`, `"ready": false`, `"reason": "required models missing or ambiguous"` |
| A2 | `L generate targets --json` | 16:33:42 | exit 0. `status: ready`, `placement.resolved {"endpoint": "http://127.0.0.1:8188", "kind": "attached"}`, `source: discovery`, `location: local`, `owner: human` |
| A3 | `L generate scan --json` | 16:33:45 | exit 0. Server `http://127.0.0.1:8188`, `"workflows": ["my_portrait_custom.json"]`, `workflows_detail [{"modified": null, ...}]`; error for port 8000 only |
| A4 | `L generate settings set placement http://127.0.0.1:8188` | 16:33:50 | exit 0: `placement is now {"endpoint": "http://127.0.0.1:8188", "kind": "attached"} (was the built-in default); restore: astrid generate settings unset placement` |
| A5 | `L generate fetch-models qwen-image-2.1-turbo t2i --comfy-url http://127.0.0.1:8188` | 16:33:52 | exit 0, 4 s. Plan below, digest `2703c254e8d7ab3378d84d283242a5d36147037ff37cff1543d8cc99ce82a52c` |
| A5-apply | `... --apply 2703c254...` | not run | R-D3: the sources are huggingface.co and pass the guard, so this would download 16.10 GiB |
| SIM | `curl -X POST 127.0.0.1:8188/_test/simulate_download` (not an Astrid command) | 16:34:04 | three 20-byte stand-in files in the three folders (`out-SIM.txt`) |
| A5b | same plan command | 16:34:04 | exit 0: `Nothing is missing for qwen-image-2.1-turbo t2i on your ComfyUI at http://127.0.0.1:8188; it is ready.` |
| A1b | `L generate defaults --json` (extra cross-check) | 16:34:07 | `image.t2i` `ready: true`, `required model roles present (model bytes unverified)` |
| A6 | `L generate image --entry qwen-image-2.1-turbo --inputs-json rewalk/work/inputs-a.json --json` (`{"prompt": "a lighthouse keeper"}`) | 16:34:29 | exit 0, 30 s, `succeeded`. stderr line 1: `Created and selected project "My first project" for this generation.` The fake got **`POST /prompt` 1408 bytes at 16:34:58.121**. stdout parses as JSON and carries `"open_url": "https://astrid.haus/tools/video-editor?project=336de335b6924d89a2c232764a83cae6"`, `image_paths`, `seed_used: 0` |
| A6n | same plus `--no-wait --json` | 16:35:04 | exit 0. Admission (`state: queued`, `project_id 336de335...`) carries `"open_url": "https://astrid.haus/tools/video-editor?project=336de335b6924d89a2c232764a83cae6"`, the same URL. No project notice this time. The fake got `POST /prompt` 1408 bytes at 16:35:33 |

The plan (A5), exact text (`out-A5-plan.txt`):
```
Missing models for qwen-image-2.1-turbo/t2i on your ComfyUI at http://127.0.0.1:8188:
  qwen_image_2.1_turbo_int8_convrot.safetensors  6.76 GiB (7256787829 bytes)  -> /home/user/wt/p4-9-evidence/rewalk/fake/models/diffusion_models  (from https://huggingface.co/Comfy-Org/Qwen-Image-2.1/resolve/aacf31a6d48e707f352ecba714cee0680da3479b/diffusion_models/qwen_image_2.1_turbo_int8_convrot.safetensors, SHA-256 8144a0182964aa8403ad6dbc011db837304167d235161b9aabaa8532e967314c)
  qwen3vl_8b_int8_convrot.safetensors  8.71 GiB (9350798360 bytes)  -> /home/user/wt/p4-9-evidence/rewalk/fake/models/text_encoders  (from https://huggingface.co/Comfy-Org/Qwen-Image-2.1/resolve/aacf31a6d48e707f352ecba714cee0680da3479b/text_encoders/qwen3vl_8b_int8_convrot.safetensors, SHA-256 8bfd0f6e12abf2d2d697ecc888e5e90b0d6741d6708f05799f53afa560452e8f)
  qwen_image_2.1_vae_bf16.safetensors  0.63 GiB (675509688 bytes)  -> /home/user/wt/p4-9-evidence/rewalk/fake/models/vae  (from https://huggingface.co/Comfy-Org/Qwen-Image-2.1/resolve/aacf31a6d48e707f352ecba714cee0680da3479b/vae/qwen_image_2.1_vae_bf16.safetensors, SHA-256 bb21f7473051e1ac368515dd3f2e15cd44d7a11748ee8823e1ddca3e4876b7c9)
Total: 16.10 GiB (17283095877 bytes); free space: 18.41 GiB (19772940288 bytes), and 1.00 GiB (1073741824 bytes) more is kept free as a margin.
Nothing has been written. ComfyUI is not restarted and nothing else on it is changed.
To download exactly this, run: astrid generate fetch-models qwen-image-2.1-turbo t2i --comfy-url http://127.0.0.1:8188 --apply 2703c254e8d7ab3378d84d283242a5d36147037ff37cff1543d8cc99ce82a52c
```

## 4. Run B (the person's saved workflow: stock shape, `widgets_values [7, "fixed", 4, 1.0]`)
Start 16:35:38 (`runB-start.txt`).

| # | Command | Start | Outcome |
|---|---|---|---|
| B1 | `curl -fsS "http://127.0.0.1:8188/userdata/workflows%2Fmy_portrait_custom.json" -o rewalk/workB/workflow.json` | 16:35:38 | ok |
| B2 | `L generate describe workB/workflow.json --placement http://127.0.0.1:8188` | 16:35:38 | exit 0. Inputs `model (string; optional, default=null)`, `seed (integer; optional, default=null)`, `node:3.filename_prefix (string; optional, default="ComfyUI")` |
| B3 | `L generate workflow workB/workflow.json --placement ... --inputs-json workB/inputs.json --json` (`{"prompt": "a lighthouse keeper"}`, as in the brief) | 16:35:49 | exit 2, `blocked`, `input_rejected`, `unsupported entry inputs: prompt`. Nothing posted (R-D4) |
| B3b | same with `workB/inputs-model.json` (`{"model": "tiny-cpu-test.safetensors"}`, no seed) | 16:36:04 | exit 0, `succeeded`, same `open_url`. **The posted node 2 is `AstridCustomSampler {"cfg": 1.0, "model": ["1", 0], "seed": 7, "steps": 4}`** (`POST /prompt` 330 bytes, 16:36:22.560). Result `seed_used: 0` |
| B4 | same with `workB/inputs-seed11.json` (`{"model": ..., "seed": 11}`) | 16:36:24 | exit 0, accepted, `succeeded`. **Posted `seed: 11`** (331 bytes, 16:36:43.071). Result `seed_used: 0` |
| B5 | copy `workB/workflow-randomize.json` (`widgets_values [7, "randomize", 4, 1.0]`) with `inputs-model.json` | 16:36:50 | exit 0, `succeeded`. **Posted `seed: 1684653229`** (not 7; 339 bytes, 16:37:08.740) |
| C1 | `L generate workflow workB/workflow.json --as-entry p49r-my-portrait --dry-run --json` | 16:37:14 | exit 0. `would_save_entry: p49r-my-portrait`, `written: false`, inputs `model`, `seed` (integer, default null), `node:3.filename_prefix`. Same as B2 |
| C2 | `L generate workflow workB/workflow.json --as-entry p49r-my-portrait --no-run` | 16:37:20 | exit 0, `{"entry": "p49r-my-portrait", "ran": false, "replaced": false, "saved": true}`. **Wall time 9.03 s** (`wall-asentry.txt`; walk 2: 7.76 s) |

## 5. Teardown
| # | Command | Start | Outcome |
|---|---|---|---|
| S3 | `RT down --json` | 16:37:54 | exit 0, `status: stopped`, `idle.safe: true`, `task_count: 0` |
| F-stop | kill the fake (pid 23288) | 16:38 | stopped |
| probe | Python socket probe (`port-probe-end.txt`) | 16:38:24 | `8188 free (bind ok)`, `8188 connect: refused`; `17341 free (bind ok)`, `connect: refused` |

The first bind attempt right after the kill failed with EADDRINUSE while connect was already refused (TIME_WAIT). The bind succeeded on the retry loop by 16:38:24. No `p4-9r` or `rewalk` process remains. Walk 1's Runtime (pid 9143) and host (21539) are untouched, and so is `/tmp/astrid-attempt-cp95sr10`.

## 6. Checks
| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | `generate scan` through the launcher lists the fake and its saved workflows (R4.1) | **PASS** | `out-A3-scan.txt`: `"url": "http://127.0.0.1:8188"`, `"workflows": ["my_portrait_custom.json"]`. (The wrong-cwd run of the older code failed, R-D1.) |
| 2 | `defaults` with empty folders: `ready: false`, "required models missing or ambiguous" (R4.H) | **PASS** | `out-A1-defaults.stdout` slot `image.t2i`: `"ready": false, "reason": "required models missing or ambiguous"` (walk 2: `ready: true`) |
| 3 | `settings set placement` prints the restore line | **PASS** | `out-A4-set-placement.txt`: `...; restore: astrid generate settings unset placement` |
| 4 | Plan lists three files, sizes, folder, total; `--apply` behaviour; after the simulated download, the exact "Nothing is missing" line (R4.H) | **PASS** (apply part not run) | `out-A5-plan.txt` (3 files, sizes, folders, `Total: 16.10 GiB`); `--apply` neither stopped at the guard nor could use a fake server: the sources are huggingface.co, so it would download from HF and was not run (R-D3); `out-A5b-plan-after-sim.txt` line is exactly `Nothing is missing for qwen-image-2.1-turbo t2i on your ComfyUI at http://127.0.0.1:8188; it is ready.` |
| 5 | `generate image` admitted, `open_url`, project created with one notice; `--no-wait --json` admission carries the same `open_url` (R4.I) | **PASS** | `out-A6-image.*` (stderr notice once, `open_url ...project=336de335b6924d89a2c232764a83cae6`, fake `POST /prompt` 16:34:58); `out-A6n-image-nowait.stdout` (`state: queued`, same `open_url`) |
| 6 | `describe --placement` lists `seed` | **PASS** | `out-B2-describe.txt` |
| 7 | No seed in inputs: the posted seed is 7 (R4.G) | **PASS** (with `{"model": ...}`, R-D4) | `out-B3b-workflow.*`; `fake/prompts.jsonl` row 3: `"seed": 7`. With `{"prompt": ...}` as in the brief: refused, `out-B3-workflow.txt` |
| 8 | `"seed": 11` accepted, and 11 arrives (R4.G) | **PASS** | `out-B4-seed11.*`; `prompts.jsonl` row 4: `"seed": 11` |
| 9 | `randomize` copy: the seed is not 7 | **PASS** | `out-B5-randomize.*`; `prompts.jsonl` row 5: `"seed": 1684653229` |
| 10 | `--as-entry --dry-run` lists the same inputs as `describe`, including `seed`; wall time of `--no-run` | **PASS** | `out-C1-asentry-dry.txt` (model, seed, node:3.filename_prefix); `out-C2-asentry-save.txt`; 9.03 s |
| 11 | Only GETs, `POST /prompt`, and `/queue` or `/interrupt` scoped to Astrid's ids reached the fake | **PASS** | `check11-requests.txt`: 97 requests. 81 GETs, 5 `POST /prompt`, 10 `POST /queue`, each `{"delete":["fake-N"]}` for N = 1..5 (Astrid's own ids, two per run), 1 `POST /_test/simulate_download` (my curl, SIM row). No `/api/free`, no `/interrupt`, no `clear`, no DELETE/PUT/PATCH. Violations: `[]` |

## 7. Minutes and command counts
| | Walk 1 (user's workflow) | Walk 2 Run A | Walk 2 Run B | Walk 2r Run A | Walk 2r Run B |
|---|---|---|---|---|---|
| First skill step to first admitted `POST /prompt`, measured | ~4 min (12:17:36-12:21:56) | 15.3 min (~14 of it P4.9.1) | ~0.5 min (15:38:21-~15:38:45) | **1.5 min** (16:33:26-16:34:58); 2.7 min counting from the wrong-cwd start 16:32:16 | **0.7 min** (16:35:38-16:36:22), including the refused `prompt` attempt; ~0.3 min from B3b |
| Skill-path commands, clean path | 21 | 6 (+1 apply, not run) | 3 | 6 Astrid (defaults, targets, scan, settings set, plan, image) + 1 apply not run + 1 simulate | 3 (curl, describe, workflow) |
| Commands as issued | 21 | 11 Astrid + ~8 diagnostic | 3 | 12 Astrid (3 wrong-cwd, A1-A6, A5b, A1b, A6n) + 1 curl | 8 (curl, describe, B3, B3b, B4, B5, C1, C2), of which 4 are check-only (B4, B5, C1, C2) |
| `--as-entry --no-run` wall time | - | - | 7.76 s | - | 9.03 s |

## 8. Status of walk-2 findings on bea57349
- P4.9.3 (`defaults` said ready with empty folders): **fixed** (check 2). After the simulated download it says `ready: true` (A1b).
- P4.9.4 (saved seed lost; `seed` offered, then refused): **fixed** for the stock shape on this fake (checks 6-10).
- P4.9.5 (project notice in the JSON stream): **fixed**. The notice is on stderr (`out-A6-image.stderr`) and stdout parses as JSON.
- P4.9.1 (stale `astrid-attempt-*` in the shared temp folder wedges the host): not retested. Avoided by `TMPDIR` (R-D0).
- P4.9.2 (door port held by another Runtime): still present, same workaround.

## 9. New findings
- **P4.9r.1 `seed_used` is `0` in every result, whatever seed was posted.** Evidence: B3b posted 7, B4 posted 11, B5 posted 1684653229, and all three results say `"seed_used": 0` (A6 says 0 too, while its `workflow_inputs` held `"seed": 4180292540`, `out-A6n-image-nowait.stdout`). A person or agent that reads `seed_used` to reproduce an image gets the wrong number. I did not trace why. It may come from the fake's `/history` shape, so check it on a real ComfyUI before fixing.
- **P4.9r.2 The skill says `settings set placement` "creates a project if there is none", but the project was made by the first `generate image`.** Evidence: A4's output says nothing about a project, and A6's stderr says `Created and selected project "My first project" for this generation.` The result is fine (one project, one notice). Only the skill line is wrong about when the project is made.
- **P4.9r.3 `fetch-models --apply` cannot be exercised end to end without huggingface.co, and the plan's "source guard" never refuses the default's own sources.** Evidence: `asset_gaps.py:208` `_token_safe_source` allows only `https://huggingface.co`, every declared source is huggingface.co, and the CLI has no option for another source. So on the skill's path, `--apply` either downloads 16.10 GiB from HF or is not run. The hash check, staging, `.astrid-partial` rename and `file_exists` refusal have still never run outside unit tests in phase 4. This belongs in Plan 34's real run, or in a test-only source override.
- **P4.9r.4 (walk harness, not product) Walk launchers that run `python -m astrid` without `-P`/`-I` pick up an `astrid/` package in the cwd.** Evidence: R-D1. From `/home/user/astrid-agent` the walk launcher ran cb91903a code, and `generate scan` failed there with `invalid choice: 'scan'`. Walk 1's and walk 2's results stand, because they ran from their evidence folders. The product launcher uses `-I`. Future walks should use `-P`.
- P4.9r.5 (minor) Before returning, each finished run sends the same scoped `POST /queue {"delete": ["fake-N"]}` twice (five runs, ten deletes). It does no harm, because it is scoped to Astrid's own ids, but it is a duplicate request.
- P4.9r.6 (minor) The brief's check-7 input `{"prompt": ...}` does not apply to this saved workflow (it has no prompt input). The run refuses it clearly: `input_rejected`, `unsupported entry inputs: prompt`. The skill still never says what goes in `inputs.json` for a saved workflow (walk 2 guess 5). The answer is the `describe` list.

## 10. Still needs a real ComfyUI (Plan 34)
Real `/object_info` shapes (stock `control_after_generate` on `seed`), `/history` and `seed_used`, a real `fetch-models --apply`, the installer and `run-astrid`, and the astrid.haus "Connected" check. Nothing remote or paid was called. No RunPod, no `astrid machines`, no HF download, no GPU.
