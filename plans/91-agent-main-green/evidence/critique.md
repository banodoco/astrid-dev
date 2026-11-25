# Critique and ambiguity pass — Agent main green

[Plan](../plan.md) · [Inputs](../inputs.md) · [Tasks](../tasks.md)

On 24 November 2026, in session https://claude.ai/code/session_011EzfW1C63rxLXsL6TkHHVV, the planner had three reviews run on the written plan and tasks. Each checked the plan's claims against astrid-agent `release/15/main` at `a09ea669`, the CI logs and the GitHub API:
- an independent critique, by a fresh high-judgment agent (Claude Opus) with no stake in the draft, briefed per the [planning skill](../../../agent/shared/workstreams/plan.md) to build as little as possible;
- two ambiguity passes (Claude Haiku), one on Phase 1 and one on Wave B.

The planner re-checked each must-fix finding in the code before accepting it. Every finding below was accepted unless it says otherwise.

## Critique

The verdict: the causes are sound, but the gate, the nightly run and the schema mechanics did not match the code.

| # | Severity | Finding (evidence) | What changed |
| --- | --- | --- | --- |
| 1 | must-fix | A pull request into `release/15/main` runs only fast checks, unit shard 1 and boundary (`ci.yml:9-13`, `:248`; the heavy jobs carry `if: github.event_name != 'pull_request'` at `:25`, `:419`, `:535`). Lanes has no `pull_request` trigger (`lanes.yml:6-16`), and pushes to plan branches start nothing. Release 14's K2/K3 comparator never passed on an unchanged tree. | AG-1 gates the manager's dispatched batch runs and the completed release-branch runs. It reuses `env/baseline-diff.py`, with `missing` also blocking, and adds hosted card runs (`tests`, `repeat` inputs). It ports nothing else. D4 and D7 were rewritten. |
| 2 | must-fix | The safety-net commit `ab95803c` is 133 commits behind `release/14/plan-39` (`2ef74155`) and lacks #433, #373 and #406. | The plan no longer ports from that branch. It names `2ef74155` for reference only. |
| 3 | must-fix | `cancel-in-progress` is false on `release/*/main` (`ci.yml:16-18`, `lanes.yml:18-20`), yet started runs were cancelled: some after 9 seconds, some after 27 minutes, and three dispatched runs too. So the "GitHub replaces waiting runs" diagnosis was wrong. Also, `schedule` runs only on the default branch. | AG-0 finds what cancels the runs. AG-10 uses dispatched runs on a frozen plan head (D15), not a nightly schedule. |
| 4 | must-fix | The timeline config schema is vendored from the Runtime (`runtime.lock.json:3-5`), and `boundary` checks it (`ci.yml:594-622`). The fixture's shape is `{numerator, denominator}`. | AG-A9 and D8 were rewritten: the schema option needs a Runtime PR and a pin bump after Plan 77's. |
| 5 | must-fix | The reader-check refusals are not only fixture shape. `test_commit_runtime_opaque_items.py:1` asserts that unknown namespaced values survive, so stripping clip-level keys would quietly delete a contract. The cluster spans 40 files, including Plan 88's. | AG-A7 (`output.resolution`, N) was split from AG-A8 (the clip-data decision, S, D13), and AG-A8 is reviewed at RS1. Plan 88's file stacks. |
| 6 | should-fix | The custody tests reach the Runtime's `tests/` through `runtime_protocol.__file__`, so they fail for the same reason as the site-packages cluster. The worker environment installs the Runtime non-editable. | AG-A7's old custody card merged into AG-A1, which also fixes `agent-setup.sh`. |
| 7 | should-fix | The worker environment can't prove the env cards (Python 3.13, depth-1 fetches, no Node, Remotion, Pinokio or ComfyUI). Several cards edit the same workflow `env:` blocks. | The env cards prove on hosted card runs. The old Node, Remotion and git-input cards merged into one card (AG-A2), and the workflow edits got a merge order. |
| 8 | should-fix | RS1 needed only the gate and the two contract cards; Wave B was held behind RS1 unnecessarily; two dependencies were missing; every card would have edited the ceiling. | RS1 depends on AG-1, AG-A8 and AG-A9. Wave B lands after AG-1. AG-B14 → AG-A9 and AG-B16 → AG-A7 were added. The ceiling became a ratchet only the manager edits. |
| 9 | should-fix | 165 Wave C IDs were in files a Wave A or B card already owned. | `make_wave_c.py` now assigns by file glob too. Wave C fell from 507 to 405 IDs. |
| 10 | should-fix | Loopholes: one local pass dropped an ID; "or the fixture" allowed a stub; "any source will do" for stale tests; uncapped D3 and D6 entries; flaky trials with no repeat mechanism; product deadlines the tests depend on. | Rules 1 and 3 were tightened: a hosted pass is needed, the real input is required, and the source must state the new behaviour and postdate the test. D6 needs an X check and the owner's acceptance. Flaky trials use `repeat`. D14 was added. |
| 11 | consider | PR-skipped jobs protect nothing at merge; ID counts were off (1,095 rows, 1,087 distinct); macOS IDs are not prefixed; reviews belong to the high-judgment role. | D4 now separates pull-request checks from release checks. Counts are by (job, id). The evidence README was corrected. RS1 and R name the review role. |
| 12 | estimate | 75–95 days was about right overall, with A1 and A11 overstated and AG-1, A9 and A10 understated. 4–5 weeks was optimistic. | 70–90 days, 5–6 weeks. |

