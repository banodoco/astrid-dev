# Release 16 — scoping evidence and review queue

Owner direction, 25 November 2026. This is the starting assignment and evidence index, **not** an assertion that research has run. Scope [Release 16](../../../16.md) only (roadmap [PR #1956](https://github.com/banodoco/astrid-dev/pull/1956), refresh the exact proposed head). Follow [Scope release](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/shared/workstreams/scope-release.md) and [Sense check](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/shared/workstreams/sense-check.md) from [PR #1960](https://github.com/banodoco/astrid-dev/pull/1960) and [PR #1962](https://github.com/banodoco/astrid-dev/pull/1962). These are proposed Markdown-first documents: use their exact source now without prematurely cutting over Plan 73.

## Coordinator

Recover the actual active scoping branch, mailbox, sessions, original dispatched packet versions and reports first. Reuse them; never restart completed work. Import actual dispatched V3/V4 packet files unchanged, or link immutable copies. This queue is the compact assignment index for new work, not a replacement for originals already dispatched. One coordinator owns the assignment/evidence index and materialises the proposal; each ChatGPT session writes and pushes its own original report. Use one proposal destination and mailbox, with one report-only branch and draft PR per assigned packet. Follow the [ChatGPT evidence-only dispatch](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/roles/orchestrator/multi-manager-dispatch.md#evidence-only-dispatch). Existing briefs remain immutable; explicitly authorize the evidence-only path for continuing read-only assignments before they write. Preserve existing delivery runs and the [run board](../../run.md).

CTX-00: install/verify latest supported astrid-dev instructions; refresh exact planning and product source identities. Use integrated Release 15 product branches as implementation baseline and actually served pins as regression/migration comparator; check main-only changes, active PRs and pending R15 handoffs. Record SHA, role and limits. Confirm session/resume and mailbox access; verify one hourly schedule or record manual fallback. At most five active ChatGPT sessions, including reviewers/replacements; N High, X Extra High, S Pro in normal Chat. At hourly check-in verify evidence PRs and exact remote report paths, resolve blockers and dispatch ready work. The first packet alone proves direct report push, draft PR and mailbox handoff. No product edits/tests/CI/spend, relabeling, active authority changes or publication.

## Release boundary

0.1.0: reliable installation, setup, creation, import, editing, saving, rendering, recovery and updates. Retain Windows/macOS/Linux, real Pinokio, fully local routes; investigate representative mainstream RTX 20/30/40/50 Windows/Linux and compatible Apple Silicon ComfyUI. RunPod experimental, money safety mandatory. Hard cut to one product contract, preserve users' work and safe migration/rollback. All accepted R16 scope ships together. Plan 31's safe first minor and visible semantic version, using completed 58, belong here. Resolve current required-check gate vs R17 and saving gate vs R18 explicitly; no hidden waivers. Future releases only provide dependency context. Preserve active Plan 56 and Plan 91 authority and handoffs.

## Research assignments

A: all depend on CTX-00. For each project check read canonical plan/inputs/tasks, actual source, relevant issues and proofs; disposition tasks and propose minimal changes. Apply sense check proportionately. Scout problems independently before mapping them to selected projects. V4 individual briefs have the detailed questions and seed issues; keep original versions intact.

| Packet | Route | Focus |
|---|---|---|
| SC-09 | X | Install/update/rollback/removal, lived-in and interrupted states |
| SC-10 | X | Real Pinokio controls and custody across OSes |
| SC-29 | N | One update path, version/status/default-pack ownership |
| SC-30 | N | Older systemd, fully local and Pinokio updates |
| SC-31 | X | Safe semantic version, Plan 29/58 reuse, manifest and protected publication, green-gate conflict |
| SC-38 | X | Native process identity, signalling and custody |
| SC-93 | X | Existing ComfyUI discovery and verified readiness |
| SC-94 | X | Consented recoverable environment/GPU setup |
| SC-90 | X | Exact dependency plan, approval, trust, resume |
| SC-35 | X | One home for user/project state, trust and recovery |
| SC-63 | X | Save contract, lost work, conflicts, outbox, R15 proof and R18 seam |
| SC-04 | X | Retained concurrency guarantees, absorb duplicates |
| SC-79 | N | Large media, streaming, import recovery |
| SC-87 | X | Full #1938 handoff and correct/recoverable rendering |
| SC-85 | N | Reuse measurement tools, installed comparisons |
| SC-56 | X | R15 workflow setup handoff only |
| ISS-01 | N | Issue-first install/update/Pinokio/state |
| ISS-02 | N | Issue-first environment/generation/execution |
| ISS-03 | N | Issue-first save/edit/media/render/custody |
| ISS-04 | N | Issue-first onboarding/diagnostics/security/qualification |
| HOR-01 | X | Adjacent-plan prerequisites, R15 handoffs and omissions |

Search all relevant product repos and astrid-dev, open/closed/reopened and unlabeled issues, user reports, actual fixes and proof. For each finding: source identity/link, impact, severity, minimal change, owner, proof and uncertainty. No fake proof.

B: cross-project investigations receive the relevant original A reports and verify disputed claims.

| Packet | Route | Depends on | Focus |
|---|---|---|---|
| INV-01 | X | SC-09/10/29/30/31/38, ISS-01/04 | One install/update/publication lifecycle, proof and ordering |
| INV-02 | S | SC-93/94/90/56/35/38, ISS-02/04, HOR-01 | Environment/hardware/workflow readiness, consent and trust |
| INV-03 | S | SC-63/04/79/35/87, ISS-03, HOR-01 | Dependable editing/persistence, R18 seam and usability gate |
| INV-04 | X | SC-35/38/09/10/90/94, ISS-01/02, HOR-01 | State, credentials, custody, migration and recovery |
| INV-05 | X | SC-79/87/63/38/85, ISS-03, HOR-01 | Correct real media/render journeys and proof |
| INV-06 | X | SC-85/31/09/10/87, ISS-04, HOR-01 | Measurement, release gates and R17 boundary |
| INV-07 | X | SC-56/63/87/85/31, HOR-01, ISS-04 | R15 reconciliation, real dependencies and sequence feasibility |

C–F: final judgments.

- AUD-01 (X): after all A/B, reconcile issue/task coverage and omitted harm.
- SYN-01 (Pro): after AUD and all original evidence, propose the actual brief and project changes. Compare foundation-first, early vertical proof and parallel dependency-led strategies; justify start/land/proof edges, critical path, lane ownership, early integrated witnesses, migration/pin order, scarce resources, freeze and gates.
- Coordinator materialises actual proposed canonical changes and records exact diff. Intent/Approach owns strategic sequence; run.md owns operational lanes; tasks.md owns task edges. Preserve existing active authority.
- REV-01 (different Pro): inspect complete original evidence and actual materialised diff; challenge coverage, simplicity, proof, and sequence; resolve blockers and independently recheck material changes.
- SC-FINAL (third fresh Pro): after REV fixes, judge the entire revised release and strategy, independently consider simpler ordering and scope; exact reviewed head, numbered verdict and evidence. Targeted recheck only for material amendments.

## Evidence and reviewer handoff

Project-specific original findings belong in the owning project's evidence (for example `plans/<slug>/evidence/release-16-scoping/SC-NN.md`); cross-project/scout/whole-release originals belong here. Link already durable originals instead of duplicating. Before dispatch save actual assignment and source identity. Each session commits and pushes its own full original to its assigned branch and draft evidence PR and posts `READY-REPORT <repo> <PR> <head> <report-path>` in STATUS. The coordinator verifies readback, authorized report-only diff and completeness, then appends a receipt below (ID, snapshot, immutable commit/path link, limits, follow-up). Do not wait until the end; do not overwrite disagreements. No blank reports as evidence. Do not publish secrets, personal/private creator materials or raw chats; use approved restricted references.

For each final reviewer assemble one brief with role/question, exact base/head, relevant canonical records, this index and full original evidence, prior findings/resolutions, permissions, report-only branch/base, proposal PR destination and verdict path. Independent reviewers have write authority only for their own report; never the assessed proposal. Integrate evidence-only PRs only where authorized; otherwise link immutable original commits. Use manual original intake only for a documented connector failure. Attach a temporary ZIP only where necessary. The Git evidence, not the ZIP, is the lasting record. Accepted findings link into project inputs/tasks or release decisions. The existing mailbox/run board owns live state; no extra tracker.

## Receipts

No original reports have been imported or verified here yet. Recover any existing coordinator work before starting. Record the actual refreshed source snapshot and links here as evidence arrives. Scope acceptance, execution and publication are separate owner decisions.
