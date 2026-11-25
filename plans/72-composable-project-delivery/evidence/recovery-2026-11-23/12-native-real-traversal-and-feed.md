# Plan 72 — original real traversal and fixed-revision feed rehearsal

**Status: executed on isolated draft #1624 only, 23 November 2026. Release 15 HOLD preserved.** This is a continuation of the [disposable parser/authored-record result](11-disposable-release15-result.md), not a Release 15 plan branch or a claim of Lead GO, formal RS1, final R, branch protection, integration or publication.

## What ran

An unchanged copy of the *original* `test_project_delivery.DeliveryCompositionTests.test_actual_repository_delivery_traversal` from the pinned Plan72 source is invoked using `python3 -m unittest` from the **detached temporary checkout** of frozen Astrid-dev `release/15/main=321523e52bddbbd13477634b05974a16b54b825b`. The test process uses `PYTHONPATH=<scratch>/scripts`, so it imports the native patched frozen checkout, not #1624's own package. The parent test asserts the real original test's successful exit, **without editing that original test or its golden fixtures**.

Before invoking it, the scratch setup uses native `git apply --check` and `git apply` for source selection **01–05**, the stored [08 recovery patch](08-source-boundaries.patch), and the proposed owner-gated [09 generic parser patch](09-release15-branch-parser-compat.patch). It copies three pinned canonical Plan72 authored files and five canonical branch rows into the *temporary* release brief, verifying their Git blob hashes. Plan72 remains a gapless **Foundational enabler**. Every test cleans up the disposable worktree; **no release or other GitHub branch/ref is written**.

## Actual exact-head evidence

| Checkpoint | Source head | Hosted evidence | Outcome |
| --- | --- | --- | --- |
| Original real-tree traversal | `3f14f7076b9da68915c7a800d06bf047b76673c1` | [Run 45232107837](https://github.com/banodoco/astrid-dev/actions/runs/45232107837) | **524/524 Python passed** including the original real test executed inside the disposable frozen checkout; repository/view checks and actual App consumer **13/13** passed |
| Authored-record negative control | `42799419b0df50202561c1500aaa3f4a53abf38a` | [Run 45232564315](https://github.com/banodoco/astrid-dev/actions/runs/45232564315) | **525/525 Python**, repository/view checks and App consumer **13/13** passed. Test temporarily removes the exact canonical `plans/72-composable-project-delivery/plan.md` in scratch, re-runs the unchanged original traversal, requires a nonzero exit with `Plan 72 names unknown folder`, restores the original bytes in `finally`, and verifies the canonical Git blob SHA again |
| Same-input fixed-revision public feed non-mutation | `5ac0fd4e5048880bbd4ef53df1d041c051640dcd` | [Run 45233070565](https://github.com/banodoco/astrid-dev/actions/runs/45233070565) | **526/526 Python**, repository/view checks and App consumer **13/13** passed. The scratch test verifies frozen exporter `scripts/export_public_vision.py` blob `672eb3a0eb6889df7dec3486eb55734d18eef282`, serializes the schema-v1 feed at fixed revision `0000000000000000000000000000000000000000`, executes the real goal-to-release traversal, builds and serializes the feed again, and asserts **byte-for-byte equality** and `schemaVersion == 1` |

**Interpretation of the original test:** It requires that `gap:AA-001`, `project:72` and `goal:pillar:artistic-ambition/finished-artistic-work` exist, and that an authentic goal-to-release path is available. It does **not** require the path to pass through enabler Plan72 or invent a Plan72 `addresses` edge. The positive result plus the missing-Plan72 negative control confirms that **actual authored Plan72 records** are required: branch-row declarations alone cannot satisfy the original loader.

**Feed parity limit:** The third test proves **same authored inputs + same source revision + same exporter → identical feed before/after the read-only delivery graph query**. It does not compare different historical Git revisions, does not establish the previously cited 161,224-byte source-pair parity, and does not replace the later paired fixed-revision feed comparison on the actual authorized Release15 integrated head. The new test does not write or publish a public feed.

## What remains genuinely blocked

- [#1245 Lead handoff](https://github.com/banodoco/astrid-dev/pull/1245#issuecomment-7106544471): latest observed GitHub comment is still `7106544471`, from the requesting manager; **no Lead ACK, named parser/record owners or Plan72 GO** recorded. Canonical Lead remains `session_011EzfW1gtAhRQwk8pgJMzhG`.
- The [Release 15 run board on main](https://github.com/banodoco/astrid-dev/blob/main/releases/15/run.md) still lists **Plan72 HOLD**, pending owner's bounded scope decision; `release/15/plan-72` is absent.
- Release-main protection, canonical full 16-plan brief authoring under the Lead, assigned owner of generic `records.py`/branch tests, Plan53 Goals ownership, and eventual authorized integration/RS1/final R are not satisfied by this rehearsal. The supplemental parser patch remains in [09-release15-branch-parser-compat.patch](09-release15-branch-parser-compat.patch), **not merged to shared parser**.
- The current #1624 code/test candidate and its three earlier independently tested source-boundary repairs remain off-release. **No original tests or negative controls were loosened. No branch protections were changed. No merge or publication performed.**

The proof is a **detached, disposable native worktree**, never a Lead-owned `release/15/plan-72` branch or a substitute for the real protected release combination.
