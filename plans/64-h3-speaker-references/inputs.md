# Inputs — H3 speaker references

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner asked for this capability in the Plan 59 session (18 Nov 2026): "a starting image for the video, and we feed a reference video, a video reference of just him speaking"; and "why would we block masked edits + video references?" They asked for a plan, not yet greenlit scope. Next: owner greenlight of this plan, including D1 and D2.

**Prior art:**
- **The node supports it.** ComfyUI `6bfaacc` `comfy_extras/nodes_minimax_h3.py` `MiniMaxH3ReferenceToVideo`:
  - inputs `ref_images` / `ref_videos` / `ref_video_audios` / `ref_audios` (lines 263–283);
  - each soundtrack is paired with its same-numbered video (313–318);
  - with `audio_vae` connected, reference audio is encoded as latents; without it, reference audio only conditions the text encoder.
- **The model is documented for it.** The MiniMax H3 model card lists reference-to-audio-video and audio-to-audio-video, and shows `<Audio n>` as a "voice timbre reference". Limits: 3 videos and 3 audio clips, each 2–15 s and 15 s total per modality; 9 images; 12 files.
- **Astrid already has most of the path:**
  - the shared builder `astrid/packs/h3_av/shared/generation.py:234` `build_generation_workflow` serves source-free generation, masked edit and Character Swap;
  - Character Swap already binds a typed video reference, with its soundtrack, through it (`compile.py` `_compile_character_swap_v2`);
  - the normaliser already assigns `<Video n>` / `<Audio n>` tags (`request_v2.py:357–390`).
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
- **(b) The plain VibeComfy workflow route only.** Kept as the SR-1 spike route, but rejected as the product path, because it skips the pack's checks, verification and composition.
- **(c) Wait for "build the invocation once" (#866).** Rejected as a prerequisite: this lowering is a step toward it, not a conflict.

**Challenge:** Design critique by a fresh high-judgment reviewer (18 Nov, read against `origin/release/14/plan-59`). Accepted:
- one lowering, not per-route tables;
- capacities in one table pinned against the node schema;
- delete the masked edit's two-slot limit;
- references condition the whole pass, so any modality on any edit (stop extending `EDIT_GUIDE_MODALITIES`);
- meaning by structure (a reference named by an audio edit's `guides` is the legacy fixed clip; everything else is conditioning; `range` is only a trim);
- audio generate in masked edits;
- source-free calls the builder directly;
- no "tag not mentioned" warning;
- no new preparation stage unless the 48 kHz check needs one.

Rejected: none. A plan-level critique of this document is recorded under References once done.

**Proof and limits:**
- **Acceptance:** the two 02c jobs in SR-6, plus SR-1's spike.
- **Failure cases:** over-limit references are refused before claiming; image-only digests are unchanged; Character Swap is unchanged.
- **Assumptions:** voice match is sample-dependent; room tone inside a masked audio window is regenerated.

**Review rounds:** Recommend 1 (a shared request contract and a user-visible flow). Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: the owner starts a run.

## Owner decisions

- **D1 — gate on the spike.** Options:
  - (a) build only if SR-1's voice is recognisably the speaker's;
  - (b) build regardless, since the model card documents it.
  
  Recommend (a): the build is cheap, but the whole point is the voice.
- **D2 — masked-edit audio scope.** Options:
  - (a) regenerate audio for the whole edit window;
  - (b) also restore the source audio outside the spoken interval during composition.
  
  Recommend (a) now, (b) only if SR-6 shows audible room-tone damage.

## Source identities

Pending — no code work yet. The base is `astrid-agent` `release/14/main` at dispatch, cut to `release/<NN>/plan-64` in `astrid-agent` only. Pins consumed: ComfyUI `6bfaacc`; the H3 motion pack `361624fb` (VibeComfy `custom_nodes.lock:31–39`).

## References

- **Owner requests:** Plan 59 session, 18 Nov 2026.
- **Issue:** [astrid-dev#890](https://github.com/banodoco/astrid-dev/issues/890).
