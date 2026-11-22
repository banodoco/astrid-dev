# Plan 77 measurement archive

This archive records synthetic local measurements collected on 2026-11-22 for Plan 77. Historical compiled opening and dispatch observations are separated from the current stock failure. The current stock run has no gesture measurement.

## Archive contents

- `historical-opening.json` contains old compiled opening timing, public head counts, and sanitized route intervals.
- `compiled-first-trace.jsonl` and `compiled-settled-trace.jsonl` preserve ordered measured event phases, timing values, framework stages, exact App, Agent, and Runtime SHAs, and outcome flags. Compiled artifact marker and served-byte comparison flags remain explicit.
- `compiled-settled-geometry.jsonl` preserves pointer and viewport geometry with fixture identity removed.
- `current-stock-failed-observed.json` contains the separate current stock failure, exact component SHAs, sanitized route intervals, and no gesture claim.
- `current-stock-restore.json` records the restore byte comparison and schema values.
- `current-stock-cleanup.json` records cleanup outcomes without local paths or port numbers.

The event traces retain monotonic millisecond values and event order. Request intervals retain start time, status, and elapsed time. Dynamic project and timeline segments and asset filenames are generalized. Free text, quoted errors, local paths, session and process identifiers, credentials, URLs, and unused keys are omitted.

## Source selection

Only source files inside the directories named in the assignment were read. Raw manifest, backup receipt, support, credential, key, environment, and signed manifest files were not opened. The optional older small-control sources were omitted. No current gesture was present in the current stock evidence.

Selected source files with original SHA-256 and byte size

- `edit-dispatch-trace/v30/compiled-opening/observed.json` — `f97c6407d1cfd8b3aac0ae13f1db13b17bed8789525c8360de2d5f4367cf6487` — 234927 bytes
- `edit-dispatch-trace/v30/compiled-dispatch/compiled-first/results.jsonl` — `30072f2c04d8efba7db92c317bf5af7e61dc10e0d755dadd81dd20e9a943cdfe` — 97486 bytes
- `edit-dispatch-trace/v30/compiled-dispatch/compiled-first/versions.json` — `c71b7604fdc6ffc271e499a534e2d19e0d45b7813043a2014840f7741393af3f` — 168 bytes
- `edit-dispatch-trace/v30/compiled-dispatch/compiled-settled/results.jsonl` — `a0fa89abb1a353946350fa6fc6ebdf466903258508e5b39f43b3756be25e6d1f` — 116573 bytes
- `edit-dispatch-trace/v30/compiled-dispatch/compiled-settled/versions.json` — `c71b7604fdc6ffc271e499a534e2d19e0d45b7813043a2014840f7741393af3f` — 168 bytes
- `edit-dispatch-trace/v30/compiled-dispatch/compiled-settled/browser-geometry.jsonl` — `d528ff5550d605e0d67ecc508bd5ea1bb92c603b1491279fe995191e0ebc808c` — 8793 bytes
- `release-current/compatibility/observed.json` — `851a7be745b718c0dfef0e62057b984255bcf05502526f49d40575b0a9e3b05d` — 467614 bytes
- `release-current/compatibility/operator-compatibility/restore-bytes.json` — `b51f68a48d1f96a1a753b44355898d076832d9d1c9ce2534fe6de834e97ec406` — 331 bytes
- `release-current/compatibility/compatibility/cleanup.json` — `43c3e7e518871e0f8fb090e37633899d89fffbabc6ac3e04558d5e8bde9a93fd` — 342 bytes

## Interpretation

Opening usability timing measures the observed local compiled preview. The first and settled compiled traces both ended without a confirmed save settlement. The settled trace records completed deferred history at pointerup and still records no timeline commit request. Current stock evidence records a failed observation without a measured gesture. All data is synthetic.
