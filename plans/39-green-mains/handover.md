# Handover — All three mains green

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Release 14](../../releases/14.md)

Written by the Release 14 release manager on 16 November 2026, about 21:00 UTC, from the branches, pull requests and CI logs as they stood then. It is a dated snapshot for the manager who takes this plan next. It does not replace [tasks.md](tasks.md); bringing that file up to date on `main` is the first step below.

## Where it stands

Wave 0 is merged into the plan branches except its measurement, and half of wave 1 is merged. The Runtime's errors fell from 1,010 to 839, and the 839 that remain have three causes, one of which is a single stale pin. Nothing is merged into `release/14/main`, and `main` records none of this.

Plan branch heads: astrid-agent `b8f269294`, astrid-runtime `4fe2c0b`, astrid-app `e94d7ab53`, astrid-dev `8ff5aaab`.

## What is proven, and what is not

"Proven" means a hosted run on the merged head. A merged change whose check still fails is not proven.

| Task | Merged | State on hosted CI |
| --- | --- | --- |
| G0 worker smoke | astrid-dev #762, Runtime #52, App #278 | Proven locally, which is what its row asks. Re-run independently on 16 November: both smokes pass, both failure cases exit 3, the five copies match. |
| G1 baseline | not merged | Open. The table exists on `p39/g1` only. Missing: a Runtime `Nightly` run and an App `Direct Journey` run on the exact heads. Both workflows can be dispatched by hand. |
| GL gates fail on a rise only | Agent #366 | Proven: `fast checks` passed on `b8f269294`. It is not on `release/14/main`, so every pull request into that branch still fails `fast checks`. |
| SF3a stored results | Agent #368, Runtime #53, App #279 | Merged, proof pending. Artifacts are uploaded; nobody has checked that each file's count equals its job's summary line. |
| RE1 Agent checkout in Runtime jobs | Runtime #54 | Works: "Astrid checkout is unavailable" (457 errors) is gone from `unit`. |
| RE3 history for `git archive` tests | Runtime #54 | Proven for `unit`: no `git archive` error remains (159 on the base). Runtime #54's description says tests that need Agent commit `321cef4b` still fail in another lane, because the public remote does not serve it; that was not seen in the `unit` log. |
| RE4 `tsc` for `unit` | Runtime #54 | Proven for `unit`. Four `sandbox-process-control` tests and three `Nightly` errors still lack the compiler. |
| RE2 no scratch-path fallback | Runtime #54 | Merged, check fails: the fallback is gone, and the tests now fail on the stale Agent pin below. |
| K1b Runtime quarantine guard | Runtime #54 | Merged, check fails: 20 quarantined tests in 10 groups, none with an issue, owner or expiry. |
| PE1, K1c App pins and guard | App #280 | Merged, proof pending: `Tests` is green, but no `Lanes`, `E2E` or `Direct Journey` run exists on the plan head. |
| AE2, K1a | Agent #369, open | Not merged. Its head moved to `32572ad0`; it had no completed checks when read. |
| AE1 | nothing | The collection abort was already gone on the base. No tools-present or macOS proof. |

### The Runtime's remaining 839 errors

Counted from the `unit (ubuntu-latest)` log of run 43938386357 on `4fe2c0b`:

| Errors | Message | What it is |
| --- | --- | --- |
| 547 | `cannot import name 'commit' from 'astrid.sdk.timeline'` (280), `No module named 'astrid.sdk.timeline.capture'` (157), `No module named 'astrid.sdk.timeline.commit'` (110) | `tests/astrid-agent.pin` is `b05ac03a`, a Release 1 candidate of 31 October. It predates these modules, which the Agent's `release/14/main` has. One pin change. |
| 168 | `v33 provider/baseline verification is pending` | RT1, a phase 2 row. |
| 124 | `migrated realm requires fresh Timeline provider registration` | RT2, a phase 2 row. |

The four causes the base had are gone from this log: no "Astrid checkout is unavailable", no scratch-path fallback, no `git archive` failure and no missing `astrid` module, 718 errors in all. The 547 are tests those fixes made reachable; on the base they stopped earlier for want of a checkout.

Agent CI on `b8f269294` (run 43934820640) had not finished: shards 2 to 6 and 8 and `darwin native` had failed, shards 1 and 7 were running. Its shard summary lines were not read.

## What exists but has not landed

- **Agent #369** (`p39/phase1-results-wiring`), AE2 and K1a.
- **astrid-dev #781** (draft), the wave 0 records, into the plan branch.
- **`p39/g1`**, with no pull request: the G1 table, and a "first repair batch" of patches for wave 1 written by a second worker that could push only to that branch. Compared with what is merged, the batch still offers only the fetch of historical Agent commit `321cef4b` for RE3 and its own AE2 and K1a, which #369 also covers. Take what #369 and #54 lack; do not apply the patches whole.

## Rulings the next manager makes or brings to the owner

1. **The Agent pin in the Runtime's tests.** RE1 allows moving it once the measurement shows it is behind. The table above shows it. Recommended: pin the Agent's `release/14/main` head, and say so in the row.
2. **The quarantine cap.** The plan caps each repository at ten entries. The Runtime has 20 tests in 10 groups. The plan does not say whether the cap counts groups or tests. This is the owner's: fix ten now, or count groups and give each an issue, owner and expiry.
3. **79 structure findings** the Agent's structure gate still reports as new, and **47 direct skip call sites** K1a finds. Each needs a cause row, not a baseline update.
4. **Agent commit `321cef4b`**, which Runtime #54 says some RE3 tests need and the public remote does not serve. Find the lane first; it is not `unit`.

## For the next manager, in order

1. Read the [Manage skill](../../skills/roles/astrid-dev-manage/SKILL.md). You answer for this plan finishing. Fill the `Run start` line in [inputs.md](inputs.md).
2. Bring [tasks.md](tasks.md) on `main` up to date by a pull request that changes only that file: it shows every row empty. Record the plan branches' cut commits in [the brief](../../releases/14.md) on `main`.
3. Change `tests/astrid-agent.pin` in the Runtime and re-run `unit`. Expect the 547 to go. Whatever replaces them is the real list.
4. Merge Agent #369 once its checks have run. Dispatch the Runtime `Nightly` and the App `Direct Journey` on the plan heads, then close G1 and merge #781.
5. Put GL on `release/14/main` as its own fix for [#742](https://github.com/banodoco/astrid-dev/issues/742); ask the release manager. Every other pull request into that branch is red until it is there.
6. Do G2, then the one review round RS1. Then wave 2: RT1 and RT2 first, since they are 292 of what is left in the Runtime.

## What this run taught

- **A wiring fix uncovers the next layer.** Runtime #54 removed 718 errors and exposed 547. Judge a wiring task by the messages that disappear, not by the total.
- **Two workers, one task list, no shared record.** One could not push product branches and saved patches; the other built the same fixes. Give a plan one manager, and give every worker the plan branch.
- **Progress went onto work branches.** The Manage skill puts it in `tasks.md` on `main`. It was not there, so the owner could not see what was done.
- **Verification was requested task by task.** The plan has one review stop after wave 1 and one at the end. A manager reads its workers' diffs and merges.
- **A run takes two hours and queues.** Prove a task with its focused tests; merge in batches; one full run per batch.
