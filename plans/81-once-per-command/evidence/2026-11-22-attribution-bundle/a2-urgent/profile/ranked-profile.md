# A-2 urgent source cProfile: one measured process per route

One cProfile sample per route, with profiling overhead. Self and cumulative seconds below are measured inside the profiled process; cumulative rows overlap. cProfile starts after interpreter and profiler bootstrap and does not directly explain all startup or process-exit seconds. The exact collector span is unavailable; the sum of exclusive timing rows is its available proxy. Outer wall minus that sum is an external residual including clock rounding and profiling/exit overhead, not an identified stage. Optional py-spy follows CLI subprocesses but does not follow the already-running Runtime/host and excludes idle threads by default.
Applicability labels are inferred from cited source code, not measured as a source-vs-installed comparison. The timings and cProfile rows are source-run observations. The timed pack host source identity stage is `both`: astrid/sdk/host_bootstrap.py:2142,2171-2175 executes that stage in installed mode too, which also adds the verifier at astrid/core/source_identity.py:102-124. `both` means shared code, not equal timing. `unknown` means installed applicability is not established by this evidence. No installed savings are inferred; the separately reported 4.397 s cache_file_witness digest-call total is not classified source-only.

## W

Outer spawn-to-exit 17.868030 s; Runtime response emission 17.590598 s; target response emission 23.005974 s; timing start: process start; exact collector span unavailable; sum of exclusive timing rows 17.597350 s; estimated external residual 0.270680 s. Task `667a5cd241cc437cab29273cc0c6c8b4`, target prompt `slot-2`. Raw: [W-cprofile-1.prof.gz](W-cprofile-1.prof.gz), [W-cprofile-1.stdout](W-cprofile-1.stdout).

| Stage | Parent | Self s | Inclusive s | Code applicability (inferred) |
| --- | --- | ---: | ---: | --- |
| other command work | — | 8.939881 | unknown | unknown; aggregated collector remainder at astrid/sdk/command_timing.py:64 |
| pack discovery | — | 2.550129 | 2.550129 | both; inferred: astrid/core/pack/discovery.py:366 |
| Runtime launcher connection | — | 0.887747 | 0.887747 | both; inferred: astrid/sdk/client.py:392-410,469-471 |
| Runtime launcher connection | — | 0.872952 | 0.872952 | both; inferred: astrid/sdk/client.py:392-410,469-471 |
| workflow build | — | 0.780428 | 0.780428 | both; inferred: astrid/sdk/generation.py:470,1900-1976 |
| pack host attachment | — | 0.485509 | 0.722325 | both; inferred: astrid/sdk/autobootstrap.py:524 |
| model registry | — | 0.168942 | 0.563164 | both; inferred: astrid/sdk/generation.py:623-626 |
| pack host attachment | — | 0.282120 | 0.519221 | both; inferred: astrid/sdk/autobootstrap.py:524 |
| pack host source identity | pack host attachment | 0.228815 | 0.228815 | both; inferred: astrid/sdk/host_bootstrap.py:2142,2171-2175; installed verifier also at astrid/core/source_identity.py:102-124 |
| pack host source identity | pack host attachment | 0.228642 | 0.228642 | both; inferred: astrid/sdk/host_bootstrap.py:2142,2171-2175; installed verifier also at astrid/core/source_identity.py:102-124 |
| pack discovery | — | 0.220894 | 0.220894 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.219222 | 0.219222 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.219185 | 0.219185 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.204772 | 0.204772 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | model registry | 0.197665 | 0.197665 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | model registry | 0.196557 | 0.196557 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.193408 | 0.193408 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.191651 | 0.191651 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.178442 | 0.178442 | both; inferred: astrid/core/pack/discovery.py:366 |
| interpreter start | — | 0.066851 | 0.066851 | unknown; generic collector only, astrid/sdk/command_timing.py:140-168 |
| gateway imports | — | 0.032627 | 0.032627 | unknown; generic collector only, astrid/sdk/command_timing.py:140-168 |
| command dispatch | — | 0.022385 | 0.022385 | unknown; generic collector only, astrid/sdk/command_timing.py:140-168 |
| Runtime GET /v1/capabilities | — | 0.015100 | 0.015100 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/projects/c0f02561ddfd40af8a6e77916b5d1671/objects | — | 0.013571 | 0.013571 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/projects/c0f02561ddfd40af8a6e77916b5d1671/objects | — | 0.012238 | 0.012238 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/projects/c0f02561ddfd40af8a6e77916b5d1671/objects | — | 0.011029 | 0.011029 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A8b1cf94eab664e9154306eb1722c5651afe811a07a4fb29742804018ab26ea62 | — | 0.010880 | 0.010880 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/app-state/user/generation | — | 0.010318 | 0.010318 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/tasks | — | 0.009805 | 0.009805 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/health | — | 0.008491 | 0.008491 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3Ad891577a457ba00c19e2668d82f4c846abd3997803ef089b6cfdc33630e50edb | — | 0.008482 | 0.008482 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| target check | — | 0.008408 | 0.008408 | both; inferred: astrid/sdk/generation.py:884,1825-1900 |
| Runtime GET /v1/objects/sha256%3Ad891577a457ba00c19e2668d82f4c846abd3997803ef089b6cfdc33630e50edb | — | 0.008282 | 0.008282 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| pack host readiness | pack host attachment | 0.008224 | 0.008224 | both; inferred: astrid/sdk/host_bootstrap.py:2230-2241 |
| Runtime GET /v1/app-state/user/generation | — | 0.008156 | 0.008156 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| pack host readiness | pack host attachment | 0.008089 | 0.008089 | both; inferred: astrid/sdk/host_bootstrap.py:2230-2241 |
| Runtime GET /v1/objects/sha256%3A8b1cf94eab664e9154306eb1722c5651afe811a07a4fb29742804018ab26ea62 | — | 0.008034 | 0.008034 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/app-state/user/generation | — | 0.007937 | 0.007937 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3Ad891577a457ba00c19e2668d82f4c846abd3997803ef089b6cfdc33630e50edb | — | 0.007561 | 0.007561 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/handshake | — | 0.007448 | 0.007448 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A3eb9cef2866c0186fbe30172701f112b35e574cf3c6575c6e4a6b5dd1e76a403 | — | 0.007230 | 0.007230 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A8b1cf94eab664e9154306eb1722c5651afe811a07a4fb29742804018ab26ea62 | — | 0.007184 | 0.007184 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A3eb9cef2866c0186fbe30172701f112b35e574cf3c6575c6e4a6b5dd1e76a403 | — | 0.007091 | 0.007091 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/handshake | — | 0.006787 | 0.006787 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/app-state/user/generation | — | 0.006732 | 0.006732 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/health | — | 0.006708 | 0.006708 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A3eb9cef2866c0186fbe30172701f112b35e574cf3c6575c6e4a6b5dd1e76a403 | — | 0.006627 | 0.006627 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/projects/c0f02561ddfd40af8a6e77916b5d1671 | — | 0.006535 | 0.006535 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime acquisition lock | — | 0.000767 | 0.000796 | both; inferred: astrid/sdk/autobootstrap.py:463-465 |
| Runtime acquisition lock | — | 0.000561 | 0.000586 | both; inferred: astrid/sdk/autobootstrap.py:463-465 |
| pack host lifecycle lock | pack host attachment | 0.000084 | 0.000084 | both; inferred: astrid/sdk/host_bootstrap.py:2241 |
| pack host lifecycle lock | pack host attachment | 0.000062 | 0.000062 | both; inferred: astrid/sdk/host_bootstrap.py:2241 |
| target check | — | 0.000050 | 0.000050 | both; inferred: astrid/sdk/generation.py:884,1825-1900 |
| in-process Runtime acquisition lock | Runtime acquisition lock | 0.000029 | 0.000029 | both; inferred: astrid/sdk/autobootstrap.py:465 |
| in-process Runtime acquisition lock | Runtime acquisition lock | 0.000024 | 0.000024 | both; inferred: astrid/sdk/autobootstrap.py:465 |

