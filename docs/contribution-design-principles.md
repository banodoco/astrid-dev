# Principles for contributing to Astrid

> **Make good contributions easy, poor decisions difficult, and results independently verifiable—with the least machinery necessary.**

Astrid Dev is a version-controlled coordination and knowledge layer for many independently operated agents, generally **one accountable owner and one contributing agent per project**. It is **not** an agent scheduler, a product source repository, or another database. Agents with different levels of context should be able to contribute without making the product or its decisions incoherent.

## Design principles

1. **One coherent path.** Understand → Decide → Do → Prove → Integrate. Enter at the first unresolved stage; keep accepted prior work. Specialist skills deepen stages rather than create competing processes.
2. **One source of truth per fact.** The [catalog](../plans/index.md) owns project status, priority, owner and estimate. A project owns its scope and inputs. Gap files own their assessment; product repositories own product behavior. Generate views and link evidence instead of copying authority.
3. **Rigor proportional to consequence.** A small issue needs a focused investigation and proof, not a project. Consequential, irreversible, safety-sensitive or cross-repository choices deserve deeper research and independent challenge. Scrutiny follows risk, **not** a fixed number of planners, documents or alternatives.
4. **Use agent judgment, don't replace it with forms.** Require decisions to be intelligible and defensible, but let competent agents choose proportionate means. Reviewers challenge the reasoning, not prose length.
5. **Build on prior art.** Before inventing an implementation, trace the actual behavior, search live and retained work, identify reusable paths and explain what is preserved. Distinguish a negative search result from an assumption that nothing exists.
6. **Evidence proves a specific claim.** A claim names its result, exact code/dependency identity, applicable environment, method, observed pass/failure and limits. A green wrapper, a URL, an old test or a completed task list is not automatically proof.
7. **CI checks objective invariants; reviewers judge meaning.** CI parses records, validates references and state transitions, and runs scoped tests. It should not score confidence by paragraph length, infer consent from a link or assert that a test demonstrates more than it does.
8. **Templates are prompts for useful information.** A draft may be short and honestly unfinished. Defined projects preserve their actual reasoning and owner decision. Add fields or files only when they reduce uncertainty for the next worker.
9. **Project boundaries should be independently useful.** Each project consumes identified inputs and produces an artifact or behavior that another agent can use with stated qualifications. A hard bug is still normally an issue; difficulty alone doesn't create a project.
10. **State transitions are minimal and explicit.** Defining scope, authorizing execution, proving a result and publishing it are different facts. Reuse current catalog and run controls; do not introduce parallel status ledgers or automatic approval through CI.
11. **Keep provenance discoverable, not duplicated.** Point to exact source commits, decisions, first failures and receipts. Distinguish historical snapshots from current facts; keep the next handoff short and link details where they live.
12. **Prefer subtraction.** Before adding a schema, validator, approval stage, role or helper, show which duplication or failure it removes. Reuse existing mechanics when their semantics match; don't force unrelated decisions into one abstraction just to reduce file count.

## Where each responsibility belongs

| Layer | Owns | Does not own |
| --- | --- | --- |
| [Contributor skill](../skills/astrid-dev/SKILL.md) | Entry, work classification and the common path | Product-specific source facts or a second authority system |
| [Domain map](../skills/astrid-dev/references/domains.md) | Where to find canonical expertise and product owners | Replicas of domain runbooks |
| Specialist skills and [run contract](../skills/astrid-dev-shared/run-contract.md) | Stage-specific judgment, source identity, authority and exact proof | New statuses or new approval rounds |
| [Issues](https://github.com/banodoco/astrid-dev/issues) | Bugs, small contributions and investigation threads | Project-sized strategy |
| [Project packs](project-format.md) | Outcome (`plan.md`), inherited facts (`inputs.md`), tasks/proof (`tasks.md`) | Copied status, competing histories or generic orchestration |
| [Project catalog](../plans/index.md) | Project accountability, priority, status and estimate | Task progress or proof validity |
| [Vision gaps](../visions/gaps.md) | Missing outcomes and evidence-based reassessment | The list of projects or automatic closure upon delivery |
| PR receipts and product evidence | What was decided, built, observed and qualified | Permissions to ship that weren't granted |
| [Documentation CI](../.github/workflows/docs.yml) | Mechanical integrity and exact-revision public projection | Architectural judgment or a claim that all relevant scenarios passed |

## Proof and review boundary

**An evidence pack is a view of existing receipts, not necessarily a new file.** For each consequential claim a reviewer should be able to answer:

- What precise behavior or decision is claimed, and what scope is excluded?
- Which repository, candidate commit/tree, dependencies, setup and inputs were actually examined?
- Which specific check or observation was performed, what happened, and which negative case matters?
- What remains unknown, untested, failed, or blocked? What previous failure did the change address?
- Where is the durable result another agent can inspect or consume?

Put detailed commands, logs and artifacts where they naturally belong (product test receipts, issue, run evidence or project records). A PR links them and states the conclusion. **CI verifies references and actual checks; independent review decides whether they substantiate the conclusion.**

## A project handoff in existing files

An agent should be able to answer four questions without reconstructing an author's chat:

| Question | Home |
| --- | --- |
| What creator outcome, scope and completion criteria? | `plan.md` |
| What code, prior art, accepted decisions and actual source revisions are inherited? | `inputs.md` |
| What must be changed, consumed and produced; what proves it? | `tasks.md` |
| What exact candidate, actual result, limitations and integration destination were delivered? | Completion PR/receipt, linked from the project when useful |

A project is typically owned and executed by one contributor. Optimize for **a dependable boundary between projects**, not an elaborate internal agent-management platform.

## Change checklist

Before introducing a new mechanism, ask: **Is the fact already owned somewhere? Is the decision objectively checkable or judgmental? Which real failure does this prevent? Can an existing parser/skill/record serve it? Can we remove an old rule instead?**

The expected result is fewer concepts and more meaningful proof—not a higher count of validated fields. This document governs design choices; [AGENTS.md](../AGENTS.md) and the run contract remain the executable authority and safety boundaries.
