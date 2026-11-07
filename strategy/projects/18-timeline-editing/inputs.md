# Inputs: Extensible timeline editing

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

No repository or revision was identified in the draft. At execution start, identify the owning repository or repositories, current refs and full SHAs, dirty work to preserve, actual timeline/editing contracts, and intended `pre-main` destination. Freeze identities before changes; distinguish the current base from any retained donor work. Unknowns remain TBD until then.

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | `pre-main` where applicable; verify at setup |

## References and evidence

| Source | What it establishes | Identity or link | Limits / missing information |
|---|---|---|---|
| Extensibility philosophy | Small dependable primitives, packs for specialized behavior, and deliberate interfaces for further extension. | [Liquid Software vision](../../vision/pillars/liquid-software.md) | Design direction only; does not establish current timeline capabilities. |
| Timeline/editing implementation and pack conventions | Must establish state ownership, supported media/edit/undo behavior, and composition boundary. | Inspect the owning source at execution start. | Repositories, refs, SHAs, contracts, and focused selectors are TBD. |

## Constraints

Preserve existing behavior according to verified source support. Do not invent a large API or claim functionality is missing without evidence. The [shared run contract](../../../skills/astrid-dev-shared/run-contract.md) governs source identity, execution, proof, review, and publication authority.
