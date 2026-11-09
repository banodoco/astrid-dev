# Pack extension points: switch on the protocol and prove it

**Vision gaps:** [Composable capabilities](../../vision/gaps/LS-003-full-stack-contributions.md) (primary) · [Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting).

**Contributes to closure:** F-008 step 3: the pack extension protocol switched on and proven with a second, non-h3 composite pack. Milestone C.

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

A pack can extend another pack. A pack declares a named **extension point** with a versioned schema. Another pack **contributes** to it. A composite pack contributes to several points at once, for example a VibeComfy workflow, a generation engine, a timeline effect and a UI panel, and it all works together through one install, trust and discovery path. This remains a draft; queue status, owner and estimate are in the [project queue](../../README.md).

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
  - the file-map input type (`{id: path}`) in VibeComfy's entry inputs;
  - the media helpers in h3 that are not specific to h3, lifted out of `h3_av/shared/compose.py` (1,398 lines) and `verify/verify.py`: mux audio onto video, splice segments, and check coverage and preservation, plus one ffprobe wrapper instead of h3's own (Astrid has `core/media.py` `MediaProbe`). Sound-on-video and a lip-sync pack would use the same helpers.
- **Astrid:** the `vibecomfy.workflows` point becomes a thin mirror of VibeComfy's registry. An Astrid pack can still contribute, and that is forwarded to `register_workflows`. A native VibeComfy plugin (an entry point) shows up in Astrid on its own. Its distribution name and version are pinned in the engine manifest's `extra`, so a RunPod machine installs exactly the same plugin. `astrid packs extensions` lists both kinds.
- **h3_av (specific, a pack that depends on VibeComfy):** request schema v1 and v2, Character Swap, masks, static regions, the planner, continuation timing (5+17k grid, the 362→360 trim), the three workflow trios, and h3's use of the shared media helpers. It is installable for standalone VibeComfy (`pip install`, entry point) and through Astrid (a pack whose only content is that plugin and its pin).
- **Proof:**
  - standalone VibeComfy runs the h3 entry with `build` and `finalize` on a CPU fake;
  - Astrid runs the same plugin through `generate` on local, attached and the RunPod CPU fake;
  - the sound-on-video pack, written as a native VibeComfy plugin, uses the lifted mux helper;
  - a grep finds no h3 code in Astrid outside the pinned plugin reference.
- **Cross-repository:** VibeComfy changes land in VibeComfy first, then Astrid pins them. Releases follow the shared run contract.

## Goal and scope

- **Included, after Plan 32 T6b:**
  - run the extension registry check inside the install transaction;
  - add the owner-dependency rule;
  - add `astrid packs extensions` to list points, contributions and problems;
  - write the protocol docs;
  - prove it with a **second, non-h3 composite pack**: **sound on video**, which reuses the existing sound-effects template and adds a `finalize` that muxes the generated audio onto the source video.
- **Deferred:**
  - folding the remaining `pack.extensions.generation.*` keys (`features`, `modes`) into a point (Plan 32 T6 deletes the hard-coded h3 backend; nothing else needs the rest yet);
  - version ranges, priority fields or point inheritance;
  - per-contribution trust;
  - hot reload of Agent-side points;
  - unifying the App manifest with the Agent registry;
  - migrating `actions`, `ui` or `rendering` into points.
- **Undecided:** whether the App's closed contribution kinds join the protocol in this plan or a later one.

## What we build on

The protocol (`astrid/core/extensions`) and the three points Plan 32 creates. h3_av is the first contribution, made in Plan 32 T6b. The sound-on-video pack is the second: it exercises a ready root, entries, a media input and `finalize`, with no `build`, from a pack outside core (`merge-run/path-review/H3-GENERALIZATION.md` section 2). See the [Liquid Software vision](../../vision/pillars/liquid-software.md); exact starting identities are in [inputs.md](inputs.md).

## Sequence

After Plan 32 T6b: P1 (validation in the install transaction, plus the owner-dependency rule) and P2 (`astrid packs extensions`) in parallel, then P3 (docs) and P4 (the sound-on-video pack), then the review rounds. All of it is CPU only; P4's live run is [Plan 34](../34-real-gpu-proof/plan.md)'s. See [tasks.md](tasks.md).

## Completion

- A pack outside core installs through `astrid packs add`, and its contribution is validated before the swap. A broken contribution, or one without its owner dependency, is refused with a fix.
- `astrid packs extensions` lists points, contributions and problems.
- The sound-on-video pack produces a video with the generated audio, locally and through the RunPod CPU fake.
- The protocol and its three points are documented.
- **Not proven here:** real inference (Plan 34). Record any extension needs the sound-on-video pack does not cover. Destination and publication authority follow the shared [run contract](../../skills/astrid-dev-shared/run-contract.md); verify the intended `pre-main` destination at setup rather than assuming it.

## Read next

- [tasks.md](tasks.md): intended work and task-scoping boundary.
- [inputs.md](inputs.md): source identities, references, and setup requirements.
