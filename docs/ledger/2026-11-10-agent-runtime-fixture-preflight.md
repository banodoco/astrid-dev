Date: 2026-11-10
Kind: fix
Source: Release 12 Track A A2 comparison
Resolved by: —

The comparison runner now installs the pinned Runtime checkout editably for the selected custody fixture tests and verifies the imported Runtime and producer fixture paths before pytest. Missing or misdirected fixtures fail as environment errors; older revisions without those selected tests skip the preflight. The shared general setup remains unchanged. Follows: 2026-11-10-agent-runtime-fixtures.