### cProfile Self

Per-function applicability is `unknown`: this evidence has source-checkout profiles only and no matched installed profile. The function file and line are the code citation; 4.397 s from cache_file_witness is a separate digest-call observation, not proof of source-only behavior.

| Function | Calls | Self s | Cumulative s | Code applicability (inferred) |
| --- | ---: | ---: | ---: | --- |
| ~:0(<built-in method _hashlib.openssl_sha256>) | 13305 | 4.471179 | 4.471179 | unknown; installed applicability unverified |
| ~:0(<method 'poll' of 'select.poll' objects>) | 14 | 1.776500 | 1.776500 | unknown; installed applicability unverified |
| ~:0(<method 'read' of '_io.BufferedReader' objects>) | 13677 | 0.663406 | 0.664036 | unknown; installed applicability unverified |
| ~:0(<method 'update' of '_hashlib.HASH' objects>) | 65994 | 0.518680 | 0.518680 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/copy.py:119(deepcopy) | 294486 | 0.287431 | 0.708195 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:257(_parse_path) | 83545 | 0.265738 | 0.481257 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.isinstance>) | 1817903 | 0.264401 | 0.351393 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:117(__init__) | 214187 | 0.235166 | 0.368526 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.exec>) | 1354 | 0.217389 | 17.567125 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.compile>) | 740 | 0.203213 | 0.203213 | unknown; installed applicability unverified |
| ~:0(<built-in method posix.lstat>) | 136224 | 0.171040 | 0.171040 | unknown; installed applicability unverified |
| <frozen posixpath>:388(realpath) | 15416 | 0.169280 | 0.588633 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/json/decoder.py:351(raw_decode) | 210 | 0.162572 | 0.163065 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:145(need_more_tokens) | 284829 | 0.160140 | 0.283907 | unknown; installed applicability unverified |
| ~:0(<method 'set_default_verify_paths' of '_ssl._SSLContext' objects>) | 33 | 0.146862 | 0.146862 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:1270(scan_plain) | 17524 | 0.146729 | 0.464076 | unknown; installed applicability unverified |
| ~:0(<built-in method posix.stat>) | 44468 | 0.144638 | 0.356421 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.len>) | 873267 | 0.139133 | 0.177756 | unknown; installed applicability unverified |
| ~:0(<built-in method sys.intern>) | 607708 | 0.138356 | 0.138356 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_abc.py:130(with_segments) | 164721 | 0.136801 | 0.626031 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:498(__init__) | 199604 | 0.132898 | 0.475099 | unknown; installed applicability unverified |
| ~:0(<method 'readinto' of '_io.BufferedReader' objects>) | 17622 | 0.132255 | 0.132255 | unknown; installed applicability unverified |
| ~:0(<built-in method _io.open>) | 21146 | 0.130456 | 0.237787 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:289(drive) | 153280 | 0.130301 | 0.788111 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:113(check_token) | 173501 | 0.127938 | 1.305678 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.id>) | 415335 | 0.126290 | 0.126290 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:174(_str_normcase) | 225199 | 0.123543 | 0.302602 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:227(__str__) | 200522 | 0.119658 | 0.685784 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:99(forward) | 174594 | 0.118225 | 0.138873 | unknown; installed applicability unverified |
| ~:0(<method 'get' of 'dict' objects>) | 756798 | 0.115784 | 0.115933 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:365(relative_to) | 26319 | 0.107583 | 1.418399 | unknown; installed applicability unverified |
| ~:0(<built-in method marshal.loads>) | 792 | 0.103590 | 0.103590 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:279(stale_possible_simple_keys) | 295675 | 0.089798 | 0.089798 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:44(__getitem__) | 72744 | 0.086634 | 0.582225 | unknown; installed applicability unverified |
| ~:0(<method 'append' of 'list' objects>) | 524836 | 0.085968 | 0.085968 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:87(peek) | 703532 | 0.084161 | 0.086317 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:156(fetch_more_tokens) | 34689 | 0.082809 | 0.939667 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:193(__eq__) | 107714 | 0.081602 | 0.386066 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/parser.py:273(parse_node) | 22851 | 0.081292 | 0.358994 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/copy.py:218(_deepcopy_dict) | 27165 | 0.080514 | 0.642194 | unknown; installed applicability unverified |

