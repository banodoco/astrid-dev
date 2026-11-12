Date: 2026-11-12
Source: Release 13 live and offline runs, 11–12 Nov (failure 12; task T8)
About: F-003
Outcome: open

`insufficient_storage` masked the real blocker, a held slot, because the Runtime reports only the first blocker. The full blocker list is on a Runtime branch (`1269ada`) and changes the schema, so it waits until after the Release 13 candidate.
