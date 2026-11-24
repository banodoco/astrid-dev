# Agent gate: Plan 88 into release/15/main at 551c190e

**Candidate:** `banodoco/astrid-agent` `release/15/plan-88` at `551c190e`, landing PR [#612](https://github.com/banodoco/astrid-agent/pull/612). The branch already contains `release/15/main` at `6a1d247a` (merged by #603), so the comparison is against that head.

**Runs compared, all whole-run and by test id (standing ruling 10):**

| Side | ci.yml | lanes.yml |
|---|---|---|
| Candidate `551c190e` | [45333914673](https://github.com/banodoco/astrid-agent/actions/runs/45333914673) | [45333919061](https://github.com/banodoco/astrid-agent/actions/runs/45333919061) |
| `release/15/main` push run | [45324437800](https://github.com/banodoco/astrid-agent/actions/runs/45324437800) | [45324437851](https://github.com/banodoco/astrid-agent/actions/runs/45324437851) |
| Baseline | [`release-15-8807f820-failing-ids.tsv`](../agent-ci-baseline-8807f820/release-15-8807f820-failing-ids.tsv) (ci.yml) | — |

The candidate's failing ids (1,874, with lane) are in [`gate-failing-ids.tsv`](gate-failing-ids.tsv). They come from the complete job logs, fetched through the jobs API, and not the 5,000-line tail. That closes the gap the lane reported in unit shards 5, 6 and 7: every id in those shards is now checked. Each unit shard's pytest summary line is present.

**Result: no new failure the candidate could cause. Gate passed.**

- **Unit, all 8 shards:** every id is in the baseline list or fails on main as well. Two ids fail on main but are not in the list. Both are `tests/core/generation/test_readiness_missing_models.py` members of the readiness group, which the baseline README already names.
- **Fixed:** four ids fail on main and pass on the candidate. Three are in the Pinokio adapter group and one is a readiness member; all of these move between runs.
- **Darwin native:** two ids are in neither main nor the list: `test_audio_render::test_rendered_mp4_contains_audio_stream` and `test_text_card_render::test_text_card_render_smoke`. Both fail with `candidate reconciliation budget ran out after ~1.3s`. These are the two macOS render tests that the baseline README (added 23 November) already names as moving.
- **Lanes:** opt-in and integration shards 1, 2 and 4 match main exactly. Shard 3 has one id in neither: `tests/integrations/test_dry_run_equals_live_run.py::test_dry_run_equals_live_run[image/t2i-attached]`.
  - It fails with `CustodyError: host graph cleanup remains unresolved`. Underneath, the attached Comfy fixture refused the connection on `/queue` (`ConnectionRefusedError`, `comfy target /queue request failed`) during host shutdown.
  - Plan 88 changes no execution, custody, generation or Comfy-target code. The one file near rendering is `astrid/packs/rendering/docs/scripts/timeline_document.py`.
  - The Lead ruled this an environment failure: it does not hold this landing. If it recurs on a later gate, Plan 87 investigates it under the custody work.
- The lane also named `test_native_word_anchor[missing-version]`. That id fails on main's lanes run too, so it is not new.

**Non-test jobs:** fast checks, boundary, windows-native-and-installer and both release wheels succeeded; landing reference skipped.

**Limits.** Each side is one run. The ids were extracted by script in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG); the logs are not kept here.
