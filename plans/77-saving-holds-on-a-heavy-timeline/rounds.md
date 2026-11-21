# Rounds — Saving holds on a heavy timeline

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Handover](handover.md)

One section per round, newest last, written by the coordinator under the [live-loop workstream](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md#the-round). Each holds: the stack versions; a table of scenario, outcome (saved or refused with the reason shown), time to Saved, head count, anything vanished; The strategist's advice (evidence, not a verdict); the fixes picked and their PRs; and **Plan deltas** for [Plans 63, 75 and 76 and 18](inputs.md#references).

No round has run yet. Round 1, on the plan branches as cut, is the baseline. The 18 November sweep (14 edit kinds, 3 saved, 11 refused, on the owner's copied timeline with the old timer) is earlier evidence, not a baseline: [evidence/results.jsonl](evidence/results.jsonl).

## Setup checks on 21 November 2026

No timed baseline yet. On App `7fc14d2f`, Agent `c00721de`, Runtime `e43bfccc`, a nine-track SDK commit advanced the public head. Fresh SDK reopen was refused with `accepted commit inputs changed during verification`, and Runtime logged a WAL move. A one-track control reopened, as did the nine-track control on App `e576c7fe`, Agent `efccee92`, Runtime `162500fe`. One subsequent bounded shot seed advanced a public head while the SDK reported its outcome unknown. Release 14 owns the fix. [Release 14 integration issue](https://github.com/banodoco/astrid-dev/issues/796)

The deliberate no-op probe on App `75120d7c`, Agent `c00721de`, Runtime `e43bfccc` produced three expected failed rows, one unchanged publication per row, and zero successful commits. It used an empty sandbox timeline. The heavy fixture must qualify before measuring Round 1.
