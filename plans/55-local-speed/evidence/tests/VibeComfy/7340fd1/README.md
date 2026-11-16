# Corrected VibeComfy bridge baseline comparison

This comparison uses the worker's Plan 55 integration baseline and the independent exact candidate run.

## Inputs and provenance

- Raw baseline: `/workspace/scratch/6ee41b0f0cca/run/ls5-bridge-baseline.log`. The worker reports this was run at integration base `c59d6999b244fd94a01559ff1c0b0eeb8f079dc2`, tree `e036602549eca52eb60cc8b3bef5c0598ecb4d5b` (Plan 55 integration, not Release 13). Its final pytest short summary contains 16 passed tests.
- Raw candidate: `/workspace/scratch/6ee41b0f0cca/run/ls5-bridge-exact.log`, independently run at candidate `7340fd1b6d197b6319c5e446142ae41474259068`, tree `eabc2a3e07cef763d463b4a81325b48a0787d56d`. Its final pytest short summary contains 24 passed tests.
- The candidate identity was verified before and after the test run; the worktree stayed clean.

## Derived inputs

`/workspace/scratch/6ee41b0f0cca/run/ls5-bridge-baseline.summary.log` and `/workspace/scratch/6ee41b0f0cca/run/ls5-bridge-exact.summary.log` were created by extracting only pytest status rows after the final `short test summary info` heading. The extraction retains every `PASSED`, `FAILED`, `ERROR`, `SKIPPED`, `XFAIL`, and `XPASS` row. Both raw summaries contain only passed test rows; there were no session setup or collection errors.

## Earlier comparison correction

The first comparison at `/workspace/scratch/6ee41b0f0cca/run/baseline-vc-7340fd1/summary.md` used the wrong baseline inputs: it combined `ls5-bridge-baseline.log` with `ls5-bridge-candidate-5.log`, so its first side represented the previous 24-test candidate as well as the 16-test baseline. It also parsed captured `ERROR vibecomfy schema gate: schema validation skipped...` application log lines from passing tests as a pseudo-test, adding one to the count. The earlier 25/25 count and its `preexisting` entry are therefore invalid for the requested base-versus-candidate comparison. The raw logs were preserved unchanged.

## Corrected diff

`summary.md` here was generated with `baseline-diff.py` from the two derived status-only files: baseline 16, candidate 24; regression 0, no-baseline 0, preexisting 0, fixed 0, missing 0.
