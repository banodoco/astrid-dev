# P95-ANCHOR — recognize explicit Markdown fragment targets

**Source:** P95-19d generic proof [BLOCKED](https://github.com/banodoco/astrid-dev/issues/1886#issuecomment-7222163084). **Route:** X, normal Chat Extra High. **Repository:** `banodoco/otto`, branch `p95/ot-fragment-anchors` → `main`. **Base:** `13cf97b873558ffa4038963bb252fd4f26eecead`. One fresh session.

## Outcome and scope

Otto's generic `link-anchors` recognizes real, rendered HTML `id` targets as well as existing Markdown heading slugs. In the Dev tree nine distinct reported target/fragment pairs are real `<a id=...>` targets in table cells, not missing headings. Preserve every existing heading algorithm, fail-closed missing target behavior and generic full-tree scan. Do not alter the legacy Dev validator or loosen checks based on path, workspace name or historical status.

**May touch:** add a fragment-target helper in `otto/markdown.py`; the fragment lookup only in `_link_anchors` in `otto/checks.py`; and a new narrowly focused Otto test file. Shared `skill_config` and workspace config, CLI, existing assertions, Dev, release documents and output defaults are another packet's scope. Keep changes to `otto/checks.py` limited to `_link_anchors`, disjoint from P95-SK's `skill_config`.

## Step 1 — inventory and stop

Read the existing heading-anchor parser, fence/comment handling and all direct call sites, including the Dev legacy validator. Propose exact rules for rendered HTML ids in normal text and Markdown table cells, quoting/case/duplicates, escaping, and correct exclusion of fenced code, inline code and comments. Show how heading slugs remain byte-identical and legacy consumers do not change. Identify a bounded safe parser and test matrix. Post the design and wait for Lead decision before writing; if reliable HTML fragment semantics need broader scope, stop rather than claiming support.

## Proof and handoff

Lead runs Otto's full suite and focused new tests, including valid explicit ids and headings, non-existent ids, duplicates, multiline comments, fenced and inline code decoys, and the real nine Dev targets. Verify that removing a real target makes the link fail and that an example hidden in code/comments cannot suppress an error. No generic check is disabled and no historic link is silently grandfathered. The packet does not clone, build, test, run CI, merge, edit plan records or start a second packet. Open a draft PR and end `READY-PROOF <repo> <PR> <head> <selectors>`.
