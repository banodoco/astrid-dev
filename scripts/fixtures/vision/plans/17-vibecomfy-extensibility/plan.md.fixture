# Pack extension points: switch on the protocol and prove it

**Project:** Pack extension points: switch on the protocol and prove it

**Goal:** Anyone can build one agent-facing tool over a family of workflows, as h3_av does for MiniMax H3: generalise its machinery into VibeComfy (entries with variants chosen by intent from their inputs; a describe and dry-run plan an agent can parse; build and after_outputs hooks; file maps; media helpers), so h3_av becomes a VibeComfy plugin pack and Astrid mirrors VibeComfy's registry and deletes its own mode inference; switch on Astrid's extension-point protocol to install families; prove it with an image family (txt2img, img2img, inpaint, outpaint) and sound on video, after Plan 32 creates the first points.

**Status:** paused

**Owner:** Unassigned

**Estimate:** about 15–18 (inferred): phase 1 about 7, phase 2 about 9

**Waiting on:** the owner's go to queue it (ready, held by the owner on 9 Nov); scope agreement; Plan 32 T6b (T6d for A4)

**Vision gaps:** [Composable capabilities](../../vision/gaps/LS-003-full-stack-contributions.md) (primary) · [Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting).

**Contributes to closure:** F-008 step 3: the pack extension protocol switched on and proven with non-h3 workflow families (an image family and sound on video). Milestone C.

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

A pack can extend another pack. A pack declares a named **extension point** with a versioned schema. Another pack **contributes** to it. A composite pack contributes to several points at once, for example a VibeComfy workflow, a generation engine, a timeline effect and a UI panel, and it all works together through one install, trust and discovery path. This remains a draft; queue status, owner and estimate are in the [project queue](../../README.md).

Since the owner's later direction of 9 Nov (below), the main outcome is that **anyone can build one agent-facing tool over a family of workflows**, as h3_av does for MiniMax H3, with the variant chosen by intent. The extension protocol is how such a family installs into Astrid.

## Direction (8 Nov 2026)

An independent review (merge-run desk, `merge-run/path-review/PACK-EXTENSION-PROTOCOL.md`) found that **Astrid already has this protocol, built and tested but unused**:
- astrid-agent `astrid/core/extensions/` (model, registry, scopes, sidecar walker; `schema/point.json`, `contribution.json`), commit `864179976`;
- a point is `<pack>/extensions/points/<name>.yaml`, with an integer version, `min_supported`, cardinality, a JSON Schema and an optional code interface;
- a contribution is `<pack>/extensions/<point>/<key>.yaml`;
- discovery covers built-in, installed, user and project roots, with shadowing, disabling and quarantine.

No pack declares a point yet, and no production code calls it. Meanwhile about nine ad hoc extension shapes exist. The protocol needs only three concepts: point, contribution, and the existing `dependencies.packs`, with a rule that contributing to `<owner>.*` requires `<owner>` as a dependency. Trust and install reuse [Plan 06](../06-packs/plan.md) unchanged: install is the trust moment, and contributions inherit their pack's trust.

[Plan 32](../32-generation-placement-targets/plan.md) creates the first three points as it builds the seams that need them:
- `generation.engine` (recipe plus `align` and `execute`; ComfyUI contributed by the `vibecomfy` pack);
- `generation.machine` (claim, ship and run, fetch, release; RunPod contributed);
- `vibecomfy.workflows` (a ready root, entries, an optional `build` and an optional `finalize`; h3_av becomes one composite pack with one contribution in Plan 32 T6b).

Environment setup is the `align` half of the engine point. It is generic in core and engine-specific in each contribution.

## Direction (owner, 9 Nov 2026): generalise into VibeComfy; h3_av becomes a pack that depends on it

What is general moves **into VibeComfy itself**, so standalone VibeComfy users get it too. What is specific to h3 becomes a VibeComfy plugin pack that depends on it. Astrid uses the same plugin, with no duplicate. This replaces "VibeComfy itself does not change" from the 8 Nov review (`merge-run/path-review/H3-GENERALIZATION.md`), and is done after Plan 32, which finishes on its current shape. The review's classification still holds: class **b** and **c** are general, and class **a** stays h3's.

