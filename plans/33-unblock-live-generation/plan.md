# Unblock live generation on RunPod and locally

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary) · [Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting).

**Contributes to closure:** F-008 step 1: on RunPod, a warm machine reused, models on attached storage not re-downloaded, `--align check|trust`, and a missing model failing before submit and naming the machine. Milestone A on CPU: every default slot and h3_av produce results through the real RunPod path against a stand-in. The real-GPU half of Milestone A is [Plan 34](../34-real-gpu-proof/plan.md) (real-GPU proof), which follows this plan.

## Outcome and scope

Every default generation slot (image, edit, voice, music, sound effects) and h3_av runs through the **one existing path**, on RunPod and locally, so Plans 01, 02 and 06 can land proven end to end on CPU. The owner chose CPU only for this plan (8 Nov); the real-GPU proof is [Plan 34](../34-real-gpu-proof/plan.md) (real-GPU proof), which follows it. That path is: the host places the job, VibeComfy builds the ComfyUI prompt, and the prompt is posted to that place's ComfyUI. The outputs come back over `/view`.

This is the short-term fix. It adds no new architecture. It finishes the missing wire that broke voice and removes preconditions that block workflows for no product reason. The structural redesign (one requirements manifest, one alignment step, one binding) is [Plan 32](../32-generation-placement-targets/plan.md).

