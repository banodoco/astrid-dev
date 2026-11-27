# H3 one compiler

**Project:** H3 one compiler

**Goal:** Every H3 request goes through one compiler, one capability table and one dry-run view, so later plans add capabilities as table rows and functions instead of routes, and agents learn one shape from one page.

**Status:** queued

**Owner:** Unassigned

**Target milestone:** 0.3

**Estimate:** 8 days (CPU only; the live check comes after)

**Waiting on:** Independent review of the revised provider seam, refreshed Plan 59/64/65 baseline, owner run authorization and release placement. No Plan 17 dependency.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

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

**Provider-ready core.** Keep one H3-owned, versioned, typed registration/assembly seam around the capability table and six lowering mechanisms. Built-ins and a separately authored test provider enter through the same deterministic, immutable per-job snapshot for admission, describe, dry run and compile. The host owns validation, scheduling, exact ownership/composition and requirements; providers return only validated contributions to the existing mechanisms. Refuse duplicate IDs, unsupported API versions, unmet dependencies and conflicts; report selected provider identity and only used node/model requirements. No external loading, pack installer or VibeComfy family migration in 66. Plan 67 activates genuine independent providers through Astrid's existing registry; 66 needs no Plan 17 work.

**Two clocks.** Clip time (`at`, `during`, `range`) places things in the video. Denoising progress (`phase`, reserved and `unavailable` here; [Plan 67](../67-h3-community-steering/plan.md) adds it) says when during generation a lever acts. Any kind may accept it; the table says which do. No field touches both.

**Invariants.**
- No code names or classifies a kind of job.
- Only composition promises exactness.
- Astrid never silently moves what was asked for: a snap is shown in the dry run, and a mismatch is refused.
- Every limit an agent meets comes from the capability table, with its source.

**Allowed is not tested.** Each lever kind carries a status:
- `compiles`: the default;
- `live-tested`: only with a cited render and date;
- `unavailable`: no lowering exists yet.

Plans 64–70 are proven by compiling. The owner's live test comes after.

**Four layers, each thin:**
1. **Tools:** one compiler; a dry run that shows the resolved job; `describe` that shows what the model and Astrid accept; refusals that name the item, the limit and a fix.
2. **One general H3 skill:** the three rules, the item kinds, how to read a dry run, and recipes shipped as templates.
3. **Problem skills such as Recast:** the order of work, judgment calls, pitfalls, and a brief template naming each shot's recipes.
4. **Templates:** a template is a request with named holes. It can be listed, shown, filled from `--set` values or a shot, written out, and submitted like any request.

**This plan builds the core only.** The injected-provider fixture is not proof of independently installed extensions; 67 owns installation, trust, activation and worker custody. It adds no new creative capability, so its live check is a clean regression check. The capabilities on top come in their own plans, each citing this plan's design, which ships in the pack as `astrid/packs/h3_av/docs/design.md`:
- [Plan 68](../68-h3-guides-and-stills/plan.md): guides and exact stills at any frame;
- [Plan 70](../70-h3-continuation-bridges-inserts/plan.md): continuation, bridges and inserts by placement, and deleting the captured continuation workflows;
- [Plan 67](../67-h3-community-steering/plan.md): community steering (timed prompts, `phase`, the curve tool, ControlNet, binding reports).

**Not in this plan. Do not build these:**
- a GPU or live run of any kind (D1). The owner tests afterwards;
- an external pack loader, generic dependency solver, native VibeComfy plugin extraction or Plan 17 family migration;
- guides or exact stills off frame 0 ([Plan 68](../68-h3-guides-and-stills/plan.md)); this plan reserves their `unavailable` rows and the guide seam;
- the continuation port, bridges or inserts ([Plan 70](../70-h3-continuation-bridges-inserts/plan.md)); continuation keeps running through the captured bundle until then;
- timed prompts, `phase` on guides or LoRAs, ControlNet, a curve-to-audio-guide tool, or per-actor binding work ([Plan 67](../67-h3-community-steering/plan.md)). No GPL node is vendored into Astrid;
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

