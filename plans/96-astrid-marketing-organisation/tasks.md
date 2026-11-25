# Tasks — Astrid Marketing organisation

[Plan](plan.md) · [Inputs](inputs.md)

Draft task list; all rows unchecked. It grants no execution authority. Re-check against the Otto tag's actual contract at dispatch.

**Task ids:** `MK-0` to `MK-7`, `R`. **Critical path:** Otto v0.1.0 and MK-0 → MK-1 → MK-2 → MK-3 and MK-4 → MK-5. MK-4 runs beside MK-3. **Test inventory:** none exists yet; Otto's own tests at the pinned tag are the framework's proof, and this workspace's `otto check` on CI is its own. No product, GPU or release CI.

**Lanes.** As in [Plan 95](../95-composable-agentic-workspaces/tasks.md): *orchestrator* cards need the owner, repository administration, or a review verdict; *packet* cards write files in one fresh session in the route's mode, and the orchestrator runs their proof.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **MK-0** Gather the owner's decisions D2–D5 | N, orchestrator | — | Read-only, plus the answers recorded in [inputs](inputs.md#owner-decisions) | D2 to D5 each carry a date and the owner's choice | [x] Done 25 November 2026: one project (Reddit announcement videos), private `banodoco/astrid-marketing`, no external action, no review budget |
| **MK-1** Create the repository and pin Otto | N, orchestrator | Otto v0.1.0; MK-0; the repository created empty by the owner or an organisation admin | `banodoco/astrid-marketing` (private); `otto.toml` stub pinning `v0.1.0`; CI running `otto check` | A clean clone installs the pinned Otto and `otto check` runs on the empty workspace; the pin names the tag's commit | [ ] |
| **MK-2** Design the workspace with Otto's stand-up playbook | X, packet | MK-1 | `otto.toml` (slug IDs, namespace, paths), record kinds and relations, `pipelines/strategy.toml` (goal → project), `strategy.md` (audience: Reddit users; brand and voice by reference to the pinned `poms_packs` skill, unstated fields left empty), and the authority policy (`agent/authority.md`) | Each playbook step is done or marked not needed, with a reason; no record kind beyond goal, project, issue and idea; product claims cite Dev by revision; the authority policy defaults to no outbound action. Gaps in the playbook are filed as Otto issues | [ ] |
| **MK-3** Configure records, templates, pipelines, views and intake | N, packet | MK-2 | Project catalogue view, Otto's `standard` template, issue forms in `.github/ISSUE_TEMPLATE/`, planted-violation fixtures in `tests/` | Orchestrator: `otto check` passes; it fails on a planted invalid link, unknown template and project with no goal in `strategy` | [ ] |
| **MK-4** Marketing overlay and local skills | X, packet | MK-2 | `agent/` documents linking Otto's guidance at the pinned tag and adding only plan, create and critique a Reddit announcement video and the publication authority rule, `skill: true` where they are skills; they point at the pinned `poms_packs` Astrid video skill and do not copy it | `otto skills build` and `check` pass; installing into a temporary destination beside `otto-*` packages clashes with none; no Otto rule is restated (each overlay rule is either Marketing-only or a link); a request to publish without approval is refused by the documented procedure | [ ] |
| **MK-5** Make the one real project: Reddit announcement videos | N, packet | MK-3, MK-4 | `projects/reddit-announcement-videos/` and its draft or review deliverable | Its agreed tasks are done with real proof; claims verified against cited sources; the deliverable is held for the owner's approval, never published | [ ] |
| **MK-6** Cancelled by the owner's 25 November 2026 scope: no loop project and no campaign | — | — | — | — | [x] Cancelled |
| **MK-7** Cancelled: folded into MK-5 (the owner's 25 November 2026 scope) | — | — | — | — | [x] Cancelled |
| **R** Cancelled: no review budget; the owner accepts the deliverable and the completion PR carries the evidence (25 November 2026) | — | — | — | — | [x] Cancelled |

### Dispatch boundaries

Plan 95's Marketing fixture is a test of Otto, not a pilot: do not repeat it here, and do not edit Otto or Dev from this plan. External publication, contact and spend are not needed to finish and each needs separate approval. No private operational data in this public planning repository.
