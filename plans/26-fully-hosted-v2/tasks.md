# Tasks — Astrid Cloud, phase 2

[Plan](plan.md) · [Inputs](inputs.md)

**Critical path:**
1. B3, the Astrid Connect spike;
2. RS1, the review stop;
3. B6, building Astrid Connect;
4. B12, the agent in the workspace;
5. B13, the end-to-end proof;
6. R, the review rounds.

**Runs alongside:**
- B10 and B11 (the LLM router and the agent on it) start as soon as Plan 25's A2 and A3 land, independent of the workspace.
- B1 and B2 (the host and durability spikes) run in parallel with B3.

Spike spend caps are set at dispatch.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| B1 Spike, host and image: in one container, run the Runtime in the foreground, the pack host, chat, OMP, ffmpeg and Remotion on Fly Machines. Check volume, wake-on-request, sleep billing, cost and egress, plus one alternative host | X | — | spike notes; a draft image definition | Recorded run: start, render, sleep, wake with the volume intact; timings and cost recorded | [ ] |
| B2 Spike, durability and data loss: back up a busy workspace to the bucket on quiet moments and on a cadence, then restore and activate on a fresh machine, carrying the backup key. Measure time, size and worst-case loss, and test continuous log shipping if the cadence cannot get near zero | S | — | spike notes | A restore passes the Runtime's integrity checks and shows the same timeline and media; the measured worst-case loss is recorded; the E6 cadence is proposed | [ ] |
| B3 Spike, Astrid Connect: the paired relay with a persistent registry and Discord identity instead of invitation codes. A laptop Runtime and a cloud Runtime both dial out to it, and a desktop and a phone browser reach either. Includes cookie media, chat and edit round-trip times | S | — | spike notes; prototype branch only | For both machines: timeline edit round-trip time, video playback, a chat turn, and another user's session refused | [ ] |
| RS1 Review stop on host, durability and Connect (at most 2 rounds). A late mistake here would redo B4–B9 | S | B1, B2, B3 | read-only | Findings become rows `RS1.<n>`; E2 and E6 are confirmed before B4 | [ ] |
| B4 Workspace image: pinned, with the Runtime supervising its own services, no systemd, and a health endpoint | N | RS1 | an image definition in `astrid-cloud` | Builds from pinned SHAs; a cold start reaches health; services restart on crash | [ ] |
| B5 Control plane in the Astrid Cloud service: a `cloud_workspaces` table, create, wake, stop and delete, and provisioning that puts the user's key into the workspace Runtime | S | RS1, Plan 25 A3 | `astrid-cloud` workspace module and migration | Tests: one workspace per user under concurrent opens; other users refused; delete removes the machine, volume and backups; the key never reaches the browser | [ ] |
| B6 Astrid Connect build: persistent registry, Discord identity, outbound connector for any Runtime, App origin chosen at run time (`connection.ts:59-77`, Dockerfile), and a machine picker in the App | S | RS1, B5 | `astrid-app` relay (`config/vite/paired*`) and Runtime connection; the connector in `astrid-runtime` or `astrid-agent` per B3 | Playwright on a phone viewport and desktop: reach the cloud workspace and a laptop; media plays; a foreign cookie is refused; local-only mode is unchanged | [ ] |
| B7 Sleep and backup inside the machine: stop only with no App, no running or queued task and no agent turn, after a backup; back up on the E6 cadence; restore on a new machine | X | RS1, B4 | the workspace supervisor and backup scheduling | Tests: a queued task blocks sleep; a closed browser with a working agent stays up; a killed machine restores within the measured loss | [ ] |
| B8 The Local and Cloud switch: moving down and up by authenticated backup, from onboarding and settings, with a parity report | X | B2, B5, B6 | Runtime backup and restore entry points; App onboarding and settings; service upload and download | Up and back keeps the same projects, timelines and media digests; the switch is offered in onboarding | [ ] |
| B9 Workspace billing per active minute at cost × 1.6; zero balance stops new turns without data loss; shown on the account page | X | B5, B7 | `astrid-cloud` metering; App account page | Tests: minutes billed once; asleep is free; zero balance refuses cleanly | [ ] |
| B10 Astrid LLM router in the Astrid Cloud service: OpenRouter-compatible (streamed chat, a models allowlist, key check), the `llm` scope, reserve-settle-refund per request at cost × 1.6, and the team's OpenRouter key | S | Plan 25 A2, A3 | `astrid-cloud` LLM module and a migration for the `llm` scope | Tests against a fake upstream: streams relayed intact; settled once even on disconnect; zero balance or missing scope refused before any upstream call; the OpenRouter key never leaks; no overdraw under concurrency | [ ] |
| B11 Agent on the Astrid LLM: OMP's OpenRouter provider points at B10 with the key from the Runtime (no paste); a generic model chooser in the App and CLI, defaulting to DeepSeek V4.1 Flash; check that OMP's completions follow the base | X | B10, Plan 25 A6 | `astrid-agent/astrid/omp_agent.py` and its OMP config; the App model chooser | A local agent turn runs on the router with no personal OpenRouter key and shows in the ledger; changing the model works; a personal key still works | [ ] |
| B12 The agent in the workspace: OMP on B11, generation through Plan 25 with the injected key, chat through Connect, renders on the machine | X | B4, B6, B11 | `astrid-agent` workspace profile | A chat turn generates and edits the timeline while the user edits; a render completes | [ ] |
| B13 End-to-end proof of the [completion journey](plan.md#completion) and its negative cases, for a small cohort | X | B7, B8, B9, B12 | read-only on product code; an evidence note | Evidence note with host, SHAs, round-trip and wake times, backup timings and spend | [ ] |
| B14 Copy: the two choices, cost, where things live, moving, deleting and the model chooser | T | B8, B11 | App strings and docs | Copy review against the principle that the user chooses where work runs, where files stay, what is shared and what it costs | [ ] |
| R Review rounds (3) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md). Findings become rows `R<round>.<n>` below this one | [ ] |

Checks use the [shared worker environment](../../env/README.md).
