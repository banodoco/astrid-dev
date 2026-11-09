# 25 — Astrid Cloud generation, phase 1 (local agent, database and files)

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../index.md).

**Vision gaps:** [F-005 — Local projects cannot yet use coherent cloud execution](../../vision/gaps/F-005-local-files-cloud-assist.md) (primary) · [F-002 — safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting: spend, consent and key revocation). This plan covers F-005's cloud *generation* half. The cloud agent session and remote rendering move to [Plan 26](../26-fully-hosted-v2/plan.md), where the agent and renderer run on the cloud workspace. Do not claim F-005 closed on this plan alone.

## Outcome and scope

A creator signs in to Astrid with Discord, buys credits with Stripe (there are no free credits), and creates an **Astrid Cloud key**. They give that key to their local Astrid once, using the same credential path as the fal key. From then on, the agent or the user can run a set of basic generations (image, image edit, upscale, image-to-video) **without their own provider accounts**. The results arrive in the local project exactly as a fal generation does today.

The agent, the project database (local SQLite) and the files stay on the user's machine, as now. Cloud work is limited to the generation and its billing. The same key is the one the cloud workspace uses in [Plan 26](../26-fully-hosted-v2/plan.md), and a local user keeps using it after Plan 26 ships.

**Included:**
- **One Astrid Cloud service, no edge functions** (owner, 9 Nov). The trimmed worker orchestrator grows into the single Astrid Cloud API, a long-lived Python service. It is the only place that holds the provider and Stripe secrets, and the only place that authenticates Astrid Cloud keys. It runs:
  - the public HTTPS API: the queue, uploads, Stripe checkout and webhook, and in [Plan 26](../26-fully-hosted-v2/plan.md) the LLM router and `open-workspace`;
  - the worker loop.
- **Supabase does three things only,** on the team's one live project, **Banodoco** (Reigh's project was deleted):
  - Auth, for Discord sign-in;
  - Postgres, for the tables, row-level security and SQL functions;
  - Storage, for the private bucket.
  - Hivemind's existing edge functions there are untouched. Astrid Cloud adds none.
- **Account:** Discord sign-in through Supabase Auth, and the `users` row, restored from the tagged Astrid App source. An **account page** in astrid-app:
  - reads the balance, the ledger and the key list straight from Supabase, which row-level security limits to the user's own rows;
  - creates and revokes keys through SQL functions;
  - calls the service only to start a Stripe Checkout.
  - The rest of the App stays local and sessionless, so it never needs a login.
- **Credits:** the restored credits ledger, in integer cents. Billing is **debit first, refund on failure**, in one locked SQL function, with a unique spend and refund per task. A task can never overdraw the balance.
- **Astrid Cloud key:** the old personal access token, hardened:
  - hashed at rest and shown once, with a prefix;
  - scope `generate` only, valid for the queue API and input uploads. Scopes are a list, so [Plan 26](../26-fully-hosted-v2/plan.md) adds `llm` to the same key;
  - last-used time and revoke.
  - Keys are minted and revoked only by SQL functions that require the signed-in Discord session, so a key can never mint keys or start checkouts.
- **Astrid Cloud queue API** in the service, shaped like fal's queue (submit, status, result, cancel):
  - submit authenticates the key, debits through the SQL function, and inserts a task row;
  - the task's idempotency key is the **local Runtime task id**, so a retried attempt never submits or charges twice.
