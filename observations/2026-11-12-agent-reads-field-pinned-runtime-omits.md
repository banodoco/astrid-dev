Date: 2026-11-12
Source: Release 13 live and offline runs, 11–12 Nov (smell 12; task T8)
About: F-003; Plan 50
Outcome: open

The Agent heartbeat reads `waiting_details`, which the pinned Runtime does not send; the field exists only on the unpinned Runtime `1269ada`. A consumer was written against a contract no pinned producer provides. Settled either by pinning a Runtime that sends it (a schema change, so after the candidate) or by removing the read. A recorded task response in Plan 50 RB-3 would stop the same drift recurring.
