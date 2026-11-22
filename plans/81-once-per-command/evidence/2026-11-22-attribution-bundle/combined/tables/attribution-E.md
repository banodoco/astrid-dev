# Attribution: E

Descriptive source measurements; cProfile values are profiled measurements and are not converted to plain wall seconds.

plain wall: n=5, median=15.425347 s, min=15.135064 s, max=16.519653 s.

timings wall: n=5, median=15.930426 s, min=15.602783 s, max=16.923032 s.

importtime wall: n=5, median=15.753123 s, min=15.425246 s, max=16.326477 s.

cprofile wall: n=5, median=34.392873 s, min=33.816035 s, max=40.267050 s.

## Stages

Self and inclusive medians are sums within each trial; missing inclusive data is unknown. Parent names are reported as recorded.

| Stage | Parent | Count median | Self s | Inclusive s |
| --- | --- | ---: | ---: | ---: |
| Runtime GET /v1/app-state/user/generation | — | 3.000000 | 0.024507 | unknown |
| Runtime GET /v1/capabilities | — | 1.000000 | 0.011361 | unknown |
| Runtime GET /v1/health | — | 1.000000 | 0.006519 | unknown |
| Runtime GET /v1/objects/sha256%3A074c0ee12e41e59bf5f13f4e199e9bfb674a1ff45179bd571320c70196fd7d67 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A0fbdc6f767cf507d617aa7621c611ed67f6cd6182a9e4c0309460dfb2a6231d1 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A387d28c73d5e25288243a9a96ca55b8a595753974bb47606adf55c1e16e8cfac | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A6cec1a01819d67724c0eb28b8232af332bb1a6edc277f0559308fc36fb46ce7b | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Abad6d33473d91ec6f5eb0104ad0378d0333e747144e2a7321d830bb783d414c7 | — | 3.000000 | 0.018755 | unknown |
| Runtime GET /v1/objects/sha256%3Abbcbd2db4033baad83a9f4979a6c1d36dbf4df51ba662443fade0a94324b4104 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Ac3c5fb93cbe5070d20dd4f32fd1bae756363cf1c0a2e43034143337b7822b0e9 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Ad5cd0bfea9d771f671d3e2819964799ec21f7ba0479b91f05ed464d851f4e21c | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Ae05a80b0493f05248a6d36be66ea87eb1ac7264631fc129295792b795cb0d69f | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Af02d24aa267b6ef65442462077f5449572483b440a0c81397c4d877df16d19df | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Afcc41ffed7a5681128315f337c1c24ef8210c2008edaac104d980b434fde590a | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/projects/0f5e5090a0444789b0c430fef2d6f701 | — | 1.000000 | 0.006266 | unknown |
| Runtime POST /v1/handshake | — | 1.000000 | 0.008065 | unknown |
| Runtime POST /v1/projects/0f5e5090a0444789b0c430fef2d6f701/objects | — | 3.000000 | 0.034412 | unknown |
| Runtime POST /v1/tasks | — | 1.000000 | 0.009510 | unknown |
| Runtime acquisition lock | — | 1.000000 | 0.000283 | unknown |
| Runtime launcher connection | — | 1.000000 | 1.006597 | unknown |
| entry lookup | — | 4.000000 | 1.088134 | unknown |
| in-process Runtime acquisition lock | — | 1.000000 | 0.000016 | unknown |
| model registry | — | 1.000000 | 0.156983 | unknown |
| other command work | — | 1.000000 | 6.183114 | unknown |
| pack discovery | — | 18.000000 | 6.608134 | unknown |
| pack host attachment | — | 1.000000 | 0.238609 | unknown |
| pack host lifecycle lock | — | 1.000000 | 0.000033 | unknown |
| pack host readiness | — | 1.000000 | 0.007645 | unknown |
| pack host source identity | — | 1.000000 | 0.137152 | unknown |
| target check | — | 2.000000 | 0.006764 | unknown |
| workflow build | — | 1.000000 | 0.418777 | unknown |

## Imports: Packages

Median self seconds from separately instrumented processes; these do not partition plain wall.

| Name | Self s |
| --- | ---: |
| astrid | 0.315427 |
| vibecomfy | 0.224414 |
| numpy | 0.036107 |
| astrid_runtime_client | 0.027913 |
| rich | 0.026524 |
| yaml | 0.012394 |
| jsonschema | 0.011908 |
| referencing | 0.011255 |
| comfy | 0.010785 |
| attr | 0.009689 |
| httpx | 0.009582 |
| PIL | 0.009043 |
| asyncio | 0.008997 |
| packaging | 0.008323 |
| filelock | 0.007953 |
| click | 0.006635 |
| importlib | 0.005807 |
| email | 0.005629 |
| pygments | 0.005555 |
| http | 0.004648 |
| ipaddress | 0.004572 |
| jsonschema_specifications | 0.003391 |
| urllib | 0.003304 |
| runtime_protocol | 0.003034 |
| typing_extensions | 0.002872 |

