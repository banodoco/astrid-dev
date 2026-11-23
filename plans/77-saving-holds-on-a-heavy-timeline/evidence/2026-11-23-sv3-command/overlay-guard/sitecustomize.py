"""Fail-closed source witness for the one native SV-3 diagnostic daemon.

Only the Runtime daemon (`python -m runtime_protocol start`) receives an import finder for the complete
`astrid` package. The exact candidate package is read-only; third-party modules remain from the installed venv.
All other processes, including `up` and `down`, are unaffected.
"""
import hashlib
import importlib.abc
import importlib.util
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


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


class AgentPackageFinder(importlib.abc.MetaPathFinder):
    """Resolve every `astrid` module from the exact candidate package; never fall back to site-packages."""

    def __init__(self, manifest_path, overlay_dir):
        self.manifest_path = manifest_path
        self.overlay_dir = overlay_dir
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("overlay_dir") != str(overlay_dir):
            raise ValueError("Agent package manifest names a different overlay directory")
        if manifest.get("agent_sha") != os.environ.get("SV3_AGENT_SHA"):
            raise ValueError("Agent package manifest does not match the requested source SHA")
        if manifest.get("agent_package_tree") != os.environ.get("SV3_AGENT_PACKAGE_TREE"):
            raise ValueError("Agent package manifest does not match the requested package tree")
        if sha256_file(manifest_path) != os.environ.get("SV3_AGENT_MANIFEST_SHA256"):
            raise ValueError("Agent package manifest digest does not match the verified receipt")
        self.files = manifest.get("files", {})
        self.package_tree = manifest["agent_package_tree"]
        if not self.files:
            raise ValueError("Agent package manifest has no candidate files")
        actual_paths = {path.relative_to(overlay_dir).as_posix() for path in overlay_dir.rglob("*")
                        if path.is_file()}
        if actual_paths != set(self.files):
            raise ValueError("Agent package overlay file inventory differs from the exact manifest")
        for relative, item in self.files.items():
            path = overlay_dir / relative
            if path.is_symlink() or not path.is_file() or path.resolve(strict=True) != path:
                raise ValueError(f"unsafe Agent package file: {relative}")
            mode = "100755" if path.stat().st_mode & 0o100 else "100644"
            if mode != item.get("git_mode") or sha256_file(path) != item.get("candidate_sha256"):
                raise ValueError(f"Agent package file failed exact manifest verification: {relative}")

    def find_spec(self, fullname, path=None, target=None):
        if fullname != "astrid" and not fullname.startswith("astrid."):
            return None
        relative_parts = fullname.split(".")
        module_relative = "/".join(relative_parts) + ".py"
        package_relative = "/".join(relative_parts) + "/__init__.py"
        directory_relative = "/".join(relative_parts)
        module_path = self.overlay_dir / module_relative
        package_path = self.overlay_dir / package_relative
        package_dir = self.overlay_dir / directory_relative
        if package_relative in self.files:
            location, relative, package = package_path, package_relative, True
        elif module_relative in self.files:
            location, relative, package = module_path, module_relative, False
        elif package_dir.is_dir() and any(name.startswith(directory_relative + "/") for name in self.files):
            if package_dir.is_symlink() or package_dir.resolve(strict=True) != package_dir:
                raise ImportError(f"unsafe Agent namespace package: {package_dir}")
            spec = importlib.util.spec_from_loader(fullname, loader=None, is_package=True)
            spec.submodule_search_locations = [str(package_dir)]
            return spec
        else:
            raise ModuleNotFoundError(f"{fullname} is absent from the exact Agent package overlay")
        if location.is_symlink() or not location.is_file() or location.resolve(strict=True) != location:
            raise ImportError(f"unsafe Agent package module: {location}")
        actual = sha256_file(location)
        expected = self.files[relative].get("candidate_sha256")
        if actual != expected:
            raise ImportError(f"Agent package module {relative} has sha256 {actual}, expected {expected}")
        locations = [str(location.parent)] if package else None
        return importlib.util.spec_from_file_location(fullname, location, submodule_search_locations=locations)


