# Tasks: one credential path

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
