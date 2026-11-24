Date: 2026-11-21
Kind: issue
Source: Release 14 Plans 59, 64 and 65 integration run
Resolved by: —

Parallel conflict resolution in one merge worktree allowed one worker to restore another worker's eight paths after a scope instruction was misunderstood. The second worker detected the unexpected mutation before its resolution was lost, and reconstructed the conflict stages from the immutable merge inputs; the run also had to recover interrupted proof after container restarts. The integration workflow should make file ownership and stage-specific path lists explicit in each worker card, check paths against those lists before writing or staging, and preserve merge inputs and proof status in durable run records so recovery does not mistake a partial run for a result.
