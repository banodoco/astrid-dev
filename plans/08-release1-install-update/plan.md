# Release 1: install and update

**Start here:** read [AGENTS.md](../../AGENTS.md), choose a workflow in the [skills guide](../../skills/README.md), follow the [run contract](../../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../../docs/glossary.md).

Prove that new users can install and update Astrid on Linux, macOS, and Windows, and that R0 users on Linux and macOS can upgrade to R1 without losing data. The project remains active under the Release 1 merge coordinator recorded in the [project queue](../../README.md); this plan does not start or authorize product work.

## Goal and scope

- **Included:** the strict five-row hosted direct-install gate; safe R0-to-R1 upgrade behavior on Linux and macOS; Windows refusal of that upgrade; stand-in next-version updates on all three operating systems; one Agent/App pin bump and one strict run.
- **Deferred:** Pinokio rows and routes ([Plan 07](../07-pinokio/plan.md)); the broader install/update confidence work in [Plan 09](../09-install-and-update-confidence/plan.md), including other routes, update consolidation, rollback fault injection, real-version migrations, Windows R0 upgrade, and post-upgrade uninstall.

The detailed R0 boundary, update assertions, and five job IDs are in [tasks.md](tasks.md). Preserve R0's data: R1 never writes the R0 root, and unsupported or ambiguous states refuse before mutation.

## What we build on

The work is based on the four repositories' `int/r1` integration heads and the R0 release served by the public install line. Prior landings and their custody are tracked in the R1 merge fixes log; exact source SHAs must be frozen for the strict run. The external R1 merge plan, decisions, and failure ledger are linked from [inputs.md](inputs.md).

## Sequence

Complete the open cleanup/refusal and update evidence, then the Windows refusal check. Bump Agent and App locks once to verified heads, run the strict gate once at frozen heads, and record the owner's ship call. Three earlier tasks are already recorded as complete; their evidence and the remaining task progress are indexed in [tasks.md](tasks.md).

## Completion

Completion requires a strict hosted pass on all five rows at frozen heads and a recorded owner ship decision. This demonstrates the specified install, update-mechanics, and safe-upgrade behavior; the same-code stand-in does not prove a real schema migration. The decision records the ship call but does not expand existing publication authority: follow the accepted R1 run and shared [run contract](../../skills/astrid-dev-shared/run-contract.md).

## Read next

- [tasks.md](tasks.md): task index, routes, dependencies, focused evidence, and progress.
- [inputs.md](inputs.md): repositories, source custody, references, and identity limits.
