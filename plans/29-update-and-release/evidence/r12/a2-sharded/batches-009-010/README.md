# A2 comparison: completed batches 009–010

Eight JSON receipts contain exact outcome IDs and statuses, Agent/Runtime/VibeComfy/lifecycle SHAs, Python and Node/esbuild versions and executable SHA-256 values, start/end times, exit and terminal summaries, failure-summary lines, and hashes of original receipts and full logs. Raw logs, environment, and credentials are excluded; test IDs can contain literal synthetic parameters. `failure-matches.json` compares exact summary lines; details remain in original local receipts.

Batch 009: R10 passed 226/226; R11, base and candidate each passed 220 and failed 6, with exact candidate failure summaries matching R11 and base. The any-passing-baseline rule will require triage because R10 passed these IDs. Batch 010 passed 92/92 on all four. Group boundaries restart session fixtures and can miss cross-group ordering effects, so this is not full-suite equivalent. These groups are partial evidence, not an A2 verdict.

Source manifest SHA-256: `885b264862a0e6e90698ed8a76a6b5b30e2dbeb1f3846ea96b356913b1a9e771`. Exact absent IDs, full manifest and source receipts are under `/workspace/r12-a2-resume/sharded/`. Targeted scan found no common GitHub token, OpenAI key, JWT, or long bearer-token patterns; this does not prove all possible secrets absent.
