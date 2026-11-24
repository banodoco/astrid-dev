# SV-L8 — commit schema validation investigation

R15-P89-03, [assignment #1777](https://github.com/banodoco/astrid-dev/issues/1777#issuecomment-7118063976). Investigation and evidence only; no product source, pin, CI or task changes. Document branch base 2a2ba3ec43d638691544683231529695d48b2872. Runtime plan source 789d3e2c97cecb10aad1d2914167e999bdbce5fe.

## Installed cost: attribute the actual stacks

[SV-3 profile archive](https://github.com/banodoco/astrid-dev/tree/51783bec00fcd8f037e7fdd4b689f29f6a3e7abf/plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-23-sv3-profile), profile candidate Runtime 297863fb04ccff8f38bf968770bbe98c5ffaec68, archive tree 55fdcc018b61c112d661dc75ac0fab432d0a7ea8. Browser receipt names App 148eaf381e3f02dc0f0d5dfc61e61ebf37dbc715 and installed Agent 5e301956dc49c8b9ba4d23a7ce96c6564bd74d2f. One cold and three warm 300-clip saves, all HTTP 200 and Saved, py-spy 0.4.1 at 100 Hz, no sampling errors. The installed Agent SHA is not resolvable by the connector; the actual installed caller names/lines below come from the raw stacks, and the source inspection/sample uses separately identified accessible Agent source.

Reprocessed the four raw speedscope blobs through the GitHub connector (not the aggregate README alone). Select the non-MainThread profile with the most samples containing a timeline_commit file or function. Reproduce the archive analyze-groups.py innermost matching category; for the jsonschema category (validators.py, _keywords.py, _utils.py under jsonschema), group by the caller stack immediately preceding the first jsonschema frame. Counts below are samples; divide by 100 for seconds. No overlapping stage sum or inferred invocation count.

| Exclusive jsonschema caller | Cold | W1 | W2 | W3 |
| --- | ---: | ---: | ---: | ---: |
| Runtime CommitRequest, service.commit_timeline:3306 -> port.validate_request:62 -> validation.validate_commit_value:250 | 34 | 23 | 23 | 21 |
| Runtime PreparedCommit, store._check_shot_destinations:2025 -> service:3273 lambda -> validation.validate_commit_value:250 | 103 | 70 | 98 | 95 |
| Agent step reads, _commit_patch.normalize_steps:70 -> validate_reads:32 | 26 | 18 | 33 | 28 |
| Agent request reads, CommitPatch.__init__:292 -> validate_reads:32 | 27 | 30 | 38 | 19 |
| Agent command validation (commands.py:137/146, direct or _normalize) | 1 | 2 | 2 | 2 |
| Provider canonical pack _validate_schema | 15 | 0 | 0 | 0 |
| Shared timeline validator setup/check | 7 | 3 | 3 | 0 |
| **Total samples** | **213** | **146** | **197** | **165** |
| **Total seconds** | **2.13** | **1.46** | **1.97** | **1.65** |
| Commit-thread selected samples | 3001 | 1964 | 2813 | 1905 |

Raw blob IDs: cold 1bd193d653565d211ef008b51ef9aa617fcfdc67, W1 9f4f3f805dcbe4e318eaaf1e1b980f501949ce07, W2 b05c8fdc4a61a72d0afc4b935003fbb30c83f599, W3 72cadbb5c7b70cf8ccb4370006b894f9abc6009f. W2's selected thread is labeled astrid-runtime-lifetime-reaper, as in the original grouping; do not silently relabel it. The other three are process_request_thread. This reproduces all four aggregate jsonschema counts exactly. In W3 the two Runtime boundaries account for 116/165 (1.16 s); repeated provider read validation accounts for 47/165 (0.47 s). Many innermost frames are descend, is_type and type, not just validator construction. The 1.65 s is a sampled exclusive bucket, not all validation, wall time or an achievable saving.

## Map to SV-L1 spans and refusal boundaries

[SV-L1 Runtime source](https://github.com/banodoco/astrid-runtime/blob/789d3e2c97cecb10aad1d2914167e999bdbce5fe/runtime_protocol/timeline_commit_execution.py#L34-L47) names handler, service_admission, initial_replay_lookup, provider_commit, port_store_accept, close, durable_reconciliation, wire_response and total, and emits exclusive_timings_ms. The first CommitRequest check is in [service.commit_timeline](https://github.com/banodoco/astrid-runtime/blob/789d3e2c97cecb10aad1d2914167e999bdbce5fe/runtime_protocol/service.py#L3301-L3317), before the narrower service_admission span starts at :3374. Provider step/request checks fall within provider_commit; PreparedCommit falls in the nested port_store_accept (port:697, store:2268). Do not add inclusive provider_commit and port_store_accept. The archived SV-3 profile predates SV-L1; these are source mappings, not invented installed stage timings.

Runtime acceptance detaches prepared values, verifies authorization/context/head, then calls _check_shot_destinations before _validate. The schema check is a wire preflight whose refusal is invalid_prepared (422); later destination/closure refusals are not interchangeable. Preview uses the same preflight after its own head check. History verification separately checks CommitContext and PreparedCommit (store:1181-1182). No authority to skip those. See [store](https://github.com/banodoco/astrid-runtime/blob/789d3e2c97cecb10aad1d2914167e999bdbce5fe/runtime_protocol/timeline_commit_store.py#L2021-L2035).

[Runtime validation](https://github.com/banodoco/astrid-runtime/blob/789d3e2c97cecb10aad1d2914167e999bdbce5fe/runtime_protocol/timeline_commit_validation.py) already has cached schema resources, a cached root validator per definition, bounded evolved-validator reuse by identity, resolver lookup reuse by complete state, and a success memo for CanonicalDocument only. Its blob 488a2049e50185266faaa2dfac5c1d805770d324 is identical on the profile candidate and current plan source. Do not reintroduce a second root cache, bypass finite_json, reuse success across requests/authority boundaries, or infer that separate CommitRequest/PreparedCommit definitions have interchangeable acceptance. The largest individual bucket is the full PreparedCommit traversal, not a proven duplicate call. Leave it in place; a further proposal for this bucket should first measure subtree validation/setup counters and preserve every installed schema/refusal.

## Smallest candidate worth a follow-up measurement

Inside one Agent CommitPatch construction only, share a bounded successful **CommitRead schema** memo across normalize_steps and the request-level validate_reads, retaining the original order and all non-schema checks. [Agent source](https://github.com/banodoco/astrid-agent/blob/3916ff313dc631d30a8a5c4160a58ce33e94a115/astrid/sdk/timeline/_commit_patch.py#L20-L41) constructs a Draft202012Validator per list, then traverses every read separately; step reads and request reads are checked at :70 and :292. _commit_patch blob 54a5e31a7e96420b3c9034f9ed206adf0a86cad2 and schema blob 8cf011bc52480db2ffbe0713516901acf8810244 are unchanged at landed Agent a09ea669a35a104451e48679e242aeb390a4df58. A root-validator instance per patch is even smaller but does not avoid per-read traversal, and its benefit is unmeasured.

The candidate is not a global validation cache. On strictly built-in, finite JSON with string keys and an owned, non-concurrently-mutated read, keep an exact (not digest-only) Unicode JSON string in insertion order, only after a successful schema check. Keep finite serialization, timeline-scope refusal, sorted members/order checks and all later read authority checks on every call. Non-strict values, oversized keys and evictions take the unchanged validation path. Bound the sample to 1024 keys of at most 16,384 ASCII-escaped characters; a tighter byte budget may be desirable. No value mutation or default insertion, no sharing across schema identities or patch instances, no cache of exceptions. **Do not use ASCII-escaped JSON as the key**: a literal surrogate pair and a supplementary scalar serialize identically with ensure_ascii=True, yet can differ under uniqueItems; the scratch test exercises this refusal. Do not use equality, object identity or hash-only keys as substitutes.

This proposal targets the next safely isolatable duplicate check, not the largest Runtime bucket. In the installed profile the step/request read checks total 0.48, 0.71 and 0.47 s on W1-W3 respectively; actual equal-read overlap is unmeasured (browser network receipt does not contain the POST bodies). Before authorizing implementation, collect redacted total/distinct/hit-eligible counters at the two call sites on the actual post-SV-L6 installed fixture; if low overlap or overhead dominates, decline this card. No claim of a 0.47 s saving, much less 1.7 s. Do not remove a Runtime refusal for this optimization.

## CPU differential (executed)

[probe.py](probe.py) is scratch only. Local Linux x86_64, Python 3.13.5, jsonschema 4.26.0, referencing 0.37.0. Command: python probe.py (from this folder). The executed script's git blob is 2cb9aa37e950d3aa7e83b06d3668568b8001e90b, SHA-256 b450b99cd0c01dd16b858019b4ba69ceba76815589f2a422c069315bbf5daaf0; verified against the committed blob. Baseline reproduces the Agent read guard and exact transitive CommitRead/AgentState/JSON schema definitions from the identified blob; it is not an import of the installed SDK. Optional argument path/to/edit-command.schema.json checks that the definitions match and then runs the full schema. No existing product test, contract or assertion edited.

Result: 58 differential cases (26 accepted, 32 refused), same acceptance or exact exception class/message, unchanged input repr, plus mutated-object refusal, bounded eviction, surrogate alias witness. Cases include null/absence, valid scope, nested values, invalid ref/path, missing/extra fields, duplicates, unsorted/mismatched members/order, NaN/infinity, cycles, non-string keys, tuples, bool/int/float, signed zero, oversized payload and warmed repeats. These are a CPU sample, not a universal equivalence theorem; acceptance of a synthetic read is not acceptance of a commit.

| Two lists of 300 reads | Baseline schema calls | Candidate calls / hits | Baseline median ms | Candidate median ms |
| --- | ---: | ---: | ---: | ---: |
| Disjoint | 600 | 600 / 0 | 124.50 | 127.67 |
| Exact overlap | 600 | 300 / 300 | 117.70 | 62.82 |

Five repetitions per row; medians on this sandbox only, not installed evidence. No full suite, hosted CI or product tests run. The Plan 77 save inventory was read; this docs-only experiment did not change that inventory. The lane can rerun the scratch script with the exact accessible Agent schema and compare the source guard; an actual implementation requires the unchanged named inventory and review.

## Handoff

Submit for lane review; no implementation packet authorized here. Re-run probe.py with the Agent schema as above and decide whether installed overlap justifies implementation. Preserve Runtime full schema admission, provider checks and proof boundaries. CI and pin requests are not applicable to an evidence-only PR. Main advanced to b0fe79451856d35b97601df41d4e462d70980444 during investigation (Plan 87 packet/board changes only, no evidence path overlap); no merge performed by this packet. Lane integrates/requalifies the final evidence as required.
