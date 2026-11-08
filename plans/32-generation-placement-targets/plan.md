# One generation path: requirements, placement, alignment, run, retrieve

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

Every generation follows one path, whatever its modality (image, edit, video, voice, music, sound effects, h3_av) and wherever it runs (local GPU, an attached ComfyUI, RunPod):

1. **Requirements:** the request yields one manifest of everything it needs: the ComfyUI base, custom nodes pinned to commits, and models with name, subdir, url, sha256 and size.
2. **Placement:** where it runs is decided once and passed down. There is a default, and any single generation can override it.
3. **Align (optional):** the place is brought in line with the manifest. The same function runs locally and on a pod, with a per-generation mode of `align`, `check` or `trust`.
4. **Run:** VibeComfy prepares the ComfyUI prompt, and it is posted to that place's ComfyUI. Readiness is judged against *that place's* inventory.
5. **Retrieve:** outputs come back to a local destination over the same `/view` client for every place.

Modality only changes the contents of the manifest and the entry's declared inputs and outputs. It never adds a branch to the path.

The short-term unblock (the inventory wire, the sfx and h3_av routing, warm reuse within a lease) is [Plan 33](../33-unblock-live-generation/plan.md). This plan replaces the mechanisms Plan 33 patches.

- **Included:**
  - one requirements function;
  - one Placement value, with a default and an override (including which local GPU);
  - one PlacementBinding that each kind of place produces;
  - one `align` function;
  - per-request model sets, so a pod fetches only what the job needs;
  - the storage volume as a model cache;
  - one submit and one retrieve;
  - one `generate` entry point, with modality as data;
  - h3_av as an ordinary job;
  - sessions as leases (pods may outlive a job);
  - deleting every superseded route;
  - one meaning per term.
- **Not included:** new providers; Wan2GP ([Plan 12](../12-multiple-inference-routes/plan.md) consumes this plan); splitting `generic_host` ([Plan 13](../13-execution-host-refactor/plan.md)).

## Design

Five pieces, each owned by one layer and each the only one of its kind:

| Piece | Shape | Owner | Replaces |
|---|---|---|---|
| **Manifest** | `requirements(entry, inputs) -> {comfyui, nodes[repo, commit], models[name, subdir, url, sha256, size]}`, built from VibeComfy's per-workflow `ReadyMetadata`, which already holds these rows | generation entries | about six requirement shapes, name-only `requirements`, and engines as fixed model bundles |
| **Placement** | frozen `{kind: local / attached / runpod, device or endpoint, policy}`; resolved request → project → user → built-in, in one place | generation facade | five re-inference sites; `--target` strings, `target_policy`, the dropped `placement` parameter |
| **PlacementBinding** | `{placement, endpoint, inventory{object_info_sha256, models[...]}, attestation}`, produced by the place: local from its model root, attached from object_info (plus an optional declared models dir), RunPod from the pod's verified receipt | the Target for that kind | the bare `comfy_url`, readiness profiles, the execution-request env channels, and Plan 33's interim channel |
| **align(binding, manifest, mode)** | `align` fetches only the missing manifest rows and installs the missing nodes; `check` reports; `trust` skips and marks the result unverified. It is the same code locally and on the pod (the pod runs the same CLI), and the receipt records the rows actually present | the Target | `generate align` vs `engines install` vs VibeComfy's hidden `ensure_models` download; the whole-lock readiness (`engine_readiness.py:745-756`) |
| **run and retrieve** | VibeComfy compiles against a provider built from the binding, posts `/prompt` and fetches over `/view`. A local GPU is a ComfyUI server Astrid starts, so it takes the same HTTP path | the VibeComfy pack | three profiles (`pip_embedded`, `local_server`, `checkout_server`), two `/view` clients, embedded copy-out |

**Engines** shrink to a base environment: a pinned ComfyUI plus Python plus a node set. Models are no longer part of an engine; they come from the manifest. Model locks become caches of manifest rows. The storage volume is a model root that a placement can mount.

**Sessions are leases, not job-scoped.** A pod may outlive the job that started it. A warm session is reused by any later job whose base engine matches. Each session has an owner and an idle timeout (by default beyond the job, overridable in the Placement policy), and the Target releases it when the lease expires. An orphaned session is a bug by construction.

**Modality is data.** The entry declares its modes, inputs (including media such as a source video) and outputs. There is one `generate(entry, inputs, placement)`. Image, video and audio become thin aliases. Refusals come from entry data in one place, never from per-modality code.

**Terms, one meaning each** (renamed as each task touches the code):
- **engine:** a base environment recipe.
- **placement:** the decision of where a job runs.
- **target:** the implementation for a kind of place.
- **binding:** a prepared place plus its inventory.
- **attached:** a user-owned server that can be checked or trusted but not aligned.
- **managed:** installed by Astrid, with a receipt.
- **readiness:** the result of checking a binding against a manifest.
- **approval:** renamed `target check`.
- **custody:** kept only for Runtime source trust.

The full glossary and the list of renames are in [inputs.md](inputs.md#planning-evidence).

## Existing work and decision

- **The merge run's path review** (`merge-run/path-review/` on the desk) traced every step against the vision above. Its verdict, from an independent review: the system is mostly design debt that keeps showing up as missing wires.
  - Placement carries no inventory.
  - Requirements are per engine, not per request.
  - Alignment is a hidden precondition.
  - The only test of the pod path was a paid live run.
- **Retained:**
  - VibeComfy's target custody and `ReadyMetadata` rows;
  - `catalog_manifests` and `_lock_coverage` (`core/generation/asset_alignment.py`, `entries.py`) as the base of `requirements()`;
  - the existing downloader and receipt parser;
  - the bridge;
  - Plan 33's inventory wire, CPU pod-path test and warm reuse.
- **Owner scope** (8 Nov 2026), unchanged from the first version: a default placement that can be overridden per generation, including the device; sessions as leases that can outlive a job. The details and the challenge are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Plan 33 lands first. Its CPU pod-path test is the characterization. Then:

1. T1: characterize every capability.
2. T2: Manifest.
3. T3: Placement.
4. T4: PlacementBinding and `align`.
5. T5: one run and retrieve.
6. T6: one `generate`, with h3_av as a job.
7. T7: live proof; then T8: completion.

T2 and T3 can run in parallel; T4 needs both. Each task deletes what it replaces in the same change, so no task leaves two ways of doing one thing. See [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:** [Plan 33](../33-unblock-live-generation/plan.md)'s landed revision, which brings the CPU pod-path test, the receipt-row inventory and warm reuse. Its exact revision is recorded in [inputs.md](inputs.md#source-identities).
- **Produces:** `requirements()`, the Placement value, PlacementBinding and `align`, plus the Target lifecycle (local, attached, RunPod). [Plan 12](../12-multiple-inference-routes/plan.md) builds Wan2GP on these. [Plan 25](../25-cloud-assist-v1/plan.md) reuses Placement, the binding and the storage-volume model cache.

## Completion

- Every default slot and h3_av, under each placement (local, attached, RunPod), goes through the five steps with no per-modality branch. A grep and the invariant test show one placement decision site, one refusal site, one submit and one retrieve.
- A RunPod job fetches only its manifest's missing models. With the storage volume mounted, a warm cache fetches nothing.
- `align`, `check` and `trust` behave the same locally and on RunPod.
- The dry run equals the live run.
- No orphaned session exists, and warm sessions are reused within their lease.
- A live proof runs the same matrix on RunPod and locally (T7).

The proof does not cover new providers, Wan2GP or the `generic_host` split. [F-003](../../vision/gaps/F-003-creative-execution.md) does not close automatically.
