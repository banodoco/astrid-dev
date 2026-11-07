# Tasks: <project name>

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

For a draft, say which task breakdown, dependencies, routes, and checks remain undecided. Do not present tentative work as ready to execute. Before dispatch, each executable task needs the fields below.

## Task index

| ID / outcome | Route | Depends on | Progress |
|---|---|---|---|
| | | | |

Link each index entry to its detailed section below. Keep short cards here; when many detailed cards have distinct phase owners, put the cards in `tasks/<phase>.md` and link to each card from this index. Add no empty task folders. The index and detailed card should have one shared progress record, not competing statuses.

## Task details

For each task record:

- **Outcome:** the specific behavior or artifact to deliver.
- **Route:** `N` by default (everything below very hard, including ordinary hard work); `X` for very hard; `S` for super hard. Use the [routing table](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings), not a separate model policy.
- **Dependencies and inputs:** exact predecessor outputs and source identities, linked from [inputs.md](inputs.md), including the prior-art/reuse decisions; do not silently replace retained work.
- **Work:** the bounded change, design, investigation, or decision and what to reuse.
- **Focused checks:** what would prove the task's result contributes to the owner's agreed end state, and the evidence appropriate to it—a feature check, visual comparison, research finding, or release receipt. For code, name explicit commands/selectors and what they establish; no broad or automatically discovered suites. Identify missing selectors during task setup instead of inventing them.
- **Done:** the required evidence and existing review/publication boundary.

Keep previously accepted review stages and authority limits. Do not create new sign-offs just to use this format.
