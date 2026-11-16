# Release 12 review round 3 (Agent 87d1fbbc4..313bbd46f)

[Handoff](../../handoff.md) · [Tasks](../../tasks.md)

## Release blockers

- **P1 — `astrid/packs/__init__.py:71`:** Verified `personal` snapshots hit the reserved-directory rejection before the relocation exception. Personal-pack tasks fail on macOS/Windows. **Fix:** allow the exact validated canonical-personal relocation through this guard.

- **P1 — `astrid/core/pack/imports.py:155`:** Personal-collection snapshots are advertised as additional collections. Actions calling pack discovery encounter both original and snapshot directories and fail with duplicate-owner errors. **Fix:** preserve the original collection identity while binding executable imports to the verified snapshot.

- **P2 — `astrid/core/execution/generic_host.py:8217,8268`:** Failed renewal/refresh blocks claims but preserves the previous `ready` marker. Reproduced owner attach returning `ready` for that blocked host. **Fix:** invalidate readiness on failure/fencing; republish after successful registration.

## Non-blocking

One host-recovery test failed on an unchanged, pre-round-3 path. Native Windows/macOS execution remains unverified.

Reviewed all four merges; targeted tests produced 194 passes and six skips, including successful reruns after disk exhaustion. Reproduced all three findings with isolated probes; source tree remains clean.