def install_agent_overlay():
    raw_overlay = os.environ.get("SV3_AGENT_OVERLAY_DIR")
    raw_manifest = os.environ.get("SV3_AGENT_MANIFEST")
    if not raw_overlay and not raw_manifest:
        return None
    if not raw_overlay or not raw_manifest:
        raise ValueError("Agent package overlay and manifest must be supplied together")
    overlay_dir = Path(raw_overlay)
    manifest_path = Path(raw_manifest)
    if (overlay_dir.resolve(strict=True) != overlay_dir or manifest_path.is_symlink()
            or manifest_path.resolve(strict=True) != manifest_path):
        raise ValueError("Agent package overlay or manifest is not canonical")
    finder = AgentPackageFinder(manifest_path, overlay_dir)
    sys.meta_path.insert(0, finder)
    return finder


def record_agent_overlay(finder):
    """Record all loaded `astrid` modules and require every origin to match the candidate manifest."""
    modules = {}
    for name, module in sorted(sys.modules.items()):
        if name != "astrid" and not name.startswith("astrid."):
            continue
        file = getattr(module, "__file__", None)
        if file is None:
            paths = list(getattr(module, "__path__", ()))
            if not paths:
                raise ValueError(f"{name} has neither an Agent module file nor namespace path")
            expected_paths = []
            for raw_path in paths:
                path = Path(raw_path).resolve(strict=True)
                if not path.is_relative_to(finder.overlay_dir):
                    raise ValueError(f"{name} namespace loaded outside the Agent package overlay: {path}")
                relative_dir = path.relative_to(finder.overlay_dir).as_posix()
                if not any(key.startswith(relative_dir + "/") for key in finder.files):
                    raise ValueError(f"{name} namespace has no candidate package content: {relative_dir}")
                expected_paths.append({"directory": str(path), "relative_dir": relative_dir})
            modules[name] = {"namespace": True, "paths": expected_paths}
            continue
        path = Path(file).resolve(strict=True)
        if not path.is_relative_to(finder.overlay_dir):
            raise ValueError(f"{name} loaded outside the exact Agent package overlay: {path}")
        relative = path.relative_to(finder.overlay_dir).as_posix()
        expected = finder.files.get(relative, {}).get("candidate_sha256")
        actual = sha256_file(path)
        if expected is None or actual != expected:
            raise ValueError(f"{name} loaded with an unmanifested or mismatched Agent module: {relative}")
        modules[name] = {"file": str(path), "relative": relative, "sha256": actual}
    if not modules:
        raise ValueError("no Agent package modules were loaded")
    return {"overlay_dir": str(finder.overlay_dir), "package_tree": finder.package_tree,
            "modules": modules}


def record_daemon(argv, finder):
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
    agent = record_agent_overlay(finder) if finder else None
    pid = os.getpid()
    start = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
    if receipt.parent.resolve(strict=True) != receipt.parent:
        raise ValueError("noncanonical witness output location")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW
    with os.fdopen(os.open(receipt, flags, 0o600), "w") as stream:
        json.dump({"runtime_sha": runtime_sha, "pid": pid, "start": start,
                   "interpreter": sys.executable, "archive": str(archive),
                   "modules": {name: str(value) for name, value in modules.items()},
                   "agent_overlay": agent, "epoch_ns": time.time_ns()}, stream)
        stream.write("\n")


argv = getattr(sys, "orig_argv", ())
if any(argv[i : i + 3] == ["-m", "runtime_protocol", "start"] for i in range(len(argv) - 2)):
    try:
        finder = install_agent_overlay()
        record_daemon(argv, finder)
    except Exception as error:
        print(f"SV-3 diagnostic daemon module witness refused: {error}", file=sys.stderr, flush=True)
        os._exit(86)
