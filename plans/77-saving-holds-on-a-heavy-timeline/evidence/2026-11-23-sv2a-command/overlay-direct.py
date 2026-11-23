"""Select the candidate modules and call the ordinary direct Runtime lifecycle."""
import json
import os
from pathlib import Path
import sys

if not sys.flags.isolated or not sys.dont_write_bytecode:
    raise SystemExit("use the retained interpreter with -I -B")
operation, *arguments = sys.argv[1:]
archive = Path(os.environ["SV2A_ARCHIVE"])
if archive.resolve(strict=True) != archive or archive.name != os.environ["SV2A_RUNTIME_SHA"]:
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
support = Path(os.environ["SV2A_SUPPORT_ROOT"])
realm = os.environ["SV2A_REALM_ID"]
manifest = Path(os.environ["SV2A_SOURCE_PROFILE"])
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
result = bootstrap(paths, boundary, config)
if args.wait:
    cli._wait_for_door(paths, result, boundary)
print(json.dumps({"ok": True, "entry": "astrid_runtime.bootstrap.bootstrap", "realm_id": realm,
                  "runtime_sha": archive.name, "runtime_module": str(Path(runtime_protocol.__file__).resolve())}))
