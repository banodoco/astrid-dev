# Dry pod: plan for the cells and engine lanes

**Answer to Hannah.** Partly, and the part it covers is the part that has been failing. The pod's job is one chain of functions. Running that chain on a CPU catches failures caused by a *declared fact*: model records, graph, nodes, dependencies, launch. It cannot catch anything that needs real weights, a real GPU or the real provider, and it only covers graphs it actually builds. Of the eight failures in the brief, five are caught by the R13 slice plus checks that already exist, two more by the later engine stop, and one never. The final five-cell GPU run stays.

## What exploration found

- **Music tonight was a missing declaration.** `ComfyUIEngine.workflow_requirements` (`astrid/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py:145-173`) fills a template's missing digest from the lock by joining on `(destination, revision)`, with the revision taken from the URL. The template says `main`, the lock a commit, so the four rows stayed `sha256=None, size=None`; the pod's `preparation.prepare.stdout.log` shows them. `_verify_models` (`astrid/core/generation/managed_preparation.py:505-517`) then reports a null declaration as "bytes differ".
  - Hugging Face's metadata shows no sign of bad bytes: the template's repository redirects to the lock's, `main` is the lock's revision, and digest and size equal the lock's. The pod's own bytes are unproven either way.
- **SFX tonight fails on the pod only because the pod renders differently.** The pod calls `emit_bundle_with_candidate(..., source_format="ready_template")` (`managed_preparation.py:415`, also `astrid/packs/vibecomfy/local_job.py:109-120`), which reaches `_ready_requirements`. The host calls `emit_bundle` (`astrid/sdk/generation.py:1771`), the scratchpad renderer.
- **Dry-run already computes the pod's manifest and nobody judges it.** `generation.py:1755` puts `requirements` in the dry-run report; for music it carries the four null rows.
- **Scale:** 52 ready templates, 208 model declarations, 141 with no digest and a `main` URL. The lock holds 36 files, some (H3) owned by an Agent pack, not a template.
- **No real engine runs offline.** The Stage 2b repro (`tests/core/generation/test_engine_dead_owner.py`) uses real custody with a tiny HTTP engine; `tests/packs/h3_av/test_cpu_rehearsal.py` posts a real graph to a fake ComfyUI.

## 1. The design: one chain, three stops

Each stop is a function the pod also calls.

| Stop | What runs | Cost |
|---|---|---|
| **A. Declarations** | the pod's render loop (`ready_template`, then `scratchpad`), `workflow_requirements`, and the row test `_verify_models` applies | seconds, inside `--dry-run` |
| **B. Engine** | `install_engine`, `engine.align` (node restore, dependency sync, doctor), `_Runner.start` through custody, health and live `object_info`, on a packaged CPU recipe | minutes, cached |
| **C. Validated** | VibeComfy's live schema check, then ComfyUI's own `validate_prompt` on the built graph, with nothing queued | seconds more |

**One path.** Stop A is one helper, `judge_declarations(workflow, scratch, engine)`, extracted from `_prepare` lines 410-438 and from `_verify_models`. It takes no installed state. `_prepare` calls it; so does the dry-run branch, on the bundle reloaded as the pod reloads it. `scripts/preflight.py` already runs dry-run for every cell, so its `catalog` check goes red with no new harness.

**Model bytes.** Nothing is downloaded.
- *Record against source:* `POST https://huggingface.co/api/models/<repo>/paths-info/<revision>` returns the LFS sha256 and size, without auth, at a commit revision (checked on the music file). Small non-LFS files are fetched and hashed. A 401 marks the row "needs token".
- *Placement, for B and C:* VibeComfy `fetch` gets a transport seam (none exists, `vibecomfy/fetch.py:488`). A head-only transport runs the same URL and destination code and writes a sparse file of the declared size. Preparation runs in a named `dry` mode that skips byte verification and marks the report `verified: false`, as `trust` does; a real run refuses such a report.
- That real bytes match the record is proved only live.

