---
description: Prepare and lead fresh-session packet delivery across accepted release work without delegating the Lead's review or integration authority.
---

# Workstream: fresh-session ChatGPT packet dispatch

## Workstream contract

**Outcome:** Lead-prepared, authorized release packets with one durable dispatch queue and review-ready task evidence.
**When to use:** When the Lead coordinates accepted release work through fresh ChatGPT manager sessions rather than a single long-lived manager.
**Inputs:** An approved release brief, current plan task records, packet scope and dependencies, owner authorization, branch destinations and evidence requirements.
**Procedure:** Prepare bounded packets and one mailbox, run Lead check-ins, review delivered task PRs and integrate only authorized work using the sections below.
**Completion:** The queue and task records reflect every packet, its evidence and disposition, with review/integration decisions owned by the Lead.

Use when the Lead prepares accepted plan work for an Orchestrator to assign to **a fresh ChatGPT manager session per packet**. The [Lead responsibilities](../SKILL.md) continue to apply.

**A lane can be the Lead for its own plan.** In a release run by [lane orchestrators](lane-orchestrators.md), a lane's orchestrator may take the Lead's part here for its own plan: it writes and reviews packets, merges into its plan branch and runs the proofs needing an installed stack or the network. It gets its own dispatch manager and mailbox; the release Lead keeps only the gate into `release/<N>/main` (Release 15, Plans 87 and 89).

## Set up once

1. **Prepare packets.** Start from what exists: bring each plan's `tasks.md` up to date, and ask any earlier manager to push its work, write a handover and stop; its open drafts become packet inputs. Group ready, compatible task IDs from **one plan** into briefs of at most ~**three human engineering days** each. An **issue packet** groups issues from the brief's list instead; its fix branches `release/<N>/<topic>` target `release/<N>/main`, per [Release](../../../shared/workstreams/astrid-dev-release/SKILL.md). Give each packet the Route of its hardest card, honestly: it sets the session's mode. Put them at `releases/<N>/packets/<id>.md` using [the packet template](../../../../templates/release/packet.md). Link, never copy, tasks, dependencies and proof; split oversized tasks first. Order the queue by priority; cap Running plus Review at what you can review. A meter, gate or check brief states which realistic ways to get to green it must catch: skips, xfails and deselection through markers, `-k`, `-m`, config or `PYTEST_ADDOPTS`. Fail closed if a registry, baseline or ceiling approves itself or grows, if a PR changes the gate without approval or runs its own gate code, or if results are missing, truncated or show zero tests. Leave crafted bypasses to path protection and human review.
**Write each packet to finish in one run** (Release 15, Plans 56, 87, 89, 82: [ledger](../../../../docs/ledger/2026-11-24-dispatch-lessons.md)). - **One contract per packet, aimed at about 3 hours.** Never bundle cards; split a big card at its seams.
- **Rule before dispatch.** Run a local baseline on the plan branch and write into the packet its exact focused selectors, the ids that already fail, the tests that must pass unchanged, and both **May touch** (files and functions) and **Must not touch**; a packet without both is not Ready. See the [packet workstream](../../astrid-dev-manage/workstreams/chatgpt-packet.md).
- **Orchestrator-run, never the packet's:** network clones and builds, the UI model or mode selector (the manager confirms it), timings and installed measurements, anything needing a real ComfyUI, GPU, installed build or generated catalog, and the proof itself. The packet ends with `READY-PROOF <repo> <PR> <head> <selectors>`. A cache or speed packet emits its counters (hit, miss, recompute); the lane reads them before trusting a timing and measures the numeric gate on the exact head.
- **A sweep carries its count:** every site found and every site changed, in the PR before review. Audit it against a count you take yourself.

