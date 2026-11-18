# Inputs — H3 dynamic output size

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — in the Plan 59 session (18 Nov 2026) the owner asked "should the output size not be a param we tweak?" and "do we have a plan to make size fully dynamic?", and asked for a plan. Next: owner greenlight, including D1 and D2.

**Prior art:**
- **The research:** [research/size.md](research/size.md) lists every place the working frame is fixed, with file:line (summarised in the plan).
- **The node allows it:** width/height 32–16384 in steps of 32 (VibeComfy schema cache `comfy_core@cpu-runtime.json`, `MiniMaxH3ReferenceToVideo`).
- **Composition is already dimension-aware** (`compose.py:632-675`). Static mask resolution happens in one function (`static_regions.resolve_static_region`), and `astrid media mask` already takes `--size`.
- **Negative finding:** no trained-resolution statement for H3 video, and no controlled quality results at small or large sizes. Hivemind `1572496981547421728` reports 2–3 MP workflows with upscaling, but uncontrolled.
- **Related tickets:** [astrid-dev#885](https://github.com/banodoco/astrid-dev/issues/885) (small size for voice-only takes), which this plan supersedes.

**Approach:** one request-level size, threaded through existing functions. Alternatives:
- **(a) A separate "voice-only" size flag.** Rejected: a second vocabulary for one concept.
- **(b) Fixed size presets.** Rejected for now: the node's own rules are simpler. Presets can be a docs table.
- **(c) Resize after generation.** Rejected: it costs the same GPU time and loses quality.

**Challenge:** Pending — the plan-level critique runs on the written plan (see References). Next: record what is accepted or rejected.

**Proof and limits:** the two DS-6 jobs; size-free requests unchanged byte for byte; quality not guaranteed at other sizes.

**Review rounds:** Recommend 1 (the request contract and mask handling are shared and user-visible). Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: the owner starts a run.

## Owner decisions

- **D1 — the size vocabulary.** Options:
  - (a) `output.size: [w, h]` in pixels, checked against the node's rules;
  - (b) a named preset plus an explicit override.
  
  Recommend (a).
- **D2 — mask coordinate space.** Options:
  - (a) masks are images resampled once to the working size, and boxes are given in a normalised 0–1 space;
  - (b) boxes stay in pixels of a declared reference size (today 1024×576) and are scaled.
  
  Recommend (b) for compatibility: existing requests and the docs use 1024×576 pixel boxes. Its scale is the mask's own stated size, so nothing changes for existing requests.

## Source identities

Pending — no code work yet. The base is `astrid-agent` `release/14/main` at dispatch, cut to `release/<NN>/plan-65` in `astrid-agent` only. Pins consumed: ComfyUI `6bfaacc`.

## References

- **Owner requests:** Plan 59 session, 18 Nov 2026.
- **Issue:** [astrid-dev#885](https://github.com/banodoco/astrid-dev/issues/885).
