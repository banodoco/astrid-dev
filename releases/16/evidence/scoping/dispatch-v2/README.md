# Release 16 — scoping coordinator handoff

This is the direct-report handoff revision of the compact operational version of the Release 16-only kit. It retains all 32 substantive assignments and their dependencies from V4. It replaces repeated common instructions and blank forms with one procedure and a single evidence index. **Do not restart or overwrite already dispatched V3/V4 work.** Preserve its exact original briefs and reports in Git; use the new packet text only for new assignments or explicitly agreed follow-ups.

## Canonical procedure and starting record

- [Scope a release](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/shared/workstreams/scope-release.md) and [Sense check](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/shared/workstreams/sense-check.md), proposed in [PR #1960](https://github.com/banodoco/astrid-dev/pull/1960) and [PR #1962](https://github.com/banodoco/astrid-dev/pull/1962). Follow the [evidence-only ChatGPT packet path](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/roles/manager/chatgpt-packet.md#receive--investigate-or-judge--submit-evidence-only) and [dispatch procedure](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/roles/orchestrator/multi-manager-dispatch.md#evidence-only-dispatch). These are authored Markdown-first `skill: true` sources. Until the separately authorized Plan 73 cutover, read the exact sources directly and use the latest supported installed astrid-dev skills. After cutover use the existing skill builder and installer; no new script or registry.
- [Release 16 scoping evidence index](https://github.com/banodoco/astrid-dev/blob/a205eba42e1fd24f561386e8888aafba78d0ed1e/releases/16/evidence/scoping/README.md), pushed on `scope/release-16-scoping-record`. This is a starting assignment/index, not a record of completed reviews. Integrate it into the current scoping proposal branch by normal reviewed process; do not create a competing run or blindly merge stale roadmap/skill migration trees. If a run already exists, use it.
- [Roadmap proposal PR #1956](https://github.com/banodoco/astrid-dev/pull/1956), refresh actual head and main. Read `context.md` for the current owner boundaries, publication questions, starting source leads and proposed acceptance journeys. Only Release 16 is commissioned.

## Start, coordinate, preserve

You are the coordinator. First recover any actual in-flight sessions, branch, mailbox, original assignments and submitted findings. Establish one existing or new research mailbox and one proposal branch; do not alter active delivery authority. Verify the latest supported astrid-dev installation and source revision; sessions unable to install read exact pinned instructions and report the limitation. Freeze a shared source register at the real heads: actual served manifest/pins (regression and migration baseline), newest integrated `release/15/main` product branches (implementation baseline), transitive/launcher pins, planning main, roadmap proposal, live R15 handoffs and main-only differences. These are not interchangeable. Save that register in the evidence index or a linked snapshot. Before dispatch, save actual packet brief and source identity to Git; attach only what the session cannot read remotely. No blank report templates are needed.

Run first packet alone to verify handoff. Then **maximum five active ChatGPT sessions**, including reviews and replacements. Use the existing route convention: N normal Chat High, X normal Chat Extra High, S Pro. N/X research does not substitute for a consequential independent high-judgment verdict. Verify the actual hourly schedule and resume ability; if unavailable name the manual fallback. Each hour recover from Git and mailbox, verify pushed reports and index their immutable links, unblock or resume work, fill slots, post one STATUS. Existing run board/mailbox owns live state; no new status CSV or scheduler. Keep active R15/R17 runs untouched. The coordinator owns the assignments and shared evidence index; each ChatGPT session writes and pushes its own original report to its dedicated report-only branch and draft PR. Before dispatch, name the report path, branch, base, proposal PR destination and evidence-only write authority. Verify the first real report push, draft PR, mailbox STATUS and remote readback before expanding concurrency. Existing dispatched briefs remain unchanged; explicitly authorize report-only writes for ongoing read-only sessions before they write.

Every session reads the relevant canonical plan/inputs/tasks, actual code, issue bodies/comments, real proof and current owner direction; source SHAs or issue/PR/proof links for all material claims. Use the sense-check questions proportionately. Distinguish observed, inferred, unverified and access gaps. Write and push one original Markdown report to your assigned branch: **reviewed identities and limits; verdict or disposition; numbered findings with BLOCKING/FOLLOW-UP/NOTE, evidence, impact, minimal change, owner and verification**. Project checks disposition existing tasks; scouts record query coverage and independent problem inventory; cross-project investigators read original prerequisite reports. No product edits, tests/CI, spending, issue mutation, branch retargeting, task completion, merge or publication.

**Durable intake:** Each session pushes its full original to its assigned report-only branch and draft PR, verifies remote readback and posts `READY-REPORT <repo> <PR> <head> <report-path>` in STATUS. The coordinator verifies the remote report, exact reviewed identities, authorized report-only diff and completeness before dependent work, and appends a concise receipt to the release evidence index (ID, snapshot, immutable commit/path link, limits, follow-up). Project-specific findings go under `plans/<slug>/evidence/release-16-scoping/<ID>.md`; cross-project/scout/release reports under `releases/16/evidence/scoping/<ID>.md`. Existing durable originals stay in their home and are linked. Integrate evidence-only PRs into the scoping proposal only where authorized; otherwise link immutable original commits. Preserve the exact reviewed proposal identity separately from evidence submission heads. Manual intake of a complete original is only a documented connector-failure fallback; never require chat transcription as the normal route. Corrections are new linked records; preserve disagreement. Do not upload secrets, private creator content, personal data or raw chats. If necessary use approved restricted pointers and note limitations. Failed push/readback is a real blocker. Keep the original actual V3/V4 assignments and already submitted reports intact; import the original kit files if those were used, not these revised texts as if they were originals.

## Dispatch order

The headers in `packets/` are the assignment source; this index is generated from their inherited dependency list for transport only. B can start as individual prerequisites finish. `CTX-00`, `MATERIALISE-00` and `REPAIR-00` are coordinator actions, not ChatGPT sessions. `ALL_WAVE_A_AND_B` means every required A/B report is durably available.

| ID | Route | Depends on | Assignment |
|---|---|---|---|
| [SC-09](packets/SC-09.md) | X | CTX-00 | Install/update confidence |
| [SC-10](packets/SC-10.md) | X | CTX-00 | Pinokio qualification |
| [SC-29](packets/SC-29.md) | N | CTX-00 | One update path |
| [SC-30](packets/SC-30.md) | N | CTX-00 | Update everywhere |
| [SC-31](packets/SC-31.md) | X | CTX-00 | Authoritative release and versions |
| [SC-38](packets/SC-38.md) | X | CTX-00 | One process identity |
| [SC-93](packets/SC-93.md) | X | CTX-00 | Existing ComfyUI |
| [SC-94](packets/SC-94.md) | X | CTX-00 | Environment setup and recovery |
| [SC-90](packets/SC-90.md) | X | CTX-00 | Exact workflow setup |
| [SC-35](packets/SC-35.md) | X | CTX-00 | One home for user state |
| [SC-63](packets/SC-63.md) | X | CTX-00 | Dependable saving |
| [SC-04](packets/SC-04.md) | X | CTX-00 | Concurrent editing |
| [SC-79](packets/SC-79.md) | N | CTX-00 | Large local media |
| [SC-87](packets/SC-87.md) | X | CTX-00 | Renderer residual |
| [SC-85](packets/SC-85.md) | N | CTX-00 | One place to measure |
| [SC-56](packets/SC-56.md) | X | CTX-00 | R15 workflow setup handoff |
| [ISS-01](packets/ISS-01.md) | N | CTX-00 | Issue-first: install, updates, Pinokio and persistent state |
| [ISS-02](packets/ISS-02.md) | N | CTX-00 | Issue-first: generation, hardware, setup and execution |
| [ISS-03](packets/ISS-03.md) | N | CTX-00 | Issue-first: editing, media, rendering and project custody |
| [ISS-04](packets/ISS-04.md) | N | CTX-00 | Issue-first: first-use journey, diagnostics, proof and release regressions |
| [HOR-01](packets/HOR-01.md) | X | CTX-00 | Upcoming plans and R15 handoffs — minimal prerequisite scout |
| [INV-01](packets/INV-01.md) | X | SC-09; SC-10; SC-29; SC-30; SC-31; SC-38; ISS-01; ISS-04 | Install, update, release identity and Pinokio lifecycle |
| [INV-02](packets/INV-02.md) | S | SC-93; SC-94; SC-90; SC-56; SC-35; SC-38; ISS-02; ISS-04; HOR-01 | Environment, GPU, workflow readiness and consent architecture |
| [INV-03](packets/INV-03.md) | S | SC-63; SC-04; SC-79; SC-35; SC-87; ISS-03; HOR-01 | Dependable editing and persistence across the R16/R18 cut |
| [INV-04](packets/INV-04.md) | X | SC-35; SC-38; SC-09; SC-10; SC-90; SC-94; ISS-01; ISS-02; HOR-01 | User state, credentials, process custody and recovery seams |
| [INV-05](packets/INV-05.md) | X | SC-79; SC-87; SC-63; SC-38; SC-85; ISS-03; HOR-01 | Real media and rendering dependability |
| [INV-06](packets/INV-06.md) | X | SC-85; SC-31; SC-09; SC-10; SC-87; ISS-04; HOR-01 | Release qualification and measurement without the R17 green programme |
| [INV-07](packets/INV-07.md) | X | SC-56; SC-63; SC-87; SC-85; SC-31; HOR-01; ISS-04 | Release 15 reconciliation and implementation sequence feasibility |
| [AUD-01](packets/AUD-01.md) | X | ALL_WAVE_A_AND_B | Independent issue-to-task coverage and omission audit |
| [SYN-01](packets/SYN-01.md) | S | AUD-01; ALL_WAVE_A_AND_B | Pro synthesis — smallest coherent dependable release |
| [REV-01](packets/REV-01.md) | S | SYN-01; MATERIALISE-00 | Independent Pro review of actual proposed Release 16 documentation |
| [SC-FINAL](packets/SC-FINAL.md) | S | REV-01; REPAIR-00 | Independent whole-release strategy and sequencing sense check |

## Final three independent Pro judgments

1. **SYN-01:** consumes all original research and audit, proposes actual canonical document changes and compares credible release sequences. Choose the smallest coherent scope and explain sequencing, critical path, start/land/proof dependencies, parallel lanes, shared writers, first integrated user journey, migration/pin/rollback order, scarce proof resources and freeze. No release 17/18 scope expansion.
2. **Materialise and REV-01:** coordinator commits the actual proposed release/plan/inputs/tasks changes and proposed existing run-board lane/readiness order. Record immutable base/head and diff. Give a different fresh Pro the full original evidence and actual diff. Repair and independently re-review material findings; record exact revised head. Do not ask the reviewer to judge a hypothetical draft or only a synthesis summary.
3. **SC-FINAL:** a third fresh Pro reads the full evidence, actual revised proposal and review resolutions, steps back from line review and attacks the whole release strategy and sequencing. Return exact-head SOUND/SOUND WITH FOLLOW-UPS/REWORK/BLOCKED verdict; target re-review only at changed claims. Owner accepts scope separately.

For each reviewer write one short assignment naming role/question, route, independence/permissions, exact base/head, source register, canonical records, links to every original finding and prior verdict, expected verdict and exact report-only branch/base, proposal PR destination and report path. The reviewer pushes its own verdict but never edits the assessed proposal. Generate the actual reviewer bundle at dispatch from those pinned records, not before research exists. A temporary ZIP of referenced files is transport only; Git is the source of truth. Do not add a second release strategy document: the brief's Intent/Approach owns strategic sequence, run.md owns operational lanes, tasks.md exact project edges, decisions.md accepted rulings. No duplicate project description or dependency tracker.

Finish with the actual reviewed scope PR and evidence links, concise remaining owner decisions and explicit blockers. Do not launch product implementation or publish. Stop check-in scheduling after verified handoff.
