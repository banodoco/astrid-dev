# Tasks — One native Astrid application

[Plan](plan.md) · [Inputs](inputs.md)

**Draft task outline:** no implementation or dispatch authorized. Before dispatch, replace broad candidate scopes with exact permitted files, pinned source/dependency identities, real focused commands, route decisions and accepted review bounds. Each proof below is a required observable result, not an executed test.

**Task ids:** NA-1 onward. **Critical path:** NA-1 → NA-2/NA-3 → RS1 → NA-4 → NA-5 → R. **Test inventory:** App installer bootstrap/manifest/local-update/launcher tests, Runtime test_portable_lifecycle.py/test_runtime_upgrade.py/test_workspace_adopt.py, Agent installer and Windows install/update journeys, Pinokio native qualifications. Re-inventory on selected tuple.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| NA-1 Inventory installation, update and OS ownership paths | N | — | App/Agent/Runtime/Pinokio read-only; plan | Exact call flow and one owner per resource; reconcile prior plans. | [ ] |
| NA-2 Native bootstrap and verified manifest prototype | X | NA-1 | Runtime native bootstrap package; isolated root | Starts with Python/Node absent, downloads/verifies pinned fixture; interrupted download resumes. | [ ] |
| NA-3 Same frontend locally and desktop renderer spike | X | NA-1 | App production bundle/local server and shell prototype | Hosted/local/dev paths use same project; three-OS media and origin test; documented shell choice. | [ ] |
| RS1 Review stop — contract/ownership before implementation (proposed one round) | S | NA-2, NA-3; Plan 100 lifecycle design | read-only | Independent critique of source, authority, parity/negative evidence and overlap; resolve findings before downstream tasks. | [ ] |
| NA-4 Implement single controller and recovery transfer | X | NA-2, Plan 100 lifecycle seam, RS1 | Native controller, installer/launcher adapters, service registration | One owner; corrupt environment recovery, duplicate-owner refusal, transactional adoption/rollback; no direct DB access. | [ ] |
| NA-5 Qualify distribution and retire duplicate paths | X | NA-3, NA-4 | Platform packaging, manifests, selected product/Pinokio journeys | Signed/verified artifacts; installed three-OS journeys, external ownership, data preservation, repair and offline proof. | [ ] |
| R Review rounds (proposed at most 3, owner confirmation pending) | S | all other tasks | read-only | Review exact integrated candidate, claims, tests, limits and retained authority per [run contract](../../agent/shared/run-contract.md#review-and-promotion-boundaries); findings become bounded rows. | [ ] |

Do not start product work, choose a release branch, rent hardware or migrate live user data from this outline. Reuse existing owner plans and do not weaken tests. Scope overlaps and exact proof commands must be resolved at review before dispatch.
