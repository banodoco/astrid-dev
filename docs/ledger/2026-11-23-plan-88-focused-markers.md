Date: 2026-11-23
Kind: issue
Source: Plan 88 TE-1 media metadata follow-up
Resolved by: —

A focused pytest file run reported 94 passes while the repository's default marker expression deselected three relevant integration cases; running those exact cases separately exposed identical fixture errors on both the candidate and its base. The runner should report excluded focused cases explicitly and guide a base comparison when they can be run safely, so a green count is not mistaken for complete file coverage.