## Imports: Modules

Median self seconds from separately instrumented processes; these do not partition plain wall.

| Name | Self s |
| --- | ---: |
| astrid.core.generation.engine_contracts | 0.021228 |
| astrid_runtime_client.generated | 0.020763 |
| vibecomfy.executor.contracts | 0.016420 |
| astrid.core.timeline.clip_fields | 0.014583 |
| astrid.core.rendering.contracts | 0.014123 |
| astrid.core.execution.thumbnail_backfill | 0.013360 |
| vibecomfy.nodes | 0.012981 |
| vibecomfy.comfy_nodes.agent.contracts | 0.012261 |
| astrid.core.generation.cli | 0.011324 |
| astrid.core.execution.generic_host | 0.010661 |
| vibecomfy.workflow | 0.010114 |
| astrid.core.pack.canonical | 0.009280 |
| vibecomfy.porting.edit.ops | 0.008028 |
| jsonschema.validators | 0.007526 |
| numpy._core._multiarray_umath | 0.006892 |
| comfy | 0.006764 |
| astrid.core.contracts.schema | 0.006730 |
| astrid_runtime_client.timeline_commit_types | 0.006585 |
| vibecomfy.porting.emit.ui | 0.006389 |
| astrid.core.generation.asset_gaps | 0.006236 |
| astrid.core.timeline.shot_composition | 0.006203 |
| astrid.sdk.media_handles | 0.006141 |
| astrid.packs.vibecomfy.invocation_preflight | 0.005491 |
| astrid.sdk.execution_request | 0.005413 |
| rich.syntax | 0.005252 |

## cProfile: Self

Shares are medians of each function’s share of its own profiled run total. Cumulative shares overlap and cannot be summed.

