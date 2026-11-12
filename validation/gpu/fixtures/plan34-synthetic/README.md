# Plan 34 synthetic video inputs

These are locally generated synthetic inputs, **not Matrix footage**. They support
repeatable contract and generation checks; they do not establish quality on the
Matrix scenes required by the full validation skill. No GPU execution is claimed
by packaging these files.

`synthetic-source.mp4` is a 1024×576, 24 fps, four-second clip with audio.
`synthetic-reference.png` is a 256×256 still. The manifest records their exact
hashes and byte sizes. No third-party footage was used. No separate license grant
for the generated media was recorded; do not infer one from this bundle.

The v2v request was adapted from Astrid Agent's
`tests/fixtures/h3_cpu/request.v2.json`, changing source identity to this synthetic
clip's SHA256. Its inherited Morpheus prompt does not describe real footage in
this bundle. The video-edit request was adapted from the `full-frame.v2` case in
`tests/packs/h3_av/fixtures/edit_binding.json`. These request adaptations are
covered by Agent's Apache-2.0 license, copied as `LICENSE.astrid-agent.txt`.
The i2v request references the synthetic still. Request files retain the prepared
input bytes; asset-map values have been changed to portable relative filenames.

For each mode (`i2v`, `v2v`, `video-edit`), resolve the request path and each
`<mode>.assets.json` value against this directory before constructing the CLI
inputs object, whose keys are `request` and `asset_map`. For example, in Python:

```python
import json
from pathlib import Path
bundle = Path("validation/gpu/fixtures/plan34-synthetic").resolve()
mode = "i2v"
inputs = {
    "request": str(bundle / f"{mode}.request.json"),
    "asset_map": {k: str(bundle / v) for k, v in
                  json.loads((bundle / f"{mode}.assets.json").read_text()).items()},
}
Path("/tmp/plan34-inputs.json").write_text(json.dumps(inputs))
```

Use the resulting object with `astrid generate video --entry h3 --mode i2v
--inputs-json /tmp/plan34-inputs.json --placement runpod` and the approved route
configuration. This example does not rent or authorize a pod. The current public
CLI does not expose separate `--request` or `--asset-map` flags.
