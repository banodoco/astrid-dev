# H3 dynamic output size

**Project:** H3 dynamic output size

**Goal:** A creator chooses the H3 working size per request (small for voice-only takes, other aspect ratios, larger where it's worth paying for), and masks, previews, composition and checks follow it.

**Status:** active

**Owner:** Session `session_011EzfW4BJ221kXBNRB4xQcG` (the Plan 59 session)

**Estimate:** 2 days (CPU only; the live test is separate and comes after)

**Waiting on:** Plan 64 SR-3 (the shared input record and limits table), which DS-1 builds on.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

A creator can ask for `output.size: [512, 288]` on image-guided generation, a masked edit or Character Swap. Continuation gets size from [Plan 70](../70-h3-continuation-bridges-inserts/plan.md) CC-7a (D1). Any width and height from 32 to 16384 in multiples of 32 is accepted. With no size given, the request is 1024×576, identical in bytes and digest to an explicit 1024×576 request. Source conform, generation, mask rasterization, composition, dry run and the completed-job record all use the same effective size.

Rectangle masks are authored on a canvas: by default 1024×576, or the canvas the mask states. They scale to the chosen size. A still-image mask scales from its own pixel size.

**Not in this plan. Do not build these:**
- a GPU or live run of any kind (D2). The owner tests afterwards;
- scaling moving (video) masks. They keep today's rule: lossless, the prepared source's size, the same clock;
- any change to how moving masks reach composition;
- a new mask-to-composition mapping layer, member digests or relocatable build-state records;
- size presets, automatic size selection or quality guidance across the range;
- tuning `ref_image_size`;
- continuation sizing, or any change to the captured continuation workflows. [Plan 70](../70-h3-continuation-bridges-inserts/plan.md) replaces them (D1).

## Existing work and decision

Reuse the v2 normalizer, source conform, the generation builder, the static-region resolver and the existing managed artifact handoff. The one structural change: composition today finds or redraws static masks on its own and resizes them a second time. Instead, the masked compiler rasterizes each static mask once at the target size, and composition reads that file. The planning evidence is in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

**Order with [Plan 64](../64-h3-speaker-references/plan.md):** Plan 64's SR-1 to SR-3 land first. This plan fills in the size in their `GenerationInputs.canvas` and reads width and height from their limits table. It creates neither. [Plan 66](../66-h3-composable-core/plan.md) follows it.

DS-1 sets the size contract. DS-2 (conform) and DS-3 (static masks) then run in parallel. DS-4 binds size at every generation entry point except continuation. DS-5 documents it. Review comes last. [Task cards](tasks.md)

## Interfaces and handoff

The request's size goes through `GenerationInputs.canvas`, which every stage reads; nothing else holds a size. Compilation passes each static mask's rasterized file to composition. The dry-run plan and the retained job result show the effective size. The standalone `media mask` preview keeps its own explicit `--size`.

## Completion

CPU tests prove each of these:

- A 512×288 and a 768×448 request compile on image-guided generation, masked edit and Character Swap, with the requested size in every width and height binding. A non-default size on continuation is refused from the limits table as a lowering limit, Plan 70 CC-7a removes.
- 256×144, 768×432, out-of-range, fractional, string and boolean sizes are refused before claim.
- A request with no size and one with explicit 1024×576 give identical bytes and digests, and compile the same graph as before this plan.
- At 768×448, decoded output keeps the prepared source pixels outside a scaled rectangle mask, on a non-16:9 source with an off-centre landmark.
- The dry run and the completed-job record show the decoded size.

Review then closes the plan. Speech quality and timing at small sizes are judged in the owner's live test afterwards. That test is not part of this plan.
