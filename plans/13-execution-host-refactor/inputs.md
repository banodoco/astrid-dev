# Inputs: execution host refactor

[Plan](plan.md) · [Tasks](tasks.md)

**Run start:** Accepted — 17 November 2026, by the owner's own message in the Release 14 Lead's session (`session_011EzfW3Zy19ncNecpQnKb7D`): every Release 14 plan except Plan 59 runs by [fresh-packet dispatch](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md). **Accountable agent:** the Release 14 Lead, that session. What it, the Orchestrator and each packet session may do, and what needs the owner, is on the [run board](../../releases/14/run.md#authority); this run covers HM1 to HM3 only; the extraction is Release 15's.

## Extraction evidence, 22 November 2026

The owner asked on 22 November 2026, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), for "a rough outline of how we should tackle the [generic host] decomposition in an elegant manner that will bias away from further growth", with Codex Luna workers to validate it. Four ran, read-only, on astrid-agent `048ab307` (`release/15/main` plus nine small unrelated fixes); their reports are in [evidence/](evidence/).

- **The map is current** ([host-check-L1.txt](evidence/host-check-L1.txt), measured from the syntax tree): 188 top-level definitions as mapped; three new methods on the class, all in its shutdown slice. Lines by responsibility: R11, the class and its coordination, 8,738; R12 2,168; R09 1,291; R14 969; R02 953; R08 771; R06 735; R10 675; R05 491; R13 422; R04 400; R03 225; R07 144; R01 35. The three stateless groups (R03, R05, R08) use neither `self` nor the filesystem adapter and read only constants. [current-inventory-20261122.csv](evidence/current-inventory-20261122.csv) lists every definition.
- **How it grew** ([host-check-L2.txt](evidence/host-check-L2.txt)): 397 lines on 30 August, 13,519 by 15 October, 18,888 on 21 November. Of the 12 largest additions, roughly 30% were new methods on the class, 25% new helpers, 20% growth inside `run_task` and `_run_task_impl`, 15% constants and schemas, and 10% code that had a sibling module to go to. Plan 55's branch adds 233 net lines to the file; Plans 69 and 77 add none.
- **Callers can keep working** ([host-check-L3.txt](evidence/host-check-L3.txt)): 13 product files and 140 test files import or use the module; product code uses 30 names, 24 of them private. 47 test patches in 9 files target names on this module; a patched definition that moves stops being patched, which is the rule on every card. `source_identity.py:39`, `scripts/ci_windows_journey.py:468` and the structure baselines name the file.
- **Why the existing guard did not hold** ([host-check-L4.txt](evidence/host-check-L4.txt)): `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale` checks that a hand-edited count is within 50 lines of the real one. The count has been edited upward five times. The test fails today for this file and 17 others.

**Challenge:** Reviewed — commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) on 22 November 2026 and done by an independent Codex critic (`gpt-6.2-astra`, high effort, read-only, no stake in the draft) against astrid-agent `048ab307` and the HM2 branch. It ran no tests. Its report is [critique-extraction.txt](evidence/critique-extraction.txt). The owner asked that such critiques be weighed, not adopted wholesale; what the planner did with each finding:

- **Accepted — the "stateless" groups have exceptions.** `CapabilityRecord.manifest()` reaches into source custody and `_AttemptLifetime` changes its own state (`generic_host.py` near 3087 and 5304). The helper check had looked at functions, not classes. The first extraction is narrowed to the genuine leaves and routed `X`.
- **Accepted — the Runtime adapter is not self-contained.** It uses digest, claim and terminal helpers and two readers that belong with the handoff code, and at least 18 tests replace it through imported module names, not the three counted. What it stands on now moves first (EX-4, now in [Plan 83](../83-execution-host-in-modules/tasks.md)), and both cards are `S`.
- **Accepted — source custody and worker bindings do not move as one.** Custody needs one accessor for a binding that is installed at run time; worker bindings and adapters import concrete packs under an exemption that covers this file alone, so those parts stay in the host.
- **Accepted — an identical body is not proof.** A patched name, a replaced `os`, rebound module state, class identity and the `-m` launch are each now a rule on every card. The check of callers had missed that production launches this file with `-m`.
- **Accepted — do not rename `os` first.** Windows tests replace `generic_host.os`; the rename is not a free prerequisite and is dropped from the path. [#1294](https://github.com/banodoco/astrid-dev/issues/1294) stays open for when those tests move.
- **Accepted — the guard.** Three fixed ceilings let deletions pay for a longer method and can be raised in the same change. EX-0 is now one check against the merge base, across the execution package, that also stops an oversized function growing.
- **Accepted — bring the safety net across first.** Eight of the nine characterisation files are still on the Release 14 plan branch. Now EX-1.
- **Accepted — the estimate.** Eleven days for the first phase was optimistic and thirty is an allowance. The plan now commits to EX-0 to EX-3 and re-estimates on the first measured extraction.
- **Kept as drafted, and the critic agreed:** owners as objects, not mixins, and the attempt last. Its named risk, handing an unsettled attempt to the reconciliation thread, is written into EX-9, now in [Plan 83](../83-execution-host-in-modules/tasks.md), with the test that catches it.

## Owner decisions

- **D1 — how much in Release 15.** **Decided 22 November 2026: the guard, the safety net and the first measured extraction (EX-0 to EX-3), about 5 to 6 days, then a re-estimate she decides on.** How it was reached, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG): she first wrote "Let's include them and the first part of the speed stuff on this release", quoting the Lead's earlier line "The first six steps are about 11 days and take roughly 6,000 lines out". The Lead recorded that as the larger scope, then told her the quoted figure predated the critique (now eight rows, about 16 days, about 4,500 to 5,500 lines) and that its recommendation after the critique was the smaller scope. She replied "I agree with you". The Lead reads that as agreement with the recommendation. If she meant the larger scope, [Plan 83](../83-execution-host-in-modules/tasks.md) is cut to EX-4 to EX-7 and joins Release 15 whole on her word; nothing here changes.
- **D2 — who may let the file grow.** **Decided 22 November 2026: only the owner,** in a pull request that changes nothing else. With a check against the merge base there is no number to raise, so an exception is a visible change to the check itself. Same exchange as D1.
- **D3 — local preparation and the command-line lifecycle (EX-8, now in [Plan 83](../83-execution-host-in-modules/tasks.md)).** **Decided 22 November 2026: not in Release 15.** It is custody-sensitive and the map ties it to [Plan 38](../38-one-process-identity/plan.md), which is in Release 16.

