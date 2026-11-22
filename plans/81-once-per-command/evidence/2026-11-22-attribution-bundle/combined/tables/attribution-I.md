# Attribution: I

Descriptive source measurements; cProfile values are profiled measurements and are not converted to plain wall seconds.

plain wall: n=5, median=11.566748 s, min=11.028328 s, max=12.080149 s.

timings wall: n=5, median=12.123561 s, min=11.636938 s, max=12.346628 s.

importtime wall: n=5, median=11.381852 s, min=11.147795 s, max=11.622176 s.

cprofile wall: n=5, median=18.418344 s, min=17.874915 s, max=20.033003 s.

## Stages

Self and inclusive medians are sums within each trial; missing inclusive data is unknown. Parent names are reported as recorded.

| Stage | Parent | Count median | Self s | Inclusive s |
| --- | --- | ---: | ---: | ---: |
| Runtime GET /v1/app-state/user/generation | — | 3.000000 | 0.024408 | unknown |
| Runtime GET /v1/capabilities | — | 1.000000 | 0.013530 | unknown |
| Runtime GET /v1/health | — | 1.000000 | 0.007500 | unknown |
| Runtime GET /v1/objects/sha256%3A022e236e9bd1e9777ebff5a9c970bec0c614cdddbaa7fbe466f4d16c7bd2a8d5 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A0d5863c04234daafc44c0800838cdf667931633d55bf20bb1d426296df3d5830 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A1da8bcc966aec8fda55421de747cfbfd4c01fd9782a21c9bd45b8039c2c2db0a | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A50377bb153ab509f432a946c9123a43825c5e535a6b80840ae25ea6018f17b92 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A5ba991c70b238c3378935d1127c39e2c4de66bcad34c74522d1aa4858841d673 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A6a929f117718447d458b50365601511371d10258c9528a905d8ae66a8ad792bd | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A8545746c4c7daf6fcd1b07241df422e2af97ee9f797b3786c88b65356ee81b27 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Aba9181db80249d574fafe3a487f61132dbef147c084a7b4400389a191a8691d6 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Abad6d33473d91ec6f5eb0104ad0378d0333e747144e2a7321d830bb783d414c7 | — | 3.000000 | 0.024247 | unknown |
| Runtime GET /v1/objects/sha256%3Ae8d628189eab2b24ef16da78d4e91f90d4518c96e4c617c3b1475501709958dc | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Aed36d1e06405f294140d58fe3e37424f0199d4441a037d8a01a36fda6502f496 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/projects/200b4f234945412da1a5deb49ab39d7d | — | 1.000000 | 0.007213 | unknown |
| Runtime POST /v1/handshake | — | 1.000000 | 0.006439 | unknown |
| Runtime POST /v1/projects/200b4f234945412da1a5deb49ab39d7d/objects | — | 3.000000 | 0.037728 | unknown |
| Runtime POST /v1/tasks | — | 1.000000 | 0.012490 | unknown |
| Runtime acquisition lock | — | 1.000000 | 0.000683 | unknown |
| Runtime launcher connection | — | 1.000000 | 1.046507 | unknown |
| entry discovery | — | 1.000000 | 0.005431 | unknown |
| in-process Runtime acquisition lock | — | 1.000000 | 0.000029 | unknown |
| model registry | — | 1.000000 | 0.058855 | unknown |
| other command work | — | 1.000000 | 6.452376 | unknown |
| pack discovery | — | 18.000000 | 2.781301 | unknown |
| pack host attachment | — | 1.000000 | 0.394091 | unknown |
| pack host lifecycle lock | — | 1.000000 | 0.000041 | unknown |
| pack host readiness | — | 1.000000 | 0.009226 | unknown |
| pack host source identity | — | 1.000000 | 0.150641 | unknown |
| target check | — | 2.000000 | 0.006352 | unknown |
| workflow build | — | 1.000000 | 0.611522 | unknown |

## Imports: Packages

Median self seconds from separately instrumented processes; these do not partition plain wall.

| Name | Self s |
| --- | ---: |
| astrid | 0.293624 |
| vibecomfy | 0.220215 |
| numpy | 0.101905 |
| astrid_runtime_client | 0.026152 |
| rich | 0.021555 |
| referencing | 0.012642 |
| attr | 0.011041 |
| packaging | 0.010761 |
| yaml | 0.010375 |
| comfy | 0.010052 |
| PIL | 0.009570 |
| httpx | 0.009105 |
| filelock | 0.008539 |
| asyncio | 0.008423 |
| jsonschema | 0.007591 |
| click | 0.005683 |
| pygments | 0.005297 |
| importlib | 0.005041 |
| email | 0.004309 |
| ipaddress | 0.004282 |
| http | 0.004069 |
| jsonschema_specifications | 0.003916 |
| urllib | 0.003800 |
| encodings | 0.002557 |
| dotenv | 0.002550 |

