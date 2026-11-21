# Inputs — Project elements

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner said on 21 November 2026 that this work ("the existing timeline work that we're working on top of") goes into the next release and should be set up properly with its plan and branch, but has not confirmed the outcome as written in [plan.md](plan.md), which is read from the commits. Next: the owner confirms or corrects the outcome.

**Prior art:** The work itself, on `release/14/plan-69`, 18 to 21 November 2026; commit lists per repository are in [source identities](#source-identities). No astrid-dev plan, pull request or issue recorded it before this pack (searched 21 November: plans, releases, pull requests, issues and the Release 14 mailbox #796).

**Approach:** Record the existing work as a plan and move it to Release 15's branches by merge, rather than rewrite or rebase it, so nothing already pushed is lost and its session can carry on.

**Challenge:** Not needed — this pack records existing work and moves its branch; it decides no new design. The work's own review happens at PE-2 and in the Release 15 qualification.

**Proof and limits:** See [completion](plan.md#completion); the outcome is read from commit titles until PE-1 checks it in the code.

**Review rounds:** Pending — Next: the owner confirms, after PE-1.

**Run start:** Pending — a session is already pushing this work (last pushes on 21 November by Codex and AstridPseudon), but no run is recorded. Next: that session records itself in the `Owner` line.

## Owner decisions

- **D1 Release.** Decided, 21 November 2026: Release 15, with its branch `release/15/plan-69` (the owner's choice in the Release 15 setup session).
- **D2 Scope.** Open: confirm or correct the [outcome](plan.md#outcome-and-scope).

## Source identities

Before 21 November the work was on `release/14/plan-69`, based on `release/14/main` (not on Plan 59): App `e0c6f7cdb` (10 commits), Agent `83d5f8fe3` (21 commits), Runtime `b2ea261` (5 commits), heads on 21 November.

`release/15/plan-69` in each repository is `release/15/main` after the 21 November forward of `release/14/main` ([astrid-dev#1224](https://github.com/banodoco/astrid-dev/issues/1224)), with `release/14/plan-69` merged in:

| Repository | `release/15/plan-69` head | Pins |
| --- | --- | --- |
| astrid-app | `5866b23bb` | Agent `58c749cab`, Runtime `1046f4074` |
| astrid-agent | `58c749cab` | Runtime `1046f4074` |
| astrid-runtime | `1046f4074` | — |

What the merge changed, and what PE-1 should check first:

- **Runtime:** Plan 59's verify-once CAS design (already on `release/15/main`) is kept; this plan's duplicate (`b2ea261`) and its API tests are dropped, and `test_descriptor_reader_does_not_inherit_live_cas_proofs` is a strict xfail for [astrid-dev#1222](https://github.com/banodoco/astrid-dev/issues/1222).
- **App:** the preview keeps both Release 15's `getCurrentFrame` and this plan's removal of the element-readiness gate.
- **Agent:** three esbuild-discovery tests in `tests/core/test_project_packs.py` fail on `release/14/plan-69` itself (`KeyError: 'ASTRID_REMOTION_PROJECT_DIR'`), and element admission needs the renderer's pinned Node v20.19.4 (`ASTRID_NODE_EXECUTABLE`).
- Every focused test failing on these heads also fails on `release/15/main` or on `release/14/plan-69`; none is new. Destination for every task: the same repository's `release/15/plan-69`.

## References

- [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md), which builds on this plan's branch.
