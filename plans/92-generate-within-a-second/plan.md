# Generate within a second

**Project:** Generate within a second

**Goal:** `astrid generate` is queued in under 1 s on a warm local machine, through a resident host and a thin client, and never uses a result that is out of date.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 5 to 6 engineering days.

**Waiting on:** [Plan 82](../82-reuse-across-commands/plan.md) (RA-2, RA-6), Release 16, and D3 ([inputs.md](inputs.md#owner-decisions)).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's [catalog](../../plans/index.md) row; its priority is its place in [priority.md](../../plans/priority.md).

**Vision gaps:** [F-008 — Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary). Its route does not name this plan.

## Outcome and scope

The second half of [Plan 82](../82-reuse-across-commands/plan.md) ([inputs.md](inputs.md#owner-decisions)). Plan 82 reaches about 3 s with disk caches; here the CLI becomes a thin client for a resident host that holds discovery results and prepared graphs.

The [floor experiment](../82-reuse-across-commands/evidence/2026-11-24-thin-client-floor/README.md) measured 0.32 s median with today's per-request work in the host; resident alone, without held results, is 4.33 s, so the gain comes from holding discovery and the prepared graph. Not measured: a real node list, model-root hashing, own-pack checks, a template miss.

**Included:** GS-1 to GS-5 ([tasks.md](tasks.md)). **Not included:** time from queued to a finished result; timeline commands; Wan2GP. A reused result is used only when shown current; no check is removed.

## Known risks and design rules

From the Lead's analysis (24 November 2026):

1. **Stale results** (pack install or update, own-pack edits, Astrid upgrade, ComfyUI restart, models): per-command change checks, refusals always recomputed, approval derived from the admitted bytes, plus Plan 82's RA-6.
2. **Lifecycle and upgrade:** a version handshake between CLI and host. If the host is missing or mismatched, today's full path runs, slower but correct. Both paths stay tested.
3. **Credentials:** whose session the host uses to admit the person's task (the experiment's session could not read executors). The local socket accepts only the user.
4. **Windows and macOS** process and IPC differences, related to [Plan 38](../38-one-process-identity/plan.md) (one process identity).
5. **Concurrent commands** from agents.
6. **Debuggability:** the CLI shows the host's real error and log location.
7. **Developer edits to packs** are picked up by the change checks.

## Existing work and decision

D1: resident first, supported by the floor experiment. [Plan 55](../55-local-speed/plan.md)'s branch (`24c68a270`) is the host's donor; see [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

GS-1 and GS-2, then GS-3 and GS-4, then GS-5. **Depends on:** Plan 82 (RA-2, RA-6); Plan 87 RN-4 (PB-7b). **Unresolved:** D3.

## Interfaces and handoff

**Consumes:** Plan 82's prepared template and receipt check; Plan 81's ceiling test. **Produces:** a resident host and thin client with a version handshake; the budget held by a test. No wire or store change; killing the host only slows the next command.

## Completion

- **The budget:** a real baseline with a real ComfyUI shows `generate` to queued under 1 s at the median, repeated and changed prompt.
- **Nothing stale:** each risk above has a test where the second result changes and the timings show the recompute.
- **Fallback:** with the host missing, stopped or of another version, the command still queues, slower, and says so.
- **Limits:** CI uses a stand-in ComfyUI; if a real node list takes most of a second, the budget is stated as Astrid's share. Landing and publishing remain the owner's.
