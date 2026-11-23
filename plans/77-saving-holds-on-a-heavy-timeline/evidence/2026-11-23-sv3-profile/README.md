# SV-3 profile run: cold save and three warm saves under py-spy, 23 November 2026

Approved for exactly: package head `fd3420607cff465187376ad41bba72f42338d68e` (profile variant, `SV3_PROFILE=1`), `package.sha256` digest `87c0bca79f9880dbb5ebde5a1e5e71720afe8d0f1ef95d6a3036e7a5a0d884fb`, candidate Runtime `297863fb04ccff8f38bf968770bbe98c5ffaec68` (tree `55fdcc018b61c112d661dc75ac0fab432d0a7ea8`: SV-2, SV-2b, SV-2d and SV-2f; dependency and contract diff against `77c38d03` empty). One attempt, one repetition, 16:15Z. Exit 0; idle-safe stop verified, ports closed, no leftover Chrome, boundaries unchanged (`cleanup.json`, `boundary.json`); free disk never below 18.5 GiB (`free-kib.tsv`). The supervised pack host ran (`rep-1/pack-host.json`).

## Result

**Warm saves are no faster than the cold one, and the dominant cost is still record copying and comparison, now from two other callers.** Release-to-Saved (`summary.tsv`): cold 32.7 s, W1 21.3 s, W2 29.1 s, W3 20.5 s. All four commit POSTs answered HTTP 200 and Saved; no refusal. S0 (verified-head read after the cold start): status 200, page writable in 7.2 s (`s0` in `rep-1/browser-sv3-measure.json`). py-spy 0.4.1 attached to the Runtime process (PID in `rep-1/candidate-daemon-module.json`) for all four saves at 100 Hz with threads, 0 sampling errors (`profile-attach-summary.json`); one speedscope file per save in `rep-1/`.

Seconds on the request thread that ran the commit (the sample set is every sample whose stack holds a `timeline_commit*` frame on the one non-main thread with the most such samples; `analyze-groups.py`, output `profile-groups.txt`; each save's group is the innermost matching frame, so groups do not overlap):

| Group | cold | W1 | W2 | W3 |
| --- | --- | --- | --- | --- |
| Commit-thread seconds (about the POST-to-200 time) | 30.0 | 19.6 | 28.1 | 19.1 |
| Record copying and comparison (`value_equal`, `deepcopy`) | 17.7 | 14.2 | 18.1 | 14.4 |
| Validation, jsonschema | 2.1 | 1.5 | 2.0 | 1.7 |
| Validation, commit auth and value | 2.0 | 1.0 | 1.9 | 0.9 |
| Patch capture and payload (`_commit_patch`, `_doc_patch`, excluding the copying above) | 1.0 | 1.4 | 1.2 | 1.1 |
| JSON encode and decode | 2.9 | 0.7 | 2.5 | 0.3 |
| Old-history verification (`_verify_accepted*`) | 1.1 | 0.1 | 1.6 | 0.1 |
| SQLite | 0.7 | 0.0 | 0.3 | 0.0 |
| Not matched by the groups | 2.5 | 0.9 | 0.7 | 0.6 |

- **The proof was reused in W1 and W3** (old-history verification 0.1 s) and **not in the cold save or W2** (1.1 and 1.6 s), consistent with SV-2f keeping the proof between saves except for one slow save in the middle (W2 also had the longest commit thread, 28.1 s). Old-history verification is no longer the main cost.
- **Record copying and comparison is 72 to 76 % of a warm save (14 to 18 s) and is still there after SV-2b.** The callers (`rep-1` profiles, caller of the first `value_equal`/`deepcopy` frame on the stack): `timeline_commit_auth.py:223 covers`, reached from `validate_step` (lines 399, 462 and 465, called by `validate` at `:3406`), 6.8 s in W1 and 7.5 s in W3 (about 11 s in W2); and `_doc_patch.py:157 payload`, reached from `_commit_patch.py:328 capture` (lines 402 and 408), 5.9 s in W1 and 5.4 s in W3 (6.0 s in W2). The `value_equal` calls in `timeline_commit_producer.py:62-69` that SV-2b targeted are called from those two places, not only from the producer path.
- Request-thread seconds sum to 19.6 s in W1 against a POST-to-200 of 19.0 s (the sampler's own scope includes the pointer-down to 200, so about 0.6 s more).

## Not established

- The sampler's effect on the timings was not measured (100 Hz); the earlier unprofiled run on `f2da02e1` had 17 to 23 s warm POST-to-200, this profiled run on `297863fb` had 18.7 to 27.1 s, so no speed-up from SV-2f is visible either way.
- Which of the two callers can share work with the other (both compare the same document records) is not established here.
- The burst scenarios (5 edits within 3 s, 10 within 5 s) are not part of this run; they are in a separate package branch awaiting its own approval.

## Text for the 'Saving a heavy timeline' section of `docs/speed.md` (not edited here: the file is not on `main` yet)

> **23 November 2026, SV-3 profile run on candidate `297863fb`:** on the 300-clip fixture a save takes about 20 s from POST to 200, cold or warm (release to Saved 20.5 to 32.7 s over four saves; no refusal). The proof is now reused between saves (old-history verification is 0.1 s on a warm save). About three quarters of a warm save (14 to 18 s) is copying and comparing records (`value_equal`, `deepcopy`) called from commit validation (`timeline_commit_auth.covers`) and patch capture (`_commit_patch.capture`). Receipts: `plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-23-sv3-profile/`.
