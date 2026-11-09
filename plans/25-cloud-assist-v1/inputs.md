# Inputs — Astrid Cloud, phase 1

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — In the planning session on 9 Nov the owner set the direction and every decision in the table below. There is no written approval yet. Next: the owner approves this scope PR, and merging it records the approval.

**Prior art:** Ten read-only surveys on 9 Nov, at the SHAs below, covered Reigh billing and keys, Reigh tasks, the worker orchestrator, the App's cloud remnants and its 5 Oct design, Runtime storage and concurrency, the Agent's generation path and remote machinery, the overlapping plans, and outside research. The findings that shape this plan:
- **The tagged App source still has the cloud stack:** the App removed its cloud side on 18 Oct. Tag [5a3ddb1](https://github.com/banodoco/astrid-app/tree/5a3ddb1a1cdfac2a8e26132bccff6aeb95be9dec) keeps the ledger, Stripe, keys and Discord sign-in. Its `create-task` returns 410.
- **Tasks:** working idempotent tasks are in [reigh-app 06ccc46](https://github.com/AstridPseudon/reigh-app/tree/06ccc462cd76a8ed425ec24728c541ebf60ab97f).
- **Reigh keys:** stored in plaintext and accepted by every function (`_shared/auth.ts:136-157`).
- **Reigh billing:** debited after completion, which allows overdraft.
- **The orchestrator** ([9d9df8c](https://github.com/banodoco/reigh-worker-orchestrator/tree/9d9df8cae6f6fd16168f416c8edaa848fa1f4ea0)):
  - has no billing;
  - has a shared worker id and stuck attempts;
  - claims without `SKIP LOCKED`.
- **Retries:** the Runtime re-queues a crashed attempt as a new attempt (`store.py:4093-4135`), so the cloud idempotency key is the local task id.
- **Agent:**
  - `FalBackend` hardcodes `cloud` (`fal.py:260`);
  - storage policies require `execution == "cloud"` (`generate_image/run.py:479`);
  - `models.yaml` has 34 fal rows, 10 with a per-unit `price`;
  - `authority_lint` flags `supabase` identifiers.
- **Runtime:** the Runtime contract has a `controlRemoteCredential` operation (`astrid_runtime_client/generated.py:21`), the credential path [Plan 36](../36-one-credential-path/plan.md) names.
- **Supabase project:** Hivemind already uses `ujlwuvkrxlvoswwkerdf` (`astrid/core/hivemind/executors/_common.py:37`). The owner confirmed it is Banodoco.

**Approach:** Restore the SQL subset from the tag and reigh-app onto Banodoco. Grow the orchestrator into the one Astrid Cloud service, with no edge functions. Give the fal backend an Astrid Cloud route. Hand the key over through the Runtime. Bill per unit, debited first.

Alternatives considered:
- edge functions;
- a separate backend or pack;
- a fal-only proxy;
- billing after completion;
- users pasting keys.

They are rejected in [plan.md](plan.md#existing-work-and-decision).

**Challenge:** Reviewed — an independent advisor critique on 9 Nov checked the first draft against code. It found the retired `create-task`, the attempt-level idempotency flaw, the overdraft race and the over-built separate backend. All its corrections were accepted, except dropping tasks and the worker, which the owner keeps.

**Proof and limits:** The proof is the completion journey in [plan.md](plan.md#completion) on one clean install, with Stripe in test mode and at most $10 of provider spend. It covers fal only. Pruna is not yet checked, and models without a per-unit price are refused until priced.

## Owner decisions

All decided by the owner on 9 Nov.

| ID | Decision |
|---|---|
| D1 | Supabase project: Banodoco, `ujlwuvkrxlvoswwkerdf`, the only live project. Reigh's was deleted |
| D2 | Service: `astrid-cloud`, the trimmed worker orchestrator renamed. It holds the Supabase migrations and deploys on Railway after A3 and A4 pass. No edge functions |
| D3 | Models: the fal models already in the catalog. Each is billed per unit at provider cost × 1.6. The owner picks new models later. Pruna is deferred |
| D4 | No welcome or free credits |
| D5 | Name: **Astrid Cloud**, with a "This computer / Astrid Cloud" choice in onboarding and settings that can be switched back and forth |
| D6 | No pasted keys: Discord sign-in in the App mints a per-device key that goes into the Runtime |
| D7 | Proof budget at most $10 provider spend; 3 review rounds |

## Source identities

| Repository | SHA | Use |
|---|---|---|
| [banodoco/astrid-app](https://github.com/banodoco/astrid-app) | `a0f253ee62a1bb26c004add9822b0bae9e851fa5` | Base: sign-in, settings, onboarding, account page |
| astrid-app tag `pre-cloud-removal` | `5a3ddb1a1cdfac2a8e26132bccff6aeb95be9dec` | Donor: ledger and key SQL, Discord, billing UI, Stripe logic |
| [AstridPseudon/reigh-app](https://github.com/AstridPseudon/reigh-app) | `06ccc462cd76a8ed425ec24728c541ebf60ab97f` | Donor: tasks table and idempotency index |
| [banodoco/reigh-worker-orchestrator](https://github.com/banodoco/reigh-worker-orchestrator) | `9d9df8cae6f6fd16168f416c8edaa848fa1f4ea0` | Base of `astrid-cloud` |
| [banodoco/astrid-agent](https://github.com/banodoco/astrid-agent) | `a105de3a4852cb61b9647dfe2c920118bd29f272` | Base: fal backend, catalog, credentials |
| [banodoco/astrid-runtime](https://github.com/banodoco/astrid-runtime) | `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` | Base: credential records, app-state |

Re-pin to current `main` at dispatch.

## References

- [App cloud-mode overview, 5 Oct](https://github.com/banodoco/astrid-app/blob/a0f253ee62a1bb26c004add9822b0bae9e851fa5/docs/design/cloud-mode-project-overview-2026-10-05.md), the earlier, heavier design.
- fal queue API: <https://fal.ai/docs/model-apis/model-endpoints/queue>.
