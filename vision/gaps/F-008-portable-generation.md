# F-008 — Generation isn't yet one portable, extensible path across machines and inference engines

**Aspiration:** [One generation path, any engine, any machine](../principles/eliminate-needless-technical-wrangling.md#one-generation-path-any-engine-any-machine) (primary) · [Everything local or cloud, by choice](../principles/local-first-cloud-capable.md#everything-local-or-cloud-by-choice) (supporting) · [Built to be found and reused](../principles/open-by-design.md#built-to-be-found-and-reused) (supporting) · [A small, dependable foundation](../pillars/liquid-software.md#a-small-dependable-foundation) (supporting) · **Assessment:** Open; path review and live RunPod attempts (2026-11-08).

## Desired state

The [generation aspiration](../principles/eliminate-needless-technical-wrangling.md#one-generation-path-any-engine-any-machine) is proven for every supported slot, including composed workflows such as h3_av, across local GPUs, a user's server and rented machines. Requests declare custom-node and model requirements and support align, check and trust modes; results return to the creator.

ComfyUI through VibeComfy is the first engine, with Wan2GP providing the second-engine proof. Rented machines can be reused while warm and retain models on attached storage, so a second job does not download them again. A new workflow, engine or provider meets its declared contract without a new route through Astrid's core.

## Current state

- **On RunPod, live attempts on 7–8 Nov 2026 produced image and edit; voice and music did not produce an output.**
  - Placement is re-decided in several places.
  - A rented pod is driven as a remote ComfyUI, so checks ran against the controller's disk.
  - Every fresh pod downloads one fixed 95.8 GB model bundle, whatever the job.
  - Pods can't be reused across jobs, and the storage volume is used only off the main path.
- **Some slots don't follow the common path.**
  - Sound effects is refused on RunPod.
  - h3_av has its own pod route.
  - About 50 sites branch by modality.
- **Building blocks exist but are not on one path.** VibeComfy already offers requirements, node install, model fetch and run commands that the Agent partly duplicates.
- **Only one engine works.** Wan2GP is a stub.

The evidence is the merge-run path review in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`, `merge-run/path-review/` (VISION, HOLISTIC, EXISTING-MACHINERY and the audits).

## Gap

There is no single, engine-neutral generation path whose placement is decided once, and its levels (workflows, engines, machines) can't yet be extended independently. Creators can't freely choose and change where a generation runs, or which inference engine runs it, and get the same behaviour, setup and result every time. Distinct from [F-003](F-003-creative-execution.md), which is about one creative job being dependable end to end on a stated setup, and from [F-005](F-005-local-files-cloud-assist.md), which is about the local-data and cloud-execution product boundary.

## Closure evidence

**Same request, different machines.** The same generation request, for every default slot plus h3_av, produces its result through the same code path on:
- a local GPU;
- a user's own ComfyUI;
- a rented RunPod machine.

**Placement is one decision.** A default placement is set and overridden for a single generation.

**Rented machines are efficient.**
- A second job reuses a warm machine.
- Models already on attached storage are not downloaded again.
- Align, check and trust behave the same everywhere.

**Each level extends independently.**
- A second inference engine (Wan2GP) runs a generation through the same placement, lease and machine route, adding only its own setup and run step.
- A workflow added as a VibeComfy plugin (h3_av) runs with no plugin-specific code in Astrid's core.
- A further kind of machine or provider can be added behind the same placement and lease contract, shown at least with a test provider, without changing the path.

**One path in the code.** Source inspection shows one placement decision site, one submit and one retrieve, and no per-modality branch on the path.

**Negative cases:** a missing model fails before submit, naming the machine; an expired lease releases the machine; no orphaned machine remains.

## Closure approach

**The idea.** Generation is one short path with replaceable pieces. VibeComfy already knows what each workflow needs and how to set up and run ComfyUI. A rented RunPod pod is just another machine. So the strategy is to stop the controller from reaching into remote machines, and instead run the same local path wherever the work runs: declare needs, choose the machine once, align it if asked, run, and bring the files back. Each level then becomes a slot that can be extended without touching the others:
- workflows (`vibecomfy.workflows`);
- engines (`generation.engine`);
- machines and providers (`generation.machine`).

Each is a point in Astrid's existing pack extension protocol, which packs fill and can combine.

**Why this order.** First make every slot work on today's route, so creators get results and the landing of the generation and pack work is proven live. Do it with deletions and small wires rather than new structure: the sound-effects refusals, h3_av's own pod route, a cached model volume and reusable pods. Then replace that route with the one path. Placement is decided once. The pod runs the local path itself. Alignment is VibeComfy's own commands with `align`, `check` or `trust`. Each job fetches only its models. h3_av becomes a VibeComfy plugin entry. Making names engine-neutral there costs a few lines, and later saves a rewrite. Only then add the second engine (Wan2GP) and document the plugin contract with a second plugin, because both need the one path to plug into.

**What creators notice at each stage.**
- First, every default slot and h3_av produce results on RunPod, models download once, and a warm pod is reused.
- Second, the same request runs the same way on their own GPU, their own ComfyUI or a rented machine, with a default they choose and can override.
- Third, new engines and community workflows appear without Astrid changing its core.

**Deliberately out.** Out of scope: new cloud APIs (everything runs on our own compute), attaching a user-owned Wan2GP instance, multi-pass h3 requests, and Astrid-wide composability beyond generation ([LS-003](LS-003-full-stack-contributions.md), [LS-004](LS-004-cross-modal-foundations.md)).

## Route to closure

| Step | Plan | Contributes (closure evidence it delivers) | Milestone |
|---|---|---|---|
| 1 | [Plan 33](../../plans/33-unblock-live-generation/plan.md) | On RunPod: a warm machine reused, models on attached storage not re-downloaded, `--align check\|trust`, a missing model failing before submit and naming the machine | A: every default slot and h3_av produce results on RunPod |
| 1b | [Plan 34](../../plans/34-real-gpu-proof/plan.md) | The same milestone proven on real GPUs: real outputs per slot, models downloaded once to the volume, a warm pod reused | A on hardware |
| 2 | [Plan 32](../../plans/32-generation-placement-targets/plan.md) | The same request through the same path on a local GPU, a user's ComfyUI and RunPod; a default placement overridden per generation; align, check and trust the same everywhere; one placement site, one submit, one retrieve, no per-modality branch; h3_av as a VibeComfy plugin with no h3 code in core; an expired lease releasing the machine, with no orphan; a test provider showing a further machine kind fits the contract | B: one path on any machine |
| 3 | [Plan 12](../../plans/12-multiple-inference-routes/plan.md) ∥ [Plan 17](../../plans/17-vibecomfy-extensibility/plan.md) | A second engine (Wan2GP) on the same path (Plan 12); the pack extension protocol switched on and proven with a second, non-h3 composite pack (Plan 17) | C: extensible at every level |
| — | unplanned | Paid consent given once per lease rather than per job; VibeComfy owning the whole ComfyUI environment, including ComfyUI itself; splitting the host file (owned by Plan 13, not a closure item) | — |

Critical path: Plan 33 U1 → U2 → U4 → U9, then Plan 34 G1–G2, then Plan 32 T1 → T2 → T4 → T5 → T6, then Plan 12's wiring. Plan 12's scoping and Linux recipe run alongside Plan 32 T2–T5, and Plan 17 runs alongside Plan 12.

## Sources and reassessment

- **Path review:** `merge-run/path-review/` in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`: VISION, HOLISTIC, PLAN-SENSE-CHECK, H3-AS-VIBECOMFY-EXTENSION, EXISTING-MACHINERY and INFERENCE-ROUTES-SEQUENCING.
- **Related:** [Plan 25](../../plans/25-cloud-assist-v1/plan.md) reuses the result.

Reassess from tested revisions and live runs, updating the assessment and the route as each plan lands. A plan alone does not close this gap.
