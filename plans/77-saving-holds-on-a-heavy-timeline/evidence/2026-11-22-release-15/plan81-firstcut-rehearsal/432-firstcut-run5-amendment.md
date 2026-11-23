# Run 5 amendment — Plan 77 first-cut Runtime mirror

The first 432-clip attempt stopped in setup on 23 November 2026. The installer exited 1 at 05:05:49 UTC with 30.77 GiB free before install. The Runtime mirror could not resolve `77c38d037f98f744bd8f41c15d95429c124a8003^0`. The manager’s Run 4 block fetched the reviewed branch into the source clone but omitted an explicit ref in the private Runtime mirror. The reviewed commit existed on a remote-tracking ref in the source clone, and the bare mirror omitted it. The Agent mirror resolved its commit. The attempt stopped before restore, adoption or contact with the fixture, so it yields no first-cut read-back measurement. The Lead retained `run4` and its receipts. [Original Run 4 amendment](432-firstcut-run4-amendment.md)

The Lead authorized one final install attempt in the new owned `/root/codex/p77box/run5` root. It reuses the exact generated App `f0ffe045` and Agent `f19aed4c` commits from `exact-tuple.txt`, and the same reviewed Runtime `77c38d037f98f744bd8f41c15d95429c124a8003`. The new root has its own stack and receipts. The Lead’s manager operates it. Keep the Run 4 record and original signed backup and proof restore intact.

## Required mirror substitution before install

In section 1, after the original new-root and ownership checks, use the Run 4 generated commit values and the new Run 5 `STACK` and `RECEIPTS`. Retain the Agent mirror construction, then create the Runtime mirror by explicitly fetching the exact Runtime commit into a local branch in that mirror. Both mirrors must resolve the exact full commits before the installer runs.

```bash
# BASE_RUNTIME, STACK, RECEIPTS, AGENT_SHA and RUNTIME_SHA come from the checked setup.
RUNTIME_MIRROR="$STACK/runtime.git"
AGENT_MIRROR="$STACK/agent.git"
test ! -e "$RUNTIME_MIRROR" && test ! -L "$RUNTIME_MIRROR"
git -C "$BASE_RUNTIME" cat-file -e "$RUNTIME_SHA^{commit}"
git init --bare "$RUNTIME_MIRROR"
git -C "$RUNTIME_MIRROR" fetch --no-tags --depth=1 "file://$BASE_RUNTIME" \
  "$RUNTIME_SHA:refs/heads/runtime-reviewed"
git -C "$RUNTIME_MIRROR" symbolic-ref HEAD refs/heads/runtime-reviewed
runtime_seen=$(git -C "$RUNTIME_MIRROR" rev-parse --verify "$RUNTIME_SHA^0")
agent_seen=$(git -C "$AGENT_MIRROR" rev-parse --verify "$AGENT_SHA^0")
test "$runtime_seen" = "$RUNTIME_SHA"
test "$agent_seen" = "$AGENT_SHA"
printf 'Runtime\t%s\nAgent\t%s\n' "$runtime_seen" "$agent_seen" \
  > "$RECEIPTS/mirror-resolution.tsv"
```

The local command proof reproduced the omission with a disposable source whose second commit was reachable only through a remote-tracking ref. The ordinary bare clone failed to resolve it. The explicit fetch and local ref resolved it, and the same commands resolved the actual reviewed Runtime commit from the manager’s source clone. This verifies the mirror commands without starting an installer or touching the fixture.

Apply the same private manifest checks and only the existing mirror path overrides. Continue once from the approved 25 GiB before-install, 12 GiB after-restore and 10 GiB before-browser checks, with the existing 5 GiB emergency floor and stop rules. If either mirror or any later gate fails, preserve partial receipts. This is the final authorized install attempt. Record Run 5 separately from the Run 4 setup failure. [Signed fixture, admission and receipt rules](432-firstcut-run4-amendment.md)
