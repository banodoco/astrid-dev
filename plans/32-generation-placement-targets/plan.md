# One generation path: requirements, placement, alignment, run, retrieve

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary) · [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (supporting).

## Outcome and scope

Every generation follows one path, whatever its modality (image, edit, video, voice, music, sound effects, h3_av) and wherever it runs (local GPU, an attached ComfyUI, RunPod):

1. **Requirements:** the request yields one manifest of everything it needs: the ComfyUI base, custom nodes pinned to commits, and models with name, subdir, url, sha256 and size.
2. **Placement:** where it runs is decided once and passed down. There is a default, and any single generation can override it.
3. **Align (optional):** the place is brought in line with the manifest. The same function runs locally and on a pod, with a per-generation mode of `align`, `check` or `trust`.
4. **Run:** VibeComfy prepares the ComfyUI prompt, and it is posted to that place's ComfyUI. Readiness is judged against *that place's* inventory.
5. **Retrieve:** outputs come back to a local destination over the same `/view` client for every place.

Modality only changes the contents of the manifest and the entry's declared inputs and outputs. It never adds a branch to the path. **h3_av becomes a VibeComfy plugin entry**, using VibeComfy's existing `vibecomfy.plugins` mechanism (templates, operations, routes), so no h3 code remains on Astrid's path.

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
- **Not included:** multi-pass h3 requests, prepared or qualified workers, resuming a parent job; new providers; Wan2GP ([Plan 12](../12-multiple-inference-routes/plan.md) consumes this plan); splitting `generic_host` ([Plan 13](../13-execution-host-refactor/plan.md)).

## Design

**A RunPod pod is just a machine.** The whole path (requirements, align, compile, check, submit, fetch) runs on the machine where ComfyUI runs, against that machine's own disk. For RunPod, the controller only rents the machine, ships the job, runs the same local command there, copies the outputs back and releases the machine. Nothing ever has to carry "what is on the pod" back to the controller. That one choice removes the bridge-based generation route, the inventory channel, the controller-side model check for remote places, the `source_video` upload problem, and h3_av's separate pod route.

There are four pieces, each the only one of its kind:

| Piece | Shape | Replaces |
|---|---|---|
| **Manifest** | `requirements(entry, inputs) -> {comfyui, nodes[repo, commit], models[name, subdir, url, sha256, size]}`, built from VibeComfy's per-workflow `ReadyMetadata`, which already holds these rows | about six requirement shapes; name-only `requirements`; engines as fixed model bundles |
| **Placement** | frozen `{kind: local / attached / runpod, device or endpoint, policy}`, resolved request → project → user → built-in in one place | five re-inference sites; `--target` strings; `target_policy`; the dropped `placement` parameter |
| **`run(job, placement)`** | **local:** start or reuse a ComfyUI on this machine (the chosen GPU), `align(manifest, mode)` against this disk, compile, submit to localhost, fetch over `/view`. **attached:** the user's ComfyUI URL; `check` (object_info) or `trust`, never `align`; submit and `/view`. **runpod:** claim a machine under the existing paid-consent and lease owner, ship the job, run `run(job, local)` on it with one generic remote Astrid invocation (runpod-lifecycle `ship_and_run`), fetch the outputs with a digest manifest, release | three profiles (`pip_embedded`, `local_server`, `checkout_server`); the generation bridge and its binding record; Plan 33's interim inventory wire; two `/view` clients; h3's own pod command |
| **`align(manifest, mode)`** | `align` fetches only the missing manifest rows and installs missing nodes; `check` reports; `trust` skips and marks the result unverified. It always runs locally, on whichever machine runs ComfyUI, and **is VibeComfy's own commands** (`doctor`, `prepare --deps sync`, `nodes restore`, `fetch`). The Agent keeps only the ComfyUI-core install, which VibeComfy lacks | `generate align` vs `engines install`; the Agent's duplicate downloader and node installer (`model_downloader.py`, `engine_runner.py` model steps); VibeComfy's hidden `ensure_models` download; whole-lock readiness (`engine_readiness.py:745-756`) |

**Engines** shrink to a base environment: pinned ComfyUI, Python and a node set. Models come from the manifest. Model locks become caches of manifest rows, and release identity stops binding the whole models lock. The storage volume is a model root a RunPod machine can mount.

**Leases stay minimal:** an owner and an idle timeout (by default beyond the job, overridable in the Placement policy). Because every slot shares one base environment, a warm machine is reusable by any later job. An orphaned machine is a bug by construction.

**Modality is data.** The entry declares its modes, inputs (including media such as a source video) and outputs, plus at most one optional `finalize` step. `finalize` is the only new piece: it is post-processing such as ffmpeg compose and verify, run on the same machine after the outputs come back, because VibeComfy has no hook for code that runs after ComfyUI. There is one `generate(entry, inputs, placement)`, with image, video and audio as thin aliases. Refusals come from entry data, in one place.

**Terms, one meaning each** (renamed as each task touches the code):
- **engine:** a base environment recipe.
- **placement:** where a job runs.
- **machine:** where ComfyUI runs (local or rented).
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

Plan 33 lands first. Its CPU pod-path test is the characterization. Then:

1. T1: characterize every capability.
2. T2: Manifest and base engines.
3. T3: Placement.
4. T4: the local run path, with `align`.
5. T5: RunPod as a remote machine.
6. T6: one `generate`, with h3_av as a job.
7. T7: live proof; then T8: completion.

T2 and T3 can run in parallel. T4 needs both, and T5 needs T4. Each task deletes what it replaces in the same change, so no task leaves two ways of doing one thing. See [tasks.md](tasks.md).

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
- `grep -ri h3 astrid/core astrid/sdk` returns nothing (about 156 lines today).
- A live proof runs the same matrix on RunPod and locally (T7).

The proof does not cover new providers, Wan2GP or the `generic_host` split. [F-003](../../vision/gaps/F-003-creative-execution.md) does not close automatically.
