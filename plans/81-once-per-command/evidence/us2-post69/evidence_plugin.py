"""External pytest recorder for US-2's real CLI samples; never records payloads."""
from __future__ import annotations

import json
import os
import threading
import time

_lock = threading.Lock()
_counts: dict[str, int] = {}


def pytest_configure(config):
    # Patch the common sampler before test modules import their function alias.
    from tests.integrations import command_latency_budgets as budgets

    original = budgets.command_sample

    def recording_sample(command, env):
        started = time.monotonic()
        sample_wall = None
        exit_code = None
        timings = []
        try:
            wall, payload = original(command, env)
            sample_wall = wall
            exit_code = 0
            candidate = payload.get("timings") if isinstance(payload, dict) else None
            if isinstance(candidate, list):
                timings = candidate
            return wall, payload
        except BaseException:
            # Preserve the unchanged test's exception; still leave evidence of
            # the command sample and elapsed time without serializing output.
            raise
        finally:
            wall_elapsed = time.monotonic() - started
            try:
                cli_index = next(i for i, item in enumerate(command) if item in {"generate", "timelines"})
                family = command[cli_index]
                subcommand = command[cli_index + 1] if cli_index + 1 < len(command) else ""
            except (StopIteration, TypeError):
                family, subcommand = "unknown", ""
            key = f"{family} {subcommand}".strip()
            safe_argv = []
            redact_next = False
            for index_arg, value in enumerate(command):
                text = str(value)
                lowered = text.lower()
                if redact_next:
                    safe_argv.append("<redacted>")
                    redact_next = False
                    continue
                if text.startswith("--") and any(word in lowered for word in ("token", "credential", "secret", "password", "api-key", "apikey")):
                    if "=" in text:
                        safe_argv.append(text.split("=", 1)[0] + "=<redacted>")
                    else:
                        safe_argv.append(text)
                        redact_next = True
                else:
                    safe_argv.append(text)
            with _lock:
                _counts[key] = _counts.get(key, 0) + 1
                index = _counts[key]
                row = {
                    "command": key,
                    "sample": index,
                    "argv": safe_argv,
                    "wall_seconds": sample_wall if sample_wall is not None else wall_elapsed,
                    "exit": exit_code,
                    "timings": timings,
                }
                with open(os.environ["US2_EVIDENCE_ROWS"], "a", encoding="utf-8") as stream:
                    stream.write(json.dumps(row, sort_keys=True) + "\n")

    budgets.command_sample = recording_sample
