# 14 — Repository cleanup

**Draft scope — not yet fully specified.** Current status and owner are in the [README queue](../README.md).

## Goal

Make Astrid's repositories easy to navigate and maintain: clear source and documentation homes, useful current instructions, and no unnecessary duplicate or abandoned material.

## Scope

Start with Astrid Agent, then inventory App, Runtime, and related first-party pack/inference repositories. Agree a bounded cleanup list for each; this is not an open-ended rewrite. The dedicated [execution host refactor](13-execution-host-refactor.md) owns the giant module.

## Initial audit candidates

The Agent snapshot `2958bacea3e3c7961788fa9c625dd9db0be282de` contains tracked `tests/.test_durations` (6,784,305 bytes), example material under `projects/astrid-intro/build/`, a prompt artifact under `output/imagegen/`, and repeated large card images across rendering examples. These are concrete inspection targets, not approved deletions: determine whether timing data, examples, and assets still serve a purpose. Preserve required checksum manifests and dependency locks. Establish equivalent evidence in other repositories before adding cleanup tasks there.

## Intended work and focused proof

- Inventory tracked files and distinguish current product code, tests, generated assets, useful examples, historical evidence, and temporary material. Establish references and packaging use before removal.
- Remove demonstrably obsolete or duplicated scripts, docs, artifacts, and dead code; consolidate competing instructions and entry points into one clear location per purpose.
- Move useful examples or historical documentation to an appropriate home and repair links. Preserve unpublished work, active experiments, required package data, and evidence still supporting releases.
- Where agent catalogs or integration instructions are duplicated, coordinate with [Plan 16](16-streamlined-agent-experience.md) so cleanup leaves one authoritative extension path.
- Make small changes by repository and category. Validate only affected imports, entry points, packaging, documentation links, and named feature checks; do not turn cleanup into a repository-wide test run.

## Completion

The agreed cleanup inventory is resolved with reasons for removals or retention, supported entry points and installed resources remain usable, and each repository has clear navigation. No deletion is justified solely by a filename, age, or stylistic preference.

## Before implementation

Confirm current repositories, base branches and SHAs, existing work to preserve, verified predecessor inputs, a fresh candidate branch, and the intended `pre-main` destination. Break the work into bounded tasks with difficulty levels and explicit focused checks after inspecting those inputs. Links to other projects provide context, not blanket scheduling gates. No broad suites or automatic test discovery.
