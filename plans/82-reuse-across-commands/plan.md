# Reuse across commands

**Project:** Reuse across commands

**Goal:** `astrid generate` on an installed Astrid is queued in about 3 s instead of about 5.8 s, because caches reuse what an earlier command worked out, and never uses a result that is out of date.

**Status:** active

**Owner:** Release 15 Plan 82 orchestrator (`session_011EzfW1e1nGMfuKEg7z7nKN`), by [packet dispatch](../../releases/15/run.md#plan-82-dispatch)

**Estimate:** About 3 to 4 engineering days.

**Waiting on:** nothing from the owner: she gave the go and decided D2 (yes) on 24 November 2026 ([inputs.md](inputs.md#owner-decisions)). RA-0b also waits on Plan 87's RN-4 reaching `release/15/main`.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's [catalog](../../plans/index.md) row; its priority is its place in [priority.md](../../plans/priority.md).

**Vision gaps:** [F-008 — Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary). Its route does not name this plan.

## Outcome and scope

Split from [Plan 81](../81-once-per-command/plan.md). This plan stops a command repeating what the one before it did: the workflow build (about 3.4 s), finding the entry (2.7 to 3.9 s), loading registries (1.5 to 1.8 s) and pack discovery. After the [floor experiment](evidence/2026-11-24-thin-client-floor/README.md) the owner kept the order: caches here, the resident host and thin client in [Plan 92](../92-generate-within-a-second/plan.md) in Release 16 ([inputs.md](inputs.md#owner-decisions)).

**The target:** about 3 s from starting `astrid generate` to admission on an installed Astrid, for a repeated and a changed prompt. Honestly: the floor experiment estimates disk caches alone near 2 s *est.*, not measured; 3 s leaves margin. Under 1 s is Plan 92's.

**Included:** shipped-pack and registry caches under the install stamp, with a read-only install; lazy imports; ComfyUI's prepared-template contract (no Wan2GP work); and RA-6, the Runtime refusing a task whose approval receipt or companion digest does not match its admitted bytes. The experiment found ten such tasks admitted and run, so RA-6 lands before any cache ships.

**The rule:** a reused result is used only when shown current; otherwise the command works it out as today and says so in its timings. **No check is removed** ([why each check](evidence/2026-11-24-why-each-check/README.md)).

**Not included:** everything resident, object-info trust, own-pack caches and node-list reuse (Plan 92); time from queued to a finished result; timeline commands.

## Existing work and decision

The [first-principles note](evidence/2026-11-23-generate-first-principles/README.md): of about 5.8 s, about 0.3 s depends on the request. [Plan 55](../55-local-speed/plan.md)'s branch (`24c68a270`) is the donor for the prepared template, which RA-2 makes content-keyed ([inputs.md](inputs.md#planning-evidence)).

## Sequence and readiness

RA-6 first; RA-0a; then RA-0b, RA-1b and RA-2; then R. **Depends on:** Plan 81 landed; Plan 87 RN-4 (PB-7b); D2. Cards: [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** Plan 81's timings and baselines. **Produces:** a written rule for each reused result; the caches; RA-6's check; a prepared template Plan 92's host can hold in memory. No wire or store change; what is kept on disk can be deleted at any time.

## Completion

- **The target:** a real baseline on an installed Astrid shows about 3 s at the median, repeated and changed prompt.
- **Nothing stale:** editing a workflow, pack file, model list or source file changes the second result, and the timings show a recompute. The graph admitted equals a full build's.
- **Refused:** a mismatched receipt or companion digest is refused; a matching one is admitted.
- **Safe to lose:** deleting what is kept only slows the next command.
- **Limits:** CI uses a stand-in ComfyUI. Landing and publishing remain the owner's.
