"""Receipts and checks for the SV-3 Runtime source overlay on a copied data root.

Operations: archive, inventory, prepare, preflight, postflight, owner-exited, ports-closed, stop-preview-listeners,
preview-after, reset-stage-timings, capture-stage-timings and timing-match. Process-group and trace proofs from SV-2a
are not carried over.
"""
import hashlib
import json
import os
from pathlib import Path
import socket
import stat
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import urlsplit


def digest_file(path):
    with path.open("rb") as stream:
        if sys.version_info >= (3, 11):
            return hashlib.file_digest(stream, "sha256").hexdigest()
        digest = hashlib.sha256()
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
        return digest.hexdigest()


def write_json(path, body):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(body, stream, indent=2)
        stream.write("\n")


def git_digest(kind, data):
    return hashlib.sha1(kind + b" " + str(len(data)).encode() + b"\0" + data,
                        usedforsecurity=False).digest()


def verify_archive(mirror, commit, archive, out):
    """Recompute the git tree of the extracted archive and compare it with the commit's tree in the mirror."""
    def tree(path):
        body = bytearray()
        entries = sorted(path.iterdir(), key=lambda item: os.fsencode(item.name) + (b"/" if item.is_dir() else b""))
        for entry in entries:
            mode = entry.lstat().st_mode
            if stat.S_ISDIR(mode):
                name, digest = b"40000", tree(entry)
            elif stat.S_ISREG(mode):
                data = entry.read_bytes()
                name = b"100755" if mode & stat.S_IXUSR else b"100644"
                digest = git_digest(b"blob", data)
                rows.append((entry.relative_to(archive).as_posix(), hashlib.sha256(data).hexdigest()))
            else:
                raise ValueError(f"unhandled archive entry {entry}")
            body += name + b" " + os.fsencode(entry.name) + b"\0" + digest
        return git_digest(b"tree", body)

    if not archive.is_absolute() or archive.resolve(strict=True) != archive or archive.name != commit:
        raise ValueError("candidate archive path is not bound to the exact commit")
    rows = []
    actual = tree(archive).hex()
    expected = subprocess.check_output(["git", "-C", str(mirror), "rev-parse", commit + "^{tree}"], text=True).strip()
    write_json(out / "archive-tree.json", {"runtime_sha": commit, "expected_tree": expected,
              "archive_tree": actual, "matches": actual == expected})
    if actual != expected:
        raise ValueError("archive bytes or modes do not match the git tree of the commit")
    with (out / "archive-files.sha256").open("x", encoding="utf-8") as stream:
        for path, digest in sorted(rows):
            print(f"{digest}  {path}", file=stream)


def program_inventory(program, interpreter, output):
    venv = interpreter.parent.parent
    version = venv.parent
    if not (venv / "lib/python3.11/site-packages").is_dir() or version.parent != program / "versions":
        raise ValueError("unexpected retained program layout")
    with output.open("x", encoding="utf-8") as stream:
        print("current", digest_file(program / "current"), file=stream)
        for name in ("manifest.json", "profile.json", "version.json"):
            print(name, digest_file(version / name), file=stream)
        print("interpreter", os.readlink(interpreter) if interpreter.is_symlink() else None,
              digest_file(interpreter), file=stream)
        for path in sorted(venv.rglob("*")):
            relative = path.relative_to(venv)
            library = Path("lib/python3.11/site-packages/anthropic/lib/credentials")
            private_directory = {".ssh", ".codex"} & set(relative.parts)
            unexpected_credentials = "credentials" in relative.parts and not (
                relative.is_relative_to(library) and (path.is_dir() or path.suffix in {".py", ".pyc"}))
            if path.name == ".env" or private_directory or unexpected_credentials:
                raise ValueError("private file in retained venv prevents full inventory")
            if path.is_symlink():
                print(relative, "symlink", os.readlink(path), file=stream)
            elif path.is_file():
                print(relative, "file", path.stat().st_mode & 0o777, digest_file(path), file=stream)
            elif path.is_dir():
                print(relative, "directory", path.stat().st_mode & 0o777, file=stream)
            else:
                raise ValueError(f"unexpected retained environment file {path}")


