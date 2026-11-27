# Update everywhere: remaining setups

[Final Release 16 programme review](../../releases/16/evidence/final-programme-review.md) records current dependencies, estimates and remaining decisions.

**Project:** Update everywhere: remaining setups

**Goal:** Finish Plan 29 for less common setups: Linux with systemd below 254, typed update contracts, refused cards, and update proof for Pinokio and fully local.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 2–3 engineering days remaining implementation plus 0.5–1 incremental integration/qualification days; shared P09/P10/P29/P30 total 6–11 + 3–5, counted once, excluding existing P38/P93/P94/P31 work and venue waits.

**Waiting on:** Reuse P29's landed updater; [SC-30](https://github.com/banodoco/astrid-dev/blob/75d69e848eaa0760993e7be3a7c13c5fa7a0f19c/plans/30-update-everywhere/evidence/release-16-scoping/SC-30.md) identifies older systemd worker lifecycle, normalized status/refusal, fully-local skew and genuine Pinokio update proof. Coordinate P09/P10/P29; task rows remain unchecked.

**Start:** [Astrid contributor skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md) and [domain map](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Release 16 residual

**End state:** older supported Linux systems and fully local installs have the same safe, truthful update/recovery outcome; actual Pinokio update proof is supplied once by P10.

P29's updater already exists. This plan closes its supported-route edges inside [P09's shared installation programme](../09-install-and-update-confidence/plan.md). It does not wait for an obsolete Release 10 milestone or create another resolver, status tree, installer or publication lane.

- **UR-15:** worker launch, query, settlement, permission/path safety and interrupted old-job digest compatibility on systemd 249/252 and current managers. Keep the separate P38 live-owner stop problem separate; removing `--expand-environment=no` or lowering the minimum version does not establish safe lifecycle support.
- **UR-16a/b, LA-2/4:** guard only the actually unvalidated helper/status seam using existing Runtime-owned types and shared reason meanings. Reuse existing contracts; do not add a redundant schema or change the versioned health/commit digest for equivalent update meaning.
- **UR-17, LA-1/3/5/6:** use the existing selected-install resolver and update decision, requiring both App and Runtime identities for current/no-op, preserving true local ownership and repairing interrupted paired updates. A hosted tab cannot take over a local launcher. Unknown is never latest.
- **UR-18a:** consume P10 PIN-4's real engine proof. **UR-18b:** extend the existing local page/endpoint/launcher fixture and qualify actual paired operation on the retained native routes.
- **LA-7:** expose a redacted App preparation/recovery failure through existing diagnostics. No new support subsystem.

Disjoint worker, decision and fixture work can proceed independently. Land only overlapping callback/schema hunks after their named producer. Existing `38-08U` reservations on P09/P29/P30 lifecycle joins remain authoritative; no competing writer is created here. Final proof binds one tuple and includes failure/refusal, recovery, preserved work and a successful subsequent update. Source/portable tests are implementation evidence, not native or release acceptance.

The four-plan estimate is counted once in P09. [Tasks](tasks.md) retains every UR/LA obligation and old progress; [inputs](inputs.md) links current findings and original owner decisions. [The prior complete plan](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/30-update-everywhere/plan.md) preserves historical sequencing. UR-R contributes one shared integrated review under existing limits, not two more broad planning rounds.
