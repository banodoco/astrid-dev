Date: 2026-11-10
Kind: fix
Source: Plan 29 release 12 final gate (orchestrator session)
Resolved by: —

During release 12's final gate, the manager brought the advisor three questions its skill could have settled. Should it re-run a gate after a fix? Should it wait for every fix before starting any run? Were the App failures its job to sort? The causes turned out to be a harness that ran `python -m astrid` where users run the `astrid` command, a journey with pinned versions that didn't match the candidate, and failures already on main. The manage skill now has the manager decide these itself. It re-runs a gate on a fix commit without asking, and starts each run as soon as its inputs are ready. It makes a failure visible and sorts it against main's latest run before asking. It fixes a gate test that drives the product differently from users.
