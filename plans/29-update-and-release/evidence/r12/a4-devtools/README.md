# A4 bounded DevTools capture investigation

This is local diagnostic evidence, not a repair or CI qualification. App candidate remains `e72d541de1d65bee74707ca1ae9c2d429ee2f721`; no product, candidate or CI files were changed. The exact CI failure in run `42954826041` contained a gate-owned request with a rejected `Fetch.failRequest` and no observed Playwright or internal-CDP network terminal. A rejection or frame commit is not treated as a terminal event.

The probes used Node `v24.22.1`, Playwright core `1.60.0`, and Chrome for Testing `148.0.7778.96`, revision `1223`, on a local Linux runner. The CI setup log shows that revision installed, but its versions artifact was inaccessible, so the CI launched-process version was not independently confirmed. Fixtures use loopback only. Logs contain fixed event names, numeric opaque identifiers and timestamps; the summary below contains no request data.

## Durable messages, streaming and real pagehide

`durable-stream.cjs` enables CDP Network durable messages, enables `Network.streamResourceContent` for two JSON responses, and keeps the test's pass-through interception route active. One response completes before navigation; the other sends a prefix and is deliberately held until after navigation commits. A genuine `pagehide` callback starts a keepalive request during navigation. In the successful local run:

- The completed response's exact body was collected, had a genuine `Network.loadingFinished`, and remained recoverable via `Network.getResponseBody` after navigation.
- The interrupted streaming response had a genuine `Network.loadingFailed` but its complete body was unavailable. CDP durable buffering and streaming cannot recover bytes the browser did not receive.
- The real pagehide request started after the navigation document response and reached the fixture server. This was an observed run, not a guarantee of delivery: one earlier run did not reach the server, so the reproduction waits up to three seconds and fails if the assertion is not met.

`Fetch.takeResponseBodyAsStream` does not preserve the original stream as-is: its CDP documentation requires canceling the intercepted request or supplying a replacement body. It therefore cannot be assumed to preserve streaming behavior.

## Independent CDP session

`dual-session.cjs` adds a separately enabled Network session, with durable buffering, alongside Playwright's own session. It generates background requests and performs 200 reloads while aborting intercepted API requests. A test-only instrumented bundle maps the same browser request ID to a collision-checked numeric digest in both sessions; raw IDs and request data are not logged.

The original run had 454 actual rejected abort commands: all had real terminal events on both sessions, and there were zero independent-only terminals. A separate reproduction had 455, also all terminal on both. These tests did **not** reproduce CI's missing internal-CDP terminal, so they do not establish whether a second session would or would not observe that particular event. Earlier preserved probes separately reproduced an interrupted streaming body and an abort command rejection crossing frame commit.

No tested mechanism handles both the missing-terminal case and an interrupted complete body while preserving genuine pagehide behavior. The scanner must continue to fail closed. A browser or DevTools mechanism that demonstrably preserves the original stream and reports actual request termination would require separate proof; no pin change or scope waiver is implied.

## Reproduce

Run from this directory using a disposable scratch directory. These commands download an exact npm package and its Playwright-pinned browser; browser OS dependencies may be required. The first probe uses the pristine bundle; only the second uses the test-only instrumented copy. Do not run these probes against real services.

```bash
TASK_PROBE_DIR="$(mktemp -d)"
mkdir -p "$TASK_PROBE_DIR/pw" "$TASK_PROBE_DIR/browsers"
npm pack playwright-core@1.60.0 --ignore-scripts --silent --pack-destination "$TASK_PROBE_DIR"
tar -xzf "$TASK_PROBE_DIR/playwright-core-1.60.0.tgz" -C "$TASK_PROBE_DIR/pw" --strip-components=1
PLAYWRIGHT_BROWSERS_PATH="$TASK_PROBE_DIR/browsers" node "$TASK_PROBE_DIR/pw/cli.js" install chromium --no-shell
TASK_PROBE_CORE="$TASK_PROBE_DIR/pw" TASK_PROBE_BROWSER="$TASK_PROBE_DIR/browsers/chromium-1223/chrome-linux64/chrome" node durable-stream.cjs
python3 instrument.py "$TASK_PROBE_DIR/pw/lib/coreBundle.js"
python3 prepare-dual.py "$TASK_PROBE_DIR/pw/lib/coreBundle.js"
TASK_PROBE_CORE="$TASK_PROBE_DIR/pw" TASK_PROBE_BROWSER="$TASK_PROBE_DIR/browsers/chromium-1223/chrome-linux64/chrome" node dual-session.cjs > "$TASK_PROBE_DIR/dual.out" 2> "$TASK_PROBE_DIR/dual.log"
cat "$TASK_PROBE_DIR/dual.out"
python3 analyze-dual.py "$TASK_PROBE_DIR/dual.log"
```

The 1.60.0 unmodified `lib/coreBundle.js` SHA-256 was `f74353fcb8e406756a70a6af0dfc4a5069acd577e35ec9d923ccf36ac009c2f5`. The instrumentation modifies a temporary npm bundle and is not a candidate change. Timing, error counts, and pagehide delivery may vary; a failed or truncated probe is inconclusive rather than evidence of success.
