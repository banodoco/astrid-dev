# Release 12, Track A — Fixes

[Release 12](../12.md) · [Track B: Generation](generation.md) · Reference only: [Plan 29 handoff](../../plans/29-update-and-release/handoff.md) and [evidence](../../plans/29-update-and-release/evidence/r12/)

Active P29 brief as of 10 Nov 2026. Follow the shared [operating principles](../12.md#operating-principles-every-manager-reads-these-first), [How-to](../12.md#how-to-tools-every-manager-uses), branch rules and [mailbox protocol](../12.md#hand-offs-all-via-mailboxes). Handoffs supply evidence and SHAs; their gates, next steps and freeze text are superseded.

## START HERE — P29 manager

- **First:** push `scratch/p29-push-test` and run `smoke.sh agent` once, per How-to. Then start **A0, A1 and A4 in parallel**, and follow A2–A7 in dependency order.
- **Push:** Agent `r12/cand-next`, `cand/29-r12`, `harness/29-r12`; App `cand/29-r12`, `release12/candidate-manifest`. Add commits; use full GitHub URLs.
- **Dispatch:** early Direct Journey, Checkpoint A and final-round runs only. Commands are below.
- **Escalation:** consult Astra for high-stakes major decisions and whenever blocked, as required by the shared [role and authority rules](../12.md#roles-one-orchestrator-two-track-managers). Use Astra for tricky or nefarious bugs, or when a previous agent struggled. Post the blocker and recommendation to the orchestrator; Hannah retains her decisions. Review round 4 uses an independent Astra worker. Normal task routes remain Luna / Terra / Sol by difficulty.
- **Handoff:** post `GATE-GREEN` with the full tuple, then end `RUN-STATUS: WAITING PUBLISHED from orchestrator` and fix any publication findings. The orchestrator publishes. After `PUBLISHED`, complete the [P29 post-publish work](../12.md#after-publish), record Hannah's successful Mac update check, post `COMPLETION-READY plan=29`, and wait for `MANAGER-CLOSED` before ending `DONE`.

## Where it stands

Status as of 11 Nov; Track A owns the next actions. Detailed evidence and task history are in the [task record](../../plans/29-update-and-release/tasks.md).

| Area | Current state and next action |
|---|---|
| **Agent** | `cand/29-r12` remains `313bbd46f1e24bfe635655d78b27ab0b321145d5`. Working handoff `ec48555d8298d155390ffbb37d1950c3e80b43a4` includes A0/A1 work and needs comparison and required release proof before A3. |
| **A2 comparison** | Grouped four-side receipts 001–018 are recorded; candidate findings in 005, 015 and 017 remain unresolved. Prepare the bounded runner for 019–052 and retain all existing receipts and environment differences. |
| **App / A4** | `cand/29-r12` is `e72d541de1d65bee74707ca1ae9c2d429ee2f721`. Early Direct Journey remains failing under the credential-capture gate. A wire-level feasibility spike is in progress; it has no gate credit and must preserve the existing checks. |
| **Harness** | `harness/29-r12` is `b550ecadf07d7a4b377be1b7af1d6252642f1b48`. |
| **Release gates** | A3 and Checkpoint A have not been reached. No `A-CAND`, `A-FROZEN` or `GATE-GREEN` has been posted; the exact-tuple checks and native Windows proof remain required. |

## Tasks

| # | Task | Depends on | Done when |
|---|---|---|---|
| A0 | **Make Agent CI measurable:** fix the three collection errors in the candidate (see CI [42799672641](https://github.com/banodoco/astrid-agent/actions/runs/42799672641)) and add `-rA` test IDs to its `ci.yml` unit jobs. This narrow release prerequisite is an exception to deferring old failures to Plan 39; do not push `main`. P32 owns further errors introduced by generation | — | Focused collection/reporting checks pass; Checkpoint A's single CI run verifies complete test IDs |
| A1 | Into `r12/cand-next`, merge `--no-ff`: the Windows donor `26380e3a` (check it against `989cd0f6c`; compare both parents). **A1b:** make the Agent's engine-recipe VibeComfy pin checked against, or derived from, the install manifest's pin at install. When `VIBECOMFY-RELEASE` arrives, set the Agent pin to it | — | Windows donor integrated and A1b implemented; focused proof passes; every `tests/test_installer_*.py` runs |
| A2 | **One focused before/after comparison** of the completed batch against base `313bbd46f`, R11 and R10. Run `env/cmp-run.sh` once per commit with the same selectors, then `baseline-diff.py` ([historical method and limits](../../plans/29-update-and-release/evidence/r12/agent-comparison.md)). On a resource-constrained shared host run sides serially; parallel runs need comparable isolated resources. Use the same Python 3.11 version, selectors, execution mode and unchanged test timeouts for every side, preserving each revision's pins. Record coverage and complete test IDs; interrupted results do not establish parity. The recorded base used Runtime `9fc53b77`; rerun a baseline if its environment/coverage is not comparable. Declare exclusions; this does not replace CI | A0, A1 including `VIBECOMFY-RELEASE` pin | No unaddressed regression under P39-D8. Record proven historical debt in Plan 39; repair regressions and rerun the affected comparison with orchestrator approval |
| A3 | Push the proven Agent head to `cand/29-r12` and post `A-CAND`. Start review round 4 on `313bbd46f..<that SHA>` and Checkpoint A's Agent CI in parallel. Prepare re-pin #1 once A4 is clear, then start the tuple checks below. If review repairs change the candidate, re-prove them and replace `A-CAND`; the orchestrator authorizes affected CI/review reruns | A2 | Review 4 has no open blocker on the Agent SHA submitted for Checkpoint A |
| A4 | Direct Journey round 7 onward (`:1264`, `:649`), then early Direct Journey runs until 0 failures. Diagnose each failure from its trace | — | Direct Journey 0 |
| **Checkpoint A** | Re-pin #1 on App `cand/29-r12` to the fixes-only tuple and agreed pins; regenerate/check locks as in Commands. Run App Tests, Direct Journey and the full matrix, reusing any same-tuple runs begun during A3. Reuse A3's Agent CI, with full D8 comparison | A3, A4 | Release checks have 0 failures (including native Windows rows), CI meets D8, review 4 is clear. Post `A-FROZEN agent=<sha> app=<sha> ci-run=<id>`. Freeze both candidates; initialize `release12/candidate-manifest` from this App SHA |
| **A5-prep** | On `release12/candidate-manifest`, merge `--no-ff` exactly the final `P20-APP` SHA, which was reproved against the frozen App. Make **re-pin #2** to `FINAL-B7` and agreed Runtime/VibeComfy pins, regenerate vendor lock, and run all pin/lock/CLI-surface/release checks below. Push and post `FINAL-TUPLE agent=<sha> app=<sha> manifest_sha256=<digest> evidence=<path>` with the full tuple and artifact hashes. Its Agent SHA must equal `FINAL-B7` and the manifest Agent pin. This prepares the final App before GPU proof without moving either `cand/29-r12` | `A-FROZEN`, `FINAL-B7`, final `P20-APP` | Exact final App and manifest ready for P34; B9 can review its merge delta |
| A5 | **Promote** after `CHECKPOINT-B`: fast-forward Agent `cand/29-r12` to `FINAL-B7` and App `cand/29-r12` to the exact prepared `FINAL-TUPLE` App SHA. No new merge or regenerated manifest | `CHECKPOINT-B` naming those Agent/App SHAs | Post `MERGED agent=<sha> app=<sha>` |
| A6 | Verify promoted SHAs and manifest digest equal `FINAL-TUPLE`, then run final App Tests, Direct Journey and the 11-row matrix. Reuse B8, review and GPU receipts for those exact inputs; do not dispatch another Agent CI. Any repair returns through the orchestrator's freeze/invalidation rules | A5 | The complete [gate](../12.md#gate-final-tuple) holds on one tuple |
| A7 | Post `GATE-GREEN tuple=<evidence-path>` containing every full SHA (Agent, App, Runtime, harness, VibeComfy, ComfyUI and lifecycle), manifest sha256 and gate receipts. The **orchestrator** gets Hannah's in-session go and publishes. P29 remains available for publication findings and Hannah's normal App update check | A6 | `PUBLISHED`, then Hannah's Mac check passes before closing Plan 29 |

## Commands

Run from the relevant checkout root.

| Step | Command |
|---|---|
| Re-pin the manifest | `node scripts/installer/pin.mjs` with the final Agent and Runtime SHAs. Read the script's usage header first; check with `node scripts/installer/pin.mjs --check` |
| Vendor lock | `node scripts/vendor-lock.mjs update config/astrid-cli-surface/vendor.lock.json --producer astrid-producer`, then `node scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json --producer astrid-producer` |
| Runtime lock check | `node scripts/vendor-lock.mjs check runtime.lock.json --producer runtime-producer` |
| Release guard | `node scripts/installer/release-check.mjs origin/main --candidate` |
| CLI surface test | `npx vitest run --config config/testing/vitest.config.ts src/integrations/runtime/cliSurfaceVerbs.test.ts` |
| App Tests / Direct Journey | Dispatch `test.yml` and `direct-journey.yml` on astrid-app with `{"ref":"cand/29-r12"}`. App lanes (`lanes.yml`) run only if the orchestrator calls for a changed-area comparison |
| Matrix | Dispatch astrid-agent `journey.yml` on `harness/29-r12` with `direct_only=true` and the `candidate` input, frozen JSON: `{"app":<40-hex>,"agent":<40-hex>,"runtime":<40-hex>,"pinokio":<40-hex>,"manifest_sha256":<64-hex>,"artifacts":{"public/install":<sha256>,"public/install.sh":<sha256>,"public/install.ps1":<sha256>}}`, all read from the App candidate. `journey.yml`'s automatic step builds the same shape |
| Agent CI | Dispatch astrid-agent `ci.yml` with `{"ref":"cand/29-r12"}` |

**If Hannah splits (H4):** skip A5-prep and A5; do not wait for `FINAL-B7`, `P20-APP` or `CHECKPOINT-B`. In A6, make re-pin #2 on the frozen fixes-only App candidate, keeping its qualified Agent and agreed pins, run the lock/pin checks and final round, and apply gates 1–3 plus Track A review 4. B8, B9 and GPU proof are not required. Then A7; record the excluded generation work for the next release.
