Date: 2026-11-15
Kind: fix
Source: Owner's request after pull request 664, 15 November 2026
Resolved by: —

Cancel superseded documentation and review-intake PR runs while isolating each main push, preserve the existing publication/refresh job concurrency, and enable squash auto-merge for trusted authors' eligible planning-only PRs through a dedicated App after repository checks and reviews pass. Holds, owner-decision wording and drafts block eligibility; only this App's requests are removed. Add offline eligibility tests and require local unit tests plus repository checks before script changes or new plans/release briefs are pushed. Product code remains outside this automation. This does not fix the GitHub-hosted runner wait: a runner reserved for this repository or fewer concurrent product-repository jobs needs the owner's decision. Follows: 2026-11-15-planning-ci-queue
