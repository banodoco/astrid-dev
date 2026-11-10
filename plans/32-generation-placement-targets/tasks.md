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
| [T8](#t8-completion) Completion | N | T1–T6b, T5c, T5d, T5f, T6b-5, T6d, S1, S2, R | astrid-dev completion PR | The PR links the implementation PRs, the integrated revision, the CPU evidence and a disposition for F-003 | [ ] |
| T5c Which machine ran a job: machine identity on the attempt and in the task list (owner, 9 Nov) | N | T5a merged to `int/32` | The code that records a task attempt when the host claims it and the machine contribution's `claim` (`astrid/core/execution/generic_host.py`, `astrid/packs/runpod/{adapter,target_selection}.py`); the Agent's task listing command (step 0: find it with `git grep -n "def .*task.*list\|tasks list" -- astrid`). The App's task table only after checking with Plan 29's orchestrator (App release 12) | Each attempt records `{placement kind, machine contribution, machine id (RunPod: pod id), lease id, device}` when its machine is claimed, and the task listing shows a "machine" column. Proof: new nodes in `tests/integrations/test_remote_machine_cpu.py`: a job on the RunPod fake records the fake pod id and lease, and a local job records `local` and its device. A listing test shows both | [ ] |
| T5d A warm machine is reused, and cleared when it dies (owner, 9 Nov) | N | T5a merged to `int/32` | The machine contribution's `claim` and `poll` and the lease record (`astrid/packs/runpod/{target_selection,worker_owner}.py`, `astrid/core/execution/warm_hold.py`), plus a new `astrid machines` command | With the default placement `{kind: runpod}` and no `machine`, a job reuses the live warm machine with the same custody key, or claims one, and that becomes the warm machine. The current machine is lease state, not a setting, so nothing in the settings document can dangle. **Liveness:** before any reuse, and on every host poll, the contribution asks the provider about each live lease. A pod that is terminated, exited or missing ends its lease with a reason (`ended: provider_terminated`), leaves warm reuse and stops being charged. The next default job then claims a fresh machine. A task pinned to that `machine` is refused with the reason and the live leases. `astrid machines` lists live and recently ended leases (id, kind, GPU, state, idle expiry, cost so far, end reason); `astrid machines release <id>` releases one. Proof: new nodes in `tests/integrations/test_remote_machine_cpu.py`: kill the fake pod between jobs, and the next default job claims a new machine while the old lease shows `provider_terminated`; a pinned job is refused; `astrid machines --json` lists both | [ ] |
| T5f A warm pod keeps no job's data, at near-zero cost per job (owner, 9 Nov) | S | T5e, T5g | `astrid/packs/runpod/pod_bootstrap.py` (`setup_runtime`), `astrid/packs/runpod/machine.py` (`runtime_check_command`, `generation_command`, `start`, `release`), `astrid/sdk/client.py` (`open_from_launcher`), and their tests | **Design (Opus review, 9 Nov).** One long-lived pod Runtime is reset in place after each job:<br>(1) at bootstrap, after `workspace create`, take an empty-realm template with `astrid-runtime backup --destination /root/astrid/realm-template`; when the source digest changes, delete `ready.json` and `down`;<br>(2) after the digest-verified fetch, `release(warm=True)` runs a detached reset BEFORE `settle`: restore the template into a sibling candidate (`POST /v1/restore`), then `POST /v1/replace` (same process, same realm id; the old root is moved aside and deleted), `rm -rf RUNS_ROOT/<old>` and the pod-agent job directory, sweep the pack-host attempt folders and truncate logs, then one full `ensure_runtime` that writes a prepared connection and `ready.json`;<br>(3) the next job's generation command takes `flock /root/astrid/reset.lock`, requires `ready.json` with no pending reset, and opens the prepared connection: no per-job `ensure_runtime`, and the entry check is folded into the generation command;<br>(4) `/root/astrid/active-job.json` holds `{run_id, local task, attempt}` while a job lives and is deleted by the reset, and the run idempotency key is `remote:<task>:<attempt>`;<br>(5) a failed reset releases the pod instead of settling it; a pending `active-job.json` at the next claim redoes the reset.<br>**Also fixes:** set `ASTRID_RUNTIME_DATA_ROOT` and `ASTRID_RUNTIME_SOURCE_MANIFEST` on the pod (it otherwise falls back to `/root/.astrid-data` with no workspace); `ASTRID_RUNTIME_DOOR_PORT=0` for any second Runtime; remove the pod-agent job directory each job (its cap is 128).<br>**Owner sign-off (9 Nov):** the source-identity check moves from job start to reset time, which is sound because pod sources change only through `pod_bootstrap`. Proof: on the RunPod CPU fake, the reset comes after fetch and before settle, and a warm job runs no `up` or `connect`; a `real_runtime` test runs the reset for real and asserts zero tasks, runs, events and objects, an empty CAS, the old root gone, and a prepared open under 1.0 s (median of 3); a failed reset releases the pod | [ ] |
| T6d Default entries are data: packs offer defaults, users pin them (owner, 9 Nov) | X | T6b-1 (the MiniMax H3 video default needs h3 as a contribution) | `astrid/sdk/generation.py` (`_DEFAULT_ENTRIES`, `_EXPLICIT_ONLY_ENTRIES`), the `vibecomfy.workflows` point schema (`entries[].default_for`), the built-in packs' contributions, the user settings read by the Placement default, and their tests | Delete the hard-coded `_DEFAULT_ENTRIES` table. An entry may declare `default_for: [{kind, mode, priority}]`, and a user pin sets any slot. **Storage (owner, 9 Nov): the Runtime, in the general format.** The user's generation settings are one document in the Runtime's existing per-user JSON store, `/v1/app-state/user/generation` (`get_user_app_state` and `update_user_app_state` in the generated client, with versioned, idempotent writes and no Runtime change). Its shape is engine-neutral: `{"placement": {kind, device?, endpoint?, policy?}, "defaults": {"<kind>.<mode>": {"pack": "<pack id>", "entry": "<entry id>"}}}`. Entries are named by pack and entry, placement kinds are machine contribution ids (`local`, `attached`, `runpod`), and an engine, where one is needed, is its contribution id (such as `vibecomfy.comfyui`). T3's Placement user default moves into this same document. So do the RunPod preferences (`[runpod]` in `~/.vibecomfy/config.toml`: GPU types, datacenter, image, volume, idle timeout, budget cap and a credential *reference* by name, written by `runpod setup` via `targets.update_config`, `targets.py` ~253 and `packs/runpod/target_selection.py` ~180-189). They move under `machines.runpod` in the same document, as placement policy for that machine contribution. No secret is ever stored there. VibeComfy's `~/.vibecomfy/config.toml` keeps only VibeComfy's own settings, such as the attached ComfyUI address. Any Astrid default already in it is imported once into the document and then no longer read for Astrid. The document is editable as a file: `astrid generate settings checkout --file <path>` and `... checkin <path>`, as `astrid preferences` does, on a version conflict refusing with both versions shown. `defaults set` and `unset` edit one key. A malformed or unknown pin is refused at the one refusal site, naming the key. Per-project overrides need a new Runtime document kind, so they are left to [Plan 12](../12-multiple-inference-routes/plan.md). Resolution is request → user pin → highest-priority pack default → none (refused at the one refusal site), the same order as Placement. Today's table moves into the built-in contributions as data, and MiniMax H3 becomes the video default. **See and set them** with one command next to `astrid generate list`: `astrid generate defaults` lists every `(kind, mode)` slot with its resolved entry, where that came from (user pin, or which pack and priority) and the other candidates, as text and `--json`. It also names where each value came from (for example "Runtime user settings, version 3", or a pack and its priority) and how to edit it (`settings checkout`). `astrid generate defaults set <kind> <mode> <entry>` and `... unset <kind> <mode>` write and remove the user pin, refusing an entry that doesn't exist or lacks that kind and mode. The SDK has the same pair (`generation.defaults()`, `generation.set_default(...)`). Proof: new nodes show that a third-party test contribution becomes a default, a user pin overrides it, an unknown pinned entry is refused at the one refusal site, and the image, audio and video slots resolve as before plus video → MiniMax H3. A test shows `astrid generate defaults --json` naming each slot's entry and source, and `set` then `unset` round-trips the user pin. Further tests: the settings document round-trips through checkout and checkin, a stale checkin is refused, an old TOML default is imported once, and a placement default set in the document is what `generate` uses. Grep: no `_DEFAULT_ENTRIES` | [ ] |
| S1 The generation skill, rewritten for the one path (owner, 9 Nov) | N | T5c, T5d, T6b, T6d | `astrid/packs/generation/docs/SKILL.md`, plus the matching sections of `astrid/packs/{vibecomfy,runpod,h3_av}/docs/SKILL.md` and any mirrored copy (step 0: `git grep -ln "generate_image\|execution.*cloud" -- "*SKILL.md"`) | One short skill that leads with the main things: `generate(entry, inputs, placement)` and the image, video and audio aliases; Placement kinds (local with device, attached, RunPod) with default and per-generation override; `align`, `check` and `trust`; RunPod (paid consent, the controller drives and pulls, lease and warm reuse, what happens when a pod dies, `astrid machines`, the volume, which machine ran a job, and the `machines.runpod` preferences); adding your own entry or shortcut through `vibecomfy.workflows`, with one minimal worked contribution; **running a ComfyUI workflow file** (one-off, no pack needed): `workflow(workflow=<file or digest>, inputs/workflow_inputs, placement)` on each placement (local, the user's own ComfyUI as `attached`, RunPod), with image and video inputs shipped through the file map. The vibecomfy skill's "Run on your own ComfyUI" section (find their ComfyUI, pick and read a saved workflow, run, follow, stop) is rewritten onto `attached` with no `comfy_url`, `source_video` upload or other legacy parameter, and when a one-off workflow should become an entry is spelled out; default slots: seeing them all (`astrid generate defaults`), pinning one (`defaults set`, or `settings checkout`, edit, `checkin`); **the generation settings document** itself: where it lives (the Runtime user store, `generation`), its shape (placement, plus `defaults` keyed `<kind>.<mode>` → `{pack, entry}`), the resolution order, and what stays in VibeComfy's own config, and offering one from a pack (`default_for`); provider APIs (fal, OpenAI, Wavespeed) are still a separate route until the providers follow-up. Proof: every command in it runs on CPU as written, as a dry run or a test node (the workflow-file run on all three placements included, on the CPU fakes), and a grep finds no `--target`, `execution: "cloud"` or `execution: "local"` left in any SKILL.md | [ ] |
| S2 Guided generation setup: the agent sets generation up for this machine (owner, 9 Nov) | N | T6d, S1 (and T5d for the RunPod step) | `astrid/packs/generation/docs/SKILL.md` (a new first section, "Set up my generation"), `docs/setup/SKILL.md` (replace "Connecting local engines such as ComfyUI or Wan2GP is not covered here yet" with a "Set up generation" step), `astrid/packs/_core/docs/SKILL.md` (a routing row for "set up my generation"), `astrid/packs/vibecomfy/local.py` (a read-only Wan2GP folder probe), `astrid/core/generation/cli.py` (`generate workflow --as-entry --dry-run` preview). App: one line in `src/shared/components/RuntimeConnection/copy.ts` `agentInstructions`, after "confirm Astrid shows Connected", but only after checking with Plan 29's orchestrator, which owns App release 12. *Proposed move (owner decision D7 in [Plan 20](../20-zero-to-first-image/inputs.md#owner-decisions-needed)): the `docs/setup/SKILL.md` step and this App line go to Plan 20's O1 and O3, which point to this section; S2 keeps the rest.* | **Works whether or not the skills are installed:** each pointer gives both the installed skill name and its public URL, as the App's brief already does for setup (`SETUP_GUIDE_URL`, `copy.ts:280`), for example `https://github.com/banodoco/astrid-agent/blob/main/astrid/packs/generation/docs/SKILL.md#set-up-my-generation`. The section is run at first run and whenever the user says "set up my generation". **Steps:**<br>(1) read what is set: `generate defaults --json`, `generate targets --json`;<br>(2) discover, read-only: the ComfyUI scan with its saved workflows, provider keys by presence only, a Wan2GP folder; show one list;<br>(3) ask once which tool is primary, and save the attached placement only on a yes;<br>(4) one question per default slot, with evidence from `generate list` readiness ("you have X's models; set it as your image default?"), then `defaults set` on a yes;<br>(5) a checklist of the other saved workflows; each ticked one is previewed (`--as-entry --dry-run`), then saved as an entry;<br>(6) print how to run each one, and offer one test generation;<br>(7) list every change and its undo.<br>**Never:** launch, restart or touch the user's ComfyUI or its queue; download or install during setup; read a key; write without its own yes. The `## Local generation` prose that the vibecomfy skill saves into preferences is replaced by the T6d settings document. Proof: a scripted fake ComfyUI (`/system_stats`, `/internal/folder_paths`, `/userdata?dir=workflows` with two saved workflows, `/object_info`), extending the scan tests; a test that walks the skill's commands (discover, save target, `defaults set`, `--as-entry`, `describe`) and checks that undo restores the previous state; a grep finding no `comfy_url` in any SKILL.md, and finding both the skill name and the URL in `docs/setup/SKILL.md` and the App brief | [ ] |
| T6b-5 h3 end to end through the facade on local-managed and attached (manager, 9 Nov) | S | T6b-3, T4i | Whatever causes the COMBO/CHOICE input-type mismatch that keeps the local-managed and attached h3 cells red (in h3's workflow or entry inputs, VibeComfy's schema check, or the stand-in ComfyUI's object_info); step 0 names the side | T6b-3 merges with T4i's seam test (`test_job_runs_h3_build_and_after_outputs_once_each`, with the sha assertion) as its interim proof. This row turns the facade-level proof green: the composed candidate is delivered end to end through `vibecomfy.run`'s `after_outputs`, on local-managed and attached, and both h3 cells leave `_RED`. It is a Completion bullet (every default slot and h3_av under each placement), so it must pass before T8. It is not deferred. | [ ] |
| F1 Re-resolve the T2b requirements lock (follow-up, advisor 9 Nov) | N | T2b merged to `int/32` | the repo's requirements lock files, touched only by its own lock command | The card's step 1 is `uv lock` (or the repo's own lock command), run as a task step, not approved partway through. The lock must match the pins in T2b's commit body (ComfyUI `423cbd20`). Proof: the lock command exits 0, and the engine selection and requirements manifest tests pass after it | [ ] |
| F2 Delete the no-op `ASTRID_ALLOW_UNQUALIFIED_GPU` setting (follow-up, 9 Nov audit) | N | T6b-2 (it deletes worker qualification) | `astrid/core/execution/gpu_environment.py` (~23-25), `astrid/installer/service.py` (`SERVICE_SETTINGS`, ~39-41), and their tests and docs | Step 0: confirm it has no effect (`git grep -n ASTRID_ALLOW_UNQUALIFIED_GPU`). Then remove it from the accepted service settings and the code, so an old value is ignored with a one-line notice rather than accepted silently. Proof: the grep finds only the notice and its test | [ ] |
| F3 Full machine contract (follow-up, Plan 32 review, 9 Nov, at 7209ffcc7; High; consumed by Plan 25) | X | T8 | `astrid/core/execution/generic_host.py:6990-7055`, `astrid/core/execution/target_provider.py:15-50`, `astrid/sdk/generation.py:1303-1308,1436-1438`, `astrid/core/generation/placement.py:215-221`, `machines_cli.py`, `preflight.py:23`, `engine_readiness.py:710-711` | Put `for_host` and `describe` into the `generation.machine` point's protocol; fold the `adapter.py` `TargetProviderBindings` mechanism into it; take RunPod names (`_runpod_paid_controls`, `_runpod_placement_policy`, the literal `'placement': 'runpod'`, the "every non-built-in kind is RunPod" rule) and the core imports of `astrid.packs.runpod` out of the SDK, `placement.py` and core. Proof: one test drives the test machine through the facade and host, with no pack named exactly like its kind | [ ] |
| F4 Collapse the two `align` implementations (follow-up, Plan 32 review, 9 Nov, at 7209ffcc7; Medium) | N | T8; the engine-protocol task in Plan 12 | `astrid/core/generation/asset_alignment.py:484-557` (`astrid generate align`) and `comfyui_engine.py:169-194` (the engine's `align`) | Keep one implementation that the CLI and the engine both call, and delete the other. Proof: a grep finds one per-model fetch-and-verify path, and the align tests pass against it | [ ] |
| R Review rounds (at most 3, owner-agreed) | S | T1–T6b, T5c, T5d, T6d | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md). **Scope freeze (owner, 9 Nov):** a finding is must-fix only if it is (a) a bug or regression, (b) a break of a Completion bullet in plan.md, or (c) in scope and leads to poor structure (a second path or decision site, a leftover legacy route or shim, or a forbidden modality or engine branch). Everything else becomes a follow-up row after T8. findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | [x] `41da1ff86` |
| D7 Final R: carry local Placement.device through the owned managed launch and attempt | X | R on `cc084ebd9` | `astrid/sdk/generation.py`, managed host/custody and their tests | Public facade CPU fake proves request/default precedence, device reaches launch and receipt, and a differently bound server is not silently reused | [x] `e1d06fa97` |
| D8 Final R: carry resolved RunPod Placement.policy | X | R on `cc084ebd9`; D7 shared SDK route | `astrid/sdk/generation.py`, RunPod admission/lease and their tests | CPU fake proves request policy overrides defaults through task serialization, offer consent and lease settlement | [x] `e1d06fa97` |
| D9 Final R: remove non-allowlisted H3 core comment | N | R on `cc084ebd9` | `astrid/core/generation/entries.py` | prescribed h3 grep returns only plan allowlist | [x] `632326bbd` |
| D10 CI: restore pinned VibeComfy setup before pytest | X | CI on `cc084ebd9` | CI setup / engine catalog and focused tests | exact CI pin-resolution command succeeds; restore a comparable full-suite CI run | [x] `d81b3edf2`; pin test passed |
| R2.1 Device override refreshes authoritative launch evidence | X | R2 on `e1d06fa97`; D7 | managed preparation, engine status/readiness and tests | Install under one visibility, generate on another, then real canonical status and readiness identify the new owned launch; preserve receipt custody | [x] `41da1ff86` |
| G1 Machine liveness and exact owner release | X | Plan 34 finding on `41da1ff86` | machine CLI, RunPod owner and tests | Preserve live unfinished custody, restrict reuse to eligible leases, bind exact release through retained and cold owner; independent review and focused CPU proof | [ ] candidate `44d192ec` |
| G2 Check idle policy test regression | N | D8, G1 | RunPod pack-actions test | Compare exact reported test on main and current head; repair a stale expectation if it is a regression | [ ] |
| G3 Earlier i2v heartbeat timeout | N | `41da1ff86` | existing CPU RunPod journey | Rerun exact earlier journey once under journey lock; if green record earlier timeout as Plan 34 follow-up, otherwise diagnose/fix Plan 32 bootstrap | [ ] |

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
  - App `--placement` rename (X): `plan32/t3-app-placement` cut from astrid-app `main`, worker `session_011EzfW15EYWoDKwCtDsn2Qj`. **Result:** no `--target` or `target_policy` call sites in astrid-app. Nothing pushed; the session is archived. The App part is done as nothing.
- Advisor check-in #7, 04:05Z:
  - **T3** is ready to merge right after T1. Its "RunPod live-lease lookup still unwired" (`Placement.machine` naming a live lease) is **deferred to T5**, which owns machines and leases. Its other failures reproduce on the clean base, so they don't block.
  - **T2 manifest** (`75e5531`): the 21 wide-run failures are being itemised against the base (`fb7944d`). Only failures new on `75e5531` block the merge.
  - **T2b started** (X, worker `session_011EzfW4aHNr5E5dZ999yK7R`) on `plan32/t2b-engine-base` (`d4fcd5d68`, T2 manifest merged with T3). Work is on `plan32/t2b-one-engine`. T2b merges after T1, T2 and T3.
  - Itemisation worker (read-only): `session_011EzfW1ZMEvnwymrMBGz278`.
- T4 and T5 prep (read-only, push nothing): census `session_011EzfW1xEePB3dQiR72qR2C`, design `session_011EzfW3L3qwN5dvVk4zYGdj`.
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

Prepare via the `prepare_workflow` API (CLI wrapper bug; Plan 17 C3).

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
- VibeComfy's hidden `ensure_models` download (`runtime/session.py:1209-1210`, and ~1672). **The census (9 Nov) found that deleting only those lines is not enough.** Three more download paths remain: `run.py:698`, `session.py:2301`, and the prepare route. Delete all three, and the lines above.
- **Downloads happen only through `align` (VibeComfy `fetch`).** No other code path may download a model.
- **First step for the T4 worker:** check the Agent-side callers of each download path, and name every caller in the commit body, before any deletion.
- **Proof for "no other download path":** a grep, and a test, showing that no code path outside `align` downloads a model. Name the grep pattern and the test in the commit body.

`model_downloader.py` and the model steps of `engine_runner.py` stay until T5. RunPod still installs through `engines install --model-cache-root` (Plan 33 U6) until T5 replaces that route. Locally, the models root becomes VibeComfy `fetch`'s (`tests/test_fetch.py::test_models_root_accepts_directory_extra_model_paths_env`).

**Proof:**
- New `tests/core/generation/test_run_local.py`: `align`, `check` and `trust` on CPU fakes for local and attached; `align` fetches only the missing rows; `trust` marks the result unverified.
- `PYT -m integration tests/packs/vibecomfy/test_local_server_run.py`, and `PYT tests/packs/vibecomfy/test_local_server_media.py tests/packs/vibecomfy/test_installed_child_path.py::test_installed_qwen_managed_child_path tests/core/generation/test_generate_align.py tests/core/generation/test_engine_runner.py`.
- `VCT tests/test_fetch.py tests/test_doctor_models.py tests/test_custom_node_refs.py`.
- One submit and one retrieve function (grep).

## T5 RunPod as a remote machine: the `generation.machine` point

**Decisions, advisor, 9 Nov (answers to the T5 design's section 9):**
1. **Where `generation.machine` comes from:** T5 declares it itself (step 1 below). `local` and `attached` are built in. The plan lives in astrid-dev, so the T5 worker gets a read-only clone of astrid-dev (`git clone --depth 1 https://github.com/banodoco/astrid-dev`) to read this card.
2. **Progress writer:** T5 adds a minimal one. When `ASTRID_PROGRESS_PATH` is set, the pod-side run writes coarse phases to it: align, submit, `executing n/m` when known, then fetch. Take them from the pod host's own `terminal["progress"]` (`generic_host.py` ~11104). Do not build a new event system. The CPU fake proves a phase reaches the controller's file before the job ends.
3. **Progress path mismatch** (`:9970` versus `:10953` and `:11106`): T5 checks it with a test first. If the directories differ, make them one, the attempt directory, in the same change.
4. **`ensure_runtime` versus the 17340 door port:** not blocking. Once T6b removes H3's route, nothing on the pod needs the door. T5 lets `ensure_runtime` pick its own port, and the CPU fake asserts there is no port clash.
5. **GraphQL shape for mounts:** the T5 worker clones `banodoco/runpod-lifecycle` read-only at `f2948817` and writes the fake's `mounts` stub from `discovery.observe_pod_mounts` itself.
6. **Scope of "source_video upload":** the remote route only. Input files ship inside the job directory, so there is no controller-to-ComfyUI upload for remote jobs. The local attached-URL `upload_media` path stays, because an attached ComfyUI needs it.
7. **GPU custody:** agreed. Key the lease on the observed `gpu_type` from the claim record, not on the preference list.

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
- `grep -ri h3 astrid/core astrid/sdk` returns no h3_av-specific line (about 156 lines today). Allowlisted, because they are not h3_av (owner, 9 Nov): the HTML `<h3>` tag in hivemind `ingest_article`, the hivemind SKILL channel name, and the `minimax-h3` vendor model id in `model_catalog`. Any other hit must go.
- A grep finds no stage graph, journal, receipt or input bundle left in `astrid/packs/h3_av`, and `! git grep -n "pending38\|checkout_from_profile\|endpoint_checkout" -- astrid` finds no legacy route.
- `PYT tests/packs/h3_av/test_compile.py tests/packs/h3_av/test_verify_fail_closed.py tests/packs/h3_av/test_compose_staged_104.py tests/packs/h3_av/test_workflow_model_urls.py`, with the deleted machinery's test files deleted and named in the commit body.

## T8 Completion

The astrid-dev completion PR links the implementation PRs, the integrated revisions, T1–T6b's CPU evidence, the review rounds and a disposition for [F-003](../../vision/gaps/F-003-creative-execution.md). It states that the live proof is a later pass of [Plan 34](../34-real-gpu-proof/plan.md).

## Run state: open list (progress 14, manager)

Integration head: `banodoco/astrid-agent` `int/32-one-generation-path` = `041fb242b` (merged T6b-3 fix6 / fix6b from `f1031678f`). Reviewer and advisor session IDs are in the run log, not here.

One line per item: owner session, branch/SHA, state, next step.

- **D1 align gets workflow path** (must-fix, Codex): owner Codex run (advisor-owned); Claude D1 worker stopped; no branch on origin. State: not started. Next: Codex pushes `plan32/d1-*` with focused proof; reviewer; merge on OK.
- **D2 dry-run submitted ⊆ built test** (must-fix, Codex): base `plan32/dry-run-invariant` `9ef4f3f`. State: base only. Next: Codex builds on 9ef4f3f; reviewer; merge on OK.
- **D3 controller-to-pod seam test** (must-fix, Codex): no branch. State: not started. Next: Codex pushes `plan32/d3-*`.
- **D4 RunPod models-lock gate decision** (must-fix, Codex): no branch. State: not started. Next: Codex decides (move to pod, remove with test, or waiver in tasks.md with evidence).
- **D5 stale "T4 STUB" text; comfyui_engine cancel raises** (must-fix, Codex): not started.
- **D6 re-tag _RED; --align trust cells for tts and sfx** (must-fix, Codex): not started.
- **Batch R, real regressions** (X): session `session_011EzfW4GKspyvvH6PvDnGp7`, branch `plan32/r-regressions` from `041fb242b`. State: dispatched. Items: Runtime opened before validation (test_entry_cli_contract); engine_install deadline type drift (test_mcp_generation_parity); audio RunPod admission needs saved preferences (test_generation_target, check T6d defaults). Next: report branch and SHA; reviewer; merge on OK.
- **Batch T, test drift** (N): session `session_011EzfW3eHhFLsHnoM3HKTRa`, branch `plan32/t-test-drift` from `041fb242b`. State: dispatched. Items: test_cli (12 facade shape), test_runpod_engine_selection (4, valid inputs), test_skills (4, generate(entry, inputs, placement)). Next: report branch and SHA; reviewer; merge on OK.
- **T6b-3 should-fix: document-path shape checks** (should-fix): owner T6b-3 `session_011EzfW1TP4SN4pbR3BKtAzQ`; on `041fb242b`. State: requested. Next: shared shape-check helper for dict and document path; focused proof; SHA to manager.
- **T6b-3 re-point of 7 test_orchestrator_manifest_schema h3 tests** (regression, not known failure): owner T6b-3 `session_011EzfW1TP4SN4pbR3BKtAzQ`. State: requested. Next: re-point to vibecomfy.run passthrough and live orchestrator, or delete; SHA to manager.
- **test_sdk_entry_contract test_launch_rejects_invalid_controls_before_selection[kwargs1]** (pre-existing stale `target=` kwarg): stale-test follow-up. Not started. Next: update test to `placement=`.
- **Registry leak** (test_registry_qualifying_discovery_refuses_corpus_change[new_manifest], shard D single-process): owner T6b-3 `session_011EzfW1TP4SN4pbR3BKtAzQ`. State: reproduction running on `e0df2459a`; leaking file not yet named. Next: T6b-3 sends the leaking file and one-line cause.
- **managed_schema pin**: owner not recorded in this file. State: open. Next: confirm owner and status.
- **census-lock check**: owner reviewer `session_011EzfW18G7mV91ATcEdxQeq`. State: open. Next: confirm the `approve` output diff is clean on a clean checkout.
- **Shard delta re-runs** (A–E, touched files only, on final head): shard C `session_011EzfW3RWkUCtWTbhTqksTB` (alive; waits for batches R and T to merge). Shards A, B, D, E session IDs: in run log. State: waiting. Next: after R and T merge, send each shard its touched files on the final head.
- **Final R** (review, must confirm the dry-run "submitted ⊆ built" check cannot hide dropped nodes): reviewer. State: waiting for all merges above. Next: request after delta re-runs are green.
- **T8 Completion**: manager. State: waiting on everything above. Next: run only after final R is OK.

Video-references: resolved on int/32 by `041fb242b` (T6b-3 fix6/fix6b); reviewer OK.
- **Follow-up (not a must-fix): prepared-worker island, RunPod account-ref refusal.** Evidence: `astrid/packs/runpod/prepared_task.py:608` (mismatch refusal) sits in `_ProductionPreparedTaskRuntime._components`, reached only via `PreparedRunPodGeneration.bind_client` (`astrid/packs/runpod/generation.py:201-214`); the machine route uses `prepare_retained_generation` (machine.py:469, adapter.py:18). Tests: `test_prepared_task.py`, `test_https_transport.py:236`. Filed under Plan 14's "prepared-worker island: audit, then delete" row. No worker in Plan 32.

## Progress 15 (manager): shard IDs and follow-ups

Shard sessions (for delta re-runs): A `session_011EzfW3CaNuPW9MVcLt8XUr`; B `session_011EzfVze1kQLDP2pHMBQfTa`; C `session_011EzfW3RWkUCtWTbhTqksTB`; D `session_011EzfW3pBGYXbnX2YtXneBT`; E `session_011EzfW2SrM1VTtVCnoePc4j`.

Follow-up (not a T8 gate): unreproduced order-dependent flake, `tests/packs/rendering/test_render_export_task_adapter.py::test_registry_qualifying_discovery_refuses_corpus_change[new_manifest]`. Evidence: fails in shard D's single-process run on e0df2459a (registry_settle completes without noticing a new local pack; no "corpus changed" raised; astrid imports from its own worktree). T6b-3 reproduced the same 290-file order in one process on e0df2459a (20m12s) and it passed; shard D's run was 216 failed / 4913 passed / 78 errors with that file's only failure being `test_render_export_adapter_writes_real_mp4_and_is_callable`. Suspect env state (tar fixture warnings at test_render_export_task_adapter.py:77; leftover state under the worktree env). Owner: T6b-3; shard D single-test run pending.

## Run state: handover progress 16 (manager to manager)

Integration head: `banodoco/astrid-agent` `int/32-one-generation-path` = `364f98e33` (batch T merged). Merged in this run, in order: T6b-3 fix6 `041fb242b`, fix7 `29607985d`, D1 `31487f181`, D5 `6483407b8` and docstring `68e930d60`, D4 `0b070ff06`, batch R `95ae37ac8`, batch T `364f98e33`.

Rule for the next manager: Codex never pushes to int/32. Fetch before every merge; on a rejected push, re-fetch and redo; never force. Never reuse a merged branch; fresh progress branches from `origin/main`.

### Open items (owner session, branch/SHA, state, next step)

- **Codex Terra run: D2, D3, D6, D4b typed filter, isolated i2v journey**: owner Codex Terra manager (it reviews and merges its own branches into int/32 with its own reviewer). State: in progress; not in int/32 yet. Next: Codex merges, reports each merge SHA for the GPU-run gate.
- **GPU run gate**: D4 is in; D2, D3, D6 and the D4b filter are pending on Codex. The GPU run pushes only `plan34/fix-*`.
- **Batch T**: merged `364f98e33`. Done. Note for the card: the old skill claim that the facade rejects `execution="openai"` no longer holds; the new text is compatible.
- **Batch R**: merged `95ae37ac8`. Done. Restore of the action-source refusal kept ahead of any Runtime launch; engine_install tests follow `models_root`; audio RunPod tests save preferences through the real client.
- **Shard A net-new (fail on head `e0df2459a`, pass on base `65037c218`)**, reported at 00:01 by session `session_011EzfW3CaNuPW9MVcLt8XUr`:
  - `tests/core/generation/test_engine_execution.py` (7): real regression candidate. `AttributeError: 'LocalLinuxExecutionContext' object has no attribute 'download_model'`; the context class lacks the method the tests expect. Next: a product owner decides fix in the context class or test re-point; not dispatched by this handover.
  - `tests/core/execution/test_generic_host_claim_loop.py` (9): likely timing under load. Next: re-run in isolation on head before treating as a regression.
  - `tests/test_installed_generation_journey.py` (3): likely environment (`has_installed_astrid()` False in the head worktree). Next: re-run with the installed lane provisioned.
- **Shard delta re-runs** (touched files only, on the final head): shards A–E. Not yet run on `364f98e33`. Next: after the merges above land, send each shard its touched files.
- **Final R** (review, must confirm the dry-run "submitted ⊆ built" check cannot hide dropped nodes): reviewer `session_011EzfW18G7mV91ATcEdxQeq`. State: waiting for D2 and the shard re-runs. Next: request after those.
- **T8 Completion**: owner new manager. State: waiting on the items above.
- **Managed_schema pin**: owner not recorded. State: open. Next: confirm owner and status.
- **Census-lock check**: owner reviewer `session_011EzfW18G7mV91ATcEdxQeq`. State: open. Next: confirm the `approve` output diff is clean on a clean checkout.
- **Registry leak** (`tests/packs/rendering/test_render_export_task_adapter.py::test_registry_qualifying_discovery_refuses_corpus_change[new_manifest]`): closed as an unreproduced, order- or state-dependent flake. Shard D's test passes alone on `e0df2459a`; T6b-3's 290-file single-process run passed. Not a T8 gate. Evidence on the follow-up list.
- **Prepared-worker island (RunPod account-ref refusal, `prepared_task.py:608`)**: follow-up, not a must-fix. Owner Plan 14 "prepared-worker island: audit, then delete" row. Evidence: `runpod/generation.py:201-214`, `test_prepared_task.py`, `test_https_transport.py:236`.
- **Follow-ups (post-T8)**: the stale `target=` test in `test_sdk_entry_contract.py` (`test_launch_rejects_invalid_controls_before_selection[kwargs1]`); the controller-side refusal test for a mismatched `ASTRID_RUNPOD_ACCOUNT_REF`; the D4 review nits (key the candidate filter on a typed error, and rename `test_audio_runpod_uses_h3_engine_and_image_keeps_comfyui`); the card note for the h3 static-vs-built bundle; the registry scope of entry hooks; exact per-artifact sizes for the disk floor; and the upgrade-transition note.

### Known pre-existing failures (fail on base `65037c218` too)

- Shard A: 405 ids across ~25 files (e.g. `scripts/test_pod_jobs` 36, `test_sdk_public_surface` 27, `sdk/test_timeline_editing_acceptance_runtime` 27, `scripts/test_pod_bootstrap` 26, `test_ci_journey` 21). Full lists are in shard A's scratchpad.
- Shard C: 365 ids fail on both head and base (environmental: `test_installer_busy_fence` 59, `test_engine_custody` 39, `test_pinokio_platform_adapter` 25, `test_failure_receipts` 25, etc.).
- `test_mcp_generation_parity` and `test_entry_cli_contract`: 6 tests fail on base too (`test_phase_one_tools_list_and_parser_registration`, `test_generate_schema_and_argv_for_all_leaves`, `test_target_launch_cli_and_mcp_envelope`, `test_runpod_generation_follow_and_release_cli_and_mcp_envelopes`, `test_public_sfx_route_receives_declared_inputs`, `test_json_and_convenience_values_use_shared_resolver`). Worker env was head's pins on base source; not verified in a base-pinned env.
- `test_t4g_local_complete`: `the_real_runner_start_probe_reuses_then_restarts_a_cpu_standin_server` fails on base `7209ffcc7` (the `_Runner` fixture lacks `plan`).

### Live sessions and what they hold

- Reviewer: `session_011EzfW18G7mV91ATcEdxQeq` (census-lock check, final R).
- Advisor/orchestrator (handed over): `session_011EzfVz8zzHLnUqSqMnGUCT`.
- T6b-3: `session_011EzfW1TP4SN4pbR3BKtAzQ` (fix6 and fix7 merged; leak closed; stop work).
- Batch R: `session_011EzfW4GKspyvvH6PvDnGp7` (merged; done).
- Batch T: `session_011EzfW3eHhFLsHnoM3HKTRa` (merged; done).
- Shard A: `session_011EzfW3CaNuPW9MVcLt8XUr` (alive; delta re-run pending; holds the net-new list above).
- Shard B: `session_011EzfVze1kQLDP2pHMBQfTa` (alive; delta re-run pending).
- Shard C: `session_011EzfW3RWkUCtWTbhTqksTB` (alive; holds the 25-item triage; delta re-run pending on `364f98e33`).
- Shard D: `session_011EzfW3pBGYXbnX2YtXneBT` (alive; holds the registry-leak evidence; delta re-run pending).
- Shard E: `session_011EzfW2SrM1VTtVCnoePc4j` (alive; delta re-run pending).
- Codex D4 and D5 workers and the Codex Terra run: their merged branches are on int/32; their session IDs are not recorded here.

## Progress 17 (Codex manager, 10 Nov)

- **Integration:** `364f98e33`; batch T and R landed as recorded above. The direct run brief authorizes this manager to merge into int/32 after the outgoing manager's mailbox handover.
- **D2:** `plan32/codex-manager-d2` merges WIP `8594ce1a` onto `364f98e33` at `4a365af8`; focused local tests 24 passed. The t2i integration reached matching graphs and bindings but failed because its align spy produced no record; diagnosing before retry. D3 and D6 await the overlapping contract work.
- **D3:** independent review of `13130089b` found file-map document members resolve against the controller cwd rather than the document directory, potentially shipping the wrong file. Fix in D3 with a document-relative regression; seam proof remains pending.
- **Census lock:** at `364f98e33`, `capability_ledger approve` on an archived clean checkout produced byte-identical lock (SHA-256 `93d926bf15009e83ad7b4547dc0a0e1d67a3937738ceea51d42f09c5a0f66fec`); command reported no census changes. Optional packs were quarantined with compatibility warnings in that archive environment.
- **managed_schema:** active VibeComfy pin is `e65f4941d09b1cb4d1dd5aae6171c73e648706f4` via the recipe and RunPod pins; the distinct historical H3 schema capture is `01f38461d633651c8857712b2331650aedaee461`. Reconcile with any remaining pin concern.
- **i2v lease loss:** image/t2i RunPod CPU-fake control on `364f98e33` passed (1 passed, 120.63s) under the journey lock. The i2v upload heartbeat timeout remains unexplained; comparing retained diagnostics, not claiming the i2v journey passed.
- **Shard A:** triaging seven `test_engine_execution.py` failures and the claim-loop and installed-lane candidates from progress 16; no disposition yet.

## Progress 18 (Codex manager, 10 Nov)

- **D3 landed:** `f61663ebf` merges `plan32/codex-manager-d3` `66e4636db`. The controller's shipped job runs through real `local_job.run_job` on the CPU fake: serialized seam 1 passed; archive/H3/seed focused checks 12 passed. Independent review cleared the file-map document-parent fix and custody checks. D2 will merge this head and reconcile its shared seed preparation.
- **D6:** at `7efe5bb65`, the serialized trust selection failed after 6 passed: `audio/sfx-local-managed-trust` reached the fake Comfy queue, which rejected the Foley VAE and video input menu values. Investigating whether the fixture's inventory or product behavior owns the failure; no pass claimed.
- **Shard A triage:** on `364f98e33`, `test_engine_execution.py` has 6 passed / 7 failed against the removed model-download method. One isolated claim-loop node fails because its fixture reads removed warmth fields; the full file was interrupted after three failures. Source-profile `test_installed_generation_journey.py` has 33 passed / 1 stale `target` failure; installed mode was not provisioned. Updating the obsolete test contracts while preserving current assertions.
- **i2v:** the green t2i control does not establish why i2v's heartbeat timed out. Advisor asked for the gate disposition; retained diagnostics show one archive, 345 fake-provider PUTs, and a later Runtime heartbeat transport timeout.

## Progress 19 (Codex manager, 10 Nov)

- **Shard A test drift landed:** `fb62a5058` merges `plan32/shard-a-test-drift` `96812b2a9`. Engine execution 6 passed after retiring 7 tests solely of the removed model-download method; claim loop 14 passed with host/client/session/attempt/process isolation retained and obsolete warmth fields removed; generation journey 34 passed in source profile (installed profile still unproven).
- **D2:** the real child align spy now fires. Exact graph comparison exposed an output-prefix mismatch; the worker is tracing the built graph and shared transform before deciding a fix. D3 is merged into its work branch.
- **D6:** the failing CPU fake's Foley VAE menu uses the generic `vae` folder rather than custom `hunyuan_foley`, and its uploaded-file menus omit `LoadVideo.file`. Correcting those fake server menus before rerunning the same serialized test; real Comfy's queue validation remains in force.
- **D4b:** typed missing-input filter and misleading test rename dispatched from `fb62a5058`, disjoint from D2's preparation functions.

## Progress 20 (Codex manager, 10 Nov)

- **D6 landed:** `376d27f08` merges `86778e332`. The serialized local/attached TTS/SFX trust and native custody selection passed 10 tests; native-attempt symlink refusal passed alone. Independent review cleared the original trust overlay and the fixture/cleanup follow-up. Trust remains unverified and the fake queue still validates its menus.
- **D3 hook boundary:** a D2-focused guard found D3 added core naming of a `build` hook. The reviewer traced an older related inconsistency as well; the existing local-job adapter is moving into VibeComfy, with the structural guard strengthened. Branch `plan32/d3-hook-boundary` `fe066bdc9`: structural, H3 and T4i checks passed (5); serialized seam rerun pending.
- **D2:** the real child spy works. The registered workflow output-prefix input can overwrite the run-scoped node value during compilation; a focused real-workflow regression passes with the proposed fix. The attached t2i cell passed; managed and remaining matrix cells pending.
- **D4b:** `plan32/codex-manager-d4b` `78a10e3cf` has typed missing-input filtering and a facade-level rewording proof (4 focused cases passed). An earlier full-file run showed an initial failure before interruption; identifying that node before integration.

## Progress 21 (Codex manager, 10 Nov)

- **D4b landed:** `2513adbda` merges `f3b6c7d27`, replacing diagnostic-text matching with a typed missing-input signal and renaming the test. Four focused selection/fail-closed cases passed. The first full-file failure (`audio/tts-auto`, missing Qwen node in local fixture) reproduces on base `fb62a5058`; the interrupted run is not a full pass.
- **D2:** the corrected t2i comparison passed attached and failed managed because the spy observed no actual align call; investigating the route without weakening the assertion. Branch must merge `2513adbda` before final proof.
- **D3 boundary:** structural, H3 and T4i checks passed; serialized seam rerun is running. The repair must merge the current int/32 head before integration.
- **Timing (owner, 10 Nov):** Plan 34 live GPU proof starts after Plan 32 completion, not in parallel. No intermediate GPU gate is needed.

## Progress 22 (Codex manager, 10 Nov)

- **D3 boundary landed:** `3bab37e51` merges `fe066bdc9`. VibeComfy owns hook-specific local-job routing; the core ownership guard now catches membership as well as calls and subscriptions. Structural/delegation, H3/T4i and serialized seam checks passed; independent review found no blockers.
- **D2 managed alignment:** the t2i attached cell passed but the managed cell recorded no align call. Trace shows the facade passes the managed target URL as `comfy_url`, causing the action to choose its attached path and skip managed alignment. Repair is underway with real supervised CPU setup and independent lifecycle review; proof remains open. Integration head must be merged into D2 before final checks.
- **Remaining:** D2 and the i2v heartbeat disposition, integrated scoped proof, the one CI full-suite comparison, final R and T8. The owner moved live GPU proof to after Plan 32 completion.

## Progress 23 (Codex manager, 10 Nov)

- **Managed cold start (Completion, X):** independent lifecycle review found that an installed managed engine whose owned server has stopped is rejected by `preflight._installed_managed_target` → `local_engine_endpoint` → read-only `engine_status` before the job can start it. Default local start/reuse is required by the plan. Worker `plan32/managed-cold-start`, base `3bab37e51`, is reproducing and repairing this separate readiness/lifecycle ordering problem with a public-facade CPU regression; it preserves ownership validation and coordinates with D2.
- **D2:** independent review supports passing `comfy_url` only for attached placement, preserving managed preflight and engine custody. Exact t2i retry on `68b26db0a` has passed attached; supervised managed cell is running. Remaining invariant matrix and integrated proof are pending.

## Progress 24 (Codex manager, 10 Nov)

- **Managed host preparation (Completion, S):** the local action's supervisor socket is denied by worker policy. Independent security review found the socket grants installation-wide process control, and private path checks do not authenticate the peer. Advisor decision: trusted host aligns the exact manifest and ensures the owned engine HTTP-ready before spawning the worker; the worker receives only HTTP, stays sandboxed, and retains managed identity. Align/start/cancel failures must spawn no worker. Branch `plan32/managed-host-preparation`, base `3bab37e51`, is assigned with real-host/supervisor success and failure-before-spawn proof and independent review.
- **Cold start:** candidate `e373aa5a7` has 16 focused passes but independent review found a persisted failed receipt can masquerade as a freshly verified absent-service status. Repair and a real-status regression are underway; do not integrate or claim public-facade proof yet.
- **D2:** attached and seed evidence continue while the host boundary is built. The managed URL change is WIP and will be reconciled with host preparation; no raw supervisor socket exception is permitted.

## Progress 25 (Codex manager, 10 Nov)

- **Managed role parity (advisor decision):** managed dry and live both select roles deterministically from entry declarations, regardless of installed alternatives. The host aligns and validates the frozen workflow against actual object_info after readiness and before spawning the worker; a mismatch refuses rather than reselects. RunPod likewise selects declarations; attached remains inventory-aware. Managed dry preview does not require a running engine. D2 owns a managed installed-alternate equality test; host preparation owns validation.
- **Host boundary:** `plan32/managed-host-preparation` is implementing host-side alignment and readiness with worker HTTP-only execution, attempt-bound preparation, cancellation drainage, and custody serialization. Independent security review identified non-reentrant install locking, exact canonical workflow/config binding, and same-supervisor cancellation barrier requirements; these remain under implementation and review.
- **Cold start:** the persisted-receipt review finding was fixed at `0e0816fdf` with 18 focused passes and independent review; its separate preflight-start design is held because startup before host alignment would violate the chosen ordering. Integrate only the needed safety work once the unified host route is settled.

## Progress 26 (Codex manager, 10 Nov: restart reconciliation)

- **Integration:** `3bab37e51`; no later Plan 32 product merge or GPU gate has occurred. The owner now wants the GPU run started at the last product merge, in parallel with the final gate.
- **D2:** clean worktree `plan32/codex-manager-d2` `3ae3df439`. Attached music, edit and h3 exact-graph matrix passed at `dd7469b1e` (3 tests); the managed installed-alternate declaration-selection regression passed at `3ae3df439`. The integrated managed host proof and full default-slot invariant remain open. Restart interrupted in-flight work; no interrupted command is counted as passing.
- **Host preparation:** clean worktree `plan32/managed-host-preparation` `0566a2cd9`; focused preparation and custody checks passed (17). Independent review cleared the scratch/model-root/deadline follow-up, but found prepared native attempt projection lacks sibling-file custody checks and fails to preserve managed identity on failure/cancellation; structured readiness failure evidence also needs work. Real host/supervisor journey and final independent review remain open. A resumed worker and separate reviewer are checking the exact checkpoint.
- **Cold start:** `plan32/managed-cold-start` `0e0816fdf` remains held; preflight-start ordering conflicts with host-align-before-start. The persisted-failure safety fix passed focused checks and review, but its integration depends on the unified route.
- **i2v:** the earlier lease/heartbeat uncertainty remains open; no new product conclusion. Full CI comparison, final R and T8 have not run.

## Progress 27 (Codex manager, 10 Nov)

- **D2 attached CPU fake:** at `e9255aabf`, TTS and SFX trust cells passed (2) using declared fake inventory and real compilation/submission; attached t2i passed at `3ae3df439`, and music/edit/h3 passed at `dd7469b1e`. Exact integrated matrix remains pending. Real weights and inference are Plan 34, not claimed here.
- **Host preparation review:** independent review of `0566a2cd9` found five blockers: real doctor rejects missing models before fetch; managed custody can release before worker/prompt drainage; raw JSON and native managed-runtime setup are incompatible with the pinned CLI; sync can invalidate earlier source/environment verification; and native attempt evidence needs safe additive projection on failure as well as success. The worker is repairing these and will run real pinned CLI and supervisor CPU proof; no host candidate is approved or merged.
- **Native dependency semantics:** `prepare --deps reuse` is not an equivalent gate (it can report success with incompatible dependencies), while T4 requires sync. Work is tracing the pinned native runtime-layout setup, pre-mutation compatibility checks and post-sync verification. The supervisor socket remains unavailable to the worker.

## Progress 28 (Codex manager, 10 Nov)

- **Explicit auxiliary trust (advisor decision):** under `--align trust`, Astrid must record declaration-supplied auxiliary rows as declared and unverified in dry output, readiness, attempts and durable producer receipts, without checking bytes or refusing absent files. Align/check require digest-verified rows. The pinned native runtime's unconditional `verified_target_provisioning` label must be translated at the Astrid boundary; a supported native unverified-auxiliary mode and repin are deferred to Plan 17. Proof must include an absent declared auxiliary model and all Astrid records.
- **Host candidate:** `744585fa6` is a review checkpoint, not approved or integrated. Focused native attempt/symlink/trust tests passed (6), and preparation/alignment-order checks passed (20). The real pinned CLI fixture reached native prepare and failed; diagnosing the exact failure before retry. Independent review and the real host/supervisor success, failure and cancellation checks remain gates.
- **D2 RunPod gap:** the existing CPU provider simulates pod output; it does not establish dry/live graph, bindings and align-manifest equality through real `local_job.run_job` for every default slot and h3. D2 is extending the shipped-job seam using the facade's actual uploaded files and real machine serialization. Attached CPU-fake cells have passed, with explicit trust for TTS/SFX; no real inference is claimed.

## Progress 29 (Codex manager, 10 Nov)

- **Native preparation (advisor decision):** one shared VibeComfy `prepare_workflow` helper is accepted for managed host and pod-side execution, using the exact frozen canonical path, verified root, native sync report and fresh observation. Keep real doctor, nodes restore, fetch and strict final checks; prove missing-dependency refusal. The CLI wrapper's `OutputSpec` reconciliation bug is Plan 17 C3; no Plan 32 repin.
- **Trust:** independent review found no blocking issue in instance-local trust diagnostic normalization at `606712a8e`; it preserves native authority, schema and non-trust behavior. Additional managed, failure/in-flight, JSONL and exact unverified-row evidence remains to be proven.
- **RunPod seam:** t2i passed through actual facade uploads, `RunPodMachine.start`, real `local_job.run_job`, actual align and full graph/bindings/manifest comparison. TTS exposed a pod-side explicit-trust propagation gap; repair is in progress, using the shared trust normalization rather than a duplicate.

## Progress 30 (Codex manager, 10 Nov)

- **H3 runtime declarations landed:** `f65973763` merges `79d495f39`; six focused compiled-workflow and declaration checks passed, and independent review cleared the scoped fix. Active H3 declarations now match the shared recipe. CPU consistency is proven; real H3 node/GPU compatibility remains Plan 34.
- **Managed host:** native preparation API checkpoint `d4da4927e` passed one real-native plain preparation test; the multi-case host/supervisor journey is still being repaired and rerun. Review requires the same shared helper and strict fresh dependency gate on the pod path. Native trust diagnostic normalization passed focused success/failure snapshot tests and was independently reviewed; final integrated proof remains open.
- **D2:** RunPod t2i passed via actual facade files, real machine serialization, real `local_job.run_job`, align and full graph/bindings/manifest checks. TTS also passed in the parameterized seam; SFX fixture and remaining cells are in progress. The pod must reuse host preparation with safe cancellation and custody.

## Progress 31 (Codex manager, 10 Nov)

- **Managed host proof:** at `07ed95f30`, the real native success path passed with an initially missing artifact fetched from loopback, HTTP readiness before sandboxed worker, successful generation and supervisor socket denied. Four corrected start/cancel/schema/pip cases plus three real local dependency-install/missing/frozen-capsule cases passed (7). This is not yet a final candidate: review identified selected pip-wheel symlink containment to fix, and managed trust plus final integrated review/proof remain open. Real CPython 3.12.3 and the pinned 3.12.10 selector source passed; a full 3.12.10 binary was unavailable locally.
- **RunPod seam:** five non-h3 defaults have passed across focused checkpoints with facade-imported files, real machine serialization and `local_job.run_job`, actual align and full graph/bindings/manifest equality. H3, shared host/pod preparation and final composed proof remain open. Explicit trust uses CPU fake inventory; real inference is not claimed.
- **Product integration head:** `f65973763`. No `GATE-READY` yet: D2 and managed-host/cold-start product work are still unmerged. The latest owner direction runs Plan 34 in parallel with end-gate tests after the last product merge.

## Progress 32 (Codex manager, 10 Nov)

- **Host-managed preparation landed:** `7dbe4eec3` merges reviewed `eaec5b355`. The exact candidate passed 13 serialized real host/native cases, 27 preparation/custody checks and 11 native trust/evidence checks. The success path fetches an initially missing loopback artifact, validates HTTP readiness before the sandboxed worker, generates over HTTP, and denies worker supervisor-socket access. Failure/cancellation and trust cases are included. Independent host review found no remaining blocker on the host scope. Real Python 3.12.3 plus the 3.12.10 selector source were checked; the full 3.12.10 binary was unavailable locally.
- **Still open:** D2 integration and real pod shared-helper caller, managed and RunPod composed invariant proof, cold-start completion on the unified path, i2v heartbeat disposition, CI comparison, final R and T8. This is not yet `GATE-READY`.

## Progress 33 (Codex manager, 10 Nov)

- **Pod shared preparation:** D2 `7edefd517` passed three real installed-engine CPU cases (align, trust and UI-JSON freeze); focused mutation and signal checks passed. Independent review cleared the staged workflow identity repair. Controller recovery regression `e681859e6` passed: unresolved exact-job cancellation fences new claims until the exact pod can be deleted.
- **H3 pod seam:** real `run_job` reached preflight and exposed a dormant empty image input being synthesized as a public string. The fix preserves full graph and refuses blank loaders reachable from declared or target output roots; three focused compatibility checks passed and independent review found no blocker. The real H3 seam rerun and additional multi-root test remain open.
- **Integration:** `7dbe4eec3`; D2 and pod shared-helper work remain unmerged, so no `GATE-READY` or full CI comparison yet. Managed host's separate exact-candidate proof is recorded in progress 32.

## Progress 34 (Codex manager, 10 Nov)

- **Blank-image preflight landed:** `bd49bd5da` merges reviewed slice `c1f67bbca`. Three unit and three serialized integration checks passed. It preserves explicit bindings and the complete graph, refusing blank image loaders reachable from declared or actual target output roots while leaving dormant placeholders unbound.
- **H3 RunPod seam:** at `f6e614cf5`, the functional body passed dry/live bindings, actual align manifest, real `local_job.run_job` and exact submitted graph on a verified pinned-source CPU fixture. Teardown failed because the fake peer wrote a non-PID marker; corrected fixture rerun is required before claiming a pass. The stand-in distribution metadata is test-only and does not prove GPU dependencies or inference.
- **Remaining product work:** D2 seed/graph invariant and shared pod preparation/cancellation; managed and RunPod composed proof. No `GATE-READY` yet. The host preparation and trust slices are already integrated at `7dbe4eec3`.

## Progress 35 (Codex manager, 10 Nov: restart reconciliation)

- **Integration remains** `bd49bd5da`; no GPU gate or subsequent product merge occurred before restart. D2 is clean and pushed at `6f63b4563` on `plan32/codex-manager-d2`.
- **D2 focused review:** independent feature review found no remaining product blockers at `6f63b4563`; prior custom-root and explicit-prefix findings were repaired and reviewed. Exact-candidate managed CPU matrix passed five cells (music/SFX/TTS/edit/h3, 5 in 900.65s) and default t2i (1 in 105.34s); the installed-alternate Z-Image cell also passed (1 in 134.55s). These use trust and CPU stand-ins, not real GPU inference.
- **RunPod invariant:** h3 passed through the real shipped-job seam at `701fd0926` (1 in 258.59s); non-h3 cells passed across earlier checkpoints. The full exact `6f63b4563` matrix was queued/running at restart and has no recorded final result. A resumed worker is checking its evidence then rerunning the required proof under the shared lock. No interrupted run counts as a pass.
- **Remaining gates:** exact composed RunPod and any affected attached proof, D2 integration and `GATE-READY`, one CI full-suite comparison, final R and T8. The earlier i2v lease/heartbeat uncertainty remains open. No paid pods were rented by this run.

## Progress 36 (Codex manager, 10 Nov)

- **D2 landed:** `cc084ebd9cf8d90d417ff302865d747652902390` merges reviewed `6f63b4563`. Its tree is identical to that candidate. Exact-candidate CPU stand-in proof passed: managed six cells (five-cell run plus t2i), managed installed-alternate, attached six and real shipped-job RunPod six including h3. Retained commands/logs: `run/d2-attached-6f63-restart.log` and `run/d2-runpod-6f63-restart.log`; managed results were recorded before restart. Trust/metadata-only stand-ins do not prove real GPU inference.
- **GPU overlap:** `GATE-READY cc084ebd9cf8d90d417ff302865d747652902390` posted to the orchestrator. Later integration merges must be announced with affected paths.
- **End gate:** the single CI dispatch is run `42754272616` on `cc084ebd9`; latest main baseline is run `42553788480` on `a105de3a`. CI comparison, exact-head focused checks and independent final R are running. T8 waits on their results. The i2v bootstrap heartbeat uncertainty remains open.

## Progress 37 (Codex manager, 10 Nov)

- **Final R on `cc084ebd9`:** D7 local device and D8 RunPod policy are dropped after Placement resolution; D9 is a literal h3 grep violation. D7/D8 are routed together because they share SDK placement handling; D9 is independent. The third-party-machine facade concern is explicitly deferred by F3 and is not a blocker. Review budget is at most three owner-agreed rounds; prior consumed count remains to be reconciled, not reset.
- **Independent integrated proof:** exact head `cc084ebd9` passed 29 scoped core checks and 4 serialized owned-pod checks; CI run `42754272616` is still the separate full-suite gate.

- **CI setup failure:** all eight unit shards of run `42754272616` fail before pytest resolving the VibeComfy pin (`UnknownEngine`); fast checks also report lint delta and release-wheel Python 3.12 smoke fails. Scope and causes are being triaged. The baseline lacks `-rA` passed IDs, so `baseline-diff.py` cannot yet classify results; advisor asked how to obtain a valid comparison within the one-dispatch brief.

## Progress 38 (Codex manager, 10 Nov)

- **D9 landed:** `632326bbd` is comment-only; prescribed h3 grep has five lines, all covered by the clarified owner allowlist (HTML tag, hivemind channel, minimax-h3 id and its two vendor endpoints).
- **D10 landed:** `d81b3edf2` fixes CI pin resolution; existing standalone pin-reader test passed (1). `85a3aaa67` adds `-rA`. Authorized CI rerun `42755164624` is in progress; all unit shards reached pytest. Both installed-wheel smoke lanes are pre-existing, matching main baseline run `42553788480`; Windows 13 failures also match that baseline. Ruff gate fails on the clean baseline as well.
- **D7/D8:** candidate device/policy work is under independent review; fixes for warm override lifecycle and inherited device identity are being checked through real readiness and CPU supervisor tests. Idle timeout versus disclosed bound remains an advisor question.

## Progress 39 (Codex manager, 10 Nov)

- **D7/D8 idle decision:** effective RunPod retention is `min(resolved idle_timeout_s, disclosed idle_seconds)` for defaults and explicit requests; zero is preserved and the effective value must appear in placement outcome/receipt. The worker is adding over-bound and zero proof before integrating the reviewed device/policy candidate.
- **CI comparison:** run `42755164624` on `85a3aaa67` reached pytest with `-rA`. Its completed Windows job's 13 failures match the same IDs/errors in main baseline run `42553788480`, job `128954912157`; both installed-wheel smoke lanes fail at the same baseline step. Shards 3, 7, 8 and Darwin have the same three collection errors as baseline; local base `a105de3a` reproduced those errors under the lock (`run/ci-baseline-a105.log`, exit 2). These are pre-existing; remaining unit shards are running. Clean full-tree Ruff 0.12.0 reports 2219 findings on `a105de3a` versus gate baseline 2128, so that gate already fails on main.
- **Baseline rule:** identical failure IDs/errors in the same base-CI job are sufficient baseline proof; local base runs are needed when that evidence is absent. Record any net-new failures once remaining shards finish.

## Progress 40 (Codex manager, 10 Nov)

- **D7/D8 landed:** `e1d06fa97` merges reviewed `34c552241`. Local request/default/ambient device binding reaches owned launch and receipt; differing visibility refuses reuse. RunPod resolved GPU policy reaches quote/claim and lifecycle operations retain the owning provider; effective idle is capped at the disclosed paid bound and reported. CPU focused and full-path cases passed; no real GPU or paid pod proof is claimed. Independent review cleared the final candidate.
- **GPU overlap:** post-gate merge `e1d06fa97` and its affected managed launch/custody/readiness and RunPod policy paths were announced to the orchestrator.
- **CI:** authorized rerun `42755164624` is on `85a3aaa67` and predates D7/D8. Advisor asked whether another exact-head CI dispatch is authorized after fixes; baseline comparison continues for the current run. Final review of the fix diff and any GPU findings remains.

## Progress 41 (Codex manager, 10 Nov)

- **R2 on `e1d06fa97`:** one blocker, R2.1: a successful device override starts the new owned server but leaves the installation receipt bound to the previous launch, so subsequent canonical status/readiness refuses it. The worker is reproducing and repairing under install custody. No blocker found in the reviewed RunPod policy, CI or grep fixes. The owner agreed at most three rounds; the next review covers the fix diff.
- **CI:** rerun `42755164624` remains in progress on `85a3aaa67`; completed unit/Darwin collection errors match main CI and the targeted local base check. Advisor asked whether a final-head CI run is authorized after product fixes.

## Progress 42 (Codex manager, 10 Nov)

- **R2.1 landed:** `41da1ff86b428d1a9359044419f840d0b59d1356` merges reviewed `e070d921e`; managed and direct local starters refresh the authoritative launch and health evidence under custody, with installed-base verification. Candidate proof passed nine CPU integration and eight focused tests. Independent exact-integrated-head proof passed six receipt-helper and four locked integration tests, including device override followed by canonical status/readiness, commit-boundary failures and modified-base refusal (`run/receipt-proof-41da.log`, both inner exits 0). A later malformed-selector retry ran no tests and exited 4.
- **Review:** independent final round 3 found no blocking findings on `e1d06fa97..41da1ff86`, resolving R2.1. This is the last of the three owner-agreed rounds. Further independently reviewed fixes may still be needed if Plan 34 reports a new bug.
- **End gate:** push-triggered CI run `42761569516` is pending on `41da1ff86`. The previous rerun was cancelled by the newer push and is incomplete. Completion preparation and separate Plan 34 validation continue in parallel; no paid pods were rented by this run.

## Progress 43 (Codex manager, 10 Nov)

- **GPU finding G1:** Plan 34 supplied `plan34/fix-machine-liveness` `44d192ec` for incorrect unfinished-custody display and release-owner binding; advisor classified it as a Plan 32 defect. Independent review and CPU proof are in progress before integration. A reported stale RunPod idle-policy test is being compared on main and head (G2).
- **Earlier i2v timeout G3:** advisor directs one rerun of the exact earlier RunPod CPU journey under the lock on `41da1ff86`. A pass leaves the earlier unreproduced heartbeat timeout as a Plan 34 liveness follow-up; another failure requires Plan 32 repair. No paid pods are authorized in this run.
- **End gate:** CI on `41da1ff86` has started; the liveness merge will trigger a new final-head run. Completion preparation remains pending the fix, its review and proof, the journey disposition and final CI comparison.
