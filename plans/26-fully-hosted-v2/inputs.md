# Inputs — Astrid Cloud, phase 2

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — In the planning session on 9 Nov the owner set the direction and the decisions below. The one Runtime per user model, Astrid Connect for reaching any machine, and Astrid's own LLM router were agreed. There is no written approval yet. Next: the owner approves this scope PR, and the host is confirmed after B1.

**Prior art:** The same 9 Nov surveys as [Plan 25](../25-cloud-assist-v1/inputs.md#planning-evidence), at the SHAs below. Findings:
- **Runtime:**
  - one stdlib-sqlite3 `realm.sqlite3` per realm, with WAL, `BEGIN IMMEDIATE`, an owner flock, and network filesystems refused (`store.py:335-342, 1505-1536`);
  - content-addressed files, with timelines holding only `/v1/objects/<sha>` (`store.py:2500-2507`);
  - authenticated backup and restore into a new inactive realm (`backup.py:1-8, 678, 816`);
  - one mutation at a time (`service.py:516-530`), version checks, and timeline rebase or merge;
  - no push channel; the App polls (`dataProvider.ts:95`).
- **Network surface:**
  - the daemon and agent client are loopback-only (`daemon.py:63-67`, `generated.py:36-40`);
  - the door accepts only Host `127.0.0.1` and refuses browser credentials (`door.py:594-608`);
  - the App's origin is fixed at build time (`connection.ts:59-77`);
  - media loads through plain `<img>` and `<video>` URLs;
  - the App's paired relay prototype (`config/vite/pairedRelay.ts`, `pairedRegistry.ts`) has an outbound WebSocket connector, a `__Host-` cookie and a closed route table, and is in-memory with invitation codes.
- **Agent:**
  - OMP behind the ACP bridge;
  - render needs local paths (`media_views.py:15-45`);
  - the installer has a foreground mode (`installer/backend.py:389, 945`);
  - OpenRouter is OMP's recommended provider and the default model is DeepSeek V4.1 Flash (`omp_agent.py:29`);
  - the key check uses `ASTRID_OPENROUTER_API_BASE` (`omp_agent.py:498`). Whether OMP's completions follow it is unverified, and B11 checks it.
- **Fly pricing** (<https://docs.fly.io/about/pricing>, 9 Nov):
  - machines are billed per second while running; shared-cpu-2x with 2 GB is $13.39/month and RAM beyond the preset is $6/GB-month;
  - volumes are $0.15/GB-month, billed even when stopped;
  - snapshots are $0.08/GB-month after 10 GB free, kept 5 days by default;
  - outbound data is $0.02/GB in North America and Europe;
  - there is no platform fee.
- **Outside research:** Turso Sync is push and pull with last-push-wins and appears to be in beta. E2B, Fly Machines and Modal pricing and suspend semantics were reviewed.

**Approach:** Move the one Runtime, with the agent, onto one cloud machine per user. The database sits on the machine's volume and files in object storage, protected by automatic and user-managed backups. Generalize the paired relay into Astrid Connect for every machine a user owns. Run the LLM through a router in the Astrid Cloud service. Bill everything as provider cost × a configurable markup per category, transparently.

Alternatives considered:
- Turso as the engine;
- Turso Sync between two copies;
- Litestream;
- a bucket-backed file store now;
- a remote door per machine;
- per-conversation sandboxes.

They are rejected in [plan.md](plan.md#existing-work-and-decision).

**Challenge:** Reviewed — an independent advisor critique on 9 Nov confirmed the one-Runtime model. It corrected the App origin and media authorization, Litestream and the bucket-backed store, and added the idle, no-systemd and paired-relay points. All were accepted.

**Proof and limits:** The proof is the journey in [plan.md](plan.md#completion) for a small cohort on the B1 host. Limits:
- one Runtime per user;
- no high availability;
- data loss bounded by B2's measured backup cadence, not zero by proof;
- latency and wake time are measured, not promised.

## Owner decisions

| ID | Decision | State |
|---|---|---|
| E1 | Database lives on the workspace volume, protected by Runtime backups to a bucket; no Turso on the live path | Decided 9 Nov |
| E2 | Host: a Fly Machines-class CPU service; B1 checks Fly first against the requirements in plan.md | Decided 9 Nov, confirmed after B1 |
| E3 | Access: Astrid Connect, the paired relay generalized to every machine a user owns (cloud workspace and local machines, from any browser including a phone) | Decided 9 Nov |
| E4 | Transparent pass-through billing: provider cost × a markup per category (generations, LLM, compute, storage). Markups are service settings, starting at 1.6, and compute and storage may be lower. Compute per running second, storage per GB-day including asleep, with the breakdown shown | Decided 9 Nov; the owner sets the markup values |
| E5 | LLM: Astrid's router (OpenRouter pass-through) in the Astrid Cloud service; a generic model chooser, defaulting to DeepSeek V4.1 Flash; the key reaches OMP through the Runtime, never pasted | Decided 9 Nov |
| E6 | Data loss: never, or very little. Automatic safety backups after quiet moments and before stop, at most minutes apart, kept 7 days. User-managed backups on top: named, scheduled, retention, restore, download, delete. Backup bytes billed as storage | Decided 9 Nov; cadence after B2 |
| E7 | Files in object storage (S3-class, for example Tigris) in phase 2, with a local cache on the machine; the database stays on the volume | Decided 9 Nov |
| E9 | Unpaid workspaces: at zero balance new work stops and storage accrues as arrears; notices at day 0, 7, 21 and 28; everything (machine, volume, objects, backups) deleted after 30 days unpaid; the ledger is kept | Decided 9 Nov |
| E8 | The Local and Cloud switch moves the whole workspace, either way, at any time | Decided 9 Nov |

## Source identities

| Repository | SHA | Use |
|---|---|---|
| [banodoco/astrid-runtime](https://github.com/banodoco/astrid-runtime) | `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` | Base: backup and restore, door, daemon |
| [banodoco/astrid-app](https://github.com/banodoco/astrid-app) | `a0f253ee62a1bb26c004add9822b0bae9e851fa5` | Base: Runtime connection, paired relay, onboarding |
| [banodoco/astrid-agent](https://github.com/banodoco/astrid-agent) | `a105de3a4852cb61b9647dfe2c920118bd29f272` | Base: OMP, chat bridge, installer foreground mode |
| Plan 25 completion PR | at its completion | Account, key handoff, service, SQL and price contracts |

Re-pin at dispatch.

## References

- [App cloud-mode overview, 5 Oct](https://github.com/banodoco/astrid-app/blob/a0f253ee62a1bb26c004add9822b0bae9e851fa5/docs/design/cloud-mode-project-overview-2026-10-05.md) and [creative workspace Runtime vision](https://github.com/banodoco/astrid-app/blob/a0f253ee62a1bb26c004add9822b0bae9e851fa5/docs/creative-workspace-runtime-vision.md). Both agree on one coordinator per realm.
- Fly Machines: <https://fly.io/docs/machines/>. Turso Sync: <https://docs.turso.tech/sync>.