| Function | Calls median | Self s | Cumulative s | Self share | Cumulative share |
| --- | ---: | ---: | ---: | ---: | ---: |
| ~:0(<built-in method _hashlib.openssl_sha256>) | 13904.000000 | 4.945304 | 4.945304 | 14.02% | 14.02% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:145(need_more_tokens) | 2167645.000000 | 1.193172 | 2.110153 | 3.48% | 6.10% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:1270(scan_plain) | 133228.000000 | 1.140585 | 3.566796 | 3.31% | 10.24% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:113(check_token) | 1319076.000000 | 0.971076 | 9.762214 | 2.84% | 28.25% |
| ~:0(<method 'poll' of 'select.poll' objects>) | 7.000000 | 0.957628 | 0.957628 | 2.78% | 2.78% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:99(forward) | 1265127.000000 | 0.881803 | 1.032385 | 2.56% | 3.00% |
| ~:0(<built-in method builtins.isinstance>) | 5760222.000000 | 0.808470 | 1.206901 | 2.38% | 3.55% |
| ~:0(<method 'read' of '_io.BufferedReader' objects>) | 14371.000000 | 0.734596 | 0.734808 | 2.11% | 2.11% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:279(stale_possible_simple_keys) | 2251323.000000 | 0.654979 | 0.654979 | 1.89% | 1.89% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:87(peek) | 5362750.000000 | 0.646435 | 0.658987 | 1.85% | 1.89% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:156(fetch_more_tokens) | 265382.000000 | 0.615357 | 7.033464 | 1.79% | 20.32% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/parser.py:273(parse_node) | 174810.000000 | 0.620133 | 2.726912 | 1.78% | 7.87% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:1311(scan_plain_spaces) | 189900.000000 | 0.601818 | 1.341321 | 1.71% | 3.84% |
| ~:0(<method 'update' of '_hashlib.HASH' objects>) | 72056.000000 | 0.557613 | 0.557613 | 1.59% | 1.59% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:752(scan_to_next_token) | 265382.000000 | 0.421260 | 0.919357 | 1.24% | 2.70% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:114(get_mark) | 698363.000000 | 0.419738 | 0.530559 | 1.23% | 1.55% |
| ~:0(<built-in method builtins.len>) | 2744545.000000 | 0.388418 | 0.443166 | 1.13% | 1.28% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:63(compose_node) | 174810.000000 | 0.382925 | 13.580346 | 1.11% | 39.17% |
| /usr/local/lib/python3.13/pathlib/_local.py:257(_parse_path) | 104424.000000 | 0.369655 | 0.675431 | 1.08% | 1.96% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:264(next_possible_simple_key) | 1985941.000000 | 0.346984 | 0.346984 | 0.98% | 0.98% |
| /usr/local/lib/python3.13/pathlib/_local.py:117(__init__) | 265014.000000 | 0.324730 | 0.508863 | 0.94% | 1.47% |
| ~:0(<built-in method posix.lstat>) | 253610.000000 | 0.322885 | 0.322885 | 0.94% | 0.94% |
| <frozen posixpath>:388(realpath) | 27141.000000 | 0.313492 | 1.025343 | 0.92% | 2.95% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/parser.py:94(check_event) | 528924.000000 | 0.309514 | 12.330149 | 0.89% | 35.60% |
| /usr/local/lib/python3.13/copy.py:119(deepcopy) | 283146.000000 | 0.319729 | 0.812500 | 0.85% | 2.15% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/jsonschema/validators.py:396(descend) | 98226.000000 | 0.282666 | 2.520310 | 0.80% | 7.27% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:545(fetch_value) | 72809.000000 | 0.268282 | 0.522340 | 0.79% | 1.53% |
| ~:0(<method 'append' of 'list' objects>) | 1510620.000000 | 0.255508 | 0.255508 | 0.75% | 0.75% |
| ~:0(<built-in method builtins.exec>) | 1374.000000 | 0.254841 | 33.977368 | 0.73% | 100.10% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:94(prefix) | 565930.000000 | 0.234144 | 0.311127 | 0.69% | 0.91% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:135(get_token) | 375103.000000 | 0.233320 | 0.671421 | 0.68% | 1.94% |
| ~:0(<built-in method posix.stat>) | 60189.000000 | 0.220982 | 0.499460 | 0.65% | 1.45% |
| ~:0(<method 'get' of 'dict' objects>) | 1236747.000000 | 0.222716 | 0.222850 | 0.64% | 0.65% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/jsonschema/validators.py:339(evolve) | 102435.000000 | 0.218471 | 0.466139 | 0.63% | 1.36% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:88(compose_scalar_node) | 146681.000000 | 0.214996 | 0.550343 | 0.60% | 1.57% |
| ~:0(<built-in method sys.intern>) | 805020.000000 | 0.201235 | 0.201235 | 0.59% | 0.59% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/resolver.py:143(resolve) | 174810.000000 | 0.196480 | 0.295228 | 0.57% | 0.86% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:1416(scan_line_break) | 354540.000000 | 0.191912 | 0.353198 | 0.56% | 1.03% |
| /usr/local/lib/python3.13/pathlib/_abc.py:130(with_segments) | 209545.000000 | 0.184914 | 0.857275 | 0.55% | 2.50% |
| /usr/local/lib/python3.13/pathlib/_local.py:498(__init__) | 248293.000000 | 0.174746 | 0.641547 | 0.52% | 1.88% |

## cProfile: Cumulative

Shares are medians of each function’s share of its own profiled run total. Cumulative shares overlap and cannot be summed.