- **D4 — one plan, one release.** On 22 November 2026, in the same session, she wrote: "I think plans should typically go all into one release". The Lead agreed and moved EX-4 to EX-9 and RS2 to [Plan 83](../83-execution-host-in-modules/tasks.md) the same day, leaving this plan wholly in Release 15. Nothing in any card changed.
- **D5 — the review.** **Decided 22 November 2026: one round at the end, by an independent reviewer on Codex Astra; landing waits for its findings.** The row had allowed two rounds, from when this plan held the whole extraction. In the same session she replied "That's perfect" to that wording.

## Starting code

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| `banodoco/astrid-agent` | TBD at start; historical observations below are not a current base | TBD at start; inspect applicable execution changes, including sandbox process control from PR #109 | TBD; no verified predecessor output recorded | TBD at start | `pre-main`, verify its existence and preserve existing publication policy |

## References and evidence

| Source | What it establishes | Identity or link | Limits / missing information |
|---|---|---|---|
| `astrid/core/execution/generic_host.py` on `pre-main` | Historical observed size: **17,067 lines** | Inspected 2026-11-05; [source](https://github.com/banodoco/astrid-agent/blob/pre-main/astrid/core/execution/generic_host.py); blob `b0ea83326115ec172a79260d657be7dd01c3c4a1` | Historical observation only; recheck the selected starting commit. |
| `astrid/core/execution/generic_host.py` on `main` | Historical observed size: **14,453 lines** | Inspected 2026-11-05; [source](https://github.com/banodoco/astrid-agent/blob/main/astrid/core/execution/generic_host.py); blob `da61b21aed220a4c35c27d62baca19eeef1b09c4` | Different historical snapshot, not the proposed execution base. |
| Agent PR #109 | Changes `generic_host.py` for sandbox process control; its work may need preservation | [PR #109](https://github.com/banodoco/astrid-agent/pull/109) | Not itself the decomposition project. Determine applicability against the selected base; do not assume PR state or merge status. |
| Inspected `main` snapshot | Handwritten orchestration includes Runtime protocol access, capability discovery, task execution and settlement, local preparation, persistent supervision, and process handoff. Generated protocol client is separate in `astrid_runtime_client/generated.py`. | Historical code inspection, 2026-11-05 | Candidate boundaries only; coupling must be checked on the actual base. |
| [Multiple inference routes](../12-multiple-inference-routes/plan.md) | Owns the shared inference lifecycle. | Project plan | Context, not a scheduling gate. |
| [Streamlined agent experience](../16-streamlined-agent-experience/plan.md) | Owns the single agent extension path. | Project plan | Context, not a scheduling gate. |

The historical counts and blob SHAs are evidence about inspected snapshots, not live source identity or authorization. The roughly 18,000-line recollection is only a clue for locating the file.

## Constraints

At setup, confirm repositories, actual base branches and SHAs, work to preserve, verified predecessor inputs, a fresh candidate branch, and the intended `pre-main` destination. The original draft specifies no review rounds or limits; retain the run configuration and existing authority at setup without adding review stages. Derive task boundaries and exact focused selectors from that source. Preserve existing execution behavior; characterize before extraction and rerun the same checks, including any touched lifecycle, cancellation, process ownership, and result-handling behavior. Do not conflate moving code with semantic fixes. Follow the [shared run contract](../../skills/shared/run-contract.md) for routes, source identity, proof, and publication limits. This draft does not authorize implementation or broad test discovery.
