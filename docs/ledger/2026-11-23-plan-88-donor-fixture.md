Date: 2026-11-23
Kind: issue
Source: Plan 88 Codex manager run
Resolved by: —

An expressly required donor cherry-pick introduced a test whose fake session predates a required base API field. The run's instruction to preserve every test and fixture left its focused proof red, even though a fixture-only adjustment was suggested. Future run briefs should distinguish a newly imported donor fixture from tests already on the target base, and state in advance whether correcting setup without changing assertions is authorized. Record the exact target base and donor proof before dispatch so this boundary is reviewable.
