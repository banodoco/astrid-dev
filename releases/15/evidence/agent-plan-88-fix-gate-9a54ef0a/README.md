# Gate: the transcript-references blocker fix (Agent #624 with App #392)

**Candidate:** astrid-agent [#624](https://github.com/banodoco/astrid-agent/pull/624) at `9a54ef0a` (`release/15/transcript-refs-envelope`), landed as `a3f3b01c`. It goes with astrid-app [#392](https://github.com/banodoco/astrid-app/pull/392) at `21f4de61`, landed as `7bc0d4b1`.

**What it fixes:** the Release 15 blocker on the Lead board (astrid-dev #1836, `r15-lead-0002`). A project became unopenable in the editor after `astrid timelines transcripts refresh`.
- **Agent (#624):** writes the full TimelineBundle envelope with `assetId`, keeps `mediaId` and `sourceId`, and validates before saving.
- **App (#392):** accepts optional `mediaId` and `sourceId`. It repairs exactly the legacy row shape, which Release 14 could write, when a project is read.
- **Assertion change:** one existing assertion changed (`test_explicit_choice_is_recorded_and_saved`, which now also expects `assetId`). The Lead approved it under the owner's delegation (#1849, `r15-lead-p88-0001`).

**Runs compared, whole-run by id:**

| Side | ci.yml | lanes.yml |
|---|---|---|
| Candidate `9a54ef0a` | 45402133396 | 45402141019 |
| `release/15/main` `514499de` | 45351510784 | 45351510868 |
| Baseline | [8807f820 list](../agent-ci-baseline-8807f820/release-15-8807f820-failing-ids.tsv) | — |

**Result: 1,876 candidate ids, of which 7 are in neither reference** ([new-ids.txt](new-ids.txt)). All failing ids are in [gate-failing-ids.txt](gate-failing-ids.txt).
- **Four are named movers in the baseline README:**
  - the two darwin render-budget tests (`test_rendered_mp4_contains_audio_stream`, `test_text_card_render_smoke`);
  - two members of the `test_readiness_missing_models` group.
  The fix touches none of their code.
- **Three are in integration shard 3.** That shard ran 2:03, against 1:23 on main, and had 126 failures against 123. The fix's files (`core/timeline/bundle.py`, `packs/timeline/cli_working.py`, `sdk/timeline_transcript_refresh.py`) are not reached by any of the three:
  - `test_command_count_capture.py::test_fresh_process_command_counts`, a timeout at 117.7 s against 68.6 s on main;
  - `test_dry_run_equals_live_run.py::test_dry_run_equals_live_run[image/t2i-attached]`, a CustodyError after the Comfy fixture refused a connection, already ruled an environment failure at the 551c190e gate;
  - `test_generic_host_activation_acceptance.py::test_uncertain_commit_preserves_exact_host_and_credential`.
- **Condition set by the Lead (#1849, `r15-lead-p88-0006`):** the three ids were re-run locally, 3 times each, on base and head.
  - `t2i-attached` passed 3 of 3 on both sides.
  - The other two failed identically on both sides for local environment reasons, so the local runs neither support nor contradict the hosted failures.
  - The head did no worse than the base, so the condition is met. If those two ids recur on a later gate, they are owned by whichever plan touches host activation or command counting.
- `test_host_bridge_outer_send_diagnostic_preserves_revoke_close[False]` fails on main too and is a named mover, so it is not new.
- Every unit shard on both sides has its pytest summary line.

**Verdict: PASS.** Agent #624 was merged by Plan 88; App #392 was merged by the Release 15 Lead.

**Limits.** Each side is one run. The ids were extracted from full job logs by script (copies in the Lead session's `/root/gate624`); the logs themselves are not kept here.
