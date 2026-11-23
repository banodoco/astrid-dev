# Plan 71 — isolated recovery exact-head and conflict audit (23 November 2026)

**State:** ISOLATED CANDIDATE; NOT ACCEPTED FOR INTEGRATION. The owner explicitly directed a **new branch based on the exact #1444 head**, with former manager retirement still UNKNOWN and all original branches/PRs left unchanged. This is not an owner GD-9 decision, reviewer PASS, branch merge, or product closure.

## Custody and branch identities

| Identity | Exact observation / invariant |
|---|---|
| Recovery ancestor | `753e32a2ab19e7ae7092310e2d58def293d27d1a`, former [draft #1444](https://github.com/banodoco/astrid-dev/pull/1444) |
| New writer-only branch | `p71/recovery-gd9-prep-20261123-1` created directly from that immutable SHA |
| Project-branch target | `project/71-gap-definition-reconciliation` at `ca97096ba6893108c90a932479e7473f679c724e` when recovered |
| Original preservation branch | `p71/rs2-c1-c2-rework-20261122-1` remains at `753e32a2ab19e7ae7092310e2d58def293d27d1a`; DO NOT UPDATE |
| Original #1444 | OPEN DRAFT / UNMERGED at the recovery snapshot; DO NOT READY, CLOSE, RETARGET, OR MERGE |
| Original synthetic merge | `0624ae2af740fbf51d774f25815c616cda3f3351`, tree `a5b4e9fce5fe78022dc22e13b2f740e141a3e56d`; **old head only** |
| New recovery scope | Five inherited proposal-evidence files **plus new Plan 71 evidence-only documents**. No canonical gap, plan task status, issue, Goal, release or App edits |
| Old manager status | Stop/retire request sent; receipt inaccessible. Cannot infer retired or exclusive global custody. New branch is isolated and must not race old refs |

No rebases, amends, force-pushes, ancient branch edits, old PR updates, or direct project/main writes. The new draft PR duplicates the inherited five-file difference of #1444 by design. **Never merge both PRs**: they represent one proposal lineage. A later authorized integrated route must select one candidate and explicitly handle this overlap without silently rewriting either.

## Source and evidence continuity

The predecessor's 22 November independent manager [qualification checkpoint](https://github.com/banodoco/astrid-dev/pull/1444#issuecomment-7085503351) establishes **proposal-only** C1/C2 merits. It is not a new RS2 pass. The original independent RS2 returned **REWORK**, its one round is **1/1 consumed**; HOLD is **1/1 consumed**; historical counters **UNKNOWN**. No repeat, reviewer substitution, original case-index read or withheld report publication is allowed. Previous worker `/root/p71_rework_worker` was owner-reported stopped; its private package was unavailable and its successful native checks were **worker-reported**, not replayed here.

- Frozen A at `ca97096b...`: 69 plans, 60 linked, 83 positive links, 20 affirmatively served gaps, two authored routes.
- Fixed GD-6 B at `6d75abf...`: 77/68 plans, 95 literal indexed mentions / 92 positive, three routes, 232 unique open/closed issues at 2026-11-22T00:59:59Z cutoff.
- Later C at `70d5ac8...`: 80/71 plans, 99 literal mentions / 96 positive. All C changes are later than A and cannot be retroactively credited to the consumed RS2.
- [C2](gd8-criterion-route-decisions-2026-11-22.md) includes 69 unique rows: **68 closure criteria and one F-008-C09 adjacent non-criterion**, with 47 `PLAN_SCOPE`, 15 `SPECIFIC_EVIDENCE_MISSING`, 7 `UNPLANNED` (47/15/6 if only closure criteria). All actual outcomes and accountable proof-owner assignments remain **NO-RESULT**. Archived `Owner:` fields are *not* delegated proof ownership.
- CA-002-C02 is prospectively P28-scoped but not an issued legal right; F-004-C03 lacks a full untrusted-pack refusal scope despite P47 conflict/recovery proposals; CA-005 one-folder and ten-contributor tests are distinct. No false P52/P53 backlinks.
- **Older native precommit guard exit 1:** `native/prepare_and_validate.py --validate` expected uncommitted modifications; its subsequent execution after those changes were committed failed its staging precondition. This is **neither a PASS nor independently demonstrated regression**. Do not weaken it or suppress the reported failure.

## Live integration delta — read-only

At the 23 November recovery read, `astrid-dev/main` was `57dd1ab951d70ed831895804a21590250f445216`. Relative to frozen project A, main and the project have **diverged histories**; their plan 71 `plan.md`, `inputs.md`, `tasks.md` contents differ, and the project-only evidence directory is not yet on main. Do not promote this branch to main as a shortcut. Reconcile with live main only **after** a genuine GD-9 source/owner decision and project integration approval.

Across the 22 `vision/gaps/*.md` files, the main and A filenames matched; **F-004 alone has a changed Git blob**. Frozen F-004 blob `ac3ad9b076bddeb1320c748f6f4c2fee4b56c191` has no route. Main F-004 blob `41e9160f8bfb7d3345899a676031cc4cc9ebcaa5` adds a specifically partial [Plan 78](https://github.com/banodoco/astrid-dev/blob/57dd1ab951d70ed831895804a21590250f445216/plans/78-live-custom-element-editing/plan.md) route and still leaves demanding pack lifecycle work unplanned. This is a **textual source observation**, not proof that P78 passed product closure.

Shared-surface coordination at read time:

| Integration source | Observed state | Consequence |
|---|---|---|
| [Dev Goals #1059](https://github.com/banodoco/astrid-dev/pull/1059) | Open draft | Plan 53 owns Goals metadata; no speculative Plan 71 source/schema edit |
| [App Goals #323](https://github.com/banodoco/astrid-app/pull/323) | Open draft | No assumed consumer compatibility for future migration |
| [Dev Plan 73 #1256](https://github.com/banodoco/astrid-dev/pull/1256) | Merged **to Plan 73 project branch** | Not evidence that the whole Markdown-first source cutover reached main; check the actual target before any shared skill edit |
| Plan 71 canonical progress on main | GD-7, GD-8, RS2, GD-9 and downstream rows unchecked | Do not mark completed based on proposal-only documents |

## Checks actually performed in isolated recovery

- **PASS, connector identity:** original #1444 source branch still equals immutable `753e32a2...`; project destination still equals `ca97096b...` at pre-branch check; three original hosted checks were green **on original head only**.
- **PASS, document structural recount:** parsed the [C2](gd8-criterion-route-decisions-2026-11-22.md) criterion table and appendix, finding 69 unique row IDs, 69 appendix rows, exact same row order, 22 gap prefixes, and distributions 47 / 15 / 7; F-008-C09 is the sole declared adjacent residual. This validates **structure**, not source-derived semantics or user outcome.
- **PASS, source inventory:** compared main and frozen gap-directory blobs and confirmed the unique F-004 source change and 22 surviving names at the observed main commit.
- **NO-RESULT, native checkout tests:** this recovery environment does not possess a full Git checkout; `git ls-remote https://github.com/banodoco/astrid-dev.git refs/heads/main` failed with `Could not resolve host: github.com`. Do not claim `python3 scripts/astrid_dev.py check`, `sync`, full unit tests or local `git diff --check` ran here.
- **Pending new-head proof:** Hosted PR documentation / vision-consumer-contract / review-intake on the **new recovery head** must be collected separately. Exact SHA and check links belong in the new PR conversation after runs finish. Old #1444 green does **not** qualify the new head.

## Open work, decision order and STOP flags

1. **Recover custody:** owner/supervisor obtains a retirement/cancellation receipt for old manager and any queued actions, or explicitly records unknown custody; protect original refs. This new branch may be inspected without requiring false global-exclusivity claims.
2. **Qualify this isolated draft:** independently audit inherited five files and the new decision envelope on their **exact final head**, verify per-file scope and changed tree, collect hosted checks; keep all `NO-RESULT` facts. If a check fails, record the actual failure and its baseline before modifying tests.
3. **Exhausted-RS2 disposition:** preserve original REWORK and its C1/C2 findings. The owner reported **conditional permission for bounded proposal-only project integration** after checks/base/tree/project rules; this does **not** certify RS2 PASS or override blockers. Any substantive unresolved row needs a named decision. No repeat reviewer/HOLD.
4. **GD-7/GD-8:** decide whether the 22-gap dispositions and C2 routes meet their *proposal* acceptance conditions; only update task progress after actual review. No route table is product completion.
5. **GD-9:** use [identity/owner decision envelope](gd9-identity-and-evidence-decision-envelope-2026-11-23.md) to request an explicit exact-head owner decision, mark missing proof/owners NO-RESULT and choose a future *current* application base. No preapproved migration.
6. **GD-10–GD-13:** only after GD-9 authorize source-owner-aligned canonical routes, affected project/issue references and original negative/consumer checks. Source drift, Plan 53/App, and Plan 73 must be rechecked at that future time.
7. **R, GD-14, final Astra High:** integrated final review and project completion are not ready. Separate GPT-6.2 Astra High sense-check remains **max two rounds**, not an RS2 substitute. No final project-to-main merge, recurring Phases 6–7, weekly workflow or bot.

**Integration posture:** The *new* PR should remain **DRAFT / NOT MERGE-READY**, target only `project/71-gap-definition-reconciliation`, keep the original PR #1444 untouched, and avoid automerge. An accepted owner instruction to prepare a candidate is **not** an instruction to promote it.
