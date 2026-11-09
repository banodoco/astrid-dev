# Inputs — Astrid Cloud generation, phase 1

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — On 9 Nov the owner described in a planning session the two-phase direction recorded here. Phase 1 has Discord sign-in, Stripe credits and an API key. The local SQLite task is mirrored to Supabase and processed by the trimmed Reigh worker orchestrator across fal and Pruna. The agent, database and files stay local. The owner agreed the split into this plan and [Plan 26](../26-fully-hosted-v2/plan.md). The owner later decided D1, D3 (the markup) and D4 in the same session. There is no traceable written approval yet. The owner also decided against edge functions: one Astrid Cloud service, with Supabase used only for Auth, Postgres and Storage. Next: the owner reviews this scope PR and answers D2 and D5, and picks the model list for D3 when ready.

**Prior art:** Ten read-only surveys on 9 Nov, at the SHAs under [Source identities](#source-identities), covered:
- the Reigh billing, Stripe and personal-access-token code;
- the Reigh Supabase task queue;
- the worker orchestrator;
- the App's 5 Oct cloud-mode design and what is left in the App;
- Runtime storage and its concurrency;
- the Agent's generation path;
- the Agent's remote-machine machinery;
- the overlapping astrid-dev plans;
- outside research on fal, Pruna and Turso.

The findings that shape this plan:
- **Cloud side removed from the App:** the App's cloud side was removed on 18 Oct. Tag `pre-cloud-removal`, [5a3ddb1](https://github.com/banodoco/astrid-app/tree/5a3ddb1a1cdfac2a8e26132bccff6aeb95be9dec), keeps 476 migrations, Stripe, credits, personal access tokens and Discord sign-in, but its `create-task` returns 410 (retired).
- **Task functions:** the working idempotent task functions are in [reigh-app 06ccc46](https://github.com/AstridPseudon/reigh-app/tree/06ccc462cd76a8ed425ec24728c541ebf60ab97f) (`supabase/functions/create-task/index.ts:230-262`).
- **Supabase projects:**
  - both point at Reigh's Supabase project, `wczysqzxlwdndgxitrvc`. The owner says that project has been deleted, so nothing is restored to it;
  - the team's one live project is **Banodoco**;
  - the Agent's Hivemind already uses project `ujlwuvkrxlvoswwkerdf` (`astrid/core/hivemind/executors/_common.py:37-41`). That is probably Banodoco, and A1 confirms it.
- **Personal access tokens:** stored in plaintext, and every authenticated function falls back to accepting one (`_shared/auth.ts:136-157`).
- **Billing:** debited after completion, with a racy spend insert and possible overdraft. Auto-top-up's trigger rate-limits itself.
- **Orchestrator problems** ([9d9df8c](https://github.com/banodoco/reigh-worker-orchestrator/tree/9d9df8cae6f6fd16168f416c8edaa848fa1f4ea0)):
  - no billing code;
  - mismatched env names;
  - a shared default worker id, so its orphan reset fights other replicas;
  - tasks at three or more attempts are stuck;
  - the claim has no `SKIP LOCKED`, so two workers can claim the same task.
- **Easy to extend:** a fal model is about 60 lines, and a new provider is about a day.
- **Agent:** `FalBackend` hardcodes the `cloud` backend (`fal.py:260, 563`). Storage policies require `execution == "cloud"` (`generate_image/run.py:479`). `authority_lint` flags `supabase` identifiers in product code.
- **Runtime:** a crashed attempt is re-queued as a new attempt (`store.py:4093-4135`, `LEASE_SECONDS = 30`), so the idempotency key must be the task id, not the attempt id.

**Approach:**
- **Reuse:** restore the bounded SQL subset from the tag (account, credits, keys) and reigh-app (tasks). Port the Stripe checkout and webhook logic into the service. Add no edge functions.
- **Queue API:** put a fal-shaped queue API in front of the tasks, so the Agent's existing `cloud` backend only gains an origin and a key.
- **Service:** grow the orchestrator's API half into the one Astrid Cloud service: the public API plus the worker loop, talking to Postgres directly, trimmed and table-driven.
- **Billing:** debit first, refund on failure.

Alternatives considered:
- **A fal-only proxy with no tasks or worker:** smaller, but loses multiple providers and the owner's server-side task model.
- **A separate `astrid_cloud` backend or pack:** needs new model rows, policy edits and edits to the generation pack anyway.
- **Supabase edge functions for the API and worker calls (Reigh's way):** rejected by the owner on 9 Nov. They add a second runtime and secret store, and time limits for long streams, when the worker is a long-lived service anyway.
- **Doing nothing:** users keep needing their own fal key.

**Challenge:** Reviewed — an independent advisor critique on 9 Nov checked the draft against code. It found:
- the retired tagged `create-task`;
- the attempt-level idempotency flaw;
- the overdraft race;
- the over-built separate backend.

It proposed the fal-shaped facade and debit-first billing. All of these were accepted. Its proposal to drop the tasks and the orchestrator was rejected per the owner's stated direction, and is recorded above as an alternative.

**Proof and limits:** The proof is the completion journey in [plan.md](plan.md#completion) on one clean local install, with Stripe in test mode and a capped live provider spend. It runs on one Supabase project and the first families only. Limits:
- no claim about Reigh users sharing the ledger;
- no claim about rendering, a cloud agent or a cloud database;
- live Supabase state is unknown until A1 records it.

## Owner decisions

| ID | Decision | Recommendation |
|---|---|---|
| D1 | Supabase project | **Decided (owner, 9 Nov):** the live **Banodoco** project, the only one. Reigh's project was deleted. The restore subset must not collide with Hivemind's existing tables and functions there |
| D2 | Home and deploy of the Astrid Cloud service (merged with the former D6) | Recommendation: rename `reigh-worker-orchestrator` to `astrid-cloud`, keep its API half, and hold the Supabase migrations in it. Deploy on Railway, where it already has config. Deploy only after A4 and A5 pass |
| D3 | Markup, models and prices | **Decided (owner, 9 Nov):** price = provider cost × 1.6, a 60% markup. **Open:** the owner picks a set of fal models (and any Pruna ones) later; this is not locked now. A6 builds the table and the price rule, seeded with whatever list the owner gives at dispatch |
| D4 | Welcome credits | **Decided (owner, 9 Nov):** none. New accounts start at zero and buy credits |
| D5 | Label: a route under `cloud` ("fal via Astrid Cloud") or its own name in the UI and consent | Its own name, **Astrid Cloud**, in consent and cost text. In code, a route of the `cloud` backend |

## Source identities

| Repository | SHA | Use |
|---|---|---|
| [banodoco/astrid-app](https://github.com/banodoco/astrid-app) | `a0f253ee62a1bb26c004add9822b0bae9e851fa5` (main, 9 Nov) | Base for the account page |
| astrid-app tag `pre-cloud-removal` | `5a3ddb1a1cdfac2a8e26132bccff6aeb95be9dec` | Donor: Supabase account, credits, Stripe, keys, Discord, billing UI |
| [AstridPseudon/reigh-app](https://github.com/AstridPseudon/reigh-app) | `06ccc462cd76a8ed425ec24728c541ebf60ab97f` | Donor: tasks table and idempotency index (its edge functions are not carried over) |
| [banodoco/reigh-worker-orchestrator](https://github.com/banodoco/reigh-worker-orchestrator) | `9d9df8cae6f6fd16168f416c8edaa848fa1f4ea0` | Donor: API worker |
| [banodoco/astrid-agent](https://github.com/banodoco/astrid-agent) | `a105de3a4852cb61b9647dfe2c920118bd29f272` | Base: fal backend, model catalog, credentials |
| [banodoco/astrid-runtime](https://github.com/banodoco/astrid-runtime) | `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` | Unchanged; task and publication semantics consumed |

Re-pin to current `main` at dispatch. The live Supabase migration ledger is an unknown until A1 records it.

## References

- [App cloud-mode overview, 5 Oct](https://github.com/banodoco/astrid-app/blob/a0f253ee62a1bb26c004add9822b0bae9e851fa5/docs/design/cloud-mode-project-overview-2026-10-05.md), the earlier, heavier design. Its billing direction (one prepaid balance) is kept. Its per-conversation sandboxes and per-user Turso are not.
- [Plan 32](../32-generation-placement-targets/plan.md): providers stay a `--backend cloud` route. [Plan 36](../36-one-credential-path/plan.md): later moves this key into Runtime credential records.
- fal queue API: <https://fal.ai/docs/model-apis/model-endpoints/queue>. Pruna hosted API: <https://docs.api.pruna.ai/>. The Pruna request and response shape is unverified, so A5 confirms it first.
