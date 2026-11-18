# Inputs — H3 speaker references

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner asked for this capability in the Plan 59 session (18 Nov 2026): "a starting image for the video, and we feed a reference video, a video reference of just him speaking"; and "why would we block masked edits + video references?" They asked for a plan, not yet greenlit scope. D1 decided (build voice references regardless). Next: owner greenlight of this plan.

**Prior art:**
- **The node supports it.** ComfyUI `6bfaacc` `comfy_extras/nodes_minimax_h3.py` `MiniMaxH3ReferenceToVideo`:
  - inputs `ref_images` / `ref_videos` / `ref_video_audios` / `ref_audios` (lines 263–283);
  - each soundtrack is paired with its same-numbered video (313–318);
  - with `audio_vae` connected, reference audio is encoded as latents; without it, reference audio only conditions the text encoder.
- **The model is documented for it.** The MiniMax H3 model card lists reference-to-audio-video and audio-to-audio-video, and shows `<Audio n>` as a "voice timbre reference". Limits: 3 videos and 3 audio clips, each 2–15 s and 15 s total per modality; 9 images; 12 files.
- **Astrid already has most of the path:**
  - the shared builder `astrid/packs/h3_av/shared/generation.py:234` `build_generation_workflow` serves source-free generation, masked edit and Character Swap;
  - Character Swap already binds a typed video reference, with its soundtrack, through it (`compile.py` `_compile_character_swap_v2`);
  - the normalizer currently numbers declared occurrences by modality (`request_v2.py:375–390`). That numbering misses audio inserted by a video soundtrack.
- **Today's refusals are hand-written:**
  - source-free "accepts image references only" (`compile.py` ~1065) and lowers into a v1 request with no modality or range (~1075);
  - the masked edit has a hand-written "two image-reference slots" limit (~612) copied from the continuation graph, and `audio_strength=0` hard-coded (`generation.py` ~440);
  - masked-edit audio regeneration without a replacement clip is refused (`compile.py:545`).
- **The worker matches the schema:** the worker recipe and the cached schema both pin ComfyUI `6bfaacc`.
- **Negative finding:** no evidence on lip-sync quality when audio is generated and the picture kept, or on VRAM and time for video references on an RTX 5090.
- **Research notes:** [voice](research/voice.md), [masked](research/masked.md), [misc](research/misc.md); the earlier spec lives on the Plan 59 branch (`release/14/plan-59`: `plans/59-into-the-minkhole-proof-point/spec-h3-video-audio-references.md`).

**Approach:** one reference lowering in front of the existing builder; routes stay derived facts.

Alternatives considered:
- **(a) Per-route special cases.** Rejected: a second vocabulary per route.
- **(b) The plain VibeComfy workflow route only.** Rejected as the product path, because it skips the pack's checks, verification and composition.
- **(c) Wait for "build the invocation once" ([#866](https://github.com/banodoco/astrid-dev/issues/866)).** Rejected as a prerequisite: this lowering is a step toward it, not a conflict.

**Challenge:** The independent planning critique of 18 November 2026 inspected the Agent snapshot below, the pinned node and both plan packs. Accepted all six Plan 64 findings and the shared integration, evidence and dispatch corrections. The earlier design review established structural fixed audio, one lowering and retention of the existing pack. The independent review identified where that lowering lost information in both canonical conversions, how paired soundtracks shift prompt tags, and why latent strength alone cannot preserve samples. SR-1 and SR-2 own occurrence identity and admission, SR-5 owns temporal composition, and SR-6 proves settled readback. The cards name the conflicting fixture expectations, sequence shared interfaces and leave voice and frame judgments to the owner's live test. The recommendations on scope, scheduling and proof are accepted. Retain the image prerequisite on source-free generation and the existing adapter and continuation contracts. The two requested recipes need no wider admission. Fable’s 18 November composability review traced the source-free bridge, masked canonical conversion and adapter compiler on the pinned revision. Accepted one frozen builder input, normalization-time audio classification, effective-row prompt validation and the shared limits table (now SR-3 and SR-2). The frame-zero timeline placement in request_v2.py supports the start-image rule below. On 18 November the plan was tightened for a less experienced implementer: GPU work removed (D2), SR-2 split into SR-1 to SR-3, a fixed `GenerationInputs` field list, defined terms, explicit non-goals, one plan order, and function names instead of line numbers.

**Proof and limits:**
- **Acceptance:** the CPU proofs in [plan.md](plan.md#completion). The owner's live test comes afterwards and is not part of this plan (D2).
- **Failure cases:** over-limit references are refused before claiming; image-only and Character Swap graphs are unchanged apart from listed differences.
- **Assumptions:** voice match is sample-dependent. Room tone inside the spoken window is regenerated (model behaviour, see Owner decisions).

**Review rounds:** Recommend 1 (a shared request contract and a user-visible flow). Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: the owner starts a run.

## Owner decisions

- **D1 — build voice references regardless (decided 18 Nov 2026, owner in the Plan 59 session: "we should build in any case voice references").** No proof run gates the build.
- **D3 — clean break in request identity (decided 18 Nov 2026, owner; recorded as [Plan 66 D4](../66-h3-composable-core/inputs.md#owner-decisions)).** SR-1 makes the break; no task preserves old digests.
- **D2 — CPU only (decided 18 Nov 2026, owner in the Plan 59 session: "we're not going to do a GPU test. This is just CPU… We'll do a test afterwards").** No task in this plan claims a machine or spends money. Voice likeness, lip sync and frame-1 continuity are judged in the owner's live test after the plan completes.

**Model behaviour, recorded here so nobody mistakes it for a decision:**
- H3 regenerates audio per window at one strength, so room tone inside the spoken window is regenerated with the voice. Sound outside the window is kept, and SR-3 proves it. Copying the original background back under the new words is a possible later improvement, not in scope.
- **Exact start image needs no new node** ([research/first-frame.md](research/first-frame.md)). A timeline image at frame 0 is lowered to the frozen-frame mechanism the masked edit already uses: regeneration starts at frame 1, and composition writes the exact frame-0 pixels. `MiniMaxH3AddGuide` is different: soft, time-positioned conditioning that leaves the latent and noise mask untouched and gives no pixel guarantee, so it's a later, separate piece. Proof: a CPU compile-and-compose check shows frame 0 is pixel-exact (SR-4). How naturally frame 1 continues is judged in the owner's live test afterwards.

## Source identities

Planning snapshot: `astrid-agent` `origin/release/14/plan-59` at `ec758a9b86a43416ace0650eb8109cb5967575dc`. The inspected worker pins ComfyUI `6bfaacc` and H3 motion pack `361624fb`. At dispatch record the actual release number, `release/<NN>/main` SHA, retained donor and dependency SHAs, and the cut `release/<NN>/plan-64` head in Agent. The planning donor does not establish the release base.

## References

- **Owner requests:** Plan 59 session, 18 Nov 2026.
- **Issue:** [astrid-dev#890](https://github.com/banodoco/astrid-dev/issues/890).
