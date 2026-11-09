# 26 — Astrid Cloud, phase 2: cloud workspace (database, agent and files in the cloud)

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../index.md).

**Vision gaps:** [F-006 — Fully hosted workspace](../../vision/gaps/F-006-fully-hosted-workspace.md) (primary) · [F-005 — cloud execution for local-first projects](../../vision/gaps/F-005-local-files-cloud-assist.md) (supporting: the cloud agent and remote rendering) · [F-002 — safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting).

## Outcome and scope

**Run Astrid on: This computer | Astrid Cloud.** Onboarding asks this, and it can be switched back and forth at any time. Switching moves the whole workspace (projects, database, files) to the other side.

In Astrid Cloud, the creator opens astrid.haus on any browser, including a phone, with nothing installed. Their database, files, agent and renders live on their own cloud machine. They can close the browser while the agent keeps working.

It is the same Astrid: the same Runtime, SQLite database and file store, the same agent and tools, and the same Astrid Cloud account and key as [Plan 25](../25-cloud-assist-v1/plan.md).

### How it works

- **One Runtime per user, moved to a cloud machine.** The Runtime already decides every write itself:
  - one mutation at a time (`service.py:516-530`);
  - version-checked documents;
  - timeline commits that are accepted, rebased or merged (`timeline_commit_store.py:742-747`).

  So the agent (on the same machine, over loopback, unchanged) and the user's App (through Astrid Connect, below) both work on that one Runtime. There is no sync and no second copy to reconcile. The App's existing 6-second poll shows each side the other's edits.
- **Where the database is stored.**
  - The live `realm.sqlite3` and the file store sit on the machine's **persistent volume**: a disk attached to the machine that survives sleep and restarts.
  - Nothing is pulled from elsewhere at start-up.
  - The volume is protected by the Runtime's own authenticated backup (`backup.py`), copied to a private bucket. Because files are content-addressed, each backup only uploads new files plus the small database copy.
  - If the machine or its host is lost, a new machine restores the latest backup.
  - **Target: near-zero data loss.** Back up after every quiet moment and before every stop, and never let a backup be more than a few minutes old while the user is active. B2 measures this and decides whether continuous log shipping is needed to get closer to zero.
- **Turso** is not on the live path. It would mean rewriting the Runtime's stdlib-sqlite3 store. It is a later option only, for reading a workspace while its machine is off, or for an offline local copy.
- **Files live in object storage; the database stays on the volume.** Images, video and audio go to an S3-class bucket (Tigris on Fly, or similar). The database refers to them by content hash, as it does now, so timelines need no migration. Only the Runtime's file store gains a bucket backend:
  - put by digest;
  - signed reads;
  - a local cache on the machine, filled on demand for the agent's render and media views (`media_views.py:15-45`).

  This keeps the volume small, so the volume is the database plus a cache. Files cost about $0.02/GB-month instead of $0.15 on a volume, they load from a CDN, and they can be viewed while the machine sleeps. A lost machine only needs the small database restored.
- **Astrid Connect: one way to reach any of your Astrid machines.** It generalizes the App's paired relay prototype (`config/vite/pairedRelay.ts`). Every Runtime a user owns, whether their laptop or their cloud workspace, dials out to the relay under their Discord identity. Any browser signed in as that user (desktop or phone) picks a machine and works on it:
  - same-origin, with a `__Host-` cookie, so images and video load;
  - a closed route table;
  - the Runtime's credential never leaves its machine.

  **The cloud workspace is just one more of the user's machines.** Reaching a home laptop from a phone comes from the same machinery.
- **The host:** Fly Machines-class. B1 checks the requirements below on Fly first:
  - a persistent volume;
  - wake on request;
  - no charge while asleep;
  - about 2 vCPU and 4 GiB;
  - an API to create one machine per user.

  The service holds the host token.
- **Sleep:** decided inside the machine. It stops only when there is no App connected, no running or queued task and no agent turn, and only after a backup. It wakes when the App connects. The platform's own auto-stop is not used.
- **The agent's LLM: Astrid's own router.** It is a thin OpenRouter pass-through inside the Astrid Cloud service, using the team's OpenRouter key. Users pick from a **generic model chooser**; the default is **DeepSeek V4.1 Flash on OpenRouter**, already the Agent's default (`omp_agent.py:29`). The Astrid Cloud key gains the `llm` scope and reaches OMP through the Runtime, as in Plan 25. Nobody pastes a key. Local users get the same thing.
- **Transparent pass-through billing.** Everything is charged at provider cost × a **markup per category**. Markups are settings in the service, not constants: generations and LLM start at 1.6, and compute and storage may be set lower. Every ledger row stores the units, the provider cost and the markup, and the account page shows a breakdown with a public price sheet.
  - **Generations:** per output.
  - **LLM:** per token. An estimate is reserved, the actual cost settled, and the rest refunded.
  - **Compute:** per second the machine runs, at the host's rate for that machine size. The service owns start and stop, so it records each run interval. A metering job charges elapsed time every minute, once per interval and minute. Asleep costs no compute.
  - **Storage:** per GB-day, for the volume's provisioned size, object-storage bytes (a running byte count kept in Postgres as files are added and deleted) and backup bytes. It is charged daily, including while the machine sleeps.
  - A monthly check compares our meters with the host's invoice.
