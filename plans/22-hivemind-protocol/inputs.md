# Inputs — Hivemind protocol

[Plan](plan.md) · [Tasks](tasks.md)

## Authoritative design input (proposed, not yet verified)

- [**The Hivemind protocol, proven on Banodoco Hivemind**](../../visions/principles/collective-intelligence/references/hivemind-protocol-proposal.md), user-supplied Markdown dated **2026-10-29**. Defines Entry/Link/Scope/Access; `cites/carries/supports/opposes/qualifies/supersedes`; `find/inspect/contribute`; local/private and public datasets, custody, conditions, evidence, agent receipts, editorial grants, and suggested migration sequence. Treat all reported corpus counts, tests, migration and exposure assertions as **claims to verify**, not established facts.
- [Collective Intelligence principle](../../visions/principles/collective-intelligence/principle.md) and [current-state bridge](../../visions/principles/collective-intelligence/bridge.md).
- [Agent learning-loop reference](../../visions/principles/collective-intelligence/references/agent-learning-loop.md) for the desired end-user experience, not protocol-level authority.

## Current source anchors to re-verify at execution

- [Banodoco Hivemind](https://github.com/banodoco/hivemind), sampled **2026-11-06**, `main` `2efd9ce7e17e19f3e7820374ddfd566cb0b4adbc`: [README](https://github.com/banodoco/hivemind/blob/2efd9ce7e17e19f3e7820374ddfd566cb0b4adbc/README.md), [DESIGN](https://github.com/banodoco/hivemind/blob/2efd9ce7e17e19f3e7820374ddfd566cb0b4adbc/DESIGN.md), `schema/038_knowledge_model.sql`, `schema/039_knowledge_model_delivery.sql`, and read/contribute executors. These describe **current** `resources/resource_revisions` (not automatically the proposed protocol).
- [Astrid Agent](https://github.com/banodoco/astrid-agent): pack and skill discovery, but no assumption that `find/inspect/contribute` are already agent-native.
- [Astrid Runtime](https://github.com/banodoco/astrid-runtime): its project/task/artifact ownership must not be duplicated inside a knowledge dataset.
- [Pinned Hivemind source-map](../../visions/principles/collective-intelligence/references/source-map.md) records the observed differences.

## Missing before execution

Owner/authorization; fresh exact source repo/ref/SHA and any retained donors/dirty changes; local dataset storage/security design; repo-side plan reconciliation; chosen API compatibility strategy; privacy/consent/legal decisions for captured community sources; narrowly scoped test selectors and evaluation fixtures. Intended destination is set by the actual owner repository rules, **not assumed to be Astrid Agent's `pre-main`**.
