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

**Base.** Start from Plan 33's landed revisions, as recorded in [Plan 33's inputs](../33-unblock-live-generation/inputs.md#source-identities) at its U9. Today those are Agent `5eac07e3f` plus Plan 33's commits, VibeComfy `e65f4941`, Runtime `b983b04` and lifecycle `f2948817`. Record the exact SHAs in [inputs.md](inputs.md#source-identities) before T1. There is one Agent candidate branch; each task starts from the head the previous task left on it. VibeComfy changes (T4, T6) go on one VibeComfy branch from its pin, and the Agent repins it in the same task.

Selectors below exist at Agent `5eac07e3f` or VibeComfy `e65f4941`, or are new files that the task (or Plan 33) creates. Agent checks use `PYT` and `PYT_POD` as defined in [Plan 33's tasks](../33-unblock-live-generation/tasks.md). VibeComfy checks use `bash "$ENV/vc-pytest.sh" -q` from the VibeComfy checkout, written `VCT` below, after `vc-setup.sh` ([env README](../02-consistent-generation/env/README.md)).

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| [T1](#t1-characterize-every-capability) Characterize every capability that calls generation, under local, attached and RunPod | N | Plan 33 landed; Plan 34's first pass (owner's order) | `tests/integrations/test_runpod_slot_path_cpu.py` (from Plan 33 U1), `tests/core/generation/test_runpod_engine_selection.py` | Every capability is a case; current failures are recorded as strict `xfail` with the reason | [ ] |
| [T2](#t2-one-requirements-manifest-and-the-engine-point) One requirements manifest; the `generation.engine` point with ComfyUI as its one contribution | X | T1 | `astrid/core/extensions/{model.py,schema/point.json}`, new `astrid/packs/generation/extensions/points/engine.yaml`, new `astrid/packs/vibecomfy/extensions/generation.engine/comfyui.yaml`, `astrid/core/generation/{entries,asset_alignment,engine_readiness,engine_recipe}.py`, `astrid/core/pack/schemas/v3/pack.json`, `astrid/packs/h3_av/shared/generation.py`, and their tests | New `tests/core/generation/test_requirements_manifest.py`; `tests/core/extensions`; the readiness and alignment nodes below | [ ] |
| [T2b](#t2b-one-base-engine) `vibecomfy-h3` and `comfyui` become one base engine | X | T2; owner decision D1 (Plan 06 PK-15B) | `astrid/packs/{comfyui,runpod,vibecomfy}` recipes and locks, `astrid/packs/engine-index.json`, the engine names in core and sdk | One engine row per platform; `PYT` the engine nodes below; no `vibecomfy-h3` literal outside history (grep) | [ ] |
| [T3](#t3-one-placement-with-default-and-override) One Placement value, with default and override | X | T1; an independent review of the Placement and lease design (Advise) | `astrid/core/generation/engine_contracts.py` (`Placement`), `astrid/sdk/{generation,invocation}.py`, `astrid/core/generation/{cli,targets}.py`, `astrid/core/generation/backends/registry.py`, `astrid/core/execution/generic_host.py` (target_policy), `astrid/packs/vibecomfy/actions/run/run.py`, `astrid/packs/h3_av/actions/transform/run.py`, and their tests | New `tests/core/generation/test_placement.py`; one decision site (grep); dry run equals live | [ ] |
| [T4](#t4-the-local-run-path-with-one-align) The local run path, with one `align` | X | T2, T3 (T2b if D1 is yes) | `astrid/packs/vibecomfy/{local_server_engine,production_engine}.py`, `astrid/packs/vibecomfy/actions/run/run.py`, `astrid/core/generation/backends/vibecomfy.py`, `astrid/core/generation/{asset_alignment,engine_runner,model_downloader}.py`, `astrid/core/engine_cli.py`; VibeComfy `vibecomfy/runtime/session.py` (`ensure_models`) | New `tests/core/generation/test_run_local.py`; one submit and one retrieve function (grep); the VibeComfy nodes below | [ ] |
| [T5](#t5-runpod-as-a-remote-machine-the-generationmachine-point) RunPod as a remote machine: the `generation.machine` point | S | T4 | New `astrid/packs/generation/extensions/points/machine.yaml`, new `astrid/packs/runpod/extensions/generation.machine/runpod.yaml`, `astrid/packs/runpod/{adapter,generation,remote_placement,target_selection,installed_session}.py`, `astrid/packs/runpod/h3_release*.py`, `astrid/core/execution/generic_host.py` (bind), `astrid/packs/vibecomfy/local_server_engine.py` (inventory channel), and their tests | New `tests/integrations/test_remote_machine_cpu.py` (every slot and h3_av, warm reuse, volume, a test machine contribution); no controller-side model check for RunPod (grep) | [ ] |
| [T6](#t6-one-generate-h3_av-as-one-vibecomfyworkflows-contribution) One `generate`; h3_av as one `vibecomfy.workflows` contribution | X | T5 | New `astrid/packs/vibecomfy/extensions/points/workflows.yaml`, new `astrid/packs/h3_av/extensions/vibecomfy.workflows/h3.yaml`, `astrid/packs/h3_av/**`, `astrid/sdk/{generation,invocation}.py`, `astrid/core/generation/{entries,preflight,delivery}.py`, `astrid/core/generation/backends/{registry,vibecomfy_workflow}.py`, `astrid/core/execution/{generic_host,worker_qualification}.py`, `astrid/packs/runpod/prepared_task.py`; VibeComfy `node_packs/_defs.py` (H3 row) | `grep -ri h3 astrid/core astrid/sdk` empty; no modality branch on the path; `tests/core/extensions`; T5's harness green | [ ] |
| [T8](#t8-completion) Completion | N | T1–T6, R | astrid-dev completion PR | The PR links the implementation PRs, the integrated revision, the CPU evidence and a disposition for F-003 | [ ] |
| R Review rounds (at most 3: owner-agreed 2, lead recommendation 3) | S | T1–T6 | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | [ ] |

**T7 (live proof). Deferred:** the live proof of this plan is a later pass of [Plan 34](../34-real-gpu-proof/plan.md) (real-GPU proof), which follows [Plan 33](../33-unblock-live-generation/plan.md). The owner decided on 8 Nov that Plans 33 and 32 are CPU only; see [inputs.md](inputs.md#owner-decisions). T8 does not wait for it.

## T1 Characterize every capability

**Outcome:** the CPU tests name every capability that reaches generation, so later tasks see what they break. **Authority:** CPU only.

1. Step 0, census: `git grep -nE "GenerationFacade|sdk\.generation|invoke(_result)?\(\s*['\"]vibecomfy\.run|['\"]h3_av\.transform" -- astrid ':!astrid/sdk/generation.py'`. List each capability, pack action or SDK caller in the commit body.
2. Add one case per capability to Plan 33's `tests/integrations/test_runpod_slot_path_cpu.py`, parametrized over `{local-managed, attached, runpod}`. Extend `tests/core/generation/test_runpod_engine_selection.py::test_default_slot_resolves_to_requested_target_or_refuses` the same way.
3. A case that fails today becomes `pytest.mark.xfail(strict=True, reason=...)` naming the task that fixes it, never a skip.

**Proof:** `PYT_POD tests/integrations/test_runpod_slot_path_cpu.py` and `PYT tests/core/generation/test_runpod_engine_selection.py` pass, with the recorded `xfail`s.

## T2 One requirements manifest and the engine point

**Outcome:** `requirements(entry, inputs) -> {engine, base, models[name, subdir, url, sha256, size], nodes[repo, commit]}`, one row shape, and the engine table built from `generation.engine` contributions. **Authority:** CPU only.

**Delegate to N helpers:** the census of requirement shapes, the schema and YAML files, the test nodes and the checks.

1. **Switch the protocol on for the Agent.**
   - Allow `side: agent` in `astrid/core/extensions/schema/point.json:11` and `model.py:86,428`.
   - Declare `astrid/packs/generation/extensions/points/engine.yaml` (cardinality `many`). Its data is `platforms -> recipe`, and its protocol is `align(manifest, mode)` and `execute(job) -> files in job.out`.
   - Contribute `astrid/packs/vibecomfy/extensions/generation.engine/comfyui.yaml`.
   - `run()`'s engine table is the registry's contributions for this point. Only `vibecomfy.comfyui` exists in this plan, and `wan2gp` is Plan 12's.
   - Environment setup is the `align` half of this point, not a separate point.
2. **One manifest.** Build `requirements()` from VibeComfy `ReadyMetadata` rows (`vibecomfy/templates.py` ~1307-1380), reusing `catalog_manifests` (`asset_alignment.py:192`) and `_lock_coverage` (`entries.py:817`). Include registered plugin roots: `_ready_entries_for` uses `include_dynamic=False` (`entries.py:38`), so also read VibeComfy's `registered_ready_roots()` (`vibecomfy/extras.py:62`).
3. Delete name-only `requirements` and the duplicated row shapes (`entries.py:785-813` path strings, the lock row, the provider inventory). Model locks become caches of manifest rows. h3's model rows come from its own templates: delete the read of the Agent lock (`h3_av/shared/generation.py:173-188`).
4. **Readiness and release identity stop binding the whole lock.** `engine_readiness.py:745-756` compares every lock row. It becomes "the manifest's rows are present", and an engine install no longer fetches models.
5. Delete the unused `engines:` property of `astrid/core/pack/schemas/v3/pack.json` (~195). Step 0: `git grep -ln "schemas/v3/pack.json" -- tests` names the schema test to run. Record in the commit that `engine-index.json` becomes generated from contributions after Plan 06 PK-15B (T2b).

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

## T2b One base engine

**Outcome:** one ComfyUI base environment per platform. Today `comfyui` (image, edit) and `vibecomfy-h3` (audio, H3) are separate RunPod engines (`test_runpod_engine_selection.py::test_audio_runpod_uses_h3_engine_and_image_keeps_comfyui`). **Depends on** owner decision D1, because deleting the `comfyui` recipe is Plan 06 PK-15B's scope, held by M06-4. **Authority:** CPU only.

1. With D1 = "T2b absorbs PK-15B": follow [PK-15B](../06-packs/tasks.md#pk-15b-delete-the-comfy-packs)'s census and reference list for the engine half, and merge into one recipe keyed `comfyui` (the contribution key). Plan 33 U6's cache directory already uses that name, and its rows are keyed by identity, so the merge forces no re-fill.
2. `engine-index.json` is generated from `generation.engine` contributions, with one shipped generator and a `--check`.

**Proof:** `PYT tests/core/generation/test_engine_recipe.py tests/core/generation/test_engine_cli.py tests/core/generation/test_engine_release.py tests/core/generation/test_runpod_engine_selection.py tests/core/extensions`, plus the generator's `--check`. A grep finds no `vibecomfy-h3` literal except history.

## T3 One Placement, with default and override

**Entry gate:** an independent review ([Advise](../../skills/astrid-dev-advise/SKILL.md)) of the Placement shape (default and override, `device`) and the lease, against T1's head. **Outcome:** a frozen `Placement{kind, device or endpoint, policy}`, resolved request → project → user → built-in at one site (`GenerationFacade._generate_on_target`, `sdk/generation.py:1052`) and passed down. **Authority:** CPU only.

**Code facts:**
- `Placement` is today a `Literal["local", "runpod"]` alias (`engine_contracts.py:9`), and `PlacementDescriptor` (~475) is pack-declared backend metadata. Replace the alias with the value and keep the descriptor until T6.
- `kind` is `local`, `attached`, or the key of a `generation.machine` contribution (T5). It is validated against the registry, not a closed enum, so packs can add machines.

1. Delete the re-inference sites:
   - `sdk/generation.py` ~1086-1090 and ~1293;
   - `generic_host.py` `target_policy` → `comfy_url` (~12177-12213);
   - `run.py` ~707-717 and ~753-758;
   - h3's own placement (`transform/run.py` ~1938-1975);
   - the CLI.
2. Rename `--target` to `--placement` and `target_policy` to `placement_policy`, per owner decision D2.

**Proof:**
- New `tests/core/generation/test_placement.py`:
  - precedence of request, project, user and built-in;
  - a per-generation override of the device;
  - an unknown machine kind refused with the known kinds listed.
- `PYT tests/core/generation/test_runpod_engine_selection.py::test_dry_run_target_and_engine_equal_live_policy tests/core/generation/test_runpod_engine_selection.py::test_runpod_request_never_selects_a_local_target tests/core/generation/test_runpod_engine_selection.py::test_local_request_never_reaches_runpod tests/core/generation/test_placement_descriptor.py tests/core/test_generation_backend_registry.py tests/core/generation/test_targets.py tests/sdk/test_generation_target.py`.
- One decision site (grep for the deleted names).

## T4 The local run path, with one `align`

**Outcome:**
- `run(job, local)` starts or reuses a ComfyUI on this machine (the chosen GPU). It runs `align(manifest, align|check|trust)` against this disk, fetching only the missing rows. Then it compiles, submits to localhost and returns files in the job directory.
- `run(job, attached)` runs `check` (object_info) or `trust`, then submit and `/view`.
- `align` is VibeComfy's own commands: `doctor`, `prepare --deps sync`, `nodes restore`, `fetch`. The Agent keeps only the ComfyUI-core install.

**Authority:** CPU only.

**Delegate to N helpers:** the census of submit, retrieve and download paths, and the deletions.

Delete, in the same change:
- `pip_embedded` copy-out (`production_engine.py` ~1165-1180);
- `checkout_server` and its `_EndpointArtifacts` `/view` client (`backends/vibecomfy.py:1432`);
- the second HTTP submit (`VibeComfyEngine._post`, `backends/vibecomfy.py:1273`);
- the `generate align` / `engines install` duplication;
- the model steps of `engine_runner.py`;
- `model_downloader.py`;
- VibeComfy's hidden `ensure_models` download (`runtime/session.py` ~1209-1210, ~1672).

**Keep Plan 33 U6's volume cache working:** the models root on a mounted volume becomes VibeComfy `fetch`'s models root (`tests/test_fetch.py::test_models_root_accepts_directory_extra_model_paths_env`). T5 moves U6's identity-keyed entries into that layout by rename on the same volume, so nothing is downloaded again.

**Proof:**
- New `tests/core/generation/test_run_local.py`: `align`, `check` and `trust` on CPU fakes for local and attached; `align` fetches only the missing rows; `trust` marks the result unverified.
- `PYT tests/packs/vibecomfy/test_local_server_run.py tests/packs/vibecomfy/test_local_server_media.py tests/packs/vibecomfy/test_installed_child_path.py::test_installed_qwen_managed_child_path tests/core/generation/test_generate_align.py tests/core/generation/test_engine_runner.py`.
- `VCT tests/test_fetch.py tests/test_doctor_models.py tests/test_custom_node_refs.py`.
- One submit and one retrieve function (grep).

## T5 RunPod as a remote machine: the `generation.machine` point

**Outcome:** `run(job, <machine>)` claims a machine under the existing paid-consent and lease owner (`target_selection`) and ships the job with its digest-pinned pack selection (Plan 06 `active_sources`). It runs `astrid generate <entry> --placement local` there, fetches the outputs against a digest manifest, and always releases. **Authority:** CPU only.

**Delegate to N helpers:** the test provider, the census of bridge and inventory code, and the deletions. The lead keeps the consent, lease and digest-manifest reasoning: this route has never run end to end.

1. Declare `astrid/packs/generation/extensions/points/machine.yaml`. Its protocol is `claim`, `ship_and_run`, `fetch` and `release`, under core consent and lease. `local` and `attached` are built in. RunPod contributes `astrid/packs/runpod/extensions/generation.machine/runpod.yaml`, and the test provider is a contribution under `tests/fixtures`.
2. Generalize `RemotePlacement.run`, `_run_job`, `_download`, `_release`, `manifest_command` and `_MANIFEST_SCRIPT` (`remote_placement.py`, kept by Plan 33 U4). Replace `clip_command_argv` and `transform_command` with the one generic invocation.
3. The lease is minimal: an owner and an idle timeout. Warm reuse covers any machine with the same base engine id (Plan 33 U7's key).
4. The storage volume is mounted as the models root. Move Plan 33 U6's cache entries into it by rename.
5. Delete:
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
  - the test machine contribution runs a job;
  - a contribution pack missing from the shipped selection is refused before the claim;
  - every machine is released.
- `PYT tests/packs/runpod/test_remote_placement.py tests/packs/runpod/test_warm_session.py tests/packs/runpod/test_target_selection.py tests/core/extensions`.
- In the lifecycle checkout: `.venv/bin/python -m pytest -q tests/test_runner.py::test_ship_and_run_terminates_pod_by_default tests/test_runner.py::test_ship_and_run_keeps_pod_when_terminate_false` (setup as in [Plan 02 P2](../02-consistent-generation/tasks.md#p2-lifecycle)).
- No controller-side model check for RunPod (grep: no `EngineBridge` use in generation, no `ASTRID_TARGET_MODEL_ASSETS`).

## T6 One `generate`; h3_av as one `vibecomfy.workflows` contribution

**Outcome:**
- One `generate(entry, inputs, placement)`, with image, video and audio as thin aliases.
- Entries declare modes, inputs (media included), outputs and an optional `finalize`.
- There is one refusal site, driven by entry data.
- h3_av is one pack with one contribution.

**Authority:** CPU only.

**Delegate to N helpers:** the h3 site census (`merge-run/path-review/H3-AS-VIBECOMFY-EXTENSION.md` section 3, 20 sites), the deletions and the checks.

1. **The workflow point.** Declare `astrid/packs/vibecomfy/extensions/points/workflows.yaml`. Its fields are `ready_root`, an optional `plugin: file.py:register`, and an optional per-template `finalize: file.py:fn` as a typed field. The `vibecomfy` pack loops over the contributions, calling `register_ready_root` and the optional `register`.
2. **h3_av's contribution.** Contribute `astrid/packs/h3_av/extensions/vibecomfy.workflows/h3.yaml`, and add `dependencies.packs: [vibecomfy]` to h3_av. Move the trios and the builder into its ready root, the request mapping into `register_op("video", "h3")`, and compose and verify into `finalize`.
3. **Node packs need no hook (decided).** A template's own node pins win over the lock (VibeComfy `custom_node_refs.py:241-247`), so move the H3 row out of `node_packs/_defs.py` ~52-57 into h3's templates. Step 0: confirm that class resolution finds a pinned class that is not listed there; if not, keep the row and record it.
4. **Delete:**
   - the hard-coded `vibecomfy-h3-workflow` backend (`backends/registry.py:28,240-250`, `backends/vibecomfy_workflow.py`);
   - the action-entry kind (`entries.py:98-139`);
   - the tracked parent, prepared and qualified workers (`core/execution/worker_qualification.py`, `runpod/prepared_task.py` ~559-581);
   - the h3 dry-run special case;
   - the duplicate modality resolution (`sdk/invocation.py` ~4853);
   - the per-modality branches in `merge-run/path-review/6-modality-branches.md`.
5. Leave Wan2GP's host branches (`generic_host.py:11673`, `:12497`) for Plan 12.

**Proof:**
- `grep -ri h3 astrid/core astrid/sdk` returns nothing (about 156 lines today).
- No modality or entry branch on the path, and the engine is chosen only by `manifest.engine` (grep).
- `PYT tests/core/extensions tests/core/generation/test_runpod_engine_selection.py tests/packs/h3_av/test_compile.py tests/packs/h3_av/test_verify_fail_closed.py tests/packs/h3_av/test_compose_staged_104.py`, plus `PYT_POD tests/integrations/test_remote_machine_cpu.py`.
- `VCT tests/test_plugin_discovery.py tests/test_custom_node_refs.py`.
- A new node `tests/core/extensions/test_registry.py::test_workflow_contribution_registers_ready_root_and_finalize`.

## T8 Completion

The astrid-dev completion PR links the implementation PRs, the integrated revisions, T1–T6's CPU evidence, the review rounds and a disposition for [F-003](../../vision/gaps/F-003-creative-execution.md). It states that the live proof is a later pass of [Plan 34](../34-real-gpu-proof/plan.md).
