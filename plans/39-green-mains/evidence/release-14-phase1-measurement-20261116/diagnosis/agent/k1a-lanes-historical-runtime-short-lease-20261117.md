# K1 prerequisite: missing historical Runtime commit in Agent Lanes short-lease integration

**Observation date:** 2026-11-17 UTC. **Route:** N-class read-only source/hosted-artifact diagnosis; **not reviewed or implemented**. This is separate from the historical RE3 Agent-object failure and from Runtime's replay/CAS-history contract. Only an explicit source check / proper provisioning repair is potentially justified here; tests and their security/lease assertions must not be relaxed.

## Exact hosted observation

At Agent's reviewed Plan 39 merged head `6bbda788c1a62abcdda242f85c7a1cae86c57d3d` (tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`), [Lanes run 43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160), attempt 1, completed **failure**. [Integration shard 3 job 133651923800](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/job/133651923800) produced [actual JUnit artifact 14285717945](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/artifacts/14285717945), ZIP SHA-256 `f0da81cc7c13bb8e8c0bac64f6a389b32a96c79406ec67fa6780b71bca76cb70`, inner XML `2851d730e6bafd2452071c7e13f70ee7b1eaf7c24503f9201f51c89b09c14d40`.

Two **specific** JUnit setup-error testcase IDs, counted exactly (not independent causes):

- `tests.integrations.test_generic_host_runtime_restart::test_real_host_renews_short_lease_during_cpu_execution`
- `tests.integrations.test_generic_host_runtime_restart::test_expired_real_lease_rejects_renewal_and_host_fails_closed`

**Exact shared literal XML error, count 2:**

```text
failed on setup with "Failed: the Runtime checkout /home/runner/work/astrid-agent/astrid-agent/astrid-runtime has no commit df3d4ddac7bf73cd858106cc51a802521a4d3552"
```

Both IDs and their **error** outcomes exist in the earlier [prior-plan Lanes shard 3 XML artifact 14277921134](https://github.com/banodoco/astrid-agent/actions/runs/43934820639/artifacts/14277921134) (prior plan head `b8f2692948d1b5987ee2938920f47aace0732792`). The new and old complete shard each have exactly the same 516 IDs and outcomes (372P/81F/62E/1S); no newly red status is claimed for either setup case. Frozen G1 shard3 XML is unavailable.

## Source trace on the exact tested head

1. [`tests/integrations/test_generic_host_runtime_restart.py`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/integrations/test_generic_host_runtime_restart.py#L20-L49) has module constant `_PINNED_RUNTIME = "df3d4ddac7bf73cd858106cc51a802521a4d3552"`; the `short_lease_runtime_source` fixture calls `use_runtime(_PINNED_RUNTIME)` **before** the actual host and lease behavior is exercised.
2. [`tests/helpers/runtime.py`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/helpers/runtime.py#L70-L97) requires `git cat-file -e df3d4dd...^{commit}` in the checkout, then a successful `git archive`. It fails explicitly if the pinned commit cannot be resolved or archived. It is not a user-facing Runtime protocol rejection.
3. [Agent `lanes.yml`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/.github/workflows/lanes.yml#L57-L109) obtains the lockfile Runtime via a normal `actions/checkout@v4` (which defaults to a shallow checkout), then explicitly fetches **nine** historical Runtime hashes: `11443b0`, `959ce04`, `efcb326`, `d9e2a71`, `1e6d899`, `becfe6d`, `6634a17`, `f103bb4`, `9ef8087`. **`df3d4dd` is not among them.** Its follow-up verification only verifies locked Runtime and historical `efcb326`.
4. GitHub resolves [Runtime source commit `df3d4ddac7bf73cd858106cc51a802521a4d3552`](https://github.com/banodoco/astrid-runtime/commit/df3d4ddac7bf73cd858106cc51a802521a4d3552) normally; this is not proof that the hosted checkout actually contained it. The real XML establishes that the hosted checkout could not access it.

**Classification:** strong and independently bounded **test-runner history-provisioning prerequisite candidate**, not proof of a product failure, stale test expectation, or a new PR369 regression. An additive exact-SHA fetch followed by `git cat-file` and matching revision verification would be a possible narrow remedy **only after owner/scope clearance and focused independent review**. Do not replace the test's source SHA or silently accept an arbitrary current Runtime: short-lease behavior was asserted on this deliberately pinned implementation. Existing history fetch / failing tests should remain visible until real proof.

## Ownership and repair stop

The two tests exercise GenericPackHost short leases and Runtime–SDK host behavior; [Plan 55's test inventory](https://github.com/banodoco/astrid-dev/blob/p39/g1/plans/55-local-speed/tasks.md#L44) explicitly owns Agent generic-host / SDK execution categories (though it does not name this *exact* integration path), and Plan 55's LS-7 owns the lease/host handoff. **Do not assign the two IDs to Plan 39 or edit the Plan 55 test contract based solely on a family match.** Obtain explicit task-owner confirmation of whether *environment-only historical source availability* may be repaired independently of the waiting Plan55 behavior work. If allowed, use an N-class isolated task branch, exact fetch-and-verify proof plus an independent reviewer before any PR merge; do not weaken lease assertions or move these tests into an opt-out lane.

This note does not perform a product change, mark K1a policy green, remove a held test, change Plan38/55 ownership, or advance formal G1/G2/RS1. The unrelated Windows-native selector draft [Agent PR373](https://github.com/banodoco/astrid-agent/pull/373) still awaits independent review and actual hosted Windows execution. Runtime replay/CAS corruption owner decision remains separate.
