# H3 continuation, bridges and inserts

**Project:** H3 continuation, bridges and inserts

**Goal:** An agent continues a clip, bridges two clips or inserts a clip mid-shot just by placing them on the canvas, at any size and with any references, and the hand-captured continuation workflows are gone.

**Status:** queued

**Owner:** Unassigned

**Target milestone:** 0.2

**Estimate:** 6 days (CPU only; the live check comes after)

**Waiting on:** Owner greenlight of scope, and Plans 66 and 68.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

On the [Plan 66](../66-h3-composable-core/plan.md) core, a clip shorter than the canvas means "generate the rest". Three placements, one request shape:
- **continuation:** a clip at frame 0, generated time after it;
- **bridge:** a clip, a generated gap, a clip;
- **insert:** a clip inside generated time.

They lower through the pinned motion-context nodes, chosen by the one arrangement function Plan 66 reserves. This plan fills the dry run's delivered-to-sampled frame map, maps guides inside a continuation, deletes the captured continuation workflows and the `continuation` flag (Plan 66 D3), ships recipes and one skill section, does the final trim pass over the skill, and holds the integrated review of Plans 66, 68 and 70.

**Not in this plan. Do not build these:**
- a GPU or live run (D1);
- more than one continuation block per job, or chain orchestration;
- a region edit inside a continuation's kept prefix (refused, suggesting two jobs);
- the `speech-continue` recipe ([Plan 67](../67-h3-community-steering/plan.md), after this plan).

## Existing work and decision

The cards CC-7a to CC-7d, their lattice summary and the assembly additions were written as part of Plan 66 and moved here unchanged when it was split. Their evidence (the captured graph's active path, the motion-context nodes, the bridge and prefix assembly contracts) and reviews are in [Plan 66's inputs](../66-h3-composable-core/inputs.md#planning-evidence); this plan's own record is in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Plans 66 and 68 land first. CC-7a's first step checks whether one full-canvas preparation (from Plan 68 CC-8) can serve prefix, insert and bridge; that decides whether CC-7b and CC-7c need lowerings of their own. Then CC-7b and CC-7c in parallel, CC-7d (deleting the captured workflows), CC-12 (recipes, the skill section and the final trim), and the integrated review. [Task cards](tasks.md)

## Interfaces and handoff

**Consumes:** Plan 66's job, table, dry-run view, composition and arrangement function; Plan 68's full-canvas builder and guide lowering.

**Produces:** prefix, bridge and insert preparation in one function; the filled delivered-to-sampled frame map; removal of the captured workflows and the `continuation` flag; their recipes and skill lines. Plan 67's `speech-continue` recipe builds on it.

## Completion

CPU tests prove each of these:
- The ported continuation matches the captured active path, apart from the listed differences, and delivers the prefix exactly across the seam.
- It compiles at 512×288 with three images and a speaker clip.
- Clip A, a 63-frame generated gap and clip B compile to a bridge, and unequal owners (120 and 90 frames, n = 39) give matching audio and video lengths. A clip placed at frame 51 compiles to an insert, and an insert at frame 34 is refused.
- A guide at delivered frame 80 in a 120 + 24 continuation is refused, cropped or kept as stated.
- With the Character Swap adapter on, continuation and bridge graphs carry both LoRAs in the model chain.
- The captured workflows and the `continuation` flag are gone, and every recipe fills, dry-runs and compiles.

The integrated review then closes Plans 66, 68 and 70 together. The owner's live check judges seams against saved takes.