### cProfile Cumulative

Per-function applicability is `unknown`: this evidence has source-checkout profiles only and no matched installed profile. The function file and line are the code citation; 4.397 s from cache_file_witness is a separate digest-call observation, not proof of source-only behavior.

| Function | Calls | Self s | Cumulative s | Code applicability (inferred) |
| --- | ---: | ---: | ---: | --- |
| ~:0(<built-in method builtins.next>) | 9975 | 0.003365 | 17.979747 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.exec>) | 1354 | 0.217389 | 17.567125 | unknown; installed applicability unverified |
| /root/codex/plan-81m/run/a2-console/astrid:1(<module>) | 1 | 0.000007 | 17.567099 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/console.py:77(entrypoint) | 1 | 0.000005 | 17.532446 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/console.py:82(main) | 1 | 0.000020 | 17.532441 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/gateway/__init__.py:72(main) | 1 | 0.000014 | 17.499483 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/gateway/__init__.py:111(_main_impl) | 1 | 0.000004 | 17.499457 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/gateway/dispatch.py:82(_dispatch_generate) | 1 | 0.000011 | 17.499453 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/contextlib.py:145(__exit__) | 83 | 0.000236 | 17.482607 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:953(main) | 1 | 0.000042 | 17.477098 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/command_timing.py:96(timing_scope) | 2 | 0.000018 | 17.416535 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/command_timing.py:67(close) | 1 | 0.000024 | 17.406731 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/threading.py:1059(join) | 1 | 0.000011 | 17.405798 | unknown; installed applicability unverified |
| ~:0(<method 'join' of '_thread._ThreadHandle' objects>) | 1 | 0.000089 | 17.361693 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:973(_main_with_errors) | 1 | 0.000023 | 17.360919 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:587(_main) | 1 | 0.000007 | 17.359178 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:618(_main_request) | 1 | 0.000009 | 17.359167 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:469(_workflow_command) | 1 | 0.000043 | 17.359158 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:526(generate) | 1 | 0.000021 | 15.681443 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:588(call) | 2 | 0.000078 | 15.681414 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:1473(workflow) | 2 | 0.000197 | 15.677562 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:1623(_generate_on_target) | 1 | 0.000102 | 10.212348 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:1653(_generate_on_target_impl) | 1 | 0.000589 | 9.852554 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/workflow_bundle.py:3234(emit_bundle) | 1 | 0.000103 | 6.336623 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:308(_resolve_class_type) | 556 | 0.002935 | 5.365395 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/generation.py:85(cache_file_witness) | 9256 | 0.054447 | 5.301016 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:197(_sync_reader) | 2226 | 0.032275 | 5.299388 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/entrypoints.py:185(emit_scratchpad_python) | 2 | 0.000070 | 5.234155 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/entrypoints.py:35(emit_canonical_python) | 2 | 0.000072 | 5.224735 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/emit_ready.py:804(emit_ready_template_python) | 2 | 0.000184 | 5.224580 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/emit_ready.py:849(_emit_ready_template_python_inner) | 2 | 0.000831 | 5.224309 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.any>) | 20406 | 0.022674 | 5.063354 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/widgets/compact_resolver.py:150(compact_widget_names_for_node) | 254 | 0.003664 | 4.927645 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/widgets/compact_resolver.py:312(_candidate_name_sources) | 254 | 0.004752 | 4.899161 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:220(<genexpr>) | 6605 | 0.020098 | 4.630987 | unknown; installed applicability unverified |
| ~:0(<built-in method _hashlib.openssl_sha256>) | 13305 | 4.471179 | 4.471179 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/contextlib.py:82(inner) | 10 | 0.000327 | 4.372776 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/pack/discovery.py:366(discover_pack_metadata) | 10 | 0.002063 | 4.371018 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/workflow_bundle.py:1581(_canonicalize_for_v2_pair) | 1 | 0.000200 | 3.377817 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/pack/discovery.py:779(discover_packs_ordered) | 4 | 0.000056 | 3.140384 | unknown; installed applicability unverified |

## I

Outer spawn-to-exit 17.308840 s; Runtime response emission 17.017210 s; target response emission 26.779669 s; timing start: process start; exact collector span unavailable; sum of exclusive timing rows 17.027645 s; estimated external residual 0.281195 s. Task `8c65945786164e2eb0c419cb2bf04117`, target prompt `slot-4`. Raw: [I-cprofile-1.prof.gz](I-cprofile-1.prof.gz), [I-cprofile-1.stdout](I-cprofile-1.stdout).

