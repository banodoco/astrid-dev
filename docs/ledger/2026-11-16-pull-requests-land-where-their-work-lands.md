Date: 2026-11-16
Kind: fix
Source: the owner's decision, Hannah, 16 November 2026, on open pull requests against `main` and retired branches
Resolved by: —

Open pull requests had accumulated against `main` and against branches that no longer existed, with nowhere to go: product `main` only moves at publication, and a pull request into a release branch must come from a branch of that release. Nobody could merge them, and nobody could tell which were live. Now there is one path for each thing: a pull request lands where its plan or issue lands. A pull request for a plan in a release is retargeted to that plan's branch; one that fixes an issue in a release lands in `release/<N>/main` from a fix branch, with a contributor's commits merged unchanged into a new branch when theirs cannot satisfy the landing check; one for a plan in no release is recorded in the plan's `inputs.md` and closed, the contributor's branch staying; one that belongs to nothing yet gets an issue or a plan first. No pull request into a product repository targets `main`, so the open list shows only live work. The rule is written once, in [Merge](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/skills/capabilities/astrid-dev-merge/SKILL.md#where-a-pull-request-lands), and the contribution workflow and the Release skill link to it. The first uses are recorded in Plan 16's and Plan 15's `inputs.md`.

Follows: 2026-11-16-work-belongs-to-something
