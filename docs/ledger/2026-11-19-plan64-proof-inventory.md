Date: 2026-11-19
Kind: issue
Source: Plan 64 whole-project run
Resolved by: —

The plan's focused test inventory missed existing callers affected by reference ordering, Character Swap controls, plain frame counts, and source-free image preparation. Seven selectors passed at the starting SHA and failed on the plan branch, but were found only when Plan 65 compared full CI results; the manager then added a baseline comparison and repaired them in astrid-agent#432. Have the manager workflow require a cheap changed-callers and existing-test inventory before freezing the local baseline, with newly discovered proof files run on both base and candidate; keep full-suite execution on CI. This preserves the narrow worker proof while exposing cross-card regressions before another plan consumes the branch.
