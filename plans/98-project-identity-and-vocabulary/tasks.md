# Tasks — One project vocabulary and identity

[Plan](plan.md) · [Inputs](inputs.md)

Draft task outline; all rows unchecked. Refresh exact source symbols, test selectors, reviewed owner decisions, permissions and integration base at dispatch. This proposal grants no execution authority.

**Task ids:** PI-1–PI-7, RS1, R. **Critical path:** PI-1 → RS1 → PI-2 → PI-3/PI-4/PI-5 → PI-6 → PI-7 → R. **Test inventory:** scripts/test_records.py, test_project_contract.py, test_checks.py, test_views.py, test_golden.py, test_pack_shape.py, test_check_completion.py, test_check_project_planning.py, test_check_gap_boundaries.py, test_release_branches.py, test_release_issues.py, test_boards.py, test_issue_intake.py, test_review_intake.py, test_claim_project.py, test_auto_merge.py, test_export_public_vision.py and final Plan 72/73/97 suites; actual App vision:check.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| PI-1 Inventory identities, references, active writers and compatibility | X | Plan 97 | Read-only tree, active runs, workflows, consumers and historical records; evidence | One-to-one ID/path inventory, exact baseline, old URLs/labels/branches, candidate overlap and rollback plan | [ ] |
| RS1 Review migration and stable identity contract | S | PI-1 | read-only | Independent source/authority/compatibility review, findings RS1.n | [ ] |
| PI-2 Canonical project resolver and narrow legacy read policy | S | RS1 | Project/record identity and path resolution, typed relationship adapters; agreed compatibility boundary | IDs preserved, old/new references resolve same entity, unknown/duplicates/collisions fail, no duplicate source | [ ] |
| PI-3 Migrate authored project packs and templates | N | PI-2 | Canonical project paths, template names, active authored links; no historical receipt rewrites | One-to-one file/content inventory, template and task parity, old links pinned/redirected only where approved | [ ] |
| PI-4 Migrate checks, views and public feed consumers | X | PI-2 | Validation, catalogue/strategy/views/export readers and fixtures; App contract read-only unless approved | Same logical records and existing gate verdicts, approved path deltas only, no lost or duplicate views, App consumer checks | [ ] |
| PI-5 Migrate role/skill docs, issue/release routing and trusted automation | S | PI-2 | Final agent docs, contribution/issue/PR templates, board/release/label readers and bots; protected workflow boundary | New project routing; legacy active branches/labels and immutable release evidence still resolve; no privileged untrusted code or weakened protection | [ ] |
| PI-6 Assemble candidate and rehearse cutover/rollback | S | PI-3, PI-4, PI-5 | Integrated exact candidate, compatibility and owner-approved run migration plan | No live run mutated; old/new consumers and aliases behave as reviewed; full docs and vision-consumer CI, rollback rehearsal | [ ] |
| PI-7 Qualified handoff to Otto | X | PI-6 | Evidence, identity/extension guide and source ownership map | Exact integrated revisions and documented allowed deltas/legacy limits; independent new project fixture and historical reference verification | [ ] |
| R Final independent review (one proposed round) | S | All tasks | read-only | Run-contract review, findings R1.n; separate integration go | [ ] |

### Dispatch boundaries

Do not use a blind search/replace or rename protected refs. PI-3/4/5 are parallel only on disjoint ownership after PI-2; one integrator owns shared files and final workflow cutover. Preserve existing required checks, trusted-base execution and project metadata. Do not alter another manager's active branch or release membership. Test migration against final integrated prerequisite source, including the actual App schema; any semantic change requires separate owner decision.
