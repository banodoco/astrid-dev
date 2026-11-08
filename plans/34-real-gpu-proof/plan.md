# Real-GPU proof of generation

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary) · [Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting).

**Contributes to closure:** F-008 step 1b: every default slot and h3_av produce real outputs on RunPod, with models downloaded once to the storage volume and a warm pod reused. Milestone A, proven on hardware.

## Outcome and scope

The CPU-proven generation path from [Plan 33](../33-unblock-live-generation/plan.md) produces real outputs on real GPUs. The proof is image, edit, voice, music, sound effects, and h3_av on the Matrix clip (80.886–83.305 s), each sent to the owner. Plans 33 and 32 are CPU only, so this plan proves what CPU cannot: real inference, real model downloads, real custom-node installs, and RunPod capacity.

- **Included:**
  1. **VibeComfy smoke on one pod.** Run each slot's workflow directly with VibeComfy's own commands, with no Astrid routing. This separates "this model or node fails on a GPU" from "our routing is wrong", and fills the storage volume once.
  2. **The Astrid route.** Run `astrid generate --target runpod` for every slot on the Plan 33 landing candidate, using the volume cache and warm reuse.
  3. **A pod census** before and after every run.
  4. **Local-managed voice on a real GPU.** Run voice through Astrid's managed local install, with the real weights present. Plan 33's CPU harness can't run this case, because VibeComfy verifies each model's sha256 (strict xfail in `test_runpod_slot_path_cpu.py::test_local_managed_voice`). Run it where a local GPU exists; otherwise run it on the pod as a local placement.
  5. **A later pass, after [Plan 32](../32-generation-placement-targets/plan.md):** the same matrix on its one path, locally where hardware exists and on RunPod.
- **Not included:** code changes. A failure that is "the controller and the pod disagree" is recorded and goes to Plan 32 rather than being patched here.

## Existing work and decision

Built from the live attempts of 7–8 Nov 2026 and the path review on the merge-run desk (`banodoco/astrid-overnight-2026-11-05`, `merge-run/path-review/`). The owner set the order on 8 Nov: Plan 33 on CPU, then this plan, then Plan 32. Later the same day the owner started Plan 32 alongside Plan 33, so this plan's first pass now runs in parallel with Plan 32, once Plan 33 lands. See [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Starts after Plan 33's CPU tasks and review pass, on the owner's go and a RunPod budget. The second pass follows Plan 32. See [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:** Plan 33's landing candidate, and later Plan 32's.
- **Produces:** recorded outputs and run records with exact revisions, plus a list of real-hardware failures, each routed to its owning plan.

## Completion

- Every slot and h3_av has a real output recorded against the tested revisions.
- Local-managed voice has a real output, and Plan 33's strict xfail on it is removed or explained.
- The 95.8 GB is downloaded at most once, a second job reuses a warm pod, and the census ends empty.
- Every failure is recorded with its owning plan.
- **Limits:** one region and the GPU types available there; this is not a performance qualification.
