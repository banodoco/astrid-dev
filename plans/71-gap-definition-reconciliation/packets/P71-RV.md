# P71-RV — High-judgment review (read-only, ChatGPT Pro)

**Source tasks:** [`tasks.md`](../tasks.md#completion-run-owner-go-24-november-2026) — the review of a submitted packet that needs a high-judgment verdict, or the final review R
**Route:** high-judgment review, read-only. Mode: **Pro** (owner, 24 November 2026). If Pro is not offered, the manager says so on the board and starts nothing.
**Estimate:** about 1 hour for a packet review; about 2–3 hours for R
**Outcome:** One verdict on the exact head the orchestrator names: `ACCEPT` or `REWORK`, with numbered findings.
**Dependencies:** a REQUEST from `p71-73-orchestrator` on the board naming the review kind (packet review or R, and its round), the pull request or branch, the exact head SHA, and the orchestrator's proof results (commands, test counts, exit codes). The manager never starts this packet without that REQUEST, and starts a **fresh** session for each REQUEST.
**May touch:** nothing. Read-only: post the verdict as one comment on the board.
**Must not touch:** any branch, pull request or file.
**Proof:** the verdict comment itself.
**PR destination:** none.
**Authority:** [run board](../run.md#authority)

One packet starts **one fresh ChatGPT session**. This one opens no pull request: it reads, posts one verdict and stops. In this plan it reviews the final review R.

## What to read

- The REQUEST, then the diff of the named head against its base (the PR's "Files changed", or the compare view the REQUEST links).
- For a packet review: that packet's file in [packets/](./), especially **May touch**, **Must not touch** and **Contract**, and the card it closes in [tasks.md](../tasks.md#completion-run-owner-go-24-november-2026).
- For R: the plan's [Completion](../plan.md#completion), the Completion run table and the rulings in [inputs.md](../inputs.md#owner-decisions).
- The run contract's [review rules](../../../skills/shared/run-contract.md#review-and-promotion-boundaries) and [the gatekeeper standard](../../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md#at-each-lead-check-in).

The orchestrator has already run the proof. Your job is judgment: does the change do what its contract says, and only that? Is anything accepted that should be refused? Is any test or check weakened? Is there a second code path or silent fallback? And for a design, is it the smallest sound one?

## The verdict comment

Post it on [astrid-dev #1880](https://github.com/banodoco/astrid-dev/issues/1880), in the board's format, `type: DECISION`, `to: p71-73-orchestrator`, `reply_to:` the REQUEST, naming the exact head you reviewed. Number each finding and label it BLOCKING, FOLLOW-UP or NOTE, with file and line:

- **BLOCKING** only for a wrong result accepted, data or install damage, a real security or custody hole, a regression from base, or a broken contract.
- **FOLLOW-UP** for real but non-blocking improvements; these become a backlog issue.
- **NOTE** for observations.

End with `ACCEPT` (no BLOCKING findings) or `REWORK`. The orchestrator turns each BLOCKING finding into a rework or an `R<round>.<n>` card. A round 2 verifies only round 1's fixes.
