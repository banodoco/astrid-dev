# SV-3 measurement, first run: stopped at setup in repetition 1, 23 November 2026

Approved for exactly: package head `08fb5ba0d5f465a7035012396dad319656368471`, `package.sha256` digest `a7e60ad3ea0c220e439c0175400ad7e0c745df8a7f63e5b52ca3258ffcf91f06`, candidate Runtime `f2da02e1dcf02439ee149f1412310c72aa4bf0bb` (tree `533503fa4c3639faafc185c34f8be8a39b6452c4`, the SV-2 fix from Runtime PR #105; dependency and contract diff against `77c38d03` empty, `dependency-and-contract.diff` is 0 bytes). Ran once from about 15:15Z. **No drag, no save, no measurement happened.** Per the approval the run was not retried.

## What happened

- Setup passed: pristine copy and audit (`pristine-copy-audit.json`), the work copy and the rebased catalog and profile (`rep-1/rebase.json`), the candidate Runtime started from the archive on the copy (`rep-1/up.json`, `rep-1/candidate-daemon-module.json`), the preview answered health.
- The browser driver died at module load: `reused-trace-helpers.mjs` reads `P77_SV2A_TRACE_TOOLS` at import time, and the SV-3 package had dropped that variable with the trace (`rep-1/browser.log`, `TypeError ... "path" argument must be of type string. Received undefined`). A one-line package defect, not a Runtime result.
- Cleanup: idle-safe down verified (`rep-1/down.json`), ports closed (`rep-1/preview-after.json`), no leftover Chrome, boundaries unchanged (`boundary.json`; the data-root and root listings gained new top-level entries only), work copy removed. Free disk never went below 17.7 GiB (`free-kib.tsv`, stop at 16 GiB). `cleanup.json` `exit_code: 1` is the driver's stop.

## A second finding: the pack host does not poll on a copied data root

`rep-1/service-pack-host-delta.txt` (6.8 KB) is three crash loops of the retained program's supervised pack host, each ending in `FileNotFoundError: .../stack/data/runtime/discovery.json`. The retained `services.json` starts it against the installed layout (`stack/data`), not against the copied data root, so it never finds the Runtime and never runs its idle claim poll. `rep-1/pack-host.json` shows `claim_lines: 0` and `pgrep_pack_host_count: 0`. Plan 78 found that this poll is what moves the Runtime's change counter and causes `head_busy`, so a run in this layout would not have measured the condition that matters. The next package version starts a pack host of its own against the copy.