It adds the capability table as lever kinds, the dry-run view, end-relative time, composition by occurrence with exact-delivery checks, and the template machinery with recipes for what exists. Request identity was already broken once in Plan 64 (D4), so nothing here preserves old digests. The evidence, the reviews and the alternatives are in [inputs.md](inputs.md#planning-evidence). The split into Plans 66, 68 and 70 is reviewed in [research/split-review.md](research/split-review.md).

## Sequence and readiness

Plans 59, 64 and 65 are recorded done, and their integration is an ancestor of published Agent main. Refresh the exact release base, focused CPU baseline and caller/pin inventory; resolve the independent critique of the revised provider seam before freezing the contract. No Plan 17 dependency. Then, in order: CC-1.1 to CC-1.4 (one resolved job, one compile call, every caller moved, then v1 and route classification removed; each mergeable on its own), RS1 (review the job contract), CC-2 (capabilities, as lever kinds), CC-3 (the dry-run view), CC-9 (end-relative time), CC-10 (composition by occurrence and exact delivery), CC-5 (templates and recipes for existing capabilities), CC-6 (the base skill rewrite and thin Recast), and the closing review. Plans 68 and 70 follow, in that order; Plan 67's first cards can start once this plan closes. [Task cards](tasks.md)

## Interfaces and handoff

**Consumes:**
- Plan 64's `GenerationInputs` record, limits table and audio rule;
- Plan 65's canvas size and static mask artifacts;
- Plan 59's shot plan and Recast skill.

**Produces:**
- `compile_job(job, bindings, out_dir)`, and the one function that reads how placed items are arranged;
- the versioned H3-local provider contract and fixture, plus the capability table keyed by lever kind, with status and node-pack columns, and `unavailable` rows reserved for guides, off-zero stills, bridges and inserts;
- the `capabilities` field in `describe`;
- the resolved-job view in the dry run and the settled result, with a reserved slot for the delivered-to-sampled frame map;
- composition by occurrence and the exact-delivery verifier;
- the guide seam (one function from ordered guides to conditioning), implemented by Plan 68;
- the recipe format with `templates list`, `templates show` and `--template` fill, and recipes for existing capabilities;
- the general H3 skill with its three guards, `docs/reference.md`, `docs/design.md`, and the thin Recast skill with its brief template.

## Completion

CPU tests prove each of these:
- `describe` lists lever kinds with their family, fields, defaults, params, status and limits; `range: [-2, end]`, `at: end` and `during: [-2, end]` resolve on each stream's clock and show in the dry run.
- The public prompt-and-image invocation, a masked edit, a fixed-audio redub, Character Swap and the captured-bundle continuation each go through preparation, build, composition and receipt via `compile_job`.
- `branch_for` is gone, and a v1 request is refused with a message to write it as v2.
- `describe --entry h3 --json` shows the same capabilities admission uses, with the reserved rows marked `unavailable`.
- A separately authored CPU fixture registers a kind through the same seam as built-ins, compiles via an existing mechanism, and appears with its provenance and used requirements in the one job snapshot. Missing, duplicate, incompatible or conflicting providers fail before claim; base H3 remains unchanged without the fixture. Core/SDK remain pack-neutral.
- Unsupported pairs are refused, naming both items and a fix. A late LoRA, a mouth edit inside a continuation prefix, `role: control`, `role: guide` and an off-zero still are refused before claim, with no build.
- Every kept or supplied span is byte-identical per channel in the decoded published file, including asymmetric stereo and off-by-one cases; the permission and strength masks are separate, and a vanished grant fails loudly.
- The dry run reports each tag's actual binding, and each occurrence's retained frames, audio and resource estimate.
- The dry run separates requested grants, effective latent influence and delivered ownership across the frame-4 boundary.
- Every recipe fills, dry-runs and compiles, and a written template submits as a plain request.
- The skill guards pass, and a cold-read agent gets from a described shot to a dry run using only the skill.

The closing review then closes the plan. The owner's live check after it is a regression check of the shipped recipes.
