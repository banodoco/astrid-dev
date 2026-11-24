# Qualification item 2d — one real `astrid generate` on a GPU (prepared, not run)

**Run only on the owner's go and her named budget** (relayed by the Lead). The Qualifier does not spend. This is the Release 14 recipe ([publication-checklist §D](../../releases/14/evidence/publication-checklist.md)) with the Release 15 differences marked. The Qualifier's part is to have every field below ready, so the run is one command after the go.

## Before any paid command (no cost)

1. Frozen SHAs recorded: Agent, Runtime, VibeComfy, App, pinned runpod-lifecycle; Runtime schema digest; served manifest digest. The installed tuple must equal them (`astrid --version`, the install manifest).
2. `astrid generate defaults --json` → choose the smallest supported **image** entry; do not assume an entry id. `astrid generate image --help` → confirm the flags below still exist on this build.
3. Credential and account access by a non-paid check (the runpod-lifecycle skill's account check); record the result without any secret.
4. Balance and remaining approved budget, privately. Pod census (`astrid machines`, the pinned lifecycle): every pod id and state, foreign pods included. **If a foreign pod exists, leave it alone and stop.**
5. Choose absolute caps so worst-case preparation, execution and teardown fit the allowance.

## The command (parameters filled from steps 2 to 5)

```bash
astrid generate image --entry "$SUPPORTED_IMAGE_ENTRY" --placement runpod \
  --gpu "RTX 4090" --max-hourly-usd "$APPROVED_HOURLY_CAP" \
  --max-usd "$SAFE_JOB_CAP" --preparation-seconds "$PREP_LIMIT" \
  --execution-seconds "$EXEC_LIMIT" --idle-seconds "$IDLE_LIMIT" --consent paid
```

Release 15 also owes a **speed reading** for the same install: run `astrid generate image` once more against an already-warm managed install (or the owner's GPU) with `time`, and report the wall clock against the "about 3 s" target. That is Tier 2 and does not block.

## Receipt (real evidence only), saved to `evidence/qualification-<sha8>/generate/receipt.md`

| Field | Value |
| --- | --- |
| Frozen SHAs, schema digest, manifest digest | |
| Run owner, authorization link, spend ceiling, balance before | |
| Credential and account access check (no secrets) | |
| Full pod census before | |
| Chosen entry, GPU, the exact command | |
| Job id, output URI and digest; the output opened and judged usable | |
| First failure reason, if any; receipt path and cleanup | |
| Stop and terminate acknowledgements; **full pod census after (must be empty of ours)** | |
| Balance after, measured spend, remaining cap | |

A usable image **and** an account pod census after teardown with none of ours are both necessary. If custody of a pod is uncertain, release what is ours and mark the row BLOCKED; a wrapper's success is not sufficient. Use the `runpod-lifecycle` package only; no raw RunPod API or SDK.

## On the owner's machine instead

If she prefers her own GPU: the same `astrid generate image --entry "$SUPPORTED_IMAGE_ENTRY"` with the default local placement on her installed Release 15 candidate, `time`d, output opened by her. That needs her machine and her go; the Qualifier requests nothing there.
