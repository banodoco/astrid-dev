# Tasks — A language-independent foundation

[Plan](plan.md) · [Inputs](inputs.md)

**Draft task outline:** no implementation or dispatch authorized. Before dispatch, replace broad candidate scopes with exact permitted files, pinned source/dependency identities, real focused commands, route decisions and accepted review bounds. Each proof below is a required observable result, not an executed test.

**Task ids:** NF-1 onward. **Critical path:** NF-1 → NF-2/NF-3 → RS1 → NF-4 → NF-5 → R. **Test inventory:** Runtime tests/test_a5_runtime_conformance.py, tests/test_native_custody.py, tests/test_installed_pack_custody_spawn.py, tests/test_profile_services.py, timeline_commit_contract/port tests; Agent generic host/custody and installed-origin tests; App generated client conformance. Re-inventory at pin.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| NF-1 Pin sources and map dependencies/authority | N | — | Runtime, Agent, App, Pinokio read-only; Dev inventory | Every cross-language seam has caller, owner, protocol, failure behavior, evidence and remove/reuse disposition. | [ ] |
| NF-2 Capture black-box reference and negative cases | X | NF-1 | Runtime contract/conformance and integration fixtures | Run named reference client/worker cases and planted unauthorized/stale/duplicate failures; exact tuple and outputs. | [ ] |
| NF-3 Design worker, lifecycle and timeline boundaries | X | NF-1 | Contract and design; no private state migration | Versioned schemas, ownership, native handle ABI and batched edit seam; backward compatibility matrix. | [ ] |
| RS1 Review stop — contract/ownership before implementation (proposed one round) | S | NF-2, NF-3 | read-only | Independent critique of source, authority, parity/negative evidence and overlap; resolve findings before downstream tasks. | [ ] |
| NF-4 Decouple private authority imports | X | NF-2, NF-3, RS1 | Runtime/Agent worker support and call sites, generated clients | Independent worker succeeds; denied or stale cases fail closed; guard catches a planted private import. | [ ] |
| NF-5 Independent client/worker and parity handoff | N | NF-4 | Conformance runner, consumer example and docs | Independent client/worker complete actual task with matching receipts; pin corpus for Plan 103. | [ ] |
| R Review rounds (proposed at most 3, owner confirmation pending) | S | all other tasks | read-only | Review exact integrated candidate, claims, tests, limits and retained authority per [run contract](../../agent/shared/run-contract.md#review-and-promotion-boundaries); findings become bounded rows. | [ ] |

Do not start product work, choose a release branch, rent hardware or migrate live user data from this outline. Reuse existing owner plans and do not weaken tests. Scope overlaps and exact proof commands must be resolved at review before dispatch.
