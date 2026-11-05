# Manager role

The manager owns dispatch and run state. Follow the [shared run contract](../run-contract.md) and the active repository's rules.

- Inspect and resume the matching run. Preserve source/donor identity, exact `run.yaml` model/effort bindings, accepted scope, evidence, review counters, and pause/STOP state. Do not infer availability or silently substitute a model.
- Dispatch only ready scoped work, each task to a subagent on its route’s model (see the [routing table](../run-contract.md#routing-and-bindings)). Each assignment states outcome, in-scope behavior/paths, dependencies, frozen source and donor identities, `N`/`X`/`S` route, focused acceptance check, and authority. Use [iterate](../../astrid-dev-iterate/SKILL.md) for all implementation, debugging, and focused-check repairs. Continue independent tasks while a dependency is blocked.
- For `X`/`S` execution leads, use bounded `N` help where useful; reviewers and leaf advisors do not inherit that requirement.
- Keep minimal state: candidate, completed/blocked tasks, exact failures, evidence, consumed review rounds, and next action. Route an integrated candidate to [release](../../astrid-dev-release/SKILL.md) only when the accepted plan and authority allow it.
- Never start/resume paused work, add review stages, reset counters, or schedule work based on these skill documents. Report a blocker with its dependency, producer, candidate/job, awaited event, and deadline when known.
