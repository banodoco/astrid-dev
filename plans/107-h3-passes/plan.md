# H3 passes

**Project:** H3 passes

**Goal:** One H3 request can run several sampling passes, with the frame and audio transforms between them, so de-rope, edit-then-extend, refine and repair are single, exact, explainable jobs.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 15–23 days (CPU only; units of at most 3 days; planning figures, not measurements; live check separately authorized)

**Waiting on:** Plan 66's extension contract and test kit (CC-13, CC-14); Plan 70's arrangements and time map; Plan 67's combined stacking proof (CS-13). All are in Release 16.

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

Plan 66 gives every H3 job a `passes[]` list and executes one pass. This plan executes several. Each pass has:
- an `init`: empty, or an earlier pass's output after declared media transforms;
- a `denoise.start`, from which H3 builds the noise schedule;
- its own socket fills;
- a consented budget ceiling;
- an optional bounded `repeat` for windows and extend.

**Included:**
- **Pass execution:** ordered passes in one job, each from its declared `init`, with per-pass provenance (seed, settings, inputs, transforms) in the receipt.
- **The `media` socket at run time.** Contributions transform IMAGE, AUDIO or LATENT at a pass's `init` or after decoding. Each declares whether it emits or inverts a time map, and whether it is exact (frame selection) or soft (for example vocoded audio).
- **Actions after a pass** (`after: <pass>`) that read that pass's output and emit data, such as a hold map.
- **A composed time map.** It supports many-to-one holds, grid padding and inverse transforms; every clock-typed parameter and every exactness check is evaluated through it. H3 verifies that an inverse returns the real delivered length, and restores kept content from the source on the world clock, never from a pass's output.
- **Budget and consent.** The dry run shows each pass's maximum frames and model calls. The artist consents to a ceiling, because a stretched pass can grow (one documented clip went from 124 to 345 frames).
- **Bounded `repeat`:** windows and extend as repeats of one pass with tail carry, replacing ad-hoc long-generation loops.
- **Proof pack: MAINodes de-rope.** Jerk Oracle runs as an action after the base pass; Time Smear is a media transform that emits the time map; Exact Recover inverts it exactly, and Audio Recover softly; the second pass declares `denoise.start`.
- **Recipes** for de-rope, edit-then-extend, refine, and Dials time curves carried correctly across passes.

**Not in this plan:**
- a separate SIGMAS or NOISE socket (passes declare `denoise.start`);
- a VAE or decode socket;
- pack-owned composition or splicing;
- other model families (LTX or Wan de-rope);
- data-dependent pass counts beyond a bounded `repeat`;
- MAINodes True Clock and DyRoPE, which patch the model class globally and are refused by Plan 66's test kit;
- per-branch model patches.

## Existing work and decision

`shared/planner.py` already derives ordered `sampling_passes()` and per-pass views. Kent's continuation cycles and MAINodes de-rope show that real H3 workflows are multi-pass, but today they hide passes inside one node or a hand-wired graph, where H3 cannot plan, check or explain them. An adversarial review of the five-socket contract found that de-rope could not be expressed without first-class passes, a media socket and a hold-capable time map. The owner placed pass execution in Release 17, after the single-pass contract ships in Release 16. Evidence: [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Start after Plan 66 CC-13 and CC-14, Plan 70's arrangements and Plan 67 CS-13 have landed on the Release 17 base. [Tasks](tasks.md) run the pass record first, then the media socket and the time map in parallel. Budget, provenance and `repeat` follow, and the de-rope proof pack and recipes come last. Recording this plan does not authorize implementation.

## Interfaces and handoff

**Consumes:** Plan 66's job record (`passes[]`, `branches[]`), extension contract, test kit and composition; Plan 70's arrangements and time map; Plan 67's three packs and stacking receipts; ComfyUI-MAINodes at a reviewed pin (the de-rope nodes).

**Produces:**
- multi-pass execution in one job;
- the runtime `media` socket;
- a composed, hold-capable time map;
- per-pass budget, consent and provenance;
- bounded `repeat`;
- the de-rope proof pack and recipes.

## Completion

CPU tests prove each of these:
- A two-pass job (generate, then re-denoise from `denoise.start` 0.55) runs from one request, with per-pass seeds and inputs in the receipt.
- A de-rope job stretches, re-denoises and recovers with the pinned MAINodes nodes. The recovered video has the real delivered length, kept frames are byte-exact against the source, and recovered audio is labelled soft.
- A wrong inverse length, a media transform without a time-map declaration, and a pass over its consented budget are each refused before claim.
- A Dials time curve lands at the same real-time moment in both passes.
- Edit-then-extend, refused in Release 16, compiles as one two-pass request.

Quality of de-roped motion is judged in a separately authorized live check.