2. **Prepare one queue.** List each packet in `releases/<N>/run.md` with its handoff state, session and next action. A packet is **Ready** only when every PR or packet it depends on has merged into its destination; otherwise **Blocked**, the dependency named in its row. `tasks.md` stays the record of progress.
3. **Own plan-level completion.** For plans assigned through this workstream, record the **Lead as the accountable agent** on its `inputs.md` Run start, with the owner's authorization; there is **no separate plan manager**. You review and land accepted task PRs, keep `tasks.md` current on `main`, and do the plan manager's [Release](../../../shared/workstreams/astrid-dev-release/SKILL.md#how-a-release-runs) steps: merging `release/<N>/main` into plan branches, and landing them. Review stops (RS1, R) are yours: commission an independent reviewer, not a packet.
4. **Prepare the boards.** Reuse the release's existing boards, or create them ([rules](../../../shared/run-contract.md#coordination-boards-and-check-ins)) by their titles; no packet issues, no labels.
5. **Hand off to the owner** with queue and mailbox links, ready/blocked packets, missing authorization and the Orchestrator launch message, filled in from the [run board template](../../../../templates/release/run.md#orchestrator-launch-message). The board's startup checks verify access, session creation, resume, the hour and the mailbox; describe any manual steps.

## At each Lead check-in

**Inputs:** your boards since your cursor, including every packet the Orchestrator's STATUS marks Review; open packet PRs; and `python3 scripts/release_branches.py check <N>`.

**Each Review:** accept, merge, open the `tasks.md` progress PR and post DONE; or list the rework on the PR and post a DECISION. Accept a gate only after the reviewer injects the realistic failures in its brief and sees the gate reject them. Judge against that threat model and leave crafted bypasses out of the findings. Route each reviewer by the run contract:

<!-- block:routing:start -->
<!-- Generated by Astrid Dev view: block-routing-skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md; sources: skills/shared/run-contract.md. Do not edit. -->
Default model for each route, using the newest available model of that family:

| Route | Work | Claude | Codex |
| --- | --- | --- | --- |
| `N` | Everything below very hard, including ordinary hard work: research, reading, running checks, most changes and fixes | Haiku | Luna |
| `X` | Very hard: intricate changes, subtle bugs, coupled or non-obvious reasoning | Sonnet | Terra |
| `S` | Super hard: deep design, or correctness that needs the deepest reasoning | Opus | Sol |
| `T` | Taste: small, editorial refinement of something that already exists, such as user-facing copy, error and refusal messages, names, a screen's layout or a doc's voice | Opus | Astra |

Reviews, plan judgment and advice use a separate high-judgment role: Opus (Claude) or Astra (Codex); configure it in run.yaml as `completion_reviewer`, `plan_judgment` and `advisor`.

**Reviews.** A review's verdict runs on the high-judgment role. A check of a bounded fix against a named oracle (its failing case or probe) may run on `X`. `N` may gather facts for a review (check status, failure IDs, diff scope) but never gives the verdict. Check a pure sync by tree equality. A bounded-fix check runs the focused tests on both base and head. A bounded-fix check goes to the high-judgment role only when its own tests cannot show it is right (see the per-card rule under [review and promotion boundaries](../../../shared/run-contract.md#review-and-promotion-boundaries)); size alone is not a reason. A meter, gate or check is reviewed by injecting the failures it must catch. The run names the actual reviewer model, flags and permissions where it records its bindings (`run.yaml`, or the run board for a dispatch run).

*From [Routing and bindings](../../../shared/run-contract.md#routing-and-bindings); edit it there.*
<!-- block:routing:end -->

**Fix it yourself when it is small.** Instead of posting rework, have a sub-agent make the fixes when all of these hold:
- the review grades the packet B+ or better;
- it leaves at most four must-fix items, each in one place, about 50 changed lines or fewer, with a failing case that defines done;
- none changes a design, protocol, schema, threat model, product default, pin or existing assertion;
- the packet's session has submitted, and its branch has not moved for 30 minutes.

The sub-agent works on the packet's branch, adding each failing-before case, in commits labelled `Lead review fixes`. A second, faster reviewer checks them; then merge and post DONE as usual. Otherwise, post the rework.

**Judge like a light gatekeeper.** Reviewers sort findings into BLOCKING, FOLLOW-UP or NOTE; block only on wrong results accepted, data or install damage, a real security or custody hole, or a regression from base. File the rest of a PR's follow-ups as one issue in astrid-dev, marked `backlog` and linked from the PR. A `tasks.md` row is for work the release must do. A regression the candidate introduced is fixed in its packet. A defect that predates it gets an issue and a test that stays executed and visibly failing, and the packet does not fix it. Changing an existing assertion, including turning a gate's limit into an observation, is the owner's call unless she has delegated it. An Orchestrator acting on her direct instructions needs her confirmation in its own chat.

**Keep work moving.** When a packet has waited more than two hours on hosted jobs, read its run list: pull-request CI may run only part of a suite, so dispatch the full run it is waiting for. Every few hours, ask a high-judgment reviewer for a second opinion on bottlenecks, order and scope; bring what exceeds your authority to the owner.

**Before merging:** find every pin change: each needs its own commit and the owner's approval or delegation. After a dependency's PR is squash-merged, re-point its pin to the squash commit. Give a gate at most two review rounds; round two only verifies round one's fixes. Then merge.

**Rulings:** when a ruling will recur, add it to the board's Standing rulings (`releases/<N>/run.md`), so that a fresh Lead, Orchestrator or packet session finds it without reading the mailbox. A ruling that holds beyond the release goes into its skill instead, and the board links it.

**Then:** triage the release's issues ([states](../../../../docs/contribution-workflow.md#issues)): an issue a task row or packet cites is `planned`, and one that a branch, pull request or running packet names is `claimed`, whoever started it. Give each uncited issue a row, or move it out. Move unblocked packets to Ready, write the next, copy the Orchestrator's STATUS into the board and refresh Now and Waiting on the owner. No Orchestrator STATUS for 2 hours, or a message of yours missing from its `acted on:` line, is the owner's to hear. Schedule your own check-ins with a scheduler that outlives your machine, re-armed each time; else say which nudge the owner gives.

## Rolling queue

When the work is not known up front (a [release qualifier](../../../shared/workstreams/astrid-dev-release/qualification.md) finding failures as it goes), the queue grows as findings arrive and the manager polls it hourly. The finder cuts an **issue packet** from the packet template, with its Repro, only when all hold:
- a failing test or exact repro that a sandbox with no network can target;
- a bounded fix of about 3 hours or less;
- a cause no plan owns.

A failure in a plan's own code goes back to that plan's lane; cross-lane findings go lane to lane. Fixes target `release/<N>/<topic>` → `release/<N>/main`. Anything that needs judgement about acceptability goes to the Lead.

## Standby Lead

When the Lead's own session may stop without warning (a usage allowance, a lost container), the owner can keep a **standby Lead** in another session, on the high-judgment role of the other family.
- **Heartbeat.** The Lead posts its hourly `STATUS` ([rules](../../../shared/run-contract.md#coordination-boards-and-check-ins)), even when nothing moved, with a marker the standby can recognise (for example its tool's footer).
- **Wait.** The standby checks the mailbox every hour and posts nothing while the newest Lead message is less than 3 hours old.
- **Take over.** After 3 hours of silence, the standby first rules out a quiet Lead: no Lead commit, branch push, pull request or board edit in those 3 hours. Then it posts one takeover message, keeps the same mailbox name, and runs the Lead's check-ins under the same Authority.
- **One Lead.** Once a takeover message exists, the earlier Lead stands down if it returns, and does nothing until the owner hands the role back.

The release keeps the standby's brief and the environment notes beside its run board, under `releases/<N>/lead/`.
