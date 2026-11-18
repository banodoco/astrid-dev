# Inputs — H3 speaker references

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner asked for this capability in the Plan 59 session (18 Nov 2026): "a starting image for the video, and we feed a reference video, a video reference of just him speaking"; and "why would we block masked edits + video references?" They asked for a plan, not yet greenlit scope. Next: owner greenlight of this plan, including D1–D3.

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
- **(b) The plain VibeComfy workflow route only.** Kept as the SR-1 spike route, but rejected as the product path, because it skips the pack's checks, verification and composition.
- **(c) Wait for "build the invocation once" (#866).** Rejected as a prerequisite: this lowering is a step toward it, not a conflict.

**Challenge:** The independent planning critique of 18 November 2026 inspected the Agent snapshot below, the pinned node and both plan packs. Accepted all six Plan 64 findings and the shared integration, evidence and dispatch corrections. The earlier design review established structural fixed audio, one lowering and retention of the existing pack. The independent review identified where that lowering lost information in both canonical conversions, how paired soundtracks shift prompt tags, and why latent strength alone cannot preserve samples. SR-2 owns occurrence identity and admission, SR-3 owns temporal composition, and SR-4 must prove settled readback. The revised cards name the conflicting fixture expectations, budget the control, sequence shared interfaces and reserve voice and frame judgments for the owner. The recommendations on scope, scheduling and proof are accepted. Retain the image prerequisite on source-free generation and the existing adapter and continuation contracts. The two requested recipes need no wider admission.

**Proof and limits:**
- **Acceptance:** the two 02c jobs in SR-6, plus SR-1's spike.
- **Failure cases:** over-limit references are refused before claiming; image-only digests are unchanged; Character Swap is unchanged.
- **Assumptions:** voice match is sample-dependent. D2 records the pending choice for room tone inside the window.

**Review rounds:** Recommend 1 (a shared request contract and a user-visible flow). Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: the owner starts a run.

## Owner decisions

- **D1 — gate on the spike.** Options:
  - (a) build only if SR-1's voice is recognisably the speaker's;
  - (b) build regardless, since the model card documents it.
  
  Recommend (a): the build is cheap, but the whole point is the voice.
- **D2 — room tone inside the authorized audio window.** Recommend accepting generated room tone under the new line. If the owner requires the original ambience mixed under speech inside that window, scope the mix and listening oracle before dispatch. Source sound on both sides is always protected.
- **D3 — first frame.** Recommend an image-guided first frame. If the owner needs an exact frame, SR-1 must check a frame-zero MiniMaxH3AddGuide with Ref2VA and compare the decoded first frame against the supplied image before promising the recipe. Reprice that check before authorizing jobs.

## Source identities

Planning snapshot: `astrid-agent` `origin/release/14/plan-59` at `ec758a9b86a43416ace0650eb8109cb5967575dc`. The inspected worker pins ComfyUI `6bfaacc` and H3 motion pack `361624fb`. At dispatch record the actual release number, `release/<NN>/main` SHA, retained donor and dependency SHAs, and the cut `release/<NN>/plan-64` head in Agent. The planning donor does not establish the release base.

## References

- **Owner requests:** Plan 59 session, 18 Nov 2026.
- **Issue:** [astrid-dev#890](https://github.com/banodoco/astrid-dev/issues/890).
