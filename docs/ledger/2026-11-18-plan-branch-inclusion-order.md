Date: 2026-11-18
Kind: papercut
Source: Plan 65 Codex manager startup
Resolved by: —

A branch-row-only registration PR failed the release-document check because the plan was not yet listed under Included plans. The host added the inclusion first, after which a fresh row-only PR passed locally. The runner brief should check release inclusion before instructing a manager to open the row-only PR, and coordinate any missing inclusion with the release owner.
