# Fixed-head installed comparison

VibeComfy A 48b5fa9e45630e1bc502651975ec0ef3a5e74c4c; B f9790674e0fc9610a51f4f3567fc1b59ef01128c. Agent baseline b324d7c1e94713e7ae48d3d98a70db1214ef658f; trial f2dd143457d7b36158e1d96af1c84ece405131df with generated generator pin witnesses. Runtime 737843e9cb92c565c266452dde540832ee2c745b.

| arm | warm-up s | measured seconds | median s | object-info SHA calls | bytes | distinct files |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| A | 13.8354 | 12.0888, 12.1335, 11.8383, 11.8279, 11.8032 | 11.8383 | 6912 | 6563328600 | 3 |
| B | 8.3789 | 5.9418, 5.7641, 5.5131, 6.0272, 5.8287 | 5.8287 | 246 | 287596236 | 3 |

Median saving: 6.0096 s (required >= 3 s). A samples are preserved from the previous run as directed; B is a fresh install and fresh run on the same box. Identical object-info SHA instrumentation was used in both arms; counts include work outside emission and instrumentation overhead is included in timings. Stand-in ComfyUI, --no-wait and --timings; Runtime byte/listener attestation off.
