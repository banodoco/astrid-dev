# Process ledger

Friction, ideas and fixes in astrid-dev itself: its skills, templates, checks and workflow. Findings about the product go to [astrid-dev's issues](../contribution-workflow.md#issues) instead. Rows 1–51 are in the [archive](../process-ledger.md).

**One file per entry**, named `YYYY-MM-DD-<short-slug>.md` (lowercase letters, digits and hyphens), so PRs never conflict. Format:

```
Date: 2026-11-08
Kind: papercut | issue | idea | fix
Source: where it came from (a plan, PR, run or person)
Resolved by: — (or the file name of the fix entry, without .md)

One short paragraph. A fix entry ends with "Follows: 2026-11-08-xyz".
```

**Add-only.** To resolve an entry, add a `fix` entry that follows it; never edit or delete another entry, except to fill in its `Resolved by:`. `python3 scripts/astrid_dev.py check` checks the format.
