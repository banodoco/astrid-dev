# Unblock live generation on RunPod and locally

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

Every default generation slot (image, edit, voice, music, sound effects) and h3_av runs live through the **one existing path**, on RunPod and locally, so Plans 01, 02 and 06 can land proven end to end. That path is: the host places the job, VibeComfy builds the ComfyUI prompt, and the prompt is posted to that place's ComfyUI. The outputs come back over `/view`.

This is the short-term fix. It adds no new architecture. It finishes the missing wire that broke voice and removes preconditions that block workflows for no product reason. The structural redesign (one requirements manifest, one alignment step, one binding) is [Plan 32](../32-generation-placement-targets/plan.md).

- **Included:**
  - a CPU test of the real pod path, so bugs show up without a paid pod;
  - the pod's verified model inventory reaching the readiness check;
  - an explicit "trust what's there" choice for places Astrid cannot inventory;
  - deleting the sound-effects RunPod refusal and letting a source video travel like any other media input;
  - h3_av reaching the pod the same way as every other generation;
  - reusing a warm pod within its lease;
  - deleting the legacy second RunPod route;
  - the live proof and landing.
- **Not included:**
  - per-request model subsets;
  - models on the storage volume;
  - one align step;
  - one Placement object;
  - collapsing the submit and retrieve paths.

  All of these are in Plan 32.

## Why it broke (summary)

Full evidence is in [inputs.md](inputs.md#planning-evidence). In short:

- **Voice:** at the host boundary, placement shrinks to one URL. On RunPod, that URL is a bridge on the controller, so the readiness check looked for the voice model's files on the controller's disk. Image and music passed only because their models are listed by the pod's ComfyUI node menus. The fix is a missing wire, and VibeComfy already has the mechanism ("target custody").
- **Sound effects** is refused on RunPod for a structural reason, not a product one: Foley needs a source video, and the host refuses to send a `source_video` to a URL-attached ComfyUI. The media upload already exists for images, audio and video inputs.
- **h3_av** builds VibeComfy workflows like everything else. On RunPod, though, it ships its whole command to a pod through a separate route, instead of placing each workflow like every other generation.
- **Every attempt paid for a fresh pod and a 95.8 GB download,** because a pod cannot be reused by the next job. The only test of the pod path was the paid live run, so bugs surfaced one per hour.

## Owner decisions recorded (8 Nov 2026)

1. **No effects are deleted.** The 15 effects of the retired `local` pack stay. They live in the owner's personal collection as an installed pack, and the App reads `end-spanning-layer` and `frame-overlay` from it like any other installed pack. This amends [Plan 06 Decision 8](../06-packs/plan.md#decisions).
2. **Storage volume:** wipe it for the live proof (authorized 8 Nov, 01:00Z) and prove h3_av on a fresh pod using it.
3. **poms_packs `main`:** go, from the tested candidate, at landing.
4. **Plan 31 → 32 renumbering** ([astrid-dev#90](https://github.com/banodoco/astrid-dev/pull/90)): merged.

## Sequence and readiness

1. U1: the CPU pod-path test comes first, and every later task adds its case to it.
2. U2: the inventory wire, plus the trust choice.
3. In parallel after U1:
   - U3: sound effects;
   - U5: warm reuse;
   - U6: delete the legacy route.
4. U4: h3_av, after U5 if one h3 job issues more than one workflow.
5. U7: live proof on the landing tuple.
6. U8: land.

The work starts from the merge run's candidates (Agent -33 `5eac07e3f`, Runtime `b983b04`, VibeComfy `e65f4941`, lifecycle `f2948817`, poms `2379ab5`) and the WIP commit `e003778be`; see [inputs.md](inputs.md#source-identities). The live proof needs the owner's go and the remaining RunPod budget. See [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:** the merge-run candidates above, and Plan 02's slot × target invariant test (`tests/core/generation/test_runpod_engine_selection.py`).
- **Produces:**
  - the host-provided placement inventory (receipt rows) and the trust choice. Plan 32 folds both into its PlacementBinding.
  - the CPU pod-path test, which Plan 32 T1 extends.
  - warm reuse within a lease, which Plan 32 generalizes.
- The landing of Plans 01, 02 and 06 records this plan's live evidence.

## Completion

- **CPU:** the pod-path test runs every default slot and h3_av through the real host bind, against a stand-in ComfyUI. The models are absent on the controller and present in the stand-in's inventory. It is red before U2 and green after.
- **Live, RunPod:** image, edit, voice, music, sound effects, and h3_av on the Matrix clip (80.886–83.305 s) each produce an output. Each slot's engine is installed once and reused warm, every pod is released, and the pod census is empty at the end.
- **Live, local:** the same slots run where local hardware exists; otherwise this is recorded as not run.
- **Negative cases:**
  - a model missing from the pod's receipt fails readiness, naming the place;
  - `trust` is refused on RunPod (the receipt is the inventory there);
  - a warm pod with a different engine is not reused.
- **Limits:** the full 95.8 GB engine download happens on the first pod for each engine; Plan 32 fixes it. No new providers.