## Imports: Modules

Median self seconds from separately instrumented processes; these do not partition plain wall.

| Name | Self s |
| --- | ---: |
| numpy._core._multiarray_umath | 0.062986 |
| astrid.core.generation.engine_contracts | 0.022268 |
| astrid_runtime_client.generated | 0.019832 |
| vibecomfy.executor.contracts | 0.017018 |
| astrid.core.rendering.contracts | 0.013694 |
| vibecomfy.nodes | 0.013052 |
| vibecomfy.comfy_nodes.agent.contracts | 0.012652 |
| astrid.core.execution.thumbnail_backfill | 0.012081 |
| astrid.core.execution.generic_host | 0.011743 |
| astrid.core.pack.canonical | 0.011252 |
| astrid.core.generation.cli | 0.011124 |
| vibecomfy.workflow | 0.009476 |
| referencing._core | 0.008259 |
| vibecomfy.porting.edit.ops | 0.008150 |
| vibecomfy.runtime.session | 0.008016 |
| astrid.core.contracts.schema | 0.006936 |
| astrid.core.model_catalog.schema | 0.006571 |
| comfy | 0.006552 |
| astrid.core.generation.asset_gaps | 0.006533 |
| astrid_runtime_client.timeline_commit_types | 0.005902 |
| astrid.core.timeline.shot_composition | 0.005888 |
| astrid.core.execution.executor.schema | 0.005350 |
| astrid.packs.vibecomfy.invocation_preflight | 0.005205 |
| astrid.sdk.media_handles | 0.005143 |
| astrid.sdk.execution_request | 0.004986 |

## cProfile: Self

Shares are medians of each function’s share of its own profiled run total. Cumulative shares overlap and cannot be summed.

