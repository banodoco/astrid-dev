# Inputs: VibeComfy extensibility with H3_AV

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

Repository ownership, starting branch and SHA, retained dirty work, and candidate branch are **TBD at execution start**. Identify and freeze the owning repository or repositories and current refs before source changes. Historical plan text does not establish a live execution base. Verify the intended `pre-main` destination then; do not assume branches.

| Input | Why it matters | Identity / limits |
|---|---|---|
| Current VibeComfy implementation | Reveals existing workflow primitives and extension contracts to reuse. | Owning source and exact identity TBD at setup. |
| H3_AV | User-provided abstraction over MiniMax H3 workflows in VibeComfy; example for customization and composition. | Owning pack/source and exact identity TBD at setup; do not infer APIs or gaps. |

## References and evidence

- [Liquid Software vision](../../vision/pillars/liquid-software.md) sets the design direction.
- The draft identifies H3_AV and current VibeComfy code as inputs but supplies no source links, SHAs, or recorded proof. Recover them at setup.
- No generation evidence is established. Scope any real-generation proof and authorized compute requirements before execution; this planning effort runs no GPU work.

## Constraints

Follow repository [Astrid development skill](../../skills/astrid-dev/SKILL.md) and the shared [run contract](../../skills/astrid-dev-shared/run-contract.md) for execution, resources, routes, and publication. Confirm source identities and destination at setup.
