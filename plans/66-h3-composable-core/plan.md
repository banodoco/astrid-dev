# H3 composable core

**Project:** H3 composable core

**Goal:** An agent makes H3 shots — continue, start from an image, start and end on exact images, inpaint, redub, speaker voice — with one request shape, one compiler and one general skill, and problem skills like Recast become short guides with templates.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 15.5 days (phase 1, the core mechanisms: 7; phase 2, continuation, bridges and inserts: 6; phase 3, templates and skills: 2.5; CPU only, the live test comes after)

**Waiting on:** Owner greenlight of scope, and Plans 59, 64 and 65.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

**Levers.** Every control on a job is a lever in one of three families:
- **Output** levers (placed items and edits) decide what's in the result. They're the only ones that can be exact.
- **Context** levers (references, guides, the prompt) are what the model looks at.
- **Process** levers (adapters and settings) change how the model runs.

Context and Process only influence.

**One ladder for any asset:**
- place it (`role: timeline`): kept exactly;
- show it at a moment (`role: guide`): soft;
- show it for the whole clip (`role: reference`): soft.

**Three rules for Output.** Placed material is kept. Time nothing covers is generated. An edit opens placed material for change. Continue, start image, bridge, insert, inpaint, redub and Character Swap are all requests in this one shape. None is a route, a flag or preset code.

**Six mechanisms.** The compiler merges levers into six things:
1. the latent and its ownership mask;
2. timed rows;
3. untimed rows;
4. the prompt text;
5. the model chain;
6. the sampler.

Composition then restores every kept pixel and sample. A new lever adds a kind to the table and a function that feeds one mechanism. It never adds a request structure or a compiler branch.

**Two clocks.** Clip time (`at`, `during`, `range`) places things in the video. Denoising progress (`phase`, reserved and `unavailable` in this plan) says when during generation a lever acts. Any kind may accept it; the table says which do. No field touches both.

**Invariants.**
- No code names or classifies a kind of job.
- Only composition promises exactness.
- Astrid never silently moves what was asked for: a snap is shown in the dry run, and a mismatch is refused.
- Every limit an agent meets comes from the capability table, with its source.

**Allowed is not tested.** Each lever kind carries a status:
- `compiles`: the default;
- `live-tested`: only with a cited render and date;
- `unavailable`: no lowering exists yet.

Plans 64–66 are proven by compiling. The owner's live test comes after.

**Four layers, each thin:**
1. **Tools:** one compiler; a dry run that shows the resolved job; `describe` that shows what the model and Astrid accept; refusals that name the item, the limit and a fix.
2. **One general H3 skill:** the three rules, the item kinds, how to read a dry run, and recipes shipped as templates.
3. **Problem skills such as Recast:** the order of work, judgment calls, pitfalls, and a brief template naming each shot's recipes.
4. **Templates:** a template is a request with named holes. It can be listed, shown, filled from `--set` values or a shot, written out, and submitted like any request.

**Phases.**
- **Phase 1 (core):** one public path and one resolved job; capabilities as lever kinds; the dry-run view; end-relative time; guides; exact stills at any frame; templates; both skills.
- **Phase 2 (continuation):** continuation, bridges and inserts by placement: a clip before, between or after generated time, through the pinned motion-context nodes. The captured continuation workflows are then deleted (D3). Git history keeps them.

**Not in this plan. Do not build these:**
- a GPU or live run of any kind (D1). The owner tests afterwards;
- more than one continuation block per job, or any chain orchestration;
- timed prompts, `phase` on guides or LoRAs, ControlNet, a curve-to-audio-guide tool, or per-actor binding work. These are [Plan 67](../67-h3-community-steering/plan.md). No GPL node is vendored into Astrid;
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

**Phase 1** runs in order: CC-1.1 to CC-1.4 (one resolved job, one compile call, every caller moved, then v1 and route classification removed; each mergeable on its own), RS1 (review the job contract), CC-2 (capabilities, as lever kinds), CC-3 (the dry-run view), CC-9 (end-relative time), CC-4 (guides), CC-8 (exact stills at any frame).

**Phase 2** is CC-7a (prefix continuation; it first checks whether one full-canvas preparation can serve prefix, insert and bridge), then CC-7b (bridges) and CC-7c (inserts) in parallel, then CC-7d (deleting the captured workflows and the `continuation` flag). It starts after CC-3, not after the skill.

**Phase 3** is CC-5 (templates, with recipes for every phase 1 and phase 2 capability) and CC-6 (both skills, written once against the finished system), followed by the final review. [Task cards](tasks.md)

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
- `describe` lists lever kinds with their family, fields, defaults, params and limits; `range: [-2, end]`, `at: end` and `during: [-2, end]` resolve on each stream's clock and show in the dry run.
- The public prompt-and-image invocation, a masked edit, a fixed-audio redub and Character Swap each go through preparation, build, composition and receipt via `compile_job`.
- `branch_for` is gone, and a v1 request is refused with a message to write it as v2.
- `describe --entry h3 --json` shows the same capabilities admission uses.
- Unsupported pairs are refused, naming both items and a fix. A late LoRA, a mouth edit inside a continuation prefix and `role: control` are refused before claim, with no build.
- Every kept or supplied span is byte-identical per channel in the decoded published file, including asymmetric stereo and off-by-one cases; the permission and strength masks are separate, and a vanished grant fails loudly.
- The dry run reports each tag's actual binding, and each occurrence's retained frames, audio and resource estimate.
- The dry run separates requested grants, effective latent influence and delivered ownership across the frame-4 boundary.
- Guides bind at the right resolved index, including the last delivered frame on an off-lattice shot.
- Exact stills at frame 0, an interior frame and the last frame each come out pixel-exact (frame 0 and frame 51 hold one frame; frame 61 and the last frame hold their four-frame chunk, clipped at the end), and the dry run shows each requested frame, chunk and hold.
- Every recipe fills, dry-runs and compiles.
- A written template submits as a plain request.
- A cold-read agent gets from a described shot to a dry run using only the skill.

**Phase 2**
- The ported continuation matches the captured active path, apart from the listed differences.
- It delivers the prefix exactly across the seam.
- It compiles at 512×288 with three images and a speaker clip.
- Clip A, a 63-frame generated gap and clip B compile to a bridge, and unequal owners (120 and 90 frames, n = 39) give matching audio and video lengths. A clip placed at frame 51 compiles to an insert, and an insert at frame 34 is refused.
- With the Character Swap adapter on, continuation and bridge graphs carry both LoRAs in the model chain.
- The captured workflows and the `continuation` flag are gone.

Review then closes the plan. How the port looks and sounds against the old workflows, and how well guides are followed, are judged in the owner's live test afterwards.