| Function | Calls median | Self s | Cumulative s | Self share | Cumulative share |
| --- | ---: | ---: | ---: | ---: | ---: |
| ~:0(<built-in method _hashlib.openssl_sha256>) | 10440.000000 | 4.444215 | 4.444215 | 24.94% | 24.94% |
| ~:0(<method 'poll' of 'select.poll' objects>) | 7.000000 | 1.049049 | 1.049049 | 5.99% | 5.99% |
| ~:0(<method 'update' of '_hashlib.HASH' objects>) | 108074.000000 | 0.829815 | 0.829815 | 4.58% | 4.58% |
| ~:0(<method 'read' of '_io.BufferedReader' objects>) | 10977.000000 | 0.662092 | 0.662490 | 3.63% | 3.65% |
| /usr/local/lib/python3.13/copy.py:119(deepcopy) | 374611.000000 | 0.369940 | 0.943107 | 2.05% | 5.23% |
| /usr/local/lib/python3.13/pathlib/_local.py:257(_parse_path) | 78630.000000 | 0.286617 | 0.511022 | 1.54% | 2.81% |
| ~:0(<built-in method builtins.isinstance>) | 1808373.000000 | 0.264768 | 0.342656 | 1.51% | 1.96% |
| /usr/local/lib/python3.13/pathlib/_local.py:117(__init__) | 219495.000000 | 0.243614 | 0.387261 | 1.37% | 2.17% |
| ~:0(<built-in method builtins.exec>) | 1351.000000 | 0.233394 | 18.055893 | 1.33% | 100.11% |
| ~:0(<method 'readinto' of '_io.BufferedReader' objects>) | 28872.000000 | 0.233380 | 0.233380 | 1.27% | 1.27% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:145(need_more_tokens) | 312120.000000 | 0.176514 | 0.313915 | 1.01% | 1.78% |
| ~:0(<built-in method posix.stat>) | 43178.000000 | 0.176612 | 0.412383 | 0.98% | 2.29% |
| ~:0(<built-in method builtins.id>) | 513120.000000 | 0.175047 | 0.175047 | 0.97% | 0.97% |
| /usr/local/lib/python3.13/json/decoder.py:351(raw_decode) | 173.000000 | 0.173991 | 0.174255 | 0.92% | 0.92% |
| ~:0(<built-in method builtins.len>) | 975734.000000 | 0.161425 | 0.206328 | 0.92% | 1.18% |
| ~:0(<built-in method _io.open>) | 23110.000000 | 0.158181 | 0.284098 | 0.88% | 1.57% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:1270(scan_plain) | 19186.000000 | 0.159491 | 0.507218 | 0.88% | 2.81% |
| ~:0(<built-in method posix.lstat>) | 117632.000000 | 0.162690 | 0.162690 | 0.85% | 0.85% |
| /usr/local/lib/python3.13/pathlib/_local.py:174(_str_normcase) | 263712.000000 | 0.148093 | 0.323716 | 0.85% | 1.71% |
| /usr/local/lib/python3.13/pathlib/_abc.py:130(with_segments) | 176138.000000 | 0.147335 | 0.683259 | 0.83% | 3.87% |
| /usr/local/lib/python3.13/pathlib/_local.py:498(__init__) | 208270.000000 | 0.144534 | 0.510963 | 0.83% | 2.86% |
| ~:0(<built-in method sys.intern>) | 598791.000000 | 0.146074 | 0.146074 | 0.82% | 0.82% |
| <frozen posixpath>:388(realpath) | 13298.000000 | 0.154906 | 0.539802 | 0.81% | 2.80% |
| ~:0(<method 'get' of 'dict' objects>) | 917744.000000 | 0.136399 | 0.136557 | 0.77% | 0.77% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:99(forward) | 205174.000000 | 0.138671 | 0.163530 | 0.77% | 0.90% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:113(check_token) | 190287.000000 | 0.145116 | 1.460809 | 0.76% | 8.08% |
| /usr/local/lib/python3.13/pathlib/_local.py:289(drive) | 133346.000000 | 0.130914 | 0.832089 | 0.71% | 4.52% |
| ~:0(<built-in method marshal.loads>) | 833.000000 | 0.121474 | 0.121474 | 0.69% | 0.69% |
| /usr/local/lib/python3.13/copy.py:218(_deepcopy_dict) | 37646.000000 | 0.125643 | 0.888687 | 0.69% | 4.93% |
| /root/codex/plan-81m/a4-agent/astrid/core/pack/discovery.py:91(visit) | 16650.000000 | 0.124483 | 3.059810 | 0.68% | 16.89% |
| /usr/local/lib/python3.13/pathlib/_local.py:365(relative_to) | 28109.000000 | 0.118871 | 1.693760 | 0.68% | 9.67% |
| /usr/local/lib/python3.13/hashlib.py:195(file_digest) | 12582.000000 | 0.126301 | 1.205776 | 0.67% | 6.69% |
| /usr/local/lib/python3.13/pathlib/_local.py:227(__str__) | 221575.000000 | 0.120294 | 0.667717 | 0.66% | 3.68% |
| ~:0(<method 'set_default_verify_paths' of '_ssl._SSLContext' objects>) | 26.000000 | 0.116406 | 0.116406 | 0.64% | 0.64% |
| /usr/local/lib/python3.13/pathlib/_local.py:44(__getitem__) | 87391.000000 | 0.107222 | 0.713292 | 0.58% | 4.07% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:279(stale_possible_simple_keys) | 323911.000000 | 0.097740 | 0.097740 | 0.54% | 0.54% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:87(peek) | 777411.000000 | 0.097553 | 0.099547 | 0.54% | 0.55% |
| /usr/local/lib/python3.13/pathlib/_local.py:193(__eq__) | 123962.000000 | 0.092907 | 0.414514 | 0.53% | 2.26% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:156(fetch_more_tokens) | 37874.000000 | 0.091335 | 1.053695 | 0.51% | 5.83% |
| ~:0(<method 'append' of 'list' objects>) | 557236.000000 | 0.094564 | 0.094564 | 0.51% | 0.51% |

## cProfile: Cumulative

Shares are medians of each function’s share of its own profiled run total. Cumulative shares overlap and cannot be summed.

