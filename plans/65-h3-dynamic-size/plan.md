# H3 dynamic output size

**Project:** H3 dynamic output size

**Goal:** A creator chooses the H3 working size per request (small for voice-only takes, other aspect ratios, larger where it's worth paying for), and masks, previews, composition and checks follow it.

**Status:** `queued`

**Owner:** Unassigned

**Estimate:** 2.5 days (1.5 plumbing, 0.5 masks, 0.5 proof and docs)

**Waiting on:** Owner greenlight of scope; D1 (the size vocabulary) and D2 (the mask coordinate space).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

**The creator's experience.** An H3 v2 request may state its working size, for example `output.size: [256, 144]`. Without it, the default stays 1024×576, so existing requests are unchanged. The chosen size is carried through the whole pipeline:
- conform (fill or fit);
- source validation and the preparation record;
- the generation node (`width`/`height`);
- the preserved-tail mask;
- static mask resolution and its preview;
- composition and paste-back;
- Character Swap;
- `astrid media mask --preview-on` and the dry-run record.

Masks are stored independent of the working size and resolved once, at one boundary.

**Included:** the request field with the node's rules (32–16384, steps of 32), one carried size value, size-independent masks, the documented coordinate space, and the docs.

**Deferred:**
- quality guidance beyond the two proof sizes;
- automatic size choice;
- the reference image size (`ref_image_size`, see [Plan 64](../64-h3-speaker-references/plan.md)'s coverage list);
- the continuation's captured graph, if it can't take the size without a graph change. Then it keeps 1024×576 and refuses another size with a clear message.

## Existing work and decision

**Today 1024×576 is assumed in:**
- generation: `generation.py:367-376` and the tail mask at `:424-425`;
- conform: `conform.py:180-184` and `:225`;
- source preflight and preparation: `prepare.py:243-244, 267, 452, 477-478`;
- mask compilation: `compile.py:487, 499, 568, 570, 594`;
- static masks: they must equal the frame size (`static_regions.py:45-80`);
- docs: `docs/SKILL.md` (:218, 237, 309-311, 497, 515).

**Already dimension-aware:** composition (`compose.py:632-675`, `:895`), take reporting, and the generation node itself.

**Smallest sound approach:** one size value from the request, threaded through the existing functions in place of the constant, and masks resolved once in `static_regions.resolve_static_region`. No new stage. Evidence and alternatives are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

1. **DS-1:** the request field and one carried value.
2. **DS-2:** conform, preflight and preparation.
3. **DS-3:** generation and the compiler's full-frame and tail masks.
4. **DS-4:** size-independent masks and preview.
5. **DS-5:** docs.
6. **DS-6:** live proof.

DS-2, DS-3 and DS-4 depend on DS-1 and change different files, so they run in parallel. Budget: about $1.50 of RunPod for DS-6. It's independent of Plan 64, and either can land first. Task details are in [tasks.md](tasks.md). Recording this plan authorizes no implementation.

## Interfaces and handoff

**Consumes:**
- the H3 v2 request contract at the integrating `release/<NN>/plan-65` head;
- the `MiniMaxH3ReferenceToVideo` width/height rules from the node schema (ComfyUI `6bfaacc`).

**Produces:**
- `output.size` in the v2 request, with the default unchanged;
- masks valid at any working size;
- the size in the dry-run plan and result;
- `media mask --preview-on` at the request's size.

**Limits:** quality at other sizes isn't guaranteed. The proof covers two sizes.

## Completion

**Observable result:**
- a voice-only continuation at 256×144 produces the line; its transcript matches a 1024×576 run of the same request, and it takes less GPU time;
- a lens edit at a non-default size (for example 768×432) keeps everything outside the mask (`timelines visualize --compare-media`: MATCH outside).

**Negative cases:**
- a size off the 32-step grid, or below 32, is refused before claiming;
- existing requests without a size compile byte-identically;
- a mask drawn for another size is resolved, not refused;
- the continuation route refuses a non-default size if it can't take one.

**Limits of the proof:** one GPU type, two sizes.
