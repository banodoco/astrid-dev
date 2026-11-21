# Terminal #444 combined CI

CI run 44714461029 on ba4741b3 concluded failure. On all eight unit shards, combined introduced zero adverse outcomes against the destination and recovered one failing call. All 14 failure-ceiling archives from each of the three revisions were size- and SHA-256-verified. Command records bound the expected head, all pytest executions reached native finish, and all comparable commands produced identical raw exits on all three heads. [Combined CI](https://github.com/banodoco/astrid-agent/actions/runs/44714461029) · [Destination 66c5ee27](https://github.com/banodoco/astrid-agent/actions/runs/44682589147) · [Source eff1c195](https://github.com/banodoco/astrid-agent/actions/runs/44643901988)

Each arm contained the same 31,064 unit IDs, 93,390 distinct phase/subtest keys and 93,391 report records. Exactly 93,388 keys match literally across all three. The remaining two each passed on all three and differed only in their generated temporary directories, one for the missing PNG inventory, one for the missing service-unit fragment. No ID, phase or subtest was lost. All 24 unit pytest executions exited 1.

| Shard | Combined artifact | Unit IDs | Phase/subtest keys |
|---|---|---:|---:|
| 1 | [14624120875](https://github.com/banodoco/astrid-agent/actions/runs/44714461029/artifacts/14624120875) | 5,375 | 16,221 |
| 2 | [14622493695](https://github.com/banodoco/astrid-agent/actions/runs/44714461029/artifacts/14622493695) | 4,028 | 12,039 |
| 3 | [14622333684](https://github.com/banodoco/astrid-agent/actions/runs/44714461029/artifacts/14622333684) | 1,933 | 5,799 |
| 4 | [14623515987](https://github.com/banodoco/astrid-agent/actions/runs/44714461029/artifacts/14623515987) | 2,073 | 6,200 |
| 5 | [14620148403](https://github.com/banodoco/astrid-agent/actions/runs/44714461029/artifacts/14620148403) | 2,379 | 7,062 |
| 6 | [14624886499](https://github.com/banodoco/astrid-agent/actions/runs/44714461029/artifacts/14624886499) | 5,365 | 16,192 |
| 7 | [14623510903](https://github.com/banodoco/astrid-agent/actions/runs/44714461029/artifacts/14623510903) | 6,098 | 18,261 |
| 8 | [14621732119](https://github.com/banodoco/astrid-agent/actions/runs/44714461029/artifacts/14621732119) | 3,813 | 11,616 |

| Unit call | Plan | Source | Combined | First failure reason |
|---|---|---|---|---|
| Missing model files, list and defaults agreement | Fail | Pass | Pass | The plan returned “no attached ComfyUI target or model probe unavailable” where the test expected “required models missing or ambiguous”. |
| Remotion parallel asset-server burst | Pass | Fail | Pass | The source timed out reading the HTTP response. |
| Pinokio CLI help and local receipt | Fail | Pass | Fail | The active process was not the configured listener owner. |
| Pinokio real local start/readiness/stop | Fail | Pass | Fail | The active process was not the configured listener owner. |

These four call keys account for every unit outcome difference across all three heads. The combined run recorded 843 failed call or subtest reports, compared with 844 on plan and 842 on source. All three recorded 363 failed setups, 57 skipped setups and 31,064 passing teardowns.

Fast checks, Darwin and Windows native/installer retained all 320, 55 and 114 respective IDs and every phase outcome on both comparisons. Boundary and Windows succeeded. Fast checks, Darwin, both release-wheel jobs, all eight unit jobs and the dependent unit aggregate failed. The two wheel commands ended at the same missing astrid import. No combined CI jobs remain pending. The independent Windows shell journey and protected approval have separate receipts.

The [official merge-tier archive](https://github.com/banodoco/astrid-agent/actions/runs/44730671649/artifacts/14626311921) verified against SHA-256 `d381099547c50ae12413b3a84468c854fb6fe2c9d199901ee5384c92aebe65a9`. The trusted plan reader normalized 14 of 19 jobs and reported 5,860 errors, 12 unknown entries, 137 covered and zero retired. The local proposed reader normalized 15 jobs, reported 5,895 errors and 10 unknown entries, and recovered all 35 Windows launcher observations. The trusted reader’s local and hosted observations and error multisets match. [Lead disposition](https://github.com/banodoco/astrid-agent/pull/444#issuecomment-7038826882)
