"""Proof collection for the one retained-stack Runtime source overlay."""
import hashlib
import json
import os
from pathlib import Path
import socket
import stat
import subprocess
import sys
from urllib.parse import urlsplit


def digest_file(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_json(path, body):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(body, stream, indent=2)
        stream.write("\n")


def git_digest(kind, data):
    return hashlib.sha1(kind + b" " + str(len(data)).encode() + b"\0" + data,
                        usedforsecurity=False).digest()


def verify_archive(mirror, commit, archive, out):
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
        raise ValueError("archive bytes or modes do not match the approved git tree")
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
        raise ValueError("retained selection moved")


def prepare_profile(support, realm, archive, out):
    catalog_path = support / "catalog.json"
    profile_path = support / "source-profiles/astrid.json"
    catalog, old = read_json(catalog_path), read_json(profile_path)
    selected(support, realm, catalog)
    if catalog["source_profiles"]["astrid"] != old or old["profile"] != "astrid":
        raise ValueError("retained profile and catalog disagree")
    for name, source in (("original-catalog.json", catalog_path), ("original-source-profile.json", profile_path)):
        with (out / name).open("xb") as stream:
            stream.write(source.read_bytes())
    profile = {**old, "runtime_checkout": str(archive)}
    write_json(out / "candidate-source-profile.json", profile)


def ports_closed():
    for port in (2400, 17500, 17501):
        with socket.socket() as sock:
            sock.settimeout(0.25)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                raise ValueError(f"reserved port {port} did not close")


def check_published(support, realm, archive, out):
    catalog = read_json(support / "catalog.json")
    selected(support, realm, catalog)
    staged = read_json(out / "candidate-source-profile.json")
    profile = read_json(support / "source-profiles/astrid.json")
    if profile != staged or catalog["source_profiles"]["astrid"] != staged:
        raise ValueError("Runtime did not publish the exact candidate profile and catalog")
    if staged["runtime_checkout"] != str(archive):
        raise ValueError("published candidate provenance lost")
    original = read_json(out / "original-catalog.json")
    expected = {**original, "source_profiles": {**original["source_profiles"], "astrid": staged}}
    if catalog != expected:
        raise ValueError("the catalog has changes outside the candidate source profile")
    return profile


def preflight(support, realm, archive, interpreter, out):
    profile = check_published(support, realm, archive, out)
    owner = read_json(support / "discovery.json")
    witness = read_json(out / "candidate-daemon-module.json")
    pid = witness["pid"]
    stat_fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
    endpoint = urlsplit(owner["endpoint"])
    if (witness["runtime_sha"] != archive.name or witness["interpreter"] != str(interpreter)
            or witness["archive"] != str(archive) or witness["start"] != stat_fields[19]
            or owner["pid"] != pid or owner["active_realm"] != realm
            or owner["realm_root"] != str(support / "realms" / realm)
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
    write_json(out / "published-catalog.json", read_json(support / "catalog.json"))
    exact = {**witness, "endpoint": owner["endpoint"], "instance": owner["runtime_instance_id"],
             "realm_id": realm, "realm_root": owner["realm_root"], "module_proofs": module_proofs,
             "published_runtime_checkout": str(archive)}
    write_json(out / "browser-preflight.json", exact)
    print(json.dumps(exact))


action, *raw = sys.argv[1:]
if action == "archive":
    mirror, commit, archive, out = raw
    verify_archive(Path(mirror), commit, Path(archive), Path(out))
elif action == "inventory":
    program_inventory(*map(Path, raw))
elif action in {"prepare", "preflight", "postflight"}:
    support, realm, archive, *rest = raw
    args = (Path(support), realm, Path(archive), *map(Path, rest))
    if action == "prepare":
        prepare_profile(*args)
    elif action == "preflight":
        preflight(*args)
    else:
        check_published(*args)
        ports_closed()
        witness = read_json(args[-1] / "candidate-daemon-module.json")
        process = Path(f"/proc/{witness['pid']}/stat")
        try:
            start = process.read_text().rsplit(")", 1)[1].split()[19]
        except FileNotFoundError:
            start = None
        if start == witness["start"]:
            raise ValueError("the exact instrumented Runtime owner is still present")
elif action == "ports-closed":
    ports_closed()
else:
    raise ValueError(f"unknown proof operation {action}")
