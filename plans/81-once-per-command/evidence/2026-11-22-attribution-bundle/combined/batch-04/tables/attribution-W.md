# Attribution: W

Descriptive source measurements; cProfile values are profiled measurements and are not converted to plain wall seconds.

cprofile wall: n=5, median=18.884807 s, min=18.675092 s, max=22.031384 s.

## Stages

Self and inclusive medians are sums within each trial; missing inclusive data is unknown. Parent names are reported as recorded.

| Stage | Parent | Count median | Self s | Inclusive s |
| --- | --- | ---: | ---: | ---: |

## cProfile: Self

Shares are medians of each function’s share of its own profiled run total. Cumulative shares overlap and cannot be summed.

| Function | Calls median | Self s | Cumulative s | Self share | Cumulative share |
| --- | ---: | ---: | ---: | ---: | ---: |
| ~:0(<built-in method _hashlib.openssl_sha256>) | 13305.000000 | 4.641986 | 4.641986 | 24.53% | 24.53% |
| ~:0(<method 'poll' of 'select.poll' objects>) | 16.000000 | 2.204361 | 2.204361 | 11.48% | 11.48% |
| ~:0(<method 'read' of '_io.BufferedReader' objects>) | 13677.000000 | 0.690481 | 0.690812 | 3.73% | 3.74% |
| ~:0(<method 'update' of '_hashlib.HASH' objects>) | 66071.000000 | 0.501815 | 0.501815 | 2.69% | 2.69% |
| /usr/local/lib/python3.13/copy.py:119(deepcopy) | 294486.000000 | 0.299533 | 0.742844 | 1.57% | 4.01% |
| /usr/local/lib/python3.13/pathlib/_local.py:257(_parse_path) | 83801.000000 | 0.279675 | 0.499233 | 1.52% | 2.71% |
| ~:0(<built-in method builtins.isinstance>) | 1818978.000000 | 0.274677 | 0.369412 | 1.48% | 1.99% |
| /usr/local/lib/python3.13/pathlib/_local.py:117(__init__) | 214733.000000 | 0.245230 | 0.384225 | 1.33% | 2.08% |
| ~:0(<built-in method builtins.exec>) | 1354.000000 | 0.224024 | 18.505400 | 1.23% | 100.11% |
| ~:0(<built-in method posix.lstat>) | 136233.000000 | 0.177886 | 0.177886 | 0.96% | 0.96% |
| <frozen posixpath>:388(realpath) | 15417.000000 | 0.176871 | 0.602001 | 0.96% | 3.26% |
| ~:0(<built-in method posix.stat>) | 44810.000000 | 0.174778 | 0.407292 | 0.93% | 2.21% |
| /usr/local/lib/python3.13/json/decoder.py:351(raw_decode) | 208.000000 | 0.183457 | 0.183969 | 0.91% | 0.91% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:145(need_more_tokens) | 284829.000000 | 0.166132 | 0.286334 | 0.89% | 1.55% |
| ~:0(<method 'set_default_verify_paths' of '_ssl._SSLContext' objects>) | 33.000000 | 0.184493 | 0.184493 | 0.87% | 0.87% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:1270(scan_plain) | 17524.000000 | 0.147568 | 0.459903 | 0.80% | 2.46% |
| ~:0(<built-in method _io.open>) | 21162.000000 | 0.145954 | 0.261777 | 0.79% | 1.42% |
| /usr/local/lib/python3.13/pathlib/_abc.py:130(with_segments) | 165268.000000 | 0.144015 | 0.662908 | 0.78% | 3.58% |
| ~:0(<built-in method builtins.len>) | 874118.000000 | 0.146413 | 0.185840 | 0.78% | 0.99% |
| ~:0(<built-in method sys.intern>) | 610048.000000 | 0.142279 | 0.142279 | 0.77% | 0.77% |
| /usr/local/lib/python3.13/pathlib/_local.py:498(__init__) | 200150.000000 | 0.144049 | 0.508987 | 0.76% | 2.72% |
| ~:0(<method 'readinto' of '_io.BufferedReader' objects>) | 17644.000000 | 0.138866 | 0.138866 | 0.75% | 0.75% |
| /usr/local/lib/python3.13/pathlib/_local.py:289(drive) | 154232.000000 | 0.136976 | 0.836345 | 0.74% | 4.54% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:113(check_token) | 173501.000000 | 0.131992 | 1.314204 | 0.72% | 7.02% |
| ~:0(<built-in method builtins.id>) | 415335.000000 | 0.130219 | 0.130219 | 0.71% | 0.71% |
| /usr/local/lib/python3.13/pathlib/_local.py:227(__str__) | 201092.000000 | 0.131676 | 0.719848 | 0.71% | 3.91% |
| /usr/local/lib/python3.13/pathlib/_local.py:174(_str_normcase) | 225304.000000 | 0.126218 | 0.303431 | 0.69% | 1.64% |
| ~:0(<method 'get' of 'dict' objects>) | 756688.000000 | 0.121775 | 0.121918 | 0.65% | 0.65% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:99(forward) | 174594.000000 | 0.120806 | 0.141811 | 0.64% | 0.75% |
| ~:0(<built-in method marshal.loads>) | 831.000000 | 0.115803 | 0.115803 | 0.63% | 0.63% |
| /usr/local/lib/python3.13/pathlib/_local.py:365(relative_to) | 26330.000000 | 0.113372 | 1.489926 | 0.62% | 8.09% |
| /usr/local/lib/python3.13/pathlib/_local.py:44(__getitem__) | 72779.000000 | 0.093556 | 0.614569 | 0.50% | 3.32% |
| ~:0(<method 'append' of 'list' objects>) | 525362.000000 | 0.089353 | 0.089353 | 0.49% | 0.49% |
| /usr/local/lib/python3.13/copy.py:218(_deepcopy_dict) | 27165.000000 | 0.087282 | 0.673282 | 0.47% | 3.65% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:87(peek) | 703532.000000 | 0.087259 | 0.089243 | 0.47% | 0.48% |
| ~:0(<method 'recv_into' of '_socket.socket' objects>) | 57.000000 | 0.084982 | 0.084982 | 0.47% | 0.47% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:156(fetch_more_tokens) | 34689.000000 | 0.084916 | 0.942416 | 0.46% | 5.04% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:279(stale_possible_simple_keys) | 295675.000000 | 0.086159 | 0.086159 | 0.46% | 0.46% |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/parser.py:273(parse_node) | 22851.000000 | 0.083222 | 0.371546 | 0.46% | 2.03% |
| /usr/local/lib/python3.13/pathlib/_local.py:193(__eq__) | 107761.000000 | 0.083369 | 0.387852 | 0.45% | 2.11% |

