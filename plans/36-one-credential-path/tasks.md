# Tasks: one credential path

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

**Draft outline only; not executable assignments.** Scope tasks after current-source inspection.

## Task index

| Work area | Route | Depends on | Progress |
|---|---|---|---|
| [Map the credential records and move each secret](#intended-work-and-proof) | TBD | Current-source inspection | Draft; not dispatched |

## Intended work and proof

- Map what the Runtime credential records support today (`credentials_dir`, `controlRemoteCredential`), and what a provider key needs (scope, rotation, revoke).
- Move each secret in the plan's list, with a one-time import.
- Fix or confirm the Codex `auth.json` cleanup on every exit path.
- Proof: a test per secret that it resolves through the credential path and that the old file is ignored after import; a grep for plain env-file reads.

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

| Canonical home | Proposed bounded amendment |
| --- | --- |
| `plans/36-one-credential-path/plan.md`, `inputs.md`, `tasks.md` | Add only a linked prerequisite to S35-4 and the **paid-route adjunct ER-P1** for #1728/#1254/#631: resolve current host credential/ref at admission, rotate safely, no stale environment fallback, protect Windows ACL/redaction/concurrent update. Preserve existing secret owner; no global credentials migration inferred. Ordinary zero-cost ER-2 does not depend on provider-key availability. |
