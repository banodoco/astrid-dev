# Release 15 Agent Tier 1 row 1 by-id comparison

Candidate head: `dc45d97c`; CI run `45658943056` (8 unit shards + darwin native); Lanes run `45658943220` (opt-in + integration shards 1–4 + installed wheel).

Counting: primary counts distinct test ids with status FAILED or ERROR. SUBFAILED rows are excluded; a parent is counted once only if it independently has FAILED/ERROR. CI `darwin:` is retained in IDs; stripping it leaves all stated union/difference counts unchanged. Continuity counts include SUBFAILED rows.

| Run | FAILED | ERROR | Primary union | SUBFAILED rows | Union with SUBFAILED rows |
|---|---:|---:|---:|---:|---:|
| CI dc45d97c | 762 | 328 | 1,090 | 33 | 1,123 |
| CI b934555c | 759 | 328 | 1,087 | 33 | 1,120 |
| CI R14 baseline | 765 | 328 | 1,093 | — | 1,093 |
| CI R15 baseline | 760 | 328 | 1,088 | — | 1,088 |
| Lanes dc45d97c | 391 | 435 | 826 | 0 | 826 |
| Lanes b934555c | 391 | 435 | 826 | 0 | 826 |
| Lanes R15 baseline | 391 | 435 | 826 | 0 | 826 |
| Lanes R14 baseline | 357 | 434 | 791 | 0 | 791 |

| Workflow | Comparison | Candidate ids absent from comparator | Comparator ids absent from candidate |
|---|---|---:|---:|
| CI | R14 list | 6 | 9 |
| CI | R15 list | 5 | — |
| CI | b934555c run | 4 | 1 |
| Lanes | R14 run | 37 | 2 |
| Lanes | R15 run | 2 | 2 |
| Lanes | b934555c run | 1 | 1 |

All 6 CI ids absent from R14 first appeared at edfc2dc9; none first appeared at dc45d97c. The 37 Lanes ids absent from R14 first appeared across earlier listed heads: 15 timeline-publication, 10 CLI-first-media, 1 CLI timeline-transfer, 8 native-batch-ingress, 1 opaque-item patch (edfc2dc9); command-count capture (b934555c); installed captured-command render (89768ef9). No ID absent from R14 first appeared at dc45d97c.

CI ids new vs R14 are all mapped: two readiness ids (#1920 / #1941 item 2 / #1928 RS1C.N15), three adapter ids (#1920 item 5 / #1938 item 9), and the core pack boundary ratchet (listed as new in the R15 baseline README). Lanes new-vs-R14 groups and known-issue labels are in [groups.tsv](groups.tsv); group totals 43 ids across both workflows. No unmapped id is new at dc45d97c.

First eight log lines, per-ID chronology, full ID lists, and per-job counts: per-ID labels and groups are in [issue-labels.tsv](issue-labels.tsv); [CI artifacts](ci-new-vs-r14-details.txt), [Lanes excerpts](lanes-new-r14-excerpts.txt), [CI comparison lists](ci-new-vs-r14.txt), [Lanes comparison list](lanes-dc45d97c-new-vs-r14.txt). CI prefix-kept and prefix-stripped comparisons agree in counts.

P87-09/render bundler: all 5 `tests/packs/rendering/test_installed_pack_element_contracts.py` tests passed on CI; the timestamp-dependent `test_registry_qualifying_discovery_refuses_corpus_change[new_manifest]` passed. None of those tests appear in Lanes logs; installed wheel job succeeded. See [P87-09 results](p87-09-render-bundler.txt).

Artifacts: [CI counts](ci-counts.tsv), [Lanes per-job counts](lanes-per-job.tsv), [group table](groups.tsv), [per-ID issue labels](issue-labels.tsv), [all primary CI IDs](ci-dc45-primary-ids.txt), [all primary Lanes IDs](lanes-dc45d97c-union-failing-ids.txt).

RUN-STATUS: DONE
