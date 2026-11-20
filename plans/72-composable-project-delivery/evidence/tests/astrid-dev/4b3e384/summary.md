# PD-0 — read-only source and CI baseline (20 November 2026)

**Scope:** Plan 72, `banodoco/astrid-dev`. This is a read-only source survey and a record of *existing* GitHub Actions; no local or new hosted test has been claimed and no application behavior was changed.

## Source identities and ownership

- **Actual pre-candidate main:** `4b3e3841af3921d9846389a4cd744f027c1db0b3`. [Existing main documentation run](https://github.com/banodoco/astrid-dev/actions/runs/44817209810) and its [documentation job](https://github.com/banodoco/astrid-dev/actions/runs/44817209810/job/136568502940).
- **After Release 15 placement PR #1071:** `ae9e105d6e1fdd298e6bc9a39162a8556aea471d` (Release 15 brief now includes Plan 72, but its `release/15/main` branch and release manager are not yet present). This is *not* the base that the following previously launched candidates were cut from.
- **Candidate core:** `06c0ce64bb86e7524bb80208388c0d7147d8f511` ([PR #1074](https://github.com/banodoco/astrid-dev/pull/1074)). **Candidate reader:** `67edfee28bcb07b4aba297508d8326354bd1c64a` ([PR #1076](https://github.com/banodoco/astrid-dev/pull/1076)); this stacks on the core. **Guide:** `b730a3057ccb2f2897516c6cbe4b0627facf6063` ([PR #1079](https://github.com/banodoco/astrid-dev/pull/1079)), stacked on an earlier reader SHA, so it must be refreshed or merged forward before qualification.
- **Competing writer:** [PR #1059](https://github.com/banodoco/astrid-dev/pull/1059), `refactor/vision-goals-authoring-20261120`, changes `vision_subject.py`, `gap_relationships.py`, vision source headings, and `export_public_vision.py`. Its original rename changes `parse_gap_aspirations`→`parse_gap_goals` and parsed subject `characteristics`→`goals`. Plan 72's new adapter was changed to accept both authoring forms without touching those established sources. Do **not** merge its changes or override its writer.

| Canonical home / existing parser | Established meaning | Plan 72 may derive |
| --- | --- | --- |
| `vision/{pillars,principles}/*.md` via `scripts/vision_subject.py:parse_subject` | Authored goal IDs and element association | Stable `goal` identities |
| `vision/gaps/*.md` via `scripts/gap_relationships.py:gap_metadata,parse_gap_aspirations` | One primary and optional supporting goals | `gap measures goal` with role/source |
| `plans/*/plan.md` via `scripts/project_contract.py:project_number,plan_gap_ids` | One primary gap, supporting gaps or foundational enabler | `project addresses gap` |
| `releases/*.md` via `scripts/records.py:release_brief,release_issue_block` | Included plans and authored issue snapshots/freeze | `release includes project`; frozen `issue listed-in release` |
| `scripts/export_public_vision.py:build` and `scripts/views.py:VIEWS` | Current schema-v1 public feed and generated pages | Derived views only; **no** competing copy |
| `scripts/checks.py:REGISTRY`, `scripts/check_docs.py` | Existing structure checks and diagnostics | Registered structural integrity, without replacing existing refusals |

## Existing CI receipts — exact commands and counts

The GitHub-hosted Linux documentation workflow uses `python3 -m unittest discover -s scripts -p "test_*.py"`, followed by the existing `python3 scripts/astrid_dev.py check --base "$base_sha" --event "$GITHUB_EVENT_PATH"` and `python3 scripts/astrid_dev.py check`. Actual workflow jobs and raw logs remain linked below.

| Source revision | Workflow / documentation job | Original full unit-test result | Additional checks |
| --- | --- | --- | --- |
| `4b3e3841af39...` (main baseline) | [44817209810 / 136568502940](https://github.com/banodoco/astrid-dev/actions/runs/44817209810/job/136568502940) | **PASS: 450/450**, `Ran 450 tests in 75.638s; OK` | Documentation and vision-consumer contract success |
| `06c0ce64bb86...` (core candidate) | [44818918534 / 136574394211](https://github.com/banodoco/astrid-dev/actions/runs/44818918534/job/136574394211) | **PASS: 456/456**, `Ran 456 tests in 42.007s; OK` | Documentation and vision-consumer contract success |
| `67edfee28bcb...` (reader candidate) | [44819951954 / 136577973721](https://github.com/banodoco/astrid-dev/actions/runs/44819951954/job/136577973721) | **PASS: 463/463**, `Ran 463 tests in 54.730s; OK` | Documentation and vision-consumer contract success |
| `b730a3057ccb...` (guide, earlier reader) | [44819398020 / 136576043828](https://github.com/banodoco/astrid-dev/actions/runs/44819398020/job/136576043828) | **PASS: 463/463**, `Ran 463 tests in 61.432s; OK` | Documentation and vision-consumer contract success |

The earlier [44813342112](https://github.com/banodoco/astrid-dev/actions/runs/44813342112) at `9949514a...` failed two baseline tests (`test_golden`, `test_views`) on a simultaneous duplicate Plan 71 transition. That failure was not attributed to Plan 72; the later, newer pre-candidate `4b3e384` baseline passed. Preserve all original golden checks.

**Limits:** These receipts prove each workflow ran at its own revision. They do **not** prove an end-to-end CLI query against live `main`, byte-identical before/after feed, successful release integration, or independent approval. The release `15` branch is not cut by this manager, the owner of Release 15 is unnamed, and the initial architecture review is still pending.

## Explicitly unsupported in the intermediate milestone

A merely labeled GitHub issue is not a shipped fix; an unfrozen issue ledger is not immutable release evidence. A listed project is not an automatically closed gap; reviewer judgment, release publication and human authorization are separate. No scheduler, execution state machine, generic pipeline DSL, second live pipeline, graph database, public evidence narrative or new approval system is authorized.

**Reproduce:** open each native GitHub Actions link above, inspect the documentation job's `Run python3 -m unittest discover -s scripts -p "test_*.py"` group and the `Ran … tests` line, then the downstream `astrid_dev.py check` steps. Rerun those commands against the stated exact SHA in an authorized local checkout. At next dispatch, re-pin the current `main`/release branch and the dependency PR heads before any integrations.
