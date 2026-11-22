# JSON report adapter

`report-to-pytest-lines.py` converts Playwright JSON reporter output and Vitest JSON reporter output into the `PASSED <node id>` / `FAILED <node id>` lines consumed by `astrid-dev/env/baseline-diff.py`. It uses the installed Playwright 1.60 JSON reporter's `suites → specs → tests` structure and Vitest 4.1 JSON reporter's `testResults → assertionResults` structure. IDs are repository-relative and whitespace-free; titles are percent-escaped so the baseline parser reads each ID intact.

Capture reports with the frameworks' built-in reporters, then adapt them:

```sh
# Playwright: configure reporter as ['json', { outputFile: 'pw.json' }]
# or use the supported PLAYWRIGHT_JSON_OUTPUT_NAME environment variable.
# Vitest: use --reporter=json --outputFile=vitest.json.
python3 run/evidence/baseline/adapter/report-to-pytest-lines.py --root "$PWD" pw.json vitest.json > tests.log
```

Use a self-baseline by converting the same report set once and passing the resulting log as both sides, for example:

```sh
astrid-baseline-diff --baseline self=tests.log --candidate tests.log --out run/evidence/baseline/self-diff
```

The adapter prints `SKIPPED <node id>` for skipped, pending, todo, or disabled test records; `baseline-diff.py` intentionally ignores those lines. A test that is absent from the JSON report also has no status line. Therefore a skipped or absent test that passed in a baseline appears in the diff's `missing` bucket. Keep the original JSON reports with the converted log, inspect every `SKIPPED` line, and compare collected test inventories across runs; do not rewrite skipped or absent tests as `PASSED`. Skipped and absent remain distinguishable in the original JSON (skipped records have an explicit status; absent records do not). The adapter exits with an error if reports contain no passed or failed cases, preventing an all-skipped or empty run from being mistaken for a valid baseline input.

Playwright flaky outcomes are emitted as `FAILED` to keep retry instability visible. Playwright global errors and Vitest file collection failures become synthetic failed IDs. For repeated IDs across supplied reports, a failure wins.

The starting baseline's Vitest commands used the default text reporter and did not retain JSON assertion reports. `vitest-text-to-pytest-lines.py` reads only completed successful logs plus their sibling `.exit` files, verifies the Vitest `Test Files` summary, and emits one `PASSED <file>::vitest-file-suite` line per named file. It deliberately does not manufacture assertion-level names absent from the raw logs. Keep this file-suite resolution distinct from assertion-level Playwright JSON lines in summaries.
