# P95-RV — High-judgment review (read-only, ChatGPT Pro)

**Source tasks:** [`tasks.md`](../tasks.md) — RS1 (the contract, one round) and R (the end, one round)
**Route:** high-judgment review, read-only. Mode: **Pro**. If Pro is not offered, the manager says so on the board and starts nothing.
**Outcome:** One verdict on the exact head the orchestrator names: `ACCEPT` or `REWORK`, with numbered findings.
**Dependencies:** a REQUEST from `p71-73-orchestrator` on the board naming the review kind (RS1 or R), the repositories, the exact head SHAs and the orchestrator's proof results. The manager starts a **fresh** session for each REQUEST.
**May touch:** nothing. Post the verdict as one comment on the board.
**Authority:** [run board](../run.md#authority)

## What to read

The REQUEST; for RS1, Otto's `docs/contract.md` and fixtures at the named head against [Plan 95](../plan.md), its [inputs](../inputs.md) and the code the module map names in astrid-dev; for R, the whole of Otto at its head and astrid-dev's `project/95-otto` against the plan's completion criteria and the parity evidence. Also the run contract's [review rules](../../../agent/shared/run-contract.md#review-and-promotion-boundaries).

Your job is judgment. RS1: is this the smallest contract that expresses Dev's shape and Marketing's, does anything in it need a feature no consumer uses, and could a later card be forced to redesign it? R: does the integrated result do what the plan says, with Dev's output unchanged, and was any test or check weakened, any second path or silent fallback added?

## The verdict comment

Post on [astrid-dev #1886](https://github.com/banodoco/astrid-dev/issues/1886) in the board's format, `type: DECISION`, `to: p71-73-orchestrator`, `reply_to:` the REQUEST, naming the exact heads reviewed. Number each finding BLOCKING (wrong result accepted, data or install damage, a real security hole, a regression, a contract that would force a redesign), FOLLOW-UP or NOTE, with file and line, and end with `ACCEPT` or `REWORK`.
