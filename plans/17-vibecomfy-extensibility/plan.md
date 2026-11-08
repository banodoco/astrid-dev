# VibeComfy plugins: document and prove the extension path

**Vision gaps:** [Composable capabilities](../../vision/gaps/LS-003-full-stack-contributions.md) (primary) · [Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting).

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

Make it easier for people and their agents to build and share creative tools on VibeComfy. Use H3_AV, a user-provided abstraction over MiniMax H3 workflows, to improve existing extension primitives and demonstrate customization and composition without forking core. This remains a draft; queue status, owner, and estimate are in the [project queue](../../README.md).

## Direction (8 Nov 2026)

An independent review (merge-run desk, `merge-run/path-review/H3-AS-VIBECOMFY-EXTENSION.md`) found that VibeComfy's existing `vibecomfy.plugins` mechanism is the extension point. [Plan 32](../32-generation-placement-targets/plan.md) (T2, T6) moves h3_av onto it as a VibeComfy plugin entry, with no h3 code on Astrid's path. After Plan 32 T6, this plan documents the plugin contract (templates, operations, routes, the per-entry `finalize` step) and proves it with a **second, non-h3 plugin**. This direction is pending the owner's scope agreement.

**Open technical choice:** where the h3 plugin lives (a VibeComfy plugin package, or a pack that registers one). Licence questions are out of scope (owner, 8 Nov 2026).

## Goal and scope

- **Included:** inspect current VibeComfy code and H3_AV; reuse existing concepts; clarify and improve relevant inputs, outputs, and composition boundaries; support workflow extension and customization without a core fork; deliver one focused example and proof.
- **Deferred:** broad workflow redesign, unrelated pack work, and GPU execution during this planning effort.
- **Undecided:** implementation tasks, exact checks, and any authorized real-generation proof, to be scoped from source.

## What we build on

H3_AV is a concrete example, not evidence of particular APIs or missing capabilities. First identify its source and the existing VibeComfy workflow and pack extension points. See the [Liquid Software vision](../../vision/pillars/liquid-software.md); exact starting identities are in [inputs.md](inputs.md).

## Sequence

Map existing inputs, outputs, composition, and pack boundaries; then improve only the primitives needed for H3_AV to be composable and customizable; document and prove that path. The [task outline](tasks.md) records what remains to be scoped.

## Completion

H3_AV demonstrates the documented extension path, users can customize and compose the relevant workflow without a core fork, and focused evidence covers the resulting contracts. Record limitations and extension needs the example does not cover. Destination and publication authority follow the shared [run contract](../../skills/astrid-dev-shared/run-contract.md); verify the intended `pre-main` destination at setup rather than assuming it.

## Read next

- [tasks.md](tasks.md): intended work and task-scoping boundary.
- [inputs.md](inputs.md): source identities, references, and setup requirements.
