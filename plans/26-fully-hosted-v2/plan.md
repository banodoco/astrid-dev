# 26 — Astrid Cloud workspace, phase 2 (cloud database, agent and files)

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../index.md).

**Vision gaps:** [F-006 — Fully hosted workspace](../../vision/gaps/F-006-fully-hosted-workspace.md) (primary) · [F-005 — cloud execution for local-first projects](../../vision/gaps/F-005-local-files-cloud-assist.md) (supporting: the cloud agent session and remote rendering it lists) · [F-002 — safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting). Completion does not automatically close any gap.

## Outcome and scope

A creator opens Astrid in a browser, signs in with Discord, and works in their **Astrid Cloud workspace**. Their project database, files, agent and renderer all live in the cloud, and nothing is installed locally. It is the same Astrid:
- the same Runtime, with the same SQLite database format and the same file store;
- the same agent and tools;
- the same generation route and Astrid Cloud key as [Plan 25](../25-cloud-assist-v1/plan.md).

They can close the browser while the agent keeps working, reopen on another device, and move their workspace to their own machine at any time, and back.

### How the live app, the agent and the data stay in step

**Do not sync two databases. Move the one Runtime.**

The Runtime already decides every write itself:
- it takes one mutation at a time (`service.py:516-530`, `BEGIN IMMEDIATE`);
- documents use version checks that answer 409 on a stale write;
- timeline commits carry a base head and come back accepted, rebased or merged (`timeline_commit_store.py:742-747`);
- the App already polls heads every 6 seconds and reconciles (`dataProvider.ts:95, 757-833`);
- the agent and the App are both just HTTP clients, and media moves by digest, never by shared path.

So each user gets **one CPU machine** running their Runtime, the pack host, chat and the agent together:
- **Agent:** it keeps talking to the Runtime over loopback, so its code is unchanged.
- **App:** the browser App talks to that Runtime instead of `127.0.0.1:17340`, through the remote access chosen in B3.
- **Edits:** a user's timeline edit and an agent's edit meet in the same Runtime and the same `realm.sqlite3`, under the existing conflict rules.

There is no replication protocol, merge code or second authority. Neither the App nor the agent ever opens the database directly; that is the Runtime contract (`astrid-runtime/README.md:32`).

### Where the data lives

