# R14-PUB-1 — The publication proofs no other packet owns

**Source tasks:** [Publishing Release 14](../../14.md) (owner decision, [mailbox](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7061951208)); gaps found by the 12:49 strategic review of 21 Nov.
**Estimate:** 1–1.5 engineering days, mostly waiting on runs.
**Outcome:** Every proof the publication rule names exists, or is ready to run, on the frozen tuple. The Lead can then publish from a checklist.
**Dependencies:** Items 1–2 can be prepared now against today's heads; their final run is on the frozen tuple (after FIX-15's final App re-pin). Items 3–4 start now.
**Proof:** each item's receipt, linked from one checklist file in astrid-dev, `releases/14/evidence/publication-checklist.md`.
**PR destination:** astrid-dev only (`releases/14/evidence/`). Run no product changes. Workflow dispatches go to the Lead.
**Authority:** [run board](../run.md#authority). Spend is within the Lead's delegated $10 GPU budget, reported.

1. **Per-ID and job-level diff against published Release 13.**
   - Agent: all eight unit shards and the integration lanes, release candidate against Agent `959da732` (Release 13's published main), with `env/baseline-diff.py` over the `-rA` logs.
   - App: Vitest and the journey IDs, candidate against App `de7dd1e6`. Reproduce the Release 13 baseline run if its logs lack IDs.
   - Compare jobs by name, and reconcile missing or renamed IDs.
   - Write one table: ID, R13, candidate, and the explanation for each pass-to-fail (most are already explained in the Lead's fact check; FIX-18 owns four).
   - Write the script once, so that the frozen-tuple rerun is one command.
2. **One rented generation.** Prepare a RunPod job on the candidate tuple: the smallest supported image workflow, teardown confirmed, and an empty pod census afterwards. Record the tuple, job ID, the usable output, the cost and the census. Check the credentials and the remaining budget first; stop if a job would exceed it. The Lead dispatches the final run on the frozen tuple.
3. **Release notes draft** (`releases/14/notes.md`):
   - an opt-in update, not required;
   - the fixes since Release 13 (#671–#674, #676, #721–#723, #839, #842, #905, #926, #966, the save-recovery card);
   - known limitations, including the inherited failing tests and that speed moves to Release 15;
   - the CLI and MCP error envelope now carry `"code": null`.
4. **Rollback runbook** (`releases/14/rollback.md`):
   - the last good Release 13 deployment and manifest (astrid.haus) and how to restore them;
   - who can restore them;
   - the triggers: a served-tuple mismatch after publish, or a save and reopen failure reported;
   - the steps, citing FIX-17's mixed-version rows as the evidence that an R14-written realm reopens on R13.

One fresh packet session submits the astrid-dev PR. The Lead reviews it and owns the publish itself.