**Declare once.** Each model record (repository, revision, path, subdir and name, sha256, bytes) has one owning pack: the VibeComfy template for a template's models, since it holds the widget value and is the only fetcher; the Agent pack for its own (H3 builds its assets from the lock, `astrid/packs/h3_av/shared/generation.py:170-180`). The Agent reads template records through workflow metadata, as `workflow_requirements` does now.
- `models.lock.json` becomes generated from all owners, with conflict detection and a "regenerate equals checked-in" test, beside `scripts/vibecomfy_pin.py`. The recipe keeps its digest of it.
- The `_pinned_locks()` fill is deleted once every consumer reads the owner. Until then a row it cannot fill is an error named "no declared digest".
- VibeComfy ratchet: records are pinned; the 141 unpinned ones sit in a quarantine that only shrinks. Gated entries stop skipping hash verification (`vibecomfy/fetch.py:222-267`).

## 2. Coverage

● caught, ◐ partly, ○ not caught.

| Failure in the brief | Where | |
|---|---|---|
| Music model-name requirement; SFX bare requirement and music digest (tonight) | A | ● |
| SFX socket types | the existing `schema` check | ● |
| TTS `pad_token_id` | the existing `constructor` check | ● |
| Engine start `request_mismatch` | B | ● |
| Engine start `endpoint_ownership` | B, run as claim-prepare then job-prepare on one root | ◐ |
| Watchdog termination denied | provider account state | ○ |

| Failure class | | Why |
|---|---|---|
| Declarations, digests | ● A | the pod's own resolver and row test; source metadata after R13 |
| Socket types | ● | recorded schemas now, live at C; 32 templates' recorded schemas lack commit provenance |
| Combo values, placement, paths | ◐ A, ◐ C | A proves the record. C proves the widget value, except where a node's own validator overrides the check |
| Node presence, imports, Python deps | ◐ B | real install, but CPU torch builds, not cu130 |
| Engine start | ● B | real custody and launch, on the CPU recipe |
| Model-load code | ◐ | only where a tiny-weights constructor test exists (TTS) |
| Downloads | ◐ | existence, auth, size; not throughput, disk or timeouts |
| Provider; GPU, VRAM, sm_120, fp8; output quality; timeouts | ○ | need the provider or the GPU. Plan 50's recordings cover provider shapes, not permissions |

| Workflow kind | | Limit |
|---|---|---|
| Image t2i and edit, video, multi-model, LoRA, path-qualified names | ● A, ◐ C | a LoRA is one more record and combo |
| Custom-node recipes | ● A, ◐ B | a pack that cannot import on CPU reports UNVERIFIED |
| Audio tts, sfx, music | ● A, ◐ C | TTS loads a model directory inside the node; validation does not prove loading |
| Gated or auth models | ◐ A | proves a token is needed, not that the pod has it |
| Video or audio inputs | ◐ | dry-run's synthetic media are invalid bytes (`scripts/catalog_dry_run.py:48`); real fixtures come with C, and decoding runs only at execution |

**Reach.** A covers the live cells and, under `--all-catalog`, catalog entries. Ready templates outside the catalog are covered only by VibeComfy's own test over every template (cells' ruling (c)), which must use the `ready_template` renderer.

**Smallest remaining live check:** the five-cell run, shaped to cover the rest. One fresh pod on the target GPU; the first cell exercises fresh install and start, the other four the warm path; lowest steps, size and duration; then an explicit release, which exercises the termination permission. It proves those five cells only. Any other workflow needs its own first live run.

## 3. Phasing

**R13 now: "declarations in dry-run".** Owner **cells**. Estimate 2–3 hours, unproven.

