# Candidate manifest provenance

The files `manifest-candidate.json` and `manifest-candidate-vc48.json` are the final candidate inputs prepared for a future qualification. They retain the `omp` npm override in `manifest-omp-npm.json` (`@oh-my-pi/pi-coding-agent@18.12.6`). Fresh candidate installs were staged for version and selected-pin preflight; no timing run was performed for these tuples.

| Manifest | Agent | Runtime | VibeComfy |
|---|---|---|---|
| `manifest-candidate.json` (after) | `705298cd7da2ba9c7378998b4fe5c0ee28438f81` | `72b129e5a2296dc58360a9896cc65fab9db4ad0c` | `950023c8846233f0006aac100d26b76711c42515` |
| `manifest-candidate-vc48.json` (vc48) | `b5c30e616e788308e9b6152adbc7064f2000db47` | `72b129e5a2296dc58360a9896cc65fab9db4ad0c` | `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` |

The after Agent is the local qualification commit at `/root/codex/plan-81m/run/final-agent-b5`, parent `b5c30e616e788308e9b6152adbc7064f2000db47`; it has no configured remote. The vc48 manifest uses that parent Agent revision, whose VibeComfy pin remains the vc48 baseline. The exact source diff for the after commit is preserved as `b5-final-pin-bump.diff` and `/root/codex/plan-81m/run/b5-final-pin-bump.diff`. These are local qualification inputs, not a claim that the pin change has landed in the shared Agent branch.

## Recreate the local qualification source

Start from the Agent parent in a disposable local checkout, apply the recorded source diff, and create a local commit. The repository path in the after manifest must point to that checkout:

```sh
git clone <Agent repository> final-agent-b5
git -C final-agent-b5 checkout --detach b5c30e616e788308e9b6152adbc7064f2000db47
git -C final-agent-b5 apply /path/to/b5-final-pin-bump.diff
git -C final-agent-b5 add -A
git -C final-agent-b5 -c user.name='Local qualification' -c user.email='local@example.invalid' commit -m 'Pin candidate VibeComfy for local qualification'
```

The recreated tree should match the recorded scratch commit's tree, but the recreated commit SHA will normally differ because commit metadata differs. Update the copied manifest's Agent SHA and `agent.repo` to the new local commit and checkout path before using it. Keep the checkout local; do not push this qualification commit. The committed manifest's `agent.repo` is `/root/codex/plan-81m/run/final-agent-b5` for this environment.

## Historical evidence

The recorded results elsewhere in `README.md`, `RESULTS.md`, `AB-RESULT.md`, and `ab-run-*` are historical. In particular, earlier after/`vc48` runs used Agent `bc75d6c592e16582fffc5f1ca1a6aa35508c9ddf` with VibeComfy `36ea976ffa24ac3ab5b5e48b7b279af7565d5c41`, or fallback Agent `9c95c680e645335a4a2ea8091f02b88934a2492b` with VibeComfy `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c`. Those tuples and their results remain unchanged and do not qualify the final manifests above. `pin-bump.diff` is the retained historical diff; `b5-final-pin-bump.diff` is the final source diff.
