Date: 2026-11-11
Kind: issue
Source: Release 12 Track A A2 comparison
Resolved by: 2026-11-11-comparison-process-survival

After a session gap, the manager initially relied on stale worker status: the A2 base log had stopped at 72% without an exit record and no comparison process remained. The original termination cause is unknown. A detached recovery wrapper was also terminated by the command environment without an exit record, leaving a second incomplete log.
