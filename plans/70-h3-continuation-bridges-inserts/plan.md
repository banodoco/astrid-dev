# H3 continuation, bridges and inserts

**Project:** H3 continuation, bridges and inserts

**Goal:** An agent continues a clip, bridges two clips or inserts a clip mid-shot just by placing them on the canvas, at any size and with any references, and the hand-captured continuation workflows are gone.

**Status:** active

**Owner:** h3-orchestrator, session [`session_011EzfW4exucHx4FeFWbexak`](https://claude.ai/code/session_011EzfW4exucHx4FeFWbexak)

**Target milestone:** 0.2

**Estimate:** 4–8 days (CPU only; re-estimated 28 Nov 2026 as units of at most 3 days; the live check comes after)

**Waiting on:** Plan 66's contract review (RS1) and composition by occurrence (CC-10); Plan 68 CC-4 for guides inside a continuation.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

On the [Plan 66](../66-h3-composable-core/plan.md) core, a clip shorter than the canvas means "generate the rest". Three placements, one request shape:
- **continuation:** a clip at frame 0, generated time after it;
- **bridge:** a clip, a generated gap, a clip;
- **insert:** a clip inside generated time.

They lower through the pinned motion-context nodes, chosen by the one arrangement function Plan 66 reserves. This plan fills the dry run's delivered-to-sampled frame map, maps guides inside a continuation, deletes the captured continuation workflows and the `continuation` flag (Plan 66 D3), and ships recipe files. The skill section, final trim and integrated review are Plan 67's (CS-8, R).

**Not in this plan. Do not build these:**
- a GPU or live run (D1);
- more than one continuation block per job, or chain orchestration;
- a region edit inside a continuation's kept prefix (refused, suggesting two jobs);
- the `speech-continue` recipe ([Plan 67](../67-h3-community-steering/plan.md), after this plan).

## Existing work and decision

The cards CC-7a to CC-7d, their lattice summary and the assembly additions were written as part of Plan 66 and moved here unchanged when it was split. Their evidence (the captured graph's active path, the motion-context nodes, the bridge and prefix assembly contracts) and reviews are in [Plan 66's inputs](../66-h3-composable-core/inputs.md#planning-evidence); this plan's own record is in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

CC-7a starts at Plan 66 RS1 and CC-10, with Plan 68 CC-4 for guides inside a continuation; it does not wait for Plan 68's stills. Its proof records a bounded comparison with full-canvas preparation. The same placement semantics do not require the same sampler initialization, so prefix and insert share a context helper and bridge keeps its native initializer, all behind one compile call (28 Nov 2026). Then CC-7b and CC-7c in parallel, CC-7d (deleting the captured workflows after CPU parity), and CC-12 (recipe files). Final recipe integration is [Plan 67 CS-8](../67-h3-community-steering/tasks.md), and the integrated review is [Plan 67 R](../67-h3-community-steering/tasks.md). Arrangement stays H3's own choose-one decision. Each arrangement publishes its frozen ranges and its delivered-to-sampled time map, which clock-typed parameters read. A pack loop, such as continuation cycles, may bring its own arrangement only by declaring its length and time map. Edit-then-extend becomes one request in [Plan 107](../107-h3-passes/plan.md). [Task cards](tasks.md)

## Interfaces and handoff

**Consumes:** Plan 66's job, table, dry-run view, composition and arrangement function; Plan 68's guide lowering.

**Produces:** prefix, bridge and insert preparation in one function; the filled delivered-to-sampled frame map; removal of the captured workflows and the `continuation` flag; their recipes and skill lines. Plan 67's `speech-continue` recipe builds on it.

## Completion

CPU tests prove each of these:
- The ported continuation matches the captured active path, apart from the listed differences, and delivers the prefix exactly across the seam.
- It compiles at 512×288 with three images and a speaker clip.
- Clip A, a 63-frame generated gap and clip B compile to a bridge, and unequal owners (120 and 90 frames, n = 39) give matching audio and video lengths. A clip placed at frame 51 compiles to an insert, and an insert at frame 34 is refused.
- A guide at delivered frame 80 in a 120 + 24 continuation is refused, cropped or kept as stated.
- With the Character Swap adapter on, continuation and bridge graphs carry both LoRAs in the model chain.
- The captured workflows and the `continuation` flag are gone, and every recipe fills, dry-runs and compiles.

Plan 67 R, the programme's integrated review, closes Plans 66, 68, 70 and 67 together. The owner's live check judges seams against saved takes.
