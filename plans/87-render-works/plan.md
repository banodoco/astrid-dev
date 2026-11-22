# A render that works, and stays working

**Project:** A render that works, and stays working

**Goal:** We can render a real timeline with built-in, collection and project elements, word-anchored clips and imported media on installed and source stacks, recover failed work, and catch a broken render path in CI.

**Status:** queued

**Owner:** Unassigned

**Estimate:** Draft estimate: about 20 engineering days in three phases (8, 6, 6), before the later custody, composition, recovery and checkpoint findings; re-estimate before dispatch.

**Waiting on:** D1–D7, scope review, a claimed run and a current release cut decision.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — this plan establishes the render/recovery contract and its safety net. [Plan 27](../27-video-render-options/plan.md) retains export choices and presets; [Plan 59](../59-into-the-minkhole-proof-point/plan.md) retains the creative proof point. We do not change a vision gap's closure route in this scope filing.

## Outcome and scope

We propose one dependable path from an admitted timeline to a registered playable render, including recovery and a CI check that uses the product. All decisions in [inputs.md](inputs.md#owner-decisions) remain open. Filing this queued plan authorizes no implementation, integration, release or running-stack change.

The proposed scope retains four groups from the independent draft: (a) registry projection, worker readiness/context, pack resolution, media swap and constrained word retiming; (b) an installed/source render journey in CI and truthful command hints; (c) measured heartbeat renewal, native custody, session/scratch recovery, progress and revert; (d) bounded write-path repairs. We add preview/render pack revision parity, fade/easing parity, early range validation, bounded task inventory, queued-work recovery and resumable/checkpointed rendering. The later additions require a new estimate and contract review before dispatch.

We defer broad save rewrites to [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md), collaboration to [Plan 76](../76-editing-together/plan.md), complete word binding to [Plan 18](../18-timeline-editing/plan.md), export controls to Plan 27, and unrelated preview, generation and project-pack CLI defects. Windows render qualification and rendering speed are outside this first journey. We reuse the measurement method from [Plan 85](../85-one-place-to-measure/plan.md) where it applies rather than invent another timing harness.

## Existing work and decision

We retain the judge's [per-change verdict table](inputs.md#per-change-verdicts) as recommendations, the sanitized [original plan](evidence/shipplan/PLAN.md), [verdicts](evidence/shipplan/VERDICTS.md) and [decision log](evidence/shipplan/DECISIONS.md) as historical inputs. Their claims are superseded where corrected below. They are not accepted decisions.

**Correction — no exemption was used.** The pause-tightening edit was skipped and never published. No edit to a film project used the word-provenance exemption. We remove the draft's retrospective audit task RW-13. Independent anchor-alignment proof is a precondition for the first actual use of any temporary exemption, not an audit of an edit that happened. The unsafe code still exists in the candidate branch; its presence is not evidence of use.

**Candidate fixes, per-change verdicts in the plan:** [astrid-agent `release/14/r6-fixes`](https://github.com/banodoco/astrid-agent/tree/release/14/r6-fixes), draft [PR #530](https://github.com/banodoco/astrid-agent/pull/530), head [`ad10ff6de`](https://github.com/banodoco/astrid-agent/commit/ad10ff6de370db547e3ae2af45311751d228f98f). Related component PRs [#525](https://github.com/banodoco/astrid-agent/pull/525) and [#526](https://github.com/banodoco/astrid-agent/pull/526) remain contributed work; we neither close nor merge them in this filing.

**Reproduction archive, do not merge:** [astrid-agent `release/14/r6-render-stopgaps`](https://github.com/banodoco/astrid-agent/tree/release/14/r6-render-stopgaps), based on `ad10ff6de`. [Inputs](inputs.md#source-identities) links every separate stopgap commit, including the exact untracked library patch. The archive omits the debug dump and replaces the private alias literal with `ASTRID_R6_MOTION_PACK_OVERRIDE`; the recorded run used a hard-coded local path. Both test files are retained as historical evidence, including the syntax-tree assertion that the real repair should replace.

### Findings after the independent draft

| Finding | Evidence and confidence | Planned repair |
| --- | --- | --- |
| Preview and render resolve different revisions of the same motion pack. The App-vendored text default is `COLOR.ink`; the collection copy uses `DEFAULT_COLOR = '#FAFAFA'`, yielding white captions on a cream plate. | Recorded finding, [#1469](https://github.com/banodoco/astrid-dev/issues/1469), [before](evidence/take/y-sheet.jpg), [after](evidence/take/probe9.jpg). | RW-30: identify and pin the same pack revision across preview/render. A local App-source alias only demonstrates the mismatch. |
| `@banodoco/timeline-composition` / `resolveAnimationReferences` refuses an entrance fade with `params.easing`: `Animation 'fade' cannot consume explicit easing progress`; preview accepts it. One clip failed a whole range. | Reported session failure and verified [exact hand patch](https://github.com/banodoco/astrid-agent/blob/release/14/r6-render-stopgaps/docs/r6/timeline-composition-fade-easing.patch); [#1500](https://github.com/banodoco/astrid-dev/issues/1500). Clean-tuple reproduction is pending. | RW-25: one explicit composition contract, preview/render regression; do not ship a silent easing discard. |
| Custody capture fails at `pid_for_task`, `kern_return: 5`, with pre/post observations still LIVE; render fails about 0.6 s later. The built-in retry excludes that substage. Failures at 1,204.993 s and 200.250 s disprove a fixed twenty-minute limit. | Verified in [Astra report](evidence/astra20/REPORT.md) and [timeline](evidence/astra20/timeline.tsv); [#1473](https://github.com/banodoco/astrid-dev/issues/1473). An exiting short-lived helper race is the leading explanation; executable identity and eventual exit are not retained, so the OS cause is inferred. | RW-23: bounded same-incarnation retry/terminal observation without weakening custody. The three-second wait in `retry-pre-observation` is behind the excluding predicate and cannot fix the recorded signature. |
| Heartbeat receipts stop abruptly 145.990–155.869 s after claim. One run has 32 successful receipts about 5 s apart, then none; authority expires exactly one last-granted lease later. | Verified by [Astra](evidence/astra20/REPORT.md), [snapshots](evidence/astra20/task-snapshots.json), [timeline](evidence/astra20/timeline.tsv); [#1472](https://github.com/banodoco/astrid-dev/issues/1472). Cause unknown. | RW-10 measures pump/read/lock/send/ACK/exit; RW-11 repairs the measured path. A 600 s, then 7,200 s lease masks stopped renewal and holds reservations longer. |
| Failed work leaves the host session slot occupied, and the Runtime can still count unresolved expired work as active. | [Range log](evidence/take/ranges-status.log), Astra recovery analysis; [#1474](https://github.com/banodoco/astrid-dev/issues/1474). Expiry is intentionally not stop proof; a dead-task symptom does not authorize blind resource release. | RW-24: one fenced recovery flow spanning native stop evidence, terminal publication, reservations and session retirement; verify the next render without restarting. |
| Task inventory fails over 4 MiB; an orphaned queued task was claimed after restart. | Retained session observations, [#1501](https://github.com/banodoco/astrid-dev/issues/1501), [#1502](https://github.com/banodoco/astrid-dev/issues/1502), range/adoption log. Exact inventory boundary and stale-client policy need isolated reproduction. | RW-26 bounded pagination; RW-27 explicit queued-work intent and reconciliation. |
| Changing a file under `remotion/node_modules` invalidates readiness until restart, reported as “Remotion isn't ready on this machine.” | Verified refusal text at 22:34–22:35 in [range log](evidence/take/ranges-status.log); [#1503](https://github.com/banodoco/astrid-dev/issues/1503). | RW-28 names stale validated inputs and the supported restart/revalidation route, retaining the guard. |
| An end of 196.5667 s is about 0.00003 s beyond the exact timeline end. Refusal is correct, but happens only after admission; rounded values look identical. | Verified in range log at 22:27; [#1504](https://github.com/banodoco/astrid-dev/issues/1504). | RW-29 checks exact frames/time before admission and prints sufficient precision. |

**How a film project finally rendered.** Four product-rendered ranges covered 0–50, 50–100, 100–150 and 150–196.5667 s nominally; the last successful request used 196.566666 s, below the exact 196.5666667 s boundary. [The log](evidence/take/ranges-status.log) records all four completed. We joined them outside the product: video stream-copied, audio decoded, trimmed/joined and encoded once ([join.sh](evidence/take/join.sh), [join-n.sh](evidence/take/join-n.sh)). Seams were measured clean in the supplied run; [seam frames](evidence/take/seam50-sheet.jpg) and [other seams](evidence/take/seams-sheet.jpg) retain visual evidence. Numerical seam measurements are not independently reproduced by this filing. This demonstrates the render path per range with stopgaps, not a reliable full-duration render or a proven custody/lease fix. RW-31 brings safe checkpoint/restart behavior into the product.

### Why this is not a simple merge onto release/15/main

About five committed fixes are simple cherry-pick candidates once their missing tests exist. `release/15/main` already contains the branch's cut commit `83d5f8fe`; the 21 extra lineage commits matter only for a merge into `release/14/main`. Both targets nevertheless conflict on launch-context code, and the diagnostic conflict must also be reconciled. The [trial cherry-picks](evidence/mergescope/REPORT.md) skipped conflicted picks, so later clean results are conditional, not an integrated pass.

The stopgaps are not fixes: a hard-coded bundler alias (published as an environment override), a 7,200 s lease, the custody wait, a hand-patched library in node_modules, three pack-path workarounds that should be one, a debug dump (excluded from the archive), and the word-provenance exemption (in the base branch, never used for a film edit). None should arrive in a release by merging this archive.

The real repairs span repositories: lease policy and client generation belong to the Runtime; fade/easing belongs to the composition package; preview/render revision identity spans the App-vendored and collection packs; retired locators are still written by the editor on import. The App → Agent → Runtime pins must move together as a qualified tuple. One root cause, heartbeat renewal stopping, remains unknown. No current CI gate exercises this representative installed/source render journey end to end; individual render-oriented tests do exist. That missing real render check let the breakage pass unnoticed, so it is part of the merge's proof, not an optional extra.

## Sequence and readiness

The shortest proposed path is RW-7 → RW-1/RW-2 → RW-3/RW-25/RW-30 → RW-8, with the journey developed first and run manually against fixes, landing only when green. The long-render/recovery path is RW-10 → RW-11, alongside RW-23 → RW-24 → RW-31. We first run the journey against actual release heads in disposable stacks to establish which lines are broken. This filing runs no product workload.

D1 keeps the release choice open: fixes to code actually on 14 can start on current issue-scoped 14 fix branches and flow forward; Plan 69-dependent and design work belongs on current 15 plan branches if that scope is accepted. If 14 has shipped, the release skill's fix-release numbering applies. We do not infer publication from equal branch heads. D7 proposes a Release 15 brief row in this scope PR; there are no product plan branches, activation or ruleset changes yet. Before any implementation, record actual base/dependency revisions, scope, authority and focused checks as [tasks.md](tasks.md) requires.

We recommend two final review rounds per phase, pending agreement, with an explicit review stop after the shared render/custody/checkpoint contract and before dependent integration. This differs from the historical judge's no-stop recommendation because later evidence adds a native identity boundary and resumable output custody. The stop protects subsequent tuple qualification from having to rebuild against a wrong contract. The existing independent critique is retained; a fresh simplification critique of the corrected shared contracts is still required before greenlight.

## Interfaces and handoff

We consume exact Runtime/Agent/App and pack/composition pins, immutable admitted timeline/media identity, the generated registry and the current task/attempt/fence/epoch protocol. We produce one worker environment builder, registry-owned pack resolution and revision identity, one composition easing rule, measured small fenced heartbeats, bounded custody/recovery, and registered checkpoint outputs. `ASTRID_RENDER_PACK_ROOTS` is an existing channel to reuse, subject to D5. Checkpoints must bind the timeline revision, range/frame boundaries, tuple, pack revisions, output identity and custody; a changed input invalidates reuse.

The handoff is the integrated candidate and its receipts, logs, focused tests and journey results, linked in the eventual completion PR. The two existing branches are donors/evidence, never qualified release heads. We retain historical source identities in [inputs.md](inputs.md#source-identities); actual dispatch pins must be refreshed. Product PRs land in accepted plan/fix branches under the release skill, not product `main`.

## Completion

- A real installed/source journey on Linux and macOS reaches a Runtime `task.completed` receipt and a registered playable artifact with expected frames, pixels, audio and word timing. Every named negative case fails at the intended boundary.
- A loaded multi-minute render renews with bounded leases through preparation, draw, encode, ingest and settlement. A crash expires/reconciles safely; a transient custody failure cannot accept a reused PID or silently abandon a live process.
- Failed/cancelled work reclaims scratch and reservations only with the required stop proof, retires the session slot, and admits the next render without a stack restart. Task inventory and queued-work intent remain inspectable.
- A resumable render reuses only validated completed ranges/checkpoints, joins with correct frame/sample boundaries, and rejects stale inputs. The same full-duration film-project workflow completes on an exact qualified Release 15 tuple with no local patches or external join procedure.
- CI runs the representative real render journey and catches deliberately reintroduced pack, worker, composition, admission and recovery failures before integration. Required-check settings remain a separate explicit decision.

Proof is limited to the named timeline fixtures, pinned tuple, supported profiles and two operating systems. A three-second journey does not prove long-render heartbeat/custody reliability; dedicated load, churn and checkpoint cases must do that. Publication remains outside this filing.
