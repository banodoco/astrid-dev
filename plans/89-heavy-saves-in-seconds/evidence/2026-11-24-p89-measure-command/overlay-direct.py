"""Select the candidate modules and call the ordinary direct Runtime lifecycle."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

if not sys.flags.isolated or not sys.dont_write_bytecode:
    raise SystemExit("use the retained interpreter with -I -B")
operation, *arguments = sys.argv[1:]
archive = Path(os.environ["SV3_ARCHIVE"])
if archive.resolve(strict=True) != archive or archive.name != os.environ["SV3_RUNTIME_SHA"]:
    raise SystemExit("candidate archive does not match authorized SHA")
sys.path.insert(0, str(archive))

import astrid_runtime
import runtime_protocol
from astrid_runtime import cli
from astrid_runtime.bootstrap import bootstrap
from astrid_runtime.runtime_boundary import LocalRuntimeBoundary
from runtime_protocol import process_control

if any(not Path(module.__file__).resolve(strict=True).is_relative_to(archive)
       for module in (astrid_runtime, runtime_protocol)):
    raise SystemExit("direct launcher imported Runtime outside the candidate archive")

if operation == "down":
    raise SystemExit(cli.main([operation, *arguments]))
if operation != "up":
    raise SystemExit("expected up or down")
args = cli.parser().parse_args([operation, *arguments])
paths = cli._paths(args)
support = Path(os.environ["SV3_SUPPORT_ROOT"])
realm = os.environ["SV3_REALM_ID"]
manifest = Path(os.environ["SV3_SOURCE_PROFILE"])
if (paths.runtime_support != support or args.source_manifest != manifest
        or manifest.resolve(strict=True) != manifest):
    raise SystemExit("the requested direct launch is outside its prepared scope")
catalog = json.loads(paths.catalog_path.read_text())
if (catalog["selected_realm_id"] != realm or len(catalog["realms"]) != 1
        or catalog["realms"][0]["realm_id"] != realm
        or Path(catalog["realms"][0]["data_root"]) != paths.realms_dir / realm):
    raise SystemExit("the retained catalog selection changed")
process_control.configure_from(paths.runtime_support)
config = cli._config(args, paths)
boundary = LocalRuntimeBoundary()
# Runtime currently starts the daemon with stdout=DEVNULL and merges child stderr into stdout.
# Supply one private receipt file to that exact subprocess call.  The child keeps its dup'd
# descriptor after this context closes, so startup failures (including sitecustomize failures
# before the daemon witness) survive even when bootstrap raises before returning a witness.
original_spawn_runtime = boundary._spawn_runtime


def spawn_runtime_with_startup_receipt(argv, *, support_root, stdout):
    daemon_start = any(argv[index : index + 3] == ["-m", "runtime_protocol", "start"]
                       for index in range(len(argv) - 2))
    if stdout != subprocess.DEVNULL or not daemon_start:
        return original_spawn_runtime(argv, support_root=support_root, stdout=stdout)

    archive_root = Path(os.environ["SV3_ARCHIVE"])
    output_root = archive_root.parent.parent
    witness = Path(os.environ["SV3_DAEMON_WITNESS"])
    repetition = witness.parent
    if (archive_root.parent.name != "source"
            or archive_root.resolve(strict=True) != archive_root
            or archive_root.parent.resolve(strict=True) != archive_root.parent
            or output_root.resolve(strict=True) != output_root
            or witness.name != "candidate-daemon-module.json"
            or not re.fullmatch(r"rep-[1-9][0-9]*", repetition.name)
            or repetition.resolve(strict=True) != repetition
            or repetition.parent != output_root):
        raise SystemExit("daemon startup receipt is outside the canonical repetition output")
    receipt = repetition / "daemon-startup.stderr"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    descriptor = os.open(receipt, flags, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        return original_spawn_runtime(argv, support_root=support_root, stdout=stream)


boundary._spawn_runtime = spawn_runtime_with_startup_receipt
result = bootstrap(paths, boundary, config)
if args.wait:
    cli._wait_for_door(paths, result, boundary)
print(json.dumps({"ok": True, "entry": "astrid_runtime.bootstrap.bootstrap", "realm_id": realm,
                  "runtime_sha": archive.name, "runtime_module": str(Path(runtime_protocol.__file__).resolve())}))