| Function | Calls median | Self s | Cumulative s | Self share | Cumulative share |
| --- | ---: | ---: | ---: | ---: | ---: |
| ~:0(<built-in method builtins.next>) | 70702.000000 | 0.016510 | 34.036877 | 0.05% | 100.54% |
| ~:0(<built-in method builtins.exec>) | 1374.000000 | 0.254841 | 33.977368 | 0.73% | 100.10% |
| /root/codex/plan-81m/attribution-evidence.env/bin/astrid:1(<module>) | 1.000000 | 0.000016 | 33.977326 | 0.00% | 100.10% |
| /root/codex/plan-81m/a4-agent/astrid/console.py:70(main) | 1.000000 | 0.000014 | 33.912228 | 0.00% | 99.97% |
| /root/codex/plan-81m/a4-agent/astrid/core/gateway/__init__.py:72(main) | 1.000000 | 0.000014 | 33.849432 | 0.00% | 99.86% |
| /root/codex/plan-81m/a4-agent/astrid/core/gateway/__init__.py:105(_main_impl) | 1.000000 | 0.000007 | 33.849399 | 0.00% | 99.86% |
| /root/codex/plan-81m/a4-agent/astrid/core/gateway/dispatch.py:82(_dispatch_generate) | 1.000000 | 0.000015 | 33.849390 | 0.00% | 99.86% |
| /usr/local/lib/python3.13/contextlib.py:145(__exit__) | 95.000000 | 0.000264 | 33.812392 | 0.00% | 99.79% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:952(main) | 1.000000 | 0.000030 | 33.808334 | 0.00% | 99.77% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/command_timing.py:79(timing_scope) | 2.000000 | 0.000044 | 33.703620 | 0.00% | 99.57% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/command_timing.py:50(close) | 1.000000 | 0.000006 | 33.671621 | 0.00% | 99.51% |
| /usr/local/lib/python3.13/threading.py:1059(join) | 1.000000 | 0.000004 | 33.671605 | 0.00% | 99.51% |
| ~:0(<method 'join' of '_thread._ThreadHandle' objects>) | 1.000000 | 0.000103 | 33.671599 | 0.00% | 99.51% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:968(_main_with_errors) | 1.000000 | 0.000031 | 33.671380 | 0.00% | 99.50% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:586(_main) | 1.000000 | 0.000020 | 33.671278 | 0.00% | 99.50% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:617(_main_request) | 1.000000 | 0.000126 | 33.671133 | 0.00% | 99.50% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/command_timing.py:171(timed_call) | 8.000000 | 0.000173 | 22.739337 | 0.00% | 65.80% |
| /usr/local/lib/python3.13/contextlib.py:82(inner) | 18.000000 | 0.000783 | 20.119201 | 0.00% | 58.16% |
| /root/codex/plan-81m/a4-agent/astrid/core/pack/discovery.py:366(discover_pack_metadata) | 18.000000 | 0.005916 | 20.116033 | 0.02% | 58.15% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/entries.py:962(resolve_entry_inputs) | 2.000000 | 0.000015 | 18.593853 | 0.00% | 53.81% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/entries.py:818(resolve_entry_inputs) | 2.000000 | 0.000044 | 18.593837 | 0.00% | 53.81% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/entries.py:941(describe_entry) | 3.000000 | 0.000029 | 18.593581 | 0.00% | 53.81% |
| /root/codex/plan-81m/a4-agent/astrid/core/pack/loader.py:466(load_pack_manifest) | 96.000000 | 0.003485 | 17.397058 | 0.01% | 49.87% |
| /root/codex/plan-81m/a4-agent/astrid/core/pack/canonical.py:951(validate_canonical_pack) | 96.000000 | 0.003400 | 17.167446 | 0.01% | 49.21% |
| /root/codex/plan-81m/a4-agent/astrid/core/pack/canonical.py:864(_admit) | 96.000000 | 0.023920 | 16.884852 | 0.07% | 49.20% |
| /root/codex/plan-81m/a4-agent/astrid/core/pack/loader.py:105(scan_packs) | 8.000000 | 0.000291 | 15.665825 | 0.00% | 45.08% |
| /root/codex/plan-81m/a4-agent/astrid/core/pack/loader.py:143(_scan_packs_locked) | 8.000000 | 0.005951 | 15.654790 | 0.02% | 45.05% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/__init__.py:74(load) | 410.000000 | 0.037146 | 14.277988 | 0.11% | 41.27% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/constructor.py:47(get_single_data) | 410.000000 | 0.001125 | 14.216995 | 0.00% | 41.08% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:2282(generate) | 1.000000 | 0.000022 | 13.935682 | 0.00% | 41.01% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:588(call) | 2.000000 | 0.000081 | 13.935528 | 0.00% | 41.01% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:2326(_generate_resolved_media) | 1.000000 | 0.000017 | 13.934824 | 0.00% | 41.00% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:2330(_media_request_impl) | 1.000000 | 0.000083 | 13.934806 | 0.00% | 41.00% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/entries.py:549(describe_entry) | 1.000000 | 0.001180 | 13.455646 | 0.00% | 39.38% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:29(get_single_node) | 410.000000 | 0.001424 | 13.626201 | 0.00% | 39.32% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:50(compose_document) | 410.000000 | 0.000958 | 13.585754 | 0.00% | 39.19% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:63(compose_node) | 174810.000000 | 0.382925 | 13.580346 | 1.11% | 39.17% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:117(compose_mapping_node) | 20635.000000 | 0.162825 | 13.567591 | 0.47% | 39.13% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/parser.py:94(check_event) | 528924.000000 | 0.309514 | 12.330149 | 0.89% | 35.60% |
| /root/codex/plan-81m/a4-agent/astrid/core/pack/canonical.py:432(_read_manifest) | 336.000000 | 0.003783 | 11.944416 | 0.01% | 34.29% |

