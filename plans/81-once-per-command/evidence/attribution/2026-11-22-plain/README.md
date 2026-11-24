# Plain CPU source baseline — 22 November 2026

Command from the evidence checkout, at harness commit `34d962f4`:

```sh
plans/81-once-per-command/evidence/attribution/launcher.sh /tmp/a4-launcher-plain-five --trials 5 --modes plain > /tmp/a4-launcher-plain-five.log 2>&1
python3 plans/81-once-per-command/evidence/attribution/rank.py /tmp/a4-launcher-plain-five/manifest.json --output /tmp/a4-plain-tables
```

The shell wrapper held `/tmp/astrid-timing.lock` throughout startup, warmups, trials, drain and teardown. The runner returned 0. Re-running the rank command in a second output directory produced byte-identical tables. `manifest.json` contains the pinned clean revisions, executable and console SHA-256, interpreter, packages, CPU and load, source and host identity, seed, redacted argv, per-trial stdout/stderr names, task and target IDs, timestamps, status and teardown status. `target-inventory.json` is the attached stand-in's advertised inventory; each `*.target.json` records its accepted graph. Loopback authorities and scratch paths in streams and argv were redacted. The runner log contains all 18 accepted trial labels. Raw means per-process results, not unredacted local authority material.

Each route has one warmup followed by five measured fresh console processes. Median wall (range) was W **12.082 s** (11.660–12.559), I **11.567 s** (11.028–12.080), E **15.425 s** (15.135–16.520). Median spawn to Runtime response emission was W/I/E 11.852/11.356/15.207 s; median spawn to target response emission was 17.246/21.195/24.966 s. The target is a CPU validation stand-in and the response hooks add overhead. These times do not measure a GPU or installed Astrid, and this run has no stage, import, function or sampling attribution. It predates A-1–A-3 and the planned fixes.
