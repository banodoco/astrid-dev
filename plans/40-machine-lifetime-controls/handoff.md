# Plan 40 handoff

> **START HERE — this file is reference only (10 Nov 2026).** Release 12 now includes this plan's work. Your orders are in [generation.md](../../releases/12/generation.md#start-here--p40-manager), with the overall plan in [releases/12.md](../../releases/12.md). Use this handoff only for SHAs, evidence and history. **Do not follow its gate, next-action, resume, freeze, budget or "release 13" text**: where they differ, the release pages win.

Updated: 2026-11-10. This hands Plan 40 to a new manager session using GitHub as its durable source. Continue with the `astrid-dev-manage` skill and the run contract.

## Goal and status

Deliver machine lifetime controls for RunPod generation machines, including machine inspection, bounded paid keep/claim behavior, preferences, capacity waiting, and safe custody. The implementation through T1–T8, T5-R1 and T4 is integrated and locally proven on Agent candidate `b15e286b686a5d1859406ebb8dc65969e84a14cb` (tree `73ba75005afaf1a4f06502f166e09a52171cfbde`). The plan phase is **not complete**: the one completion-review round found four blocking issues; those repairs, T9, its focused review, and the frozen full-CI comparison remain.

No live provider or GPU calls were made by this manager. RunPod activity count: 0 rented by this run before handoff; 0 after; nothing to release. This count is from run records and local work state, not a live provider query. The run used CPU fakes only.

## GitHub state and exact heads

| Repository/ref | SHA | State |
| --- | --- | --- |
| `banodoco/astrid-agent` source base `origin/int/32-one-generation-path` | `99724131d2c3eff11867a189986c4ba147e5a81b` | Plan 32 donor/base. |
| `banodoco/astrid-agent` `int/40-machine-lifetime` | `b15e286b686a5d1859406ebb8dc65969e84a14cb` | Complete local integration candidate; intentionally not pushed to `int/**` during the runner freeze. |
| `banodoco/astrid-agent` `plan40/staging-int40` | `b15e286b686a5d1859406ebb8dc65969e84a14cb` | Pushed handoff/share branch; use this exact ref to resume. All merged task changes are reachable from it. |
| `banodoco/astrid-dev` `main` at handoff branch creation | `6ec9ea94924acf9e5398ad24cfc5d12023744d17` | Includes D12/T9 card via PR #347, R1 findings via #345, progress and process-ledger updates. |

There are no unpushed commits in either base clone. `int/40-machine-lifetime` is ahead of its remote because the freeze forbids pushing `int/**`; its full head is safely published on `plan40/staging-int40`. No unmerged product task branch needs preserving. Product merges landed on local `int/40` as recorded in `tasks.md`; notable recent merges are T5-R1 `c8f56c5829e5b5a4e7e8b09e12466a4e3916feb9`, T8 `a9b52ba850bc7361c12b56ecc7a17fd5ce7d41f6`, and T4 `b15e286b686a5d1859406ebb8dc65969e84a14cb`.

## Task state

- **Complete on the candidate:** T1, T2, T3, T4 parts 1 and 2, T5, T5-R1, T6, T7, T7b and T8. Merge SHAs and focused proof are in [`tasks.md`](tasks.md); progress PRs #341–#343 document the last repairs and completions.
- **Review round 1:** completed on the exact candidate `b15e286b686a5d1859406ebb8dc65969e84a14cb` by the configured reviewer (`gpt-6.1-sol`). The plan permits one round and that budget is consumed. Four blocking findings were recorded in PR #345 and as R1.1–R1.4 in [`tasks.md`](tasks.md):
  1. **R1.1 (S):** first `tasks.show` interruption can skip cancellation because no latest status/task state has been seeded; cover RunPod generation and claim, and non-RunPod isolation.
  2. **R1.2 (N):** explicit `--datacenter any` is confused with omission in setup; saved fixed DC can survive a JSON update and the interactive path can prompt/resolve incorrectly. Preserve volume-pinned DC.
  3. **R1.3 (N):** setup inventory `ValueError` and failed `runpod.setup` result can expose a resolved credential sentinel. Sanitize both paths while retaining typed local validation messages.
  4. **R1.4 (X):** `generate workflow` lacks per-job `--gpu` and `--datacenter`; pass them through shared RunPod consent/digest without changing saved preferences or paid bounds.
