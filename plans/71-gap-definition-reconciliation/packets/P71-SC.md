# P71-SC — The owner's project-wide sense check (round 1 of at most 2)

**Source tasks:** [`tasks.md`](../tasks.md#completion-run-owner-go-24-november-2026) — SC
**Route:** high-judgment review, read-only. Mode: **GPT-6.2 Astra at High**, as the owner asked on 24 November 2026. If that mode is not offered, the manager says so on the board and starts nothing; the orchestrator asks the owner.
**Estimate:** about 1–2 hours
**Outcome:** One verdict, `SOUND`, `SOUND WITH FOLLOW-UPS` or `REWORK`, on the exact head the orchestrator names, with numbered findings.
**Dependencies:** the final review R and its findings closed; the orchestrator's REQUEST on the board naming the exact head of `project/71-gap-definition-reconciliation`. The manager never starts this packet without that REQUEST.
**May touch:** nothing. Read-only: post the verdict as one comment on the board.
**Must not touch:** any branch, pull request or file.
**Proof:** the verdict comment itself.
**PR destination:** none.
**Authority:** [run board](../run.md#authority)

One packet starts **one fresh ChatGPT session**. This one opens no pull request: it reads and posts one verdict, then stops.

## What to read

The plan's [plan.md](../plan.md), [inputs.md](../inputs.md) and [tasks.md](../tasks.md) on `main`; the diff from `main` to the named head of `project/71-gap-definition-reconciliation`; the final review's findings and their fixes, linked from the board.

## Questions

Is the gap definition clear and usable by a newcomer; does keeping all 22 gaps follow from the evidence; are the follow-up issues the right residue; did anything in this project grow beyond what its goal needs?

Step back from line-level review, which R already did: judge whether the project as a whole does what its goal says, simply, and whether anything should be cut.

## The verdict comment

Post it on [astrid-dev #1880](https://github.com/banodoco/astrid-dev/issues/1880), in the board's format, `type: DECISION`, `to: p71-73-orchestrator`, naming the exact head. Number each finding and label it BLOCKING (wrong result accepted, data or install damage, a real security or custody hole, a regression), FOLLOW-UP or NOTE, with file and line. The orchestrator turns each finding into an `SC1.<n>` card. A round 2, if needed, verifies only round 1's fixes.