- **Worker loop in the same service:** the API half of [reigh-worker-orchestrator](https://github.com/banodoco/reigh-worker-orchestrator/tree/9d9df8cae6f6fd16168f416c8edaa848fa1f4ea0), with its known bugs fixed. It no longer calls edge functions:
  - it claims tasks straight from Postgres with `SKIP LOCKED`;
  - it completes tasks, and refunds failed ones, through SQL functions;
  - it uploads outputs to the private bucket and returns signed URLs.
  - It is driven by **one model table**: family to provider, endpoint, provider cost and the price charged. The price is **provider cost plus a 60% markup**. It adds a Pruna handler next to fal.
- **Agent:** the existing fal (`cloud`) backend gains an **Astrid Cloud route**: a queue origin, the Astrid key, and the upload switch. Existing model rows, storage policies, publication and the local Runtime task are unchanged. The first families' rows (fal and Pruna) are added to `models.yaml`. The rows a key can run are the **Astrid Cloud pack**.
- **Docs and records:** an Astrid Cloud row in `where-things-run.md`, and consent and cost wording.

**Not included:**
- cloud agent sessions, remote rendering, a cloud database or cloud files ([Plan 26](../26-fully-hosted-v2/plan.md));
- auto-top-up: the current version is broken, so it stays off and becomes a follow-up issue;
- Reigh shots, generations rows or timeline placement on completion;
- the GPU half of the orchestrator;
- TTS and other families beyond the first set;
- teams;
- a login inside the local App;
- moving the key into Runtime credential records. That is [Plan 36](../36-one-credential-path/plan.md), which moves this key along with fal's.

## Existing work and decision

Almost everything exists already. See [inputs.md](inputs.md#planning-evidence) for the source trail and the alternatives considered.

- **Account, credits, Stripe and keys:** the Astrid App at tag `pre-cloud-removal` ([5a3ddb1](https://github.com/banodoco/astrid-app/tree/5a3ddb1a1cdfac2a8e26132bccff6aeb95be9dec)) targeted Reigh's Supabase project, which has since been deleted, so these are applied fresh to Banodoco.
  - **Reused as SQL:** the credits ledger with its balance and protection triggers, `user_api_tokens` (to be hashed and scoped), the `users` row created on first sign-in, and the row-level security patterns.
  - **Reused as UI:** Discord sign-in (`useDiscordSignIn`), `CreditsManagement`, `useCredits` and `useApiTokens`.
  - **Ported, not redeployed:** the Deno edge functions `stripe-checkout` and `stripe-webhook` become two service endpoints, keeping:
    - the signature check, with a timestamp tolerance added;
    - the unique-session-id rule;
    - the rounded amount check.
  - **Not restored:** `generate-pat` and `revoke-pat`, which become SQL functions, and `grant-credits`, since there is no welcome bonus.
  - **Task schema:** the tagged `create-task` is retired (it returns 410), so the tasks table and its idempotency index come from [reigh-app](https://github.com/AstridPseudon/reigh-app/tree/06ccc462cd76a8ed425ec24728c541ebf60ab97f), trimmed of Reigh's project, shot and generation columns. Reigh's task edge functions are not carried over; their logic becomes SQL functions and service code.
- **Worker:** the orchestrator's API loop, handler registry and resilient fal submit/poll (it persists the request id for restart) are reused, with its edge-function client replaced by direct Postgres calls. Its dead weight is deleted:
  - the GPU side;
  - banodoco handlers;
  - shadow mode;
  - the legacy fal call.
- **Agent:** `FalBackend` (`astrid/core/generation/backends/fal.py`) and `fal_submit_and_poll` already talk to a fal-shaped queue. Giving them a second origin keeps every `cloud` model row, storage policy (`generate_image/run.py:479`) and publication path as is. Plan 32 already rules that providers stay a `--backend cloud` route for now.
- **Rejected:**
  - **A fal-only proxy with no tasks and no orchestrator.** It is smaller, but the owner wants server-side tasks and a multi-provider worker (fal plus Pruna, later GPU), so the queue API keeps fal's shape over that worker instead.
  - **Supabase edge functions for the API (Reigh's way).** Rejected by the owner on 9 Nov. Edge functions would mean:
    - a second runtime (Deno beside the Python worker);
    - a second place for secrets and key checks;
    - time limits that long LLM streams would hit.
    - The worker is a long-lived service anyway.
  - **A separate backend id or pack.** It needs new model rows, storage policy edits and edits to the generation pack's network policy anyway.
  - **Post-hoc measured billing (Reigh's way).** It allows overdraft, and its spend insert is racy.

## Sequence and readiness

The critical path is:
1. A1, the source and live-project baseline;
2. A2, the Supabase schema on Banodoco: ledger, keys, tasks, and the debit, refund and claim SQL;
3. A4, the service's API: the queue, uploads, and Stripe checkout and webhook;
4. A5, the service's worker loop;
5. A7, the agent route;
6. A9, the end-to-end proof;
7. R, the review.

The account page (A3) and the model table and prices (A6) run alongside. See [tasks.md](tasks.md).

**Owner decisions** are recorded in [inputs.md](inputs.md#owner-decisions). Already decided on 9 Nov:
- D1: the Banodoco Supabase project.
- D3: a 60% markup.
- D4: no welcome credits.

Still open before dispatch:
- D2: the service's repository and deployment. It now covers D6 too: the trimmed orchestrator repository renamed, or a new one, on Railway or similar. The Supabase migrations live with the service.
- D3: the list of fal (and Pruna) models. The owner picks these and need not lock them now; A6 only needs the table and the price rule.
- D5: the "Astrid Cloud" label in the UI and consent.

**Budget:** a capped live proof, roughly $10 of provider spend plus a Stripe test-mode run. Recording this plan authorizes no deployment, migration on the live project or spend.

## Interfaces and handoff

**Consumes:**
- the tagged App source;
- the reigh-app tasks schema;
- the orchestrator API half at the SHAs in [inputs.md](inputs.md#source-identities);
- the Agent's fal backend and model catalog at the current Agent `main`;
- the live Supabase project's actual migration ledger, recorded by A1 before anything is changed.

**Produces** (contracts that [Plan 26](../26-fully-hosted-v2/plan.md) builds on):
1. **The Astrid Cloud account:** a Discord identity, a `users` row and a credits balance in cents.
2. **The Astrid Cloud key contract:** format, scope `generate`, hashed storage and revoke.
3. **The Astrid Cloud service:** one API origin; the queue contract (fal-shaped submit, status, result and cancel); the idempotency rule (one local task id is one cloud task); the debit and refund SQL functions; the key check. Plan 26 adds its LLM router and workspace endpoints to this service.
4. **The model table:** family to provider, endpoint and price.

Plan 26's cloud workspace calls the same API with the same key.

## Completion

On a clean local install, a new user signs in with Discord, starting with a balance of zero. They buy credits in Stripe test mode, create a key and set it with `run-astrid credential set`. They generate an image, an edit, an upscale and an image-to-video through the Astrid Cloud route, and each lands in the local project as a normal generation. The ledger shows one debit per task, at provider cost plus 60%.

**Negative cases:**
- a failed provider task is refunded;
- killing the local Agent mid-generation and restarting produces no second charge or second provider request;
- a zero balance is refused before any provider call;
- a revoked key is refused at once;
- the key cannot mint keys or start a checkout, and nothing outside the service can claim or complete tasks;
- a Stripe test payment credits once, even when the webhook is replayed.

Evidence names the exact SHAs, the Supabase migration list applied, the providers and models used, and the spend. It is not proof of a hosted workspace.
