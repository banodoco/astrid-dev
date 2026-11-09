Date: 2026-11-09
Kind: fix
Source: Plan 29 release 12 run (orchestrator session)
Resolved by: —

Release 12 lost about three hours to permission prompts nobody saw: a four-repo manager session ran repo commands (no allow list loads with more than one repository), and a one-repo worker chained a heredoc, `cd` and a `git -c user.*` override into one Bash call. The manage skill now says: product-repo commands run in one-repo worker sessions, files are written with the Write tool, one simple command per Bash call, and a prompt is reported to the advisor at once.
