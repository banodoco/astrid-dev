---
name: astrid-dev-bugfix
description: Investigate reported Astrid failures, reproduce UI issues in a browser when appropriate, restore the user's working setup safely, and track evidence and upstream fixes in astrid-dev.
---

# Bug fixing

**Outcome:** understand the failure, recommend the fastest safe way to restore this user's actual workflow, and leave one central incident record—even when no code is changed. **A bug is an issue, not a new project**, unless it reveals a separate independently useful outcome.

Read [the development entrypoint](../astrid-dev/SKILL.md), [shared run contract](../astrid-dev-shared/run-contract.md), and relevant product repository instructions. Use their existing model bindings, authority, focused checks and review rules. This skill owns the **user-incident path**, not a second implementation/release workflow.

## Locate the running system

Confirm installed versions, exact source pins, frontend mode and selected workspace before diagnosing against `main`.

- [astrid-app](https://github.com/banodoco/astrid-app): frontend at [astrid.haus](https://astrid.haus) or a local source editor (often `127.0.0.1:5180`).
- [astrid-runtime](https://github.com/banodoco/astrid-runtime): local daemon/API and authoritative projects, tasks, timelines, events, media/CAS, SQLite and credentials.
- [astrid-agent](https://github.com/banodoco/astrid-agent): installer, CLI/SDK, chat, agent integrations and creative packs. Chat may use Astrid, Claude Code, Codex or Hermes; generation may run locally, at a provider or on a remote worker.

Both frontend modes normally connect to the user's **local Runtime**, not a website-hosted project database. Identify the actual browser → Runtime → agent/pack → execution path; a source checkout is not the live workspace.

Resolve the *actual* Runtime data root from installer selection, configured arguments and `ASTRID_RUNTIME_DATA_ROOT`. Common defaults: Windows `%LOCALAPPDATA%\Astrid Runtime`; macOS `~/Library/Application Support/Astrid Runtime`; Linux `$XDG_DATA_HOME/astrid-runtime` (usually `~/.local/share/astrid-runtime`). Check the selected realm under `runtime/realms/`, `runtime/discovery.json`, `runtime/catalog.json`, `runtime/source-profiles/`, process/service state, installer and service logs. Keep `credentials/`, tokens and private project content confidential; never assume defaults apply to a source or older installation.

References: [Runtime](https://github.com/banodoco/astrid-runtime/blob/main/README.md) · [Setup](https://github.com/banodoco/astrid-agent/blob/main/docs/setup/SKILL.md) · [Where execution runs](https://github.com/banodoco/astrid-agent/blob/main/docs/reference/where-things-run.md).

## Investigate and reproduce

Start with the original failing user journey, observed evidence and a source-level hypothesis. For ambiguous or cross-repository incidents, delegate bounded **N-route** investigations of environment, code paths or competing causes when helpers are available. Do not launch four parallel agents for a simple reproducible failure; scale the investigation to uncertainty and impact. Treat hypotheses as hypotheses.

**If the failure involves the frontend, use an available browser to reproduce it when appropriate.** Prefer the user's actual frontend route: `astrid.haus` or their local editor. Capture sanitized steps, expected vs observed behavior, the URL/build, screenshot or recording if useful, browser console/network failures and Runtime health/handshake correlation. Compare hosted/local modes only if it helps isolate the bug. **A remote browser may not reach the user's localhost or credentials**; don't substitute an unrelated healthy environment and call it a reproduction. If access is unavailable, document what is blocked and use other evidence.

Investigate read-only first. Before any action that could alter projects, machine setup, credentials or paid workloads, state its effects and obtain approval. Never casually wipe/reinstall the workspace or expose private diagnostics.

## Deliver a recovery recommendation

Create a concise, sanitized `bug-evidence-pack.md`:

1. **Observed failure:** goal, reproduction (including browser evidence where applicable), environment and timeline.
2. **State and evidence:** installed pins, selected workspace/database, relevant logs, affected code paths and links.
3. **Root cause:** established facts, competing explanations, uncertainty and whether widespread, upgrade-specific or machine-specific.
4. **Get the user working ASAP:** ordered recovery steps, required backup, risks, rollback and verification against the **original failing workflow**. One-off local repairs are allowed; do not present an unsafe guess as a solution.
5. **Upstream decision:** whether to contribute the quick fix, build a deeper solution or defer it, plus minimal regression proof that would prevent recurrence.

Give the user the pack and a practical recovery recommendation; invite them to share it with the maintainer. Offer to apply recovery, with a rough effort and risk summary, **only with approval**. If approved, verify the user's original journey and data preservation and record exactly what changed.

## One issue for every incident, not a project

Search for duplicates, then **file or update one [bug issue](../../docs/contribution-workflow.md#issues) in banodoco/astrid-dev**, whether the result is fact-finding, a one-machine workaround or an upstream fix. Post the incident record (the five-part pack above, redacted) as a comment on it, with links to **every related product PR** with its repository, purpose and status. Every PR must link back to this issue. If public sharing isn't authorized or the evidence cannot be sanitized, prepare a ready-to-post issue and obtain approval instead of publishing.

## Upstream only when justified

A proven reusable repair may become a focused PR; a machine-only workaround stays documented in the issue. For a structural fix, investigate existing patterns with N-route helpers and seek high-judgment architectural challenge against overengineering. Then use [Iterate](../astrid-dev-iterate/SKILL.md) for authorized implementation and focused checks; follow the [shared run contract](../astrid-dev-shared/run-contract.md) for routing/review and [Release](../astrid-dev-release/SKILL.md) for integration/promotion where applicable. Use the [PR template](../../templates/product-pr/bug.md). Cross-link PRs and verified results in the central issue.

**Done:** the user has evidence and a safe recovery proposal (plus verified outcome if attempted), and the incident has a central issue URL or a publish-ready draft. Never claim a frontend or machine is fixed unless the original failure was actually verified.