- **Backups the user manages.** Automatic safety backups always run (after quiet moments, before stop, at most minutes apart) and are kept for 7 days. On top of that the user can:
  - make a named backup at any time;
  - choose a schedule and retention, for example daily for 30 days;
  - restore any backup (the Runtime restores into a new realm and then switches over);
  - download a backup to their own machine;
  - delete backups.

  Backup bytes are billed as storage.
- **When the balance runs out:**
  - New generations, LLM calls and machine wakes stop at zero, with a clear message.
  - Storage keeps accruing as arrears, which are settled on the next top-up.
  - The user is told at day 0, 7, 21 and 28, with a one-click "download my workspace" throughout.
  - Topping up at any point restores everything.
  - **After 30 days unpaid, everything is deleted:** the machine, the volume, the objects in storage and the backups. Only the ledger and account rows are kept, for accounting. Deletion is checked and recorded.


**Not included:**
- live local-and-cloud sync;
- offline cloud editing;
- teams and sharing;
- per-conversation sandboxes;
- LLM providers other than OpenRouter;
- per-project moves;
- replacing local mode, which stays the default.

## Existing work and decision

The source trail is in [inputs.md](inputs.md#planning-evidence). Reused:
- the Runtime as the single authority;
- its backup and restore;
- the App's Runtime client, polling and paired relay prototype;
- the installer's foreground mode;
- OMP's OpenRouter path (`astrid agent key set openrouter` with `ASTRID_OPENROUTER_API_BASE`, `omp_agent.py:490-530`);
- Plan 25's account, key handoff, service, SQL and price table.

Rejected:
- Turso or a replicated live database;
- Litestream, which clashes with the Runtime's file-swapping upgrade (`upgrade.py:1190-1196`);
- a bearer token per request, which media tags can't carry;
- a separate relay per use case;
- the 5 Oct design's sandbox per conversation.

## Sequence and readiness

1. **Start once Plan 25 lands:** B10 (the LLM router) and B11 (the agent on it). Local users get them first.
2. **Spikes, in parallel:** B1 (host and image), B2 (durability and data loss) and B3 (Astrid Connect).
3. **RS1:** the review stop.
4. **Build:** B4–B9.
5. **The agent in the workspace:** B12.
6. **Proof:** B13.
7. **Review:** R.

Details are in [tasks.md](tasks.md). Budget and the spike spend caps are set at dispatch. Nothing is deployed for users before B13.

## Interfaces and handoff

**Consumes:** Plan 25's account, key handoff, service, SQL and price contracts, at its completion PR; the Runtime backup, restore and door; the App's Runtime client and relay prototype.

**Produces:**
- the workspace contract: one Runtime per user on a volume, its backups, sleep and wake, and restore;
- **Astrid Connect**: a user's machines reachable from any signed-in browser;
- the move contract, for the Local and Cloud switch;
- the Astrid LLM contract: an OpenRouter-compatible router, the `llm` scope, per-token billing and the model chooser;
- the metering contract: compute and storage meters, per-category markups and a transparent ledger;
- the backup contract: automatic and user-managed backups, restore and download;
- the unpaid lifecycle: freeze, notices, arrears and deletion at 30 days.

## Completion

With nothing installed, a new user picks Astrid Cloud in onboarding, signs in with Discord and buys credits. They create a project and chat with the agent on the default model. They edit the timeline while the agent edits it too, and conflicts resolve visibly. They close the browser mid-render; the render finishes and the machine sleeps afterwards. They reopen on a phone, and the machine wakes with everything there. They make a named backup and restore it. They switch to This computer, which moves the workspace down, then back to Astrid Cloud. A local user reaches their laptop from their phone through Astrid Connect.

**Negative cases:**
- a machine with a queued task does not sleep;
- a destroyed machine restores with loss inside B2's measured target;
- another user cannot reach the workspace or its media;
- a zero balance stops generations, LLM calls and wakes with a clear message;
- a workspace left unpaid for 30 days is fully deleted, objects and backups included, and a top-up on day 29 restores it;
- the ledger's compute and storage charges match the host's own usage within a stated tolerance;
- files still load while the machine sleeps;
- local mode is unchanged.

The evidence names the host, the SHAs, backup and wake timings, and the spend.
