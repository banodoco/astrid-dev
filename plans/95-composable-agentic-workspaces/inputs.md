# Inputs — Otto — Composable agentic workspaces

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — 24 Nov 2026 owner selected Otto (O-T-T-O) as the shared importable repo/framework, Astrid Dev and Astrid Marketing as first consumers, distinct and multiple pipelines, reusable project templates and local skills. Requested updated work plans. Next: independent critique, record durable approved scope and resolve remaining repository/interface/cutover decisions.

**Prior art:** [Plan 48](../48-one-record-model/plan.md) done; [71](../71-gap-definition-reconciliation/plan.md) active; [72](../72-composable-project-delivery/plan.md) queued for Release 16 with review candidate; [73](../73-markdown-first-agent-skills/plan.md) active, on main 83ab5c0ec2842023f9227451fbb0d71adfee428c. [Plan 97](../97-extensible-project-templates/plan.md) and [Plan 98](../98-project-identity-and-vocabulary/plan.md) now explicitly own template and naming work before extraction. Candidate and current source findings below. No accessible banodoco/otto or banodoco/astrid-marketing repository was returned by the lookup (404); this is not proof of nonexistence or name availability.

**Approach:** Extract proven infrastructure rather than fork Dev or build a speculative execution engine. Named pipelines are local, discoverable declarative compositions over canonical typed relationships; the framework provides validation, navigation, views and skill sync. Start with shared project/task/issue defaults and optional local extension; do not require a new schema to bootstrap a workspace.

**Challenge:** Pending — This changes shared contracts and checks and needs a fresh high-judgment source-capable reviewer before scope greenlight. Next: challenge the necessity of each addition, removals and migration risks against the actual integrated prerequisite tree; record findings and owner dispositions. This drafting session is not independent review.

**Proof and limits:** Two actual independently configured consumers, exact Dev parity, multiple pipelines/one project, adding and removing local pipelines/templates/skills without core edits, native skill coexistence and independent package upgrade/rollback. No actual migration, CI or independent review during this proposal. No marketing account access or real external posting required.

**Review rounds:** Pending — Recommend one RS1 on the minimal interface and one RS2 on integrated isolation/trust before cutover, then one final R. Next: owner agrees counts and independent reviewer bindings.

**Run start:** Pending — Planning only. Next: record owner-authorized run, accountable session, advisor, exact source/destination, permitted actions and limits after prerequisite handoff and scope approval.

### Existing plan handoffs — no change to active scopes

