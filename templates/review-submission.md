# Review submission

Use this compact summary in a **product repository PR**. A bug PR may use its existing bug template instead. Link real observations; omit irrelevant sections rather than creating empty evidence paperwork.

**Related work:** Link the Astrid-dev project `plan.md` or incident issue. For project work, identify the project ID and the task/outcome.

## Claim and change
- **What changed and why:** The user-visible behavior and how this builds on retained work.
- **Exact source:** This PR/head SHA; any required Runtime/Agent/App/provider revisions and cross-repository dependencies.
- **Other PRs:** Links, sequencing and unresolved interfaces, if applicable.

## Evidence
- **Claim → check → observed result:** Name the focused commands, environment, test artifacts or reproducible manual demonstration and actual outcomes.
- **Negative and recovery paths:** What fails safely and what remains untested.
- **Previous failure or regression:** Original failing case and how it now behaves, if applicable.

## Review decision
- **Requested:** Review this implementation / Integrate into named branch / Qualify the combined candidate (choose one).
- **Remaining risks:** Data safety, security, compatibility, migration, rollback, costs and unsupported cases—or explicitly none found within the tested scope.

The reviewer examines the code and actual evidence, not just this summary. CI success alone does not authorize promotion or deployment. The final project completion assessment lives in Astrid-dev.
