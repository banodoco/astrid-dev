Date: 2026-11-25
Kind: fix
Source: Release 15 Lead, from the Release 15 boards banodoco/astrid-dev #1757, #1776, #1777, #1824, #1834 and #1836 (24–25 November 2026), at the owner's request
Resolved by: —

Release 15's lost time was mostly waiting between sessions, not the work itself. Managers relayed on an hourly rhythm (median about 55 minutes per hop, about 170 packet-hours). Rulings came one at a time, a ChatGPT manager was stood down while its plan still had packets to come, and ChatGPT managers ran out of their roughly two-hour windows with no way for a board comment to wake them. Claude orchestrators also wrote fixes themselves under the fix-it-yourself rule, against the owner's wish that packet work stays in ChatGPT. Minor findings held landings until the owner ruled that only harm blocks. Two parties disagreed about one CI run because one counted pytest's summary counters and the other distinct ids. The Qualifier was nearly run against an App whose pins named older heads.

The Lead skill now carries two principles: decide once with the condition attached, and ship when safe (harm-only blocking, a raised bar for code that deletes user files, and a named freeze list). The release workstream replaces fix-it-yourself with "fixes are packet work", adds conditional rulings, the 20-minute cadence, keeping managers up and pins naming what ships, and counts distinct ids. The dispatch workstream adds the cadence and an end-of-window resume handoff.

Follows: 2026-11-24-dispatch-lessons