- **Database:** `realm.sqlite3` on the workspace's **persistent volume**. Its durable copy is the Runtime's own authenticated backup (`backup.py` `create_backup`, `restore_backup`), pushed to a private bucket when the machine goes idle, before it stops, and nightly. A lost machine is restored on a fresh one.
- **Turso (owner's first idea) is not on the live path.** As the Runtime's engine it would mean rewriting the stdlib-sqlite3 store: WAL and owner-lock assumptions, `PRAGMA data_version`, TEMP tables, the backup API and exact-schema checks. That buys multi-machine access a single-writer design doesn't need. It stays a later option for reading a workspace while its machine is off, or for a local offline copy (E1).
- **Files:**
  - the App already sees every file as a URL (`/v1/objects/<sha>`), served by the workspace;
  - bytes stay in the Runtime's file store on the volume and travel in the backups;
  - Plan 25 generations already arrive through the normal publish path.
  - Moving bytes themselves into a bucket-backed store is deferred (E7). The agent's render and media views need a verified local path (`astrid/sdk/media_views.py:15-45`), so it is a cross-repository change and needs its own reason, such as volume size.

### Included

- **Workspace image:** Runtime in the foreground supervising its services, the agent (OMP), chat, ffmpeg, Bun and Node/Remotion. No systemd.
- **Workspace host:** chosen by a spike, with the volume and wake-on-open.
- **Control plane:** in the same Supabase project as Plan 25:
  - a `cloud_workspaces` record;
  - one `open-workspace` function: Discord session in; workspace ensured running; a short-lived session for the App out.
  - provisioning with the user's Astrid Cloud key;
  - stop and delete.
- **Remote access:** the App picks its Runtime origin at run time, not build time (`connection.ts:59-77`, Dockerfile). Media authorized by cookie, so `<img>` and `<video>` work. Either the paired relay or a remote door (B3). A **Cloud** choice in the App.
- **Idle policy inside the machine:** it stops only with no App heartbeat, no running or queued Runtime task and no active chat turn, after a backup. The platform's own auto-stop is not used, because it would kill an agent working with the browser closed.
- **Move to cloud and back:** whole-workspace moves through backup and restore. "Export to local custody" is the same operation in reverse.
- **Rendering on the workspace:** the existing FFmpeg and Remotion paths.
- **Workspace usage in credits** (E4).
- **Delete my workspace.**

### Not included

- live local-and-cloud sync;
- offline cloud editing;
- several Runtimes per user;
- teams and sharing;
- per-conversation sandboxes;
- brokered LLM inference (E5);
- per-project import;
- a bucket-backed file store (E7);
- replacing the local-first mode, which stays the default.

## Existing work and decision

See [inputs.md](inputs.md#planning-evidence). Reused:
- the Runtime, unchanged as the authority;
- its backup and restore;
- the App's existing Runtime client and polling;
- the App's **paired relay prototype** (`config/vite/pairedRelay.ts`, `pairedRegistry.ts`, `scripts/astrid-local-connector.ts`). The Runtime machine dials out over WebSocket, the browser stays same-origin with a `__Host-` cookie, and a closed route table is enforced. It is in-memory today, with an 8-hour time-to-live and invitation codes;
- the installer's foreground mode and the worker-environment setup scripts;
- the RunPod pack's claim, lease and spend-cap pattern, if RunPod CPU wins B1;
- Plan 25's account, key, credits and generation route.

**Rejected:**
- **Turso or a replicated live database:** see above.
- **Litestream:** the Runtime's offline upgrade truncates the WAL and swaps the file (`upgrade.py:1190-1196`), and its schema check is exact (`v33_manifest.py:118-130`).
- **A bearer token per request:** media tags cannot carry it.
- **The App reading the database directly.**
- **The 5 Oct design's E2B sandbox per conversation and per-user Turso realm:** more machinery than one machine per user.

## Sequence and readiness

1. **Three spikes, independent of each other:**
   - B1: host and image;
   - B2: backup and restore across machines;
   - B3: remote access.
2. **RS1:** a review stop on the chosen architecture.
3. **Build, which can run in parallel:** the image, the control plane, remote access, the idle and backup policy, and the moves.
4. The agent in the workspace, then billing.
5. **B11:** the end-to-end proof.
6. **R:** review.

**Readiness gates:**
- Plan 25 has produced its account, key and queue contracts (A2, A4).
- The owner has answered E1–E8 after the spikes.
- The budget is approved.
- Nothing is deployed for users before B11 passes.

## Interfaces and handoff

**Consumes:**
- Plan 25's account, key, credits and queue contracts, at its completion PR;
- the Runtime backup and restore contract and its door, at the SHAs in [inputs.md](inputs.md#source-identities);
- the App's Runtime client and paired relay.

**Produces:**
1. **The workspace contract:** one Runtime per user on a volume, the image, `open-workspace`, the idle and backup policy, and restore on a new machine.
2. **The remote Runtime access contract:** session, cookie-authorized media, route table and origin chosen at run time.
3. **The move contract:** local to cloud and cloud to local, by authenticated backup.

Later hosted features build on these. Turso, bucket-backed storage and teams each need their own scope.

## Completion

In a browser with nothing installed, a new user signs in with Discord, opens a cloud workspace, creates a project and generates with credits. They edit the timeline while the agent edits it at the same time. Both see each other's changes within the poll interval, and conflicts resolve with the existing rebase and merge or a visible retry.

They close the browser mid-task, and the agent finishes. They reopen on another device, and the machine wakes with the work there. They render a video on the workspace, move the workspace to their local Astrid and back, and delete it.

**Negative cases:**
- an idle machine with a queued task does not stop;
- a destroyed machine is restored from the last backup, with the data loss inside E6;
- another user's session cannot reach this workspace or its media;
- a revoked key or a zero balance stops generations;
- the local-first mode is unchanged.

The evidence names the host, the SHAs, backup timings, wake latency and spend.