| Stage | Parent | Self s | Inclusive s | Code applicability (inferred) |
| --- | --- | ---: | ---: | --- |
| other command work | — | 7.847107 | unknown | unknown; aggregated collector remainder at astrid/sdk/command_timing.py:64 |
| model registry | — | 0.241574 | 2.750212 | both; inferred: astrid/sdk/generation.py:623-626 |
| pack discovery | model registry | 2.311332 | 2.311332 | both; inferred: astrid/core/pack/discovery.py:366 |
| workflow build | — | 1.238530 | 1.889664 | both; inferred: astrid/sdk/generation.py:470,1900-1976 |
| Runtime launcher connection | — | 0.878195 | 0.878195 | both; inferred: astrid/sdk/client.py:392-410,469-471 |
| pack host attachment | — | 0.519868 | 0.761307 | both; inferred: astrid/sdk/autobootstrap.py:524 |
| pack discovery | — | 0.278907 | 0.278907 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.235037 | 0.235037 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack host source identity | pack host attachment | 0.233214 | 0.233214 | both; inferred: astrid/sdk/host_bootstrap.py:2142,2171-2175; installed verifier also at astrid/core/source_identity.py:102-124 |
| pack discovery | workflow build | 0.231046 | 0.231046 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.217154 | 0.217154 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.210717 | 0.210717 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.209074 | 0.209074 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.207010 | 0.207010 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | workflow build | 0.203973 | 0.203973 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | workflow build | 0.203096 | 0.203096 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.202803 | 0.202803 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.202524 | 0.202524 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.202300 | 0.202300 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.202280 | 0.202280 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.200173 | 0.200173 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | model registry | 0.197306 | 0.197306 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.196264 | 0.196264 | both; inferred: astrid/core/pack/discovery.py:366 |
| interpreter start | — | 0.076130 | 0.076130 | unknown; generic collector only, astrid/sdk/command_timing.py:140-168 |
| gateway imports | — | 0.034457 | 0.034457 | unknown; generic collector only, astrid/sdk/command_timing.py:140-168 |
| command dispatch | — | 0.024011 | 0.024011 | unknown; generic collector only, astrid/sdk/command_timing.py:140-168 |
| pack discovery | — | 0.019142 | 0.019142 | both; inferred: astrid/core/pack/discovery.py:366 |
| Runtime GET /v1/capabilities | — | 0.017204 | 0.017204 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/projects/c0f02561ddfd40af8a6e77916b5d1671/objects | — | 0.013403 | 0.013403 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/projects/c0f02561ddfd40af8a6e77916b5d1671/objects | workflow build | 0.012980 | 0.012980 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/tasks | — | 0.010553 | 0.010553 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| entry discovery | — | 0.010189 | 0.010189 | both; inferred: astrid/sdk/generation.py:1744-1745 |
| Runtime GET /v1/objects/sha256%3Abad6d33473d91ec6f5eb0104ad0378d0333e747144e2a7321d830bb783d414c7 | — | 0.009789 | 0.009789 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/projects/c0f02561ddfd40af8a6e77916b5d1671/objects | — | 0.009784 | 0.009784 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A38619f12ed94d488302dd517980065603bba4afe3534523a2d0c3adacd2a4f7e | — | 0.008627 | 0.008627 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/projects/c0f02561ddfd40af8a6e77916b5d1671 | — | 0.008324 | 0.008324 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| target check | — | 0.008315 | 0.008315 | both; inferred: astrid/sdk/generation.py:884,1825-1900 |
| pack host readiness | pack host attachment | 0.008183 | 0.008183 | both; inferred: astrid/sdk/host_bootstrap.py:2230-2241 |
| Runtime GET /v1/app-state/user/generation | — | 0.008112 | 0.008112 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/handshake | — | 0.008061 | 0.008061 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/app-state/user/generation | — | 0.007867 | 0.007867 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/app-state/user/generation | — | 0.007750 | 0.007750 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A38619f12ed94d488302dd517980065603bba4afe3534523a2d0c3adacd2a4f7e | — | 0.007694 | 0.007694 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/health | — | 0.007576 | 0.007576 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A38619f12ed94d488302dd517980065603bba4afe3534523a2d0c3adacd2a4f7e | — | 0.006761 | 0.006761 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A2681be6d911fee60c7dc4d1a5db38df31c2455dbcc5fe30dfea4e31b870f8587 | — | 0.006731 | 0.006731 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A2681be6d911fee60c7dc4d1a5db38df31c2455dbcc5fe30dfea4e31b870f8587 | — | 0.006730 | 0.006730 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A2681be6d911fee60c7dc4d1a5db38df31c2455dbcc5fe30dfea4e31b870f8587 | — | 0.006437 | 0.006437 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3Abad6d33473d91ec6f5eb0104ad0378d0333e747144e2a7321d830bb783d414c7 | — | 0.006385 | 0.006385 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3Abad6d33473d91ec6f5eb0104ad0378d0333e747144e2a7321d830bb783d414c7 | — | 0.006133 | 0.006133 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime acquisition lock | — | 0.000723 | 0.000754 | both; inferred: astrid/sdk/autobootstrap.py:463-465 |
| pack host lifecycle lock | pack host attachment | 0.000043 | 0.000043 | both; inferred: astrid/sdk/host_bootstrap.py:2241 |
| target check | workflow build | 0.000039 | 0.000039 | both; inferred: astrid/sdk/generation.py:884,1825-1900 |
| in-process Runtime acquisition lock | Runtime acquisition lock | 0.000031 | 0.000031 | both; inferred: astrid/sdk/autobootstrap.py:465 |

### cProfile Self

Per-function applicability is `unknown`: this evidence has source-checkout profiles only and no matched installed profile. The function file and line are the code citation; 4.397 s from cache_file_witness is a separate digest-call observation, not proof of source-only behavior.

