# Plan 87 handover — state for the packet sessions

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md)

Written on 24 November 2026 by the orchestrator when the work moved from one Codex manager to fresh ChatGPT packet sessions ([run board](../../releases/15/run.md#plans-87-and-89-dispatch)). The Codex manager adds its per-card detail (heads, evidence paths) in a follow-up; the facts below are enough to start. Evidence from the runs lives on the orchestrator's box under `/home/user/p87/run/`; where a packet needs a file from there, ask on the mailbox and the orchestrator copies it into `plans/87-render-works/evidence/`.

## Where the plan branch is

`release/15/plan-87` in each repository. Merged so far: Runtime `release/15/main` `24e2c929` (merge `093f1c62`); RN-7 Runtime `7946fb16` and Agent `ea02d116`; RN-6 `f58c2a16`. Not yet on it: RN-1 to RN-3 (draft astrid-agent#567, branch `p87/rn3-worker-env`; held until RN-2's own-object path has a real render), RN-4 (`p87/rn4-roots-clean`, in review).

## Cards

| Card | State | Branch and head | What remains |
|---|---|---|---|
| RN-11 CI render check | Candidate pushed | astrid-agent `p87/rn11-contract` `431312dd` | Merge the plan branch in; the built-in and fade-with-easing cases; pack-element cases after RN-4 |
| RN-9 custody retry | Candidate pushed, 119 focused Linux passes, independent static review PASS | astrid-agent `p87/rn9-custody` `ed305461` | Darwin-native and a real render unproved; high-judgment review (S) |
| RN-5 pinned pack revision | Candidate partial; the first App candidate mapped the wrong pack and was rejected | astrid-agent `p87/rn5-pack-parity` `a9c8d12f`, `p87/rn5-motion-source` `0a23e77e`; astrid-app `p87/rn5-editor-revision` `cda9fe4f` | Waits for RN-4; pin moves only by the orchestrator (`READY-PIN`) |
| RN-8 lease | Not started | none | Needs the orchestrator's long-render measurement first |
| RN-14 motion pack on a fresh install | Not started | none | Size first; waits for RN-5's pin |

## Rules that bit during the run

- **Existing tests stay unchanged.** A test added by our own unmerged commit may be revised; say which tests are new in the PR.
- **Never hand-write registry entries or timelines** in contract inputs: use the product import and commit paths. Timeline ids are unique across the whole stack. Tracks paint in reverse order: put a title track **above** an opaque background track, or the title is hidden (the first blank-frame result was this).
- **No vendored third-party code.** The RN-4 manifest reader uses `js-yaml` from the Remotion project directory when resolvable, else a strict whitelist of the base parser's shapes, and raises a named error on anything else.
- **Boundary is caller versus host.** A request never chooses filesystem roots; worker-versus-host isolation is [#1760](https://github.com/banodoco/astrid-dev/issues/1760), not this plan.
- **Fixtures shrink; limits do not move.** Plan 88 owns the `film-shaped` fixture builder.
- **Local tests:** only the card's named files; a base test a change could break may be run once by itself. Never a full suite. The 120 s pytest timeout stays; run a heavy test alone.
- **Pins:** a packet never moves one; post `READY-PIN`.
- **Easing:** `fade`, `slide-left` and `slide-up` declare `supportsEasing` and ignore it ([#1739](https://github.com/banodoco/astrid-dev/issues/1739)); RN-6 only aligned the declarations.

## The stack (orchestrator's lane)

Real renders run on an isolated installed stack at `/home/user/p87/wt-rn0-app2.env` (started with `SL1_SCRATCH=... scripts/save-loop/start-isolated-linux.sh` from a disposable App copy). It carries temporary overlays that never go on the plan branch: Runtime `24e2c929`, Agent `97d1258d` then Plan 88's `dddc2f7c`, RN-6 and RN-7. Packet sessions cannot reach `github.com` or this stack: they prove with focused tests and post `READY-PROOF`.

## Open decisions

None are waiting on a packet. The orchestrator's open items: RN-2's real own-object render (gate for #567), the landing gate into `release/15/main`, and the 30-minute lease measurement for RN-8.
