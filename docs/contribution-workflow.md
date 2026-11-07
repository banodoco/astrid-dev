# Contribute to Astrid: claim, propose, review, complete

**Start at [the Astrid development skill](../skills/astrid-dev/SKILL.md).** It gives agents one contributor process. The [domain map](../skills/astrid-dev/references/domains.md) locates source and specialists; this page explains GitHub actions. [Our contribution principles](contribution-design-principles.md) explain what must stay simple.

## Choose a route

| You want to… | Action | Approval boundary |
| --- | --- | --- |
| Fix a bug or small issue | Search/open an [Astrid-dev issue](https://github.com/banodoco/astrid-dev/issues) and submit a focused product PR | Reproduction, actual proof and appropriate product PR review; no project pack |
| Take on an existing project | Claim one `queued` and `Unassigned` project through a one-cell catalog PR | **Claim may auto-merge.** It gives ownership, not execution authority |
| Propose new substantial work | Open a [project proposal issue](https://github.com/banodoco/astrid-dev/issues/new?template=project-proposal.md), then a reviewed scope PR | Maintainer accepts the new scope and project pack |
| Submit project work | Open product PRs; optionally open an Astrid-dev implementation review PR | An owner’s PR is **queued for review**, not auto-approved |
| Finish a project | Open an Astrid-dev completion PR linking integrated evidence | Independent completion review and authorized merge |

No mandatory project-conversation issue. Questions belong in an issue or PR; update the authoritative project documents only when a decision actually changes.

## Write or improve documentation

**Writing uses the same reviewed issue/PR pipeline as code; no new project or evidence form for small edits.** Find the owner of the information before making a second document:

| Writing work | Canonical source and route |
| --- | --- |
| Vision, artistic pillars, creator principles, public copy | [Vision authoring guide](../vision/README.md). Edit the source files in `vision/` and run `python3 scripts/export_public_vision.py --sync-readme` to refresh their derived overview; after review, CI publishes the public JSON feed. Don't copy editorial content into Astrid App |
| Gap statements or gap evidence | [Gap contract](../vision/README.md). Material changes need a boundary review; factual current-state/evidence updates use normal PRs |
| New project scope, plan decisions or task briefs | [Project catalog and pack](project-format.md); new scope uses reviewed project proposals, existing project changes inherit the owner and accepted scope |
| Agent instructions, workflows or contributor docs | [Main skill](../skills/astrid-dev/SKILL.md), stage-specific skills, [run contract](../skills/astrid-dev-shared/run-contract.md), or this guide—each owns its own concern. Documentation CI checks these paths |
| Product API, UI, installer or extension technical docs | The owning [product repository](../skills/astrid-dev/references/domains.md). Submit the documentation PR there and link it to the relevant issue/project |
| Typo, small wording or README improvement | Normal, focused PR. No project, new skill, evidence-pack file or planning ceremony |

Describe the intended correction and relevant source; give a real reviewer a way to verify technical claims. For consequential vision/architecture changes, review the *meaning*, not just Markdown validity. Don't invent a documentation-only state machine or keep copies of old drafts for posterity.

## Claim a project without waiting for a maintainer

1. Find an existing `queued`, `Unassigned` [catalog project](../plans/index.md), read its `plan.md`/`inputs.md`/`tasks.md`, and check blockers.
2. [Edit the catalog on GitHub](https://github.com/banodoco/astrid-dev/edit/main/plans/index.md) (fork if needed) and change **only that row’s Owner** from `Unassigned` to your own `@GitHubUsername`. Open a PR using [the claim template](../.github/PULL_REQUEST_TEMPLATE/claim.md).
3. When configured, the protected claim bot verifies the authenticated PR author, one-cell change, permitted status, successful documentation CI and that the live main catalog still has the project available. It then automatically squash-merges and replies with next steps. If two people compete, the second claim fails closed.
4. **This is ownership only.** It neither changes status to `active` nor accepts unresolved scope, grants code execution, incurs cost, or permits release. Honor the project’s accepted scope and existing authority/STOP controls.

If the safe claim bot is not enabled, the **same PR** can be merged by a maintainer. No extra registration service, OAuth application for contributors or duplicate owner record.

### After claiming: start, pause or hand back

1. Check the project's `Waiting on` field, `inputs.md` planning decision and existing run controls. If the scope is already accepted **and** a specific authorized start is recorded, follow it; do not request the same approval again.
2. If scope is unresolved, open a [scope-review PR](../.github/PULL_REQUEST_TEMPLATE/project-scope.md) against the *existing* project. If the scope is settled but execution authority is missing, ask the maintainer in a [project question](https://github.com/banodoco/astrid-dev/issues/new?template=project-question.md) for an explicit go specifying the task, permitted environment/cost and destination. Record that decision in the existing project/run context and, when authorized, use an ordinary reviewed catalog PR to update status to `active`. **Claiming alone never activates work.**
3. If you cannot continue, preserve your work, open PRs and blockers. For a **non-active** project, submit a small reviewed PR changing your own `@handle` to `Unassigned`. For an **active** project, first arrange a reviewed handoff to another owner or a reviewed transition to `paused` alongside release; CI doesn't permit an active project without an owner. None of these are auto-claims. Don't rewrite project history.

No lease timer or separate ownership system. The catalog is authoritative, and normal GitHub history records claims and handoffs.

## Propose and greenlight new work

A proposal issue captures the desired independent outcome, relevant existing work and gaps, alternative issue/project placements, and likely proof. Anyone can propose—without claiming the work.

To accept a new independent project, open a **scope PR** with one `queued` catalog entry and the existing three-file pack: `plan.md` (outcome, scope, interfaces, completion), `inputs.md` (prior art, reuse choice, actual owner decision, uncertainty), and `tasks.md` (work and focused proof). Use [the scope template](../.github/PULL_REQUEST_TEMPLATE/project-scope.md) (choose it from the GitHub PR template chooser, or copy its opening lines):

```text
Project: plans/NN-project-name/plan.md
Review request: scope
```

A maintainer compares the plan with existing issues, projects, gaps and source evidence. Their review/merge greenlights **the scope**, not implementation or publishing. Leave unaccepted proposals as an issue/draft PR with a specific next decision; don't manufacture accepted decisions just to satisfy CI.

## Submit work for review

A project can have **multiple PRs across Runtime, Agent, App and other repositories**. Each product PR links the project/task, states exact source/dependency revisions, describes the claim and actual checks, and names what remains unproven. Use the small [review submission](../templates/review-submission.md) in a target product repo; the product repo’s own CI, reviewers, branch and release rules remain authoritative.

If the contributor needs an Astrid-dev PR to review a project handoff or implementation evidence, use [the implementation-review template](../.github/PULL_REQUEST_TEMPLATE/implementation-review.md) (select it when creating the PR) and identify the canonical plan:

```text
Project: plans/NN-project-name/plan.md
Review request: implementation
```

**PR intake requires those two exact opening lines** (`Project:` and `Review request:`). The generic GitHub PR template doesn't infer a project or review lane from checkboxes; add those lines explicitly or choose the matching template. Small bug PRs don't need them.

The low-permission [review-intake workflow](../.github/workflows/review-intake.yml) checks the GitHub PR author against the **live catalog owner**. A matching, non-draft request receives `needs-review` and an acknowledgement. Scope PRs are also queued when their project files/catalog change appropriately. This means **accepted into the review queue**, **not approved**. Reviewers watch the [open queue](https://github.com/banodoco/astrid-dev/pulls?q=is%3Apr+is%3Aopen+label%3Aneeds-review). A label is not a reviewer assignment: a maintainer must take responsibility or request a reviewer through GitHub's normal review UI. This workflow does not run fork code, approve, merge or deploy.

**Independent review:** A fresh qualified reviewer examines actual diff and retained implementation, claims versus tests, first failures, negative cases, model provenance, dependencies and risks. They return concrete blocking findings or a justified acceptance with limitations. The contributor repairs the same failing cases on the new candidate. Human approval remains necessary for consequential changes, security, user data, migrations, costs and deployment under the product repositories’ policies. A CI pass or an agent’s advice alone does not override these authorities.

**Integration:** Freeze the intended target/donor revisions and reuse unchanged proof only where justified. Separate green product PRs do not qualify a combined Runtime/Agent/App installation. The [release skill](../skills/astrid-dev-release/SKILL.md) governs cross-repository integration and separately authorized promotion.

## Record models as work happens

`run.yaml` configures **intended** model roles, but the review should report which models were **actually used**. Record the provider, exact model ID where visible, task, role, effort if available, and whether the information is **runtime-observed with a receipt** or **self-reported**. Do this at the relevant invocation, not from memory at the end.

In an **Astrid-dev checkout** (not necessarily a product-repository checkout), the [model-use helper](../scripts/model_usage.py) is available:

```sh
python3 scripts/model_usage.py --run-dir plans/<project>/.otto/runs/<id> record \
  --provider openai --model-id <actual-model-id> --role implementation \
  --task <task-id> --basis self-reported
python3 scripts/model_usage.py --run-dir plans/<project>/.otto/runs/<id> summary
```

When the running agent framework offers actual invocation metadata, it should write the same records directly. The local JSONL stays gitignored under `.otto/`; copy the helper's one-line **Models used:** summary into the review PR (and add source receipts where appropriate). If the identity is inaccessible, use **Unknown — reason**. A manual record is not proof of what the model provider actually executed.

## Submit a completed project

Once the required product changes are integrated into their intended destinations and the **combined result** has been qualified, the owner submits one Astrid-dev completion PR using the [completion template](../.github/PULL_REQUEST_TEMPLATE/project-completion.md):

```text
Project: plans/NN-project-name/plan.md
Review request: completion
```

It changes that project’s catalog status to `done` and includes the existing `## Completion assessment — Plan NN`: actual evidence, implementation PRs in every repo, the exact integrated candidate, **Models used**, what remains unproven and a justified disposition for each linked vision gap (or the enabler exception). This concise PR summary is the **review evidence pack**: link real receipts, do not create another required file.

CI enforces the mechanical completion contract and current references. A reviewer judges actual integrated behavior against the project’s agreed acceptance criteria. A maintainer merges only after required independent review and authorization. Completing the project does **not** automatically close a vision gap or deploy the result.

## Get help and keep decisions discoverable

Ask a project question using the [optional issue template](https://github.com/banodoco/astrid-dev/issues/new?template=project-question.md) (or comment on a relevant PR). Reference the plan ID and tag the owner/maintainer when appropriate. Record durable scope decisions in the project pack, not a new standing conversation hub.

The README and main skill point here, templates link back, and the automated claim/review response gives the next action. **Maintainers:** [safe automation setup and adversarial smoke tests](contribution-automation-setup.md).
