---
name: astrid-dev-gpu-validate
description: Full GPU validation. Run every default generation slot and h3_av on real GPUs across RunPod, local-managed and attached placements, within a hard budget, releasing every pod and recording one dated evidence file per run.
---

# Full GPU validation

**Outcome:** real outputs on real GPUs for every default slot and h3_av on the revision under test, a pass or fail per cell, every pod released, and one dated record in [`validation/gpu/`](../../validation/gpu/README.md). CPU proof cannot show real inference, model downloads, custom-node installs or RunPod capacity; this skill does. It was built by [Plan 34](../../plans/34-real-gpu-proof/plan.md), and real-GPU proof is this skill, run again, not a new project.

Read [the entrypoint](../astrid-dev/SKILL.md) and the [shared run contract](../astrid-dev-shared/run-contract.md). They own routing, provenance, review and authority; this skill owns only the GPU run.

## When to run it

- **On owner request:** "run full GPU validation".
- **As a release gate:** [Release](../astrid-dev-release/SKILL.md) requires a passing run on the exact candidate for any release that touches generation.

No schedule. Every run spends money, so it needs the owner's standing budget (below). Without it, stop and ask; don't start a pod.

## Budget

- **Hard cap: $20 per run** (owner, 9 Nov 2026). The first run, Plan 34, has $24.
- **Before:** read the RunPod account balance and write it in the record. If the balance is below the cap, stop and tell the owner.
- **During:** after each cell, add the pod's elapsed cost to the running spend. When the next cell's worst-case cost would pass the cap, stop: release every pod, record the cells not run as `not run (budget)`, and end.
- **After:** read the balance again; spend is the difference. If it disagrees with your running total by more than $1, say so in the record.

## Pod hygiene

- Every pod action (census, create, attach a volume, stop, terminate, balance) goes through **runpod-lifecycle** at the pin in Agent's `astrid/packs/runpod/pins.json`, or through Astrid's own `astrid machines`, which uses it. Never call the raw RunPod SDK or API.
- **Census before and after every run:** the pod count and each pod id with its status. Write both into the record.
- A pod in the "before" census that this run did not make is not yours: leave it, and tell the owner.
- Release every pod this run made, whatever happened, including on an error or an interrupted session. The run is not over until the "after" census holds no pod of yours.
- Never store, print or paste a credential. Use the credential reference the environment provides; redact any key that appears in a log before it goes in the record.

## The matrix

Rows: every slot from `astrid generate defaults --json` on the Agent revision under test, read at run time (never a hard-coded list), plus h3_av on the Matrix clip (80.886–83.305 s).

Columns:

| Placement | Where |
| --- | --- |
| `runpod` | always |
| `local` (managed install) | only where a local GPU exists; otherwise run it on the pod as a local placement and say so |
| `attached` | a ComfyUI the run starts on the pod or local GPU, reached as the user's own |

Each cell is one `(slot, placement)` pair with pass, fail or not run.

Also check what CPU cannot prove (fetch destination against the checked models root, volume reuse across pods, poll-after-start, transport under large outputs): see [Plan 34 G5](../../plans/34-real-gpu-proof/tasks.md) and record each in the evidence file.

## Step 1: VibeComfy smoke, one pod

Make one pod in the storage volume's datacenter. For each slot, run that slot's workflow **directly with VibeComfy's own commands** (`prepare`, `fetch`, `run`), with no Astrid routing. A failure here is a model or node failure, not a routing failure. This step also fills the storage volume once; the models must not be downloaded again later. Record each slot's output or its first failing line.

## Step 2: the Astrid route

On the same volume, run `astrid generate <entry> … --placement runpod` per slot, then `--placement local` and `--placement attached`. Use warm reuse and the volume cache. Record:

- the **cold** timing (first job on a fresh pod) and **warm** timings (later jobs);
- the **per-job overhead** (total time minus the ComfyUI execution time);
- that the second job **reused the warm pod** (same pod id) and that the pod was **reset** between jobs (no leftover outputs or queue);
- that no model was downloaded again.

Send each output to the owner. A slot that failed in Step 1 is marked `blocked (step 1)` here, not re-run.

## Failures

Each failing cell goes to [Bug fixing](../astrid-dev-bugfix/SKILL.md): reproduce it on CPU where possible, fix it as a repair task through [Iterate](../astrid-dev-iterate/SKILL.md) on the owning plan's integration line, then re-run that cell live. Release the pod while the fix is made unless the fix is minutes away and the budget allows. **A run ends when every cell passes or the budget is spent.**

## Evidence record

One file per run: `validation/gpu/<YYYY-MM-DD>-<short-sha>.md`, where the short sha is the Agent revision under test. Commit it to astrid-dev, and link it from the plan or release it serves.

```markdown
# GPU validation — <YYYY-MM-DD> — <short-sha>

Requested by: <owner request | release gate for <candidate>>
Budget: $<cap> · Balance before: $<x> · after: $<y> · Spend: $<x−y> (running total $<z>)

## Revisions
| Repo | SHA |
| --- | --- |
| astrid-agent | <full sha> |
| astrid-runtime | <full sha> |
| VibeComfy | <full sha> |
| runpod-lifecycle | <full sha> |

## Pods
| Pod id | GPU | Datacenter | Volume | Made by this run | Released |
| --- | --- | --- | --- | --- | --- |

Census before: <n> pods — <ids and status>
Census after: <n> pods — <ids and status>

## Step 1: VibeComfy smoke
| Slot | Workflow | Result | First failing line |
| --- | --- | --- | --- |

## Step 2: Astrid route
| Slot | runpod | local | attached | First failing line |
| --- | --- | --- | --- | --- |
| h3_av (Matrix 80.886–83.305 s) | | | | |

Timings: cold <s> · warm <s, s, …> · per-job overhead <s> · warm pod reused: <pod id, yes/no> · reset between jobs: <yes/no> · models re-downloaded: <none | which>

## Failures
| Cell | First failing line | CPU repro | Issue / repair task | Re-run result |
| --- | --- | --- | --- | --- |

## Limits
One region; the GPU types available there; not a performance qualification.
```

A cell passes only on a real output from the inner command, bound to the revisions above. A prepared-only result, a wrapper's green status or an earlier run is not a pass.

## Never

- Run without the owner's standing budget, or past the cap.
- Leave a pod running, or touch a pod this run did not make.
- Store, print or commit a credential.
- Use the raw RunPod SDK instead of runpod-lifecycle.
- Patch around a failure on the pod and call the cell passed.
