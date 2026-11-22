# PL-2 retained-run causal audit (read only)

Candidate: `88ac863600492401bc22e352999660f3d5b01020` in `worktrees/pl-2-verify`.

## Browser error audit

The retained Playwright JSON reports 50 expected passes and 14 unexpected failures, over 13m50. The 14 failure messages are assertion/predicate timeouts (including missing expected page elements, visibility/count/style/attribute mismatches, and a 5s predicate timeout). They are not reported as uncaught page exceptions. A read-only scan of all 14 retained `trace.zip` files found 45 console trace events, zero console events with error severity, zero page-error/error events, and zero occurrences of “Invalid hook call”, dispatcher, or null `useState` phrases. The raw `run.log` and `results.json` likewise contain no matching React dispatcher/null-useState error text. Thus the retained failures present as ordinary readiness/assertion failures, not recorded browser-console or page errors. This only describes captured artifacts; it cannot prove an exception was never emitted outside the retained trace events.

## Vite cache and overlap evidence

`worktrees/pl-2-verify/config/vite/vite.config.ts` does not set `cacheDir` or `root`; it configures `optimizeDeps` at lines 178 onward. Vite therefore uses its default cache directory under `node_modules/.vite`. `worktrees/pl-2-verify/node_modules` resolves to `/home/user/codex/planet84/worktrees/baseline/node_modules`, so any Vite instances rooted in these worktrees that use that default location share the physical optimizer cache.

The recorded run began at `2026-11-22T21:48:06.799Z` and lasted 830,046 ms (ended about 22:01:57Z). Process evidence captured during the run showed our dedicated Vite dev server on port 43284 and two long-lived `vite preview` processes on ports 4173 and 4175. Current process start times corroborate the previews started at 21:25:40Z and 21:33:11Z. The separate Vite dev server on port 4192 started at 22:05:12Z, after the Playwright run ended. The available run snapshots do not establish a second simultaneous Vite dev server during the test; they do establish overlapping preview servers. Preview serves built output and is not evidence by itself that a second dependency optimizer was active. Because process snapshots were not a complete continuous recording, absence of another dev server is not proven.

## Qualified conclusion

The artifacts do not contain the null-`useState`/dispatcher failure found by the separate causal probe. Shared physical `node_modules/.vite` is a credible concurrency seam if another optimizer was active, but the retained evidence does not show that it was. Treat the 14 assertions as observed failures with cause unresolved; no product attribution or rerun is made in this audit.
