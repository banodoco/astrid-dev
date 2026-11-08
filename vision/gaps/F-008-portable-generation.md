# F-008 — Generation isn't yet one portable, extensible path across machines and inference engines

**Applies to:** [Eliminate needless technical wrangling](../principles/eliminate-needless-technical-wrangling.md) (primary) · [Local-first, cloud-capable](../principles/local-first-cloud-capable.md) (supporting) · [Open by design](../principles/open-by-design.md) (supporting) · [Agent-Powered Liquid Software](../pillars/liquid-software.md) (supporting) · **Assessment:** Open; path review and live RunPod attempts (2026-11-08).

## Desired state

Any generation, in any modality (image, edit, video, voice, music, sound effects and composed workflows such as h3_av), runs through **one path**:
1. Declare what the request needs: custom nodes and models.
2. Choose where it runs once: this machine and a chosen local GPU, a user's own server, or a rented GPU machine such as RunPod. There is a default the creator sets and can change per generation.
3. Optionally bring that machine in line with the needs (align, only check, or trust what is there).
4. Run it on the chosen inference engine. ComfyUI through VibeComfy comes first; others such as Wan2GP follow.
5. Get the result back.

A rented machine behaves like any other machine: it runs the same path. It can be reused while warm, and it keeps models on attached storage so they are downloaded once. **Every level is a replaceable piece**, extended through a declared contract rather than a core change:
- **workflows:** a VibeComfy plugin adds templates such as h3_av;
- **engines:** ComfyUI, Wan2GP;
- **machines and providers:** local GPU, a user's server, RunPod, another rented-GPU provider.

Adding one reuses the rest of the path rather than adding per-modality or per-pack routes.

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

## Sources and reassessment

The rectifying sequence:
1. [Plan 33](../../plans/33-unblock-live-generation/plan.md): unblock every slot live on today's route.
2. [Plan 32](../../plans/32-generation-placement-targets/plan.md): the one path; a pod is just a machine; VibeComfy does align and run; h3_av is a VibeComfy plugin.
3. [Plan 12](../../plans/12-multiple-inference-routes/plan.md): Wan2GP on the same path.
4. [Plan 17](../../plans/17-vibecomfy-extensibility/plan.md): the plugin contract.

[Plan 25](../../plans/25-cloud-assist-v1/plan.md) reuses the result. Astrid-wide composability beyond generation (UI, timeline, packs) is [LS-003](LS-003-full-stack-contributions.md) and [LS-004](LS-004-cross-modal-foundations.md). Reassess from tested revisions and live runs; a plan alone does not close this gap.
