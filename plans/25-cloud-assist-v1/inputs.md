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
- **Runtime:** there is no record for an outbound secret. `controlRemoteCredential` is per remote task (see the ambiguity pass below), so the key's home is new work in A6.
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
| D3 | Models: the fal models already in the catalog. Each is billed per unit at provider cost × a markup. The markup is a setting per category, starting at 1.6 for generations; the owner may lower it. Each ledger row shows the cost and the markup. The owner picks new models later. Pruna is deferred |
| D4 | No welcome or free credits |
| D5 | Name: **Astrid Cloud**, with a "This computer / Astrid Cloud" choice in onboarding and settings that can be switched back and forth |
| D6 | No pasted keys: Discord sign-in in the App mints a per-device key that goes into the Runtime |
| D7 | Proof budget at most $10 provider spend; 3 review rounds |

## Reviews

- **Final review (R):** at most 3 rounds, agreed by the owner (D7). The plan spans four repositories plus a service, takes money and holds a credential, so the run contract's guide gives 3.
- **Review stop RS1, after A2 and A6 (and A2's `docs/api.md`):** recommended at most 1 round. Pending — the owner has not yet agreed it. Next: the owner agrees or removes it in this scope PR. **Why:** A3, A4, A11, A7, A13, A14 and A16 all build on the SQL functions, the queue contract and the Runtime secret record, and Plan 26 B5, B10 and B11 consume them. A late finding (for example the idempotency scope, an overdraw path, or a key readable through the door) would mean redoing up to seven tasks, and after A18 it would be on a live project with real fal spend. RS1 clears before anything is applied to Banodoco.

## Ambiguity pass (9 Nov, task cards)

Done by reading the source at the SHAs below. Resolved from code or from the owner's decisions; each resolution is in the task card named.

**Corrections to the first draft:**
- **There is no Runtime record for an outbound key today.** `controlRemoteCredential` is per-task remote-worker credential control (Runtime `contract/openapi/workspace-v1.yaml:767-773`, actions `:1132-1140`). The `<data-root>/credentials/` store holds inbound bearer tokens for Runtime actors (`runtime_protocol/auth.py:16-17`, `server.py:725-739`). So A6 builds the first one, limited to the `astrid_cloud` name (Q2).
- **9 `cloud` rows are priced, not 10.** The tenth `price` in `models.yaml` is `minimax-music-3.0` on WaveSpeed. No image-to-video row is priced, and the completion journey needs one (A5).
- **One local task id can be more than one cloud task.** The Runtime's explicit retry re-queues the same task id (`runtime_protocol/service.py:8111-8149`). So the idempotency key is unique only among live cloud tasks: a crash restart reuses the task, and a deliberate retry after a refunded failure charges again (A2).
- **reigh-app's idempotency index is global** (`supabase/migrations/20260213200001_task_idempotency_key.sql:12-14`). Here it is per account (A2).
- **The orchestrator is not a trim.** It claims, completes and fails tasks only through edge functions (`api_orchestrator/task_utils.py:20-27`, `:208-343`) and has no HTTP API. Its handlers are per Reigh task type (`task_handlers.py:22-45`). Kept: the resilient fal tracking (`fal_utils.py:81-102`, `:438-483`). The API, the database layer and one generic handler are new (A12, A3, A4).
- **No task id reaches the fal backend.** The host passes a `task_identity` input to actions that declare it (Agent `astrid/core/execution/generic_host.py:1551-1554`); the generation actions don't yet (A7).
- **The fal path accepts only fal's queue origin** (`astrid/core/util/http.py:79-106`) and uploads with the user's fal key (`:369-460`), so the route needs an allowed-origin parameter and its own upload (A7).
- **App `main` has no Supabase code in `src`;** only the dependency remains (`package.json:170`). Sign-in is restored from the tag (A14).

**Resolved without the owner:**
- **Tables live in their own `astrid_cloud` schema,** and accounts are created by the App's first call, not a trigger on `auth.users`. Banodoco is shared with Hivemind (`astrid/core/hivemind/executors/_common.py:37-41`), so nothing of ours touches its objects, and rollback is one `drop schema` (A2, A18).
- **The Agent talks only to the service origin.** Uploads and results pass through it, because `authority_lint` flags `supabase` in product code and journey logs (`scripts/reshape/authority_lint.py:90`, `:1365-1367`) (A3, A7).
- **The key is write-only from the App and the door;** only the pack-host actor reads it (Runtime `daemon.py:31`, `door.py:190`), and no backup or export carries it (A6). The host reads it only from the Runtime, with no file or environment fallback, so it is never pasted (A13).
- **The setting lives in Plan 32 T6d's generation document** (`/v1/app-state/user/generation`), as the field `generate_with`. App-state is keyed by actor (`service.py:4797-4803`), so A15 first checks that the App and the CLI share one (A15).
- **Choosing Astrid Cloud wins over a user's own `FAL_KEY`,** because the user chose it (D5). This computer keeps today's behaviour, including fal-direct with the user's key. Cloud never silently falls back to local (A15).
- **Units come from the request,** and a price must be a ceiling for the parameters the service accepts, or the row stays unpriced (A3, A5).
- **Cancel refunds only before the provider call.** Revocation refuses the next request at once, because each request checks the key with no cache (A2, A3).
- **The $10 cap is enforced in the service:** a daily provider-spend cap and, while Stripe is in test mode, an allowlist of accounts. Otherwise anyone could buy test-mode credits and spend real fal money (A2, A18).
- **Live mode is outside this plan.** Completion is in Stripe test mode. Switching to live mode and opening the allowlist is a later release decision.
- **Missing worker scripts:** `env/` has nothing for `astrid-cloud` (Python plus Postgres), the Runtime, or the App. E1 adds them there, not in this folder.

## Owner questions

- **Q1 — Accounts and access for the live steps.** Pending — A1, A18 and A10 need them. Next: the owner provides, at dispatch:
  - (a) how a worker reads (A1) and writes (A18) Banodoco: a Supabase access token saved as a network secret for `api.supabase.com`, or the owner runs those steps. The token also reaches Hivemind's objects;
  - (b) the Stripe test-mode account and webhook secret;
  - (c) the Railway project;
  - (d) the fal account the service bills to;
  - (e) the service's hostname (proposed `cloud.astrid.haus`), which the Agent pins in code and in the pack's network policy;
  - (f) the Discord accounts on the test-mode allowlist.
- **Q2 — A6 builds the first piece of Plan 36.** Pending — [Plan 36](../36-one-credential-path/plan.md) is a draft and hasn't mapped the Runtime's records. Next: the owner confirms that A6 builds the record for `astrid_cloud` only and Plan 36 widens it later, or orders Plan 36's mapping first (which adds its time to the critical path).
- **Q3 — RS1.** Pending — see [Reviews](#reviews). Next: the owner agrees 1 round, or drops the stop.

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

- The A1 baseline note, when A1 has run.
- [App cloud-mode overview, 5 Oct](https://github.com/banodoco/astrid-app/blob/a0f253ee62a1bb26c004add9822b0bae9e851fa5/docs/design/cloud-mode-project-overview-2026-10-05.md), the earlier, heavier design.
- fal queue API: <https://fal.ai/docs/model-apis/model-endpoints/queue>.