def read_json(path):
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"not a regular receipt {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def selected(support, realm, catalog):
    actual = catalog["realms"]
    if (catalog["selected_realm_id"] != realm or len(actual) != 1
            or actual[0]["realm_id"] != realm or actual[0]["data_root"] != str(support / "realms" / realm)):
        raise ValueError("selection does not match the data root it is read from")


def prepare(orig_support, work_support, realm, archive, out):
    """Rebase the COPIED catalog and source profile from the original data root to the work copy.

    catalog.json and source-profiles/astrid.json store absolute data_root paths. The original stack is only read.
    The copy is rewritten, the rewrite is checked for any residual original-data path, and the candidate profile
    is written under out for the Runtime's source manifest.
    """
    orig_data = orig_support.parent
    catalog_path = orig_support / "catalog.json"
    profile_path = orig_support / "source-profiles/astrid.json"
    catalog, old = read_json(catalog_path), read_json(profile_path)
    selected(orig_support, realm, catalog)
    if catalog["source_profiles"]["astrid"] != old or old["profile"] != "astrid":
        raise ValueError("retained profile and catalog disagree")
    for name, source in (("original-catalog.json", catalog_path), ("original-source-profile.json", profile_path)):
        with (out / name).open("xb") as stream:
            stream.write(source.read_bytes())
    work_catalog_path = work_support / "catalog.json"
    work_profile_path = work_support / "source-profiles/astrid.json"
    if digest_file(work_catalog_path) != digest_file(catalog_path) or \
            digest_file(work_profile_path) != digest_file(profile_path):
        raise ValueError("the work copy does not match the original catalog and profile before the rebase")
    rebase = {"from": str(orig_support), "to": str(work_support), "files": {}}
    rewritten = {}
    for name, path in (("catalog.json", work_catalog_path), ("source-profiles/astrid.json", work_profile_path)):
        before = digest_file(path)
        text = path.read_text(encoding="utf-8").replace(str(orig_support), str(work_support))
        if str(orig_data) in text:
            raise ValueError(f"residual original data path in rebased {name}")
        rewritten[name] = text
        rebase["files"][name] = {"sha256_before": before}
    for name, text in rewritten.items():
        (work_support / name).write_text(text, encoding="utf-8")
        rebase["files"][name]["sha256_after"] = digest_file(work_support / name)
    write_json(out / "rebase.json", rebase)
    rebased_catalog = json.loads(rewritten["catalog.json"])
    rebased_profile = json.loads(rewritten["source-profiles/astrid.json"])
    selected(work_support, realm, rebased_catalog)
    write_json(out / "rebased-original-catalog.json", rebased_catalog)
    profile = {**rebased_profile, "runtime_checkout": str(archive)}
    # The retained services.json starts the pack host and chat against the installed layout (stack/data). Write a copy
    # with every path under stack/data swapped to the work copy and name it as the service declaration, so the
    # Runtime's own supervisor starts them against the copy (a host started by anyone else is refused by its custody).
    stack_data = str(orig_support.parent.parent / "data")
    declaration = Path(old["service_declaration"])
    services = json.loads(declaration.read_text(encoding="utf-8"))

    def swap(value):
        if isinstance(value, str):
            return str(work_support.parent) + value[len(stack_data):] if value.startswith(stack_data) else value
        if isinstance(value, list):
            return [swap(item) for item in value]
        if isinstance(value, dict):
            return {key: swap(item) for key, item in value.items()}
        return value

    swapped = swap(services)
    if stack_data in json.dumps(swapped):
        raise ValueError("residual installed-layout data path in the rewritten service declaration")
    write_json(out / "services.json", swapped)
    profile["service_declaration"] = str(out / "services.json")
    write_json(out / "candidate-source-profile.json", profile)


def ports_closed():
    for port in (2400, 17500, 17501):
        with socket.socket() as sock:
            sock.settimeout(0.25)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                raise ValueError(f"reserved port {port} did not close")


def check_published(work_support, realm, archive, out):
    catalog = read_json(work_support / "catalog.json")
    selected(work_support, realm, catalog)
    staged = read_json(out / "candidate-source-profile.json")
    profile = read_json(work_support / "source-profiles/astrid.json")
    if profile != staged or catalog["source_profiles"]["astrid"] != staged:
        raise ValueError("Runtime did not publish the exact candidate profile and catalog")
    if staged["runtime_checkout"] != str(archive):
        raise ValueError("published candidate provenance lost")
    original = read_json(out / "rebased-original-catalog.json")
    expected = {**original, "source_profiles": {**original["source_profiles"], "astrid": staged}}
    if catalog != expected:
        raise ValueError("the catalog has changes outside the candidate source profile")
    return profile


