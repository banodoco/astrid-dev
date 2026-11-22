# Candidate manifest provenance

The files `manifest-candidate.json` and `manifest-candidate-vc48.json` are the final candidate inputs prepared for a future qualification. They retain the `omp` npm override in `manifest-omp-npm.json` (`@oh-my-pi/pi-coding-agent@18.12.6`). No install, fetch, or timing run was performed for these final tuples as part of this manifest update.

| Manifest | Agent | Runtime | VibeComfy |
|---|---|---|---|
| `manifest-candidate.json` (after) | `868053db361e8355089d23c69b3a72fec60e7f3b` | `72b129e5a2296dc58360a9896cc65fab9db4ad0c` | `06ad021ffc84f4ae687b144873d3745c7297c43c` |
| `manifest-candidate-vc48.json` (vc48) | `13d328dc01638b96bf7e07308737ca380f8eaef8` | `72b129e5a2296dc58360a9896cc65fab9db4ad0c` | `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` |

The after Agent is a local qualification commit whose parent is `13d328dc01638b96bf7e07308737ca380f8eaef8`. The checked-in source diff is `final-pin-bump.diff`, copied from `/root/codex/plan-81m/run/final-pin-bump.diff`; it contains the VibeComfy pin/recipe updates for `06ad021ffc84f4ae687b144873d3745c7297c43c`. The scratch checkout `/root/codex/plan-81m/final-agent-candidate` has commit `868053db361e8355089d23c69b3a72fec60e7f3b` and no configured remote. This local commit is qualification provenance, not a claim that the pin change has landed in the shared Agent branch.

## Recreate the local qualification source

Start from the Agent parent in a disposable local checkout, apply the recorded source diff, and create a local commit. The repository path in the after manifest must point to that checkout:

```sh
git clone <Agent repository> final-agent-candidate
git -C final-agent-candidate checkout --detach 13d328dc01638b96bf7e07308737ca380f8eaef8
git -C final-agent-candidate apply /path/to/final-pin-bump.diff
git -C final-agent-candidate add -A
git -C final-agent-candidate -c user.name='Local qualification' -c user.email='local@example.invalid' commit -m 'Pin candidate VibeComfy for local qualification'
```

The recreated tree should match the recorded scratch commit's tree, but the recreated commit SHA will normally differ because commit metadata differs. Update the copied manifest's Agent SHA and `agent.repo` to the new local commit and checkout path before using it. Keep the checkout local; do not push this qualification commit. The committed manifest's `agent.repo` is `/root/codex/plan-81m/final-agent-candidate` for this environment.

## Historical evidence

The recorded results elsewhere in `README.md`, `RESULTS.md`, `AB-RESULT.md`, and `ab-run-*` are historical. In particular, earlier after/`vc48` runs used Agent `bc75d6c592e16582fffc5f1ca1a6aa35508c9ddf` with VibeComfy `36ea976ffa24ac3ab5b5e48b7b279af7565d5c41`, or fallback Agent `9c95c680e645335a4a2ea8091f02b88934a2492b` with VibeComfy `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c`. Those tuples and their results remain unchanged and do not qualify the final manifests above. `pin-bump.diff` is the retained historical diff; `final-pin-bump.diff` is the final source diff.