- **Included:**
  - a CPU test of the real pod path, so bugs show up without a paid pod;
  - the pod's verified model inventory reaching the readiness check (an interim wire that Plan 32 replaces);
  - one `--align check|trust` flag;
  - deleting the sound-effects RunPod refusals (Foley's source video already travels as an ordinary media input);
  - h3_av reaching the pod the same way as every other generation, with MiniMax H3 as the video default;
  - the engine's models kept on the storage volume, so the 95.8 GB downloads once rather than for every pod;
  - reusing a live pod for the next job (the checks that refuse it relaxed);
  - deleting the dead RunPod preparation binder (the rest of the legacy second RunPod route moves to Plan 32 T6b);
  - the landing.

  Music has not yet produced an output live; its CPU result is recorded here, not assumed.
- **Not included:**
  - per-request model subsets (the volume cache makes them less urgent);
  - a generic per-request model cache (this plan caches the one engine's models on the volume);
  - one align step;
  - one Placement object;
  - collapsing the submit and retrieve paths.

  All of these are in Plan 32.

## Why it broke (summary)

Full evidence is in [inputs.md](inputs.md#planning-evidence). In short:

- **Voice:** at the host boundary, placement shrinks to one URL. On RunPod, that URL is a bridge on the controller, so the readiness check looked for the voice model's files on the controller's disk. Image and music passed only because their models are listed by the pod's ComfyUI node menus. The fix is a missing wire, and VibeComfy already has the mechanism ("target custody").
- **Sound effects** is refused on RunPod by an explicit refusal with no product reason. Foley's source video is an ordinary media input, which already travels in the staged assets and is uploaded like images and audio; the host's `source_video` rejection covers a different input.
- **h3_av** builds VibeComfy workflows like everything else. On RunPod, though, it ships its whole command to a pod through a separate route, instead of placing each workflow like every other generation.
- **Every attempt paid for a fresh pod and a 95.8 GB download,** because a pod cannot be reused by the next job. The only test of the pod path was the paid live run, so bugs surfaced one per hour.
- **The deeper cause** is that RunPod is used as a remote ComfyUI. The controller does every check across a bridge, so every check that touches files needs the pod's state carried back. Plan 32 makes a pod a generic machine that runs the same local path. This plan keeps today's route at minimum size, so the landing is not blocked on that redesign.

## Owner decisions recorded (8 Nov 2026)

1. **No effects are deleted.** Of the 15 effects in the retired `local` pack, the two the App needs for every user (`end-spanning-layer` and `frame-overlay`) move to core `rendering`, as `video-editor` did. The other 13 move to a pack in the owner's personal collection, under a non-reserved id, because `local` is reserved and skipped by discovery. This amends [Plan 06 Decision 8](../06-packs/plan.md#decisions).
2. **Storage volume:** wipe it (authorized 8 Nov, 01:00Z) and use it as the engine's model cache (U6). The code to do this already exists off the main path (`scripts/pod_session.py`).
3. **Everything runs on our own compute**, locally or on RunPod; video defaults to MiniMax H3 via h3_av, not a cloud API. Licence questions are out of scope for this plan.
4. **poms_packs `main`:** go, from the tested candidate, at landing.
5. **Plan 31 → 32 renumbering** ([astrid-dev#90](https://github.com/banodoco/astrid-dev/pull/90)): merged.

Later the same day the owner chose CPU only, at most 2 review rounds, and [Plan 17](../17-vibecomfy-extensibility/plan.md) as the home of the pack extension protocol (M-78). She also refused image-only video without an entry and accepted the amended scope (M-79); see [inputs.md](inputs.md#owner-decisions).

## Sequence and readiness

1. U1: the CPU pod-path test comes first, and every later task adds its case to it.
2. U2 (the interim inventory wire and `--align`), then U3 (sound effects), then U4 (h3_av), which share the SDK files.
3. U6 (models on the volume), then U5 (delete the dead binder).
4. U7 (pod reuse), from the U6 head, rebased onto U5.
5. The review rounds, then U9: land, on the owner's go.

The live proof is deferred to [Plan 34](../34-real-gpu-proof/plan.md) (real-GPU proof), which follows this plan.

The work starts from the merge run's candidates (Agent -33 `5eac07e3f`, Runtime `b983b04`, VibeComfy `e65f4941`, lifecycle `f2948817`, poms `2379ab5`) and the WIP commit `e003778be`; see [inputs.md](inputs.md#source-identities). Every task runs on CPU. See [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:** the merge-run candidates above, and Plan 02's slot × target invariant test (`tests/core/generation/test_runpod_engine_selection.py`).
- **Produces:**
  - the CPU pod-path test, which Plan 32 T1 extends;
  - `--align check|trust`, which Plan 32 keeps;
  - the interim inventory wire, which Plan 32 T5 deletes.
- The landing of Plans 01, 02 and 06 records this plan's CPU evidence.
- [Plan 34](../34-real-gpu-proof/plan.md), which follows this plan, consumes the landed head for the real-GPU proof.

## Completion

All evidence is on CPU (owner, 8 Nov).
- **Pod path:** the CPU pod-path test runs every default slot and h3_av (the Matrix request) through the real RunPod host bind, against a stand-in ComfyUI with real node schemas. The models are absent on the controller and present in the stand-in's receipt. It is red on the base for voice and sfx, and green at the end. Local-managed voice and attached voice (with `--align trust`) are green too.
- **Volume and reuse:** with a saved volume, the install uses the volume model cache, and a second pod's install copies from it instead of downloading. Two sequential generates on one engine use one claim and one install, and no orphaned pod remains.
- **Negative cases:**
  - a model missing from the pod's receipt fails readiness, naming the place;
  - an entry no engine lock covers is refused before any pod is claimed;
  - `--align check` on an attached server without the files fails with a fix;
  - a tampered cache row fails its sha256.
- **Not proven by this plan:** real inference, real model downloads to the volume, RunPod capacity, and whether the cache accepts RunPod's network volume. These move to [Plan 34](../34-real-gpu-proof/plan.md) (real-GPU proof), which follows this plan.
- **Limits:** the first fill of the volume downloads the full 95.8 GB engine (about 36 minutes), and each fresh pod copies its rows from the volume. Per-request model sets and a pod that is a generic machine come in Plan 32. A session that switches between image (engine `comfyui`) and voice (`vibecomfy-h3`) pays a new pod per switch until Plan 32 T2b merges the engines, and reuse across two separate `astrid generate` processes is not proven on CPU. Local H3 video needs a source video or reference images, because no plain text-to-video H3 model is in the lock (the cloud `minimax-h3` entry is not used: everything runs on our own compute). The `_refs` H3 variant is not covered until Plan 32 T2. No new providers.
