# Tasks — Astrid Marketing organisation

[Plan](plan.md) · [Inputs](inputs.md)

Draft task list; all rows unchecked. It grants no execution authority. Re-check against the Otto tag's actual contract at dispatch.

**Task ids:** `MK-0` to `MK-7`, `R`. **Critical path:** Otto v0.1.0 and MK-0 → MK-1 → MK-2 → MK-3 → MK-5 → MK-6 → MK-7 → R. MK-4 runs beside MK-3. MK-0 can finish at any time before MK-1. **Test inventory:** none exists yet; Otto's own tests at the pinned tag are the framework's proof, and this workspace's `otto check` on CI is its own. No product, GPU or release CI.

**Lanes.** As in [Plan 95](../95-composable-agentic-workspaces/tasks.md): *orchestrator* cards need the owner, repository administration, or a review verdict; *packet* cards write files in one fresh session in the route's mode, and the orchestrator runs their proof.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **MK-0** Gather the owner's decisions D2–D4 | N, orchestrator | — | Read-only, plus the answers recorded in [inputs](inputs.md#owner-decisions) | D2 (strategy, brand and audience sources; the two proof projects and the campaign), D3 (repository name and visibility; permitted product sources) and D4 (external permissions: none by default) each carry a date and the owner's choice | [ ] |
| **MK-1** Create the repository and pin Otto | N, orchestrator | Otto v0.1.0; MK-0; the owner's go for the repository | The repository D3 names; `otto.toml` stub pinning `v0.1.0`; CI running `otto check` | A clean clone installs the pinned Otto and `otto check` runs on the empty workspace; the pin names the tag's commit | [ ] |
| **MK-2** Design the workspace with Otto's stand-up playbook | X, packet | MK-1 | `otto.toml` (slug IDs, namespace, paths), record kinds and relations, `pipelines/strategy.toml` and `pipelines/intake.toml`, the campaign document shape, `strategy.md`, and the authority policy (`agent/authority.md`) | Each playbook step is done or marked not needed, with a reason; no record kind beyond goal, project, campaign, issue and idea; product claims cite Dev by revision; the authority policy defaults to no outbound action. Gaps in the playbook are filed as Otto issues | [ ] |
| **MK-3** Configure records, templates, pipelines, views and intake | N, packet | MK-2 | Project catalogue and campaign views, Otto's `standard` and `loop` templates, issue forms in `.github/ISSUE_TEMPLATE/`, planted-violation fixtures in `tests/` | Orchestrator: `otto check` passes; it fails on a planted invalid link, unknown template, campaign including a goal, and project with no goal in `strategy`; an ungrouped project passes | [ ] |
| **MK-4** Marketing overlay and local skills | X, packet; then a `T` pass on the overlay's voice | MK-2 | `agent/` documents linking Otto's guidance at the pinned tag and adding only create, critique, campaign coordination and publication authority, `skill: true` where they are skills | `otto skills build` and `check` pass; installing into a temporary destination beside `otto-*` packages clashes with none; no Otto rule is restated (each overlay rule is either Marketing-only or a link); a request to publish without approval is refused by the documented procedure | [ ] |
| **MK-5** Run a small real standard project | N, packet | MK-3, MK-4 | The owner-selected project from D2 and its draft or review deliverable | Its agreed tasks are done with real proof; claims verified against cited sources; the deliverable is approved or held, never published without approval | [ ] |
| **MK-6** Run a bounded loop project and coordinate the campaign | X, packet | MK-5 | The owner-selected loop project, its rounds document and the campaign document | A real baseline and method, at least one round with an observation and a stop or next decision; both projects in the campaign with one task list each; `otto pipeline show strategy <campaign>` lists them; no forced publication | [ ] |
| **MK-7** Fresh-agent trial and handoff | X, orchestrator (arranges a fresh, uncoached agent) | MK-6 | A throwaway branch for the trial; a handoff note in the repository | With only the repository, the agent finds the strategy, creates a project from an idea, and adds a skill and a pipeline or template without changing Otto or Dev; a recorded learning informs a next action; limits and next decisions are listed | [ ] |
| **R** Final review (one round) | S, orchestrator (`completion_reviewer`) | All tasks | Read-only | Plan [Completion](plan.md#completion) in full: setup proof, permission isolation, no unsupported impact claims; findings become `R1.<n>` rows below | [ ] |

### Dispatch boundaries

Plan 95's Marketing fixture is a test of Otto, not a pilot: do not repeat it here, and do not edit Otto or Dev from this plan. External publication, contact and spend are not needed to finish and each needs separate approval. No private operational data in this public planning repository.
