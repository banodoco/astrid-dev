# Tasks — Update everywhere: remaining setups

[Final Release 16 programme review](../../releases/16/evidence/final-programme-review.md) records current dependencies, estimates and remaining decisions.

[Plan](plan.md) · [Inputs](inputs.md)

## Current Release 16 dispatch interpretation — 27 November 2026

This is the canonical residual reading of these existing task IDs after [installation/update sense-check #2060](https://github.com/banodoco/astrid-dev/issues/2060). It preserves original tests, safety requirements and historical progress; it does not mark product acceptance complete, create a new author, change existing proof contracts or add review rounds. The [P09 programme](../09-install-and-update-confidence/plan.md) owns the shared lifecycle and qualification sequence; P31 owns publication. Refresh live reservations before assigning any shared function, especially the existing `38-08U` joins on [#2050](https://github.com/banodoco/astrid-dev/issues/2050).

| Existing IDs | Current R16 disposition |
| --- | --- |
| UR-15 | Old-systemd worker lifecycle and legacy-job compatibility; independent from P38 managed-warm contract. |
| UR-16a | One Runtime-owned contract only for an unvalidated seam; reuse existing types/tests first. |
| UR-16b / LA-2 / LA-4 | One normalized paired status and reason contract; do not mandate duplicate wrapper schemas or digest churn. |
| UR-17 | Existing decision meanings including behind/current/ahead/unknown and actual owner. |
| UR-18a | P10 PIN-4 actual engine proof, counted once. |
| UR-18b / LA-3 | Existing local fixture plus native paired skew/interruption/recovery and successful retry. |
| LA-1 | Existing selected-install resolver with read-only authority output; no new resolver. |
| LA-5 / LA-6 | Exclusive true local owner and existing repair route; no hosted service takeover. |
| LA-7 | Existing redacted diagnostics for App prepare/recovery failure. |
| UR-R | Shared programme review; every LA row remains in acceptance. |
| Closed/unmerged #178 UR19–31 | Historical proposals, not fresh dispatch block. R0 retention policy maps to P09 IU-19; other genuine residuals map to existing capability/decision/copy/readiness/native-proof owners; broad CI expansion stays later. |

The following historical cards and ledgers preserve their original IDs, evidence and checkboxes. Earlier release numbers, bases, donor hints, “open” snapshots and promotion commands are historical, not current R16 dispatch instructions. Where a retained acceptance obligation appears below, the table names its current owner rather than discarding it. Promised native routes stay unqualified until demonstrated; a named limitation is not automatic acceptance.


Routes: **N** = normal, **X** = very hard, **S** = super hard (see the [run contract](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/run-contract.md)). X and S tasks delegate research, reading, mechanical edits and checks to N helpers, and keep the judgment and the final change.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| UR-15 Remove the systemd 254 floor | S | Plan 29 | agent `update_job*.py`, journey matrix; contract update helper | On systemd 249, the Linux worker runs from an owner-only file with no `$` or `%` expansion. An update started before the change still reconciles. An Ubuntu 22.04 row passes | [ ] |
| UR-16a Helper-protocol schema owned by the Runtime | X | Plan 29 UR-10 | runtime helper-protocol schema; agent helper tests | A JSON Schema (Python on both sides) under `astrid_runtime/`, outside `contract/`; both repos test against it | [ ] |
| UR-16b Update-status schema, kept outside the versioned contract | N | Plan 29 UR-11 | app `client.ts`; update-status schema | The App validates against it, and `schema_digest` is unchanged | [ ] |
| UR-17 Refusal rule | N | Plan 29 UR-1 | app `CopyRefusedInstructions.tsx`, `RuntimeConnectionPanel.tsx`, `RuntimeConnectionPill.tsx`, `copy.ts` | Use the existing shared update decision meanings and reason table; refused cards show update wording only when the installed release is behind | [ ] |
| UR-18a Pinokio update proof | N | — | agent `scripts/pinokio_row_driver.py` (coordinate with Plan 10) | The Pinokio row runs the launcher's own Update action (`update.js`), not a direct installer re-run | [ ] |
| UR-18b Fully local update proof | X | Plan 29 UR-9 | app local-update control tests | A dev:local test drives the in-page updater (no new hosted row) | [ ] |
| LA-1 The launcher asks the Agent where Astrid lives (local review mechanism 1) | X | Plan 29 UR-15, a1 | agent `installation.py` (`--json` entry), app `dev-local-workspace-options.mjs`, `local-update-backend.mjs` | One resolver answers the launcher; the launcher's own path logic is deleted | [ ] not started (Plan 30) |
| LA-2 One status shape and one page operation for local pages (local review mechanism 3) | X | LA-1, UR-15l-2, Plan 30 UR-16b | app `localUpdateStatus.ts`, `updateStatus.ts`, `pageUpdateStatus.ts`, `useInstallerUpdate.ts`, `resolveUpdate.ts` | One status schema for hosted and local; "behind" based on releases, not commit ancestry | [ ] not started (Plan 30) |
| LA-3 Every editor/Runtime skew has a transition (local review L8) | S | LA-1, LA-2 | app `local-update-control.mjs`, `dev-local-workspace.mjs:435-452` | Each editor/Runtime skew state has a defined update transition, tested | [ ] not started (Plan 30) |
| LA-4 One reason table across the Agent and the App (local review) | X | UR-15l-2, Plan 30 UR-16b/UR-17 | agent `outcome.py` (export REASONS as JSON with a schema), app `installerUpdateReasons.ts` | A schema test fails when a reason is added in one place only | [ ] not started (Plan 30) |
| LA-5 Hosted Update now vs a running local launcher | X | LA-1 | runtime `update.py` status (local launcher reason `local-launcher`), app `resolveUpdate.ts` | With dev:local running, astrid.haus shows the local-launcher reason and the `npm run update` line | [ ] not started (Plan 30) |
| LA-6 Define local repair | N | LA-1 | app `AstridUpdatesSection.tsx:159`, `copy.ts`, `dev-local-workspace.mjs:61-73` | A degraded Runtime under dev:local shows one repair line, then restart dev:local | [ ] not started (Plan 30) |
| LA-7 App-half update log | N | UR-15l-2 | app `local-update-checkout.mjs`, `local-update-runner.mjs`, runtime `diagnostics.py` | A failed `npm ci` in prepare appears in Download diagnostics under its own label | [ ] not started (Plan 30) |
| UR-R Up to two independent reviews before closing | S | UR-15–UR-18b and LA-1–LA-7 | all Plan 30 scopes (read-only review) | Same review rounds as [Plan 29](../29-update-and-release/tasks.md#ur-r-review-rounds); findings become rows `UR-R<round>.<n>` directly below this one, done before the next round | [ ] |

## Task details

### UR-15 systemd floor
- **Why the floor exists:** it is there only for `systemd-run --expand-environment=no` (`update_job_platform.py:222`).
- **The fix:** use Windows' approach (`_worker_command`, `update_job.py:1341-1381`). The Linux argv becomes `python -B -X utf8 -I <owner-only job file>`.
- **Effect on in-flight updates:** the worker digest changes, so an update that started before the change must still reconcile (`update_job.py:623, 693, 1279`).
- **Before adding the 22.04 row:** it needs owner approval after a probe.

### UR-16 Contracts
`/v1/update/status` is not in `contract/` today. Adding it there would change `SCHEMA_DIGEST` and switch off `supportsFullV2Commit` in the App (`contract-metadata.ts:22-27`). Keep both schemas outside `contract/`.



## Proposed Release 16 scope reconciliation (25 November 2026)

This is a proposed scoping amendment from [SYN-01](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md); scope, execution and publication remain subject to the existing independent reviews and owner decisions. Existing task progress, accepted decisions and historical evidence remain unchanged. Where historical sequencing differs, the following describes the proposed R16 task-level sequencing; it does not change existing delivery authority.

preserve unchecked rows and LA “not started.” UR-15 accepts P29 UR-R2.5: both launch flags and query/settlement on systemd 249/252, not just one flag removal. UR-16a produces one shared helper schema; UR-16b, LA-2 and LA-4 consume normalized statuses and exact reason mapping. UR-17 uses existing decision meanings for truthful action/refusal, including installed-ahead and unknown; no second `resolveRefusal`. UR-18a discovery starts now, final proof depends on P10 PIN-2/3 and the frozen tuple; UR-18b reuses page→endpoint→launcher fixture. LA-1 read-only selected installation can start now; LA-3 no-op requires **both** actual halves current; LA-5 refuses service takeover; LA-6 repairs the existing route; LA-7 includes redacted App-preparation failures. Qualify ambiguous P29 suffix references, and extend UR-R dependencies from UR-15–18b to **all LA-1–7**. Historical UR19→P09 retained-root policy; UR20→autostart/capability; UR21/22→shared decision; UR23/24/26/28→copy; UR25→Windows proof; UR27/29→bounded readiness; UR30→tuple provenance; broad UR31 CI expansion stays later absent a minimal required witness. Evidence: [SC-30](../../releases/16/evidence/scoping/README.md#receipts), [INV-01](../../releases/16/evidence/scoping/README.md#receipts), [AUD-01](../../releases/16/evidence/scoping/README.md#receipts).
