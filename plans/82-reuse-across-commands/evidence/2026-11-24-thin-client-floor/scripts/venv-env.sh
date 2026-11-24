# Source after env.sh: apply the selected version's env the way run_astrid.py does.
VROOT=$PROGRAM/versions/$(cat $PROGRAM/current)
VPY=$VROOT/py/bin/python
eval "$(python3 -c '
import json,shlex,sys
r=json.load(open(sys.argv[1]))
for k,v in r["env"].items(): print("export %s=%s" % (k, shlex.quote(v)))
' $VROOT/version.json)"
export ASTRID_INSTALL_PROGRAM_ROOT=$PROGRAM
