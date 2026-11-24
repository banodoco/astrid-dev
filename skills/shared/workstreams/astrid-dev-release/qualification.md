# Release qualification

## Workstream contract

**Outcome:** By the freeze, a one-page verdict on whether the candidate meets the release's bar, with evidence.
**When to use:** Every release, from the day it has a freeze date.
**Inputs:** The brief, `run.md`, the served release's runs and heads, each plan's proof.
**Procedure:** Write the bar, map coverage, build only gaps, re-run the rest on the frozen candidate.
**Completion:** Every row of `releases/<N>/qualification.md` is closed by evidence and the Lead holds the verdict.

## Who

One **Qualifier** session per release reports to the release [Lead](../../../roles/astrid-dev-lead/SKILL.md). It has its own board, `board: release <N> qualification`, and rolling ChatGPT queue ([rolling queue](../../../roles/astrid-dev-lead/workstreams/multi-manager-release.md#rolling-queue)). Its launch message is a short pointer to this page and `run.md`; [check-ins](../../run-contract.md#coordination-boards-and-check-ins) follow the run contract. It reports; acceptance is the Lead's recommendation and the owner's call.

## The bar

Each release records its bar in `releases/<N>/qualification.md` ([Release 15's](../../../../releases/15/qualification.md) is the model).

- **Tier 1 blocks shipping:**
  - no new failures against the published previous release, by id, whole run to whole run, in every repository;
  - each promise of the release works on a real installed build of the frozen candidate;
  - Agent writes open in the App;
  - update from the previous release, plus rollback;
  - nothing harmful;
  - the owner's go on exact SHAs.
- **Tier 2** should pass, or ship as a known issue with the owner's OK.
- **Tier 3** is not this release.

**Rolled back** means the product's own rollback, not a reinstall, restores the previous release's exact App, Agent and Runtime versions. Its Runtime starts and opens a project saved under the new release, timeline identical wherever it can represent it; one edit saves; updating again works.

## The coverage map is the backlog

Each checklist row has **Covered by** (plan, task, evidence), **Gap** and a kind:
- **re-run:** the plan's own tool, wrapped, on the candidate, so numbers stay comparable (same method);
- **new:** a gap nobody covers; only these are built;
- **N/A:** with the reason.

Order rows by user harm, then freeze risk. Name the row before writing any script; a re-run row needs no new code. A new row is a no-network packet, or stays with the Qualifier (installed runs, hosted CI, harm).

## Phases

- **Phase 0**, from the moment the release has a freeze date: write the bar and each repository's previous-release reference set, script the installed journeys, and dry-run them on each landing.
- **Phase 1**, on the frozen candidate: everything, timing-sensitive journeys twice, then the one-page verdict.

## Autonomy

The Qualifier orders its own backlog, cuts its own packets, and takes free CI slots, landing gates first. It escalates only landing into the release branch, a failure it judges harmful, freeze risk, and disagreement with a plan's numbers (post both numbers). It never fixes plan code; findings go to the owning plan's board.

## Lessons from Release 15

- Check which version is actually installed before trusting a measurement: the App's pins can install another plan's Runtime.
- Rebuild fixtures from a recipe in a repository; never hold one only in a session's container.
- Forward the previous release's harness fixes, or its journey workflows cannot pass.
