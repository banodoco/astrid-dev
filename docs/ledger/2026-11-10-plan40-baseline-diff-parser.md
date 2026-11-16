Date: 2026-11-10
Kind: issue
Source: Plan 40 T8 integrated proof at `ef4373875ecdce570e38cb6c9d02c8923ce57605`
Resolved by: —

The first raw-log comparison treated three captured application `ERROR` lines as pytest node results, so the manager had to filter the log to actual passed/failed node lines before running the baseline comparator; that comparison then reported 0 regressions and 1 baseline failure. Update `baseline-diff.py` or its documented runner to consume only pytest node-result lines (or structured test results) so application log messages cannot become test IDs.
