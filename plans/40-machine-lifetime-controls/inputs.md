# Inputs — Machine lifetime controls

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Hannah chose this outcome on 10 Nov 2026 in session https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT. She asked for "a simple version" now, a proper RunPod version later: a machine that "doesn't have an automatic kill time" and "a way to quickly check when it's going to die". The orchestrator proposed (1) a display of when each machine is released, (2) `keep --for` with fresh consent, and (3) `keep --until-release` still bounded by a spend cap, and recommended against an uncapped option (a forgotten pod costs about $24 a day at $0.99/hr). Hannah: "Yeah, let's do that. Can you give that to a Codex manager? Can you spec it out?"

**Prior art:** read at Agent `origin/int/32-one-generation-path` 99724131d (nothing run).
- **Idle limit:** request, then `ASTRID_WARM_IDLE_SECONDS`, then 1800 s (`astrid/core/execution/warm_hold.py:27,30-44`; `astrid/packs/runpod/worker_owner.py:61-76`). The claim takes the smaller of the settings preference and the consented idle (`machine.py:551`); `acquire` refuses a larger idle (`worker_owner.py:300`); `settle` sets `idle_expires_at = min(now + idle, paid_expires_at)` (`worker_owner.py:351`).
- **Paid limit and cap:** `PaidRunConsent.validate` turns the cap into time, expiry = min(deadline, now + cap ÷ hourly) (`target_selection.py:264-282`), stored as `paid_limits` (`:513-516`) and `lease.paid_expires_at` (`worker_owner.py:313`). There is no separate spend meter: the cap is enforced only through that expiry.
- **Who releases:** only in-process timers in the host's `RunPodLeaseOwner` (`warm_hold.py:47-51`; `worker_owner.py:174-215`). If the host stops, the pod keeps billing until the next host's `recover()` releases it with reason `restart` (`worker_owner.py:217-231`, `adapter.py:291`). If the computer sleeps, release happens late, after it wakes (`worker_owner.py:201`).
- **Journal fields:** `hourly_usd`, `estimated_cost_usd`, `accounted_at`, `paid_expires_at`, `idle_expires_at` (`worker_owner.py:313-318,351`). `lease_row` shows `idle_expires_at` only while idle and hides the paid expiry (`machine.py:939`). Its cost is accrued only on reuse or release (`worker_owner.py:315-318,482-484`), so the shown cost is stale.
- **No extension exists, by design:** host operations are setup, ls, status and release (`adapter.py:144-160,415-419`); a machine id is accepted only for release (`sdk/generation.py:312-315`). Reuse refuses "existing claim lifetime cannot be extended by reuse" (`target_selection.py:472-477`) and replayed consent (`:478-480`); `packs/runpod/docs/SKILL.md:39-41`; tests `tests/packs/runpod/test_target_selection.py:504`, `tests/packs/runpod/test_warm_session.py:146,325,727`.

**Approach:** compared (a) all three as asked, with `--until-release` unbounded; (b) the display and `keep --for`, with `--until-release` as "keep up to the cap" (idle release off, expiry set by the cap); (c) the display only. Chose (b): (a) cannot be made safe, because the only enforcement is a timer in the host, which a crash or sleep stops; (c) does not give Hannah a way to keep a machine. (b) needs no new journal schema and no daemon: it reuses `lease_row`, `PaidRunConsent.validate`, the owner's `_arm` and the release task path, and drops the idle-only filter in `lease_row`.

**Challenge:** money and paid consent are involved, so a read-only critic (orchestrator-delegated, 10 Nov) traced the code above and recommended (b). Accepted:
- the keep operation lives on the owner, under its lock, needs the exact pod, a claimed record, an `idle` or `active` lease and the owner's current epoch, and refuses while a release is in flight;
- fresh consent goes through the existing `validate()` at the recorded rate and offer digest;
- cost is accrued to now before the new limit is written;
- keep must refuse when the host has no live owner: building a new owner there would run `recover()` and release the very pod the user wants to keep;
- the reuse rule is unchanged, and `SKILL.md` gains one sentence on keep.

Rejected: an uncapped keep; a pod-side cap (it would need a credential on the pod).

**Proof and limits:** CPU fakes through the real CLI and host operation, listed in [plan.md](plan.md#completion). No real pod is kept here; Plan 34 can check it live.

## Owner decisions

- **D1.** `--until-release` always needs `--max-usd`. It turns off idle release; the machine is released at the cap's expiry or on `astrid machines release`. No uncapped option. (Hannah agreed to the capped proposal, 10 Nov.)
- **D2.** Release needs a running host. `keep` refuses when no host owns the machine, and the CLI says that release happens only while a host is running. (A consequence of D1 and the current design; the provider-side cap is deferred.)
- **D3.** Ships with release 13, after Plan 32 lands on Agent `main` (Hannah put Plan 32 in release 13, 10 Nov).
- **D4.** One review round at the end, S route: the plan changes paid consent. No review stop: the plan is under five days and has one load-bearing task (T2), which the final review covers.

## Deferred

- A session-level keep: hold a machine across jobs and tools from one setting, with extend and release.
- Better default output: `generate` writes to `./outputs/<task-id>/` under the current folder, named by the workflow. A per-project folder and readable names are a separate follow-up.
- A provider-side or pod-side cap that holds when no host runs.

## Source identities

- **Base:** Agent `origin/int/32-one-generation-path` at 99724131d (Plan 32's integration branch; Plan 32 lands on `main` after release 12).
- **Integration branch:** `int/40-machine-lifetime` in astrid-agent, cut from int/32 at the run's start. When int/32 moves, merge it in (never rebase). When Plan 32 lands on `main`, merge `main` in.
- **Destination:** Agent `main` after Plan 32, in release 13.

## References

The critic's report is summarized above; the source lines are the record.
