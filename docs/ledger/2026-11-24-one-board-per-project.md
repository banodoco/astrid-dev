Date: 2026-11-24
Kind: fix
Source: Release 15 Lead session, from the owner's decision of 24 November 2026
Resolved by: —

Release 15 reporting was inconsistent: lane orchestrators sent the Lead a direct `send_message` (the workstream said "one short report each hour" without a place), managers and packet sessions used per-plan issue mailboxes, the Lead and manage skills named no channel, and history sat in private sessions the owner could not follow. One orchestrator also lost its hourly wake when an old scheduled task was disabled, while only some workstreams said to create one. The run contract now holds one rule (a Lead board plus one board per plan or dispatch, STATUS to the parent there, `send_message` only as a doorbell, every role's own hourly scheduled task and keep-awake); the run board template carries a Boards table; each role and workstream links to it, and the duplicate keep-awake and schedule bullets are gone. Follows: 2026-11-24-dispatch-lessons
