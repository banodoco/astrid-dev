# Final CI comparison and parser correction

Candidate run `44447425471` at `513204189161c4f72abc73e4fe7d46d7e97ac534` was compared to the union of all eight shards in base run `44378598394` at `b50371baf101d6f706269fab38cdf3a7a5eb2013`.

Shard 1 has 43 FAILED and 54 ERROR results: every complete node ID matches the base with the same status. `shard-1-full-ids.json` records the exact IDs and log line references. Across shards 2–8, the full-ID comparison found the same three candidate-only failures documented in `isolated-flips.md`, and no status switches. Their isolated checks were adjudicated by the host as runner-environment sensitivities; CI remains red.

## Correction to earlier evidence

The earlier report's base shard 1 gap of three arose from parsing parameterized node IDs containing spaces. Full IDs reconcile with its terminal summary. More importantly, the 33-failure gap in both candidate and base shard 6 came from `SUBFAILED(...)` entries omitted by the comparison parser, not collapsed pytest output. All 33 candidate failed subtests match the base union by parent ID and subtest parameters; `shard-6-subfailed.json` identifies each and both log locations. No other candidate shard has SUBFAILED entries. This correction supersedes the count-gap explanation in `shards-2-6-7-8.md` and `isolated-flips.md`.

Windows native, boundary and wheels for 3.11 and 3.12 passed. Darwin native, fast checks and unit shards 1–8 failed; their comparison details and the three isolated flips remain recorded in this evidence directory. No full-suite result is represented as green.
