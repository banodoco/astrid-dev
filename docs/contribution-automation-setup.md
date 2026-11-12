# Maintainer setup for contribution automation

The [contributor workflow](contribution-workflow.md) is public and works without automation. This document is **operational setup for maintainers**, not another approval process.

## Security boundary

There are three deliberately separate GitHub workflows:

| Workflow | Runs when | Permission | May do |
| --- | --- | --- | --- |
| [Review intake](../.github/workflows/review-intake.yml) | A PR opens or changes | `contents:read`, `pull-requests:write`, `issues:write` | Check an owner against the project's `plan.md` on live `main`; label a valid request `needs-review`; comment. **Never merge, approve or deploy.** |
| [Issue intake](../.github/workflows/issue-intake.yml) | An issue opens or is edited | `contents:read`, `issues:write` | Add the type label and `plan:`/`gap:` labels, nothing else. |
| [Claim merger](../.github/workflows/claim-project.yml) | Unprivileged documentation CI succeeds on a PR | Dedicated repository-scoped GitHub App | Auto-merge **only** a validated change to the Owner line of a queued, unassigned project's `plan.md`. Never checkout or execute fork code. |

The claim bot is disabled by default; if GitHub refuses to run a first-time contributor's CI until approved, claiming cannot skip that platform safeguard. All three use trusted `main` code. Proposed code and PR metadata are untrusted input.

## One-time configuration

1. **Protect `main` first.** In GitHub **Settings → Rules → Rulesets**, require pull requests, the Documentation integrity check and an independent human approval for ordinary changes. Restrict force pushes and direct pushes. Configure normal product-repository review rules separately. The claim script also refuses privileged merging unless the main branch reports `protected: true`.
2. **Create/install a dedicated GitHub App** scoped to `banodoco/astrid-dev` only, with **Contents: write**, **Pull requests: write**, and **Issues: write** (for claim confirmation). Allow this App a narrow *pull-request-only* bypass of the main review requirement. No broad personal access token or blanket organization bypass.
3. In repository **Settings → Secrets and variables → Actions**, set `CLAIM_BOT_APP_ID` (variable), `CLAIM_BOT_PRIVATE_KEY` (secret), and finally `CLAIM_AUTO_MERGE_ENABLED=true` (variable). Leave the last flag unset/false until the prior controls are tested. If your organization's rules cannot provide a PR-only bypass, keep auto-merge off and handle claim PRs manually.
4. **Assign review ownership.** The low-permission intake adds `needs-review` (creating it if missing). Have maintainers watch [the review queue](https://github.com/banodoco/astrid-dev/pulls?q=is%3Apr+is%3Aopen+label%3Aneeds-review), or configure GitHub's ordinary reviewer/CODEOWNERS mechanisms. A label is **a request**, not an assigned human or completed review.

These settings cannot be created merely by merging workflow files. GitHub repository administrators must configure the ruleset/App and verify their permissions.

## Adversarial smoke test before enabling claim merges

From a second GitHub account, submit one owner-only claim PR from a fork against a queued unassigned project. Confirm that the merged `**Owner:**` line in the project's `plan.md` names the PR author, the source revision is correct, and the bot's reply links to the real plan. Then verify that *none* of the following can auto-merge:

- A claim for somebody else's `@handle`, or a blocked/active/already-owned project
- Two projects in one PR, an edited goal/status, any changed workflow/code or an extra file
- A stale PR after somebody else claims the **same project** or changes that project's `plan.md`. An edit to another project's `plan.md` should **not** invalidate the claim; GitHub's normal merge must preserve both changes.
- A PR whose CI failed or did not run, or a PR with changing head SHA
- A PR while `main` protection is absent

For review intake, confirm that a proposal with the required scope pack is labelled but **not** approved, and an owner's implementation/completion request is queued. The generic PR template must include explicit `Project:` and `Review request:` lines (or the contributor chooses a specialized template); check that an invalidated PR loses its `needs-review` label. A non-owner's attempt must not enter the owner-specific review queue. Repeat after editing the PR body.

Check the GitHub workflow logs, repository ruleset history and generated vision feed. Do not interpret local unit tests as a full live security verification.

## Failure and recovery

If protection, App credentials or GitHub Actions policies prevent claiming, the exact same owner-only PR can be merged by an authorized maintainer. No separate claim database is needed. If intake fails or a label isn't applied, the PR stays open for normal manual review; **nothing should be auto-approved because routing failed**. An existing label doesn't prove the current commit is qualified.

**Cross-repository scope:** the current `needs-review` automation runs on **Astrid-dev PRs**. Implementation PRs in Runtime, Agent, App or other product repositories use their own native GitHub review/branch protections and the [common review submission](../templates/product-pr/review.md). Do not mistake this single-repository workflow for product-wide automated review. A final Astrid-dev completion PR links the externally reviewed and integrated work.

Do not create a mandatory conversation issue for each project; [Issues](contribution-workflow.md#issues) says where questions go.
