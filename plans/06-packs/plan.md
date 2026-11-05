# Packs v1.3

**Start here:** read [AGENTS.md](../../AGENTS.md), choose a workflow in the [skills guide](../../skills/README.md), follow the [run contract](../../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../../docs/glossary.md).

Move the existing 19-pack CPU scope out of Agent core into `poms_packs`, while keeping supported workflows working. Finish the pack installation, discovery, update, and editing integration across Agent, Runtime, and App, then promote the reviewed result to `pre-main`.

“v1.3” is a working project name, not a confirmed package/release version. Current status, owner, and estimate live in the [project queue](../../README.md).

## What we build on

| Existing input | How we use it |
|---|---|
| Verified Hivemind and core/pack boundary work (PK-2 and PK-3) | Reuse the accepted commits and evidence; do not rebuild them without a changed dependency. |
| Namespace/schema repairs and retained PK-4 work | Preserve the fixes and resolve the recorded core/pack boundary failure. |
| Eight parked feature branches and the accepted Agent health changes | Compose their retained work once, preserving required behavior. |
| Current Agent, Runtime, and App `pre-main`, plus the poms base | Provide the integration bases after Release fixes integration (Plan 05), which includes the earlier generation and concurrent-editing increments. |

These are historical retained inputs, not a fresh execution report. Their exact identities and evidence sources are in [inputs.md](inputs.md).

## The sequence

1. **Repair the known boundary failure.** After project start, fix the recorded PK-4 core/pack and locking problem on the retained inputs. This can happen before the final integration bases are ready.
2. **Freeze the integration bases and combine retained work.** After [Release fixes integration](../05-remaining-fixes/plan.md), PK-0 records current bases. Combine the parked work and namespace/schema repairs without losing completed work.
3. **Finish pack behavior across the repositories.** Complete the Agent's discovery, trust, transactions, rendering, and management work. Runtime's data-move work can proceed independently once PK-0 is ready. App loading work waits for that Runtime result and the transaction checks, not the whole Agent chain.
4. **Move and prove the packs.** Remove the designated packs from core, install them from `poms_packs`, and check the installed CPU and browser journeys. Complete the existing transaction and final reviews.
5. **Promote the reviewed result.** Publish the immutable candidate, then promote those same reviewed commits to `pre-main`. If the destination moved, reconcile and recheck only affected work; do not build a second combined release by default.

## What this does not include

GPU work, H3 changes, and training remain deferred; H3, RunPod, and training stay in core as the existing migration card specifies. The 19 packs are not a count of remaining tasks. Only the original focused checks are authorized—no broad suites or new review gates.

Read [tasks.md](tasks.md) for the task index and individual instructions. Read [inputs.md](inputs.md) for branches, preserved commits, original cards, and publication rules. This reorganization does not start or resume product work.