| Existing work | Actual state on inspected main | Otto consumes | Explicit disposition |
| --- | --- | --- | --- |
| Plan 48 | done | record helpers, check/view registries, pack-shape, lifecycle | No reopen; extract mechanisms later. |
| Plan 51 | done | one home, one word, avoid duplicate rules | No reopen. |
| Plan 53 | active | final goal reader and public feed compatibility | Do not expand; verify landed contract with 71/72. |
| Plan 71 | active; [recovery draft #1625](https://github.com/banodoco/astrid-dev/pull/1625) | accepted gap definition, calibrated examples, migration/closure provenance | Finish current phases 1–5 and review; do not activate deferred recurring phases or impose gaps on Marketing. |
| Plan 72 | queued on main for Release 16; [review candidate #1161](https://github.com/banodoco/astrid-dev/pull/1161) | typed refs/edges, canonical adapters, deterministic traversal, negative cases, two read-only compositions | Finish existing RS1 and R, no new DSL, no second operational pipeline in that plan. Otto owns configurable kinds/named pipelines. |
| Plan 73 | active; [recovery draft #1627](https://github.com/banodoco/astrid-dev/pull/1627) | Markdown-first authored docs, safe compiler/install and native discovery | Finish coordinated cutover under its original scope. Otto owns namespace, two-workspace package ownership, distribution and upgrades. |
| Plan 52 / 31 / 58 / 44 | intake, release publishing, strategy, evidence respectively | Dev's actual local contracts and checks | No unrelated expansion or mandatory dependency on unstarted work; recheck overlaps, protect owner authority and coordinate base/hand-off. |

Plans 71–73 are not edited or redispatched by this proposal. Their current scope and reviewed evidence remain authoritative. Plan 97 waits for integrated prerequisites; Plan 98 waits for 97; Otto waits for 98 and 97. Plan 96 uses accepted Otto/Marketing starter. Design/discovery can overlap only with separate authority and no competing writer. A single accountable manager for each new project; use ordinary whole-project or authorized dev-only route for work confined to Dev, explicit cross-repo authority for Otto and Marketing. No active release assignment selected here.

### Inspected coupling and reuse

- [records.py](https://github.com/banodoco/astrid-dev/blob/83ab5c0ec2842023f9227451fbb0d71adfee428c/scripts/records.py), [checks.py](https://github.com/banodoco/astrid-dev/blob/83ab5c0ec2842023f9227451fbb0d71adfee428c/scripts/checks.py), [views.py](https://github.com/banodoco/astrid-dev/blob/83ab5c0ec2842023f9227451fbb0d71adfee428c/scripts/views.py) mix reusable interfaces and fixed Dev project/release fields, check/target lists, principle count/names and view namespace. [project_contract.py](../../scripts/project_contract.py), [lifecycle.py](../../scripts/lifecycle.py) and [export_public_vision.py](../../scripts/export_public_vision.py) fix domain assumptions. Move domain registrations to Dev; keep existing oracles. Plan 97/98 handle their own changes first.
- Plan 72 candidate [16eaf64899f2dde82c7cb79ad92b88928afbd374](https://github.com/banodoco/astrid-dev/blob/16eaf64899f2dde82c7cb79ad92b88928afbd374/scripts/relationships.py) fixes RECORD_KINDS, RELATION_KINDS and primary/enabler rules in the index; [project_delivery.py](https://github.com/banodoco/astrid-dev/blob/16eaf64899f2dde82c7cb79ad92b88928afbd374/scripts/project_delivery.py) reads domain records and exposes two code-defined queries. Generalise registration and define named graph compositions only after final review. Do not treat candidate implementation as accepted.
- Plan 73 candidate [99e9131ef1944f2b22f46ec9e58a65cdd72d187c](https://github.com/banodoco/astrid-dev/blob/99e9131ef1944f2b22f46ec9e58a65cdd72d187c/scripts/agent_documents.py) derives astrid-dev-* names; [skill_builder.py](https://github.com/banodoco/astrid-dev/blob/99e9131ef1944f2b22f46ec9e58a65cdd72d187c/scripts/skill_builder.py) and [skill_installer.py](https://github.com/banodoco/astrid-dev/blob/99e9131ef1944f2b22f46ec9e58a65cdd72d187c/scripts/skill_installer.py) embed namespace, package marker, checkout-reference and cleanup rules. Reuse final package safety and tests; parameterize identity in all ownership paths. Existing .otto/runs directories are Dev run state, not an already distributed Otto package.
- [Run contract](../../skills/shared/run-contract.md), [boards.py](../../scripts/boards.py), [maintainer setup](../../docs/contribution-automation-setup.md) and [docs workflow](../../.github/workflows/docs.yml) distinguish common authority/accountability from hardcoded Dev boards, review, release, App feed and trusted writeback. Keep privileged behavior opt-in and local; do not execute contributor extension code under write credentials.

### Ten vivid boundaries of the end state

1. A new workspace imports Otto and adopts a few defaults; no Astrid-specific infrastructure or mandatory pipeline is required.
2. Dev defines Goals → Gaps → Projects → Releases; Marketing defines Goals → Projects → Campaigns; neither definition changes Otto.
3. One organisation can define multiple named pipelines; graph queries can overlap, branch and feed back, with no automatic execution.
4. One project can appear in two pipelines with one identity, owner, task list, status and evidence; deleting a pipeline deletes no project.
5. A project can use the standard or loop template, or a locally introduced research template; the common record remains the same.
6. Writing a Markdown skill and opting in makes it discoverable; both namespaces sync to the same host without overwriting one another.
7. A release can ship a tightly gated product tuple while a campaign coordinates optional projects and independent delivery; neither grouping is mandatory.
8. Marketing can reference an actual Dev release by source/revision and report feedback without copying product facts or claiming unverified shipment.
9. A small workspace can have projects, tasks, issues and a handful of skills; no required analytics, audience, hypothesis or content database.
10. Otto upgrades are explicit and independently pinned; changing local methodology or adding a pipeline/template/skill does not change another workspace or confer merge, publish or spend authority.

### Alternatives

Fork Dev (duplicates tooling, hardcoded release/skill paths); parameterise names only (does not give independent pipeline/record semantics); build a universal execution DSL or graph database (unnecessary operations and security surface); extract small importable package with trusted local registries, declarative graph compositions and Markdown workstreams (recommended). A fixture-only proof is an intermediate milestone, not completion; two independent consumers plus cold extension prove reuse. Prefer fewer files/interfaces if integrated sources support them.

## Owner decisions

- **D1 (direction selected, 24 Nov):** Otto is the name of the shared importable repo/framework; Astrid Dev and Astrid Marketing first; pipelines and skills independently defined, multiple pipelines per workspace, shared project templates and optional grouping.
- **D2 (open):** actual repository owner/name availability, visibility, Python package/CLI distribution and pinned version/rollback method; recommend smallest importable package, no automatic public registry publication. Repo lookup did not confirm availability. Explicit creation go required.
- **D3 (open):** minimal workspace manifest and local extension registration, pipeline declaration file and project-scope selection. Recommend declarative composition over existing relationship kinds and one source of facts; no execution DSL or mandatory stage.
- **D4 (open):** trusted extension/policy boundary, generated output ownership, skill namespace and GitHub-only reference access; preserve Dev security and evidence. No inherited credentials.
- **D5 (open):** safe cutover after Plan 98, minimal Marketing consumer and repository visibility/access; recommend restricted private strategy, public-safe fixtures, no external action.
- **D6 (open):** review budget and execution authority across three repositories; choose actual branch destinations and accountable manager after critique.

## Source identities

Planning snapshot: banodoco/astrid-dev main 83ab5c0ec2842023f9227451fbb0d71adfee428c (24 November 2026). Prior proposal [PR #1868, original head 6f1dfd829d21103b477da8ad12add8f49cbcb3e3](https://github.com/banodoco/astrid-dev/tree/6f1dfd829d21103b477da8ad12add8f49cbcb3e3) is planning history, not execution authority. At dispatch record final accepted prerequisite commits, actual overlapping writers, base/ref/dirty state, destination, protected CI and named run authority. Re-read moved paths after Plan 73. For release-linked work use the authorized release/plan branch route; an astrid-dev-only run requires explicit owner authorization. No new repository, run, merge or release is authorized by this pack. Record the final accepted Plan 71 rubric/closure receipts, Plan 72 relationship API/proofs, Plan 73 compiler/install/native discovery and Plan 97/98 exact integration receipts. The original candidate SHAs and current draft PRs are not acceptance or execution authority. Record actual Otto and Marketing repo identities and package pin after authorized creation; no assumed private repo access in hosted CI.

## References

[Plan 48](../48-one-record-model/plan.md) · [Plan 51](../51-astrid-dev-clean-up/plan.md) · [Planning skill](../../skills/shared/workstreams/astrid-dev-plan/SKILL.md) · [Run contract](../../skills/shared/run-contract.md) · [Design principles](../../docs/contribution-design-principles.md). [Plan 97](../97-extensible-project-templates/plan.md) · [Plan 98](../98-project-identity-and-vocabulary/plan.md) · [Plan 96](../96-astrid-marketing-organisation/plan.md) · [Original scope PR #1868](https://github.com/banodoco/astrid-dev/pull/1868).
