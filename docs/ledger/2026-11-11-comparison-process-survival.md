Date: 2026-11-11
Kind: fix
Source: Release 12 Track A A2 recovery
Resolved by: —

Recover by checking live processes, log timestamps and explicit exit records rather than assuming a worker or detached process survived. Preserve every incomplete log separately, verify inputs again, and restart the affected side in a persistent command session with fresh output and basetemp. Recheck that the process survives and the log advances; on any later session gap repeat the check rather than assuming survival. This does not establish the unknown cause of the original stop. Follows: 2026-11-11-comparison-process-interruption.
