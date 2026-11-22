# Attribution: W

Descriptive source measurements; cProfile values are profiled measurements and are not converted to plain wall seconds.

timings wall: n=5, median=12.085370 s, min=11.698617 s, max=12.334390 s.

## Stages

Self and inclusive medians are sums within each trial; missing inclusive data is unknown. Parent names are reported as recorded.

| Stage | Parent | Count median | Self s | Inclusive s |
| --- | --- | ---: | ---: | ---: |
| Runtime GET /v1/app-state/user/generation | — | 4.000000 | 0.029591 | unknown |
| Runtime GET /v1/capabilities | — | 1.000000 | 0.013566 | unknown |
| Runtime GET /v1/health | — | 2.000000 | 0.013706 | unknown |
| Runtime GET /v1/objects/sha256%3A191e196e3e469c030e39ff4a2f04631ea2a15f901d8162bad0f4a33e93c614ec | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A195d9587568b8c7337dd64170c12c51b215a7e4d16ac2e7b879188902bd15996 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A353e245a3cf446db0f2fcdb1cb26471aafa58718216d75a6b2543ab8e3ef5ac3 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A3eb9cef2866c0186fbe30172701f112b35e574cf3c6575c6e4a6b5dd1e76a403 | — | 3.000000 | 0.020174 | unknown |
| Runtime GET /v1/objects/sha256%3A4243272bc8a1969ff442cb834ef17f722dc7418c867439f6fc8bb4930169eb3c | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A578a767a5c81b33d6a7670af8dbb4bbac5c741d05e124e8bcefa5ac40004b542 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A60a4bebd29fc8bb2824466078651a37c5c864cdc5e1b4dcca18e3f485172e2b1 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3A83a8c3a986cf0c0092de2dd052e6012a37305b8ba5156c3f8df06d25358435f3 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Aa24c69d7054d75b85d9013c590efaa34b5ce59c46c2fec040f64da876f47321e | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Aad3de176f1b453330775e09780576255e1c7309c18f80042d1a82ab07ac92935 | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/objects/sha256%3Af2f5173e437db3e4d3c3265cc6c189a906be7e15fa1bebf2a99cffa7d1d4898e | — | 0.000000 | 0.000000 | unknown |
| Runtime GET /v1/projects/de251aa5b7f8466aae6d95a946dea751 | — | 1.000000 | 0.007043 | unknown |
| Runtime POST /v1/handshake | — | 2.000000 | 0.013247 | unknown |
| Runtime POST /v1/projects/de251aa5b7f8466aae6d95a946dea751/objects | — | 3.000000 | 0.035295 | unknown |
| Runtime POST /v1/tasks | — | 1.000000 | 0.008896 | unknown |
| Runtime acquisition lock | — | 2.000000 | 0.000967 | unknown |
| Runtime launcher connection | — | 2.000000 | 2.052320 | unknown |
| in-process Runtime acquisition lock | — | 2.000000 | 0.000030 | unknown |
| model registry | — | 1.000000 | 0.042765 | unknown |
| other command work | — | 1.000000 | 6.686327 | unknown |
| pack discovery | — | 10.000000 | 1.817729 | unknown |
| pack host attachment | — | 2.000000 | 0.502105 | unknown |
| pack host lifecycle lock | — | 2.000000 | 0.000081 | unknown |
| pack host readiness | — | 2.000000 | 0.014979 | unknown |
| pack host source identity | — | 2.000000 | 0.271157 | unknown |
| target check | — | 2.000000 | 0.006718 | unknown |
| workflow build | — | 1.000000 | 0.329517 | unknown |

