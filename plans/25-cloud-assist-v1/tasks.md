# Tasks — Astrid Cloud, phase 1

[Plan](plan.md) · [Inputs](inputs.md)

**Critical path:**
1. A1;
2. A2;
3. A3;
4. A4;
5. A7;
6. A10;
7. R.

A5 runs alongside A2, A6 after A2, A8 after A7 and Plan 20's onboarding work, and A9 after A8.

No deployment, Banodoco migration or spend happens before the owner approves this scope PR. The proof spend is capped at $10.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| A1 Baseline of Banodoco: applied migrations, the Discord provider and callback URLs, buckets, and Hivemind's tables and functions. Lists the SQL to restore and any name collisions | N | — | read-only; a baseline note linked from inputs.md | The note lists the migrations, Hivemind's objects, the restore list and the renames | [ ] |
| A2 Schema and SQL on Banodoco:<br>• `users` on first Discord sign-in, starting at zero;<br>• ledger and triggers;<br>• per-device keys, hashed with a scope list, minted and revoked by SQL functions that need the session;<br>• tasks with a local-task idempotency index;<br>• debit at submit (locks the user row, never below zero);<br>• refund on failure;<br>• `SKIP LOCKED` claim;<br>• row-level security | S | A1 | `astrid-cloud/supabase/migrations` | SQL tests on a local Supabase:<br>• concurrent debits never overdraw;<br>• refund once;<br>• no double claim;<br>• keys only minted with a session;<br>• other users' rows invisible | [ ] |
| A3 Service API on one HTTPS origin:<br>• fal-shaped submit, status, result and cancel (key check, debit, task insert, signed result URLs);<br>• signed uploads;<br>• Stripe checkout (session required) and webhook (timestamp tolerance, rounded amount, unique session) | S | A2 | `astrid-cloud` API module | Service tests:<br>• the same idempotency key gives one task and one charge;<br>• zero balance and unpriced models are refused before a task exists;<br>• a revoked key is refused;<br>• a replayed webhook credits once | [ ] |
| A4 Worker loop in the service:<br>• Postgres claim, complete and refund;<br>• the fal handler for every priced catalog row;<br>• outputs to the private bucket.<br>Deletes the GPU side, banodoco, shadow mode, the legacy fal call and the edge-function client. Fixes the env names, worker ids and stuck attempts | X | A2, A5 | `astrid-cloud` worker module | Recorded-fixture handler tests; a two-worker claim test; live fal tasks inside the cap | [ ] |
| A5 Per-unit price table: every catalog fal row gets its provider cost per unit; the charge is always cost × the generation markup (a service setting, starting at 1.6), rounded up to a cent, and stored with the cost and markup on the ledger row; unpriced rows are not served. One source, checked against `models.yaml` | N | A1 | `astrid-cloud` price table; `price` fields in `astrid-agent/astrid/core/model_catalog/models.yaml` | Tests: the charge equals cost × the current markup; changing the setting changes new charges only; the server and catalog agree; an unpriced row is refused | [ ] |
| A6 Key handoff through the Runtime, no paste:<br>• after Discord sign-in the App mints a device key and stores it with the Runtime's credential records (`controlRemoteCredential`, the Plan 36 path);<br>• the Agent's `astrid_cloud` credential reads it from the Runtime;<br>• sign-out and revoke remove it | X | A2 | `astrid-runtime` credential record for this key; `astrid-agent/astrid/core/util/credentials_scope.py`; `astrid-app/src` sign-in | Tests:<br>• sign-in leaves a working key in the Runtime and none in files or the browser;<br>• the Agent reads it;<br>• sign-out removes it | [ ] |
| A7 Agent route and setting:<br>• the `cloud` backend gains the Astrid Cloud route (service origin, the A6 key, uploads, origin allowed by `_validate_fal_queue_url`);<br>• route selection from the user's setting in Runtime app-state, overridable per generation;<br>• generation pack network policy;<br>• no `supabase` identifiers | X | A3, A6 | `astrid-agent` `backends/fal.py`, `util/http.py`, `packs/generation/pack.yaml`, setting read | Tests against a fake queue: publishes like fal; restart re-uses the cloud task; a missing key or revoked device gives a clear refusal; `authority_lint` passes | [ ] |
| A8 Local and Cloud choice: onboarding and App settings offer "This computer / Astrid Cloud", switchable any time, written to Runtime app-state; the account page shows balance, ledger, buy credits and devices | N | A6, A7, Plan 20 onboarding | `astrid-app/src` settings, onboarding and account route (restored billing UI); the Plan 20 onboarding skill's Cloud branch | Playwright: choose Cloud in onboarding, sign in, buy (test mode), generate, switch to This computer and back | [ ] |
| A9 Copy: the choice, cost line (provider cost, markup, balance), refusals, devices; where-things-run and credentials docs | T | A8 | App strings; `astrid-agent/docs/reference/where-things-run.md`, `credentials.md` | Copy review against the principle that the user chooses where work runs, what is shared and what it costs | [ ] |
| A10 End-to-end proof of the [completion journey](plan.md#completion) and its negative cases, at most $10 | X | A4, A8, A9 | read-only on product code; an evidence note | Evidence note with SHAs, migrations, models, ledger rows and spend | [ ] |
| R Review rounds (3) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md). Findings become rows `R<round>.<n>` below this one | [ ] |

Checks use the [shared worker environment](../../env/README.md). Each card gains literal commands at dispatch.
