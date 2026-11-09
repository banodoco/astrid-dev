# Tasks — One generation path

[Plan](plan.md) · [Inputs](inputs.md)

Routes: `N` is the default, `X` very hard, `S` super hard ([run contract](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings)). An `X` or `S` lead delegates reading, mechanical edits and running checks to `N` helpers and keeps the judgment and the final change.

**Rules for every task:**
- Each task deletes what it replaces in the same change, so no task leaves two ways of doing one thing.
- Write each new test first and see it fail on the base. Run only the selectors named in the task.
- **CPU only** (owner, 8 Nov): no paid pod, no GPU, no real model download, no provider call.
- Rename a glossary term ([inputs.md](inputs.md#planning-evidence)) in the task that touches it, not in a separate pass.
- The three extension points follow [Plan 17](../17-vibecomfy-extensibility/plan.md)'s protocol (`astrid/core/extensions`). Declare only the points named here, and add no versions, priorities or entry-point discovery.
- Changes to the Placement or `run` shape after T5 need [Plan 12](../12-multiple-inference-routes/plan.md)'s owner informed.
- Start only on the owner's go.

**Base.** Start from Plan 33's landed revisions, as recorded in [Plan 33's inputs](../33-unblock-live-generation/inputs.md#source-identities) at its U9. Today those are Agent `5eac07e3f` plus Plan 33's commits, VibeComfy `e65f4941`, Runtime `b983b04` and lifecycle `f2948817`. Record the exact SHAs in [inputs.md](inputs.md#source-identities) before T1. There is one Agent candidate branch; each task starts from the head the previous task left on it. VibeComfy changes (T4, T6b) go on one VibeComfy branch from its pin, and the Agent repins it in the same task.

Selectors below exist at Agent `5eac07e3f` or VibeComfy `e65f4941`, or are new files that the task (or Plan 33) creates. Agent checks use `PYT` and `PYT_POD` as defined in [Plan 33's tasks](../33-unblock-live-generation/tasks.md). VibeComfy checks use `bash "$ENV/vc-pytest.sh" -q` from the VibeComfy checkout, written `VCT` below, after `vc-setup.sh` ([env README](../02-consistent-generation/env/README.md)).

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| [T1](#t1-characterize-every-capability) Characterize every capability that calls generation, under local, attached and RunPod | N | Plan 33's U3 and U4 landed (they edit the same `SLOTS` and `REFUSALS` symbols); supersedes Plan 34's first pass (owner, 8 Nov) | `tests/integrations/test_runpod_slot_path_cpu.py` (from Plan 33 U1), `tests/core/generation/test_runpod_engine_selection.py` | Every capability is a case; current failures are recorded as strict `xfail` with the reason | started 8 Nov 01:00Z: N worker `session_011EzfVzhN9u5vhD1RvK4qo9` on `plan32/t1-characterize` (4290ee8, int/32 at 66e4777 plus Plan 33 U3+U5 at 2db4c88, merged early per the advisor, since U3 has not yet landed in int/33) |
| [T2](#t2-one-requirements-manifest-and-the-engine-point) One requirements manifest; the `generation.engine` point with ComfyUI as its one contribution | X | T1 | `astrid/core/extensions/{model.py,schema/point.json}`, new `astrid/packs/generation/extensions/points/engine.yaml`, new `astrid/packs/vibecomfy/extensions/generation.engine/comfyui.yaml`, `astrid/core/generation/{entries,asset_alignment,engine_readiness,engine_recipe}.py`, `astrid/core/pack/schemas/v3/pack.json`, `astrid/packs/h3_av/shared/generation.py`, and their tests | New `tests/core/generation/test_requirements_manifest.py`; `tests/core/extensions`; the readiness and alignment nodes below | T2a merged to `int/32` at `66e4777` (X worker `session_011EzfW2DmXnu72Y984yPcSd`); the manifest (T2 rest) waits on T1 |
| [T2b](#t2b-one-base-engine-comfy-packs-deleted) One base engine; the `comfyui` and `comfy_wrap` packs deleted | X | T2, T3 (shared `sdk/generation.py`; T3 first) | `astrid/packs/{comfyui,comfy_wrap}` (deleted), `astrid/packs/{runpod,vibecomfy}` recipes and locks, `astrid/packs/engine-index.json`, the engine and pack names in core, sdk, registries, docs and tests, and the App's `comfy_wrap` references | One engine row per platform; the PK-15B absence and engine selectors below; no `vibecomfy-h3`, `comfy_wrap` or `packs/comfyui` literal outside history (grep) | [ ] |
| [T3](#t3-one-placement-with-default-and-override) One Placement value, with default and override | X | T1; an independent review of the Placement and lease design (the advisor) | `astrid/core/generation/engine_contracts.py` (`Placement`), `astrid/sdk/{generation,invocation}.py`, `astrid/core/generation/{cli,targets}.py`, `astrid/core/generation/backends/registry.py`, `astrid/core/execution/generic_host.py` (target_policy), `astrid/packs/vibecomfy/actions/run/run.py`, `astrid/packs/h3_av/actions/transform/run.py`, and their tests | New `tests/core/generation/test_placement.py`; one decision site (grep); dry run equals live | [ ] |
| [T4](#t4-the-local-run-path-with-one-align) The local run path, with one `align` | X | T2b | `astrid/packs/vibecomfy/{local_server_engine,production_engine}.py`, `astrid/packs/vibecomfy/actions/run/run.py`, `astrid/core/generation/backends/vibecomfy.py`, `astrid/core/generation/asset_alignment.py`, `astrid/core/engine_cli.py`; VibeComfy `vibecomfy/runtime/session.py` (`ensure_models`) | New `tests/core/generation/test_run_local.py`; one submit and one retrieve function (grep); the VibeComfy nodes below | [ ] |
| [T5](#t5-runpod-as-a-remote-machine-the-generationmachine-point) RunPod as a remote machine: the `generation.machine` point | S | T4 | New `astrid/packs/generation/extensions/points/machine.yaml`, new `astrid/packs/runpod/extensions/generation.machine/runpod.yaml`, `astrid/packs/runpod/{adapter,generation,remote_placement,target_selection,installed_session}.py`, `astrid/packs/runpod/h3_release*.py`, `astrid/core/generation/{model_downloader,engine_runner}.py` (the downloader and model steps), `astrid/core/execution/generic_host.py` (bind), `astrid/packs/vibecomfy/local_server_engine.py` (inventory channel), and their tests | New `tests/integrations/test_remote_machine_cpu.py` (every slot and h3_av, warm reuse, volume, a test machine contribution); no controller-side model check for RunPod (grep); remote progress reaches the local run while the job runs, and cancel stops the job and releases the machine | [ ] |
| [T6](#t6-one-generate-and-the-vibecomfyworkflows-point) One `generate`; the `vibecomfy.workflows` point and its hooks | X | T5 | New `astrid/packs/vibecomfy/extensions/points/workflows.yaml`, `astrid/sdk/{generation,invocation}.py`, `astrid/core/generation/{entries,preflight,delivery}.py`, `astrid/core/generation/backends/{registry,vibecomfy_workflow}.py`, and their tests | One `run()` site calls `build` and `finalize`; the file-map input type; no modality branch (grep); `tests/core/extensions`; T5's harness green | [ ] |
| [T6b](#t6b-h3_av-becomes-one-contribution) h3_av becomes one contribution; the legacy RunPod route deleted with its last caller | X | T6 | `astrid/packs/h3_av/**`, new `astrid/packs/h3_av/extensions/vibecomfy.workflows/h3.yaml`, `astrid/packs/runpod/{remote_placement,prepared_task}.py` (h3 parts), `astrid/core/execution/{worker_qualification,generic_host}.py`, `astrid/core/generation/{delivery,preflight}.py`, `astrid/sdk/invocation.py`, `astrid/packs/vibecomfy/{endpoint_checkout.py,actions/run/run.py}`, `astrid/core/generation/backends/registry.py`, `astrid/sdk/generation.py` (`workflow(placement=)`); VibeComfy `node_packs/_defs.py` (H3 row) | The Matrix request on the CPU fake; `grep -ri h3 astrid/core astrid/sdk` empty; no stage graph, journal, receipt, input bundle or legacy route left (grep) | [ ] |
| [T8](#t8-completion) Completion | N | T1–T6b, R | astrid-dev completion PR | The PR links the implementation PRs, the integrated revision, the CPU evidence and a disposition for F-003 | [ ] |
| R Review rounds (at most 3, owner-agreed) | S | T1–T6b | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | [ ] |

**T7 (live proof). Deferred:** the live proof of this plan is a later pass of [Plan 34](../34-real-gpu-proof/plan.md) (real-GPU proof), which follows [Plan 33](../33-unblock-live-generation/plan.md). The owner decided on 8 Nov that Plans 33 and 32 are CPU only; see [inputs.md](inputs.md#owner-decisions). T8 does not wait for it.

**Sequence (manager, 8 Nov; advisor-reviewed).** A dependency is a needed result or a shared symbol, not a shared file. T3's entry gate is done (see its card); T3 starts as soon as T1 lands.

| Step | Tasks | Waits on | Parallel with |
| --- | --- | --- | --- |
| 0 | Environment smoke passes on `int/32-one-generation-path` | the astrid-agent wrapper fix | nothing |
| 1 | **T2a**: `generation.engine` point, ComfyUI contribution, registry loading; no caller switched | step 0 | T1 |
| 2 | **T1** | Plan 33's U3 and U4 landed | T2a |
| 3 | **T2 manifest** (rest of T2): `requirements()` and the engine table | T1, T2a | T3 |
| 4 | **T3**: one Placement value, default and override | T1 | T2 manifest |
| 5 | **T2b**: one base engine, comfy packs deleted. Chained to T3 only if a symbol check finds a shared function, which is then named here. | T2 manifest (and T3 only if that check finds a shared function) | T3 |
| 6 | **T4**: local run path with `align` | T2b | nothing |
| 7 | **T5**: RunPod as a remote machine | T4 | T6, if their symbols are disjoint |
| 8 | **T6**: one `generate`, `vibecomfy.workflows` point. Needs T4's single `run()`, not T5's result. | T4 | T5, if their symbols are disjoint |
| 9 | **T6b**: h3_av as one contribution | T5 and T6 | nothing |
| 10 | **R** review rounds, then **T8** completion | T1–T6b | nothing |

**Critical path:** Plan 33 U3 and U4 → T1 → T3 → T4 → T5 → T6b → R → T8. T6 runs in parallel with T5 once T4 lands, if their symbols are disjoint, and T6b waits for both. T2a runs now, in parallel with the open Plan 33 work.

**Manager state (run `plan32-2026-11-08-m1`, 8 Nov 2026, updated at T2a's merge).**
- Access: astrid-agent push access **granted** by the owner. astrid-app and vibecomfy push access **granted** on the owner's retry; both are cloned for later tasks.
- `int/32-one-generation-path` is **cut** at `8df5c09c2` from the head of `int/33-unblock-live-generation`, and now at **`66e4777`** (T2a fast-forwarded in).
- Environment: smoke **passed** (33 passed on `int/32` at `8df5c09c2`, via the `agent-setup.sh` then `agent-pytest.sh` path, because the `astrid-agent-pytest` wrapper is broken until the fix in astrid-dev #145 reaches the environment).
- T2a: **merged** to `int/32` at `66e4777`. Its worker reported both proofs passing: `tests/core/extensions` and `tests/core/generation/test_runpod_engine_selection.py`.
- Plan 33: U3+U5 and U2 landed on `int/33`. `int/33` is at `a105de3a` (main-merged, landing only). `int/33` is merged into `int/32`, now at `372f34fb1`. The overlap rule has ended.
- T1: `plan32/t1-characterize` pushed at `af2ffae`. Per the advisor, the 17 red cells are **characterized, not xfailed**: each asserts today's actual refusal or error, with a `# T1 characterization: flips in T<n>` comment. (The repo's skip guard turns xfail into failures, `tests/lanes.py:246`.) T1 merges into `int/32` when it is green.
- Dispatched 8 Nov, 02:41Z, each cut from T1's head merged with `int/33`, so they have the harness, and each merges after T1:
  - T3 (X, Placement): `plan32/t3-placement`, worker `session_011EzfW2k9PnrwJ5yrqnVXnT`.
  - T2 manifest (X): `plan32/t2-manifest`, worker `session_011EzfW1odTqKuC8ycfPKmfq`. Builds on T2a's engine point already on `int/32`.
  - App `--placement` rename (X): `plan32/t3-app-placement` cut from astrid-app `main`, worker `session_011EzfW15EYWoDKwCtDsn2Qj`.
- Owner decisions, 8 Nov, relayed by the advisor:
  - No GPU validation of Plan 33's route. Plan 34's first pass is dropped, and Plan 32 goes as fast as possible.
  - Plan 33 U4 (h3_av) is stopped and U7 (reuse window) is cancelled; both are superseded by T6b and T5. Plan 33 finishes U2, U3 with U5, U6, one review round, then U9.
  - T1 now waits on Plan 33's U3 only (not U4). Start T1 when U3 lands in `int/33`, merging `int/33` into `int/32` first.
  - Once Plan 33's U9 lands, the Plan 33 overlap rule ends and Plan 32 runs at full parallelism under its sequence table.
  - New Plan 32 work: make MiniMax H3 the default video entry. It was Plan 33 U4's data change, and it belongs with T6, where defaults move into contributions.
- Overlap rule while Plan 33 is open: dispatch only tasks that touch no function an open Plan 33 task touches, and ask the advisor before anything in `sdk/generation.py`, `remote_placement.py`, `adapter.py`, `generic_host.py` or `local_server_engine.py`.

## T1 Characterize every capability

**Outcome:** the CPU tests name every capability that reaches generation, so later tasks see what they break. **Authority:** CPU only.

1. Step 0, census: `git grep -nE "GenerationFacade|sdk\.generation|invoke(_result)?\(\s*['\"]vibecomfy\.run|['\"]h3_av\.transform" -- astrid ':!astrid/sdk/generation.py'`. List each capability, pack action or SDK caller in the commit body.
2. Add one case per capability to Plan 33's `tests/integrations/test_runpod_slot_path_cpu.py`, parametrized over `{local-managed, attached, runpod}`. Extend `tests/core/generation/test_runpod_engine_selection.py::test_default_slot_resolves_to_requested_target_or_refuses` the same way.
3. A case that fails today becomes `pytest.mark.xfail(strict=True, reason=...)` naming the task that fixes it, never a skip.

**Proof:** `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py` and `PYT tests/core/generation/test_runpod_engine_selection.py` pass, with the recorded `xfail`s.

## T2 One requirements manifest and the engine point

**Outcome:** `requirements(entry, inputs) -> {engine, base, models[name, subdir, url, sha256, size], extra}` (`extra` owned by the engine; ComfyUI: `nodes[repo, commit]`), one row shape, and the engine table built from `generation.engine` contributions. **Authority:** CPU only.

**Delegate to N helpers:** the census of requirement shapes, the schema and YAML files, the test nodes and the checks.

1. **Switch the protocol on for the Agent.**
   - Allow `side: agent` in `astrid/core/extensions/schema/point.json:11` and `model.py:86,428`.
   - Declare `astrid/packs/generation/extensions/points/engine.yaml` (cardinality `many`). Its data is `platforms -> recipe`, and its protocol is `requirements(entry, inputs)`, `align(manifest, mode)`, `execute(job) -> files in job.out`, `cancel(job)` and an optional `probe(endpoint)`.
   - Contribute `astrid/packs/vibecomfy/extensions/generation.engine/comfyui.yaml`.
   - `run()`'s engine table is the registry's contributions for this point. Only `vibecomfy.comfyui` exists in this plan, and `wan2gp` is Plan 12's.
   - Environment setup is the `align` half of this point, not a separate point.
2. **One manifest.** Build `requirements()` from VibeComfy `ReadyMetadata` rows (`vibecomfy/templates.py` ~1307-1380), reusing `catalog_manifests` (`asset_alignment.py:192`) and `_lock_coverage` (`entries.py:817`). Include registered plugin roots: `_ready_entries_for` uses `include_dynamic=False` (`entries.py:38`), so also read VibeComfy's `registered_ready_roots()` (`vibecomfy/extras.py:62`).
3. Delete name-only `requirements` and the duplicated row shapes (`entries.py:785-813` path strings, the lock row, the provider inventory). Model locks become caches of manifest rows. h3's model rows and its `comfy_commit` become literals in its own templates. Delete the read of the Agent lock (`h3_av/shared/generation.py:173-188`) and the uses of `engine_source_revision("vibecomfy-h3")` (`compile.py:576,774,1115`, `generation.py:265`), and the action-entry model scan (`entries.py` ~785-800).
4. **Readiness and release identity stop binding the whole lock.** `engine_readiness.py:745-756` compares every lock row. It becomes "the manifest's rows are present", and an engine install no longer fetches models.
5. Delete the unused `engines:` property of `astrid/core/pack/schemas/v3/pack.json` (~195). Step 0: `git grep -ln "schemas/v3/pack.json" -- tests` names the schema test to run. Record in the commit that `engine-index.json` is deleted in T2b, after Plan 06 PK-15B.

**Proof:**
- `PYT tests/core/extensions`, plus new nodes in `tests/core/extensions/test_model.py`: `test_agent_side_point_parses` and `test_client_and_agent_are_the_only_sides`.
- New `tests/core/generation/test_requirements_manifest.py`:
  - every default slot and h3 yields a complete manifest;
  - a registered plugin root's template is included;
  - no row lacks a sha256 or size;
  - `engine` is `comfyui`.
- `PYT tests/core/generation/test_generate_align.py::test_real_catalog_inventory_has_exact_unlocked_models tests/core/generation/test_target_asset_declaration.py::test_engine_model_locks_leave_foley_assets_in_the_workflow_declaration tests/core/generation/test_engine_readiness.py tests/core/generation/test_engine_recipe.py tests/core/generation/test_entries.py tests/packs/h3_av/test_workflow_model_urls.py`.
- `VCT tests/test_plugin_discovery.py::test_dynamic_ready_template_rows_are_explicit_and_unindexed`.
- No second requirements shape is left (grep for the deleted names).

## T2b One base engine; comfy packs deleted

**Outcome:** one ComfyUI base environment per platform, and the `comfyui` and `comfy_wrap` packs gone. Today `comfyui` (image, edit) and `vibecomfy-h3` (audio, H3) are separate RunPod engines (`test_runpod_engine_selection.py::test_audio_runpod_uses_h3_engine_and_image_keeps_comfyui`). The owner decided to delete the old packs here (M-79, D1), superseding the M06-4 hold on [Plan 06](../06-packs/plan.md) PK-15B for them. **Input:** the T3 head (T3 lands first because both touch `sdk/generation.py`). **Authority:** CPU only.

**Delegate to N helpers:** PK-15B's census, the mechanical reference updates, the regenerations and the checks.

1. Follow [PK-15B](../06-packs/tasks.md#pk-15b-delete-the-comfy-packs) in full: its census, its delete list, its reference list (Agent and App) and its new node `test_comfyui_engine_has_no_recipe_after_comfy_pack_removal`. Re-run the census on this head, because line numbers have moved. Record in the completion PR that PK-15B's comfy-pack deletion was done here.
2. Merge the remaining recipes into one engine keyed `comfyui` (the contribution key). Plan 33 U6's cache directory already uses that name, and its rows are keyed by identity, so the merge forces no re-fill.
3. `engine-index.json` is deleted; its readers (`engine_recipe`, `engine_runner`, `entries`, `engine_release`, `engine_bootstrap`, `validate_first_party`) use the `generation.engine` registry.

**Proof:**
- PK-15B's absence checks and selectors (its step 5), including the App grep.
- `PYT tests/core/generation/test_engine_recipe.py tests/core/generation/test_engine_cli.py tests/core/generation/test_engine_release.py tests/core/generation/test_runpod_engine_selection.py tests/core/extensions`; `git grep -n engine-index.json` finds no reader.
- A grep finds no `vibecomfy-h3` literal except history.

## T3 One Placement, with default and override

**Entry gate:** done. The advisor reviewed the Placement shape and the lease on 8 Nov, against the updated plan.md, so T3 starts as soon as T1 lands. The review's decisions:
- **Shape:** `Placement{kind, device?, endpoint?, engine?, machine?, policy}`, frozen and validated.
  - `device` is a local GPU index.
  - `endpoint` and `engine` are for `attached`.
  - `machine` is optional and names one live lease, so a task can ask for a specific rented machine and waits or refuses if that machine is gone.
  - `policy` is typed and small: `idle_timeout_s` (default `warm_hold.DEFAULT_IDLE_SECONDS`, 1800) and `gpu_types` for rented machines. Unknown keys are refused. The `--align` mode stays its own flag.
- **Where it lives:** in the task's input, as task data. The dry run, the host and retries all read the same value, and the Runtime target stays `default`. It is resolved once, in `_generate_on_target`.
- **User default:** stored in the existing global target config read by `targets.resolve_target`, not in a new file.
- **Lease:** no new lease object. Keep `RunPodLeaseOwner`, the warm hold and its idle timer, keyed on machine custody (account, GPU, image, volume, shipped source digest).
- **Cross-repository:** the `--target` → `--placement` rename (D2) also changes the App. Its App callers are a second, separate worker and PR, in the App repository, landed together with T3's Agent change. **Outcome:** a frozen `Placement{kind, device or endpoint, policy}`, resolved request → user default → built-in at one site (`GenerationFacade._generate_on_target`, `sdk/generation.py:1052`) and passed down. **Authority:** CPU only.

**Code facts:**
- `Placement` is today a `Literal["local", "runpod"]` alias (`engine_contracts.py:9`), and `PlacementDescriptor` (~475) is pack-declared backend metadata. Replace the alias with the value and keep the descriptor until T6.
- `kind` is `local`, `attached`, or the key of a `generation.machine` contribution (T5). It is validated against the registry, not a closed enum, so packs can add machines.

1. Delete the re-inference sites:
   - `sdk/generation.py` ~1086-1090 and ~1293;
   - `generic_host.py` `target_policy` → `comfy_url` (~12177-12213);
   - `run.py` ~707-717 and ~753-758;
   - h3's own placement (`transform/run.py` ~1938-1975);
   - the CLI.
2. Rename `--target` to `--placement` and `target_policy` to `placement_policy` in one change, including the App's callers, with no alias (owner decision D2, M-79).

**Proof:**
- New `tests/core/generation/test_placement.py`:
  - precedence of request, user default and built-in;
  - a request naming a `machine` that has no live lease is refused, with the live leases listed;
  - a per-generation override of the device;
  - an unknown machine kind refused with the known kinds listed.
- `PYT tests/core/generation/test_runpod_engine_selection.py::test_dry_run_target_and_engine_equal_live_policy tests/core/generation/test_runpod_engine_selection.py::test_runpod_request_never_selects_a_local_target tests/core/generation/test_runpod_engine_selection.py::test_local_request_never_reaches_runpod tests/core/generation/test_placement_descriptor.py tests/core/test_generation_backend_registry.py tests/core/generation/test_targets.py tests/sdk/test_generation_target.py`.
- One decision site (grep for the deleted names).

## T4 The local run path, with one `align`

**Outcome:**
- `run(job, local)` starts or reuses a ComfyUI on this machine (the chosen GPU). It runs `align(manifest, align|check|trust)` against this disk, fetching only the missing rows. Then it compiles, submits to localhost and returns files in the job directory.
- `run(job, attached)` runs the engine's `probe` (ComfyUI: object_info) or `trust`, then the engine's `execute`; an engine without `probe` refuses attach.
- The `comfyui` engine's `align` is VibeComfy's own commands: `doctor`, `prepare --deps sync`, `nodes restore`, `fetch`. The Agent keeps only the ComfyUI-core install.

**Authority:** CPU only.

**Delegate to N helpers:** the census of submit, retrieve and download paths, and the deletions.

Delete, in the same change:
- `pip_embedded` copy-out (`production_engine.py` ~1165-1180);
- `checkout_server` and its `_EndpointArtifacts` `/view` client (`backends/vibecomfy.py:1432`);
- the second HTTP submit (`VibeComfyEngine._post`, `backends/vibecomfy.py:1273`);
- the `generate align` / `engines install` duplication;
- VibeComfy's hidden `ensure_models` download (`runtime/session.py` ~1209-1210, ~1672).

`model_downloader.py` and the model steps of `engine_runner.py` stay until T5. RunPod still installs through `engines install --model-cache-root` (Plan 33 U6) until T5 replaces that route. Locally, the models root becomes VibeComfy `fetch`'s (`tests/test_fetch.py::test_models_root_accepts_directory_extra_model_paths_env`).

**Proof:**
- New `tests/core/generation/test_run_local.py`: `align`, `check` and `trust` on CPU fakes for local and attached; `align` fetches only the missing rows; `trust` marks the result unverified.
- `PYT -m integration tests/packs/vibecomfy/test_local_server_run.py`, and `PYT tests/packs/vibecomfy/test_local_server_media.py tests/packs/vibecomfy/test_installed_child_path.py::test_installed_qwen_managed_child_path tests/core/generation/test_generate_align.py tests/core/generation/test_engine_runner.py`.
- `VCT tests/test_fetch.py tests/test_doctor_models.py tests/test_custom_node_refs.py`.
- One submit and one retrieve function (grep).

## T5 RunPod as a remote machine: the `generation.machine` point

**Outcome:** `run(job, <machine>)` claims a machine under the existing paid-consent and lease owner (`target_selection`) and ships the job with its digest-pinned pack selection (Plan 06 `active_sources`). It runs `astrid generate <entry> --placement local` there, copies its progress file back on each poll, fetches the outputs against a digest manifest, and always releases. Cancelling the local run stops the remote job and releases the machine (owner, 8 Nov). **Authority:** CPU only.

**Delegate to N helpers:** the test provider, the census of bridge and inventory code, and the deletions. The lead keeps the consent, lease and digest-manifest reasoning: this route has never run end to end.

1. Declare `astrid/packs/generation/extensions/points/machine.yaml`. Its protocol is `claim`, `start`, `poll`, `cancel`, `fetch` and `release` (mirroring the existing `PodOps`), under core consent and lease. `local` and `attached` are built in. RunPod contributes `astrid/packs/runpod/extensions/generation.machine/runpod.yaml`, and the test provider is a contribution under `tests/fixtures`.
2. Generalize `RemotePlacement.run`, `_run_job`, `_download`, `_release`, `manifest_command` and `_MANIFEST_SCRIPT` (`remote_placement.py`, kept by Plan 33 U4). Replace `clip_command_argv` and `transform_command` with the one generic invocation.
3. The lease is minimal: an owner and an idle timeout. Warm reuse covers any machine with the same base engine id (Plan 33 U7's key).
4. The storage volume is mounted as the models root. Pin the mount before any write: pass the cache device and mount id (from `scripts/pod_storage_probe.py`, as `scripts/pod_session.py` ~1056-1110 does), so an unmounted volume refuses instead of caching onto container disk. Plan 33 U6 deferred this pin here, and it is required before any real-pod run (Plan 34). Move Plan 33 U6's identity-keyed cache entries into that layout by rename on the same volume, so nothing is downloaded again.
5. **Progress and cancel, the same as a local job.** Each `_run_job` poll copies the remote attempt's `.astrid-progress.json` into the local attempt's file, which the host already sends in its heartbeat (`generic_host.py:9945`, ~11076-11086). Cancel: the host already sees the task as cancelled; it calls the machine's `cancel` (RunPod: `job_cancel`, `remote_placement.py:111`), then `release`. No new event API, and runpod-lifecycle doesn't change. Verify that `astrid generate` starts its Runtime headless on the pod (`sdk/client.py` `ensure_runtime`); if not, the remote invocation is `astrid action run vibecomfy.run`.
6. Delete:
   - `model_downloader.py` and the model steps of `engine_runner.py` (moved here from T4, because RunPod installs used them until now);
   - the generation bridge path in `adapter.bind_endpoint` and its binding record;
   - Plan 33 U2's inventory document;
   - the warm-reuse window check;
   - `h3_release.py`, `h3_release_remote.py`, `h3_release_bootstrap.py` and `tests/packs/runpod/test_h3_release.py`;
   - h3's verify imports in `remote_placement.py`.

**Proof:**
- New `tests/integrations/test_remote_machine_cpu.py` (`PYT_POD`):
  - every default slot and h3_av through the RunPod contribution on a CPU fake;
  - a second job on a warm machine fetches nothing;
  - a volume-cached model fetches nothing;
  - an install whose volume is not mounted (the device or mount id doesn't match) refuses before writing any model;
  - the test machine contribution runs a job;
  - a contribution pack missing from the shipped selection is refused before the claim;
  - the remote job's progress appears in the local attempt's progress file before the job ends;
  - cancelling the local run mid-job stops the remote job and releases the machine;
  - every machine is released.
- `PYT tests/packs/runpod/test_remote_placement.py tests/packs/runpod/test_warm_session.py tests/packs/runpod/test_target_selection.py tests/core/extensions`.
- In the lifecycle checkout: `.venv/bin/python -m pytest -q tests/test_runner.py::test_ship_and_run_terminates_pod_by_default tests/test_runner.py::test_ship_and_run_keeps_pod_when_terminate_false` (setup as in [Plan 02 P2](../02-consistent-generation/tasks.md#p2-lifecycle)).
- No controller-side model check for RunPod (grep: no `EngineBridge` use in generation, no `ASTRID_TARGET_MODEL_ASSETS`).

## T6 One `generate` and the `vibecomfy.workflows` point

**Outcome:**
- One `generate(entry, inputs, placement)`, with image, video and audio as thin aliases.
- Entries declare modes, inputs (media included), outputs, an optional `build` and an optional `finalize`.
- There is one refusal site, driven by entry data.

**Authority:** CPU only.

**Delegate to N helpers:** the census of branches and legacy-route callers, the deletions and the checks.

1. **The workflow point.** Declare `astrid/packs/vibecomfy/extensions/points/workflows.yaml` (version 1, `side: agent`, cardinality `many`, `effects_allowed: [none]`). Its fields:
   - `ready_root` (required): the `vibecomfy` pack calls `plugin_api().register_ready_root()` for each contribution (VibeComfy `extras.py:48`).
   - `entries`: a list in VibeComfy's thin-entry shape `{id, kind, modes, bundle, needs, binds, defaults}` (VibeComfy `entries.py:45-70`), because plugin templates are absent from the static template index.
   - `build: file.py:fn` (optional): `build(inputs, files, out) -> {workflow, bindings, plan}`. It runs on the machine, on CPU and deterministically. `requirements()` reads the built graph's rows, and the dry run calls it and prints `plan`.
   - `finalize: file.py:fn` (optional): `finalize(job_dir, inputs, files, outputs) -> outputs`. It runs on the same machine after execute and before copy-back, and if it raises, the job fails. The docs must say this is not VibeComfy's template `finalize` (`templates.py:1381`).
2. **The hooks.** The `comfyui` engine's `execute` (and its dry run) calls `build` and `finalize` at one site; core `run()` never names them. Add the entry input type for a map of files (`{id: path}`), shipped in the existing managed-assets archive, whose manifest already keys by binding name (`asset_manifest.py:111-125`). `entries._input_type` has no such type today (`entries.py:171-176`).
3. **Node packs need no hook (decided).** A template's own node pins win over the lock (VibeComfy `custom_node_refs.py:241-247`).
4. **Delete:**
   - the hard-coded `vibecomfy-h3-workflow` backend (`backends/registry.py:28,240-250`, `backends/vibecomfy_workflow.py`);
   - the action-entry kind (`entries.py:98-139, 636-640`);
   - the duplicate modality resolution (`sdk/invocation.py` ~4853);
   - the per-modality branches in `merge-run/path-review/6-modality-branches.md`;
5. Leave Wan2GP's host branches (`generic_host.py:11673`, `:12497`) for Plan 12.

**Proof:**
- No modality or entry branch on the path, and the engine is chosen only by `manifest.engine` (grep).
- `PYT tests/core/extensions tests/core/generation/test_runpod_engine_selection.py tests/core/test_generation_backend_registry.py`.
- New nodes:
  - `tests/core/extensions/test_registry.py::test_workflow_contribution_registers_ready_root_entries_build_and_finalize`;
  - `tests/core/generation/test_entries.py::test_file_map_input_ships_in_the_managed_assets_archive`;
  - `tests/core/generation/test_run_local.py::test_build_and_finalize_run_once_at_the_run_site`.
- `PYT_POD tests/integrations/test_remote_machine_cpu.py`.
- `VCT tests/test_plugin_discovery.py tests/test_custom_node_refs.py`.

## T6b h3_av becomes one contribution

**Outcome:** h3_av is one pack with one `vibecomfy.workflows` contribution, and every piece of h3 machinery that the generic path makes obsolete is deleted. The inventory is `merge-run/path-review/H3-GENERALIZATION.md` section 1 (class d) and `H3-AS-VIBECOMFY-EXTENSION.md` section 3 (20 sites). **Authority:** CPU only.

**Input (Plan 33 U4 finding, advisor, 8 Nov):** the h3_av CPU case fails on the base `8df5c09c2` even when run alone, with `task_status_unavailable` and `transport_timeout` and four consecutive claim failures in the runtime status poll. It is a real failure, not load. Reference only: branch `plan33/u4-h3-default` at `9352f8d` (unmerged; it over-deletes `tests/packs/runpod/test_managed_source_root.py`, so do not take it whole).

**Delegate to N helpers:** the site census, the deletions and the checks. The lead keeps the `build` and `finalize` boundaries.

1. Contribute `astrid/packs/h3_av/extensions/vibecomfy.workflows/h3.yaml`, and add `dependencies.packs: [vibecomfy]` to h3_av.
   - `ready_root`: the three trios, plus the builder templates.
   - `entries`: h3 with modes `i2v`, `v2v` and `video-edit`.
   - `build`: wraps `prepare_request` and `compile_preparation` (`compile.py:1039`), including the trio choice and the ffprobe source measurement.
   - `finalize`: wraps `compose_candidate` and `verify_candidate`, so preservation is still proven.
2. Move the H3 node-pack row out of VibeComfy `node_packs/_defs.py` ~52-57 into h3's templates. Step 0: confirm that class resolution finds a pinned class that is not listed there; if not, keep the row and record it.
3. **Delete:**
   - the seven-stage graph, the tracked parent and `ManagedParentClient`;
   - the operation journal and resume;
   - the raw and final receipts and the publication finalizer;
   - the input bundle (`shared/input_bundle.py`), because the generic managed-assets archive replaces it;
   - worker qualification, prepared workers and the cleanup receipt (`core/execution/worker_qualification.py`, `runpod/prepared_task.py` ~559-581), including the `legacy_prepared` route (`transform/run.py:1947-1952`);
   - h3's pod-route remnants in `remote_placement.py` and the release builder, where T5 has not already removed them;
   - the legacy RunPod route, moved here from Plan 33 U5 because h3's `legacy_prepared` route is its last caller: `runpod_route` and `endpoint_checkout` in `run.py` (709-726, 1012-1036), `endpoint_checkout.py` and its five `generic_host.py` imports (1400, 9412, 9795, 11697, 17156), the legacy branch of `resolve_workflow_descriptor` (`registry.py` ~168-180), and the `placement` parameter of `workflow()`. Step 0, census: `git grep -n "endpoint_checkout\|checkout_from_profile\|read_host_workflow_execution_request\|load_workflow_endpoint\|pending38"`. On `5eac07e3f` the tests that use them are:
     - `tests/core/generation/test_workflow_route.py`;
     - `tests/core/execution/test_workflow_endpoint_handoff.py`;
     - `tests/sdk/test_generation_workflow.py`;
     - `tests/sdk/test_runpod_front_door.py`;
     - `tests/core/generation/test_comfy_provenance_journey.py`;
     - `tests/core/generation/test_producer_result_recovery.py`;
     - `tests/core/generation/backends/test_vibecomfy_http_polling.py`.

     Delete or narrow each, and name it in the commit body.
   - the h3 special cases in `generic_host.py`, `delivery.py`, `preflight.py` and `sdk/invocation.py`.

   Multi-pass requests and parent resume are not included.

**Proof:**
- The Matrix request (Plan 33 U1's fixture) runs as an ordinary `generate` on the CPU fake: `PYT_POD tests/integrations/test_remote_machine_cpu.py`.
- The h3_av status-poll case (the Input above) reproduces on the base, and it passes after T6b: its test is named in the commit body, with the poll failure as its recorded cause.
- `grep -ri h3 astrid/core astrid/sdk` returns nothing (about 156 lines today).
- A grep finds no stage graph, journal, receipt or input bundle left in `astrid/packs/h3_av`, and `! git grep -n "pending38\|checkout_from_profile\|endpoint_checkout" -- astrid` finds no legacy route.
- `PYT tests/packs/h3_av/test_compile.py tests/packs/h3_av/test_verify_fail_closed.py tests/packs/h3_av/test_compose_staged_104.py tests/packs/h3_av/test_workflow_model_urls.py`, with the deleted machinery's test files deleted and named in the commit body.

## T8 Completion

The astrid-dev completion PR links the implementation PRs, the integrated revisions, T1–T6b's CPU evidence, the review rounds and a disposition for [F-003](../../vision/gaps/F-003-creative-execution.md). It states that the live proof is a later pass of [Plan 34](../34-real-gpu-proof/plan.md).
