# Respond to an Astrid bug

**Goal:** understand the failure, get this user working safely as soon as possible, and leave one traceable record—even if the outcome is only an investigation or a one-off local repair.

Use this alongside the existing [development workflow](../skills/astrid-dev/SKILL.md) and [shared run contract](../skills/astrid-dev-shared/run-contract.md). It does not replace their authority, model-routing, testing or review rules.

## Orient yourself

Inspect the **installed versions, selected workspace and actual running processes**, not just repository `main`.

- [**astrid-app**](https://github.com/banodoco/astrid-app): the frontend, served at [astrid.haus](https://astrid.haus) or locally via `npm run dev:local` (usually `127.0.0.1:5180`).
- [**astrid-runtime**](https://github.com/banodoco/astrid-runtime): the local service/API and authoritative workspace—projects, timelines, tasks, events, SQLite, media/CAS and credentials.
- [**astrid-agent**](https://github.com/banodoco/astrid-agent): installer, CLI/SDK, chat, agent integrations and creative packs. Chat may use Astrid, Claude Code, Codex or Hermes; execution may use local engines, providers or remote workers.
- **astrid-dev**: the central incident issue and development coordination. Product PRs belong in their owning repositories.

Both hosted and locally developed frontends connect to the **user's local Runtime**; neither the browser location nor an app checkout tells you where the data or inference lives. Trace the actual frontend → Runtime → agent/pack → execution route.

Find the **selected** Runtime data root from installer records and overrides such as `ASTRID_RUNTIME_DATA_ROOT`. Typical defaults:

| Windows | macOS | Linux |
| --- | --- | --- |
| `%LOCALAPPDATA%\Astrid Runtime` | `~/Library/Application Support/Astrid Runtime` | `$XDG_DATA_HOME/astrid-runtime` (usually `~/.local/share/astrid-runtime`) |

Inspect `runtime/discovery.json`, `runtime/catalog.json`, `runtime/source-profiles/`, the selected `runtime/realms/` database, service/installer logs, and the relevant chat/configuration state. Treat `credentials/` as sensitive. Paths may differ on older or source installations. See [Runtime layout](https://github.com/banodoco/astrid-runtime/blob/main/README.md), [setup](https://github.com/banodoco/astrid-agent/blob/main/docs/setup/SKILL.md) and [execution routes](https://github.com/banodoco/astrid-agent/blob/main/docs/reference/where-things-run.md).

## 1. Investigate

Send parallel **Haiku / N-route sub-agents** after distinct questions:

1. **Evidence:** intended action, last-known-good behavior, reproduction, timeline, errors and relevant logs/doctor output.
2. **Machine and data:** OS, install/upgrade history, exact versions and pins, process/service health, selected data root, database/media state and unusual dependencies.
3. **Code:** trace the interacting paths across the relevant repositories and versions; find invariants, recent changes, existing fixes and tests.
4. **Alternatives:** determine what evidence supports or rules out a shared regression, upgrade-path bug, interrupted state, provider issue or machine-specific fault.

Have the coordinator synthesize findings; use additional N agents to resolve gaps and higher-judgment review when warranted. Distinguish observations, hypotheses and unknowns. **Read-only first**; never disclose secrets or assume a destructive reset is safe.

## 2. Recommend the fastest safe recovery

Produce a short, sanitized `bug-evidence-pack.md` containing:

- **What happened:** symptom, reproduction, timeline, affected versions and environment.
- **What the machine holds:** selected workspace/data root, service and database condition, key redacted evidence and linked code paths.
- **Likely cause:** verified facts, competing explanations, confidence and missing evidence.
- **Get this user working:** concrete, ordered steps, data backup, risks, rollback and a test using the **original failing workflow**. A one-off workaround is fine; never invent a safe recovery.
- **Long-term choice:** whether the repair is reusable, what deeper bug remains, and a proportionate way to test against recurrence.

**Give the pack and recommendation to the user**, ask them to share it with the maintainer, and offer to perform recovery with a rough scope and risk summary. **Obtain approval before changing their installation, data or code.** After an approved recovery, verify the original workflow *and* data preservation; record exactly what changed.

## 3. Track every incident centrally

**Always create or update one issue in [astrid-dev/issues](https://github.com/banodoco/astrid-dev/issues)**—whether fact-finding only, locally repaired, unresolved or fixed upstream. Search for an existing matching issue first. Use [the issue template](../templates/bug-issue.md).

The issue is the durable record of the failure, evidence pack, current recovery advice, actual one-off changes, upstream decision and **every related PR** (repo, link, purpose, status). Link back to this issue from each PR. Update it as the situation changes; don't open separate issues for each stage.

Public reports must be sanitized and user-approved. If you lack permission to post or the user has not approved sharing details, **prepare a ready-to-post issue** and ask for the missing authorization—never publish private local state.

## 4. Fix the underlying problem only when warranted

After restoring the user, decide independently:

- **Reusable and properly engineered:** propose a focused product PR using [the PR template](../templates/bug-pr.md).
- **Machine-specific workaround:** document it in the central issue; do not upstream it merely because it worked.
- **Systemic but bigger:** have an Opus/Astra-level reviewer challenge the smallest sound design before implementation; avoid disproportionate v0 infrastructure.

Follow the existing [Iterate workflow](../skills/astrid-dev-iterate/SKILL.md), [routing bindings](../skills/astrid-dev-shared/run-contract.md#routing-and-bindings), focused proof and authorized review/promotion paths. Update the central issue with links to all PRs across Runtime, Agent, App or other repositories, plus results and remaining limitations.

**Done means:** the user has the evidence pack, a safe recovery recommendation (and verified result if performed), and a central issue URL or ready-to-post draft. Any code PRs are cross-linked; no unverified success is claimed.
