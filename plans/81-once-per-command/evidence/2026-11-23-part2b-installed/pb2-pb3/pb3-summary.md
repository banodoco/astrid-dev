# PB-3 template bundle comparison

Read-only PB-3 evidence comparing VibeComfy base `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` with candidate `589e542a1178b2a999d10fc4f4d9803c349587a5`.

The [CSV](pb3-comparison.csv) has 53 template rows for each cache mode (cold and warm). Each row compares SHA-256 for both `workflow.py` and `workflow.vibe.json`, revision IDs, warning lists, and failures. Raw JSONL records are preserved in the adjacent `pb3-*-{cold,warm}.jsonl` files.

| Mode | Templates | Full row matches | Digest mismatches | Revision mismatches | Warning mismatches | Failure rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| cold | 53 | 53 | 0 | 0 | 0 | 0 |
| warm | 53 | 53 | 0 | 0 | 0 | 0 |

Warning and failure observations:

- **cold:**
  - base `audio/ace_step_1_5_t2a_song`: `[["PendingDeprecationWarning", "vibecomfy.templates.ref('name') is a legacy generated-template fallback; new generated templates bind InputSpec.node to node objects inside build()."]]`
  - candidate `audio/ace_step_1_5_t2a_song`: `[["PendingDeprecationWarning", "vibecomfy.templates.ref('name') is a legacy generated-template fallback; new generated templates bind InputSpec.node to node objects inside build()."]]`
  - No failures.
- **warm:**
  - base `audio/ace_step_1_5_t2a_song`: `[["PendingDeprecationWarning", "vibecomfy.templates.ref('name') is a legacy generated-template fallback; new generated templates bind InputSpec.node to node objects inside build()."]]`
  - candidate `audio/ace_step_1_5_t2a_song`: `[["PendingDeprecationWarning", "vibecomfy.templates.ref('name') is a legacy generated-template fallback; new generated templates bind InputSpec.node to node objects inside build()."]]`
  - No failures.

Reproduction commands (run from each checkout):

```sh
PYTHONHASHSEED=0 TZ=UTC LC_ALL=C.UTF-8 <venv>/bin/python /home/user/p81b/run/pb3_compare.py --mode cold --output-root /home/user/p81b/run/pb3-bundles-<arm> > /home/user/p81b/run/pb3-<arm>-cold.jsonl 2> /home/user/p81b/run/pb3-<arm>-cold.stderr
PYTHONHASHSEED=0 TZ=UTC LC_ALL=C.UTF-8 <venv>/bin/python /home/user/p81b/run/pb3_compare.py --mode warm --output-root /home/user/p81b/run/pb3-bundles-<arm> > /home/user/p81b/run/pb3-<arm>-warm.jsonl 2> /home/user/p81b/run/pb3-<arm>-warm.stderr
```

Base uses `/home/user/p81b/wt/vc-baseline.env/venv`; candidate uses `/home/user/p81b/wt/pb-3.env/venv`. Both ran Python 3.13.18, with matching `uv.lock` SHA-256 `b2886aa61f7a46e2c386bdc7f2f1d51990ef8171eac411d5494be7847bad5a18`; candidate environment was created offline with `uv sync --locked --all-groups --extra dev`. `PYTHONHASHSEED=0`, `TZ=UTC`, and `LC_ALL=C.UTF-8` were used for both. Warm mode emitted each template twice in one process and records the second emission; cold mode resets the object-info cache before each template emission.

Environment receipt: `uv pip freeze` showed identical versions for the shared application and test dependencies. The baseline environment additionally has `build`, `hatchling`, `pathspec`, `pip`, `pyproject-hooks`, `tomlkit`, and `trove-classifiers`; these packaging tools are absent from the candidate environment. The editable VibeComfy entry differs only by the checkout path. The comparison imports the project from its respective checkout and does not use those extra packaging tools.