- **Into VibeComfy (general):**
  - a workflow-family registration on its existing `PluginAPI` (`vibecomfy/extras.py:27-52`; plugins load from the `vibecomfy.plugins` entry points and `vibecomfy_extras/`): `register_workflows(ready_root, entries, build=None, finalize=None)`, with exactly the contract of Plan 32's `vibecomfy.workflows` point (entries in the thin-entry shape `{id, kind, modes, bundle, needs, binds, defaults}`; `build(inputs, files, out) -> {workflow, bindings, plan}`; `finalize(job_dir, inputs, files, outputs) -> outputs`);
  - VibeComfy's own run path calls `build` before submit and `finalize` after outputs. It has no post-ComfyUI hook today. Name it so it is not confused with template assembly (`templates.py:1381`);
  - entry `inputs` with `file` and `file_map` types, and `needs` as objects, in VibeComfy's entry inputs (its strict validator, `vibecomfy/entries.py:49,61`, cannot express h3 today);
  - `vibecomfy run --entry` with inputs and media staging (uploads move from Astrid into VibeComfy);
  - the post-output hook is named `after_outputs`, not `finalize` (which collides with `templates.finalize` and `VibeWorkflow.finalize`);
  - `build` must be pure: it also runs on the controller, because `requirements()` calls it;
  - the media helpers in h3 that are not specific to h3, lifted out of `h3_av/shared/compose.py` (1,398 lines) and `verify/verify.py`: mux audio onto video, splice segments, and check coverage and preservation, plus one ffprobe wrapper instead of h3's own (Astrid has `core/media.py` `MediaProbe`). Sound-on-video and a lip-sync pack would use the same helpers.
- **Astrid:** the `vibecomfy.workflows` point becomes a thin mirror of VibeComfy's registry. An Astrid pack can still contribute, and that is forwarded to `register_workflows`. A native VibeComfy plugin (an entry point) shows up in Astrid on its own. It enters only through a thin pack that pins `{distribution, version, sha256}`. Astrid loads pinned distributions only, never drop-ins, and lists unpinned entry points without loading them. The pin travels in the engine manifest's `extra.plugins`, so a RunPod machine installs exactly the same wheel, and plugin digests are part of machine custody. `astrid packs extensions` lists both kinds.
- **h3_av (specific, a pack that depends on VibeComfy):** request schema v1 and v2, Character Swap, masks, static regions, the planner, continuation timing (5+17k grid, the 362→360 trim), the three workflow trios, and h3's use of the shared media helpers. It is installable for standalone VibeComfy (`pip install`, entry point) and through Astrid (a pack whose only content is that plugin and its pin).
- **Proof:**
  - standalone VibeComfy runs the h3 entry with `build` and `finalize` on a CPU fake;
  - Astrid runs the same plugin through `generate` on local, attached and the RunPod CPU fake;
  - the sound-on-video pack, written as a native VibeComfy plugin, uses the lifted mux helper;
  - a grep finds no h3 code in Astrid outside the pinned plugin reference.
- **Cross-repository:** VibeComfy changes land in VibeComfy first, then Astrid pins them. Releases follow the shared run contract.

## Direction (owner, 9 Nov 2026, later): one route over a family of workflows

