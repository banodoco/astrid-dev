Date: 2026-11-19
Kind: papercut
Source: Plan 65 final CI comparison
Resolved by: —

The initial CI comparison parsed only FAILED and ERROR lines and split node IDs at whitespace. It missed 33 failed subtests reported as SUBFAILED and truncated parameterized IDs containing spaces, causing incorrect count-gap explanations. The manager rechecked complete IDs through the pytest detail separator and matched all 33 subtests to the base by parent and parameters. The green comparison skill or runner should parse SUBFAILED entries and complete parameterized IDs, reconcile every summary count, and refuse a classification when any result is unaccounted for.