def preflight(work_support, realm, archive, interpreter, out):
    profile = check_published(work_support, realm, archive, out)
    owner = read_json(work_support / "discovery.json")
    witness = read_json(out / "candidate-daemon-module.json")
    pid = witness["pid"]
    stat_fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
    endpoint = urlsplit(owner["endpoint"])
    if (witness["runtime_sha"] != archive.name or witness["interpreter"] != str(interpreter)
            or witness["archive"] != str(archive) or witness["start"] != stat_fields[19]
            or owner["pid"] != pid or owner["active_realm"] != realm
            or owner["realm_root"] != str(work_support / "realms" / realm)
            or endpoint.scheme != "http" or endpoint.hostname != "127.0.0.1" or endpoint.path
            or endpoint.query or endpoint.fragment or endpoint.username or endpoint.password or not endpoint.port):
        raise ValueError("candidate process proof disagrees with the selected live owner")
    module_proofs = {}
    package_paths = {
        "runtime_protocol": "runtime_protocol/__init__.py",
        "astrid_runtime": "astrid_runtime/__init__.py",
        "timeline_commit_execution": "runtime_protocol/timeline_commit_execution.py",
        "timeline_commit_store": "runtime_protocol/timeline_commit_store.py",
    }
    for name, relative in package_paths.items():
        path = Path(witness["modules"][name])
        if path.resolve(strict=True) != archive / relative:
            raise ValueError("candidate module resolves outside its expected archive package")
        module_proofs[name] = {"file": str(path), "sha256": digest_file(path)}
    write_json(out / "published-source-profile.json", profile)
    write_json(out / "published-catalog.json", read_json(work_support / "catalog.json"))
    exact = {**witness, "endpoint": owner["endpoint"], "instance": owner["runtime_instance_id"],
             "realm_id": realm, "realm_root": owner["realm_root"], "module_proofs": module_proofs,
             "published_runtime_checkout": str(archive)}
    write_json(out / "browser-preflight.json", exact)
    print(json.dumps(exact))


def owner_exited(out):
    witness = read_json(out / "candidate-daemon-module.json")
    process = Path(f"/proc/{witness['pid']}/stat")
    try:
        fields = process.read_text().rsplit(")", 1)[1].split()
        start = fields[19] if fields[0] not in {"Z", "X"} else None
    except FileNotFoundError:
        start = None
    if start == witness["start"]:
        raise ValueError("the exact instrumented Runtime owner is still present")


def listener_pids(port):
    """PIDs with a listening socket on a loopback port, found through /proc socket inodes. Used only for the
    TERM/KILL fallback on ports 2400 and 17500, as in the SV-2a package."""
    inodes = set()
    for name in ("tcp", "tcp6"):
        try:
            lines = Path(f"/proc/net/{name}").read_text().splitlines()[1:]
        except OSError:
            continue
        for line in lines:
            fields = line.split()
            if fields[3] == "0A" and int(fields[1].rsplit(":", 1)[1], 16) == port:
                inodes.add(fields[9])
    owners = set()
    for entry in os.listdir("/proc") if inodes else ():
        try:
            names = os.listdir(f"/proc/{entry}/fd") if entry.isdigit() else ()
        except OSError:
            continue
        for name in names:
            try:
                target = os.readlink(f"/proc/{entry}/fd/{name}")
            except OSError:
                continue
            if target.startswith("socket:[") and target[8:-1] in inodes:
                owners.add(int(entry))
    return sorted(owners)


def stop_preview_listeners():
    """Fallback only: TERM, then KILL, whatever still listens on ports 2400 and 17500."""
    import signal
    import time
    for sig, tries in ((signal.SIGTERM, 100), (signal.SIGKILL, 50)):
        pids = sorted(set(listener_pids(2400)) | set(listener_pids(17500)))
        if not pids:
            return
        for pid in pids:
            try:
                os.kill(pid, sig)
            except OSError:
                pass
        for _ in range(tries):
            if not (listener_pids(2400) or listener_pids(17500)):
                return
            time.sleep(0.1)


