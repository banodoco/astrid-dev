# CA-005 — Many contributors and agents can't yet work in parallel through one clear process

**Applies to:** [A Shared Creative Endeavor](../pillars/shared-endeavour.md) (primary) · [Completely open by design](../principles/open-by-design.md) (supporting) · **Assessment:** Open; initial assessment (2026-11-11) from a read of astrid-dev's own scripts, templates and packs, reassessed 2026-11-12 after Plan 51 finished (route step 2). Neither is from observed work at scale.

## Desired state

Someone new, or their agent, can learn from one place each what kinds of record Astrid's development workspace keeps, what is checked and when, which pages are written by hand and which are generated, and how to extend any of them. Many people and agents can then propose, claim, progress and finish projects at the same time without waiting on, or overwriting, one another.

## Current state

The contribution principles, skills, templates and checks exist and a small number of contributors use them daily. As read on 11 Nov 2026 ([findings](../../plans/48-one-record-model/inputs.md#what-exists-today)): there is no list of what is checked; local and CI runs can disagree; one generated-page pipeline exists and is not reusable; several facts have two hand-kept homes; every change to any project's owner, standing or estimate edits one shared table; ten of 47 project plans follow the template; and two projects share a number. This shows structure only. Nothing here has been observed with many contributors working at once.

**After Plan 51 (12 Nov 2026):** each rule is written in one place and each role and unit of work is defined once, in a glossary; one skill says where a change to astrid-dev goes and how to prove it; the skills and contributor docs hold fewer words than at the project's start (29,410 to 29,181 at its last merge), and the scripts fewer lines (3,005 to 2,996). One fresh worker, given the new skill and the extending guide, added a check; its confusions were recorded, and seven were fixed in the skill and the guide. That is one worker on one task. A new generated page was not tried, and nothing was run with many contributors at once.

## Gap

The workspace's structure is carried by prose and by separate scripts, so it is hard to learn, hard to extend in one place, and it funnels unrelated work through shared files. Unlike [CA-003](CA-003-vision-experiments-progress.md), this is about people being able to work through the process together, not about the public following why work happened; unlike [CA-004](CA-004-sharing-and-discovery.md), it concerns contributing to Astrid's development, not finding published creative contributions.

## Closure evidence

- One command lists every check and every generated page, and gives the same result locally and in CI.
- A new project lands by adding only its own folder. Ten contributors adding or updating different projects from the same starting point all merge without conflict.
- Each kind of fact has one source. Asked where to change five different facts, a fresh contributor finds each single source from the documentation.
- A fresh agent adds a check and a generated page from the extension guide alone; its confusions are recorded and resolved.
- Refusals work: a hand edit to a generated page, a claim made for someone else, and a project marked finished without its completion form are each rejected.
- Reassessed after a real period in which at least ten contributors worked at the same time, with the process stalls of that period recorded.

## Closure approach

Finish the shared layer the existing scripts already imply before more projects arrive: one way to read a record, one list of checks behind one command, and one way to generate a page. Then let each project carry its own facts, so the catalog is generated from the plans and unrelated work stops meeting in one file. This order keeps the first step free of rule changes, and makes the second step a move onto something already reviewed.

For contributors, the first stage means one command and one list to learn; the second means claiming and updating a project touches only that project. Declaring the pack shape, the lifecycle and a common evidence form is deliberately left until a recorded failure asks for it. Proof at real scale needs real contributors and has no plan yet.

## Route to closure

| Step | Plan | Contributes (closure evidence it delivers) | Milestone |
|---|---|---|---|
| 1 | [Plan 48](../../plans/48-one-record-model/plan.md) | one command lists every check and generated page; a project lands by adding only its own folder; one source per fact; a fresh agent extends it from the guide; refusals work | A: one model, and plans define the list |
| 2 | [Plan 51](../../plans/51-astrid-dev-clean-up/plan.md) | each rule and term has one source; a fresh agent changes astrid-dev from one skill and the guide it links (shown for one new check; not for a new generated page) | B: one home per rule and one word per term |
| — | unplanned | reassessment after a real period with at least ten contributors working at the same time | — |

Critical path: step 1, then step 2, then the unplanned reassessment.

## Sources and reassessment

[Plan 48 inputs](../../plans/48-one-record-model/inputs.md) · [contribution design principles](../../docs/contribution-design-principles.md) · [process ledger](../../docs/ledger/README.md). Reassess when Plan 48's phases land, and again against real parallel work. A plan alone does not close this gap.
