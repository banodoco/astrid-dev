# 25 — Astrid Cloud, phase 1: cloud generation (local agent, database and files)

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../index.md).

**Vision gaps:** [F-005 — Local projects cannot yet use coherent cloud execution](../../vision/gaps/F-005-local-files-cloud-assist.md) (primary) · [F-002 — safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting: spend, consent and revocation). This plan is F-005's cloud generation half. The cloud agent and remote rendering are in [Plan 26](../26-fully-hosted-v2/plan.md).

## Outcome and scope

**Generate with: This computer | Astrid Cloud.** Onboarding asks once, and the setting can be switched back and forth at any time. A single generation can also override it.

Choosing Astrid Cloud works like this:
1. The user signs in with Discord in the App.
2. The App gets a key for this device and hands it to the local Runtime. **Nobody pastes a key.**
3. The user buys credits with Stripe. There are no free credits.
4. From then on, the agent and the user run the fal models Astrid already ships without any provider account of their own. Each result lands in the local project exactly as a fal generation does today.

The agent, the project database (local SQLite) and the files stay on the user's machine.

**Pieces:**
- **Supabase (the Banodoco project, `ujlwuvkrxlvoswwkerdf`):** used only for:
  - Auth (Discord);
  - Postgres (tables, row-level security, SQL functions);
  - Storage (a private bucket).
  - No edge functions.
- **The Astrid Cloud service (`astrid-cloud`):** the trimmed worker orchestrator, renamed. It is the one long-lived service and the only holder of provider and Stripe secrets. It runs:
  - the fal-shaped queue API (submit, status, result, cancel), signed uploads, and Stripe checkout and webhook;
  - the worker loop, which claims, completes and refunds tasks in Postgres.
- **Billing per unit:** each model's provider cost per unit (image, second, audio) × the **generation markup**. The markup is a setting in the service, not a constant, and starts at 1.6. Every ledger row records the provider cost, the markup and the units, and the account page shows them. It is charged when the task is submitted, refunded on failure, and can never overdraw. One local task id is one cloud task, so a restart never charges twice.
- **Key:** one per device, hashed at rest, with a scope list (`generate` now; Plan 26 adds `llm`). Revocable per device on the account page. It can't mint keys or buy credits. The App hands it to the local Runtime, and the Agent reads it from there. The Runtime has no record for an outbound secret yet: `controlRemoteCredential` is per remote task. A6 builds that record for this key only, as the first piece of [Plan 36](../36-one-credential-path/plan.md)'s credential path (owner question Q2).
- **Agent:** the existing fal (`cloud`) backend gains an Astrid Cloud route, chosen by the user's setting in Runtime app-state ([Plan 35](../35-one-home-for-user-state/plan.md)). Existing model rows, storage policies and publication are unchanged.
- **App:** Discord sign-in, the Local and Cloud choice in settings and onboarding, and an account page (balance, ledger, buy credits, devices).

**Not included:**
- the cloud workspace, cloud agent, rendering and LLM ([Plan 26](../26-fully-hosted-v2/plan.md));
- Pruna and new models: Pruna is deferred until its API is checked, and the owner picks new models later;
- auto-top-up;
- Reigh's shots and generations side effects;
- the GPU half of the orchestrator;
- teams.

## Existing work and decision

Almost all of this exists. The source trail is in [inputs.md](inputs.md#planning-evidence).
- **Tagged App source:** the Astrid App at tag `pre-cloud-removal` ([5a3ddb1](https://github.com/banodoco/astrid-app/tree/5a3ddb1a1cdfac2a8e26132bccff6aeb95be9dec)) gives:
  - the credits ledger SQL with its triggers;
  - key storage;
  - Discord sign-in;
  - the billing UI;
  - the Stripe logic, which is ported from its Deno functions into the service.
- **reigh-app:** gives the tasks table and its idempotency index ([06ccc46](https://github.com/AstridPseudon/reigh-app/tree/06ccc462cd76a8ed425ec24728c541ebf60ab97f)).
- **reigh-worker-orchestrator:** gives the worker loop, handler registry and restart-safe fal polling ([9d9df8c](https://github.com/banodoco/reigh-worker-orchestrator/tree/9d9df8cae6f6fd16168f416c8edaa848fa1f4ea0)).
- **The Agent:** gives the fal backend and 34 fal model rows, 10 of them already priced per unit.

Rejected:
- edge functions;
- a separate backend or pack;
- billing after completion (it allows overdraft);
- pasting keys;
- a fal-only proxy with no tasks.

## Sequence and readiness

**Three stages:** the account, billing and the service first (it produces what Plan 26 consumes), then the Agent, sign-in and the App, then the proof and review. A review stop (RS1) on the SQL, the queue contract and the Runtime key record comes before anything builds on them or reaches Banodoco.

**Critical path** (about 12 elapsed days): A1 → A2 → RS1 → A14 → A16 → T2 → A10 → R. The service (A3 → A18) and the Agent route (A7) run alongside. A15 waits for [Plan 32](../32-generation-placement-targets/plan.md) T6d's generation settings document. A8 waits for [Plan 20](../20-zero-to-first-image/plan.md)'s "Set up generation" card (P2.3), so it adds one branch to it rather than competing with it. Details and the stage estimates are in [tasks.md](tasks.md).

All the owner's decisions are recorded in [inputs.md](inputs.md#owner-decisions). The live proof spend is capped at **$10**, with Stripe in test mode. Recording this plan authorizes no deployment or spend.

## Interfaces and handoff

**Consumes:** the donors above at the SHAs in [inputs.md](inputs.md#source-identities), the Banodoco project's baseline (A1), and the Agent's fal backend and catalog.

**Produces** (for [Plan 26](../26-fully-hosted-v2/plan.md)):
- the Astrid Cloud account;
- the per-device key and its handoff through the Runtime;
- the service with its queue contract and the debit and refund SQL;
- the per-unit price table;
- the Local and Cloud setting.

## Completion

On a clean install, onboarding offers "This computer" and "Astrid Cloud". The user picks Cloud, signs in with Discord, starts at zero, buys credits in Stripe test mode and never sees a key. They generate an image, an edit, an upscale and an image-to-video from the existing models, each landing in the local project. The ledger shows one charge each, at provider cost × the generation markup, with both visible. They switch to "This computer" and back.

**Negative cases:**
- a failed task is refunded;
- killing the Agent mid-task and restarting means no second charge or provider call;
- a zero balance is refused before any provider call;
- revoking the device on the account page stops it at once;
- an unpriced model is refused;
- a replayed Stripe webhook credits once.

Evidence names the SHAs, the migrations, the models and the spend.
