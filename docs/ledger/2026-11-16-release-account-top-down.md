Date: 2026-11-16
Kind: fix
Source: the owner's decision in the advisor's session on 16 November 2026, after a review found that releases had no place in the README and that the Release skill never stated its idea before its steps
Resolved by: —

Two refinements of 2026-11-16-release-branches-per-repository, which said a release branch is "cut from the served release" and that "once a release's branches exist its number is fixed", are recorded here and supersede those two sentences. A release branch is cut from the newest release branch still unpublished if there is one, otherwise from the served release. A release keeps its number, except that a fix release to the published release takes the served number plus one, and a release in progress holding that number is renumbered. Both were already the rule in the Release skill; this entry makes the ledger agree. The documentation is also restructured top-down: the README gains "From projects to releases", "How a release runs" opens with one paragraph stating the whole idea, its 17 steps become 11 with the numbering procedure after them, each rule has one home in the Release skill, the requested-lane section is folded into "Promote or publish", the glossary defines the served release, the integrated candidate and lane once, and stale sentences in the contribution workflow are corrected. No rule changed.

Follows: 2026-11-16-release-branches-per-repository
