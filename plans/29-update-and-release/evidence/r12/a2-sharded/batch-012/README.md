# A2 comparison: completed batch 012

Four JSON receipts contain exact outcome IDs and statuses, Agent/Runtime/VibeComfy/lifecycle SHAs, Python and Node/esbuild versions and executable SHA-256 values, start/end times, exit and terminal summaries, failure-summary lines, and hashes of original receipts and full logs. Raw logs, environment, and credentials are excluded; test IDs can contain literal synthetic parameters. Exact absent IDs and the source manifest live under `/workspace/r12-a2-resume/sharded/inventory/`.

R10 passed 20/20 selected IDs, R11 65/65, base 91/91 and candidate 99/99. Candidate is the authorized clean-host rerun; the previous overlapping receipt is preserved separately at `/workspace/r12-a2-resume/sharded/history/012/candidate-overlap-064646` and excluded. No pytest timeout was reported. Group boundaries restart session fixtures and may miss cross-group ordering effects; this is not full-suite equivalent. Batch 012 is partial evidence, not an A2 verdict.

Source manifest SHA-256: `885b264862a0e6e90698ed8a76a6b5b30e2dbeb1f3846ea96b356913b1a9e771`. Targeted scan found no common GitHub token, OpenAI key, JWT, or long bearer-token patterns; this does not prove all possible secrets absent.
