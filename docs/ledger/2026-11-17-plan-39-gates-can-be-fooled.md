Date: 2026-11-17
Kind: issue
Source: an independent probe of Plan 39's merged gates, run by the Release 14 Lead under the new rule that a gate is accepted only after its fooling cases are tried, 17 November 2026
Resolved by: —

Plan 39's gates were merged on proof that they pass, not that they fail when they should. The probe graded them D overall:
- **Agent lint and type gates:** they compare counts, block only five codes, and accept a same-PR edit to their own baselines. 93 mypy pairs above baseline pass as "not blocking".
- **Structure gate:** it is not in `fast checks`.
- **The Agent release branch:** it has failed its mypy gate since #370.
- **Runtime guard:** it is always red under CI's xdist, so it cannot show a new failure.
- **Runtime and App guards:** both accept forged declared tags.
- **App guard:** it cannot see vitest's expected failures.
- **Deselection:** nothing guards it.
- **Required checks:** no release or plan branch requires any check.

Rows GL.1, K1b.1, K1c.1, SF3a.1 and K0 and packets R14-P39-07 to 09 fix the gates, each proved by its fooling cases. Making checks required is the owner's setting (row K2 and the owner row in Plan 39).
