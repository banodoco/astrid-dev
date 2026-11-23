# Plan 40 handover — Machine lifetime controls

**23:10 UTC, 22 November 2026.** Waiting for Plan 81. [Plan](plan.md) · [Tasks and exact proof commands](tasks.md) · [Inputs and authority](inputs.md) · [Release 15](../../releases/15.md)

## Done

- Reconciled against Agent `release/15/main` at `8807f820eb47d6018db723511e024a0a123fbe95`. The Release 13 redesign is already there. The old integration branches are reference history. [Reconciliation](tasks.md#reconciled-against-release15main-22-november-2026) · [astrid-dev #1458, merge `bf91dda7`](https://github.com/banodoco/astrid-dev/pull/1458)
- **R1.1–R1.3** passed on the starting tree. Scratch reversals proved first-poll cancellation, interactive explicit-`any`, and setup redaction. **R1.2x** independently proved explicit-`any` clears a saved JSON datacenter while a volume still pins its datacenter. All three setup selectors passed on the task commit. **R1.4** added 26 passing authored-workflow refusal cases. Its exact-commit two-file run had 167 passes and two inherited failures. [R1 proofs](tasks.md#release-15-execution-proof) · [Agent #537, merge `b72818a99d5a96cbb26f35dcbad70aaddec3716b`](https://github.com/banodoco/astrid-agent/pull/537) · [Agent #536, merge `7703c50261c51aa5976484fae07402f9d59aa38d`](https://github.com/banodoco/astrid-agent/pull/536) · [astrid-dev #1478, merge `29de7275`](https://github.com/banodoco/astrid-dev/pull/1478)
- Rehearsed Plan 81 `5ea8d4bb06ca755cf5aeb7bd70a9f3d9e752390f` in local merge `48d55707cfcabedf56d692816d16148edf7188cd`. No conflicts or shared changed files. Plan 81 alone changed `astrid/sdk/generation.py`. All 42 focused cases passed. Rehearsal branch, worktree, and environment were discarded. Log in `run/rehearse-p81-pytest.log`.
- CPU inventory at `8807f820` gave 519 passes and one local 120-second timeout in `tests/integrations/test_remote_machine_cpu.py::test_an_installed_pack_entry_and_an_as_entry_user_entry_run_on_the_machine`. The timeout is a container observation and absent from the hosted list. Both SDK failures in `tests/sdk/test_generation_target.py` are inherited: `test_auto_probes_attached_before_managed_readiness` and `test_generate_without_claimed_machine_refuses_before_admission`. The Release Lead owns the five other Release 15 additions outside these files. [Red Agent CI run 45031908687](https://github.com/banodoco/astrid-agent/actions/runs/45031908687) · [Lead’s exact hosted failure IDs](../../releases/15/evidence/agent-ci-baseline-8807f820/release-15-8807f820-failing-ids.tsv) · [astrid-dev #1484, merge `9e9db53c`](https://github.com/banodoco/astrid-dev/pull/1484) · [Baseline wording PR #1485](https://github.com/banodoco/astrid-dev/pull/1485)

## Recover the workspace

Agent `release/15/plan-40` is clean and pushed at `7703c50261c51aa5976484fae07402f9d59aa38d`. Release main was last verified at `8807f820`. Zero pods created. From the run workspace containing `astrid-agent/`, `astrid-dev/` and `run/`:

```sh
cat run/to-codex.md run/to-orchestrator.md
cat astrid-dev/plans/40-machine-lifetime-controls/.otto/runs/2026-11-22-release-15/run.yaml
git -C astrid-dev fetch origin main
git -C astrid-dev show origin/main:plans/40-machine-lifetime-controls/tasks.md
git -C astrid-agent fetch origin release/15/main release/15/plan-40
git -C astrid-agent status --short --branch
git -C astrid-agent worktree list
git -C astrid-dev worktree list
git -C astrid-agent log -8 --oneline origin/release/15/main
```

Use the published plan and branches if the local run records are unavailable. Verify any unfinished worktree or CI run before resuming. Baseline and proof logs are under `run/`.

## Next, in order

1. Wait for the Release Lead to notify the host that Plan 81 landed. Landing order is **81 → 40 → 77 → 78**.
2. Fetch and verify `release/15/main`, then on the clean Plan 40 branch run `git -C astrid-agent merge --no-ff origin/release/15/main`. Capture both parent SHAs and the merge SHA.
3. Run the named R1 oracles, including R1.2x, and the R1.4 tests on release main and the integrated head. Also rerun each inventory file the merge touches on both sides. Use a scratch baseline checkout with the additive test diff for cases missing there. Use `-rA` and the named commands in [tasks.md](tasks.md#release-15-execution-proof) with CPU fakes. The review round is **used**. Repairs get bounded checks only.
4. Tell the Lead before dispatching. Run **one** hosted Agent CI on the exact pushed integrated head, with only one Agent CI run active across Release 15. Compare its tests by ID against the Lead’s hosted list above and report any additions or missing evidence.
5. Repeat the [headline proof](plan.md#completion) through the CLI and host on CPU fakes. Record release time, minutes left, accumulated cost and hourly rate for idle and busy leases. Show that keep moves the deadline with fresh consent, the paid cap still releases the lease, and reuse cannot extend it. Update `tasks.md` with the actual evidence and exact SHAs.
6. Open the landing PR from `release/15/plan-40` to Agent `release/15/main`. The owner approves landing through the host. Report readiness with the head SHA and evidence.

## Decisions the landing relies on

- **10 Nov 2026, plan scope.** Hannah asked for “a way to quickly check when it’s going to die” and accepted the capped proposal. The [plan goal](plan.md) says a person “sees when it will stop (release time, minutes left, cost so far, hourly rate)” and can keep the machine “always within a spend cap they set and with fresh paid consent.”
- **10 Nov 2026, D12.** Hannah said, “We shouldn't kill a pod when a job fails.” Keep it idle under the consented limits while reuse remains safe.
- **12 Nov 2026, D13.** “unless the actual machine fails for some kind of terminal reason, we should never automatically terminate it”. Retain reachable, owned machines with verified stopped jobs after preparation failure. Safety and paid-limit release still apply.
- **12 Nov 2026, D14.** The decision record says “claiming is separate from generating” and “generate never claims automatically.” Named machines queue jobs. The idle timer counts only with no jobs, keep extends it, and the spend cap still bounds the lease. [Owner decisions D12–D14](inputs.md#owner-decisions)
- **22 Nov 2026, reconciliation.** D14 supersedes T5’s `generate --gpu/--datacenter`. GPU and datacenter choices live on claim and describe. R1.4 before was “`generate workflow` accepts ordered `--gpu` and `--datacenter`”. After, workflow uses the existing machine and refuses claim controls with `astrid machines claim` guidance. The owner has yet to ratify the rewritten card by name. [Before and after](tasks.md#reconciled-against-release15main-22-november-2026)
