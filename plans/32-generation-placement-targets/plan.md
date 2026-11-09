# One generation path: requirements, placement, alignment, run, retrieve

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary) · [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (supporting).

**Contributes to closure:** F-008 step 2: the same request through the same path on a local GPU, a user's ComfyUI and RunPod; a default placement overridden per generation; align, check and trust the same everywhere; one placement site, one submit and one retrieve with no per-modality branch; h3_av as a VibeComfy plugin; lease release with no orphan; and a test provider showing a further machine kind fits the contract. Milestone B on CPU; its live half is a later pass of [Plan 34](../34-real-gpu-proof/plan.md).

## Outcome and scope

Every generation follows one path, whatever its modality (image, edit, video, voice, music, sound effects, h3_av) and wherever it runs (local GPU, an attached ComfyUI, RunPod):

1. **Requirements:** the request yields one manifest of everything it needs: the ComfyUI base, custom nodes pinned to commits, and models with name, subdir, url, sha256 and size.
2. **Placement:** where it runs is decided once and passed down. There is a default, and any single generation can override it.
3. **Align (optional):** the place is brought in line with the manifest. The same function runs locally and on a pod, with a per-generation mode of `align`, `check` or `trust`.
4. **Run:** VibeComfy prepares the ComfyUI prompt, and it is posted to that place's ComfyUI. Readiness is judged against *that place's* inventory.
5. **Retrieve:** the engine writes its outputs to the job directory; the machine copies that directory back under a digest manifest. How an engine collects its own outputs (ComfyUI's `/view`, Wan2GP's spool) stays inside that engine.

Modality only changes the contents of the manifest and the entry's declared inputs and outputs. It never adds a branch to the path. **h3_av becomes a VibeComfy plugin entry**: one pack with one `vibecomfy.workflows` contribution (ready root, entries, optional `build` and `finalize`). No h3 code remains on Astrid's path.

The short-term unblock (the inventory wire, the sfx and h3_av routing, warm reuse within a lease) is [Plan 33](../33-unblock-live-generation/plan.md). This plan replaces the mechanisms Plan 33 patches.

- **Included:**
  - one requirements function;
  - one Placement value, with a default and an override (including which local GPU);
  - one local run path (Astrid starts ComfyUI, aligns, submits, fetches);
  - RunPod as a remote machine that runs that same local path;
  - attached servers checked or trusted;
  - per-request model sets and the storage volume as a model cache;
  - warm reuse under a minimal lease;
  - one `generate` entry point, with modality as data;
  - h3_av as a VibeComfy plugin entry, with h3's existing pod route generalized into the RunPod machine route;
  - deleting every superseded route;
  - one meaning per term.
- **Not included:** multi-pass h3 requests, prepared or qualified workers, resuming a parent job; VibeComfy ops and router as an Astrid call path; new providers; Wan2GP ([Plan 12](../12-multiple-inference-routes/plan.md) consumes this plan); splitting `generic_host` ([Plan 13](../13-execution-host-refactor/plan.md)).
- **Follow-up (owner, 9 Nov): providers on the one path.** fal, OpenAI and Wavespeed (`astrid/core/generation/backends/{fal,openai,wavespeed}.py`) stay a separate `--backend cloud` route in this plan. The follow-up makes a provider a placement kind with only an `execute` step: nothing to align, no machine to rent, outputs in the job directory, and the same `generate(entry, inputs, placement)`. It is planned with astrid-dev-plan when this plan completes.

## Design

**A RunPod pod is just a machine.** The whole path (requirements, align, compile, check, submit, fetch) runs on the machine where the engine runs, against that machine's own disk. For RunPod, the controller only rents the machine, ships the job, runs the same local command there, copies its progress file back on each poll, copies the outputs back and releases the machine. A remote job shows progress and cancels like a local one, through the host's existing progress file and cancel check. Nothing ever has to carry "what is on the pod" back to the controller. That one choice removes the bridge-based generation route, the inventory channel, the controller-side model check for remote places, the `source_video` upload problem, and h3_av's separate pod route.

There are four pieces, each the only one of its kind:

| Piece | Shape | Replaces |
|---|---|---|
| **Manifest** | `requirements(entry, inputs) -> {engine, base, models[name, subdir, url, sha256, size], extra}`, built by the engine contribution. `extra` belongs to the engine and is validated by it (ComfyUI: `nodes[repo, commit]`). For ComfyUI the rows come from VibeComfy's per-workflow `ReadyMetadata`, which already holds them | about six requirement shapes; name-only `requirements`; engines as fixed model bundles |
| **Placement** | frozen `{kind: local / attached / runpod, device or endpoint, policy}`, resolved request → user default → built-in in one place. It is task data: the Runtime target stays `default`, and the controller's host claims the task and drives the machine | five re-inference sites; `--target` strings; `target_policy`; the dropped `placement` parameter |
| **`run(job, placement)`** | **local:** the engine's `align(manifest, mode)` against this disk, then its `execute(job)` on this machine (the chosen GPU); ComfyUI's starts or reuses a ComfyUI and submits to localhost. **attached:** `{engine, endpoint}`; the engine's `probe(endpoint)` (ComfyUI: object_info) or `trust`, never `align`; an engine without `probe` cannot be attached. **runpod:** claim a machine under the existing paid-consent and lease owner, start `run(job, local)` on it with one generic remote Astrid invocation (the detached job in `remote_placement._run_job`), copy its progress file back on each poll, fetch the job directory with a digest manifest, release; cancel is `job_cancel`, then release | three profiles (`pip_embedded`, `local_server`, `checkout_server`); the generation bridge and its binding record; Plan 33's interim inventory wire; two `/view` clients; h3's own pod command |
| **`align(manifest, mode)`** | `align` fetches only the missing manifest rows and installs missing nodes; `check` reports; `trust` skips and marks the result unverified. It always runs locally, on whichever machine runs the engine, and belongs to the engine contribution. The `comfyui` engine's `align` is VibeComfy's own commands (`doctor`, `prepare --deps sync`, `nodes restore`, `fetch`), and the Agent keeps only the ComfyUI-core install, which VibeComfy lacks | `generate align` vs `engines install`; the Agent's duplicate downloader and node installer (`model_downloader.py`, `engine_runner.py` model steps); VibeComfy's hidden `ensure_models` download; whole-lock readiness (`engine_readiness.py:745-756`) |

**Engine-neutral from the start.** The engine table is built from `generation.engine` contributions, using the existing extension protocol (`astrid/core/extensions`, [Plan 17](../17-vibecomfy-extensibility/plan.md)). Only `vibecomfy.comfyui` exists in this plan; [Plan 12](../12-multiple-inference-routes/plan.md) adds `wan2gp` as a second contribution. Machines are the same: a `generation.machine` point, with RunPod and T5's test provider as contributions, and `local` and `attached` built in. Environment setup is the `align` half of the engine point. Core owns the `align`, `check` and `trust` mode, running it on the machine, the volume and receipts. Each engine defines what aligned means for it. The manifest names its `engine` (`comfyui` first, then `wan2gp`) and its `base` environment. `run()` picks the engine's `align` and `execute` from that table at one site, and `run` returns files in the job directory, whatever the engine. The engine protocol is `requirements(entry, inputs)`, `align(manifest, mode)`, `execute(job) -> files in job.out`, `cancel(job)` and an optional `probe(endpoint)`; core never names an engine's internals. For ComfyUI, the base is a pinned ComfyUI, Python and a node set; for Wan2GP, its pinned source and requirements. Models come from the manifest. Model locks become caches of manifest rows, and release identity stops binding the whole models lock. The storage volume is a model root a RunPod machine can mount.

**Leases stay minimal:** an owner and an idle timeout (by default beyond the job, overridable in the Placement policy). A warm machine is reusable by any later job, so the lease is keyed on machine custody (account, GPU, image, volume, shipped source digest), and each job aligns its own base and models. Switching between engines never forces a new machine. An orphaned machine is a bug by construction.

**Modality is data.** The entry declares its modes, inputs (including media such as a source video) and outputs, plus an optional `build` (the graph built from the inputs, on CPU, also used by the dry run) and an optional `finalize` step. These are the only new pieces, both typed fields of the `vibecomfy.workflows` point. `finalize` is for post-processing such as ffmpeg compose and verify, run on the same machine after the outputs come back, because VibeComfy has no hook for code that runs after ComfyUI. There is one `generate(entry, inputs, placement)`, with image, video and audio as thin aliases. Refusals come from entry data, in one place.

**Terms, one meaning each** (renamed as each task touches the code):
- **engine:** a base environment recipe.
- **placement:** where a job runs.
- **machine:** where the engine runs (local or rented).
- **attached:** a user-owned server that can be checked or trusted but not aligned.
- **managed:** installed by Astrid, with a receipt.
- **readiness:** the result of `align` in `check` mode.
- **approval:** renamed `target check`.
- **custody:** kept only for Runtime source trust.

The full rename list is in [inputs.md](inputs.md#planning-evidence).

## Existing work and decision

- **The merge run's path review** (`merge-run/path-review/` on the desk) traced every step against the vision above. Its verdict, from an independent review: the system is mostly design debt that keeps showing up as missing wires.
  - Placement carries no inventory.
  - Requirements are per engine, not per request.
  - Alignment is a hidden precondition.
  - The only test of the pod path was a paid live run.
- **Retained:**
  - VibeComfy's `ReadyMetadata` rows;
  - `catalog_manifests` and `_lock_coverage` (`core/generation/asset_alignment.py`, `entries.py`) as the base of `requirements()`;
  - the existing downloader;
  - runpod-lifecycle's `ship_and_run`;
  - the generic remote helpers in `packs/runpod/remote_placement.py` (`_run_job`, `_download`, `_release`);
  - the paid-consent and lease owner;
  - Plan 33's CPU pod-path test and `--align check|trust`.
- **Chosen over the alternatives:** an independent sense check (`merge-run/path-review/PLAN-SENSE-CHECK.md`) found that keeping the remote-ComfyUI model needs three objects (Placement, a PlacementBinding with the pod's inventory, and a Target interface) just to carry "what is on the pod" back to the controller. Running the path on the machine needs one Placement value and one `run`.
- **Owner scope** (8 Nov 2026), unchanged from the first version: a default placement that can be overridden per generation, including the device; sessions as leases that can outlive a job. The details and the challenge are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Plan 32 runs alongside Plan 33 and does not wait for any GPU proof (owner, 8 Nov). Plan 34 runs once, after this plan. Plan 33's CPU pod-path test is the characterization. Then:

1. T1: characterize every capability.
2. T2: the manifest and the engine point.
3. T3: Placement, then T2b: one base engine, with the `comfyui` and `comfy_wrap` packs deleted (owner, M-79).
4. T4: the local run path, with `align`.
5. T5: RunPod as a remote machine, through the machine point.
6. T6: one `generate`, with the `vibecomfy.workflows` point and its `build` and `finalize` hooks; then T6b: h3_av becomes one contribution.
7. The review rounds, then T8: completion.

All of it is CPU only. The live proof (T7) is a later pass of [Plan 34](../34-real-gpu-proof/plan.md). T2 and T3 can run in parallel. T2b needs both, T4 needs T2b, and T5 needs T4. Each task deletes what it replaces in the same change, so no task leaves two ways of doing one thing. See [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:** [Plan 33](../33-unblock-live-generation/plan.md)'s landed revision, which brings the CPU pod-path test, the receipt-row inventory and warm reuse. Its exact revision is recorded in [inputs.md](inputs.md#source-identities).
- **Produces:** `requirements()`, the Placement value, `run(job, placement)` and `align`, plus the remote-machine lifecycle with a lease. [Plan 12](../12-multiple-inference-routes/plan.md) builds Wan2GP on these. [Plan 25](../25-cloud-assist-v1/plan.md) reuses Placement, the remote machine and the storage-volume model cache.

## Completion

- Every default slot and h3_av, under each placement (local, attached, RunPod), goes through the five steps with no per-modality branch. A grep and the invariant test show one placement decision site, one refusal site, one submit and one retrieve.
- A RunPod job fetches only its manifest's missing models. With the storage volume mounted, a warm cache fetches nothing.
- `align`, `check` and `trust` behave the same locally and on RunPod, because on RunPod they run on the machine itself.
- The controller never checks model files for a RunPod job (grep: no generation bridge, no inventory channel).
- The dry run equals the live run.
- No orphaned machine exists, and warm machines are reused within their lease.
- A remote job's progress reaches the local run while it runs, and cancelling it releases the machine.
- Scale is the host's concurrency times its live leases. A pod-side Runtime worker is out of scope: the Runtime binds only to loopback (`runtime_protocol/daemon.py:64-66`).
- A test machine contribution runs a job through the same `generation.machine` contract.
- `grep -ri h3 astrid/core astrid/sdk` returns nothing (about 156 lines today).
- All of the above is CPU evidence (owner, 8 Nov). Not proven by this plan: real inference, real model downloads, RunPod capacity and the volume on a real pod. The live proof (T7) is a later pass of [Plan 34](../34-real-gpu-proof/plan.md) (real-GPU proof), which follows Plan 33.

The proof does not cover new providers, Wan2GP or the `generic_host` split. [F-003](../../vision/gaps/F-003-creative-execution.md) does not close automatically.
