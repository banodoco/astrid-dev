# Real-GPU proof of generation

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary) · [Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting).

**Contributes to closure:** F-008 step 1b: every default slot and h3_av produce real outputs on RunPod, with models downloaded once to the storage volume and a warm pod reused. Milestone A, proven on hardware.

## Owner direction (9 Nov 2026): a repeatable protocol, not a one-off

This plan **builds a skill, `skills/astrid-dev-gpu-validate/SKILL.md` ("full GPU validation"), and does its first run.** After that, real-GPU proof is the skill, run again, not a new project.
- **The protocol:**
  - a fixed matrix of every default slot and h3_av × RunPod, local-managed (where a GPU exists) and attached;
  - first a VibeComfy-only smoke on the same pod, so model or node failures are told apart from routing failures;
  - a pod census before and after every run, a hard budget per run, and every pod released;
  - one dated evidence record per run in astrid-dev, `validation/gpu/<date>-<short-sha>.md` (the Agent revision under test), with pass or fail per cell, spend and pod ids;
  - each failure goes to astrid-dev-bugfix: reproduced on CPU where possible, fixed, re-run live.
- **When it runs:**
  - when the owner asks ("run full GPU validation");
  - as a required gate in `astrid-dev-release` for any release that touches generation, for which this plan edits the release skill.
  No schedule for now.
- **Budget:** $20 per run of the skill (owner, 9 Nov). The first run, this plan, has $24 (owner, 9 Nov; previously $25), with "fix every issue you find".
- **The first run happens after Plan 32 completes,** on its integrated revision.

## Outcome and scope

The CPU-proven generation path from [Plan 32](../32-generation-placement-targets/plan.md) produces real outputs on real GPUs. **Owner, 8 Nov:** the first pass, on Plan 33's route, is dropped, because Plan 32 replaces how a RunPod job runs. This plan now runs once, after Plan 32. The proof is image, edit, voice, music, sound effects, and h3_av on the Matrix clip (80.886–83.305 s), each sent to the owner. Plans 33 and 32 are CPU only, so this plan proves what CPU cannot: real inference, real model downloads, real custom-node installs, and RunPod capacity.

- **Included:**
  1. **VibeComfy smoke on one pod.** Run each slot's workflow directly with VibeComfy's own commands, with no Astrid routing. This separates "this model or node fails on a GPU" from "our routing is wrong", and fills the storage volume once.
  2. **The Astrid route.** Run every slot on Plan 32's one path on RunPod, using the volume cache and warm reuse.
  3. **A pod census** before and after every run.
  4. **Local-managed voice on a real GPU.** Run voice through Astrid's managed local install, with the real weights present. Plan 33's CPU harness can't run this case, because VibeComfy verifies each model's sha256 (the `gpu`-marked `test_runpod_slot_path_cpu.py::test_local_managed_voice`). Run it where a local GPU exists; otherwise run it on the pod as a local placement.
  5. **Locally too,** where hardware exists: the same matrix on Plan 32's one path.
- **Fixes are included** (owner, 8 Nov: "fix every issue you find"). Each real-hardware failure is reproduced on CPU where possible, fixed as a repair task on Plan 32's integration line (route X or S), then re-run live. The run stops only when every slot passes or the budget is spent.
- **Budget:** $24 of RunPod spend for the whole plan (owner, 9 Nov; was $25 on 8 Nov). A pod census runs before and after every run, and spend is recorded per run.

## Existing work and decision

Built from the live attempts of 7–8 Nov 2026 and the path review on the merge-run desk (`banodoco/astrid-overnight-2026-11-05`, `merge-run/path-review/`). The owner set the order on 8 Nov: Plan 33 on CPU, then this plan, then Plan 32. Later the same day the owner started Plan 32 alongside Plan 33, so this plan's first pass now runs in parallel with Plan 32, once Plan 33 lands. See [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Starts as soon as Plan 32's CPU tasks and review pass, with the $24 budget approved (owner, 9 Nov). Check the account balance first. See [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:** Plan 32's landing candidate.
- **Produces:** recorded outputs and run records with exact revisions, plus a list of real-hardware failures, each routed to its owning plan.

## Completion

- Every slot and h3_av has a real output recorded against the tested revisions.
- Local-managed voice has a real output, and Plan 33's `gpu`-marked case passes on it.
- The 95.8 GB is downloaded at most once, a second job reuses a warm pod, and the census ends empty.
- Every failure is recorded with its owning plan.
- **Limits:** one region and the GPU types available there; this is not a performance qualification.
