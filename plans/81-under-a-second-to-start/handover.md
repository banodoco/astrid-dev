# Handover — Under a second to start

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md)

For the manager who takes this plan. Nothing has started. Use the [Manage skill](../../skills/roles/astrid-dev-manage/SKILL.md) and its whole-project workstream.

## First actions

1. **Read** [plan.md](plan.md), [tasks.md](tasks.md), then the research report named in each card ([evidence/](evidence/)). The reports cite lines at the commits in [inputs.md](inputs.md#source-identities); re-check each before briefing a worker.
2. **Check what is decided.** D1 to D5 in [inputs.md](inputs.md#owner-decisions) are the owner's. US-1 and US-2 need none of them.
3. **Cut `release/15/plan-81`** from `release/15/main` in astrid-agent, astrid-runtime and VibeComfy, and record the commits in the brief's Branches table and in [inputs.md](inputs.md#source-identities).
4. **Start US-1.** When it lands, run US-2 to record today's numbers before anything is made faster: those are the ceilings.
5. **Write the cache design note for RS1** while US-2 runs, and commission its review. Do not dispatch US-3, US-4 or US-5 before RS1 clears.

## Workers

The owner's standing preference since 21 November 2026 is Codex workers, Luna where the work allows, with the manager reading every diff and re-running every proof. Routes are on each card. Reviews and RS1 go to the high-judgment role.

## Standing up a Runtime to measure

This worked on 22 November 2026 in a cloud container, from source, with everything under one scratch folder (`$WORK`). It needs the Agent's dependencies installed and the Runtime checkout importable.

```bash
export HOME="$WORK/home" TMPDIR="$WORK/tmp" PYTHONDONTWRITEBYTECODE=1
export ASTRID_RUNTIME_DATA_ROOT="$WORK/data" ASTRID_RUNTIME_SOURCE_MANIFEST="$WORK/manifest.json"
export ASTRID_RUNTIME_CHECKOUT=<runtime checkout> ASTRID_PACK_HOST_PYTHON=<python> PYTHONPATH=<VibeComfy checkout> ASTRID_RUNTIME_DOOR_PORT=0
python -m astrid_runtime workspace create --realm-root "$WORK/realm" --process-control sandbox --hosted-origin off --json
python -m astrid_runtime run --hosted-origin off --json
```

In a second shell with the same environment:

```bash
python -m astrid projects create exp --name Experiment --select --json
python -m astrid timelines create --project exp --slug demo --name demo --json
python -m astrid timelines edit demo --project exp --add-layer media --layer-asset "$WORK/tiny.png" --on 0 --for 3 --track V1 --id opening --idempotency-key first --json
```

The source manifest's fields follow the Runtime fixture at astrid-runtime `tests/test_astrid_product_down.py:39`. Stop the Runtime and the host it starts when done. The full account, with timings by request, is [evidence/research-G.txt](evidence/research-G.txt).

## Known traps

- **Stale is worse than slow.** Every cache in this plan decides which code or which graph runs. If a card cannot state what makes its cache stale, it is not ready.
- **Plan 77 is in the same timeline files.** Merge its work before US-6 and US-7, and do not touch the heavy-timeline save path: that is Plan 77's loop.
- **Plan 55's template belongs to one process** (`prepared.py` near line 567 on its branch). Reusing it across commands is a design decision for RS1, not a cherry-pick.
- **`release/15/main` has 35 failing tests** in `tests/packs/runpod/test_h3_release.py` from a pinned-digest mismatch. They are not this plan's and must not be fixed here ([run board](../../releases/15/run.md)).
- **Numbers from a shared container are relative.** Use US-2's own medians as the record.
