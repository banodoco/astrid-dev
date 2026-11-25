# Workflow set-up

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

**Project:** Workflow set-up

**Goal:** Any ComfyUI workflow, on your own ComfyUI, a managed one or a rented machine, either runs or stops with a named next step; a pack Astrid has not reviewed installs after one informed yes, and the saved workflow remembers it.

**Status:** active

**Owner:** Release 15 Lead (`session_011EzfW1gtAhRQwk8pgJMzhG`); accountable agent `session_011EzfW2ePdUMAHRAcAm3nur`

**Estimate:** About 18.5 engineering days (inferred): phase 0 about 2.5, WS-7 with recipe transport 1.5, LE-1 to LE-11 about 8, and 6.5 from the UX review (LE-12 to LE-18 and consent hardening in LE-2), of which 3.75 (LE-12 to LE-15, LE-2 hardening) are needed for the SAM run to pass; a plain 90/10 without the loose-end tasks is about 6.

**Waiting on:** Reconcile the Release 15 first-slice landing and pins against the freeze; the remaining cards and final review are marked Release 16 in [tasks](tasks.md), including the owner-run live SAM check after R. Do not close the whole plan.

**Start:** [Astrid contributor skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md) and [domain map](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): a workflow is only portable if the place it lands can be made ready for it without a person hunting for files. [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting): nothing runs another person's code without an informed yes.

## Outcome and scope

A person or their agent runs `astrid generate workflow FILE --as-entry NAME [--add URL[@REF]] [--add-model DEST=URL#sha256] [--consent code]` on any workflow and a target. Every handled state ends in a result with an issue and a fix that says who acts (`agent` or `human`) and gives either the exact command or a manual step with the command to run afterwards. A missing class is looked up once (ComfyUI-Manager, Comfy Registry, GitHub) and offered as a candidate, never installed from a guess. A pack off the reviewed list installs only after consent, with a plain warning of what its code can reach; `--add` pins the current commit; the entry remembers the approval so the next run needs no flag. On a rented or managed target nothing outside the approved refs is installed, and the target's own `doctor` check reads the target's lock, not the shipped one.

**Not included (moved to [Plan 90](../90-workflow-setup-exact-plan/plan.md), the follow-up):** a plan digest and `--apply DIGEST`, `generate requirements`, a reusable per-user trust list, Runtime and App approvals (Plan 35), update and rollback plans, running a pack's `install.py` (never), first-use model hashing, locking pip's transitive resolution (stated as "resolved at install"), identifying files by content (issue 665), a ComfyUI on another machine.

**The rule, enforced by `test_setup_next_steps.py`:** every non-success result has at least one issue; every issue links to a fix with `who` and exactly one of `argv` or `instruction{step, then_argv}`; warnings never invent a repair. Argument errors, interrupts, missing-machine exits and infrastructure faults keep today's handling.

## Existing work and decision

The parts exist: VibeComfy's resolver, lock, controlled installer and fetch receipts; Astrid's `fetch-models` digest, `align` consent and target checks, the readiness envelope and the engine's path from workflow refs to the target. The amendment joins them through one plan function, one approved-action record in the entry, a declarative dependency recipe and a refusal at the target. Evidence, alternatives and the critique are in inputs.md.

## Sequence and readiness

**Phase 0** (this lane's first cards, issue 1731): WS-0a–0e, WS-0g. **Phase 1:** the three contract cards first on day one (LE-1a, WS-7a, LE-2a), then WS-7b, LE-1b, LE-2b, a review stop (RS1), the rest of LE-3 to LE-18b, and one live run (WS-L, the owner's). **Phase 2:** WS-5. **Phase 3:** WS-6b, then R (up to two Codex Astra rounds). Critical path: WS-7a and LE-1a → LE-2b → RS1 → LE-13 → LE-11 → WS-6b → R; with three workers about 9 elapsed days, with one about 21 (inferred). [tasks.md](tasks.md) has the details and the real conflict hot spots. Recording this plan authorizes no work.

## Interfaces and handoff

**Consumes:** Plan 32's requirements manifest; VibeComfy's lock, installer, resolver and fetch, at the commit pinned for [Release 15](../../releases/15.md); issue 722's download path.

**Produces:**
- `fixes[].who`, `fixes[].argv`, `fixes[].instruction` on the existing `{status, issues, fixes}` envelope (statuses unchanged; new states are issue codes);
- `--consent code`, `--add URL[@REF]`, `--add-model`;
- `custom_node_refs` recipe fields `requirements_txt` and `pip_no_deps` carried in `extra.nodes`;
- an approval record in the entry, separate from the source refs and bound to identity plus recipe hash, so a later digest can wrap it without re-checking old approvals.

## Completion

- With SAM-Audio in no list, a dry run on a rented machine returns `blocked` with the SAM candidate (or the manual step), then `needs_consent` with the warning, then, after `--consent code`, installs exactly the approved ref; a second run is `ready` with no flag. Live: one SAM separation run on one rented machine.
- A rented-machine dry run with a missing pack is never `ready`.
- Negative cases: an unapproved ref is refused at the target with nothing cloned; two entries pinning different commits of one pack on one target are refused; a pack whose dependencies would change an installed package is refused; `install.py` is never executed; a registry 401 degrades to a candidate with a warning, not a crash.
- Limits: the consent flag can be typed by an agent; approved code runs with the target's access; the plan does not meet exact-plan approval or resumable model reconciliation.

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

Completed Stage 1 remains historical. Proposed residual handoff maps each retained R16 item into Plan 90, with the owner-reserved WS-L after Plan 90 review; no competing delivery lane. See the full mapping in tasks.md.
