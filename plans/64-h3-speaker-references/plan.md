# H3 speaker references

**Project:** H3 speaker references

**Goal:** A creator makes a character say a new line in their own voice by giving H3 a reference video or audio clip of them speaking, with the picture regenerated from a start image or kept under a mouth mask.

**Status:** `queued`

**Owner:** Unassigned

**Estimate:** 3 days (2 for the shared builder, normalization and compatibility work, 1 for proof and docs)

**Waiting on:** Owner greenlight of scope.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

A creator supplies dialogue in the existing prompt and an identified speaker clip. Source-free generation animates a visually guided first frame from a still image. A masked edit keeps the source picture outside the mouth mask and source audio outside the authorized audio interval. Inside that interval H3 generates the new line. Room tone inside that interval is regenerated, and the first frame is guided, not pinned. Both are model behaviour, recorded in [inputs.md](inputs.md#owner-decisions).

Both routes accept image, video and standalone audio conditioning within the preparation limits in SR-2. Source-free still requires an image. Character Swap reuses the lowering within its one-image, one-video adapter contract. Captured continuation retains its two image slots. Continuation moves onto the builder under [#866](https://github.com/banodoco/astrid-dev/issues/866), including small-size continuation for [#885](https://github.com/banodoco/astrid-dev/issues/885). Deferred work also includes the product AddGuide lowering after the D3 check, fixed audio as a timeline audio item, dialogue lines as a v2 piece bound to speaker rows, and removing model_tags from the digest through an identity migration. A second model is deferred. Only the shared limits table is in scope for that extension. Plan 65 defers moving-mask scaling.

## Existing work and decision

The shared generation builder already binds a video with its soundtrack for Character Swap. Extend that builder and the existing canonical spec to preserve typed reference occurrences through the public request, preparation and compilation. Keep the existing compositor as the owner of edit intervals. The independent critique, source revision and outstanding owner decisions are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

After scope and spend approval, SR-1 compares the speaker clip to a matched no-reference baseline. The owner judges recognisability. SR-2 establishes the request, spec, pass and builder contracts. SR-3 and SR-4 then proceed in parallel. The executable recipes precede editorial work in SR-5. SR-6 exercises both recipes on shot 02c. Both SR-5 and SR-6 feed final review. Budget and dispatch details are in [tasks.md](tasks.md).

## Interfaces and handoff

SR-2 supplies one ordered set of effective reference inputs to the shared builder, compilation record, dry run and result receipt. Each row identifies the occurrence, requested trim, effective input and prompt tag. Fixed replacement audio retains its own edit binding.

Coordinate with [Plan 65](../65-h3-dynamic-size/plan.md) on normalization, the source-free branch, masked and adapter calls, the builder and both skills. SR-2 owns removal of the v2→v1 translation. Prefer SR-2 first, then rebase DS-3 onto its builder interface. If size lands first, retain its public source-free size proof through SR-2. On the integrated head compile a mixed-reference masked request at 768×448 and compare the default image-only behavior with the baseline on CPU. Reconcile the exposed width/height inventory in SR-5 and DS-5. Each plan has its own live proof.

## Completion

For both 02c recipes the transcript contains exactly “tuning workflows by hand” and the owner recognises Morpheus against the fixed reference. Inspect the corrected lenses in the guided shot and the mouth motion inside the mask in the kept shot. Compare decoded picture outside the mask and source audio on both sides of a partial edit to the prepared source. SR-4 must show the same effective rows in the dry run and the settled result. Out-of-limit and unmeasurable conditioning inputs fail before claim. Existing image-only bundles, masked digests, fixed audio and Character Swap bindings pass their compatibility fixtures. SR-6 and the integrated review complete the plan. This proves one speaker, shot and GPU type. Release is a separate decision.