| Function | Calls | Self s | Cumulative s | Code applicability (inferred) |
| --- | ---: | ---: | ---: | --- |
| ~:0(<built-in method _hashlib.openssl_sha256>) | 10440 | 4.335779 | 4.335779 | unknown; installed applicability unverified |
| ~:0(<method 'poll' of 'select.poll' objects>) | 7 | 0.887941 | 0.887941 | unknown; installed applicability unverified |
| ~:0(<method 'update' of '_hashlib.HASH' objects>) | 107948 | 0.867411 | 0.867411 | unknown; installed applicability unverified |
| ~:0(<method 'read' of '_io.BufferedReader' objects>) | 10977 | 0.634457 | 0.634633 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/copy.py:119(deepcopy) | 374611 | 0.368184 | 0.908312 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:257(_parse_path) | 78593 | 0.268213 | 0.491822 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.isinstance>) | 1807973 | 0.253346 | 0.327247 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:117(__init__) | 219367 | 0.247340 | 0.386506 | unknown; installed applicability unverified |
| ~:0(<method 'readinto' of '_io.BufferedReader' objects>) | 28836 | 0.225365 | 0.225365 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.exec>) | 1351 | 0.219040 | 16.989869 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/json/decoder.py:351(raw_decode) | 175 | 0.168534 | 0.168746 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.len>) | 975356 | 0.167048 | 0.213545 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.id>) | 513120 | 0.164208 | 0.164208 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:145(need_more_tokens) | 312120 | 0.158103 | 0.274536 | unknown; installed applicability unverified |
| ~:0(<built-in method posix.stat>) | 43216 | 0.154024 | 0.375438 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_abc.py:130(with_segments) | 176010 | 0.150046 | 0.685915 | unknown; installed applicability unverified |
| <frozen posixpath>:388(realpath) | 13297 | 0.149864 | 0.512240 | unknown; installed applicability unverified |
| ~:0(<built-in method posix.lstat>) | 117623 | 0.149461 | 0.149461 | unknown; installed applicability unverified |
| ~:0(<built-in method _io.open>) | 23085 | 0.147669 | 0.257399 | unknown; installed applicability unverified |
| ~:0(<built-in method sys.intern>) | 598474 | 0.144616 | 0.144616 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:174(_str_normcase) | 263544 | 0.143225 | 0.300227 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:498(__init__) | 208142 | 0.141907 | 0.507719 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:1270(scan_plain) | 19186 | 0.139795 | 0.447327 | unknown; installed applicability unverified |
| ~:0(<method 'get' of 'dict' objects>) | 917852 | 0.133033 | 0.133121 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:113(check_token) | 190287 | 0.128115 | 1.285280 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:289(drive) | 133244 | 0.125450 | 0.788421 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:99(forward) | 205174 | 0.123166 | 0.146205 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:365(relative_to) | 28091 | 0.122342 | 1.734621 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/pack/discovery.py:91(visit) | 16632 | 0.121375 | 3.094499 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/copy.py:218(_deepcopy_dict) | 37646 | 0.119523 | 0.861059 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/hashlib.py:195(file_digest) | 12564 | 0.119319 | 1.220162 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:227(__str__) | 221408 | 0.117462 | 0.641651 | unknown; installed applicability unverified |
| ~:0(<built-in method marshal.loads>) | 831 | 0.108811 | 0.108811 | unknown; installed applicability unverified |
| ~:0(<method 'set_default_verify_paths' of '_ssl._SSLContext' objects>) | 26 | 0.108018 | 0.108018 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:44(__getitem__) | 87335 | 0.107651 | 0.733164 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:193(__eq__) | 123887 | 0.094487 | 0.391902 | unknown; installed applicability unverified |
| ~:0(<method 'append' of 'list' objects>) | 557173 | 0.088529 | 0.088529 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:237(_format_parsed_parts) | 160914 | 0.086760 | 0.155612 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:87(peek) | 777411 | 0.086154 | 0.087725 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:279(stale_possible_simple_keys) | 323911 | 0.083988 | 0.083988 | unknown; installed applicability unverified |

### cProfile Cumulative

Per-function applicability is `unknown`: this evidence has source-checkout profiles only and no matched installed profile. The function file and line are the code citation; 4.397 s from cache_file_witness is a separate digest-call observation, not proof of source-only behavior.

