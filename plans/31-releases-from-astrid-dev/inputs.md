# Inputs — Releases defined and published from astrid-dev

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Release-led strategy direction (10 Nov 2026):** The owner asked that each release be planned in advance as a living strategy document, showing a one-line highlight, fuller outcome, included plans with one-line reasons, and intended approach. The top-level strategy should mostly summarize those releases. This amends the earlier JSON-only record design: `releases/<N>.md` is the human-readable draft and the permanent final ledger entry, with a machine-readable pin block added only for final publication. The draft/strategy consistency check can land as an ordinary documentation improvement now; the publish gate, final-record migration and product integrations remain Plan 31's separately authorized work. A draft must never imply a go to ship, and old records must be imported from actual receipts only. No separate Markdown log or duplicate release plan.


**Scope decision:** Pending — on 8 Nov 2026 the owner asked for releases to be defined and published from astrid-dev, with CI and protection, as a new project that starts after Plan 29 ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)). Next: the owner answers the open decisions below and confirms the scope.

**Prior art:** read-only maps of the release number in the App, Agent, Runtime and Pinokio at App `915bfa84d87268038f396dc999dc2095683e5d8a`, plus two independent design reviews ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)). Key findings:
- The integer `release` is checked as an integer in every repository and persisted on users' disks, so switching the wire format would cost 8–12 days.
- On App `main`, `pin.mjs` added 1 on every pin run, which is how release went from 1 to 9 on 7 Nov.
- At least six consumers read the manifest from an App checkout or image, not from astrid.haus.
- The vision feed already publishes from astrid-dev to a generated-only branch, after testing with the App's parser.
- astrid-dev `main` and App `main` are unprotected, and every product repository is public.

**Approach:** astrid-dev release records, checked by CI with the App's existing manifest check, published like the vision feed. The App syncs one generated copy, so nothing in the Agent, Runtime or Pinokio changes. This replaces Plan 29's UR-8b (version helper, App PR #208), UR-8c (markdown log, astrid-dev PR #82) and UR-8d, and UR-8's tuple guard.

**Challenge:** Reviewed — two independent high-judgment reviews ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)). The first kept the App manifest as the source. The owner then asked for astrid-dev as the source, and the second review, briefed for the simplest reliable design, chose syncing a generated App copy over having astrid.haus serve the manifest at runtime. Proxying would add server code to the install path, make installs depend on GitHub at install time, and change five consumers. It also cut signatures, a separate go-check bot, version arithmetic and the markdown log.

A third high-judgment review on 8 Nov 2026, after Plan 29's lessons ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)), split the four tasks into twelve plus an owner row and resized the plan from 6–7 to about 12.5 days. All of its findings were accepted:
- Work lands on `int/31` with a go-live task (RL-G), instead of PRs on `main`.
- The fail-closed gate is its own S task, not inside an N task.
- Each commit must be an ancestor of its repository's `main`. Fetchable isn't enough, because GitHub serves fork and PR commits through the parent.
- `CODEOWNERS` covers the publishing code as well as `releases/`.
- A typed shared manifest schema (RL-2a) replaces the hand-written parsers.
- `release-contract` checks against the App branch the PR targets, so it can be proven before Release.
- The deletion list is updated for what Plan 29's UR-8 already removed. Deleting `release-guard` needs an owner row (O-2), since Plan 29 makes it required.
- The sync stays off behind an owner-set variable, runs the App's checks itself before pushing, and is a named Release-skill step.
- RL-3 adds `QuietUpdateNotice.tsx` and the local launcher, and shows "an earlier version" for a release with no version.
- A worker setup script for the App (RL-0) lets workers run the proofs. Proofs that need other repositories are labelled hosted.
- The plan is phased, because it is over ten days.

**Review rounds:** Pending — recommend at most three. This is release and security work, and it moves the trust root for code users run into astrid-dev. Next: the owner confirms the number.

**Ambiguity pass:** Pending. The tasks include X and S, and other agents will run them, so N helpers run one per task group before the plan starts, resolving choices from code and listing only real owner decisions. It waits for the start because Release 10 and the Green mains rule change the files it reads. Next: run it when the owner gives the go.

**Proof and limits:** see [plan.md](plan.md#completion). astrid-dev `main` protection is a prerequisite for the first publish. A release goes live within one sync interval plus a deploy.

## Owner decisions

Already decided (8 Nov 2026, recorded in [Plan 29's inputs](../29-update-and-release/inputs.md#owner-decisions), decisions 7–8):
- **Versions:** `major.minor.patch`, patch by default, minor or major only when the owner declares it. Release 10 is `0.0.10`.
- **Wire ordering:** the integer `release` stays the ordering key.
- **Required:** its own per-release decision with a reason, never implied by kind. Kind changes no behaviour for now.
- **History:** it starts at a legacy record for the release live when this plan starts, expected to be Release 10 = 0.0.10.
- **Hosted App deploys** are not releases.
- **Source:** astrid-dev defines and publishes each release. This replaces Plan 29 decision 9's "App manifest stays the source".

Open, each with a recommendation:
1. **Sync trigger and push identity:** a scheduled pull plus a manual run, or an instant push from astrid-dev. Recommend the scheduled pull. Either way, the sync pushes to App `main`, which will be protected. The workflow token probably can't be put on a ruleset bypass list (unconfirmed; confirm at start). If so, the sync needs a GitHub App or deploy key that can write only to the App. That is a new credential, the owner sets it up, and RL-2c becomes S.
2. **Who can approve a release:** only the owner in `CODEOWNERS`, or any maintainer. Recommend only the owner.
3. **Protection timing:** protect astrid-dev `main` now, since it's required before the first publish. App `main` follows (owner row O-2). Recommend now.
4. **Versions for past releases:** the legacy record maps releases 1 to N as `0.0.<n>`, so every existing install has a version to show. Recommend yes.
5. **Phasing:** phase 1 is publishing from astrid-dev; phase 2 is versions on screen (RL-3, about a day). Recommend these phases. RL-3 could instead join phase 1 for one go-live, at the cost of a longer first review.

## Source identities

Record exact base SHAs when each task starts. Land all work on `int/31-releases-from-astrid-dev`, in astrid-dev and the App, cut from each `main` when the run starts. Only the Release skill moves either branch to `main` (RL-G).
