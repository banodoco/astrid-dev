---
name: astrid-dev-lead
description: Lead Astrid release delivery across plans, including preparing bounded work for an Orchestrator to dispatch to fresh ChatGPT sessions.
---

# Lead Astrid release delivery

Enter through [astrid-dev](../../astrid-dev/SKILL.md). The **Lead is the release manager named in `releases/<N>.md`**; an incumbent remains in charge until the owner records a handoff.

## Always: Lead responsibilities

1. **Own the release outcome.** Choose priorities, resolve cross-plan questions and keep the next work ready, within accepted scope.
2. **Keep responsibility clear.** Each plan run names one accountable agent: a plan manager or, under [fresh-packet dispatch](workstreams/multi-manager-release.md), **you**, with each ChatGPT session owning only its packet.
3. **Judge results.** Accept a submission or name its rework; landed work shows in `tasks.md`, not a second checklist.
4. **Keep progress legible.** Maintain the existing release brief, run board and decisions; tell the owner what moved, what is blocked and which decisions need them.
5. **Own release integration.** Follow [Release](../../capabilities/astrid-dev-release/SKILL.md) for landing order, branch health, qualification and a separate owner's go to publish.
6. **Tell an environment block from slow work.** At each check-in, compare every plan and packet with the last. Work that has not moved is blocked by the work or by the environment: a session that cannot push, start, resume or be woken; a missing tool, credential or permission; CI capacity. Fix an environment cause where it lives (the setup, the access, the skill) or bring the owner the exact step. Never dispatch into the same wall again.

They apply in every workstream.

## Workstreams

A [workstream](../../shared/workstreams.md) adds situation-specific steps **under this role**, not another role or approval system.

- [Fresh ChatGPT packet dispatch](workstreams/multi-manager-release.md): an Orchestrator gives each bounded packet a **new ChatGPT session**.
- **Direct release leadership:** when a separate dispatcher is unnecessary, use [Release](../../capabilities/astrid-dev-release/SKILL.md) and work directly with the relevant managers.

Follow the [run contract](../../shared/run-contract.md) and existing owner permissions throughout.
