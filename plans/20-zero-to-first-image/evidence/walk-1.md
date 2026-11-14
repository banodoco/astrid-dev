# P4.0 walk 1

[Plan](../plan.md) · [Tasks](../tasks.md) · [Inputs](../inputs.md)

Committed by the planning session from the phase 4 manager's message of 14 Nov 2026 (`session_011EzfW4R5yz8EETVbzZaLCF`). The manager's notes come first. The walker's text follows unchanged, except that HTML entities from the message transport are decoded (`&lt;` → `<`).

## Manager's notes

**Result: ready to tick.** Both runs were admitted on CPU against the fake ComfyUI.
- Run A, the user's saved UI workflow: about 20 min and 56 rows. About 15 min of that was Runtime and installer setup; the skill steps were 21 rows in about 4 min.
- Run B, the shipped default: about 14 min and 9 rows, mostly spent building the fake's node schemas. Its first block was an artifact of the fake.

**Manager rulings on the findings:**
- **P4.0.26 corrected after an independent read-only code review.** The worry was that a run on a person's own ComfyUI clears its queue or unloads its models. It does not.
  - On an attached target, Astrid sends `POST /queue {"delete":[id]}` only for prompt ids it submitted and recorded in its own attempt journal (`vibecomfy_local_server.py` `cleanup_prompts`; `comfy_target.py:296-307`). It sends `POST /interrupt {"prompt_id": id}` only while that prompt of its own is running.
  - The attached client refuses any other control body (`comfy_target.py:207-218`: "attached Comfy target refuses unowned control operations").
  - `{"clear":true}`, a bare `/interrupt` and `/api/free` exist only in `VibeComfyEngine` (`vibecomfy.py:930/1267/1286`, which nothing in Astrid constructs) and in the owned-engine release (`engine_custody.py:1422`).
  - The fake's six 21-byte `POST /queue` bodies are exactly `{"delete":["fake-1"]}`, because the fake always answers with prompt id `fake-1`. The two before admission cleaned up Run A's journal. The fake's request log has no `/api/free`.
  - **What remains is a low-severity finding:** when the person's ComfyUI refuses that scoped delete, the run fails with "managed session release was not verified". That message names neither the endpoint nor a fix. It goes to P4.6.1.
- **Routing:**
  - P4.0.25 and P4.0.26 → P4.6.1.
  - P4.0.7, P4.0.17 and P4.0.18 → P4.4, in flight.
  - P4.0.14 → P4.3, landed.
  - P4.0.15 → P4.2, in flight; its card tests that the saved placement alone is enough.
- **For P4.5 and P4.8 to decide:** P4.0.1, .3, .22, .23 and .24, the installer behind a proxy. Even with repository pins, the oh-my-pi tools stage needs `codeload.github.com`.
- **Housekeeping and environment notes, not product work:** P4.0.11, .12 and .13. They come from walking a source checkout instead of a real install.

---

# P4.0 walk 1: onboarding path on CPU against the fake ComfyUI (rewrite)