def preview_after(out):
    listeners = listener_pids(2400)
    proxy = listener_pids(17500)
    write_json(out / "preview-after.json", {"port_2400_listener_pids": listeners,
                                            "port_17500_listener_pids": proxy,
                                            "ports_closed": not listeners and not proxy})
    if listeners or proxy:
        raise ValueError("port 2400 or 17500 is still listening after stop")


def audit_tree(tree, out):
    """Link audit before the pristine copy. Fails on a symlink that resolves outside the tree, and on a regular file
    whose hard links are not all inside the tree (its inode has more links than entries found inside)."""
    tree = Path(tree)
    root = os.path.realpath(tree)
    findings, symlinks, inside_count, nlink, samples = [], 0, {}, {}, {}
    for dirpath, dirnames, filenames in os.walk(tree, followlinks=False):
        for name in dirnames + filenames:
            path = os.path.join(dirpath, name)
            info = os.lstat(path)
            if stat.S_ISLNK(info.st_mode):
                symlinks += 1
                target = os.path.realpath(path)
                if not (target == root or target.startswith(root + os.sep)):
                    findings.append({"kind": "symlink_outside_tree", "path": os.path.relpath(path, tree),
                                     "link_text": os.readlink(path), "resolves": target})
            elif stat.S_ISREG(info.st_mode) and info.st_nlink > 1:
                inside_count[info.st_ino] = inside_count.get(info.st_ino, 0) + 1
                nlink[info.st_ino] = info.st_nlink
                samples.setdefault(info.st_ino, os.path.relpath(path, tree))
    for inode, links in nlink.items():
        if inside_count[inode] != links:
            findings.append({"kind": "hardlink_with_links_outside_tree", "path": samples[inode],
                             "link_count": links, "links_inside_tree": inside_count[inode]})
    write_json(Path(out), {"tree": str(tree), "symlinks": symlinks, "multi_link_files": len(nlink),
                           "findings": findings, "ok": not findings})
    if findings:
        raise ValueError(f"link audit found {len(findings)} finding(s); see {out}")

def capture_stage_timings(rep_dir, work_data, idle_safe_stop):
    """Copy the per-copy Runtime's raw timing sink and rotations into the repetition receipt."""
    rep, work = Path(rep_dir), Path(work_data)
    receipt_path = rep / "timing-sink-capture.json"
    if receipt_path.exists():
        return read_json(receipt_path)
    source = work / "logs/commit-stage-timings.jsonl"
    target_dir = rep / "timing-sink"
    names = [source.name + suffix for suffix in (".3", ".2", ".1", "")]
    files = []
    error = None
    target_dir.mkdir(mode=0o700)
    for name in names:
        path = source.with_name(name)
        if not path.exists() and not path.is_symlink():
            continue
        if path.is_symlink() or not path.is_file():
            error = f"unsafe Runtime timing sink entry: {path}"
            break
        data = path.read_bytes()
        output = target_dir / name
        with output.open("xb") as stream:
            stream.write(data)
        files.append({"file": f"timing-sink/{name}", "source": str(path), "bytes": len(data),
                      "lines": len(data.splitlines()), "sha256": hashlib.sha256(data).hexdigest()})
    reset_receipt = read_json(rep / "timing-sink-reset.json") if (rep / "timing-sink-reset.json").is_file() else None
    status = "error" if error else ("unscoped" if reset_receipt is None else ("captured" if files else "missing"))
    idle_safe = idle_safe_stop is True or str(idle_safe_stop).lower() in {"1", "true", "yes"}
    receipt = {"status": status, "runtime_work_data": str(work), "idle_safe_stop": idle_safe,
               "captured_at_utc": datetime.now(timezone.utc).isoformat(),
               "source_base": str(source), "files": files, "reset_receipt": reset_receipt,
               "error": error}
    write_json(receipt_path, receipt)
    if error:
        raise ValueError(error)
    return receipt


