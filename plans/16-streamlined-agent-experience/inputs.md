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
| Agent PR #109 | Sandbox account/service integration precedent | [PR #109](https://github.com/banodoco/astrid-agent/pull/109) | Verify exact retained output and source identity at setup. |

The intended extension is one owned implementation location in one repository, with onboarding, app, and execution host consuming the definition rather than parallel lists and provider-specific switches. This allows generic consumer plumbing while establishing the contract; afterward a representative agent should not need handwritten provider edits across repositories. Preserve the distinction between signing into an agent/provider and connecting the local Astrid Runtime. Keep credentials and private logs out of plans.

## Constraints

First-increment account/provider flows and “path runs” need clarification. Existing routes remain until resolved. Follow [shared run policy](../../skills/astrid-dev-shared/run-contract.md) for source verification, execution, review, and publication; planning this draft does not authorize product work.