| Function | Calls | Self s | Cumulative s | Code applicability (inferred) |
| --- | ---: | ---: | ---: | --- |
| ~:0(<built-in method builtins.exec>) | 1351 | 0.219040 | 16.989869 | unknown; installed applicability unverified |
| /root/codex/plan-81m/run/a2-console/astrid:1(<module>) | 1 | 0.000009 | 16.989827 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/console.py:77(entrypoint) | 1 | 0.000006 | 16.953129 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/console.py:82(main) | 1 | 0.000022 | 16.953124 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.next>) | 10376 | 0.002892 | 16.936443 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/gateway/__init__.py:72(main) | 1 | 0.000016 | 16.918286 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/gateway/__init__.py:111(_main_impl) | 1 | 0.000005 | 16.918256 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/gateway/dispatch.py:82(_dispatch_generate) | 1 | 0.000012 | 16.918251 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/contextlib.py:145(__exit__) | 71 | 0.000195 | 16.897365 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:953(main) | 1 | 0.000039 | 16.894274 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/command_timing.py:96(timing_scope) | 2 | 0.000046 | 16.831141 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/command_timing.py:67(close) | 1 | 0.000010 | 16.819654 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/threading.py:1059(join) | 1 | 0.000019 | 16.772776 | unknown; installed applicability unverified |
| ~:0(<method 'join' of '_thread._ThreadHandle' objects>) | 1 | 0.000225 | 16.772150 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:973(_main_with_errors) | 1 | 0.000004 | 16.769952 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:587(_main) | 1 | 0.000011 | 16.769948 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:618(_main_request) | 1 | 0.000074 | 16.769933 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:588(call) | 2 | 0.000156 | 15.059619 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:2290(image) | 1 | 0.000021 | 15.055762 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:2323(_media_request) | 1 | 0.000020 | 15.055733 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:2330(_media_request_impl) | 1 | 0.000069 | 15.055713 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:1623(_generate_on_target) | 1 | 0.000090 | 12.289215 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:1653(_generate_on_target_impl) | 1 | 0.000550 | 11.976817 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/workflow_bundle.py:3234(emit_bundle) | 1 | 0.000221 | 6.277689 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/contextlib.py:82(inner) | 17 | 0.000555 | 5.712424 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/pack/discovery.py:366(discover_pack_metadata) | 17 | 0.003791 | 5.709683 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/entrypoints.py:185(emit_scratchpad_python) | 2 | 0.000068 | 5.471040 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/entrypoints.py:35(emit_canonical_python) | 2 | 0.000070 | 5.461979 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/emit_ready.py:804(emit_ready_template_python) | 2 | 0.000224 | 5.461833 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/emit/emit_ready.py:849(_emit_ready_template_python_inner) | 2 | 0.000913 | 5.461508 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:308(_resolve_class_type) | 556 | 0.002797 | 5.419085 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:197(_sync_reader) | 2226 | 0.034226 | 5.408561 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/generation.py:85(cache_file_witness) | 9236 | 0.060927 | 5.339255 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.any>) | 18665 | 0.023676 | 5.045904 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/widgets/compact_resolver.py:150(compact_widget_names_for_node) | 254 | 0.003873 | 5.033591 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/widgets/compact_resolver.py:312(_candidate_name_sources) | 254 | 0.004696 | 5.004535 | unknown; installed applicability unverified |
| /root/codex/plan-81m/VibeComfy/vibecomfy/porting/object_info/consume.py:220(<genexpr>) | 6675 | 0.023477 | 4.719954 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/command_timing.py:247(timed_call) | 6 | 0.000110 | 4.677856 | unknown; installed applicability unverified |
| ~:0(<built-in method _hashlib.openssl_sha256>) | 10440 | 4.335779 | 4.335779 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/model_catalog/registry.py:105(load_default) | 2 | 0.000156 | 3.348378 | unknown; installed applicability unverified |

## E

Outer spawn-to-exit 32.502096 s; Runtime response emission 32.212040 s; target response emission 41.792982 s; timing start: process start; exact collector span unavailable; sum of exclusive timing rows 32.220534 s; estimated external residual 0.281562 s. Task `78e526a44d8d458992e1adebc8bd0879`, target prompt `slot-6`. Raw: [E-cprofile-1.prof.gz](E-cprofile-1.prof.gz), [E-cprofile-1.stdout](E-cprofile-1.stdout).

| Stage | Parent | Self s | Inclusive s | Code applicability (inferred) |
| --- | --- | ---: | ---: | --- |
| entry lookup | — | 2.544009 | 17.315278 | both; inferred: astrid/sdk/generation.py:1066,1731-1751 |
| other command work | — | 7.522665 | unknown | unknown; aggregated collector remainder at astrid/sdk/command_timing.py:64 |
| model registry | entry lookup | 0.367862 | 4.611599 | both; inferred: astrid/sdk/generation.py:623-626 |
| entry lookup | — | 0.000775 | 2.397758 | both; inferred: astrid/sdk/generation.py:1066,1731-1751 |
| pack discovery | entry lookup | 2.396983 | 2.396983 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | entry lookup | 2.158025 | 2.158025 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | model registry | 2.150842 | 2.150842 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | entry lookup | 2.135584 | 2.135584 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | model registry | 2.092895 | 2.092895 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | entry lookup | 2.069026 | 2.069026 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | entry lookup | 1.923734 | 1.923734 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | entry lookup | 1.873302 | 1.873302 | both; inferred: astrid/core/pack/discovery.py:366 |
| workflow build | — | 0.976533 | 1.597568 | both; inferred: astrid/sdk/generation.py:470,1900-1976 |
| Runtime launcher connection | — | 0.938305 | 0.938305 | both; inferred: astrid/sdk/client.py:392-410,469-471 |
| pack host attachment | — | 0.368552 | 0.592554 | both; inferred: astrid/sdk/autobootstrap.py:524 |
| pack discovery | — | 0.241003 | 0.241003 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.217891 | 0.217891 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack host source identity | pack host attachment | 0.215913 | 0.215913 | both; inferred: astrid/sdk/host_bootstrap.py:2142,2171-2175; installed verifier also at astrid/core/source_identity.py:102-124 |
| pack discovery | — | 0.214202 | 0.214202 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.212395 | 0.212395 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.209370 | 0.209370 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.207501 | 0.207501 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | workflow build | 0.206142 | 0.206142 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | — | 0.202905 | 0.202905 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | workflow build | 0.202126 | 0.202126 | both; inferred: astrid/core/pack/discovery.py:366 |
| pack discovery | workflow build | 0.199696 | 0.199696 | both; inferred: astrid/core/pack/discovery.py:366 |
| interpreter start | — | 0.094308 | 0.094308 | unknown; generic collector only, astrid/sdk/command_timing.py:140-168 |
| gateway imports | — | 0.039380 | 0.039380 | unknown; generic collector only, astrid/sdk/command_timing.py:140-168 |
| command dispatch | — | 0.028628 | 0.028628 | unknown; generic collector only, astrid/sdk/command_timing.py:140-168 |
| Runtime GET /v1/capabilities | — | 0.014944 | 0.014944 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/projects/c0f02561ddfd40af8a6e77916b5d1671/objects | workflow build | 0.013032 | 0.013032 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/projects/c0f02561ddfd40af8a6e77916b5d1671/objects | — | 0.012793 | 0.012793 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/projects/c0f02561ddfd40af8a6e77916b5d1671/objects | — | 0.011917 | 0.011917 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A90935c7ec57c50743f72e73e3a1ae5dd61ddd6069317eb5041bf7c29c0f6ff48 | — | 0.009828 | 0.009828 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A90935c7ec57c50743f72e73e3a1ae5dd61ddd6069317eb5041bf7c29c0f6ff48 | — | 0.009690 | 0.009690 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3A90935c7ec57c50743f72e73e3a1ae5dd61ddd6069317eb5041bf7c29c0f6ff48 | — | 0.009249 | 0.009249 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/app-state/user/generation | — | 0.009084 | 0.009084 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3Adcbd2285751cba8d7cc33a60c4dd455878c384798da679c7a9eb96f7559b6cae | — | 0.008766 | 0.008766 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/health | — | 0.008732 | 0.008732 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/tasks | — | 0.008495 | 0.008495 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3Adcbd2285751cba8d7cc33a60c4dd455878c384798da679c7a9eb96f7559b6cae | — | 0.008259 | 0.008259 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| target check | — | 0.008244 | 0.008244 | both; inferred: astrid/sdk/generation.py:884,1825-1900 |
| Runtime GET /v1/app-state/user/generation | — | 0.008227 | 0.008227 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3Abad6d33473d91ec6f5eb0104ad0378d0333e747144e2a7321d830bb783d414c7 | — | 0.008144 | 0.008144 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| pack host readiness | pack host attachment | 0.007989 | 0.007989 | both; inferred: astrid/sdk/host_bootstrap.py:2230-2241 |
| Runtime GET /v1/objects/sha256%3Abad6d33473d91ec6f5eb0104ad0378d0333e747144e2a7321d830bb783d414c7 | — | 0.007953 | 0.007953 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/app-state/user/generation | — | 0.007795 | 0.007795 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3Adcbd2285751cba8d7cc33a60c4dd455878c384798da679c7a9eb96f7559b6cae | — | 0.007549 | 0.007549 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/objects/sha256%3Abad6d33473d91ec6f5eb0104ad0378d0333e747144e2a7321d830bb783d414c7 | — | 0.007289 | 0.007289 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime GET /v1/projects/c0f02561ddfd40af8a6e77916b5d1671 | — | 0.007195 | 0.007195 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| Runtime POST /v1/handshake | — | 0.007062 | 0.007062 | both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540 |
| entry lookup | — | 0.006968 | 0.006968 | both; inferred: astrid/sdk/generation.py:1066,1731-1751 |
| Runtime acquisition lock | — | 0.000505 | 0.000574 | both; inferred: astrid/sdk/autobootstrap.py:463-465 |
| pack host lifecycle lock | pack host attachment | 0.000099 | 0.000099 | both; inferred: astrid/sdk/host_bootstrap.py:2241 |
| in-process Runtime acquisition lock | Runtime acquisition lock | 0.000069 | 0.000069 | both; inferred: astrid/sdk/autobootstrap.py:465 |
| entry lookup | — | 0.000064 | 0.000064 | both; inferred: astrid/sdk/generation.py:1066,1731-1751 |
| target check | workflow build | 0.000039 | 0.000039 | both; inferred: astrid/sdk/generation.py:884,1825-1900 |

