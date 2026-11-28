Date: 2026-11-19
Kind: issue
Source: Plan 65 Codex manager review and CI
Resolved by: —

The named focused inventory missed pinned schema, identity, planner and preparation contracts that Plan 65 changed. DS-1 landed with four regressions and full CI later exposed a planner binding conflict; the manager repaired them without weakening tests. Before task integration, the runner should include existing pinned tests covering changed shared contracts in the baseline and focused proof, and explicitly flag missing dependency files before dispatch.
