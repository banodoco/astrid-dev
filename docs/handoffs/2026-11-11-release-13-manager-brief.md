# Release 13 manager brief

Start message for the one manager session that owns generation. Written 11 Nov 2026 after the split.

## Your job

Make the generation path one that can be run and debugged without confusion, then rebuild it on published Release 12 and prove it live. Read, in this order: [Release 13](../../releases/13.md) (findings, phases, GPU rules, budget, open decisions), the [Release 12 operating principles](../../releases/12.md#operating-principles), the [iterate skill](../../skills/astrid-dev-iterate/SKILL.md) and the [run contract's cheapest-first rule](../../skills/astrid-dev-shared/run-contract.md#cheapest-model-first). The [task detail](../../releases/13/generation.md) and the [transition handoff](2026-11-11-release12-track-b-transition.md) are reference for SHAs, task cards and the GPU cell table; their cross-track protocol is superseded.

## What you may do now

**Phase 0 only, and only unpaid work.** Release 12 has not published, so there is nothing to rebuild on yet, and no budget is authorized.

- **Start immediately:** G1 (launch-and-wait instruction), G2 (fence the other launchers), G4 (one source of truth for pins), G5 (choose one attach design).
- **G3 (the failure receipt): design now, build after H10.** The design can be written and reviewed today. It brings redacted logs back from a pod, which the current rule forbids, so do not merge an implementation until the orchestrator confirms Hannah's answer.
- Work on fresh branches off `release12/gen-candidate` `1439ccc6`. Do not push to any `main`, any `cand/` branch or the Release 12 branches.

## How to work

- **You manage; sub-agents do.** Start each task on the cheapest model that could plausibly do it and escalate one step only on evidence. A worker brief names one outcome, the exact repository, branch and files, what "done" looks like, and what to return.
- **Verify before you document.** G1's commands, flags and GPU display names must be read from the code at the candidate, not copied from a handoff. The handoffs' example commands use GPUs the owner has since ruled out.
- **Check diffs and output, not summaries.** Rule on every finding within the hour.
- **Iterate freely** on CPU. Keep raw logs. Never weaken a check.

## Paid work

**None until the orchestrator tells you H11 is answered and Release 12 is published.** When it is:

- RTX 4090 or RTX 5090 only; video cells name the 5090 alone.
- One waiting product command per cell. Waiting for stock is normal: `stock_unavailable` in a preview or progress line is not a failure. Do not add time windows, geographic filters or your own retry loop.
- A census before each rental and after each release. You supervise a rented machine until the census is empty; no check-in or scheduler does that for you.
- Money is reported as "spent $X of $Y".
- The RunPod credential is not present in a fresh session. Request it through the supported private mechanism when Phase 2 starts; never print it.

## What comes to the orchestrator

A direct message with a recommendation for: any decision that is Hannah's (H10, H11 and H12 are already open), the G5 attach-design choice with its evidence, and any blocker you cannot clear in half a day. The orchestrator checks in about every three hours and tells you when Release 12 is published and on which SHAs.

## Limits

No force-push or rebase. Never read `.env` or credential files. No model names in commits or pull requests. Do not retry or route around the GPU evidence record that an automatic approval review rejected; that decision is the orchestrator's.