### cProfile Self

Per-function applicability is `unknown`: this evidence has source-checkout profiles only and no matched installed profile. The function file and line are the code citation; 4.397 s from cache_file_witness is a separate digest-call observation, not proof of source-only behavior.

| Function | Calls | Self s | Cumulative s | Code applicability (inferred) |
| --- | ---: | ---: | ---: | --- |
| ~:0(<built-in method _hashlib.openssl_sha256>) | 13904 | 4.668022 | 4.668022 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:145(need_more_tokens) | 2167645 | 1.106146 | 1.946118 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:1270(scan_plain) | 133228 | 1.063467 | 3.334496 | unknown; installed applicability unverified |
| ~:0(<method 'poll' of 'select.poll' objects>) | 7 | 0.945692 | 0.945692 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:113(check_token) | 1319076 | 0.907040 | 9.126904 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:99(forward) | 1265127 | 0.821046 | 0.963086 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.isinstance>) | 5759869 | 0.758541 | 1.126928 | unknown; installed applicability unverified |
| ~:0(<method 'read' of '_io.BufferedReader' objects>) | 14371 | 0.717701 | 0.718038 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:279(stale_possible_simple_keys) | 2251323 | 0.603631 | 0.603631 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:87(peek) | 5362750 | 0.601215 | 0.612752 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:156(fetch_more_tokens) | 265382 | 0.581465 | 6.593625 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/parser.py:273(parse_node) | 174810 | 0.579081 | 2.526806 | unknown; installed applicability unverified |
| ~:0(<method 'update' of '_hashlib.HASH' objects>) | 71972 | 0.576087 | 0.576087 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:1311(scan_plain_spaces) | 189900 | 0.565213 | 1.255825 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:114(get_mark) | 698363 | 0.400740 | 0.507173 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:752(scan_to_next_token) | 265382 | 0.388556 | 0.851688 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.len>) | 2744196 | 0.367618 | 0.418893 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:63(compose_node) | 174810 | 0.353568 | 12.678724 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:257(_parse_path) | 104384 | 0.334542 | 0.610179 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:264(next_possible_simple_key) | 1985941 | 0.314150 | 0.314150 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_local.py:117(__init__) | 264886 | 0.299951 | 0.472816 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/parser.py:94(check_event) | 528924 | 0.291785 | 11.502008 | unknown; installed applicability unverified |
| ~:0(<built-in method posix.lstat>) | 253538 | 0.286273 | 0.286273 | unknown; installed applicability unverified |
| <frozen posixpath>:388(realpath) | 27133 | 0.285249 | 0.908739 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/copy.py:119(deepcopy) | 283146 | 0.267225 | 0.675741 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/jsonschema/validators.py:396(descend) | 98226 | 0.260487 | 2.341305 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:545(fetch_value) | 72809 | 0.254058 | 0.501040 | unknown; installed applicability unverified |
| ~:0(<method 'append' of 'list' objects>) | 1510560 | 0.241836 | 0.241836 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.exec>) | 1374 | 0.228708 | 32.172387 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/reader.py:94(prefix) | 565930 | 0.220233 | 0.292639 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:135(get_token) | 375103 | 0.216164 | 0.619944 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:88(compose_scalar_node) | 146681 | 0.206224 | 0.522348 | unknown; installed applicability unverified |
| ~:0(<method 'get' of 'dict' objects>) | 1236861 | 0.203629 | 0.203734 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/jsonschema/validators.py:339(evolve) | 102435 | 0.200955 | 0.433985 | unknown; installed applicability unverified |
| ~:0(<built-in method posix.stat>) | 60235 | 0.188430 | 0.436622 | unknown; installed applicability unverified |
| ~:0(<built-in method sys.intern>) | 804686 | 0.182156 | 0.182156 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/resolver.py:143(resolve) | 174810 | 0.179557 | 0.274816 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:1416(scan_line_break) | 354540 | 0.176378 | 0.326667 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/pathlib/_abc.py:130(with_segments) | 209417 | 0.171794 | 0.800402 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/scanner.py:295(save_possible_simple_key) | 152234 | 0.169663 | 0.286139 | unknown; installed applicability unverified |

