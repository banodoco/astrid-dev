# Tasks — Project elements

[Plan](plan.md) · [Inputs](inputs.md)

The work so far was done before this pack existed; its commits are listed by repository in [inputs](inputs.md#source-identities). The remaining tasks are written once the owner confirms the scope.

**Task ids:** `PE-1` onward. **Critical path:** PE-1 → PE-2. **Test inventory:** to be listed by PE-1.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| PE-1 Inventory what `release/15/plan-69` holds against the [outcome](plan.md#outcome-and-scope): what is done, what is half done, and the tests that cover each, from the code and its tests rather than commit titles. Write the remaining tasks below. | N | — | read-only | One row per outcome bullet with its evidence (file, test, result) or its gap | [ ] |
| PE-2 Land the plan into `release/15/main`: merge `release/15/main` in, regenerate pins, prove the [completion](plan.md#completion) on the combined tree | X | PE-1 and the tasks it adds | `release/15/plan-69` in astrid-app, astrid-agent, astrid-runtime | The completion case passes on the combined tree; the focused tests named by PE-1 pass on base and head | [ ] |
