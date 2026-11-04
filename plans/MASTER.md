# Initiative plan index

This page groups the staged project plans; it is not a second status board. The root [README queue](../README.md) owns project status and human-days estimates, and the [archive](../ARCHIVE.md) owns terminal project rows. Task checkboxes in project plans track task-level work only.

## Project plans

| Sequence | Project | Focused plans |
|---:|---|---|
| 1 | Installer consent | [01 — Installer consent](01-installer-consent.md) |
| 2 | Generation | [02 — Completion](02-generation-completion.md), [03 — Integration](03-generation-merge.md) |
| 3 | Concurrent editing | [04 — Concurrent edits](04-concurrent-edits.md) |
| 4 | Remaining fixes | [05 — Remaining fixes](05-remaining-fixes.md) |
| 5 | Packs | [06 — Packs](06-packs.md) |
| 6 | Pinokio | [07 — Pinokio](07-pinokio.md) |

Plans 01–06 are the staged pre-main sequence. Generation work can be prepared independently after an explicit start, but its final integration consumes the installer increment. Pinokio begins with reconciliation of the existing historical plans. It has no blanket dependency on Packs, and Packs has no blanket dependency on Pinokio; reconciliation may establish a concrete dependency, which must then be recorded in the relevant run before it gates work.

## Shared references

- [Initiative source and donor plan](../references/PLAN.md)
- [Generation inclusion decision](../references/INCLUDING-GENERATION.md)
- [Donor manifest](../references/donor-manifest.json)
- [Portable evidence summary and source limits](../references/evidence-summary.md)

Refresh source heads, branch availability, and evidence before any later execution. These documents preserve prior planning evidence; they do not assert current source state or start product work.