**Her framing** (spoken, paraphrased; source in [inputs.md](inputs.md#owner-direction-9-nov-later)):
- h3_av is a tool for building workflows from what an agent needs. It gives an agent, in a form it can parse, one tool on top of a set of workflows, here MiniMax H3.
- Generalise all the machinery that makes that work, so other people can build tools like it for other kinds of workflow.
- Her example is an image tool. It is set up differently when the user wants inpainting or another variant, but it gives them a single route to all of them: one agent-facing tool over a family of workflows, with the variant chosen by intent.
- Not building it yet: think it through, then update this plan.

**What the earlier 9 Nov design leaves out.** It generalises how one entry is built and finished (`build`, `after_outputs`, file maps and media helpers). It does not generalise how a tool picks *which* workflow to run. Today that choice lives in three unrelated places, and an agent can read none of them:
- h3's `branch_for`, in code;
- Astrid's hard-coded `_infer_image_mode` and `_infer_video_mode`;
- VibeComfy's router, whose predicates are opaque lambdas.

A thin entry also has exactly one `bundle`. So today "one tool, variants by intent" can only be written by hiding the choice inside `build`, where neither `describe` nor a dry run can show it. The first-principles split, with file:line evidence, is in [inputs.md](inputs.md#what-the-h3_av-machinery-is).

**Design: a workflow family is an entry with variants.** This is part of VibeComfy's `register_workflows` contract, and Astrid's `vibecomfy.workflows` point mirrors it.
- An entry may carry an ordered `variants` list. Each variant is `{id, mode, bundle, when, summary, inputs, defaults}`; `bundle` and `inputs` are optional when the family has a `build`. An entry without `variants` is a one-variant family, so every existing entry and every version-1 contribution stays valid.
- **`when`** is a small declarative test over named inputs: `present: [...]`, `absent: [...]` and `equals: {path: value}`. The first variant that matches wins, and the last may have no `when`, as the fallback. An explicit `variant` input overrides the test. If the inputs don't fit the chosen variant, the request is refused.
- **`route: file.py:fn`** is optional, for rules `when` cannot express, such as h3's tests over its media list. It returns `{variant, reason}`, is pure and runs on CPU.
- **`request`** is optional: a JSON Schema for one structured request document (h3's v1 and v2). Without it, inputs are flat typed ports.
- `build(inputs, files, out, *, variant)` and `after_outputs` work as before. `after_outputs` may return `{outputs, evidence}`, for example a preservation check, so there is no separate verify hook.
- Every refusal has one shape, `{code, field, fix}`, lifted from h3's `H3RequestError`.
- A variant's `id` is the family's own name; its `mode` comes from the shared vocabulary (`t2i`, `inpaint`, `v2v` and so on), so Plan 32 T6d's default slots still key on `(kind, mode)`.

**The agent contract, which every family gets for free:**
- **Discover:** `vibecomfy entries --json` and `astrid generate list` show one row per family.
- **Describe:** `describe --entry <id> --json` gives the request schema or inputs, then the variants in order, each with its mode, its `when` (or the route's summary), inputs, defaults and availability. One read tells an agent every route.
- **Plan:** `--dry-run` returns one envelope: `{entry, variant, reason, inputs (defaults applied), bindings, needs, warnings, ignored_fields, details, submission: eligible | blocked, error}`. `details` is the family's own plan from `build`. h3's `plan.json` becomes this envelope with h3 details (timing, trim, mask previews).
- **Run:** the same command without `--dry-run`, on any placement.

**Burn down: three routers become one.**
- VibeComfy's built-in router rules (`router/_rules.py:53-70`) become variants of built-in `image` and `video` families. `router.pick` reads those, and `register_route` leaves `PluginAPI` (owner decision 1 in [inputs.md](inputs.md#open-owner-decisions)).
- Astrid deletes `_infer_image_mode`, `_infer_video_mode` and `_EXPLICIT_ONLY_IMAGE_MODES`. A `generate image` with no entry uses the kind's default family, which routes. A user's `(kind, mode)` pin from Plan 32 T6d still wins for the mode the family routes to.
- h3's `branch_for` becomes its `route`. Its own CLI (`astrid h3 plan|run|compose|edit`) is deleted in favour of describe, `--dry-run` and run.

**Where it lands:**
- **VibeComfy:** variants, `when`, the route hook, selection, describe, the plan envelope, the refusal shape, and the router rules as built-in families, together with V1–V3 from the earlier direction.
- **Astrid:** projects VibeComfy's describe and plan without reshaping them; raises the `vibecomfy.workflows` point to version 2 with `min_supported: 1`; deletes its mode inference; adds one section on families to the generation skill.
- **h3:** its request schemas, its route (`branch_for`), builders, timing, Character Swap, masks, its plan details, and an `after_outputs` built on the media helpers.

**Tested against two families:**
- **Image:** txt2img, img2img, inpaint (with a mask) and outpaint, as a native plugin with no Python apart from an optional preservation check. The variant is chosen by which inputs are present. This proof is required, because sound on video has a single variant and does not test routing at all.
- **Sound on video:** a one-variant family proving `after_outputs` and the mux helper.
- **Lip-sync, considered:** audio-driven lip-sync fits. Text-driven lip-sync needs TTS and then lip-sync in sequence, a multi-pass request. That stays out of scope and is recorded as an extension need.

## Goal and scope

**Goal:** anyone can build one agent-facing tool over a family of workflows, with variants chosen by intent and a describe and dry-run plan an agent can parse, first in standalone VibeComfy and then through Astrid. h3_av becomes one such family, a VibeComfy plugin. Astrid's extension protocol is switched on to install families.

- **Included, phase 1 (VibeComfy, standalone):** workflow families in VibeComfy (V1, V5, V2, V3, V4) and the image family proved standalone (IMG, first half).
- **Included, phase 2 (Astrid, after Plan 32 T6b; A4 after T6d):**
  - run the extension registry check inside the install transaction, with the owner-dependency rule (P1);
  - add `astrid packs extensions` to list points, contributions and problems (P2);
  - the mirror and pinned plugins (A1, A2);
  - h3 as a plugin (H1, A3);
  - family routing through `generate`, deleting Astrid's mode inference (A4), and the image family through Astrid (IMG, second half);
  - sound on video as a native plugin (S2, replacing the earlier Astrid-only P4);
  - the protocol and family docs (P3).
- **Deferred:**
  - folding the remaining `pack.extensions.generation.*` keys (`features`, `modes`) into a point (Plan 32 T6 deletes the hard-coded h3 backend; nothing else needs the rest yet);
  - version ranges, priority fields or point inheritance (the point's existing integer `version` and `min_supported` are enough);
  - per-contribution or per-variant trust;
  - variants that chain workflows (multi-pass, such as text-driven lip-sync);
  - routing by a language model: routing is deterministic from inputs, and the agent states its intent through inputs or `variant`;
  - hot reload of Agent-side points;
  - unifying the App manifest with the Agent registry;
  - migrating `actions`, `ui` or `rendering` into points.
- **Undecided:** whether the App's closed contribution kinds join the protocol in this plan or a later one. Also the open owner decisions in [inputs.md](inputs.md#open-owner-decisions).

## What we build on

- The protocol (`astrid/core/extensions`) and the three points Plan 32 creates. h3_av is the first contribution, made in Plan 32 T6b.
- VibeComfy's `PluginAPI`, thin entries, `InputSpec` and router.
- h3_av's planner, refusal shape and media code, as the donor of the general pieces.
- The image family exercises routing, a mask file input, numeric outpaint inputs and an explicit override. Sound on video exercises a ready root, a media input and `after_outputs`, with no `build`.

See the [Liquid Software vision](../../vision/pillars/liquid-software.md); exact starting identities are in [inputs.md](inputs.md).

## Sequence

- **Phase 1:** V1, then V5, then V2, with V3 alongside; then V4 and IMG's standalone half. Phase 1 starts once Plan 32 T6b-2 fixes the point's shape.
- **Phase 2, after Plan 32 T6b:**
  - P1 and P2 in parallel;
  - A1, then A2, then A3 (with H1);
  - A4 once A1, V5 and Plan 32 T6d have landed, then IMG's Astrid half;
  - S2 after A2;
  - P3, then the review rounds.

All of it is CPU only; the live runs are [Plan 34](../34-real-gpu-proof/plan.md)'s. See [tasks.md](tasks.md).

## Completion

- **One route, variants by intent:**
  - standalone, and through `astrid generate image --entry image`, an agent discovers, describes, dry-runs and runs the image family;
  - each of its four variants is chosen from the inputs alone, and the dry run gives the reason;
  - an explicit `variant` overrides the choice;
  - a mask without an image is refused with `{code, field, fix}`.
- `generate image` and `generate video` with no entry route through the built-in families. A grep finds no `_infer_image_mode` or `_infer_video_mode`, and no built-in rule in VibeComfy's `router/_rules.py`.
- `describe --entry h3` lists h3's variants; its dry run is the generic envelope; `astrid h3` is gone.
- A pack outside core installs through `astrid packs add`, and its contribution is validated before the swap. A broken contribution, or one without its owner dependency, is refused with a fix.
- `astrid packs extensions` lists points, contributions and problems.
- The sound-on-video plugin produces a video with the generated audio, locally and through the RunPod CPU fake.
- The protocol, its points and how to write a family are documented.
- **Not proven here:** real inference (Plan 34), including inpaint and outpaint quality. Record any extension needs the two families do not cover. Destination and publication authority follow the shared [run contract](../../skills/astrid-dev-shared/run-contract.md); verify the intended `pre-main` destination at setup rather than assuming it.

## Read next

- [tasks.md](tasks.md): intended work and task-scoping boundary.
- [inputs.md](inputs.md): source identities, references, and setup requirements.
