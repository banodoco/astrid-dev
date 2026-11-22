# F-2 canonical YAML counts — 22 November 2026

A count-only scratch observer ran one fresh workflow (W) and one image (I) CLI against the source fixture, with Agent `2ec9c24123a69916fe726023e2eede4c3386b1ce`, Runtime `182311f9d363712c0339254bd27e091d0e18318d` and VibeComfy `799d90f619a6723d0b376b7e77aef09c244a0821`. Each command succeeded with one Runtime admission and one target acknowledgement; teardown returned zero. No elapsed timing was recorded.

| Route | Direct canonical YAML loads | Distinct paths | Repeated path loads |
| --- | ---: | ---: | ---: |
| W | 42 | 42 | 0 |
| I | 42 | 42 | 0 |

W had 11 discovery fingerprints, 33 tree fingerprints, 12 active-source inventory calls and 10 other discovery deepcopies; I had 18, 54, 18 and 17 respectively. The observer's per-discovery breakdown was empty, so these totals do not establish the per-hit split. An earlier explicit-entry (E) profile counted 336 direct canonical parses over 42 paths; that is a different route. Under the host's W threshold of roughly 20 repeated canonical parses, this observed W result does not support building the parse store; the simple repeat-parse bound is zero for this observation. This single source-fixture observation does not establish all routes or installed behavior.

Raw count-only artifacts are in `run/f2-counts/attempt-3/` on the run host. The first two scratch-observer attempts failed before yielding counts; their diagnostic manifests were retained. No YAML content or credentials were recorded.
