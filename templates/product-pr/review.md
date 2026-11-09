# Review submission

Use this concise summary in a **product repository PR**. A small bug can use its existing bug template. Link primary receipts rather than copying logs or adding another document.

**Related work:** Canonical Astrid-dev `plan.md` (project ID/task), or incident issue.

## Claim and change
- **Outcome and source:** What changed, retained implementation, candidate SHA and relevant Runtime/Agent/App/provider revisions
- **Other PRs:** Cross-repository dependencies, integration order and unresolved contracts

## Evidence and model provenance
- **Claim → check → actual result:** Named command/visual comparison, environment, exit/result and exact receipt; what a failed case does
- **Routes used:** Route (N, X, S or T) for each piece of research, planning, implementation and review, with a specific model name only where the run used one other than its route's. Or `Unknown — reason`. See [route recording](https://github.com/banodoco/astrid-dev/blob/main/docs/contribution-workflow.md#record-routes-as-work-happens).
- **Remaining uncertainty:** Unrun scenarios, first failure/regression, recovery and source provenance limits

## Review decision
- **Request:** Review implementation / integrate a named candidate / qualify the combined result
- **Risks:** Data, security, compatibility, migrations, rollback, cost and unsupported cases—or explicitly none found within the tested scope

The reviewer independently examines actual code and evidence. A CI pass or review label is not a merge or deployment authorization. The final Astrid-dev completion assessment points to all relevant PRs.
