# Tasks — Update everywhere: remaining setups

[Plan](plan.md) · [Inputs](inputs.md)

Routes: **N** = normal, **X** = very hard, **S** = super hard (see the [run contract](../../skills/astrid-dev-shared/run-contract.md)).

| Task / outcome | Route | Depends on | Focused proof | Progress |
| --- | --- | --- | --- | --- |
| UR-15 Remove the systemd 254 floor | S | Plan 29 | On systemd 249, the Linux worker runs from an owner-only file with no `$` or `%` expansion. An update started before the change still reconciles. An Ubuntu 22.04 row passes | [ ] |
| UR-16a Helper-protocol schema owned by the Runtime | X | Plan 29 UR-10 | A JSON Schema (Python on both sides) under `astrid_runtime/`, outside `contract/`; both repos test against it | [ ] |
| UR-16b Update-status schema, kept outside the versioned contract | N | Plan 29 UR-11 | The App validates against it, and `schema_digest` is unchanged | [ ] |
| UR-17 Refusal rule | N | Plan 29 UR-1 | A separate `resolveRefusal`; refused cards show update wording only when the installed release is behind | [ ] |
| UR-18a Pinokio update proof | N | — | The Pinokio row runs the launcher's own Update action (`update.js`), not a direct installer re-run | [ ] |
| UR-18b Fully local update proof | X | Plan 29 UR-9 | A dev:local test drives the in-page updater (no new hosted row) | [ ] |

## Task details

### UR-15 systemd floor
- **Why the floor exists:** it is there only for `systemd-run --expand-environment=no` (`update_job_platform.py:222`).
- **The fix:** use Windows' approach (`_worker_command`, `update_job.py:1341-1381`). The Linux argv becomes `python -B -X utf8 -I <owner-only job file>`.
- **Effect on in-flight updates:** the worker digest changes, so an update that started before the change must still reconcile (`update_job.py:623, 693, 1279`).
- **Before adding the 22.04 row:** it needs owner approval after a probe.

### UR-16 Contracts
`/v1/update/status` is not in `contract/` today. Adding it there would change `SCHEMA_DIGEST` and switch off `supportsFullV2Commit` in the App (`contract-metadata.ts:22-27`). Keep both schemas outside `contract/`.