## Ambiguity pass: Phase 1

Paths and line numbers were resolved from the code and written into the cards:
- AG-A1: `ci.yml:341-342` → the model at `:473-474`.
- AG-A2: the three Node and esbuild variables and their sources; `ASTRID_NODE_EXECUTABLE`; the registry step at `lanes.yml:497-510`; the lifecycle variable name mismatch (`ASTRID_TEST_LIFECYCLE_CHECKOUT` set, `ASTRID_RUNPOD_LIFECYCLE_CHECKOUT` read at `tests/_checkouts.py:80`); the two missing Runtime objects.
- AG-A3: the hard-coded chunk at `test_remotion_layer_tail_compat.py:41`; the resources that exist but aren't found.
- AG-A5: C87 and C91 are other causes, so they moved to Wave C.
- AG-A6: the `runtime_abi` fixture at `tests/sdk/test_timeline_commit_provider.py:38`.
- AG-A8: `opaque` is at `:166`, not `:165`.
- AG-A9: the schema line `:546`, and `test_word_binding_recipe.py`.
- AG-A10: the lambda at `test_native_batch_ingress.py:97`.
- AG-2: astrid-dev has no `ci/` folder, so the card creates it.

Owner decisions it raised became D10 (moved packs), D11 (the composition package pin) and D12 (the authentic legacy archive).

## Ambiguity pass: Wave B

Corrected cluster assignments:
- ci:C16 is a product rejection, so B1 and B2 merged into one pack-discovery card.
- ci:C59 is not a budget cause, so it moved to Wave C.
- lanes:C30 and lanes:C42 are installer recovery, not Pinokio, so they moved to the installer card.
- ci:C52 is the reader-check family, so it moved to AG-A7.

Corrected paths:
- `domain_timelines.py` doesn't exist, so AG-B6 finds the parser.
- `generic_host.py:12151`, not `:12499`.
- The `bridge.parent` fixture already declares schema v3, so its cause is open.
- The refusal behind AG-B16 is raised in the Runtime.

It found 13 hidden overlaps between cards. Each is now either a dependency or a single merged card (B10, B11, B15 and B13 absorbed their neighbours). It listed the Wave C rows that belong to Wave B cards, which led to the file-glob ownership.