| Task | Route | Scope | Proof | Depends |
|---|---|---|---|---|
| DP-1 Shared helper; separate messages for "no declared digest" and "bytes differ" | N | `managed_preparation.py:_prepare`, `:_verify_models` → `judge_declarations` | `tests/core/generation/test_managed_preparation.py` | — |
| DP-2 Dry-run calls DP-1 and blocks on a fault | N | `astrid/sdk/generation.py:1745-1762` | `tests/core/generation/test_catalog_entries_dry_run.py`, `tests/scripts/test_preflight.py`. **Red then green:** at `58442e7a0` with VibeComfy `b3f20f3`, sfx and music fail with tonight's two causes and tts, t2i, edit pass; with DP-3 and the foley fix all five pass | DP-1 |
| DP-3 Pin the music template's four records | N | VibeComfy `ready_templates/audio/ace_step_1_5_t2a_song.py:25-29`; then re-pin with `scripts/vibecomfy_pin.py` | values equal `paths-info` at the lock's revision, recorded on the card; VibeComfy `tests/test_ready_templates.py` | — |

DP-2 green also needs cells' `r13/foley-requirement`.

**After R13,** in place of Plan 50's candidate follow-up "a real pod agent and a no-op CPU engine". RB-1 to RB-4 are unchanged: they cover the provider and Runtime, this the pod's job.

| Task | Route | Owner | Scope | Proof | Depends |
|---|---|---|---|---|---|
| DP-4 Source-metadata check in preflight | N | cells | `scripts/preflight.py:CHECKS`, new `check_sources` | `tests/scripts/test_preflight.py` with recorded responses | DP-2 |
| DP-5 Declare once | X | cells | lock generator beside `scripts/vibecomfy_pin.py`; `comfyui_engine.py:_pinned_locks`; VibeComfy `vibecomfy/fetch.py:verify` | regenerate-equals-checked-in; pin ratchet in VibeComfy `tests/test_ready_templates.py` | DP-2 |
| DP-6 Fetch transport seam, head-only transport, `dry` mode | X | cells | VibeComfy `vibecomfy/fetch.py:download_many`; Agent `managed_preparation.py:_verify_alignment` | VibeComfy `tests/test_fetch.py`; a real run refuses a `dry` report | DP-5 |
| DP-7 Stop B: packaged, verified CPU recipe and lock; real engine through custody, twice on one root | X | engine | `astrid/packs/runpod/lock-inputs`; `engine_runner.py:install_engine`, `_Runner.start` | integration case beside `tests/core/generation/test_engine_dead_owner.py`; fails on the parent of `8a425ee6b` | — |
| DP-8 Stop C: validate without queueing, by a route in the CPU recipe that calls ComfyUI's `execution.validate_prompt`; valid media fixtures | X | engine, with cells | CPU recipe extension; `astrid/core/generation/backends/comfy_target.py` | a wrong combo value and a wrong socket type are each refused; non-empty `node_errors` fails | DP-6, DP-7 |
| DP-9 Hosted CPU job on `int/*` | N | test | CI workflow; venv cached by lock digest | job green; UNVERIFIED rows listed | DP-8 |

## 4. Astra sense-check

One Astra run at high effort, told to use Luna helpers. It said it would use two; its transcript does not show the spawns, so that is unverified. Its verdict on the first draft was **reject as written**. This plan is the revision and has had no second review.

**Accepted:**
- `_prepare` needs installed receipts, so the stop A helper now stands alone and dry-run calls it.
- The check must render as `ready_template`, or it misses SFX.
- A CPU recipe derived at run time is refused by `engine_runner.py:228`. It is now packaged, and dependency coverage dropped to partial.
- Submit-then-interrupt races execution, because ComfyUI queues before answering. Stop C now validates without queueing.
- Placeholders reporting their declared digest made integrity evidence circular. Replaced by the `dry` mode.
- The lock has owners other than templates (H3). Ownership is per pack, and the fill stays until consumers migrate.
- `--all-catalog` does not reach every ready template, and synthetic media are invalid. Coverage narrowed.
- The R13 slice shrank: the Hugging Face check and stops B and C moved out.

**Rejected:** dropping the statement that Hugging Face shows no bad bytes. The metadata was read in this session and is reported as that, with the pod's own bytes marked unproven.

**Unverified, for cells to check first:** the counts of path-qualified (23, from the decision log), custom-pack, media-input and gated templates; and that the SFX error escapes the render loop's `WorkflowBundleError` fallback on the pod (no traceback was kept).
