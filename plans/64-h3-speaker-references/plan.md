# H3 speaker references

**Project:** H3 speaker references

**Goal:** A creator makes a character say a new line in their own voice by giving H3 a reference video or audio clip of them speaking, with the picture regenerated from a start image or kept under a mouth mask.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 2.5 days (CPU only; the live test is separate and comes after)

**Waiting on:** Owner greenlight of scope.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

A creator writes the new line in the prompt and supplies an identified speaker clip: a video with its soundtrack, or a standalone audio clip. Two routes use it:

- **Source-free:** H3 animates a still image. The still is either a reference that guides the picture, or a `role: timeline` image at frame 0, which becomes the exact first frame.
- **Masked edit:** the source picture is kept outside the mouth mask. Source audio is kept outside the edit's time window. H3 generates the new line inside it.

Both routes accept image, video and standalone audio references, within the limits table in SR-2. Source-free generation still requires an image. Character Swap keeps its contract: one image and one video. Captured continuation keeps its two image slots.

**Not in this plan. Do not build these:**
- a GPU or live run of any kind (D2). The owner tests afterwards;
- several speakers bound to their own voices;
- copying the original room tone back under the new line;
- `MiniMaxH3AddGuide`, timeline images at any frame other than 0, or any new Comfy node;
- fixed audio as a timeline audio item, or dialogue lines as their own request piece;
- removing `model_tags` from the request digest;
- moving continuation onto the shared builder ([#866](https://github.com/banodoco/astrid-dev/issues/866));
- a second model. Only the shared limits table is designed to extend to one.

## Existing work and decision

The shared generation builder (`build_generation_workflow`) already binds a video with its soundtrack for Character Swap. This plan adds one lowering in front of it. Every route builds the same `GenerationInputs` record, and the builder takes only that record. The existing compositor keeps ownership of edit intervals. The planning critique, the source snapshot and the owner decisions are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

SR-1 carries typed references through the request and spec. SR-2 adds the limits table and admission. SR-3 lowers everything once into the builder. SR-4 (exact start image), SR-5 (masked audio) and SR-6 (dry-run and result rows) then run in parallel. SR-7 documents the recipes once SR-3 to SR-5 work. Review comes last. Details are in [tasks.md](tasks.md).

## Interfaces and handoff

SR-3 supplies one ordered list of effective reference rows to the builder, the compilation record, the dry run and the result receipt. Each row names the occurrence, its requested trim, the effective input and its prompt tag. Fixed replacement audio keeps its own edit binding and gets no row.

**Order with [Plan 65](../65-h3-dynamic-size/plan.md):** this plan's SR-1 to SR-3 land first. Plan 65 builds on the `GenerationInputs` record and limits table they create, and adds the size field to them. Plan 65 does not create either.

## Completion

CPU tests prove each of these:

- A mixed image, video and standalone-audio request compiles on both source-free and masked routes. Each reference reaches the right node input with the right prompt tag.
- Over-limit and unmeasurable references are refused before a machine is claimed, with the limit named in the message.
- In a masked edit with a partial time window, decoded audio before and after the window matches the source sample for sample. Decoded picture outside the mouth mask matches the source pixel for pixel.
- With a frame-0 timeline image, decoded frame 0 equals the prepared still pixel for pixel.
- The dry run and the settled result show the same reference rows.
- Existing image-only bundles, masked digests, fixed-audio splices and Character Swap bindings match their current fixtures.

Review then closes the plan. Voice likeness and lip sync are judged in the owner's live test afterwards. That test is not part of this plan.
