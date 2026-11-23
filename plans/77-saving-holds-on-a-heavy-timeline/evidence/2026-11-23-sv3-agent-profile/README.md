# SV-3 (A) profile: cold and three warm saves under py-spy on Runtime `c9e535bd` with Agent PR #560, 23 November 2026

Approved for exactly: package head `8f1899f28ac1890bac408ae942945a4600a600d8`, `package.sha256` digest `1b2cf43708fc240b5785542037be6c96fa45fbcf3a7fa4bcb3ad31987666989f`, run in `SV3_PROFILE=1` mode (one repetition: S0, cold, W1, W2, W3 under py-spy 0.4.1 at 100 Hz with threads, then B5 and B10 without the sampler), candidate Runtime `c9e535bdd05f1e800dd864b5c91445c69dfacb4f` and Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` overlaid (two files; `agent-overlay.json`, `rep-1/agent-loaded.json`: `failures: []`, installed files unchanged afterwards). One attempt, 18:36Z, exit 0; idle-safe stop verified, ports closed, no leftover Chrome, boundaries unchanged; free disk never below 17.3 GiB. py-spy attached to all four saves with no errors (`profile-attach-summary.json`), one speedscope file per save in `rep-1/`.

## Timings of this repetition (release to Saved)

cold 23.2 s, W1 13.3 s, W2 13.4 s, **W3 21.9 s**; POST to 200 20.1, 11.6, 11.7 and 20.0 s. No refusal, all HTTP 200. S0: verified-head status 200, editor writable after 5.7 s. Bursts (unattached sampler): B5 5 POSTs, all 200, last edit release to Saved 58.0 s, 5 of 5 edits in the document, matches; B10 10 POSTs, all 200, 120.4 s (the driver's 120 s settle wait timed out although all POSTs had returned 200), 10 of 10 edits in the document, final start 230.900 s against 230.846 s expected (0.054 s, reported `false` at the 0.05 s tolerance).

## Seconds on the request thread of each save (`profile-groups.txt`, produced by `analyze-profile.py`)

The commit thread is the one non-main thread with the most samples whose stack holds a `timeline_commit*` frame; each sample is put in the innermost matching group (copying and comparison is split by its caller); the groups sum to the thread total.

| Group | cold | W1 | W2 | W3 |
| --- | --- | --- | --- | --- |
| Commit-thread seconds | 20.2 | 11.9 | 11.4 | 20.5 |
| Copy and compare (`value_equal`, `deepcopy`) called from `timeline_commit_auth.covers` | 8.6 | 5.7 | 5.6 | 9.0 |
| Copy and compare from other callers | 1.4 | 1.2 | 1.1 | 1.5 |
| Copy and compare from patch capture/payload | 0.04 | 0.04 | 0.04 | 0.03 |
| jsonschema validation | 1.5 | 1.7 | 1.6 | 1.4 |
| Commit auth and value validation (excluding the above) | 1.5 | 1.0 | 0.8 | 1.8 |
| Patch capture and payload (`_commit_patch`, `_doc_patch`) | 0.9 | 1.0 | 1.0 | 0.9 |
| JSON encode and decode | 2.5 | 0.7 | 0.6 | 3.2 |
| Old-history verification (`_verify_accepted*`) | 1.1 | 0.1 | 0.1 | 1.4 |
| SQLite | 0.5 | 0.0 | 0.0 | 0.6 |
| Other | 2.1 | 0.6 | 0.6 | 0.7 |

- **The Agent capture fix worked:** patch capture/payload copy-and-compare dropped from about 6 s (previous profile on `297863fb`) to 0.04 s; capture itself is about 1 s.
- **The largest cost now is copy/compare called from `timeline_commit_auth.covers`: 5.6 to 5.7 s of an 11.4 to 11.9 s warm save (48 %), 8.6 to 9.0 s of the two slow saves.** The calls come from `validate_step` at `timeline_commit_auth.py:399`, `:462` and `:465`, `validate` at `:3406`. Together with copy/compare from other callers and jsonschema it is about 8.5 s of 11.9 s.
- **W3 and the cold save are slow (about 20 s) because the proof was rebuilt:** old-history verification 1.4 and 1.1 s, JSON encode 3.2 and 2.5 s (`iterencode` from `canonical_json` in `util.py:25`, 2.4 to 3.0 s), SQLite 0.5 to 0.6 s, and extra auth validation, about 8 s more than W1 and W2 in total. W1 and W2 reused it (history verification 0.1 s, JSON 0.6 s). So something cleared the proof between W2 and W3 (inferred from the profile only; no trace).

## Top 15 frames by self time (all four saves are in `profile-groups.txt` with their callers)

In the warm saves W1 and W2 the 15 largest self frames are the lines of `value_equal` (`timeline_commit_producer.py:60-70`, about 0.2 to 1.2 s each, 4.9 s together for W1) and its generator expressions (`:67`, `:69`, 0.6 to 0.7 s each), all called from `timeline_commit_auth.covers` (`timeline_commit_auth.py:223`) except `_doc_patch`/`_commit_patch` `equal` (`_command_state.py:40`, 0.16 to 0.23 s, from `capture` at `_commit_patch.py:358`), `iterencode` (0.4 to 0.55 s, `canonical_json`), `deepcopy` internals (0.15 to 0.2 s each) and jsonschema `is_type` (0.14 s). In the cold and W3 saves `iterencode` is the top frame (2.4 and 3.0 s, from `canonical_json` in `util.py:25`), followed by `value_equal:67`/`:69` (1.3 to 1.8 s), then `check` at `timeline_commit_store.py:349` (0.85 to 1.03 s, from `_verify_accepted`), `digest` at `timeline_commit_validation.py:96` (0.66 to 0.81 s, from `_history_chain`), and `_read` at `timeline_commit_store.py:293` (0.49 s, the SQLite fetch for the history prefix).

## Not established

- The sampler's own effect on the timings (100 Hz); W1 and W2 here took 13.3 and 13.4 s against 12.7 s median unprofiled warm saves.
- What cleared the proof before W3 (and again before the cold save, which is expected). The saves are 2 to 3 minutes apart in this repetition.
- The `SV-L1` timing lines are still absent (`commit-timing-summary.json`: 0 lines); see the earlier report on the daemon logging setup.
