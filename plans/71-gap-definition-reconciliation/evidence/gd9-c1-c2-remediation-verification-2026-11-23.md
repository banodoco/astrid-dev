# C1/C2 remediation implementation — source and local-helper test receipt

**23 November 2026, source-only delegated run.** The original independent RS2 **REWORK 1/1 consumed** and HOLD **1/1 consumed**, historical private counters **UNKNOWN**, no new independent reviewer or owner GD-9 approval. This records tests that **actually ran**; the entire native repository checkout and the latest committed Python module self-test have **NOT** been run in the unavailable networked local source environment.

## Committed source identities

| Exact artifact | Git blob (immutable source) | Role |
|---|---|---|
| [C1/C2 source resolution](gd9-c1-c2-source-resolution-2026-11-23.md) | `44bb55aebc2dbe545bc4751f31852a1f9b08a714` | Source declaration counts, two C2 errata and unresolved semantics |
| [Two-rule C2 correction JSON](gd9-c2-semantic-corrections-2026-11-23.json) | `24ddee801ba1113ca1d0a80bfe5db0f51bb5f4cd` | Original-vs-proposed labels, source line, classification and NO-RESULT guards |
| [Read-only native replay checker](gd9_source_replay.py) | `d1a74d6e062b8d597d25fa4addbd6a5412497502` | Reconstruct all A/B/C raw/positive units; fail closed on wrong-source/invented owner; keep C2 unchanged |
| [69-row original-source witness map](gd9-c2-exact-wording-witness-matrix-2026-11-23.md) | `c0dba59349e30b4e0be047b8ab133971643c1de4` | All 69 C2 row source locations, two flagged errata, F-008-C09 adjacent noncriterion |
| [Native disposable checkout instructions](gd9-native-disposable-validation-packet-2026-11-23.md) | `d3c0143c5bb7ee6a086ad8fc95b66ac10145d5ef` | Exact-head original tests, full source replay, generated-view diff only in disposable checkout |
| Historical C2 inherited source | `bba487a5357c5c405b266421af6d49e4c5a2f481` | Unchanged and still byte-identical to original #1444's C2 blob |

## Actual C1 source executions

A direct GitHub `fetch_file` census checked the complete `Vision gaps:`/ `Vision role:` declaration in **69/69 frozen A plans** and **77/77 frozen B plans**, with one linked ID count and one **per-plan deduplicated raw gap-ID count** from the declaration only. `Vision role` mentions do not count. The B→C GitHub diff contained all **seven** plan-file changes (P13/P55/P75/P77 modified with **zero** membership change, P81/P82/P83 added **four** new raw and affirmative links). Reconstructed counts:

| Exact source | A (`ca97096...`) | B (`6d75abf...`) | C (`70d5ac8...`) |
|---|---:|---:|---:|
| Numbered plans | **69** | **77** | **80** |
| Gap-linked plans | **60** | **68** | **71** |
| Explicit affirmative links | **83** | **92** | **96** |
| Raw unique IDs within `Vision gaps:` declarations | **85** | **95** | **99** |
| Nonaffirmative raw-only mentions | P37 AA-001/LS-002 (2) | P37 (2), P18 formerly F-001 (1) | Same three as B |

This **corrects A's historic raw-vs-affirmative column label** and source-reproduces B/C raw results without claiming the missing historical worker's `plans.json` artifact is recovered. P72 `Vision role` context is excluded, not a reason to add two positive links. The same logic and A/B/C expected tuple `85/95/99` is **committed in the native checker**; the source-reconstruction results above were run through connector-backed JavaScript, not represented as a native checkout run.

## Actual C2 correction and negative-source executions

Read original C2, frozen CA-005 line 23, frozen CI-003 line 19 and frozen P42 line 23. The two-rule JSON was verified against exact source SHA/line, original exact C2 first-cell wording, original C2 categories (`CA-005-C03 UNPLANNED`, `CI-003-C03 PLAN_SCOPE`), and the no-owner/no-outcome approval guards. Applying the rules **only in memory** produced the two proposed label replacements; confirmed **69/69 original C2 IDs and order unchanged**, **47/15/7** class counts unchanged, **69/69 literal witness locations** preserved, and **68** genuine S5 tasks unchanged. **Neither label was edited in inherited C2 or any canonical source.**

**Ten deliberately invalid JSON/source variants were rejected** by the same source-enforced validation: wrong frozen pin; fabricated accountable proof owner; false outcome `PASS`; invented CA-005 quote; wrong CI-003 source line; fabricated P42 deduplication span; wrong CA-005 C2 class; duplicate rule ID; corrupt original C2 blob SHA; and a nonexisting original row label. These are source/data validation tests, **not real creative outcomes or formal independent source semantics**.

**Executed local Python helper checks:** an isolated Python file reproducing the new `raw_declaration_ids` and `corrected_c2_in_memory` function bodies was bytecode-compiled and executed locally: **three raw-declaration positives, two raw-declaration negatives, one semantic-correction positive, seven rejected correction negatives**. These are local *helper* unit tests, **not** the current entire committed `gd9_source_replay.py --self-test` blob and not the `--head` full repository source scan. The latest exact file's native complete test and original suite remain **NO-RESULT**. See the [disposable-checkout commands](gd9-native-disposable-validation-packet-2026-11-23.md).

## Strict remaining decision gates

1. **Source-semantic equivalence:** the historic **65 direct/four bounded variants** assertion still lacks the four named IDs. A distinct non-author technical assessor must review all 69 full source passages/plan claims, label direct/split/variant/unsupported and name the four or withdraw the count. **Independent 65/4 qualification NO-RESULT.**
2. **Original raw manifest provenance:** `plans.json` exact former indexing implementation is unavailable, although its **95/99 results** are reproduced under a transparent source scanning rule. **Byte-equivalent historic manifest re-execution NO-RESULT**, not a blocker to communicating reconstructed counts.
3. **GD-9 and task/owner authority:** original formal independent RS2 remains **REWORK 1/1 consumed**; original HOLD remains **1/1 consumed**, and GD-9 owner decision is **NO-RESULT**. All 68 actual positive/adverse product outcomes, accepted accountable proof producers and independent verifiers **NO-RESULT**. Historic plan `Owner:` values are not appointments.
4. **Native/integration:** full exact-head `python3 gd9_source_replay.py --self-test` and `--head`, original repo `check/sync`, full test suite, paired App source/consumer exercises and final independent R **NO-RESULT** in this environment. Hosted documentation/intake/vision checks are distinct from native validation. No original test or branch protection weakened.

**No canonical gap edits, no migration, no issue/Goal/App/status changes, no merge of #1444 or #1625, no reuse of HOLD/RS2 and no deferred Phase 6–7 activation.** This is a bounded implementation and empirical source-only verification on an isolated draft branch, not a completion or sign-off receipt.
