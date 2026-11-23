# PB-4 installed comparison

Agent base b324d7c1e94713e7ae48d3d98a70db1214ef658f; Runtime 737843e9cb92c565c266452dde540832ee2c745b. Trial Agent fd9e83b0a8ce120b00605cd3fc9f9632a6390a90 differs by generator pins and generated digest witnesses. Before VibeComfy 48b5fa9e45630e1bc502651975ec0ef3a5e74c4c; after 589e542a1178b2a999d10fc4f4d9803c349587a5.

| arm | warm-up (s) | five measured seconds | median (s) | hash calls | bytes hashed | distinct files |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| before | 13.8354 | 12.0888, 12.1335, 11.8383, 11.8279, 11.8032 | 11.8383 | 6912 | 6563328600 | 3 |
| after | 9.2049 | 6.3726, 6.0844, 6.1281, 6.0739, 6.1507 | 6.1281 | 246 | 287596236 | 3 |

Median saving: 5.7102 seconds; acceptance threshold: 3 seconds.

The same sitecustomize instrumentation in both installed environments counts SHA-256 operations from object-info file witness and generation validation frames; counts include work outside emission and identify three distinct witnessed files. Timings include its overhead. Both arms used `--timings`, the stand-in ComfyUI and `--no-wait`; runtime byte/listener attestation was off as in the run block. Local branch fetch proofs, selected manifests, harness diffs, raw stderr and JSON receipts are retained.
