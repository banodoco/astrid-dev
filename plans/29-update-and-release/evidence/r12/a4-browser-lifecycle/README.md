# A4 Playwright and Chromium lifecycle investigation

This is diagnostic evidence, not a proposed repair or a green release check. No product or CI code changed. The candidate examined is App `e72d541de1d65bee74707ca1ae9c2d429ee2f721`. The joined CI failure was run `42954826041`; its job setup installed Playwright Chromium and headless shell `148.0.7778.96`, revision `1223`. Its versions artifact was inaccessible, so the installed version is observed, but the actual launched process version is not independently established.

The CI lifecycle log joins the gated app-state request to a `Fetch.failRequest` call that began before frame commit and was rejected after commit. Playwright's `route.abort()` resolved, raw headers were captured, and neither a Playwright terminal event nor a CDP network terminal was recorded before timeout. The diagnostic log deliberately did not retain the protocol error text, so its rejection reason is unknown.

## Source ownership and history

- Playwright 1.60's `CRNetworkManager` owns Chromium `Fetch.failRequest`, receives `Network.loadingFailed`, and reports request failure. Its `RouteImpl.abort` invokes `catchDisallowedErrors`, which swallows generic protocol errors. This same abort/catch behavior remains in inspected 1.61 and 1.65 bundles. [Playwright v1.60 source](https://github.com/microsoft/playwright/blob/v1.60.0/packages/playwright-core/src/server/chromium/crNetworkManager.ts).
- Chromium 148's `FetchHandler::FailRequest` delegates to `DevToolsURLLoaderInterceptor::ContinueInterceptedRequest`. The interceptor can reject a missing interception job as `Invalid InterceptionId` or reject a job in an invalid state. These are possible mechanisms; the CI log does not identify its actual error. [Fetch handler](https://chromium.googlesource.com/chromium/src/+/refs/tags/148.0.7778.96/content/browser/devtools/protocol/fetch_handler.cc) and [interceptor](https://chromium.googlesource.com/chromium/src/+/refs/tags/148.0.7778.96/content/browser/devtools/devtools_url_loader_interceptor.h).
- [Playwright commit 18f21e8cb131 / PR #43730](https://github.com/microsoft/playwright/commit/18f21e8cb131) makes Chromium document detachment fail tracked in-flight requests by emitting Playwright `requestfailed`, even when no CDP loading terminal arrived. Its regression tests discuss Chromium missing `loadingFailed` across navigation. [Issue #43508](https://github.com/microsoft/playwright/issues/43508) concerns response-body promises cut off by navigation. A lifecycle-inferred `requestfailed` is not a genuine CDP terminal and cannot satisfy this task's stated terminal requirement.
- Chromium [commit a8156242fd5e](https://github.com/chromium/chromium/commit/a8156242fd5e) fixes a request hanging when `Fetch.disable` arrives during asynchronous interception preparation. The scanner keeps an interception route active during this navigation and the CI trace had already seen a paused request; this is not evidence that the fix applies.

## Local comparisons

All tests used local-only loopback fixtures, Node `v24.22.1`, and instrumented copies of npm Playwright bundles. Browser pairs were the bundled headless-shell builds:

| Playwright core | Chromium headless shell | Streaming body across commit | Abort after commit |
| --- | --- | --- | --- |
| 1.60.0 | 148.0.7778.96, revision 1223 | `response.text()` unavailable | Playwright abort resolved; CDP rejected with local classification `Invalid InterceptionId` |
| 1.61.0 | 149.0.7827.55, revision 1228 | unavailable | same |
| 1.65.0 | 158.0.8127.18, revision 1254 | unavailable | same |

The abort-after-commit fixture deliberately waits until commit before calling abort. It reproduces a stale route and its swallowed rejection; it does **not** reproduce the CI command already in flight before commit.

The joined stress fixture starts repeated background fetches, aborts intercepted requests immediately, and performs 35 reload attempts. In one run, 1.60 had 50 rejected aborts, 33 overlapping an observed frame commit at millisecond resolution, with none of those 33 missing a CDP terminal. 1.61 had 59 rejected, 41 overlapping commit, none of those 41 missing a CDP terminal. A 1.65 run had 20 rejected, 11 overlapping commit; all 11 lacked a CDP terminal but had a Playwright `requestfailed`. That 1.65 run recorded one navigation error. Counts vary with timing. The browser and Playwright versions both change between rows, and the local probe is not the CI journey; none of these results proves what caused the CI missing terminal.

An earlier 1.60 stress run of 1,000 reloads had 1,078 rejected aborts, 868 overlapping commit, and no missing CDP terminal among those overlapping requests. A separate 1.60 real pagehide keepalive probe held the request across commit: abort succeeded, a terminal event arrived, and the request did not reach the server. A barrier or policy that treats every late request as the same lifecycle category is therefore not justified.

No supported-version comparison establishes a behavior-preserving fix while the scanner requires a genuine terminal and complete observed bodies. A version bump that treats 1.65's inferred terminal as genuine would weaken that condition. The gate and checks should remain fail-closed pending a sound ordering or evidence mechanism.

## Reproduce locally

Use a disposable directory, Node, Python 3, network access to the npm and Playwright download registries, and no credentials. The scripts only generate loopback traffic and log fixed events, numeric opaque IDs, and times. Instrumentation is test-only and modifies a disposable Playwright bundle, not the application. Save console logs only in a private scratch directory; results may vary and navigation errors are counted explicitly.

```bash
TASK_PROBE_DIR="$(mktemp -d)"
mkdir -p "$TASK_PROBE_DIR/pw" "$TASK_PROBE_DIR/browsers"
npm pack playwright-core@1.65.0 --ignore-scripts --silent --pack-destination "$TASK_PROBE_DIR"
tar -xzf "$TASK_PROBE_DIR/playwright-core-1.65.0.tgz" -C "$TASK_PROBE_DIR/pw" --strip-components=1
PLAYWRIGHT_BROWSERS_PATH="$TASK_PROBE_DIR/browsers" node "$TASK_PROBE_DIR/pw/cli.js" install chromium-headless-shell
python3 instrument.py "$TASK_PROBE_DIR/pw/lib/coreBundle.js"
TASK_PROBE_CORE="$TASK_PROBE_DIR/pw" TASK_PROBE_BROWSER="$TASK_PROBE_DIR/browsers/chromium_headless_shell-1254/chrome-headless-shell-linux64/chrome-headless-shell" node compare-probe.cjs > "$TASK_PROBE_DIR/compare.out" 2> "$TASK_PROBE_DIR/compare.log"
TASK_PROBE_CORE="$TASK_PROBE_DIR/pw" TASK_PROBE_BROWSER="$TASK_PROBE_DIR/browsers/chromium_headless_shell-1254/chrome-headless-shell-linux64/chrome-headless-shell" node joined-stress.cjs > "$TASK_PROBE_DIR/stress.out" 2> "$TASK_PROBE_DIR/stress.log"
python3 analyze.py "$TASK_PROBE_DIR/stress.log"
```

Run from the directory containing these scripts. To compare 1.60.0 or 1.61.0, replace the package version and browser revision with `1223` or `1228`, respectively. The `pagehide-probe.cjs` fixture can also be run with the same environment variables, but its held-route behavior is timing-dependent and may require an external timeout. Treat a timed-out probe as inconclusive. Browser installations may require OS dependencies.

Playwright npm tarball SHA-256 values checked locally: 1.61.0 `b5ab14f09f3aaacdedbc2cb1431b0552cec8995fba35d841779a4ed535ce0200`; 1.65.0 `315247c55a793ca760b2f05bdcee0e6a53fd65b1f22d1d3de8323c8c9395add3`. The pinned 1.60.0 `lib/coreBundle.js` SHA-256 was `f74353fcb8e406756a70a6af0dfc4a5069acd577e35ec9d923ccf36ac009c2f5`.