- **Next, in order:** finish R1.1–R1.4, then T9. Do not dispatch additional review rounds. T9 gets its own focused independent review as specified by its card.
- **T9 (S) is not started.** D12 and the full card are on astrid-dev main through PR #347. The card in [`tasks.md`](tasks.md) requires failed jobs and ordinary preparation errors to settle idle within existing consent limits; immediate release is reserved for unsafe or unknown reuse, including custody mismatch, lost/unknown lease, unverifiable preparation/install, and host shutdown. Record a bounded, redacted failure summary under the owner lock using Plan 34 fix N `e0d95d7b859bd2e8d6f83124b4bc7f2828eb5c49`; never include messages, prompts, URLs, logs or keys. Prove expiry, each unsafe path, secret absence, warm retry without a second create, success unchanged, and both claim-preparation release sites. Post the integrated T9 SHA promptly for Plan 34.
- **CI:** full Agent CI has not been dispatched. The release 12 runner freeze remains active; wait until the orchestrator explicitly lifts it. The reviewer was allowed to run before CI; CI remains a separate gate.

## Proof and known limits

- Scoped Agent baseline at `99724131d2c3eff11867a189986c4ba147e5a81b`: 295 passed, 15 deselected, 1 warning across the plan inventory and focused files. Supplemental generic-host baseline: 165 passed and one known optional-pack import/quarantine failure.
- T8 integrated composed proof: 377 passed, 18 deselected, with the same one baseline-confirmed optional-pack import failure; comparison was 0 regressions / 1 pre-existing. Generation CLI proof: 64 passed; two approved claim integration selectors passed. T4 parser audit: 19 cases passed; T4 focused proof: 142 passed, one existing pending-deprecation warning. Full details and exact logs were local/ignored in `.otto`; durable focused results and merge SHAs are summarized in [`tasks.md`](tasks.md), and the source/tests are in the pushed candidate branch.
- No full-suite/CI result, live-provider result, or live GPU result is claimed.
- The required process-ledger entry was merged in astrid-dev PR #344 (`0cbd70acd5688e96f0380e5771ea9e82ee21cc3d`): baseline-diff initially misread application `ERROR` log lines as pytest node results; prefer a node-result-only or structured result parser.
- **Keep-after-failure keeps the machine, not the evidence.** The reset that runs before a kept machine goes idle deletes the job's run and job folders and truncates every log (`astrid/packs/runpod/pod_reset.py:213-233` at Agent `1439ccc6`), so nothing is left to inspect. Release 13's G3 collects the failure folder before the reset.

## Decisions and evidence

- D1–D12 and deferrals are in [`inputs.md`](inputs.md). Particularly preserve D2: keep/release refuse without a live owner, because owner construction can run recovery and release a pod; and preserve the existing rule that reuse cannot extend a paid limit.
- D12/T9 source and routing: astrid-dev PR #347. Review findings: PR #345. Process ledger: PR #344. T5-R1/T8/T4 progress and proofs: PRs #341–#343. Earlier progress entries remain in `tasks.md` history.
- Share branch: [Agent `plan40/staging-int40`](https://github.com/banodoco/astrid-agent/tree/plan40/staging-int40). Review finding record: [astrid-dev PR #345](https://github.com/banodoco/astrid-dev/pull/345). Decision/card: [astrid-dev PR #347](https://github.com/banodoco/astrid-dev/pull/347).

## Resume instructions

1. Read this file, [`tasks.md`](tasks.md), [`inputs.md`](inputs.md), the manage skill, and the shared run contract. Read the orchestrator mailbox for current freeze/steering notes.
2. In the Agent base clone, fetch and inspect `origin/plan40/staging-int40`; verify it resolves to `b15e286b686a5d1859406ebb8dc65969e84a14cb`. Keep the base clone on `int/40-machine-lifetime`; workers get fresh worktrees from the share branch. Do not push to `int/**` while the freeze is active.
3. Start R1.1–R1.4 in the specified order/scopes from the latest staged candidate; each worker runs only its focused proof from its task card. Then start T9 (S) from the integrated repaired head, using CPU fakes and the T9 focused command in `tasks.md`; have its independent focused reviewer inspect the exact T9 SHA.
4. After the freeze lifts, run the one full CI comparison on the integrated head. Batch product merges and cancel superseded runs per the run contract. Do not publish/tag a release; Release owns that step.
5. Keep progress in `tasks.md` and the normal tasks-only astrid-dev PR flow. When the phase is complete and reviewed, follow the plan completion template and the orchestrator's release-13 routing.

Focused commands recorded for the blocking review repairs:

```sh
bash scripts/worker-env/agent-pytest.sh -q tests/sdk/test_invoke_settlement_and_replay.py
bash scripts/worker-env/agent-pytest.sh -q tests/packs/runpod/test_machine.py
bash scripts/worker-env/agent-pytest.sh -q tests/core/generation/test_cli.py
```

T9 focused command:

```sh
bash scripts/worker-env/agent-pytest.sh -q tests/packs/runpod/test_machine.py tests/packs/runpod/test_warm_session.py tests/core/execution/test_warm_hold.py tests/core/generation/test_cli.py
```
