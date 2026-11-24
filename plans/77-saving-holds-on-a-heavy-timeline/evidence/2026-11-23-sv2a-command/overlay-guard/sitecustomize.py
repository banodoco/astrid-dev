"""Fail-closed module witness for the one native diagnostic daemon."""
import json
import os
from pathlib import Path
import sys
import time


def argument(argv, name):
    hits = [i for i, field in enumerate(argv) if field == name]
    if len(hits) != 1:
        raise ValueError(f"exactly one {name} is required")
    return argv[hits[0] + 1]


def record_daemon(argv):
    if not sys.dont_write_bytecode:
        raise ValueError("diagnostic child may not write bytecode")
    archive = Path(os.environ["SV2A_ARCHIVE"])
    receipt = Path(os.environ["SV2A_DAEMON_WITNESS"])
    runtime_sha = os.environ["SV2A_RUNTIME_SHA"]
    support = Path(os.environ["SV2A_SUPPORT_ROOT"])
    realm = os.environ["SV2A_REALM_ID"]
    if archive.resolve(strict=True) != archive or archive.name != runtime_sha or (archive / ".git").exists():
        raise ValueError("unexpected candidate archive")
    if (argument(argv, "--root") != str(support / "realms" / realm)
            or argument(argv, "--support-root") != str(support)
            or argument(argv, "--realm-id") != realm
            or argument(argv, "--runtime-checkout") != str(archive)):
        raise ValueError("unexpected daemon scope")
    import runtime_protocol
    import astrid_runtime
    from runtime_protocol import timeline_commit_execution, timeline_commit_store

    modules = {
        "runtime_protocol": Path(runtime_protocol.__file__).resolve(strict=True),
        "astrid_runtime": Path(astrid_runtime.__file__).resolve(strict=True),
        "timeline_commit_execution": Path(timeline_commit_execution.__file__).resolve(strict=True),
        "timeline_commit_store": Path(timeline_commit_store.__file__).resolve(strict=True),
    }
    if any(not location.is_relative_to(archive) for location in modules.values()):
        raise ValueError("the daemon selected a Runtime package outside the exact source archive")
    pid = os.getpid()
    start = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
    if receipt.parent.resolve(strict=True) != receipt.parent:
        raise ValueError("noncanonical witness output location")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW
    with os.fdopen(os.open(receipt, flags, 0o600), "w") as stream:
        json.dump({"runtime_sha": runtime_sha, "pid": pid, "start": start,
                   "interpreter": sys.executable, "archive": str(archive),
                   "modules": {name: str(value) for name, value in modules.items()},
                   "epoch_ns": time.time_ns()}, stream)
        stream.write("\n")


argv = getattr(sys, "orig_argv", ())
if any(argv[i : i + 3] == ["-m", "runtime_protocol", "start"] for i in range(len(argv) - 2)):
    try:
        record_daemon(argv)
    except Exception as error:
        print(f"SV-2a diagnostic daemon module witness refused: {error}", file=sys.stderr, flush=True)
        os._exit(86)
