# Tasks — Provider-independent agent infrastructure

[Plan](plan.md) · [Inputs](inputs.md)

**Draft task outline:** no implementation or dispatch authorized. Before dispatch, replace broad candidate scopes with exact permitted files, pinned source/dependency identities, real focused commands, route decisions and accepted review bounds. Each proof below is a required observable result, not an executed test.

**Task ids:** AG-1 onward. **Critical path:** AG-1 → AG-2 → RS1 → AG-3 → AG-4 → AG-5 → R. **Test inventory:** Agent astrid/chat/acpProcessHost.test.ts, astrid-project-chat/runtime/shared-session/local-agent tests, Runtime test_profile_services.py and task/idempotency/custody tests, App agent chat/runtime session contracts. Re-inventory exact tuple.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| AG-1 Trace session and task ownership | N | Plan 100 contract | Agent chat/ACP and Runtime read-only inventory | Map durable/ephemeral data, provider identity, context scopes, receipts and failure transitions. | [ ] |
| AG-2 Define portable checkpoint and adapter contract | X | AG-1 | Session/capability schemas, authorization and retention design | Explicit provider limits, revocation and resume semantics; negative fixture designs. | [ ] |
| RS1 Review stop — contract/ownership before implementation (proposed one round) | S | AG-2 | read-only | Independent critique of source, authority, parity/negative evidence and overlap; resolve findings before downstream tasks. | [ ] |
| AG-3 Implement independent provider adapters and recovery | X | AG-2, RS1 | Agent adapters, Runtime session interfaces | Two distinct adapters; admitted work survives agent loss or safely settles; no duplicate effects. | [ ] |
| AG-4 Integrate native session authority and UI | X | AG-3, Plan 103 | Rust session records, existing ACP and App client adapters | Native headless session records; scoped reconnect, restart, revocation and editor readback. | [ ] |
| AG-5 Qualify real handoff and failure cases | N | AG-4 | Installed provider journeys, controlled CPU fixture | Real project handoff and replacement proof, provider portability limits and no unintended spend. | [ ] |
| R Review rounds (proposed at most 3, owner confirmation pending) | S | all other tasks | read-only | Review exact integrated candidate, claims, tests, limits and retained authority per [run contract](../../agent/shared/run-contract.md#review-and-promotion-boundaries); findings become bounded rows. | [ ] |

Do not start product work, choose a release branch, rent hardware or migrate live user data from this outline. Reuse existing owner plans and do not weaken tests. Scope overlaps and exact proof commands must be resolved at review before dispatch.