def reset_stage_timings(work_data, out, rep_dir):
    """Remove only known timing sink files from the disposable work-copy before this repetition starts."""
    work, output, rep = Path(work_data), Path(out).resolve(strict=True), Path(rep_dir)
    if (work.is_symlink() or work.parent != output or not work.name.startswith("work-data-")
            or work.resolve(strict=True) != work):
        raise ValueError("timing sink reset is not scoped to a canonical repetition copy")
    logs = work / "logs"
    if logs.is_symlink() or (logs.exists() and (not logs.is_dir() or logs.resolve(strict=True) != logs)):
        raise ValueError("copied Runtime logs directory is unsafe")
    removed = []
    names = ["commit-stage-timings.jsonl", "commit-stage-timings.jsonl.1",
             "commit-stage-timings.jsonl.2", "commit-stage-timings.jsonl.3"]
    if logs.exists():
        for name in names:
            path = logs / name
            if not path.exists() and not path.is_symlink():
                continue
            if path.is_symlink() or not path.is_file() or path.resolve(strict=True) != path:
                raise ValueError(f"unsafe copied Runtime timing sink entry: {path}")
            path.unlink()
            removed.append(name)
    write_json(rep / "timing-sink-reset.json", {
        "work_copy": str(work), "logs_directory": str(logs), "removed_known_files": removed,
        "reset_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "only four known timing sink files inside the disposable work copy"})


def timing_match(rep_dir):
    """Pair raw sink JSONL records with commit POSTs and preserve each payload, including `covers` counters."""
    rep = Path(rep_dir)
    browser = read_json(rep / "browser-sv3-measure.json")
    capture = read_json(rep / "timing-sink-capture.json")
    lines = []
    raw_lines = []
    for item in capture.get("files", []):
        path = rep / item["file"]
        data = path.read_bytes()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError(f"captured Runtime timing sink changed: {path}")
        for raw in data.decode("utf-8").splitlines():
            raw_lines.append(raw)
            try:
                parsed = json.loads(raw)
                lines.append(parsed if isinstance(parsed, dict) else None)
            except ValueError:
                lines.append(None)
    with (rep / "commit-timing-lines.jsonl").open("x", encoding="utf-8") as stream:
        for raw in raw_lines:
            stream.write(raw + "\n")
    order = []
    for scenario in browser["scenarios"]:
        if scenario.get("mode") == "burst":
            order.append((scenario["name"], None, (scenario.get("burst") or {}).get("n_posts") or 0, None))
        else:
            for drag in scenario["drags"]:
                order.append((scenario["name"], drag["index"], drag.get("post_count_network") or 0, drag.get("post_to_200_ms")))
    total = sum(item[2] for item in order)
    malformed = sum(item is None for item in lines)
    matched = capture.get("status") == "captured" and len(lines) == total and malformed == 0
    result = {"sink_status": capture.get("status"), "sink_files": capture.get("files", []),
              "posts": total, "lines": len(lines), "malformed_lines": malformed,
              "lines_matched": len(lines) if matched else 0,
              "mismatch": not matched, "per_drag": {}, "burst": {}}

    def values(chunk, post_to_200):
        if not chunk or any(item is None for item in chunk):
            return {"runtime_wall_ms": None, "exclusive_sum_ms": None,
                    "exclusive_sum_over_post_to_200_pct": None,
                    "covers": [item.get("covers") for item in chunk if item is not None]}
        try:
            wall = sum(float(item["runtime_wall_ms"]) for item in chunk)
            exclusive = sum(float(value) for item in chunk for value in item["exclusive_timings_ms"].values())
        except (KeyError, TypeError, ValueError, AttributeError):
            return {"runtime_wall_ms": None, "exclusive_sum_ms": None,
                    "exclusive_sum_over_post_to_200_pct": None,
                    "covers": [item.get("covers") for item in chunk]}
        pct = exclusive / post_to_200 * 100 if post_to_200 else None
        return {"runtime_wall_ms": wall, "exclusive_sum_ms": exclusive,
                "exclusive_sum_over_post_to_200_pct": pct,
                "covers": [item.get("covers") for item in chunk]}

    if matched:
        cursor = 0
        for name, index, posts, post_to_200 in order:
            chunk = lines[cursor:cursor + posts]
            cursor += posts
            if index is None:
                result["burst"][name] = values(chunk, None)
            else:
                result["per_drag"][f"{name}/{index}"] = values(chunk, post_to_200)
    write_json(rep / "commit-timing-summary.json", result)
    if capture.get("status") != "captured":
        raise ValueError(f"Runtime commit-stage timing sink is {capture.get('status')}; see timing-sink-capture.json")


def timing_self_check(root):
    """Off-stack synthetic proof of raw JSONL matching, per-run reset, and `covers` preservation."""
    base = Path(root).resolve(strict=True)
    work = base / "work-data-1"
    logs = work / "logs"
    logs.mkdir(parents=True)
    for suffix in ("", ".1", ".2", ".3"):
        (logs / f"commit-stage-timings.jsonl{suffix}").write_text('{"event":"historical"}\n')
    (logs / "keep.log").write_text("untouched in copied data\n")
    rep = base / "rep-1"
    rep.mkdir()
    reset_stage_timings(work, base, rep)
    if any((logs / f"commit-stage-timings.jsonl{suffix}").exists() for suffix in ("", ".1", ".2", ".3")):
        raise ValueError("self-check did not remove copied historical timing sink files")
    if not (logs / "keep.log").is_file():
        raise ValueError("self-check removed an unrelated copied log")
    payloads = [
        {"event": "timeline_commit_timing", "runtime_wall_ms": 12.5,
         "exclusive_timings_ms": {"commit": 10.0}, "covers": {"calls": 7, "elapsed_ns": 81,
                                                                       "value_equal_calls": 3}},
        {"event": "timeline_commit_timing", "runtime_wall_ms": 20.0,
         "exclusive_timings_ms": {"commit": 18.0}, "covers": {"calls": 9, "elapsed_ns": 95,
                                                                       "value_equal_calls": 4}},
    ]
    sink = logs / "commit-stage-timings.jsonl"
    raw = "".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in payloads)
    sink.write_text(raw, encoding="utf-8")
    capture_stage_timings(rep, work, True)
    write_json(rep / "browser-sv3-measure.json", {"scenarios": [
        {"name": "cold", "mode": "single", "drags": [{"index": 0, "post_count_network": 1,
                                                                    "post_to_200_ms": 100.0}]},
        {"name": "B1", "mode": "burst", "burst": {"n_posts": 1}},
    ]})
    timing_match(rep)
    summary = read_json(rep / "commit-timing-summary.json")
    copied = (rep / "commit-timing-lines.jsonl").read_text(encoding="utf-8")
    if (summary["lines_matched"] != 2 or summary["per_drag"]["cold/0"]["covers"] != [payloads[0]["covers"]]
            or summary["burst"]["B1"]["covers"] != [payloads[1]["covers"]] or copied != raw):
        raise ValueError("raw timing JSONL or covers counters did not survive matching")

    missing_work = base / "work-data-2"
    missing_work.mkdir()
    missing_rep = base / "rep-2"
    missing_rep.mkdir()
    reset_stage_timings(missing_work, base, missing_rep)
    capture_stage_timings(missing_rep, missing_work, False)
    write_json(missing_rep / "browser-sv3-measure.json", {"scenarios": []})
    try:
        timing_match(missing_rep)
    except ValueError as error:
        if "sink is missing" not in str(error):
            raise
    else:
        raise ValueError("missing timing sink did not fail clearly")
    missing = read_json(missing_rep / "commit-timing-summary.json")
    if missing["sink_status"] != "missing" or not missing["mismatch"]:
        raise ValueError("missing timing sink did not record its mismatch")
    print(json.dumps({"raw_jsonl_matched": True, "covers_preserved": True,
                      "historical_sink_cleared": True, "missing_sink_refused": True}))


AGENT_PACKAGE = "astrid"


def git_bytes(mirror, *args):
    return subprocess.check_output(["git", "-C", str(mirror), *args])


def agent_prepare(mirror, base, sha, overlay_dir, out):
    """Extract and verify the complete exact `astrid` package as a daemon-only overlay.

    Third-party dependencies remain installed. The candidate package tree and every file digest are independently
    checked before the overlay is made read-only. No installed file is written.
    """
    mirror, overlay_dir, out = Path(mirror), Path(overlay_dir), Path(out)
    if git_bytes(mirror, "rev-parse", base + "^{commit}").decode().strip() != base:
        raise ValueError("agent base SHA does not resolve to the approved commit")
    if git_bytes(mirror, "rev-parse", sha + "^{commit}").decode().strip() != sha:
        raise ValueError("agent candidate SHA does not resolve to the approved commit")
    dependency_diff = git_bytes(mirror, "diff", "--name-only", base, sha, "--", "pyproject.toml", "setup.py",
                                "setup.cfg", "uv.lock", "packages/python/pyproject.toml",
                                "packages/python/setup.py", "packages/python/setup.cfg", "contract",
                                ":(glob)**/*requirements*", ":(glob)**/*.lock",
                                ":(glob)**/constraints*.txt").decode().splitlines()
    if dependency_diff:
        raise ValueError("Agent dependency or contract inputs changed")
    package_tree = git_bytes(mirror, "rev-parse", f"{sha}:{AGENT_PACKAGE}").decode().strip()
    base_tree = git_bytes(mirror, "rev-parse", f"{base}:{AGENT_PACKAGE}").decode().strip()
    if len(package_tree) != 40 or len(base_tree) != 40:
        raise ValueError("could not resolve exact Agent package trees")

    def extract_tree(commit, destination):
        destination.mkdir(mode=0o700, parents=True)
        archive = subprocess.Popen(["git", "-C", str(mirror), "archive", "--format=tar", commit, AGENT_PACKAGE],
                                   stdout=subprocess.PIPE)
        try:
            subprocess.run(["tar", "-xf", "-", "-C", str(destination)], stdin=archive.stdout, check=True)
        finally:
            if archive.stdout:
                archive.stdout.close()
        if archive.wait() != 0:
            raise ValueError(f"could not archive {AGENT_PACKAGE} from {commit}")
        package = destination / AGENT_PACKAGE
        rows = []

        def tree(path):
            body = bytearray()
            for entry in sorted(path.iterdir(), key=lambda item: os.fsencode(item.name) +
                                (b"/" if item.is_dir() else b"")):
                mode = entry.lstat().st_mode
                if stat.S_ISDIR(mode):
                    git_mode, digest = b"40000", tree(entry)
                elif stat.S_ISREG(mode):
                    git_mode = b"100755" if mode & stat.S_IXUSR else b"100644"
                    data = entry.read_bytes()
                    digest = git_digest(b"blob", data)
                    rows.append((entry.relative_to(destination).as_posix(), hashlib.sha256(data).hexdigest(),
                                 len(data), git_mode.decode()))
                else:
                    raise ValueError(f"unhandled Agent package archive entry {entry}")
                body += git_mode + b" " + os.fsencode(entry.name) + b"\0" + digest
            return git_digest(b"tree", body)

        actual_tree = tree(package).hex()
        expected_tree = git_bytes(mirror, "rev-parse", f"{commit}:{AGENT_PACKAGE}").decode().strip()
        if actual_tree != expected_tree:
            raise ValueError(f"extracted Agent package tree {actual_tree} != {expected_tree}")
        return package, rows, actual_tree

    candidate_package, candidate_rows, _ = extract_tree(sha, overlay_dir)
    files = {path: {"candidate_sha256": digest, "candidate_bytes": size, "git_mode": mode}
             for path, digest, size, mode in candidate_rows}
    manifest = {"agent_sha": sha, "agent_tree": git_bytes(mirror, "rev-parse", sha + "^{tree}").decode().strip(),
                "agent_package_tree": package_tree, "agent_base": base, "agent_base_package_tree": base_tree,
                "overlay_dir": str(overlay_dir), "files": files}
    write_json(out / "agent-overlay.json", manifest)
    for directory in sorted([candidate_package, *[path for path in candidate_package.rglob("*") if path.is_dir()]],
                            key=lambda item: len(item.parts), reverse=True):
        os.chmod(directory, 0o500)
    for path in candidate_package.rglob("*"):
        if path.is_file():
            os.chmod(path, 0o400)
    os.chmod(overlay_dir, 0o500)


def agent_preflight(rep_dir, top_out, site, overlay_dir):
    """Checks every loaded Agent module came from the exact candidate package overlay."""
    rep_dir, top_out = Path(rep_dir), Path(top_out)
    site, overlay_dir = Path(site).resolve(), Path(overlay_dir).resolve()
    top = read_json(top_out / "agent-overlay.json")
    witness = read_json(rep_dir / "candidate-daemon-module.json")
    agent = witness.get("agent_overlay")
    if not agent or agent["overlay_dir"] != str(overlay_dir):
        raise ValueError("daemon witness has no agent overlay record for this overlay directory")
    if agent.get("package_tree") != top.get("agent_package_tree"):
        raise ValueError("daemon witness names a different Agent package tree")
    failures = []
    modules = agent.get("modules", {})
    if not modules:
        failures.append("daemon witness recorded no Agent modules")
    for name, record in modules.items():
        if record.get("namespace") is True:
            paths = record.get("paths", [])
            if not paths:
                failures.append(f"{name} has an empty namespace witness")
            for item in paths:
                relative_dir = item.get("relative_dir")
                if (not isinstance(relative_dir, str)
                        or item.get("directory") != str(overlay_dir / relative_dir)
                        or not any(path.startswith(relative_dir + "/") for path in top["files"])):
                    failures.append(f"{name} namespace is outside the exact candidate package")
            continue
        relative = record.get("relative")
        if not isinstance(relative, str) or relative not in top["files"]:
            failures.append(f"{name} has no exact candidate file record")
            continue
        expected_file = str(overlay_dir / relative)
        if record.get("file") != expected_file:
            failures.append(f"{name} loaded from {record.get('file')}")
        if record.get("sha256") != top["files"][relative]["candidate_sha256"]:
            failures.append(f"{name} loaded with a different sha256")
    write_json(rep_dir / "agent-loaded.json", {"modules": modules, "failures": failures})
    if failures:
        raise ValueError("agent overlay preflight failed: " + "; ".join(failures))


def agent_finish(top_out):
    """After the run: verify the complete package overlay and merge exact module-origin witnesses."""
    top_out = Path(top_out)
    receipt = read_json(top_out / "agent-overlay.json")
    overlay = Path(receipt["overlay_dir"])
    expected_paths = set(receipt["files"])
    actual_paths = {path.relative_to(overlay).as_posix() for path in overlay.rglob("*") if path.is_file()}
    overlay_matches = actual_paths == expected_paths
    if overlay_matches:
        for relative, item in receipt["files"].items():
            path = overlay / relative
            if path.is_symlink() or not path.is_file():
                overlay_matches = False
                break
            actual_mode = "100755" if path.stat().st_mode & stat.S_IXUSR else "100644"
            if (digest_file(path) != item["candidate_sha256"]
                    or actual_mode != item["git_mode"]):
                overlay_matches = False
                break
    loaded = {}
    for path in sorted(top_out.glob("rep-*/agent-loaded.json")):
        loaded[path.parent.name] = read_json(path)
    receipt["overlay_content_unchanged"] = overlay_matches
    receipt["loaded_by_repetition"] = loaded
    temporary = top_out / "agent-overlay.json.tmp"
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    os.replace(temporary, top_out / "agent-overlay.json")
    if not overlay_matches:
        raise ValueError("the complete Agent package overlay changed during the run")
    if any(item["failures"] for item in loaded.values()):
        raise ValueError("an agent overlay preflight recorded failures")



action, *raw = sys.argv[1:]
if action == "audit-tree":
    audit_tree(*raw)
elif action == "reset-stage-timings":
    reset_stage_timings(*raw)
elif action == "capture-stage-timings":
    capture_stage_timings(*raw)
elif action == "timing-self-check":
    timing_self_check(*raw)
elif action == "agent-prepare":
    agent_prepare(*raw)
elif action == "agent-preflight":
    agent_preflight(*raw)
elif action == "agent-finish":
    agent_finish(*raw)
elif action == "timing-match":
    timing_match(*raw)
elif action == "archive":
    mirror, commit, archive, out = raw
    verify_archive(Path(mirror), commit, Path(archive), Path(out))
elif action == "inventory":
    program_inventory(*map(Path, raw))
elif action == "prepare":
    orig_support, work_support, realm, archive, out = raw
    prepare(Path(orig_support), Path(work_support), realm, Path(archive), Path(out))
elif action == "preflight":
    work_support, realm, archive, interpreter, out = raw
    preflight(Path(work_support), realm, Path(archive), Path(interpreter), Path(out))
elif action == "postflight":
    work_support, realm, archive, out = raw
    check_published(Path(work_support), realm, Path(archive), Path(out))
    ports_closed()
    owner_exited(Path(out))
elif action == "owner-exited":
    owner_exited(Path(raw[0]))
elif action == "ports-closed":
    ports_closed()
elif action == "stop-preview-listeners":
    stop_preview_listeners()
elif action == "preview-after":
    preview_after(Path(raw[0]))
else:
    raise ValueError(f"unknown proof operation {action}")
