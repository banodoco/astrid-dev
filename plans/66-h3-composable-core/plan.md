# H3 composable core

**Project:** H3 composable core

**Goal:** An agent makes H3 shots — continue, start from an image, start and end on exact images, inpaint, redub, speaker voice — with one request shape, one compiler and one general skill, and problem skills like Recast become short guides with templates.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 12.5 days (phase 1, the core: 7; phase 2, continuation and bridges: 5.5; CPU only, the live test comes after)

**Waiting on:** Owner greenlight of scope, and Plans 59, 64 and 65.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

**One model.** Every H3 job is:
- a **canvas** (size and duration);
- **placed items**, which are exact: video, stills and audio at a time;
- **conditioning**, which is soft: untimed references, and guides at a frame (`role: guide`);
- **grants**: stream, interval, optional region, strength, seed;
- prompt, model and sampling settings.

Three rules decide what happens. Placed material is kept. Time nothing covers is generated. A grant opens placed material for change. Continue, start image, inpaint, redub and Character Swap are all requests in this one shape. None is a route, a flag or preset code.

**Four layers, each thin:**
1. **Tools:** one compiler; a dry run that shows the resolved job; `describe` that shows what the model and Astrid accept; refusals that name the item, the limit and a fix.
2. **One general H3 skill:** the three rules, the item kinds, how to read a dry run, and recipes shipped as templates.
3. **Problem skills such as Recast:** the order of work, judgment calls, pitfalls, and a brief template naming each shot's recipes.
4. **Templates:** a template is a request with named holes. It can be listed, shown, filled from `--set` values or a shot, written out, and submitted like any request.

**Phases.**
- **Phase 1 (core):** one public path and one resolved job; capabilities; the dry-run view; guides; exact stills at any frame; templates; both skills.
- **Phase 2 (continuation):** continuation, bridges and inserts by placement: a clip before, between or after generated time, through the pinned motion-context nodes. The captured continuation workflows are then deleted (D3). Git history keeps them.

**Not in this plan. Do not build these:**
- a GPU or live run of any kind (D1). The owner tests afterwards;
- more than one continuation block per job, or any chain orchestration;
- timed text prompts, an Event Curve tool, or any GPL node vendored into Astrid;
- shot-plan schema changes, or automatic take recording on shots;
- an endless-continuation skill, take lineage or continue-from-take;
- variations or multi-pass chains in the core;
- a planner that picks the method, a workflow engine, or a template language beyond named holes;
- normalized mask coordinates or a second model.

## Existing work and decision

Request v2 already has the model's shape: timeline and reference items with per-item edit grants. This plan removes what sits between that request and one compiler:
- request v1 as the internal format (the public hook builds v1 today);
- `branch_for` and the per-route compilers;
- the route-specific refusals.

It adds the guide role, templates and the continuation port. Request identity was already broken once in Plan 64 (D4), so nothing here preserves old digests. The evidence, the reviews and the alternatives are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Plans 59, 64 and 65 land first.

**Phase 1** runs in order: CC-1 (one public path and job), RS1 (review the job contract), CC-2 (capabilities), CC-3 (the dry-run view), CC-4 (guides), CC-8 (exact stills at any frame), CC-5 (templates), CC-6 (both skills).

**Phase 2** is CC-7 (the continuation port, then deleting the captured workflows), followed by the final review. [Task cards](tasks.md)

## Interfaces and handoff

**Consumes:**
- Plan 64's `GenerationInputs` record, limits table and audio rule;
- Plan 65's canvas size and static mask artifacts;
- Plan 59's shot plan and Recast skill.

**Produces:**
- `compile_job(job, bindings, out_dir)`;
- the `capabilities` field in `describe`;
- the resolved-job view in the dry run and the settled result;
- `role: guide`;
- the recipe format with `templates list`, `templates show` and `--template` fill;
- the general H3 skill, `docs/reference.md`, and the thin Recast skill with its brief template.

## Completion

CPU tests prove each of these:

**Phase 1**
- The public prompt-and-image invocation, a masked edit, a fixed-audio redub and Character Swap each go through preparation, build, composition and receipt via `compile_job`.
- `branch_for` is gone, and a v1 request is refused with a message to write it as v2.
- `describe --entry h3 --json` shows the same capabilities admission uses.
- Unsupported pairs are refused, naming both items and a fix.
- The dry run separates requested grants, effective latent influence and delivered ownership across the frame-4 boundary.
- Guides bind at the right resolved index, including the last delivered frame on an off-lattice shot.
- Exact stills at frame 0, an interior frame and the last frame each come out pixel-exact, and the dry run shows each one's 4-frame hold.
- Every recipe fills, dry-runs and compiles.
- A written template submits as a plain request.
- A cold-read agent gets from a described shot to a dry run using only the skill.

**Phase 2**
- The ported continuation matches the captured active path, apart from the listed differences.
- It delivers the prefix exactly across the seam.
- It compiles at 512×288 with three images and a speaker clip.
- Clip A, a gap and clip B compile to a bridge; a clip placed at frame 51 compiles to an insert.
- The captured workflows and the `continuation` flag are gone.

Review then closes the plan. How the port looks and sounds against the old workflows, and how well guides are followed, are judged in the owner's live test afterwards.
