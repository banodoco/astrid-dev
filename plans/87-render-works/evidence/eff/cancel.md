# Cancel and stuck task recovery — 22 Nov 2026

Source commits: Agent `ad10ff6de370db547e3ae2af45311751d228f98f` (dirty); Runtime `b2ea261f36f5f39c5f9964b02c8012c420e0b359`.

## Observations

1. **Lease expiry:** 20:46:10, task `012acee7276f4dd083acc6c397fc3f1a`, attempt `34e394859bd6490c99dc506cd1eb193d`: “task 012acee7276f4dd083acc6c397fc3f1a, attempt 34e394859bd6490c99dc506cd1eb193d: lease expired with unresolved custody; reconciliation required. Recover with: astrid tasks cancel 012acee7276f4dd083acc6c397fc3f1a”. 21:58:59, task `0e2e4fe68146438f9c19cfbb155b9098`, attempt `70b131ebf9724504aee061f7c452433b`: same wording with its IDs (`take/almost-ready-v38-full.log:5`; `take/ranges-status.log:10`). Producer `astrid/sdk/invocation.py:3612–3627`; renewal cause unknown (`astra20/REPORT.md:3`). Cancels 20:46:30.492 / 21:59:04.162: `stop_observed=false`, state `cancelled` (`astra20/REPORT.md:11,13,41`; snapshots).
2. **Custody cleanup:** 21:09:35, task `8ce6fa34e4c34558a197316aff737f1e`: “owned command cleanup uncertain: post-capture candidate is LIVE; terminal disposition is ineligible; original execution failure: CustodyError: post-capture candidate is LIVE; terminal disposition is ineligible” (`take/almost-ready-v38-full-3.log:24`; `generic_host.py:10944–10949`). Artifact: `retained-cleanup-containment.json` (`twentymin/REPORT.md:81`).
3. **Poisoned session:** “managed session release was not verified”, 21:11:39–21:13:10; task IDs `1bfaac89d0f34416a89534ba7c4e302e`, `ca34f94217334e6fa8bdcb3bc5bd5652`; first retry ID not found (`take/ranges-status.log:2–5`; `take/r6-part0-try2.log:4`; `try3.log:4`). Unverified release keeps `_active`: `managed_tool_session.py:527–545` (#1474).
4. **Occupancy:** queued at 21:59:27: “current executor occupancy: registered_host=astrid-pack-host active_tasks=1”; queued task ID not logged (`take/r6-part1-try2.log:1–2`). Producer `astrid/sdk/invocation.py:3528–3534`; count `store.py:4410–4412`.
5. **Orphan queue:** 22:03:03 “ADOPT waiting for task 480bca0b78d64ce89c88ffc626f463cf (part 1, 50-100)” after 22:00:58 restart; failed 22:04:33 (`take/ranges-status.log:11–14`). Client-ended claim/liveness unverified (#1502); repro: queue behind blocked session, end client, restart.
6. **Scratch:** 20:48:43: “task admission refused: needs 6.90 GB plus 2.15 GB free-space reserve; 7.74 GB free. Free disk space and try again.” Task ID not found (`take/almost-ready-v38-full-2.log:1`); producer `Runtime/store.py:3215`. #1475 reports 2.9 GB under `data/attempts/<id>/astrid-attempt-*`; host cleanup `generic_host.py:789–805,14045–14053`; no clearing command found.
7. **Cancel after failure:** task `5327fa0e32eb4c2e84995564486dcf2f`; response `ok:true`, remains `failed` (`tighten/FRICTION.md:72–82`). Runtime returns terminal unchanged (`store.py:6575–6580`). RW-15 wording (`shipplan/PLAN.md:165`, `VERDICTS.md:139`); cancel wording not found in `edits/DEFECTS.md`.

## Recovery in source

`domain_tasks.py:236–244` → `server.py:1345–1353` → `service.py:8117–8155` → `store.py:6561–6667`. Cancel does not signal processes; host polling aborts and cleans process group (`generic_host.py:12065–12072,10930–10949`). Reconcile settles attempt/contains delegated children (`store.py:3608–3628`); reaper preserves expired blockers, no auto-reconcile (`4093–4142`). Exact owner release requires adapter proof (`generic_host.py:7278–7307`; `managed_tool_session.py:474–498`); no force-clear CLI. Scratch cleanup is host-only.

## Issues

Open: #1472 “bug: long renders lose the execution lease while the Runtime is unresponsive”; #1473 “bug: custody cleanup aborts a live render when descendant capture fails”; #1474 “bug: a failed render leaves the managed session slot occupied”; #1475 “bug: failed render scratch is not reclaimed and blocks the next admission”; #1476 “bug: render failures and frame progress are invisible outside the invoking command”; #1502 “bug: an orphaned queued render is claimed after a source-stack restart”; #1320 “observation: timelines visualize fails with ‘renderer lease channel closed’ after about 57 seconds from source in a container”; #1246 “bug: a failed timeline commit can leave the timeline stuck with no supported way to clear it”; #1430 “Restore removed clips or revert a time range to an earlier revision”; #759 “Source Runtime: identity mismatch after source changes, and a stale pack-host registration after restart”. All are open. No dedicated cancel/reconciliation issue found; search: cancel/reconciliation/custody/lease/occupancy/session release. PR-D/H unfiled (`shipplan/VERDICTS.md:139`).

## Draft issue

**Title:** Reconcile failed render custody and report truthful task cancellation

Film project:
1. “lease expired with unresolved custody; reconciliation required” (`astrid/sdk/invocation.py:3623–3627`); repro: expiry; expected: verified stop.
2. “owned command cleanup uncertain” (`astrid/core/execution/generic_host.py:10944–10949`); repro: live descendant/capture failure; expected: verified cleanup.
3. “managed session release was not verified” (`astrid/core/execution/managed_tool_session.py:536–545`); repro: failed release, retry render; expected: owner release.
4. “current executor occupancy: registered_host=astrid-pack-host active_tasks=1” (`astrid/sdk/invocation.py:3528–3534`); repro: dead task; expected: accurate count.
5. “ADOPT waiting for task …” (`take/ranges-status.log:13`; #1502); repro: end client/restart; expected: explicit recovery.
6. Admission scratch refusal (`Runtime/store.py:3215`; #1475); repro: failed task/low disk; expected: safe cleanup.
7. Cancel failed task succeeds but stays failed (`store.py:6575–6580`); repro: cancel terminal task; expected: truthful state.

Related: #1472–#1476, #1502, #1320.
