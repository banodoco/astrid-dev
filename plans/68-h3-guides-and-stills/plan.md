# H3 guides and exact stills

**Project:** H3 guides and exact stills

**Goal:** An agent steers a shot softly with an image, clip or sound at any frame, and pins exact stills at any frame, including start and end images.

**Status:** active

**Owner:** h3-orchestrator, session [`session_011EzfW4exucHx4FeFWbexak`](https://claude.ai/code/session_011EzfW4exucHx4FeFWbexak)

**Target milestone:** 0.2

**Estimate:** 3–5 days (CPU only; re-estimated 28 Nov 2026 as units of at most 3 days; the live check comes after)

**Waiting on:** Plan 66's contract review (RS1), its view writer (CC-3) and composition by occurrence (CC-10).

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

This plan adds two capabilities on the [Plan 66](../66-h3-composable-core/plan.md) core, following its design (`astrid/packs/h3_av/docs/design.md`):
- **Guides** (`role: guide`): an image, clip or audio at a frame, including the last delivered frame. They're soft Context levers that lower to H3's timed rows through the one guide function Plan 66 reserves.
- **Exact stills at any frame:** a placed still holds its H3 time chunk (one frame at frames 0, 17, 34, …; four frames elsewhere), built from a full-canvas source. Composition by occurrence and exact delivery come from Plan 66 CC-10.

It flips the reserved `role: guide` and off-zero still rows from `unavailable`, amends the design file, and ships recipes (guided end, soft keyframes, start and end on exact images, exact mid-shot keyframe) plus one short skill section.

**Not in this plan. Do not build these:**
- a GPU or live run (D1);
- `phase` on guides, or the curve tool ([Plan 67](../67-h3-community-steering/plan.md));
- guides or stills inside a continuation ([Plan 70](../70-h3-continuation-bridges-inserts/plan.md));
- an exact still that shares a chunk with another exact owner (refused, naming both).

## Existing work and decision

The cards CC-4 and CC-8 were written as part of Plan 66 and moved here unchanged when it was split, apart from composition, which stayed in Plan 66. Their evidence and reviews are in [Plan 66's inputs](../66-h3-composable-core/inputs.md#planning-evidence); this plan's own record is in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

CC-4 (guides) starts at Plan 66 RS1 and CC-3; CC-8 (exact stills) also needs Plan 66 CC-10; CC-11 ships example inputs and recipe files, and the final cold-read integration happens once in [Plan 67 CS-8](../67-h3-community-steering/tasks.md). [Plan 70](../70-h3-continuation-bridges-inserts/plan.md) no longer waits for stills: it needs only CC-4, for guides inside a continuation (28 Nov 2026). Guides are rows: H3's assembler is the only writer of guide positions and phase schedules, positions are clock-typed and converted through the time map, and a pack may add a guide-position fragment (for example Virtual Head Start) only by declaring that write. [Task cards](tasks.md)

## Interfaces and handoff

**Consumes:** Plan 66's job, capability table, dry-run view, composition by occurrence, recipe format and guide seam.

**Produces:** `role: guide` and its lowering function; placed stills at any frame with chunk holds; the full-canvas source builder; their recipes and skill lines. Plan 67 wraps the guide function for `phase`; Plan 70 uses the full-canvas builder.

## Completion

CPU tests prove each of these:
- Guides bind at the right resolved index, including the last delivered frame on an off-lattice shot; clip and audio guides are cropped as the node does, and the dry run shows each crop.
- Exact stills at frame 0, frame 51, an interior frame and the last frame come out pixel-exact (frames 0 and 51 hold one frame; others hold their four-frame chunk, clipped at the end), and the dry run shows each requested frame, chunk and hold.
- Two stills in one chunk, and two exact owners of one stream and span, are refused, naming both.
- Every new recipe fills, dry-runs and compiles; the skill guards pass.

The owner's live check after this plan judges guide adherence and visible holds.
