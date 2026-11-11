# Direct Journey diagnostic 42932713990

The [diagnostic run](https://github.com/banodoco/astrid-app/actions/runs/42932713990) used App `ecb873300466f10c756894469cbb47349186b472`, Agent `313bbd46f1e24bfe635655d78b27ab0b321145d5`, Runtime `42ae24aff8d2cb854f874ce134161077a3ba3641`, and the existing early manifest pins. It was diagnostic only. The direct job passed; three-products had two passed, one failed and 11 skipped.

The sanitized stdout sequence for scanner 1, request 387, a GET in the app-state category, is:

| UTC time | Event | Navigation generation |
| --- | --- | --- |
| 00:40:41.260 | Gate entry and abort begin | 9 |
| 00:40:41.264 | Raw headers capture ended | 9 |
| 00:40:41.264 | Main-frame commit | 10 |
| 00:40:41.268 | Abort call ended | 10 |
| 00:40:51.234 | Drain timeout: blocked admission has no terminal event | 10 |

No response or Playwright terminal event was logged for that request before timeout. Abort completion after commit does not by itself prove the browser blocked dispatch; the scan failed closed. The event sequence supplies a concrete interleaving for a bounded repair and regression test, not an A4 pass. The restart journey was skipped. No header values, bodies, tokens or dynamic URL contents are recorded here.
