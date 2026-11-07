# Contribute to Astrid: claim, propose, submit, complete

**One entrypoint:** [the Astrid development skill](../skills/astrid-dev/SKILL.md). [The domain map](../skills/astrid-dev/references/domains.md) points to product repositories and specialized skills. This page is the *how-to* for GitHub contribution events; [the design principles](contribution-design-principles.md) explain why the process is intentionally small.

## Choose the smallest unit

- **Bug or small improvement:** search or open an [Astrid-dev issue](https://github.com/banodoco/astrid-dev/issues); use the [bug-fixing skill](../skills/astrid-dev-bugfix/SKILL.md) as needed. Submit a focused product PR. No project pack or ownership claim is needed.
- **Existing project task:** consult its [catalog](../plans/index.md), [plan](../templates/project/plan.md), inputs and tasks. Inherit accepted scope and current source evidence.
- **New independent outcome:** [propose it as an issue](https://github.com/banodoco/astrid-dev/issues/new?template=project-proposal.md). Anyone may suggest work; an issue is a conversation, **not** a second project registry. Once the outcome, prior art and boundaries are ready, open one Astrid-dev **scope PR** with the [three-file project pack](project-format.md) and catalog entry. A maintainer reviews and greenlights the scope by approving/merging that PR; mere submission is not acceptance.

## Claim a project, without waiting for a maintainer

1. Check [the project catalog](../plans/index.md) for a `queued` project whose **Owner** is `Unassigned`, and read its plan and dependencies. A claim can reserve the project even when scope remains queued for approval.
2. [Edit the catalog on GitHub](https://github.com/banodoco/astrid-dev/edit/main/plans/index.md) (fork if asked). Change **only that row's Owner cell** from `Unassigned` to your own `@GitHubUsername`. Open a PR using the [claim PR template](../.github/PULL_REQUEST_TEMPLATE/claim.md). No other changes, including status, priority, estimate or waiting-on.
3. The optional claim automation runs after documentation CI passes. It confirms the PR author's GitHub identity, the exact one-cell diff, and that live `main` still has the project unassigned; it then squash-merges the claim PR and comments with your next step. If two people claim simultaneously, the stale claim must be rebased or another project chosen.
4. **Claiming is not scope approval or execution authorization.** Review the plan's scope and waiting-on constraints; propose a scope update if needed. Respect the [run contract](../skills/astrid-dev-shared/run-contract.md) and any existing STOP controls.

When claim automation is not configured, the exact same one-cell PR is reviewed and merged normally. You do **not** need a separate project discussion issue for claims.

## Propose and greenlight new work

A proposal issue should answer the outcome, relevant existing work, why this is not an issue/task of an existing project, and how success might be demonstrated. Discussion belongs in the issue only while deciding.

The **scope PR** then creates the full project record:
- `plan.md`: outcome, boundaries, consumed interfaces and what completion would prove
- `inputs.md`: source-grounded prior art, alternatives/reuse choice, appropriate challenge and traceable owner decision
- `tasks.md`: bounded work, dependencies and focused proof
- one catalog row, initially **`queued`**, with a GitHub owner if already claimed (or `Unassigned`) and no claim of active execution

A maintainer challenges the fit against existing gaps/projects and reviews the actual source findings. Once satisfied, they approve and merge the scope PR; the `inputs.md` record should reflect the accepted decision. If approval is not yet possible, leave the issue or a draft PR open and give a concrete requested change. **Do not auto-merge new scope.**

There is one owner for each project, but product implementation may involve other reviewers. Permission to run, spend, access credentials or publish remains separate from scope approval and an owner claim.

## Implement, review and integrate

A project may have **multiple PRs in different repositories**. Each product PR should link the canonical Astrid-dev `plan.md` and identify its exact candidate revision, what is claimed, tests and failures, and any other PRs needed. Use the compact [review-submission template](../templates/review-submission.md) if the target repository has no suitable template. Keep all substantive code reviews in their own PRs—not copied into a project issue.

**Independent review** means a reviewer (human or qualified agent) inspects the actual diff, retained implementation, selected checks, their inner results and limitations. Agent review is advice unless the product repository's existing policies authorize it. Humans approve consequential architecture, data custody, security, migrations and publication. Repair failed checks on the corrected candidate; don't turn unrelated tests into evidence.

**Integration** follows the product repos' pin order, existing [release skill](../skills/astrid-dev-release/SKILL.md) and authorization. Separately green product PRs do not prove the assembled Runtime/Agent/App tuple. Never silently change the intended destination or deploy just because a merge is green.

## Submit a completed project

When all required product changes have reached their intended integration destination and the *combined* outcome is verified, submit one **Astrid-dev completion PR**:

- Update the catalog status to `done`, preserving the existing project folder.
- Include the already-required `## Completion assessment — Plan NN` in the PR description, with linked evidence and an assessment of **each linked gap** (or an explicit foundational-enabler explanation).
- Use the [completion PR template](../.github/PULL_REQUEST_TEMPLATE/project-completion.md) to link **all relevant implementation PRs**, actual integrated candidate(s), focused checks, negative scenarios and limitations. A compact review summary in the PR **is the evidence pack**; link original receipts instead of duplicating them in a new required file.
- Optionally add the final PR/receipt link to the project plan's handoff section when it improves future discovery.

CI checks structural transitions, references and required assessments. The independent reviewer judges whether the evidence establishes the project outcome, particularly across repos. A maintainer merges the completion PR; the gap only changes when its own evidence merits reassessment.

## Questions and visibility

Questions may be raised in [Astrid-dev issues](https://github.com/banodoco/astrid-dev/issues/new), clearly referencing the plan ID, or directly on the relevant PR. **No mandatory project conversation hub**. When a decision changes the agreed scope, update the project document so the next agent doesn't need to reconstruct a chat.

The [README](../README.md) and main skill point here. The claim PR receives a bot response when auto-merged. Project and submission templates link back to this guide. People can contribute without installing a skill; agents should read it at the outset.

## Enable secure claim auto-merge (maintainer setup)

The repository's existing `main` branch was **unprotected when this workflow was authored**. Do not turn on privileged automatic merging before protecting ordinary changes.

1. Under GitHub **Settings → Rules → Rulesets**, protect `main`: require PRs, relevant documentation checks and human review for normal changes, restrict direct pushes and force-pushes.
2. Create/install a dedicated **GitHub App**, restricted to `banodoco/astrid-dev`, with repository **Contents: write**, **Pull requests: write**, and **Issues: write** (for the optional confirmation comment). Give this App **PR-only bypass** of the review ruleset; do not grant a general contributor, broad organization bot or personal token that bypass.
3. In repository **Settings → Secrets and variables → Actions**, add variable `CLAIM_BOT_APP_ID`, secret `CLAIM_BOT_PRIVATE_KEY` and variable `CLAIM_AUTO_MERGE_ENABLED=true` **after** protection and App installation are ready.
4. Test one claim from a separate GitHub account and verify that a non-owner, two-row, stale, changed-status and code-bearing PR cannot auto-merge. Confirm the normal `main` push and published vision feed update.

The [claim workflow](../.github/workflows/claim-project.yml) uses `workflow_run` only **after successful ordinary PR CI**, checks out the trusted default branch, and reads the fork's proposed catalog **as inert data**. It checks against both the PR's original base and live `main`, then merges with the exact head SHA. It never runs fork code with privileged credentials. The bot is **disabled by default** until the three settings above are configured. If GitHub itself holds a first-time contributor's CI for approval, that contributor's auto-claim also waits; this is a GitHub Actions policy, not a project approval decision.

GitHub native rulesets and PR reviews remain the authority; do not create another permissions database.
