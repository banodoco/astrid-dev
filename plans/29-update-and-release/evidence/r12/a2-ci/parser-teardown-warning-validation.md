# A2 parser counterexamples: offline validation

Exact local source: `b4ddfb7dd9766d19526286e53cbc8768170178a6` on `handoff/r12-a2-parser-errors`; no trigger or CI. A brief coordinated host window was released after completion.

The bounded synthetic real-pytest script produced:

```text
PYTEST_FORMAT_COUNTEREXAMPLE passed; 2 IDs, pass + teardown error, known skip; exit 1
PYTEST_WARNING_COUNTEREXAMPLE passed; 1 failed ID, native final-warning heading; exit 1
```

Both underlying synthetic pytest exits are intentionally 1. Their complete structured outputs preserve failures/errors/skips, account for both statuses on the one exact teardown-error ID, and reconcile terminal totals. No raw log or reason text is uploaded. The parser accepts the one fixed known local-evidence skip reason and pytest's exact final-warning heading; warning-origin lines are ignored only when equal to an expected frozen ID inside a properly terminated warning section. Unknown repeats, skip reasons, extra status-looking lines and malformed section boundaries fail closed.

Independent bounded lightweight units passed: sanitizer 17, strict receipt guard 6, full-plan 12, prior receipts 4; total 39. No CI or heavy suite ran. These demonstrate the synthetic pytest formats, not the unretained raw output from live groups 028, 035 or 041, and do not classify their failures.