Outcome:
- Run A (user's saved UI workflow): admitted. `POST /prompt` reached the fake at 12:21:56Z, about 20 minutes after the walk started (12:01:54Z). Conversion evidence in section 5.
- Run B (shipped default image entry `qwen-image-2.1-turbo`): admitted at `POST /prompt` (1408 bytes) after the fake was extended with the template's core node classes (AST-extracted from ComfyUI eee5918) and the template's model files. Its first block (missing core nodes) was a fake artifact, not an Astrid gap.
- The real installer did NOT complete. It stopped at its tools stage (oh-my-pi source archive, HTTP 403). Everything after that ran on the sanctioned venv launcher (manager fallback rule).

Deviations, in one place:
- D1 Installer: the real `astrid.installer.cli` with a local manifest (`--manifest`, `repo` pins). Failed; see section 2.
- D2 Launcher: `launcher.sh` (the manager's `env -i ...` line) plus `ASTRID_RUNTIME_DATA_ROOT=<home>/.local/share/astrid-runtime` (needed, see P4.0.11). No `run-astrid` launcher exists. The installer did not create one.
- D3 Runtime: started with `astrid-runtime up --wait` after `astrid-runtime workspace create` with a source-profile JSON (`--hosted-origin off`, so no astrid.haus door; the "Connected" check in skill step 3 was not possible).
- D4 `vibecomfy` installed as a distribution: `pip install --no-deps <vibecomfy source>` (P4.0.13).
- D5 A project was created: `projects create p40-walk --name "P4.0 walk" --select` (P4.0.14).
- D6 Fake ComfyUI changed: (a) `control_after_generate` moved from a separate input to a stock-style option on `seed` (variant 2, used for Run A's admission; variant 1 kept); (b) for Run B only: the 13 core node classes of the template, AST-extracted from ComfyUI eee5918 (read-only), and the template's model filenames under `/models/diffusion_models`, `/models/text_encoders`, `/models/vae`; (c) `POST /queue` and `POST /api/free` answer 200 `{}` (the first version answered 404 and the backend's release failed, row B8). None of this is verified against a real ComfyUI server.
- D7 The skill's preinstall step and the curl installer were not run.

Versions:
- Checkout Agent `r13/compose` at `a371431db94a75b6a83bd57cb3068d51e9ce8b36`; tracked files clean.
- Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c` (runtime.lock.json; protocol `workspace.v1`, schema digest `sha256:9628bb5f...`, matching the hosted manifest's runtime schema digest).
- VibeComfy `d3850831265c54bb811808c2bc85c53ef5ac7ec9`, `vibecomfy` 2.8.0 as distribution.
- Lifecycle `7f0b025e9391baac9f5c2fb7393617ea6fef0704` (sanctioned env only; not in the installer manifest, P4.0.23).
- Python 3.13.18.
- Fake: `fake_comfyui.py` (ComfyUI 0.3.32 in `/system_stats`).
- Hosted install manifest (public GET, `https://astrid.haus/install-manifest.json`, release 12) used as the shape of the local-pin manifest.

Clock: walk start 12:01:54Z. Run A elapsed is from that time. Run B elapsed is from its own start (12:22:11Z).

Launcher shorthand: `L` = the sanctioned venv `python -m astrid` under `env -i` plus the data-root variable; `PY` = the same python (for `-m astrid.packs.vibecomfy.local`); `RT` = the sanctioned venv's `astrid-runtime`.

## 1. Run A command table

Rows 1-15 are the first venv attempt. Rows 16-26 are Runtime setup on the sanctioned env. Rows 27-33 are the real-installer attempts. Rows 34-56 are the skill steps and the admission.

| # | Command | Start (UTC) | Outcome |
|---|---|---|---|
| 1 | read `docs/setup/SKILL.md`; checkout log and status | 12:01:54 | checkout a371431, clean |
| 2 | `python3 -m venv <evidence>/venv` | 12:02 | ok |
| 3 | `pip install -e <checkout>` | 12:02 | exit 0; wrote ignored `astrid.egg-info/` into checkout (P4.0.9) |
| 4 | `python -m astrid --help` | 12:03 | census printed; generation lists `image`, `video` only |
| 5 | `ls <home>/.local/share/astrid` | 12:03 | No such file or directory |
| 6 | `python -m astrid install --help` | 12:03 | `No module named 'runtime_protocol'` |
| 7 | `python -m astrid status` | 12:03 | same |
| 8 | `python scripts/ci_install_runtime.py` | 12:04 | `ERROR: HTTP error 403 while getting https://github.com/banodoco/astrid-runtime/archive/6855dfa8....tar.gz` |
| 9 | proxy status check | 12:04 | proxy enabled; no reason for the 403 |
| 10 | search for `runtime_protocol` | 12:04 | copies under other workers' envs; not used |
| 11 | read `entries.py` (`describe_workflow`) and `production_engine.py` (`load_workflow_path`, `_canonicalize_ui_workflow`) | 12:05 | static reading (section 5) |
| 12 | read `scripts/worker-env/README.md`, `agent-setup.sh` | 12:06 | sanctioned env recipe read |
| 13 | fake smoke test | 12:03-12:05 | all endpoints answered |
| 14 | VibeComfy pin check | 12:05 | `d3850831...` |
| 15 | `git status --short --ignored` | 12:06 | ignored `astrid.egg-info/`, `__pycache__` |
| 16 | `L generate --help` (sanctioned env) | 12:06:40 | lists list, image, video, audio, describe, workflow, align, targets, launch, defaults, settings, release, failure |
| 17 | remove egg-info; write `launcher.sh`; `L status` | 12:06 | `workspace: unavailable`, `runtime: unavailable`, `next action: run the Astrid install line again` |
| 18 | `L status --json` | 12:06:51 | `runtime.support.catalog_missing`; discovery path under `<checkout>/.astrid-data/` (P4.0.11) |
| 19 | `RT doctor` | 12:07 | NOT OK; `Runtimes found 0 running` |
| 20 | `RT up --wait` | 12:07 | `No workspace is configured; run astrid-runtime workspace create or workspace attach.` |
| 21 | `RT workspace create ... --hosted-origin off` (no source manifest) | 12:07 | `Source profile manifest is missing or invalid` |
| 22 | write a source profile; re-run 21 | 12:07 | `Source profile protocol/schema is incompatible. Restart the runtime with a compatible source profile` |
| 23 | set `protocol_version` `workspace.v1`, `schema_version` `workspace-schema-v1` (from `bootstrap.py:43-44`); re-run 21 | 12:07 | `status: configured_create` |
| 24 | `RT up --wait` | 12:07:52 | started, `door_endpoint: http://127.0.0.1:17340` |
| 25 | `RT status`; `L status --json` | 12:08 | runtime healthy; `L status` still unavailable (wrong data root, P4.0.11) |
| 26 | add `ASTRID_RUNTIME_DATA_ROOT`; `L status` | 12:08 | `workspace: ready`, `runtime: ready` |
| 27 | public GET of `https://astrid.haus/install-manifest.json` | 12:08 | keys `schema_version, release, agent, runtime, tools, vibecomfy, lifecycle` |
| 28 | write a local manifest with `repo` pins | 12:08 | written |
| 29 | installer `--yes --manifest ... --autostart off --command on --skills on --skill-copies off` | 12:08:55 | `The lifecycle source repository does not match its reviewed identity.` / `Astrid was NOT installed` (P4.0.23) |
| 30 | remove the `lifecycle` key; re-run 29 | 12:09:01 | `Failed to download .../python-build-standalone/.../cpython-3.11.13...` (`invalid peer certificate: UnknownIssuer`) |
| 31 | set `tools.python` to 3.13.18; re-run | 12:09:14 | `Failed to fetch: https://pypi.org/simple/aiodns/` `invalid peer certificate: UnknownIssuer` (P4.0.22) |
| 32 | re-run with the proxy and CA variables passed through | 12:09:26 | past uv and dependencies; failed in the tools stage: `HTTP Error 403: Forbidden` at `astrid/installer/tools.py:162` (`_install_omp_source` → `fetch_archive`, `https://codeload.github.com/banodoco/oh-my-pi/tar.gz/78f0e096...`). `Astrid was NOT installed ... Nothing was installed.` (ended 12:16:21) |
| 33 | curl that URL | 12:16 | 403 |
| 34 | restart fake; `L status` | 12:17 | ready |
| 35 | read generation skill "Set up my generation" | 12:17 | read |
| 36 | `L generate defaults --json` | 12:17:36 | image.t2i = `qwen-image-2.1-turbo`, pack default |
| 37 | `L generate targets --json` | 12:17 | ready, `http://127.0.0.1:8188`, `location: local`, `owner: human` |
| 38 | `PY -m astrid.packs.vibecomfy.local scan` | 12:17:55 | found 8188, `workflows: ["my_portrait_custom.json"]` |
| 39 | `curl -s 127.0.0.1:8188/userdata/workflows%2Fmy_portrait_custom.json -o work/my_portrait_custom.json` | 12:18 | nodes CheckpointLoaderSimple, AstridCustomSampler, SaveImage |
| 40 | (asked) which tool is primary: their ComfyUI. `L generate settings checkout --file work/generation.json` | 12:18 | version 0 |
| 41 | edit `placement` to attached 8188; `settings checkin` | 12:18 | changed, version 1 |
| 42 | `L generate targets --json` | 12:18 | ready, 8188 |
| 43 | `L generate list --json` | 12:18:17 | 138 rows; `qwen-image-2.1-turbo` `target model probe unavailable` |
| 44 | (asked) default slots: not changed in Run A | 12:18 | not run |
| 45 | `L generate describe work/my_portrait_custom.json --json` | 12:18 | inputs `model`, `node:3.filename_prefix`; AstridCustomSampler's inputs absent |
| 46 | same, with the fake's request log cleared | 12:19 | fake log EMPTY: no `/object_info` during describe |
| 47 | `L generate workflow FILE --as-entry p40-my-portrait --dry-run --json` | 12:19 | `would_save_entry`, `written: false` |
| 48 | (asked) `L generate workflow FILE --as-entry p40-my-portrait --no-run --json` | 12:19:12 | `saved: true`, `ran: false`; no request to the fake |
| 49 | `L generate workflow FILE --placement http://127.0.0.1:8188 --inputs-json work/inputs-a.json --dry-run --json` (variant 1 fake) | 12:20 | blocked: `Node 2 (AstridCustomSampler) is missing required input control_after_generate.` Fake log: `/system_stats`, `/object_info`, `/object_info` |
| 50 | fake variant 2; same dry-run | 12:21 | ready |
| 51 | same as run, no project | 12:20:43 | `project is required for generation; pass --project <project> or select a current project in the workspace runtime` |
| 52 | `L projects create p40-walk --name "P4.0 walk" --select` | 12:20:51 | created, selected |
| 53 | same run | 12:20:51 | `packages:missing=vibecomfy` (P4.0.13) |
| 54 | `L doctor --json` | 12:21 | runtime compatible |
| 55 | `pip install --no-deps <vibecomfy source>` | 12:21:37 | vibecomfy 2.8.0 |
| 56 | same run | 12:21:37 | **Fake log: `POST /prompt` 342 bytes (ADMITTED 12:21:56Z)**; then `GET /history/fake-1` 404 (the fake lacks it), `POST /queue` x3 (cleanup). Exit 2: `HTTP Error 404: Not Found`, `local_server prompt cleanup failed: comfy target /queue request failed` |

Admitted: row 56, 12:21:56Z. About 20 min from walk start; about 4 min from the first skill step (row 36); about 14 min from the Runtime being ready (row 26). 56 rows, of which skill-path rows (36-56) = 21.

## 2. Real installer attempts

Four attempts: (1) lifecycle identity refusal; (2) uv could not download CPython 3.11.13 from GitHub; (3) uv could not reach PyPI (`invalid peer certificate: UnknownIssuer`, because `env -i` dropped the proxy and CA variables); (4) the tools stage got HTTP 403 for the oh-my-pi source archive. Result: `Astrid was NOT installed`; no launcher was created. `--yes` was used on the manager's direction; no real user answered the consent question. `--sandbox` was not used (OpenShell seccomp, not a no-service mode).

## 3. Run B command table (from 12:22:11Z)

| # | Command | Start | Outcome |
|---|---|---|---|
| B1 | `L generate defaults --json` (row 36) | - | image.t2i = `qwen-image-2.1-turbo` |
| B2 | `L generate list --json` | 12:22 | `ready: false`, `target model probe unavailable`, `target_kind: attached` |
| B3 | `L generate describe --entry qwen-image-2.1-turbo --json` | 12:22 | inputs seed, diffusion_model, text_encoder, vae, prompt, negative_prompt, width, height, ... |
| B4 | `L generate image --entry qwen-image-2.1-turbo --inputs-json work/inputs-b.json --placement http://127.0.0.1:8188 --dry-run --json` (fake without core nodes) | 12:22 | blocked: `Missing ComfyUI node CLIPLoader; install its locked node pack. Run: astrid generate align --apply --consent user_env --entry qwen-image-2.1-turbo` (same for UNETLoader, VAELoader) |
| B5 | hand stubs for the three loaders; same | 12:22 | 9 `missing_node_pack`: CFGGuider, EmptyLatentImage, KSamplerSelect, ManualSigmas, QwenImage21Cache, RandomNoise, SamplerCustomAdvanced, TextEncodeQwenImage21, VAEDecode |
| B6 | `L generate align --entry qwen-image-2.1-turbo` (inspect) | 12:23 | `No installed managed ComfyUI target; install ComfyUI before running astrid generate align` |
| B7 | 13 template classes AST-extracted from ComfyUI eee5918 into the fake; model filenames served; same dry-run | ~12:24-12:34 | ready |
| B8 | same, real run (fake: `POST /queue`, `/api/free` 404) | 12:35:13 | failed before admission: `managed session release was not verified` (`managed_tool_session.py:538-543`). Fake log: `POST /queue`, `GET /queue`, no `/prompt` |
| B9 | fake answers 200; same run | 12:35:54 | **`POST /prompt` 1408 bytes (ADMITTED between 12:35:54Z and 12:36:31Z)**; then `GET /history/fake-1` 404, then cleanup. Exit 2 on `/history` 404 (fake limit) |

Posted prompt: 13 nodes (UNETLoader, CLIPLoader, VAELoader, EmptyLatentImage 1024x1024, TextEncodeQwenImage21 "a lighthouse keeper", QwenImage21Cache, ManualSigmas, RandomNoise seed 1753952450, KSamplerSelect euler, CFGGuider cfg 1.0, SamplerCustomAdvanced, VAEDecode, SaveImage).

Run B: admitted, about 14 min (first blocker at about 1 min; building the fake's schemas took most of the time). 9 rows (8 run).

## 4. Minutes and command counts

| Run | Start | Admitted | Elapsed | Commands |
|---|---|---|---|---|
| A | 12:01:54 | 12:21:56 | ~20 min (setup ~15 min) | 56 rows (skill rows 21) |
| B | 12:22:11 | 12:35:54-12:36:31 | ~14 min (mostly fake work) | 9 rows |

## 5. UI-to-API conversion (Run A)

1. `describe` with `comfy_url=''` does not use the server schema: the fake's log was empty (row 46), and the output omits the custom node's inputs. `entries.py` `describe_workflow` calls `load_workflow_path(path, scratch, comfy_url='')`; `_canonicalize_ui_workflow` fetches `/object_info` only `if schema_url:`.
2. Conversion against the server schema happens at placement dry-run and run (`/object_info` requested, rows 49 and 56). The custom node survived: node 2 has `class_type: AstridCustomSampler`.
3. Variant 1 (separate `control_after_generate` input): dry-run blocked (row 49).
4. Variant 2 (`control_after_generate` as an option of `seed`): ready (row 50).
5. POSTed prompt: `"1": CheckpointLoaderSimple {"ckpt_name": "tiny-cpu-test.safetensors"}`, `"2": AstridCustomSampler {"cfg": 1.0, "model": ["1", 0], "seed": 1535184052, "steps": 4}`, `"3": SaveImage`. The saved `widgets_values` `[7, "fixed", 4, 1.0]` gave steps 4 and cfg 1.0, but seed became 1535184052 (not 7), and `control_after_generate` was dropped.
Verdict: converted against the server schema at dry-run and run, not at describe; the custom node survived. Not verified: how a real ComfyUI declares `control_after_generate`.

## 6. What this walk cannot show (for Plan 34)

- The real installer on a machine that can download GitHub archives (oh-my-pi, python-build-standalone) and PyPI with a trusted CA.
- The `run-astrid` launcher the installer creates.
- The "Connected" check with the astrid.haus door.
- A real ComfyUI's `/object_info`, `/models` and `/userdata`, including the `control_after_generate` shape (P4.0.17).
- A real ComfyUI's history and queue API (the fake has no `/history/<id>`).
- The managed ComfyUI install (`engines install`, `align --apply`).
- A real server's response to the scoped queue delete.
- A real image, timings, GPU checks and the RunPod path.
- Whether the saved seed is preserved (P4.0.18).

## 7. Findings

- P4.0.1: the skill's only install line has no checkout route; the working route is a manifest with `repo` pins (`astrid/installer/backend.py` 1339-1356), which the skill never mentions.
- P4.0.2 superseded (install artifact).
- P4.0.3: a person running a cloud agent behind a proxy hits the same 403 (GitHub archive for the Runtime). Fix: `repo` pins in the manifest. Stumble: the oh-my-pi source has no local route and still needs `codeload.github.com` (403), so the real installer cannot complete behind this proxy even with local pins. P4.5 or P4.8 should decide whether the docs or installer need a line.
- P4.0.4 recurs: no `run-astrid` launcher without a successful install.
- P4.0.5 open: the skill's preinstall step downloads `scripts/preinstall_setup_skill.py` from `main`; not run.
- P4.0.6 recurs: `python3 -m astrid --help` lists only `generate image` and `generate video`; the other generate verbs appear only in `generate --help`.
- P4.0.7 confirmed: `describe` makes no `/object_info` request and omits the custom node's inputs.
- P4.0.8 unreached: the skill's `nvidia-smi` check.
- P4.0.9: an editable install writes ignored `astrid.egg-info/` into the checkout.
- P4.0.10 resolved: the sanctioned env was used throughout.
- P4.0.11: a source checkout's CLI data root is `<checkout>/.astrid-data`; `status` says runtime unavailable until `ASTRID_RUNTIME_DATA_ROOT` is set.
- P4.0.12: `workspace create` needs a source-profile JSON with `workspace.v1` / `workspace-schema-v1`; the checkout ships none.
- P4.0.13: `vibecomfy` is not registered as a distribution on PYTHONPATH alone, so the Runtime reports `packages:missing=vibecomfy`.
- P4.0.14: generation with no project fails with "project is required for generation"; the skill never says to create one.
- P4.0.15: each generation command passed `--placement`; whether the saved placement alone is enough was not tested.
- P4.0.16: `generate targets` reports an attached 8188 as `location: local`, `owner: human` (ambiguous labels).
- P4.0.17: the `control_after_generate` shape decides whether a saved workflow converts and is ready.
- P4.0.18: the saved seed 7 became 1535184052 in the POSTed prompt; `control_after_generate` was dropped.
- P4.0.19: the post-admission failure is a fake limit (no `/history`).
- P4.0.20 fake artifact: core nodes not declared.
- P4.0.21 fake artifact: the align remedy only mattered because the fake lacked core nodes.
- P4.0.22: uv in the installer does not trust the proxy CA by default, and `env -i` strips `HTTPS_PROXY` and the CA variables.
- P4.0.23: the installer's lifecycle pin must be the canonical GitHub repository, so the local-pin route does not cover it.
- P4.0.24: the hosted manifest's `tools.python` is 3.11.13 (a GitHub download); 3.13.18 on the system avoided it.
- P4.0.25 (for P4.6.1): on an older ComfyUI that genuinely lacks core nodes, Astrid says "Missing ComfyUI node CLIPLoader; install its locked node pack. Run: astrid generate align --apply ...". These are core classes, so the right advice is "update ComfyUI".
- P4.0.26 (corrected by the manager; see above): on an attached ComfyUI, Astrid's only control requests are scoped deletes, and interrupts of its own witnessed prompt. When the person's server refuses that scoped delete, the run fails with "managed session release was not verified", which names neither the endpoint nor a fix.
