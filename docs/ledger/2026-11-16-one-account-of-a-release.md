Date: 2026-11-16
Kind: fix
Source: three independent reviews of the release skills on 16 November 2026, and the owner's decisions, Hannah, the same day
Resolved by: —

How a release runs was spread over Release, Manage, Orchestrate and Get to green, which contradicted each other: donor commits against merge-only branches, "from the served release" against "from the earlier release's branch", fix releases against fix branches, three descriptions of when CI runs, and no owner for the release branch. The owner decided three things. A plan's manager gets their own part green on the combined tree and merges it into `release/<NN>/main`, then marks their row `merged`; getting the release branch itself green is a named stage of the release, with no tester build, candidate freeze or request for the go until it is green on the exact commit. When a merge turns the release branch red, its author fixes forward or reverts promptly, and other plans land only if their own proof is unaffected. The release manager is the release's orchestrator, one role named on the brief, who owns the release branch; plan managers own their plan branches and landings. The Release skill's "How a release runs" is now the one account of the branches and the order, the CI triggers are stated once in Get to green, and the other skills link to them.

Follows: 2026-11-16-release-branches-per-repository
