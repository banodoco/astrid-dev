# Release 12 — Task list

[Release 12](../12.md) · Reference: [Plan 29 task record](../../plans/29-update-and-release/tasks.md), [evidence](../../plans/29-update-and-release/evidence/r12/), [takeover note](../../docs/handoffs/2026-11-11-track-a-machine-takeover.md) · [Manager brief](../../docs/handoffs/2026-11-11-release-12-manager-brief.md)

The single task list for Release 12 as of 11 Nov 2026, after the split. Follow the [operating principles](../12.md#operating-principles). Older handoffs supply SHAs and evidence; their next steps, gates and run authorizations are superseded.

## Where it stands (verified on GitHub, 11 Nov)

| Area | State |
|---|---|
| **Agent candidate** | `cand/29-r12` `313bbd46f1e24bfe635655d78b27ab0b321145d5`. `r12/cand-next` is `733ac5a4`, ten commits ahead |
| **Agent work to integrate** | `handoff/2026-11-10/track-a-ec48555` `ec48555d` (the A0/A1 batch, contains `r12/cand-next`); `handoff/r12-source-git-lookup` `53908e55` (Windows Git-source repair, one commit on top of it) |
| **App candidate** | `cand/29-r12` `e72d541d`. App `main` `1ca25bd1` is 20 commits ahead (the onboarding tour) and conflicts with the candidate in four files. App `main`'s own Tests are red |
| **App work to integrate** | The single test commit `1d5a1d69` from `scratch/r12-three-products-route-fix`. Do not take its parent `e12690f` (a provisional manifest) |
| **Harness** | `harness/29-r12` `b550ecad` |
| **Direct Journey** | Latest candidate run: 1 failed, 1 flaky, **11 skipped**. The true failure count is unknown |
| **CI** | Nothing running. No `A-FROZEN` or `GATE-GREEN` exists |

## Tasks

Routes are starting points (`N` cheapest); escalate per the [run contract](../../skills/astrid-dev-shared/run-contract.md#cheapest-model-first). T1, T2, T3 and T4 start in parallel.

| # | Task | Route | Done when |
|---|---|---|---|
| T0 | **Set up once.** A Python 3.11 environment for the Agent (`bash scripts/worker-env/agent-setup.sh`), a push test to Agent `scratch/r12-push-test`, and a way to read CI failure output (job logs if artifact downloads are still refused). Workers keep raw output while diagnosing | N | A focused Agent test runs locally; a failing CI job's error text is readable |
| T1 | **App: merge `main` into the candidate.** Merge App `main` into `cand/29-r12` with a merge commit; resolve the four conflicts (`WelcomeJourney.integration.test.tsx`, `prepareStarterProject.cancellation.test.ts`, `prepareStarterProject.test.ts`, `QuietUpdateNotice.tsx`) against both parents. Cherry-pick `1d5a1d69`. Then make App Tests green, including whatever is red on `main` | X for the conflicts, N after | App Tests 0 failures on the merged head |
| T2 | **Agent: integrate.** Fast-forward `r12/cand-next` to `53908e55` (which carries `ec48555d`). Run every `tests/test_installer_*.py` and the focused checks for the Windows repair | N | Focused checks pass on the integrated head |
| T3 | **Agent: rule on the four findings**, then fix. **005** (`test_external_pack_loading_m1_03.py:284`): the new guard from `cbf7b424` changed the refusal message; the security assertion still holds. Likely test drift: update the test to the new message and cite the commit. **028** (`test_installer_acl.py:326`): `297056f` moved the manifest write after the first source fetch. Rule whether that reordering is intended; if it is, fix the test's mock, and if it is not, restore the order. **015, 017** (`test_process_group.py:1436`, the native render scope test): timeouts that also appeared on baselines under a loaded host. Run those two groups once on a clean CI runner, base and candidate; a pass on both closes them | N to reproduce, X to rule on 028 | Each finding has a recorded ruling and its fix or closure |
| T4 | **Direct Journey to 0 failures, 0 skipped.** In `three-products.spec.ts:416` a request aborted at navigation never reports a terminal event, so the credential scan in `tests/e2e/local/support/tokenSniff.ts` fails closed (correctly). Keep the fail-closed scan. **Recommended fix, pending H9:** the App settles or cancels its in-flight requests before it navigates, so every request reaches a terminal event. First find out what the 11 skipped tests do once this one passes; fix each from its trace. `:2978` failed a body capture once and passed on retry: reproduce before ruling | S to design, N to iterate | A Direct Journey run on the App candidate with 0 failed and 0 skipped |
| T5 | **Candidate.** Push the integrated Agent head to `cand/29-r12` and tell the orchestrator. Dispatch one Agent `ci.yml` run on it; the orchestrator runs the review in parallel. Compare complete test IDs against the two recorded baseline runs in [gate item 2](../12.md#gate-one-frozen-tuple) and rule on every `regression`, `no-baseline` and `missing` bucket | N to dispatch and diff, manager rules | No unaddressed regression; review has no open blocker |
| T6 | **Re-pin and qualify.** One re-pin commit on App `cand/29-r12` (release number **12**), vendor lock regenerated, pin and lock checks from the commands below. Then App Tests, Direct Journey and the 11-row matrix on that exact tuple. The provisional matrix showed a Linux autostart-off "timed out waiting for the card" failure that was never followed up: expect it and fix it from its trace | N, X for a red row | All release checks 0 failures on one tuple. Post `A-FROZEN agent=<sha> app=<sha> ci-run=<id>` |
| T7 | **Gate and publish.** Post `GATE-GREEN` with every full SHA (Agent, App, Runtime, harness, VibeComfy, ComfyUI, lifecycle), the manifest sha256 and the run links. The orchestrator gets Hannah's go and publishes. Stay available for publication findings and her Mac check | — | `PUBLISHED`, then her Mac check passes |

## Not doing

- The remaining 66 pairs of the grouped A2 comparison, its runner branches (`handoff/r12-a2-parser-errors`, `handoff/r12-a2-incomplete-receipts`, the `scratch/r12-a2-*` refs) and any further runner design. Gate item 2 replaces it (H7).
- The Direct Journey diagnostic branches (`handoff/2026-11-11/r12-a4-protocol-diagnostics-status`, `spike/r12-a4-wire`). Read them for what was learned; do not integrate them.
- `handoff/r12-a2-personal-reserved-message`: only if T3 rules that 005 is a wording regression rather than test drift.
- Anything generation: `FINAL-B7`, `P20-APP`, GPU cells, the generation branches. They are [Release 13](../13.md).

## Commands

Run from the relevant checkout root.

| Step | Command |
|---|---|
| Agent tests | `bash scripts/worker-env/agent-setup.sh` once, then `PYTEST_ADDOPTS=-rA bash scripts/worker-env/agent-pytest.sh -q <selectors>`. Focused selectors locally; the full suite runs on CI |
| Compare Agent CI | `python3 -I env/baseline-diff.py --baseline r11=<log> --baseline r10=<log> --candidate <log>` on complete `-rA` logs. Exit 0 alone is not a pass: collection aborts or missing baseline IDs mean unqualified |
| Dispatch a workflow | `POST https://api.github.com/repos/<owner>/<repo>/actions/workflows/<file>/dispatches` with `{"ref":"<branch>","inputs":{...}}`, or the equivalent tool |
| Re-pin the manifest | `node scripts/installer/pin.mjs` with the final Agent and Runtime SHAs. Read its usage header first; check with `node scripts/installer/pin.mjs --check` |
| Vendor lock | `node scripts/vendor-lock.mjs update config/astrid-cli-surface/vendor.lock.json --producer astrid-producer`, then the same with `check` |
| Runtime lock check | `node scripts/vendor-lock.mjs check runtime.lock.json --producer runtime-producer` |
| Release guard | `node scripts/installer/release-check.mjs origin/main --candidate` |
| CLI surface test | `npx vitest run --config config/testing/vitest.config.ts src/integrations/runtime/cliSurfaceVerbs.test.ts` |
| App Tests / Direct Journey | Dispatch `test.yml` and `direct-journey.yml` on astrid-app with `{"ref":"cand/29-r12"}` |
| Matrix | Dispatch astrid-agent `journey.yml` on `harness/29-r12` with `direct_only=true` and the frozen `candidate` JSON: `{"app":<40-hex>,"agent":<40-hex>,"runtime":<40-hex>,"pinokio":<40-hex>,"manifest_sha256":<64-hex>,"artifacts":{"public/install":<sha256>,"public/install.sh":<sha256>,"public/install.ps1":<sha256>}}`, all read from the App candidate |
| Agent CI | Dispatch astrid-agent `ci.yml` with `{"ref":"cand/29-r12"}` |
