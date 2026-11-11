Date: 2026-11-11
Kind: issue
Source: Release 12 shared-host comparison and observer preparation
Resolved by: —

Short tests-first observer runs overlapped Track A's resource-sensitive comparison because workers interpreted the heavy-test restriction as permitting their own short selectors; their exact wall-clock start and end times were not captured. The runs were reported with that limit, not as proof of no overlap. Until an automated host scheduler enforces isolation, the orchestrator owns one explicit shared-host test lease: a manager requests a bounded window, starts tests only after the orchestrator grants it, records command, version, start/end and exit receipt, and releases it before another manager starts. Reading and design remain independent. A future mechanism should enforce and audit this lease rather than relying on worker judgment.
