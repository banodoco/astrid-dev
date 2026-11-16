Date: 2026-11-16
Kind: fix
Source: the owner's decisions, Hannah, 16 November 2026, on Release 14's fix branches and on a fix release meeting a release in progress
Resolved by: —

Two things. First, fix branches carried no reason: a fix row's Role was bare `fix`, so nothing said what a branch was for. Now every piece of work says what it belongs to, at its branch: a plan branch by its name, a fix branch by its astrid-dev issue, written `fix #<issue>` in the brief's Role. A pull request into `release/<NN>/main` must name its plan or issue, enforced by each product repository's `landing reference` check, now one of the required checks. The Branches check rejects a bare `fix`, and `release_branches.py check` confirms the issue exists, or reports it not verified without a token; Release 14's table is brought to the real state. Second, the Release skill said a release's number is fixed once its branches exist, and that a fix to the published release takes the next free number, which the App's release guard (exactly the served number plus one) would refuse for the release in progress. The guard stays strict: a fix release always takes the served number plus one, and a release in progress holding that number is renumbered by its release manager in one step (brief, branches, Branches table, a line in the brief, `release:NN` labels, open pull requests retargeted). The rule is stated once in "How a release runs", and the fix-release section links to it.

Follows: 2026-11-16-one-account-of-a-release
