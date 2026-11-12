difficulty: terra (X, write)

# M6: `machines claim --datacenter X` wins over the volume's datacenter, with a one-line notice; the stock wait names its cause and the override

**Repo:** Astrid. **Clone:** `/home/user/wt/c-m6` (branch `r13/machines-m6`, base `r13/machines` at `__BASE__`, which includes M1, M2 and M4). Work in this clone only.

Read first (binding): `/home/user/wt/briefs/wave3/machines-design.md` (owner decision O7: "this shouldn't necessarily pin to one data center. We should be able to override that"; and the live evidence "a volume pinning to an empty datacenter" in `/home/user/wt/briefs/wave3/usability-log.md`) and `/home/user/wt/briefs/wave3/machines-plan.md` (row **M6** and "Volume and datacenter"). After M2, GPU, datacenter and volume are claim-time choices only (`generate` no longer takes `--gpu` or `--datacenter`), so this task is about `machines claim`.

## Outcome
1. **Preferences hold an optional volume and an optional datacenter.** A saved volume implies its datacenter as a fact, not a pin.
2. **`machines claim --datacenter X`, where X differs from the saved volume's datacenter,** claims in X on ephemeral disk (no network volume) and prints one notice line on stderr, for example: `datacenter X differs from volume <name>'s datacenter <Y>; this machine uses ephemeral disk (models download to it)`. It no longer refuses. Today the refusal is in the SDK's datacenter handling (`_runpod_job_preferences`-style check "conflicts with the selected network volume's datacenter", or wherever M2 left it) and in the offer filter in `astrid/packs/runpod/target_selection.py` (about lines 288-300 and 745-755). With `--json` the notice is a field, not a stderr line. The saved preferences are unchanged.
3. **The stock wait names its cause and the override.** While waiting for capacity (`target_selection.py` about lines 575-590, `RunPod capacity attempt …: no stock yet`), and in the `stock_unavailable` message (about line 80, which still tells people to pass `--max-hourly-usd` to `generate`, which no longer exists), say what is out of stock (GPU list and datacenter) and, when a volume pins the datacenter, that `--datacenter` (or `--datacenter any`, if the provider supports it) on `machines claim` overrides it. Keep it to one line per attempt.
4. A claim with no `--datacenter` keeps using the volume and its datacenter, as today.

## Out of scope
Wording polish beyond these lines (M8 does layout and voice later; write plain, accurate lines); docs and skills (M9); integration tests (M10: list what breaks, don't edit).

## Tests
In `tests/packs/runpod/test_target_selection.py` (new tests only) and `tests/core/test_machines_claim.py`; each must fail before and pass after:
- (a) a claim with `--datacenter X` differing from the saved volume's datacenter selects an offer in X with no network volume and prints the notice once; saved preferences unchanged;
- (b) a claim without `--datacenter` still uses the volume's datacenter;
- (c) the capacity-wait line names the GPUs and datacenter and, when a volume pins the datacenter, the `--datacenter` override; the `stock_unavailable` message no longer mentions `generate --max-hourly-usd`.

Convert any existing test that pins the old refusal (it encodes the pin the owner removed, O7) and list it. Proof, from `/home/user/wt/c-m6`, before (new tests excluded) and after:
```
TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q tests/packs/runpod/test_target_selection.py tests/core/test_machines_claim.py tests/sdk/test_generation_target.py --basetemp=$PWD/.tmp-tests/pt
```
Then ruff and `git diff --check`.

__RULES__
