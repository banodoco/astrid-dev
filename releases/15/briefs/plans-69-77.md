# Release 15 lane brief — Plans 69 then 77

[Release 15](../../15.md) · [Run board](../run.md)

You are the **manager** for two Release 15 plans, run back to back by you alone: first [Plan 69](../../../plans/69-project-elements/plan.md), then [Plan 77](../../../plans/77-saving-holds-on-a-heavy-timeline/plan.md). Use the [Manage skill](../../../agent/roles/manager.md): its [whole-project workstream](../../../agent/roles/manager/whole-project.md) for Plan 69 and its [live-loop workstream](../../../agent/roles/manager/live-loop.md) for Plan 77. The owner set this order on 21 November 2026 ([decision](https://github.com/banodoco/astrid-dev/issues/1224#issuecomment-7067275617)).

## The two plans

| | Plan 69 — editing a real clip | Plan 77 — saving holds on a heavy timeline |
| --- | --- | --- |
| What | Land the editing work the owner already did: project elements (a project's own effects and components) and practical editor and timeline fixes | A live loop: build a heavy timeline, test every edit in the real editor, fix what is slow or refused, repeat until saves take about 2 s |
| State | Code done on `release/15/plan-69`; check it, settle one question, land it | Not started; branches ready, with Plan 69 and Release 14's Plan 59 integration already merged in |
| Tasks | PE-1 inventory, PE-2 [#1222](https://github.com/banodoco/astrid-dev/issues/1222), PE-3 land, R | SL-0 fixture, SL-1 stack, SL-2 harness, SL-3 recover crash work, SL-4 the loop, R |
| Start here | [handover](../../../plans/69-project-elements/handover.md) | [handover](../../../plans/77-saving-holds-on-a-heavy-timeline/handover.md) |
| Estimate | about 2 days | about 4 days, more if rounds need it |

## Order

1. **Plan 69:** PE-1 and PE-2 in parallel, then the review, then ask the owner's go for PE-3 (landing into `release/15/main`).
2. **Plan 77:** start as soon as you have asked for that go; do not wait for it. Its first action brings its branches current with Plan 69 ([handover](../../../plans/77-saving-holds-on-a-heavy-timeline/handover.md#first-actions-on-a-new-machine)).
3. When Plan 69 lands, merge `release/15/main` into `release/15/plan-77` before the next loop round.

## Building on the existing code

Nothing is rebuilt from scratch, and nothing is rebased: newer work comes in by merge, and pins are regenerated after each merge ([how](../../../plans/69-project-elements/handover.md#pins)).

- **Already in the branches:** `release/15/plan-69` holds the owner's editing work on top of `release/15/main` (which holds `release/14/main`). `release/15/plan-77` holds all of that, plus Release 14's integration of Plans 59, 64 and 65 and the 18 November save-loop harness. Plan 77's SL-3 ports the crash-day branches listed in its handover.
- **Plan 69, before landing:** merge `release/15/main` into `release/15/plan-69` (PE-3).
- **Plan 77, at its start and before each loop round:** merge in whatever is newer, in this order: `release/15/plan-69` (or `release/15/main` once Plan 69 has landed), then Release 14's work.
- **Release 14's work, when it moves:** when the Release 14 Lead lands `release/14/int-59-64-65` (Plan 59 with App R14-FIX-16) in `release/14/main`, merge `release/14/main` directly into each `release/15/plan-77` yourself; Plan 77's authority allows it, and you need not wait for a forward into `release/15/main`. Its save-path conflicts are the Lead's combination already made, so take `release/14/main`'s side unless a test says otherwise.

## Before you start

- **Read, in order:** this brief; [releases/15.md](../../15.md) (Included plans, Branches); Plan 69's handover, tasks and inputs; Plan 77's handover, plan and tasks.
- **Bindings:** one `run.yaml` per plan, from [Plan 77's handover](../../../plans/77-saving-holds-on-a-heavy-timeline/handover.md#runyaml): models checked on 21 November, who runs what, and when to move up a tier. Workers run on Codex; you keep every judgment.
- **Machine:** Plan 69 runs anywhere with Python 3.11+, Node 22 and the renderer's Node 20.19.4. Plan 77's stack needs either a Mac with a live Astrid install (the release script) or the direct route in its SL-1, and 25 GB free.
- **Check the heads** with `git ls-remote` against the tables in each handover.

## Authority

- **May, without asking:** open and merge pull requests into `release/15/plan-69` and `release/15/plan-77` after focused proof; dispatch workers; merge `release/15/main`, `release/15/plan-69` and `release/14/main` into those branches as above; regenerate pins; update both plans' `tasks.md`, `inputs.md`, `handover.md` and Plan 77's `rounds.md` through astrid-dev pull requests.
- **Needs the owner:** landing either plan into `release/15/main`; anything into `release/14/*` or a product `main`; publishing; touching a live install or the owner's timelines; paid spend.
- **Not yours:** forwarding Release 14 into `release/15/main` itself, and Release 15's run board beyond your lane's line. The release manager named in the brief was the setup session and may not be running; if it does not answer, ask the owner.

## Report

- **Progress:** each plan's `tasks.md` is its record, updated by small PRs as the whole-project workstream says; Plan 77's rounds go in its `rounds.md`.
- **Your lane line:** keep it current on the [run board](../run.md).
- **Stop and ask the owner** when a Plan 77 stop rule fires, when PE-2's answer needs a design change, or when a merge of `release/15/main` brings a conflict on the save path you cannot settle from the code.

## Known open items

- [#1222](https://github.com/banodoco/astrid-dev/issues/1222): the Runtime CAS question (Plan 69, PE-2).
- **App R14-FIX-16** (stop on a rejected save, copy out or discard) is not yet in Release 15. It waits for the Release 14 Lead to combine it with Plan 59's save work. When it arrives through a forward, Plan 77 must take it in: it changes exactly what the loop measures.
- **[Plan 78](../../../plans/78-live-custom-element-editing/plan.md)** (live custom-element editing) also builds on Plan 69. It is in Release 15 but not in this lane unless the owner adds it.