## cProfile: Cumulative

Shares are medians of each function’s share of its own profiled run total. Cumulative shares overlap and cannot be summed.

| Function | Calls median | Self s | Cumulative s | Self share | Cumulative share |
| --- | ---: | ---: | ---: | ---: | ---: |
| ~:0(<built-in method builtins.next>) | 9975.000000 | 0.003455 | 18.920543 | 0.02% | 102.24% |
| ~:0(<built-in method builtins.exec>) | 1354.000000 | 0.224024 | 18.505400 | 1.23% | 100.11% |
| /root/codex/plan-81m/attribution-evidence.env/bin/astrid:1(<module>) | 1.000000 | 0.000015 | 18.505358 | 0.00% | 100.11% |
| /root/codex/plan-81m/a4-agent/astrid/console.py:70(main) | 1.000000 | 0.000015 | 18.462795 | 0.00% | 99.81% |
| /root/codex/plan-81m/a4-agent/astrid/core/gateway/__init__.py:72(main) | 1.000000 | 0.000015 | 18.428403 | 0.00% | 99.54% |
| /root/codex/plan-81m/a4-agent/astrid/core/gateway/__init__.py:105(_main_impl) | 1.000000 | 0.000007 | 18.428381 | 0.00% | 99.54% |
| /root/codex/plan-81m/a4-agent/astrid/core/gateway/dispatch.py:82(_dispatch_generate) | 1.000000 | 0.000016 | 18.428374 | 0.00% | 99.54% |
| /usr/local/lib/python3.13/contextlib.py:145(__exit__) | 83.000000 | 0.000219 | 18.409477 | 0.00% | 99.41% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:952(main) | 1.000000 | 0.000028 | 18.403783 | 0.00% | 99.35% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/command_timing.py:79(timing_scope) | 2.000000 | 0.000025 | 18.343792 | 0.00% | 99.00% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/command_timing.py:50(close) | 1.000000 | 0.000023 | 18.334166 | 0.00% | 98.95% |
| /usr/local/lib/python3.13/threading.py:1059(join) | 1.000000 | 0.000014 | 18.333322 | 0.00% | 98.95% |
| ~:0(<method 'join' of '_thread._ThreadHandle' objects>) | 1.000000 | 0.000123 | 18.287757 | 0.00% | 98.70% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:968(_main_with_errors) | 1.000000 | 0.000028 | 18.286888 | 0.00% | 98.70% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:586(_main) | 1.000000 | 0.000009 | 18.285059 | 0.00% | 98.68% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:617(_main_request) | 1.000000 | 0.000009 | 18.285049 | 0.00% | 98.68% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:468(_workflow_command) | 1.000000 | 0.000056 | 18.285042 | 0.00% | 98.68% |
| /root/codex/plan-81m/a4-agent/astrid/core/generation/cli.py:525(generate) | 1.000000 | 0.000024 | 16.420688 | 0.00% | 87.85% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:588(call) | 2.000000 | 0.000083 | 16.420651 | 0.00% | 87.85% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:1473(workflow) | 2.000000 | 0.000216 | 16.416455 | 0.00% | 87.82% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:1623(_generate_on_target) | 1.000000 | 0.000096 | 10.574433 | 0.00% | 56.19% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/generation.py:1653(_generate_on_target_impl) | 1.000000 | 0.000569 | 10.253314 | 0.00% | 54.12% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/workflow_bundle.py:3234(emit_bundle) | 1.000000 | 0.000142 | 6.712555 | 0.00% | 35.50% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:308(_resolve_class_type) | 556.000000 | 0.003091 | 5.661458 | 0.02% | 29.68% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/entrypoints.py:185(emit_scratchpad_python) | 2.000000 | 0.000073 | 5.536838 | 0.00% | 29.39% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/entrypoints.py:35(emit_canonical_python) | 2.000000 | 0.000069 | 5.527069 | 0.00% | 29.33% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/emit_ready.py:804(emit_ready_template_python) | 2.000000 | 0.000204 | 5.526891 | 0.00% | 29.33% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:197(_sync_reader) | 2226.000000 | 0.036538 | 5.594604 | 0.19% | 29.33% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/emit_ready.py:849(_emit_ready_template_python_inner) | 2.000000 | 0.000924 | 5.526610 | 0.00% | 29.33% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/generation.py:85(cache_file_witness) | 9256.000000 | 0.062575 | 5.577375 | 0.34% | 29.30% |
| ~:0(<built-in method builtins.any>) | 20406.000000 | 0.022254 | 5.307567 | 0.12% | 28.01% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/widgets/compact_resolver.py:150(compact_widget_names_for_node) | 254.000000 | 0.003741 | 5.218029 | 0.02% | 27.13% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/widgets/compact_resolver.py:312(_candidate_name_sources) | 254.000000 | 0.004553 | 5.187715 | 0.02% | 26.98% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:220(<genexpr>) | 6605.000000 | 0.023237 | 4.874598 | 0.12% | 25.55% |
| /usr/local/lib/python3.13/contextlib.py:82(inner) | 10.000000 | 0.000342 | 4.514333 | 0.00% | 24.71% |
| /root/codex/plan-81m/a4-agent/astrid/core/pack/discovery.py:366(discover_pack_metadata) | 10.000000 | 0.002137 | 4.509502 | 0.01% | 24.69% |
| ~:0(<built-in method _hashlib.openssl_sha256>) | 13305.000000 | 4.641986 | 4.641986 | 24.53% | 24.53% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/client.py:391(open_from_launcher) | 2.000000 | 0.000098 | 3.622418 | 0.00% | 19.50% |
| /root/codex/plan-81m/a4-agent/astrid/sdk/autobootstrap.py:426(ensure_runtime) | 2.000000 | 0.002209 | 3.585400 | 0.01% | 19.28% |
| /root/codex/plan-81m/VibeComfy/vibecomfy/workflow_bundle.py:1581(_canonicalize_for_v2_pair) | 1.000000 | 0.000189 | 3.801044 | 0.00% | 19.10% |

