Date: 2026-11-25
Kind: fix
Source: Release 15 Lead, from the Release 15 boards banodoco/astrid-dev #1834 and #1836 and the publication of 25 November 2026
Resolved by: —

Four things in Release 15's qualification and publication cost time or nearly let harm through. First, every Remotion render on a fresh install failed with the manifest-pinned motion pack, while the plan's installed proofs had passed on a hand-prepared copy of that pack; the Qualifier caught it only by installing exactly what the manifest says. Second, a qualifier and a plan disagreed about one CI run (46 new failures against 1) because one counted pytest's summary counters. Third, which VibeComfy shipped was unclear, because the branch head differed from the commit the Agent pins. Fourth, raising the App's `required` floor at the go changed the App commit and the update path, and that forced a re-run of the update journeys. The release workstream now says that installed proofs install exactly what the manifest installs, that failures are counted as distinct ids, that what ships is what the pins name, that the `required` floor is settled before the update journeys, and that the owner's go may be conditional on the verdict.

Follows: 2026-11-25-release-15-lead-lessons