| Function | Calls median | Self s | Cumulative s | Self share | Cumulative share |
| --- | ---: | ---: | ---: | ---: | ---: |
| ~:0(<built-in method builtins.exec>) | 1351.000000 | 0.233394 | 18.055893 | 1.33% | 100.11% |
| /root/codex/plan-81m/attribution-evidence.env/bin/astrid:1(<module>) | 1.000000 | 0.000015 | 18.055861 | 0.00% | 100.11% |
| /root/codex/plan-81m/a4-agent/astrid/console.py:70(main) | 1.000000 | 0.000014 | 18.015534 | 0.00% | 99.87% |
| ~:0(<built-in method builtins.next>) | 10376.000000 | 0.003015 | 17.998242 | 0.02% | 99.83% |
| /root/codex/plan-81m/a4-agent/astrid/core/gateway/__init__.py:72(main) | 1.000000 | 0.000013 | 17.979923 | 0.00% | 99.66% |
| /root/codex/plan-81m/a4-agent/astrid/core/gateway/__init__.py:105(_main_impl) | 1.000000 | 0.000007 | 17.979899 | 0.00% | 99.66% |
| /root/codex/plan-81m/a4-agent/astrid/core/gateway/dispatch.py:82(_dispatch_generate) | 1.000000 | 0.000013 | 17.979892 | 0.00% | 99.66% |
| /usr/local/lib/python3.13/contextlib.py:145(__exit__) | 71.000000 | 0.000216 | 17.961477 | 0.00% | 99.54% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:952(main) | 1.000000 | 0.000026 | 17.955140 | 0.00% | 99.52% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/command_timing.py:79(timing_scope) | 2.000000 | 0.000042 | 17.882825 | 0.00% | 99.16% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/command_timing.py:50(close) | 1.000000 | 0.000011 | 17.863462 | 0.00% | 99.05% |
| /usr/local/lib/python3.13/threading.py:1059(join) | 1.000000 | 0.000024 | 17.783384 | 0.00% | 98.71% |
| ~:0(<method 'join' of '_thread._ThreadHandle' objects>) | 1.000000 | 0.000139 | 17.782340 | 0.00% | 98.71% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:968(_main_with_errors) | 1.000000 | 0.000005 | 17.778998 | 0.00% | 98.70% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:586(_main) | 1.000000 | 0.000013 | 17.778992 | 0.00% | 98.70% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:617(_main_request) | 1.000000 | 0.000086 | 17.778972 | 0.00% | 98.70% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:588(call) | 2.000000 | 0.000117 | 15.480318 | 0.00% | 88.16% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:2290(image) | 1.000000 | 0.000023 | 15.477422 | 0.00% | 88.14% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:2323(_media_request) | 1.000000 | 0.000018 | 15.477394 | 0.00% | 88.14% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:2330(_media_request_impl) | 1.000000 | 0.000069 | 15.477378 | 0.00% | 88.14% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:1623(_generate_on_target) | 1.000000 | 0.000090 | 12.928421 | 0.00% | 71.69% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:1653(_generate_on_target_impl) | 1.000000 | 0.000564 | 12.554844 | 0.00% | 69.28% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/workflow_bundle.py:3234(emit_bundle) | 1.000000 | 0.000224 | 6.412104 | 0.00% | 35.55% |
| /usr/local/lib/python3.13/contextlib.py:82(inner) | 17.000000 | 0.000526 | 6.069848 | 0.00% | 34.67% |
| /root/codex/plan-81m/a4-agent/astrid/core/pack/discovery.py:366(discover_pack_metadata) | 17.000000 | 0.003429 | 6.067314 | 0.02% | 34.66% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:308(_resolve_class_type) | 556.000000 | 0.003135 | 5.595408 | 0.02% | 31.18% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:197(_sync_reader) | 2226.000000 | 0.035017 | 5.584504 | 0.19% | 31.12% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/entrypoints.py:185(emit_scratchpad_python) | 2.000000 | 0.000073 | 5.588280 | 0.00% | 30.99% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/entrypoints.py:35(emit_canonical_python) | 2.000000 | 0.000071 | 5.578478 | 0.00% | 30.93% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/emit_ready.py:804(emit_ready_template_python) | 2.000000 | 0.000215 | 5.578335 | 0.00% | 30.93% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/emit_ready.py:849(_emit_ready_template_python_inner) | 2.000000 | 0.000892 | 5.578046 | 0.00% | 30.93% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/generation.py:85(cache_file_witness) | 9236.000000 | 0.063718 | 5.486763 | 0.35% | 30.77% |
| ~:0(<built-in method builtins.any>) | 18665.000000 | 0.019800 | 5.169584 | 0.11% | 29.07% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/widgets/compact_resolver.py:150(compact_widget_names_for_node) | 254.000000 | 0.004117 | 5.212174 | 0.02% | 28.96% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/widgets/compact_resolver.py:312(_candidate_name_sources) | 254.000000 | 0.004634 | 5.182456 | 0.03% | 28.79% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:220(<genexpr>) | 6675.000000 | 0.024228 | 4.848669 | 0.13% | 27.09% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/command_timing.py:171(timed_call) | 6.000000 | 0.000124 | 4.593108 | 0.00% | 25.66% |
| ~:0(<built-in method _hashlib.openssl_sha256>) | 10440.000000 | 4.444215 | 4.444215 | 24.94% | 24.94% |
| /root/codex/plan-81m/a4-agent/astrid/core/model_catalog/registry.py:105(load_default) | 2.000000 | 0.000157 | 3.753928 | 0.00% | 21.44% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/workflow_bundle.py:1581(_canonicalize_for_v2_pair) | 1.000000 | 0.000195 | 3.434252 | 0.00% | 19.09% |

