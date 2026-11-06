# VibeComfy extensibility with H3_AV

**Vision gaps:** [Composable capabilities](../../visions/gaps/LS-003-full-stack-contributions.md) (primary).

**Start here:** read [AGENTS.md](../../AGENTS.md), choose a workflow in the [skills guide](../../skills/README.md), follow the [run contract](../../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../../docs/glossary.md).

Make it easier for people and their agents to build and share creative tools on VibeComfy. Use H3_AV, a user-provided abstraction over MiniMax H3 workflows, to improve existing extension primitives and demonstrate customization and composition without forking core. This remains a draft; queue status, owner, and estimate are in the [project queue](../../README.md).

## Goal and scope

- **Included:** inspect current VibeComfy code and H3_AV; reuse existing concepts; clarify and improve relevant inputs, outputs, and composition boundaries; support workflow extension and customization without a core fork; deliver one focused example and proof.
- **Deferred:** broad workflow redesign, unrelated pack work, and GPU execution during this planning effort.
- **Undecided:** implementation tasks, exact checks, and any authorized real-generation proof, to be scoped from source.

## What we build on

H3_AV is a concrete example, not evidence of particular APIs or missing capabilities. First identify its source and the existing VibeComfy workflow and pack extension points. See the [extensibility philosophy](../../docs/extensibility-philosophy.md); exact starting identities are in [inputs.md](inputs.md).

## Sequence

Map existing inputs, outputs, composition, and pack boundaries; then improve only the primitives needed for H3_AV to be composable and customizable; document and prove that path. The [task outline](tasks.md) records what remains to be scoped.

## Completion

H3_AV demonstrates the documented extension path, users can customize and compose the relevant workflow without a core fork, and focused evidence covers the resulting contracts. Record limitations and extension needs the example does not cover. Destination and publication authority follow the shared [run contract](../../skills/astrid-dev-shared/run-contract.md); verify the intended `pre-main` destination at setup rather than assuming it.

## Read next

- [tasks.md](tasks.md): intended work and task-scoping boundary.
- [inputs.md](inputs.md): source identities, references, and setup requirements.
