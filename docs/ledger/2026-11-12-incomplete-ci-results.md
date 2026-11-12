Date: 2026-11-12
Kind: issue
Source: Release 13 test manager, first comparison of int/r13 against Release 12 main
Resolved by: 2026-11-12-green-skill

The per-test comparison couldn't start without hand recipes nobody had written down.
- Agent `main` unit shard 5 is cancelled at 120 minutes in every run, because `tests/sdk/test_h3_endpoint_r4.py` hits the 600 s pytest-timeout repeatedly, so it has no results at all.
- The `int/r13` Lanes workflow ran zero tests, because a setup step's inline call had been fixed in `ci.yml` but not in `lanes.yml`.
- Raw GitHub job logs carry a timestamp prefix, so `baseline-diff.py` finds no ids in them.
- The Runtime logs `-ra`, so its logs carry no passes.
- The Agent `unit` aggregate reads "skipped", not red, when a shard is cancelled.

The REST recipes for logs and dispatch were deleted in #527, and the rules contradicted each other: "never run broad suites" against "full suite on CI", and "never take on full CI health" against Plan 39. Nothing said how to get a complete picture, when to batch fixes or when to spec a project. Plan 39's strict-xfail quarantine also can't work in the Agent, whose guard fails every xfail (`tests/lanes.py`). That is left to Plan 39.
