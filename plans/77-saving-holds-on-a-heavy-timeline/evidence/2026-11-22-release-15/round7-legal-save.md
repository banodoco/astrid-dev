# Measured legal save on the repaired Round 7 tuple

The isolated v30 restore had the same authenticated database bytes and visual fixture as stock. The trusted V6 move used the same free-interval plan, 189.293747811 s. The accepted clip start was 189.300 s. The Runtime acceptance and independent public read agreed on publication `txn-2f2b09cc5279421e9fac2046c04c5755`, one active head, all 300 clip IDs and ten occurrences, and the exact one-clip document change. The stock HTTP acceptance returned the same resulting revision and content digest, with its own publication ID. Stock's independent public postflight and browser Saved were unobserved.

| Segment | Stock legal arm | Repaired candidate |
| --- | ---: | ---: |
| Pointer release to first scoped POST | 10.7595 s | 1.5151 s |
| POST to HTTP 200 accepted | 32.5641 s | 36.1249 s |
| HTTP response to confirmed Saved | unobserved | 0.6809 s |
| End to end | unconfirmed | 38.3209 s |

The candidate handoff was ready 1.3658 s before release. Capture began 0.0379 s after release, resolved at 1.0652 s, and accounted for about 1.0273 s. The badge showed Saving at 1.2158 s, and the exact POST began at 1.5151 s. No named durable enqueue or pump phases were emitted in this compiled trace, so the remaining 0.4499 s between capture resolution and POST is unassigned. The UI briefly showed “not saved” at 31.570 s, then confirmed Saved at 38.321 s. On stock the first two warm history GETs failed at 60 s each before later successes. A scoped history GET started about 2.6 s after the accepted response and failed at 60 s. Its retry and the independent public read were unfinished when the test stopped. The stock arm captured network intervals, the pointer path and the exact acceptance receipt. It did not retain the internal editor phase trace or a Runtime profile. Its sandbox was already removed when profiling was requested.

## Runtime sample

The 100 Hz nonblocking py-spy recorder ran on the same verified Runtime process from just before the trusted gesture through the exact HTTP 200. It covered 38.324 wall s and 36.19 Runtime process CPU s. It retained 3,291 samples with 487 reported sampling errors. SHA-256 of the raw speedscope file is `f31722b9e3782aabef6af15c6041456c10686f8a22ed580873c252a55a1dca76`. The 5, 15 and 30 s dumps were successful. The hot request thread has 32.14 s of sampled stack weight out of 32.91 s across eleven sampled threads. The table uses the request thread as denominator.

| Inclusive frame category | Weighted s | Share |
| --- | ---: | ---: |
| Accepted-history record verification, including its dependencies | 12.06 | 37.5% |
| Direct historical replay, key collection and preceding-row hash walk | 10.37 | 32.3% |
| Historical semantic replay function itself and its callees | 6.84 | 21.3% |
| Head and history-entry reconciliation frames | 11.12 | 34.6% |
| JSON Schema evaluation | 9.76 | 30.4% |
| Runtime port accept wrappers | 3.54 | 11.0% |
| Current store accept at its validation call | 2.43 | 7.6% |
| Current acceptance validation and its callees | 2.32 | 7.2% |
| Durable result lookup and its nested verification | 1.93 | 6.0% |
| Current request-context check | 0.30 | 0.9% |
| Receipt insertion frame | 0.01 | about 0.03% |

The inclusive rows overlap. Of the 9.76 JSON Schema seconds, 3.98 also had explicit replay frames. The remaining 5.78 cannot be assigned to the current acceptance validation. For a disjoint partition, 12.06 s had the historic verifier present, 9.48 s had broader validation or schema frames with no historic-verifier marker, and 10.60 s had neither marker. Only 2.32 s has the exact current validation marker. No wait bound follows from this profile because the nonblocking sampler omits many idle stacks and lost some samples.

The largest self costs include producer value equality across two lines (3.75 s), Python deep copies across leaves (about 3.36 s), JSON Schema descent (2.72 s), and JSON encoding (2.61 s). The 5 s dump shows accepted history hashing and replay below the current read of history and head. The 15 s dump is inside JSON Schema reference evaluation. The 30 s dump is in an authenticated history entry reached by the current accept context check.

The candidate's history-related request work occupies substantially more sampled time than its new acceptance validation. The scoped verified opening and read isolation allow the editor to dispatch earlier on this sample and confirm the result. The 36.125 s Runtime service interval remains the largest cost. Remembered verification runs as a separate Runtime follow-up. The first-cut landing gate continues independently. The separately tested validation memo has no measured effect yet.
