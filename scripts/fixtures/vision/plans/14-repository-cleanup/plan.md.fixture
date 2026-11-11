# Repository cleanup

**Vision role:** Foundational enabler — improves source navigability without itself proving a user-facing outcome.

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

Make Astrid's repositories easier to navigate and maintain, with clear homes for source and documentation and no unnecessary duplicate or abandoned material. This remains a draft until the cleanup inventory is bounded.

## Goal and scope

Start with Astrid Agent, then assess App, Runtime, and related first-party pack and inference repositories. Agree a bounded cleanup list for each; this is not an open-ended rewrite. The [execution host refactor](../13-execution-host-refactor/plan.md) owns the giant module. Preserve unpublished work, active experiments, required package data, and evidence that still supports releases, including required checksum manifests and dependency locks.

Coordinate with [Plan 16](../16-streamlined-agent-experience/plan.md) where agent catalogs or integration instructions overlap, so cleanup leaves one authoritative extension path.

## What we build on

An initial Agent snapshot identifies concrete files and directories to inspect. The exact snapshot and evidence limits are in [inputs.md](inputs.md); none of those candidates is approved for deletion. Also carried from [Plan 07](../07-pinokio/plan.md): the retired old-launcher Pinokio route in astrid-agent (`execute_pinokio_backend` and the M4-4a backend checks) should be removed once nothing selects it.

## Sequence

1. Inventory tracked files and establish references and packaging use before removal.
2. Agree a bounded per-repository cleanup list, with reasons to retain or remove each candidate.
3. Make small changes by repository and category; consolidate competing instructions and entry points by purpose.
4. Move useful examples or historical documentation to an appropriate home and repair links.
5. Check affected imports, entry points, packaging, documentation links, and named feature behavior.

The task outline and work remaining to scope are in [tasks.md](tasks.md).

## Completion

The agreed inventory is resolved with reasons for removals or retention, supported entry points and installed resources remain usable, and each repository has clear navigation. A filename, age, or stylistic preference alone never justifies deletion. Checks remain focused; no repository-wide test run or automatic test discovery.

## Read next

- [tasks.md](tasks.md): intended work and task scoping boundary.
- [inputs.md](inputs.md): audit evidence, source identities, and limits.
