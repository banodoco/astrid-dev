# Inputs — Astrid Cloud workspace, phase 2

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — On 9 Nov the owner described the phase 2 direction in a planning session. The database moves to the cloud, the agent runs on a remote CPU workspace, the App runs off the same database, and files are reached as URLs. It uses the same key, tools and storage method as local. The owner asked how the live App and the agent stay on the same data. The answer recorded in [plan.md](plan.md#how-the-live-app-the-agent-and-the-data-stay-in-step) is one Runtime per user on the workspace, with Turso kept off the live path. There is no traceable written approval yet. Next: the owner reviews this scope PR, confirms the one-Runtime model, and answers E1–E8 after spikes B1–B3.

**Prior art:** The same 9 Nov read-only surveys as [Plan 25](../25-cloud-assist-v1/inputs.md#planning-evidence), at the SHAs below. The findings that shape this plan:

- **Runtime storage:**
  - one stdlib-sqlite3 file per realm, `realm.sqlite3`, with WAL required, `BEGIN IMMEDIATE`, an owner-lock flock and a refusal of network filesystems (`store.py:335-342, 1505-1536`);
  - a content-addressed file store, with timelines only carrying `/v1/objects/<sha>` (`store.py:2500-2507`);
  - authenticated backup and restore of SQLite plus the file store (`backup.py:1-8, 678, 816`).
- **Concurrency:**
  - one mutation at a time (`service.py:516-530`);
  - document version checks that answer 409;
  - timeline commits accepted, rebased or merged;
  - no push channel and no timeline change feed. The App polls (`dataProvider.ts:95`).
- **Network surface:**
  - the daemon and agent client are loopback-only (`daemon.py:63-67`, `generated.py:36-40`);
  - the door accepts only Host `127.0.0.1`, the astrid.haus origin and no browser credentials (`door.py:594-608`);
  - the App's origin is fixed at build time (`connection.ts:59-77`);
  - media loads through plain `<img>` and `<video>` URLs;
  - the paired relay prototype exists (`astrid-app/config/vite/pairedRelay.ts`).
- **Agent:**
  - OMP behind the ACP bridge, forwarded through the door;
  - render and media views need verified local paths (`media_views.py:15-45`, `project_render.py:875-890`);
  - the installer assumes systemd but has a foreground mode (`installer/backend.py:389, 945`);
  - RunPod claims are GPU-only, though `h3_release.py` has a CPU pod route.
- **Outside research on 9 Nov:**
  - Turso Sync is push and pull with last-push-wins and no change notifications; its status appears beta;
  - pyturso maturity is unverified;
  - E2B, Fly Machines and Modal pricing and suspend semantics.

**Approach:** Keep the Runtime as the single authority and move it, with the agent, onto one CPU machine per user. Durability comes from a persistent volume plus Runtime backups to a bucket. Access goes through the paired relay or a remote door with cookie-authorized media. Wake and idle are policed from inside the machine. Moves and exports use backup and restore.

Alternatives considered:
- Turso as the Runtime engine;
- Turso Sync between a local and a cloud copy (two writers, last-push-wins);
- Litestream replication;
- a bucket-backed file store now;
- per-conversation sandboxes (the 5 Oct design);
- a browser that reads the database directly.

They are rejected for the reasons in [plan.md](plan.md#existing-work-and-decision).

**Challenge:** Reviewed — an independent advisor critique on 9 Nov checked the draft against code. It confirmed the one-Runtime model. It corrected:
- the claim that only the door must change (the App origin and media authorization must change too);
- Litestream, which clashes with upgrades;
- the bucket-backed file store, which breaks the agent's local-path seam.

It added the idle-watcher, no-systemd and paired-relay points. All were accepted.

**Proof and limits:** The proof is the browser-only journey in [plan.md](plan.md#completion) on the B1 host for a small cohort. Limits:
- one Runtime per user;
- no high availability: a lost machine loses work since the last backup, inside E6;
- latency and wake time are measured, not promised;
- no claim about teams, offline cloud editing or very large media libraries.

## Owner decisions

| ID | Decision | Recommendation |
|---|---|---|
| E1 | Database durability: a volume plus Runtime backups, or Turso | Volume plus backups. Revisit Turso only to read a workspace while its machine is off, or for a local offline copy |
| E2 | Workspace host (after B1): Fly Machines, RunPod CPU or E2B | Decide on B1's measurements of wake time, volume, cost and egress. Fly fits a volume with wake-on-request best; RunPod reuses our claim and lease code |
| E3 | Remote access (after B3): the paired relay or a remote door on a subdomain, and the domain layout under astrid.haus | The paired relay, if B3 shows it carries media and chat at acceptable latency |
| E4 | Workspace usage tariff: credits per active minute, idle free | Per active minute in the same ledger, at cost plus the Plan 25 markup |
| E5 | The agent's LLM key in the workspace | The user's own key (as locally), stored through the Runtime credential path ([Plan 36](../36-one-credential-path/plan.md)). Brokered inference later |
| E6 | Acceptable data loss: backup frequency | On idle, before stop, and at most every 15 minutes while active |
| E7 | Bytes in a bucket-backed file store now or later | Later, with its own reason such as volume size |
| E8 | Unit of moving: the whole workspace (realm), or per project | The whole workspace. Per-project import later |

## Source identities

| Repository | SHA | Use |
|---|---|---|
| [banodoco/astrid-runtime](https://github.com/banodoco/astrid-runtime) | `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` | Base: backup and restore, door, daemon |
| [banodoco/astrid-app](https://github.com/banodoco/astrid-app) | `a0f253ee62a1bb26c004add9822b0bae9e851fa5` | Base: Runtime connection, paired relay, Cloud entry |
| [banodoco/astrid-agent](https://github.com/banodoco/astrid-agent) | `a105de3a4852cb61b9647dfe2c920118bd29f272` | Base: OMP, chat bridge, installer foreground mode, RunPod pack |
| Plan 25 completion PR | (at its completion) | Account, key, credits and queue contracts |

Re-pin at dispatch.

## References

- [App cloud-mode overview, 5 Oct](https://github.com/banodoco/astrid-app/blob/a0f253ee62a1bb26c004add9822b0bae9e851fa5/docs/design/cloud-mode-project-overview-2026-10-05.md) and [creative workspace Runtime vision](https://github.com/banodoco/astrid-app/blob/a0f253ee62a1bb26c004add9822b0bae9e851fa5/docs/creative-workspace-runtime-vision.md). Both agree on one coordinator per realm. This plan keeps that and drops their per-user Turso and per-conversation sandboxes.
- Turso Sync: <https://docs.turso.tech/sync>. E2B billing: <https://e2b.dev/docs/billing>. Fly Machines: <https://fly.io/docs/machines/>.
