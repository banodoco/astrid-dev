# A2 comparison: completed batches 013–014

Eight JSON receipts contain exact outcome IDs and statuses, Agent/Runtime/VibeComfy/lifecycle SHAs, Python and Node/esbuild versions and executable SHA-256 values, start/end times, exit and terminal summaries, failure-summary lines, and hashes of original receipts and full logs. Raw logs, environment, and credentials are excluded; test IDs can contain literal synthetic parameters. `failure-matches.json` compares exact summary lines, which can be truncated by pytest; details remain in original local receipts.

013 candidate's platform-boundary failure summary matches base, differs from R10/R11. 014 candidate, base and R11 each have four identical failure-summary lines, while R10 passed those IDs; all four have three skips. The any-passing-baseline rule requires triage. No pytest timeout was reported. Group boundaries restart session fixtures and may miss cross-group ordering effects; this is not full-suite equivalent. These groups are partial evidence, not an A2 verdict.

Source manifest SHA-256: `885b264862a0e6e90698ed8a76a6b5b30e2dbeb1f3846ea96b356913b1a9e771`. Exact absent IDs, manifest and source receipts are under `/workspace/r12-a2-resume/sharded/`. Targeted scan found no common GitHub token, OpenAI key, JWT, or long bearer-token patterns; this does not prove all possible secrets absent.
