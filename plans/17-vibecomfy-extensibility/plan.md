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
- `vibecomfy.workflows` (templates, an optional `register`, and an optional `finalize`; h3_av becomes one composite pack with one contribution).

Environment setup is the `align` half of the engine point. It is generic in core and engine-specific in each contribution.

## Goal and scope

- **Included, after Plan 32 T6:**
  - run the extension registry check inside the install transaction;
  - add the owner-dependency rule;
  - add `astrid packs extensions` to list points, contributions and problems;
  - write the protocol docs;
  - prove it with a **second, non-h3 composite pack** (a workflow plus a timeline effect);
  - fold `pack.extensions.generation.*` into a point.
- **Deferred:**
  - version ranges, priority fields or point inheritance;
  - per-contribution trust;
  - hot reload of Agent-side points;
  - unifying the App manifest with the Agent registry;
  - migrating `actions`, `ui` or `rendering` into points.
- **Undecided:** the exact second composite pack, and whether the App's closed contribution kinds join the protocol in this plan or a later one.

## What we build on

H3_AV is a concrete example, not evidence of particular APIs or missing capabilities. First identify its source and the existing VibeComfy workflow and pack extension points. See the [Liquid Software vision](../../vision/pillars/liquid-software.md); exact starting identities are in [inputs.md](inputs.md).

## Sequence

Map existing inputs, outputs, composition, and pack boundaries; then improve only the primitives needed for H3_AV to be composable and customizable; document and prove that path. The [task outline](tasks.md) records what remains to be scoped.

## Completion

H3_AV demonstrates the documented extension path, users can customize and compose the relevant workflow without a core fork, and focused evidence covers the resulting contracts. Record limitations and extension needs the example does not cover. Destination and publication authority follow the shared [run contract](../../skills/astrid-dev-shared/run-contract.md); verify the intended `pre-main` destination at setup rather than assuming it.

## Read next

- [tasks.md](tasks.md): intended work and task-scoping boundary.
- [inputs.md](inputs.md): source identities, references, and setup requirements.
