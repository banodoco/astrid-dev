# H3 speaker references

**Project:** H3 speaker references

**Goal:** A creator makes a character say a new line in their own voice by giving H3 a reference video or audio clip of them speaking, with the picture regenerated from a start image or kept under a mouth mask.

**Status:** `queued`

**Owner:** Unassigned

**Estimate:** 2 days (1 build, 1 proof and docs)

**Waiting on:** Owner greenlight of scope; one GPU spike (task SR-1) before build tasks start.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

**The creator's experience.** The H3 v2 request treats a reference as one composable piece: a `reference` of modality `image`, `video` or `audio`, tagged `<Picture n>` / `<Video n>` / `<Audio n>` in the prompt. Any H3 route built on the shared graph builder (source-free generation, masked edit, Character Swap) accepts it, up to the node's own limits. Two recipes become possible and documented:
- **Start image + speaker reference** (source-free): the corrected frame plus a 2–15 s clip of the speaker; H3 animates the image and speaks the line in that voice.
- **Kept picture + mouth mask + speaker reference** (masked edit): only the lower face and the audio inside the line's window are regenerated.

**Included:**
- one reference lowering for the builder;
- `ref_audios` support in the builder;
- audio regeneration (`action: generate`) in masked edits;
- one meaning per spelling for audio;
- a record of each reference's tag, trim and node slot;
- the recipes in the H3 and recast skills;
- the pack's list of node inputs it still doesn't expose.

**Deferred:**
- continuation built from the same builder ([astrid-dev#866](https://github.com/banodoco/astrid-dev/issues/866));
- fixed content respelled as timeline items, including an exact start frame via `MiniMaxH3AddGuide` ([astrid-dev#863](https://github.com/banodoco/astrid-dev/issues/863));
- output size ([Plan 65](../65-h3-dynamic-size/plan.md));
- multi-speaker voice-to-face binding beyond what SR-1 shows;
- collapsing v1 onto v2 ([astrid-dev#860](https://github.com/banodoco/astrid-dev/issues/860)).

## Existing work and decision

**Retain and build on:**
- the node `MiniMaxH3ReferenceToVideo` (ComfyUI `6bfaacc`), already on the worker: 9 images, 3 videos, 3 audio clips, each 2–15 s and 15 s total per modality;
- the model card's documented voice-timbre reference prompting;
- the shared builder `build_generation_workflow` (`astrid/packs/h3_av/shared/generation.py`);
- the normaliser's reference tags (`request_v2.py:357-390`);
- Character Swap's video-reference binding, which already goes through the builder with its soundtrack.

**Smallest sound approach:** a single lowering in front of the builder, used by every route, plus deletion of the hand-written per-route refusals. No new pack and no new route.

Evidence, alternatives and the design critique are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

1. **SR-1 GPU spike (gate):** through the plain VibeComfy workflow route, run one start image plus one Morpheus reference clip with `audio_vae` connected. Listen, transcribe, and measure time and VRAM. If the voice isn't his, stop, and the owner decides whether to continue.
2. **SR-2 and SR-3:** the lowering and the masked-edit audio generate. They change different functions, so they run in parallel, with a merge order.
3. **SR-4 records, SR-5 docs.**
4. **SR-6 live proof:** two jobs on shot 02c.

Budget: about $3 of RunPod for SR-1 and SR-6 together. Task details are in [tasks.md](tasks.md). Recording this plan authorizes no implementation.

## Interfaces and handoff

**Consumes:**
- the H3 v2 request contract at the integrating `release/<NN>/plan-64` head;
- the ComfyUI pin `6bfaacc` from the worker recipe (VibeComfy `custom_nodes.lock`);
- the effective-settings record from `p59/h3-overrides`, if merged; otherwise SR-4 adds the reference rows to the dry-run plan only.

**Produces:**
- the v2 request accepting typed video and audio references on builder routes;
- a refusal that names the limit for anything over the node's caps;
- a dry-run and result record of each reference's tag, range and slot;
- the recipes in `astrid/packs/h3_av/docs/SKILL.md` and `recast-scene/SKILL.md`.

**Limits:**
- voice-match quality is sample-dependent;
- audio strength is one value per window, so in the masked recipe the room tone inside the window is regenerated unless composition restores it outside the spoken interval.

## Completion

**Observable result:** on 02c, both recipes produce Morpheus saying exactly "tuning workflows by hand,". That's checked by `timelines transcripts show` (words and nothing else), by the owner recognising the voice, and by the lenses or kept picture being intact (`timelines visualize --compare-media`).

**Negative cases:**
- a 4th video reference, a 16 s reference, or a reference without measurable stream durations is refused before any machine is claimed;
- existing image-only requests compile byte-identically;
- Character Swap compiles identically.

**Limits of the proof:** one speaker, one shot, one GPU type (RTX 5090). Integration and release follow the release process.
