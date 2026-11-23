"""Run the installed Runtime's direct lifecycle on its already-selected sandbox."""
import json
import os
from pathlib import Path
import sys
import time

from astrid_runtime import cli
from astrid_runtime.bootstrap import bootstrap
from astrid_runtime.runtime_boundary import LocalRuntimeBoundary
from runtime_protocol import process_control

args = cli.parser().parse_args(["up", *sys.argv[1:]])
paths = cli._paths(args)
assert args.data_root and Path(args.data_root).resolve() == paths.app_support
catalog = json.loads(paths.catalog_path.read_text())
assert len(catalog["realms"]) == 1
selected = catalog["realms"][0]
assert selected["realm_id"] == catalog["selected_realm_id"]
assert Path(selected["data_root"]) == paths.realms_dir / selected["realm_id"]
process_control.configure_from(paths.runtime_support)
config = cli._config(args, paths)
assert args.source_manifest and Path(args.source_manifest).resolve() == paths.app_support / "runtime/source-profiles/astrid.json"
class ObservedBoundary(LocalRuntimeBoundary):
    def _spawn_runtime(self, argv, *, support_root, stdout):
        process, broker = super()._spawn_runtime(argv, support_root=support_root, stdout=stdout)
        stat_file = Path("/proc") / str(process.pid) / "stat"
        fields = stat_file.read_text().rsplit(")", 1)[1].split()
        witness = Path(os.environ["P77_R7_NATIVE_PID_WITNESS"])
        assert witness.is_absolute() and witness.parent.resolve() == witness.parent
        with witness.open("x") as handle:
            json.dump({"pid": process.pid, "birth_ticks": int(fields[19]),
                       "witness_boottime_s": time.clock_gettime(time.CLOCK_BOOTTIME)}, handle)
        return process, broker


boundary = ObservedBoundary() if os.environ.get("P77_R7_NATIVE_PID_WITNESS") else LocalRuntimeBoundary()
result = bootstrap(paths, boundary, config)
if args.wait:
    cli._wait_for_door(paths, result, boundary)
print(json.dumps({"ok": True, "entry": "astrid_runtime.bootstrap.bootstrap", "realm_id": selected["realm_id"]}))
