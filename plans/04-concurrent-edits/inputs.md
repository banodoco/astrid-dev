# Inputs: refined concurrent editing

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code and branch policy

The following are retained historical donor/checkpoint commits, not live bases or proof of current target state. Repository URLs, refs, dirty state, custody, and live starting SHAs were not recorded; identify each at execution.

| Repository | Historical retained input | Starting identity | Candidate / destination |
|---|---|---|---|
| Agent | `4f111c2153184a73a5ca333a16f4b9a69a3313f1` | Branch and current SHA TBD | Fresh isolated candidate; promote reviewed head to `pre-main` |
| App | `438159b030cd3b0b81653415f1018f9a1349f0c5` | Branch and current SHA TBD | Fresh isolated candidate; promote reviewed head to `pre-main` |
| Runtime | `33e9195a8ac57c4ba61f372ef6f25139c37eaa97` | Branch and current SHA TBD | Fresh isolated candidate; promote reviewed head to `pre-main` |

The integration consumes the exact Agent/App/Runtime tuple promoted by Plan 02 integration (consistent generation), then the retained CE work. The concrete base is that promoted tuple plus then-current destination refs; freeze actual current `pre-main` heads when integration starts. The audit did not freeze Plan 04's merge base or target heads. Do not reuse historical `lane/M-GPU/integrated`; use fresh isolated candidate branches and promote the exact independently reviewed heads. Follow the [shared run contract](../../skills/astrid-dev-shared/run-contract.md) and the product repositories' actual branch/release controls for moved targets and publication authority.

## References and evidence

| Source | What it establishes | Limits / missing information |
|---|---|---|
| Historical App repair findings | Audit reports App repair head `438159b030cd3b0b81653415f1018f9a1349f0c5` passed the original eight hosted cases plus migration/owner and scope checks, with zero blocking items. | Historical report, not a fresh run. It explicitly says Agent SDK evidence does not replace independent final Agent/App/Runtime tuple acceptance. Full logs and original card corpus are not bundled. |
| Historical CE acceptance notes | These are the named source records for acceptance scope and retained evidence; the original plan records seven SDK nodes, eight hosted cases, and 351 prior SDK passes. | Detailed source records are not present here. Reuse 351 SDK passes only for unchanged internals; they do not prove a newly composed tuple. Recover the original documents/evidence at setup where exact decisions are needed. |
| CE-0 and CE-LIMIT | Named prerequisites; CE-LIMIT has an existing explicit check. | Their definitions, evidence, and CE-LIMIT selector were not supplied. Recover exact records and selector; do not infer or invent them. |

The SDK selectors and hosted wrapper requirements are recorded in [CE-FINAL](tasks.md#ce-final). Historical SHAs and observations are not current source identities and cannot be used to claim future candidate acceptance.

## Constraints

Execution requires the initiative's explicit start and the accepted run controls. Preserve the existing END review scope, stage, and remaining-round budget; the migration source does not specify their exact values. No full SDK/UI suite. Publication follows the existing project and [shared run contract](../../skills/astrid-dev-shared/run-contract.md); this plan adds no authorization or review stage.
