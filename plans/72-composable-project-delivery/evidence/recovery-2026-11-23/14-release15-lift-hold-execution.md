# Plan 72 — Release 15 HOLD-to-integration execution packet

**Prepared 23 November 2026 on isolated draft [#1624](https://github.com/banodoco/astrid-dev/pull/1624).** **Release 15 HOLD remains in force.** This packet is a handoff to the already recorded Release 15 Lead, **not** an acceptance decision, release-branch cut, merge instruction, reviewer dispatch, protection waiver or publication permission.

The Lead recorded in canonical `releases/15.md` is `session_011EzfW1gtAhRQwk8pgJMzhG` (accepted via [#1245](https://github.com/banodoco/astrid-dev/pull/1245)). No newer Lead reply to the [specific owner-routing request](https://github.com/banodoco/astrid-dev/pull/1245#issuecomment-7106544471) was present on the thread at this check. The [live Release 15 run board](https://github.com/banodoco/astrid-dev/blob/main/releases/15/run.md) explicitly lists **Plan 72 HOLD until the owner decides its scope**. The plan branch `release/15/plan-72` does not exist.

## 1. Release gate — decisions and receipts required before any real write

| Gate and accountable decision-maker | Specific required evidence | Present disposition |
| --- | --- | --- |
| **G1 — Owner: accept bounded Plan72 scope and independent challenge** | Actual dated owner decision resolving `Scope decision: Pending` and `Challenge: Pending` in canonical [Plan72 inputs](https://github.com/banodoco/astrid-dev/blob/main/plans/72-composable-project-delivery/inputs.md), with the supplementary #1161 critique and exact accepted exclusions | **HOLD**. Release placement was selected, but source/architecture scope was not formally accepted. Isolated preparation is separately authorized |
| **G2 — Existing Release15 Lead: accept custody/start** | ACK Plan72 GO/HOLD and one exclusive release-integration writer; exact then-current `release/15/main` SHA and branch-cut source; actual `release/15/plan-72` cut authorization, without assuming the older manager has retired | **HOLD**. Lead exists but no Plan72-specific ACK; Plan72 plan branch absent |
| **G3 — Owner/admin: protect release branches** | Actual enforced ruleset IDs/URLs and readback: no delete/force-push, required status checks, up-to-date landing reference and allowed landing method for `release/15/main`; check each affected repository, not only default `main` | **HOLD**. Live `protected:false` on Astrid-dev, Agent, Runtime, App and VibeComfy release/15/main. Active repository ruleset only Astrid-dev #27040267 targeting `main`. No protection changes are authorized here |
| **G4 — Release/Plan48 generic parser owner + Release15 Lead** | Name parser and branch-table writer; jointly qualify [09 generic parser patch](09-release15-branch-parser-compat.patch) and an exact release-owned `releases/15.md` migration containing all included-plan rows and correct repository release rows; retain original negative tests | **BLOCKED**. Frozen release source lists Plans 39/50/40 but has **zero** plan rows. The stricter parser must **not** land independently of its brief migration |
| **G5 — Plan72 authored-record owner + Release Lead** | Select the canonical Plan72 `plan.md`, `inputs.md`, `tasks.md` by verified blobs after owner decisions; record the actual Plan72 Included-plan and branch rows without manufacturing a cut or goal-gap link | **Prepared only**. Plan72 is a `Foundational enabler`, no `addresses` edge; frozen release tree lacks its pack and membership |
| **G6 — Independent review stop on actually accepted integrated head** | Named source-capable high-judgment reviewer/effort/session, scope, exact head and a recorded **formal RS1** verdict; historical private review counters verified, no silent reset | **Not dispatched**. Existing one prospective RS1 stop and final R remain future gates |

**The Lead cannot infer G1–G6 from an off-release green CI run.** In particular, a `not yet cut` Branches row does not create a Git branch, a proposed scope PR does not accept scope, and a draft source PR cannot be treated as an authorized release landing.

### Most recent reference identities, for **preflight only**

- Frozen Astrid-dev `release/15/main`: `321523e52bddbbd13477634b05974a16b54b825b`; branch `protected:false`; its `releases/15.md` blob `75ab70c56014b18b94ec887cd29ec64a126c39d4`. Re-pin everything after Lead GO.
- Source chain donor [#1212](https://github.com/banodoco/astrid-dev/pull/1212): `f13a584a31cb1d29b335533563420e1de35e3481`; untouched.
- Current recovered implementation `scripts/project_delivery.py`: blob `7f5a9659540984c05137d2f39e8e4e4a2ad25b5a`. Its three earlier source-boundary repairs remain unchanged.
- Verified additional 12-test disposable checkout harness `scripts/test_project_delivery_release15_scratch.py`: blob `c5d1cbe9c8bc3c27b02333a6c41e9b4e93b000dc` on test head `49e3edcbed20f593373903ea266738a84b64c540`. This is **not** the eventual release-branch head.
- Canonical Plan72 record blobs: `plan.md` `9066011c5547ce6ec62944f85a5847f2858409ac`; `inputs.md` `5caae0ebc3dec1748251677b18c2ec1b38663d59`; `tasks.md` `0ecdcca32053cd124f2bf07293e264e1a73ed6b1`. Verify these remain the approved files before applying.

## 2. Already executed — evidence to reuse, not repeat blindly

| Check on isolated native scratch/source | Exact completed evidence | What it establishes |
| --- | --- | --- |
| Preserve Plan72 fixes and canonical 01–05, 08, 09 selection | [11 native disposable result](11-disposable-release15-result.md), [CI 45225037635](https://github.com/banodoco/astrid-dev/actions/runs/45225037635) | Real `git worktree --detach`, sequential `git apply --check`/apply, three canonical authored records and verbatim release branch rows, then cleanup. No release ref write |
| Original authored traversal, missing Plan72 negative, feed stability | [12 traversal and feed receipt](12-native-real-traversal-and-feed.md), [CI 45233580645](https://github.com/banodoco/astrid-dev/actions/runs/45233580645) | The **unchanged original real-tree test passes** on the selected frozen checkout, and fails source-labeled when canonical Plan72 `plan.md` is temporarily absent and then restored |
| Paired code-revision public feed | [13 paired-feed receipt](13-paired-code-public-feed-parity.md), [CI 45243989495](https://github.com/banodoco/astrid-dev/actions/runs/45243989495) | Frozen readers versus selected readers, with **416 identical authored Markdown files**, schema v1 and fixed revision; byte-identical **150,702-byte** feed, SHA-256 `38b04ed594662eaafdf54f95e599f0a6136f31d3729f2b59b4eaf929bdcef658`. This is **not** a universal feed golden or a served-release comparison |
| CLI, AA-001 absence and real Plan72 Release15 membership | [CI 45256075100](https://github.com/banodoco/astrid-dev/actions/runs/45256075100) at `49e3edcbed20f593373903ea266738a84b64c540` | **530/530 Python + 13/13 App passed**, real native `project_delivery.py` CLI and expected failure with missing authored AA-001. Plan72 is an enabler included by the actual Release15 Included-plan line; the same branch row **without that line** does not grant membership |

**Critical interpretation of real traversal:** The artistic-ambition goal's three actual frozen paths run via `gap:F-003`, Projects `20`, `32`, `34`, to `release:13`, with the observed primary/supporting roles. `gap:AA-001` is an existing authored record and is required by the original test, **not** the gap in those three particular paths. Plan72 is a distinct **gapless enabler** and must not be given a fabricated `addresses` edge merely to make it appear in a goal-to-release traversal. Its real inclusion in `release:15` is proved by `release:15 -> project:72` from `releases/15.md`, not by branch metadata.

**Limits:** Native scratch results exercise the selected **frozen baseline** plus exact selected authored records. No tests have run on a Lead-accepted actual Release15 Plan72 branch (it does not exist). Any changed base, plan authoring, branch table, Plan53 goal parser, or shared check invalidates the corresponding subset of these receipts; requalify them on the real integrated head.

## 3. Future authorized handoff sequence — not commands to execute now

**Step A — Lead/owner gates.** Before touching a release ref, complete G1–G5, identify one writer for each shared source, verify actual `release/15/main` and all relevant protection rules; confirm the exact scope, revision, branch cut and integration order. Record those decisions in the canonical Plan72 inputs, Release15 run board and brief, as appropriate. Do not overwrite or retarget older #1161/#1199/#1201/#1212 branches.

**Step B — release-owned shared compatibility.** Under the Release/Plan48 owner, re-pin frozen `records.py`/`test_check_docs.py` and use the preflighted [09 parser compatibility patch](09-release15-branch-parser-compat.patch) **together with** the Lead's complete `## Included plans` and `## Branches` migration. The pinned frozen brief has only 39/50/40 and no plan rows; the scratch proof includes 5 verbatim source rows, **but that is not a substitute for later live Release15 branch records**. Never wholesale replace the evolving current release brief with the newest default-main file.

**Step C — source selection and authored Plan72 pack.** On the one authorized plan branch cut from the then-live release main, select the exact **01 typed core (#1074), 02 reader (#1076), 03 RED tests (#1199), 04 guards (#1201), 05 source ownership (#1212)** donor diffs, then the stored [08 source-boundary patch](08-source-boundaries.patch) and owner-approved 09 parser patch. Verify each donor path, base blob and `git apply --check` before `git apply`. Preserve Plan53's separate [#1059](https://github.com/banodoco/astrid-dev/pull/1059) ownership; do not import #1161's composed merge ancestry or all of newer default `main`. Import the approved three authored Plan72 records and the actual approved release-membership rows. [README](README.md) and [10 authored-record inventory](10-release15-authored-records.md) contain the exact path and fixture recipe. The PD10 `docs/extending.md` hunk is context-incompatible with frozen Release15 and is **deferred until after RS1**.

**Step D — native combined-source qualification and original oracles.** From the actual integrated plan worktree, not the off-release draft:

```sh
git rev-parse HEAD
git status --porcelain
git diff --check
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/astrid_dev.py check
python3 scripts/astrid_dev.py list
python3 scripts/project_delivery.py check --root .
python3 scripts/project_delivery.py goal pillar:artistic-ambition/finished-artistic-work --root .
python3 scripts/release_branches.py check 15
```

The release-branches check may require credentials or a fetched clone; if unavailable, mark **UNVERIFIED**, never PASS. Keep **all original tests and fixtures unchanged**, notably `test_project_delivery.py::test_actual_repository_delivery_traversal`, records/branch-table negative tests, `test_golden.py`, `test_views.py`, and the new CLI/AA-001/Plan72-membership controls. Run native hosted Documentation integrity and actual App `vision-consumer-contract` on **the exact combined release head**. Validate generated-view staleness and output schema. Compute *paired fixed-revision public-feed parity with identical actual authored inputs*; the 150,702-byte rehearsal digest is specific to its inputs, not a release acceptance criterion.

**Step E — independent design and remaining project tasks.** Only after accepted G1–G6 and the independent **formal RS1 stop** on the rightful source head (or separately recorded owner exception) should PD6/PD7/PD8/PD10 downstream changes begin. Plan72 is not complete merely because the initial readers, query and scratch parity work: the check-registry integrity rule, accepted source-refactor choices, document extension, actual release-head proof, PD11 and final independent **R** remain gated. The Release Lead, not this scratch packet, determines whether/when the plan branch lands. Publication still needs the owner's separate exact-commit approval.

## 4. Minimal Lead response that would unblock the next phase

Record **one** response on the existing [#1245 Plan72 handoff](https://github.com/banodoco/astrid-dev/pull/1245#issuecomment-7106544471) or the canonical Release15 run board with:

- **Scope:** owner-approved Plan72 bounded contract and accepted critique link, or explicit HOLD with decision owner.
- **Custody:** Plan72 GO/HOLD, sole accountable release-plan writer, current protected `release/15/main` SHA and permitted exact cut ref.
- **Parser/authoring:** named Release/Plan48 `records.py`/test owner, named release-brief + Plan72 authored-pack owner; exact 09 disposition, all-included-plan migration order and Plan53 boundaries.
- **Protection:** enforced ruleset ID/readback for each affected `release/15/main` branch, required contexts/up-to-date and no-force/no-delete verification.
- **Review:** accepted RS1 stage, independently source-capable reviewer binding and preserved historical review-budget receipt, without treating any prior supplementary critique as formal RS1.

**Until this response and actual receipts exist: continue isolated evidence only; Release15 HOLD, no merge/cut/protection change/RS1.**
