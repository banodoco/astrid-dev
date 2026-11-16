# Inputs: Streamlined agent setup and execution

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| Astrid app | TBD at start | TBD at start | None verified | TBD at start | `pre-main` if confirmed by shared policy |
| Astrid agent | TBD at start | TBD at start | None verified | TBD at start | `pre-main` if confirmed by shared policy |

Historical observations below are leads, not live bases. Recover current branches, SHAs, retained work, predecessor records, candidate branches, and destination before execution. Confirm `pre-main` exists rather than assuming it.

## References and evidence

| Source | What it establishes | Identity or link | Limits / missing information |
|---|---|---|---|
| App local inspection | Existing agent choices, readiness, sign-in/model model in `src/integrations/astrid/localAgents.ts`; connection/session APIs in `src/integrations/astrid/acpRoutes.ts`; setup and Runtime connection in `src/app/onboarding/WelcomeLocalSetup.tsx` and `WelcomeConnection.tsx` | Snapshot `2958bacea3e3c7961788fa9c625dd9db0be282de` | Read-only historical snapshot; recheck current source |
| Agent local inspection | Local-agent host/ACP bridge in `astrid/chat/`; skills and capability execution in `astrid/mcp_server.py` and `astrid/omp_invoke.py` | Snapshot `d38edf434a575f3aed941c516fe2a5338135820b` | Read-only historical snapshot; recheck current source |
| Agent PR #112 — Octop local agent integration | Closest precedent; inspected at head `c7444ad3be79569715fe5d36d6b7cce0f801b4c0`. Eighteen changed files: eight implementation/build files and ten test or smoke files. Integration touches identity/catalog metadata, discovery/sign-in probing, launch routing, skills sync/harness registration, and rebuilt bundle. | [PR #112](https://github.com/banodoco/astrid-agent/pull/112) | Distinguish generated output and useful coverage from duplicated handwritten work; raw file count is not the objective. Current source correspondence unverified. |
| Agent PR #110 — DeepSeek Harness local chat agent (contributed work) | A second hand-edited agent integration: DeepSeek Harness as a local chat agent. Eighteen changed files; recorded at head `f98ffaaf6fba471daa0f71d0ee2a942eea4e8078`. Closed unmerged on 2026-11-16; the contributor's branch stays. | [PR #110](https://github.com/banodoco/astrid-agent/pull/110) | Not merged; the agent is to come in through this plan's one place to add an agent. Current source correspondence unverified. |
| Agent PR #111 — developer guide for connecting DeepSeek Harness (contributed work) | The developer guide that goes with #110; recorded at head `3472959a1195ef524f62b1f27caf22929f763210`. Closed unmerged on 2026-11-16. | [PR #111](https://github.com/banodoco/astrid-agent/pull/111) | Describes the hand-edited route; rewrite against the one place to add an agent. |
| App PR #126 — DeepSeek Harness row in the agent setup card (contributed work) | The app side of #110: a DeepSeek Harness row in the agent setup card; recorded at head `04f96a51cf26f7e5eb28678565db0330f5163300`. Closed unmerged on 2026-11-16. | [PR #126](https://github.com/banodoco/astrid-app/pull/126) | Not merged; the app should read the definition, not a hand-added row. |
| App PR #127 — Octop in the setup card and agent identity (contributed work) | The app side of #112: Octop in the setup card and agent identity; recorded at head `be675847ffa3b7417cc027e60901578c7eb9635e`. Closed unmerged on 2026-11-16. | [PR #127](https://github.com/banodoco/astrid-app/pull/127) | Not merged; same limit as #126. |
| Agent PR #109 | Sandbox account/service integration precedent | [PR #109](https://github.com/banodoco/astrid-agent/pull/109) | Verify exact retained output and source identity at setup. |

The intended extension is one owned implementation location in one repository, with onboarding, app, and execution host consuming the definition rather than parallel lists and provider-specific switches. This allows generic consumer plumbing while establishing the contract; afterward a representative agent should not need handwritten provider edits across repositories. Preserve the distinction between signing into an agent/provider and connecting the local Astrid Runtime. Keep credentials and private logs out of plans.

## Decisions

- 2026-11-16: the owner said both agents, Octop and DeepSeek Harness, are wanted in Astrid, through this plan's one place to add an agent rather than by merging the hand-edited integrations. The five pull requests (Agent #112, #110 and #111, App #126 and #127) were closed and are recorded above. When this plan joins a release, its manager brings the work into the plan branch by merging those commits, or asks the contributors to reopen against the plan branch.

## Constraints

First-increment account/provider flows and “path runs” need clarification. Existing routes remain until resolved. Follow [shared run policy](../../skills/astrid-dev-shared/run-contract.md) for source verification, execution, review, and publication; planning this draft does not authorize product work.
