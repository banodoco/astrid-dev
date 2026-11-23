"""Optional process-local live-delay hook, enabled only for a named trial."""
from __future__ import annotations

import contextlib
import json
import os
import re
import sys
import time

_target = os.environ.get("US2_EVIDENCE_STAGE", "")
_family = os.environ.get("US2_EVIDENCE_FAMILY", "")

if _target:
    # This runs only in the live trial's temporary PYTHONPATH directory. Keep
    # the process-local hook inert for pytest and unrelated child interpreters.
    argv = sys.argv[1:]
    active = bool("--timings" in argv and argv and ((argv[0] == "generate" and _family == "generate")
                            or (argv[0] == "timelines" and _family == "timelines")))
    if active:
        from astrid.sdk import command_timing as _ct

        _real_stage = _ct.stage
        _fired = False

        @contextlib.contextmanager
        def _delayed_stage(name):
            global _fired
            with _real_stage(name):
                matches = name == _target
                if _target == "Runtime GET /v1/objects/{digest}":
                    matches = bool(re.fullmatch(r"Runtime GET /v1/objects/sha256%3A[0-9a-f]{64}", name))
                if matches and not _fired and _ct._current.get() is not None:
                    _fired = True
                    start = time.monotonic()
                    time.sleep(1.5)
                    row = {
                        "family": argv[0],
                        "stage": name,
                        "delay_seconds": time.monotonic() - start,
                        "pid": os.getpid(),
                    }
                    with open(os.environ["US2_EVIDENCE_EVENTS"], "a", encoding="utf-8") as stream:
                        stream.write(json.dumps(row, sort_keys=True) + "\n")
                yield

        _ct.stage = _delayed_stage