### cProfile Cumulative

Per-function applicability is `unknown`: this evidence has source-checkout profiles only and no matched installed profile. The function file and line are the code citation; 4.397 s from cache_file_witness is a separate digest-call observation, not proof of source-only behavior.

| Function | Calls | Self s | Cumulative s | Code applicability (inferred) |
| --- | ---: | ---: | ---: | --- |
| ~:0(<built-in method builtins.next>) | 70702 | 0.015664 | 32.289560 | unknown; installed applicability unverified |
| ~:0(<built-in method builtins.exec>) | 1374 | 0.228708 | 32.172387 | unknown; installed applicability unverified |
| /root/codex/plan-81m/run/a2-console/astrid:1(<module>) | 1 | 0.000010 | 32.172349 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/console.py:77(entrypoint) | 1 | 0.000008 | 32.127526 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/console.py:82(main) | 1 | 0.000025 | 32.127518 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/gateway/__init__.py:72(main) | 1 | 0.000018 | 32.087659 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/gateway/__init__.py:111(_main_impl) | 1 | 0.000006 | 32.087626 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/gateway/dispatch.py:82(_dispatch_generate) | 1 | 0.000012 | 32.087620 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/contextlib.py:145(__exit__) | 95 | 0.000242 | 32.062727 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:953(main) | 1 | 0.000045 | 32.059034 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/command_timing.py:96(timing_scope) | 2 | 0.000037 | 31.985837 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/command_timing.py:67(close) | 1 | 0.000006 | 31.963823 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/threading.py:1059(join) | 1 | 0.000004 | 31.963810 | unknown; installed applicability unverified |
| ~:0(<method 'join' of '_thread._ThreadHandle' objects>) | 1 | 0.000086 | 31.963806 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:973(_main_with_errors) | 1 | 0.000029 | 31.963587 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:587(_main) | 1 | 0.000013 | 31.963510 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/cli.py:618(_main_request) | 1 | 0.000106 | 31.963414 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/command_timing.py:247(timed_call) | 8 | 0.000148 | 21.326022 | unknown; installed applicability unverified |
| /usr/local/lib/python3.13/contextlib.py:82(inner) | 18 | 0.000663 | 18.915482 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/pack/discovery.py:366(discover_pack_metadata) | 18 | 0.004390 | 18.911027 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/entries.py:962(resolve_entry_inputs) | 2 | 0.000014 | 17.314961 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/entries.py:818(resolve_entry_inputs) | 2 | 0.000044 | 17.314947 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/entries.py:941(describe_entry) | 3 | 0.000028 | 17.314680 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/pack/loader.py:466(load_pack_manifest) | 96 | 0.003361 | 16.310675 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/pack/canonical.py:951(validate_canonical_pack) | 96 | 0.003241 | 16.098376 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/pack/canonical.py:864(_admit) | 96 | 0.023353 | 15.943778 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/pack/loader.py:105(scan_packs) | 8 | 0.000258 | 14.804769 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/pack/loader.py:143(_scan_packs_locked) | 8 | 0.004956 | 14.793650 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/__init__.py:74(load) | 410 | 0.035111 | 13.345020 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/constructor.py:47(get_single_data) | 410 | 0.001009 | 13.284551 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:2282(generate) | 1 | 0.000023 | 13.025150 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:588(call) | 2 | 0.000071 | 13.024967 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:2326(_generate_resolved_media) | 1 | 0.000018 | 13.024272 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/sdk/generation.py:2330(_media_request_impl) | 1 | 0.000082 | 13.024254 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:29(get_single_node) | 410 | 0.001370 | 12.723226 | unknown; installed applicability unverified |
| /root/codex/plan-81m/profile-a2/astrid/core/generation/entries.py:549(describe_entry) | 1 | 0.001055 | 12.702998 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:50(compose_document) | 410 | 0.000862 | 12.683806 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:63(compose_node) | 174810 | 0.353568 | 12.678724 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/composer.py:117(compose_mapping_node) | 20635 | 0.151843 | 12.666237 | unknown; installed applicability unverified |
| /root/codex/plan-81m/attribution-evidence.env/lib/python3.13/site-packages/yaml/parser.py:94(check_event) | 528924 | 0.291785 | 11.502008 | unknown; installed applicability unverified |

