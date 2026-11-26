# Tasks — One native timeline engine

[Plan](plan.md) · [Inputs](inputs.md)

**Draft task outline:** no implementation or dispatch authorized. Before dispatch, replace broad candidate scopes with exact permitted files, pinned source/dependency identities, real focused commands, route decisions and accepted review bounds. Each proof below is a required observable result, not an executed test.

**Task ids:** TE-1 onward. **Critical path:** TE-1 → TE-2 → RS1 → TE-3 → TE-4 → TE-5 → R. **Test inventory:** Runtime test_timeline_commit_{contract,acceptance,auth*,crash,history_reuse,restore*,closure*,film_fixture,port,execution}.py and tests/test_timeline_commit_cost.py; Agent SDK timeline tests and App timeline contracts/real save-render fixtures. Re-inventory exact names/lanes.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| TE-1 Freeze semantic oracle and edit corpus | N | Plan 100 timeline seam | Runtime/Agent/App contracts, real and synthetic fixtures | Exact command, revision, rounding, restore, denial, crash and renderer readback vectors; reference runs. | [ ] |
| TE-2 Design pure timeline kernel and transaction boundary | X | TE-1 | Rust crate API, typed command/result contract | No storage or provider coupling; review deterministic representation and authority, extension and migration semantics. | [ ] |
| RS1 Review stop — contract/ownership before implementation (proposed one round) | S | TE-2 | read-only | Independent critique of source, authority, parity/negative evidence and overlap; resolve findings before downstream tasks. | [ ] |
| TE-3 Implement native rules in reviewed slices | X | TE-2, RS1 | Rust timeline crate and differential vectors | Differential parity per operation, history/undo, nested timeline/opaque fields; planted rounding error fails. | [ ] |
| TE-4 Wire Python reference and TS/Python clients | X | TE-3 | Agent SDK provider adapter, Runtime commit seam, App SDK | Both clients commit through same runtime, no direct persistence; preview reconciliation and concurrency negative proof. | [ ] |
| TE-5 Measure installed real timeline and render parity | X | TE-4 | Heavy fixture, installed benchmarks and rendering readback | Compare accepted timing and correctness gates, repeated saves and crash/undo; exact crate and receipts for Plan 103. | [ ] |
| R Review rounds (proposed at most 3, owner confirmation pending) | S | all other tasks | read-only | Review exact integrated candidate, claims, tests, limits and retained authority per [run contract](../../agent/shared/run-contract.md#review-and-promotion-boundaries); findings become bounded rows. | [ ] |

Do not start product work, choose a release branch, rent hardware or migrate live user data from this outline. Reuse existing owner plans and do not weaken tests. Scope overlaps and exact proof commands must be resolved at review before dispatch.
