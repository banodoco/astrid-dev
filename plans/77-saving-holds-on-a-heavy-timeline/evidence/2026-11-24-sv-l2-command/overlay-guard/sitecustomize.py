"""Fail-closed module witness and Agent SDK overlay for the one native SV-3 diagnostic daemon.

Runs at interpreter start in every process that starts with this directory on sys.path. Only the Runtime daemon
(argv `-m runtime_protocol start`) records its modules and, when SV3_AGENT_OVERLAY_DIR is set, installs the Agent
SDK overlay finder. Every other process, including `up` and `down`, does nothing here.
"""
import hashlib
import importlib
import importlib.abc
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

# Exactly the two Agent SDK modules the candidate changes. Everything else is loaded from the installed package.
OVERLAY_MODULES = {
    "astrid.sdk.timeline._commit_patch": "astrid/sdk/timeline/_commit_patch.py",
    "astrid.sdk.timeline._doc_patch": "astrid/sdk/timeline/_doc_patch.py",
}


def argument(argv, name):
    hits = [i for i, field in enumerate(argv) if field == name]
    if len(hits) != 1:
        raise ValueError(f"exactly one {name} is required")
    return argv[hits[0] + 1]


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_expected_hashes(text):
    """SV3_AGENT_FILE_SHA256 is `relative/path=sha256;relative/path=sha256` with exactly the two overlay files."""
    entries = {}
    for item in text.split(";"):
        relative, separator, digest = item.partition("=")
        if not separator or relative in entries:
            raise ValueError("malformed SV3_AGENT_FILE_SHA256")
        entries[relative] = digest
    if set(entries) != set(OVERLAY_MODULES.values()) or any(len(value) != 64 for value in entries.values()):
        raise ValueError("SV3_AGENT_FILE_SHA256 must name exactly the two overlay files")
    return entries


class AgentOverlayFinder(importlib.abc.MetaPathFinder):
    """Serves the two candidate modules from the overlay directory. Every other name is left to the normal finders."""

    def __init__(self, overlay_dir, expected):
        self.overlay_dir = overlay_dir
        self.expected = expected

    def find_spec(self, fullname, path=None, target=None):
        relative = OVERLAY_MODULES.get(fullname)
        if relative is None:
            return None
        location = self.overlay_dir / relative
        if location.is_symlink() or not location.is_file():
            raise ImportError(f"agent overlay file is missing or not a regular file: {location}")
        actual = sha256_file(location)
        if actual != self.expected[relative]:
            raise ImportError(f"agent overlay file {relative} has sha256 {actual}, expected {self.expected[relative]}")
        return importlib.util.spec_from_file_location(fullname, location)


def install_agent_overlay():
    overlay = os.environ.get("SV3_AGENT_OVERLAY_DIR")
    if not overlay:
        return None
    overlay_dir = Path(overlay)
    if overlay_dir.resolve(strict=True) != overlay_dir:
        raise ValueError("agent overlay directory is not canonical")
    finder = AgentOverlayFinder(overlay_dir, parse_expected_hashes(os.environ["SV3_AGENT_FILE_SHA256"]))
    sys.meta_path.insert(0, finder)
    return finder


def record_agent_overlay(overlay_dir):
    """Imports the two overlay modules (they must come from the overlay) and records the other timeline modules."""
    modules = {}
    for name, relative in OVERLAY_MODULES.items():
        module = importlib.import_module(name)
        location = Path(module.__file__).resolve(strict=True)
        if not location.is_relative_to(overlay_dir) or location != overlay_dir / relative:
            raise ValueError(f"{name} did not load from the agent overlay: {location}")
        modules[name] = {"file": str(location), "sha256": sha256_file(location)}
    others = {}
    for name, module in sorted(sys.modules.items()):
        if name.startswith("astrid.sdk.timeline.") and name not in OVERLAY_MODULES:
            file = getattr(module, "__file__", None)
            if file:
                others[name] = str(Path(file).resolve(strict=True))
    commit = None
    try:
        commit = str(Path(importlib.import_module("astrid.sdk.timeline.commit").__file__).resolve(strict=True))
    except ImportError as error:
        commit = f"not importable: {error.__class__.__name__}"
    return {"overlay_dir": str(overlay_dir), "modules": modules, "other_timeline_modules": others,
            "astrid.sdk.timeline.commit": commit}


def record_daemon(argv):
    if not sys.dont_write_bytecode:
        raise ValueError("diagnostic child may not write bytecode")
    archive = Path(os.environ["SV3_ARCHIVE"])
    receipt = Path(os.environ["SV3_DAEMON_WITNESS"])
    runtime_sha = os.environ["SV3_RUNTIME_SHA"]
    support = Path(os.environ["SV3_SUPPORT_ROOT"])
    realm = os.environ["SV3_REALM_ID"]
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
    overlay = os.environ.get("SV3_AGENT_OVERLAY_DIR")
    agent = record_agent_overlay(Path(overlay)) if overlay else None
    pid = os.getpid()
    start = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
    if receipt.parent.resolve(strict=True) != receipt.parent:
        raise ValueError("noncanonical witness output location")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW
    with os.fdopen(os.open(receipt, flags, 0o600), "w") as stream:
        json.dump({"runtime_sha": runtime_sha, "pid": pid, "start": start,
                   "interpreter": sys.executable, "archive": str(archive),
                   "modules": {name: str(value) for name, value in modules.items()},
                   "agent_overlay": agent,
                   "epoch_ns": time.time_ns()}, stream)
        stream.write("\n")


argv = getattr(sys, "orig_argv", ())
if any(argv[i : i + 3] == ["-m", "runtime_protocol", "start"] for i in range(len(argv) - 2)):
    try:
        install_agent_overlay()
        record_daemon(argv)
    except Exception as error:
        print(f"SV-3 diagnostic daemon module witness refused: {error}", file=sys.stderr, flush=True)
        os._exit(86)
