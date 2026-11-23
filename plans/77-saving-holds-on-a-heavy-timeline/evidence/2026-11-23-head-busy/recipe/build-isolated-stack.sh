set -eu
mkdir -p /root/codex/le4/isolated3/home/{tmp,data,state,cache,config,runtime,data-dirs,config-dirs} /root/codex/le4/isolated3/manifest-copy/public
export HOME=/root/codex/le4/isolated3/home TMPDIR=/root/codex/le4/isolated3/home/tmp
export XDG_DATA_HOME=$HOME/data XDG_STATE_HOME=$HOME/state XDG_CACHE_HOME=$HOME/cache XDG_CONFIG_HOME=$HOME/config XDG_RUNTIME_DIR=$HOME/runtime XDG_DATA_DIRS=$HOME/data-dirs XDG_CONFIG_DIRS=$HOME/config-dirs
git clone --no-checkout /root/codex/plan78/astrid-agent /root/codex/le4/isolated3/agent
git -C /root/codex/le4/isolated3/agent checkout --detach 64cecdae9f679537f4a6dc82e5102e53b6943ef7
test "$(git -C /root/codex/le4/isolated3/agent rev-parse HEAD)" = 64cecdae9f679537f4a6dc82e5102e53b6943ef7
python3 -c 'import json; d=json.load(open("/root/codex/le4/isolated3/agent/runtime.lock.json")); print("Runtime lock:", d["source_commit"]); assert d["source_commit"] == "737843e9cb92c565c266452dde540832ee2c745b"'
git clone --filter=blob:none --branch release/15/main https://github.com/banodoco/astrid-app.git /root/codex/le4/isolated3/app
git -C /root/codex/le4/isolated3/app rev-parse HEAD
git clone --no-checkout /root/codex/le4/isolated2/omp /root/codex/le4/isolated3/omp
git -C /root/codex/le4/isolated3/omp cat-file -e '78f0e0960f471c2c62b943272a48c33366f239fe^{commit}'
cp /root/codex/le4/isolated3/app/public/install-manifest.json /root/codex/le4/isolated3/manifest-copy/public/install-manifest.json
sed '/^--- a\/scripts\/installer\/manifest.test.mjs/,$d' /root/codex/plan78/run/app-motion-pin.patch > /root/codex/le4/isolated3/manifest-only.patch
(cd /root/codex/le4/isolated3/manifest-copy && patch -p1 < /root/codex/le4/isolated3/manifest-only.patch)
(cd /root/codex/le4/isolated3/manifest-copy && node /root/codex/le4/isolated3/app/scripts/installer/pin.mjs 64cecdae9f679537f4a6dc82e5102e53b6943ef7 --in public/install-manifest.json --out /root/codex/le4/isolated3/install-manifest.json)
python3 -c 'import json; p="/root/codex/le4/isolated3/install-manifest.json"; d=json.load(open(p)); d["tools"]["omp"]["source"]["repo"]="/root/codex/le4/isolated3/omp"; open(p,"w").write(json.dumps(d,indent=2)+"\n")'
node /root/codex/le4/isolated3/app/scripts/installer/pin.mjs --check --in /root/codex/le4/isolated3/install-manifest.json
(cd /root/codex/le4/isolated3/app && npm ci)
sh /root/codex/le4/run2/install-bootstrap.sh --root /root/codex/le4/isolated3/program --data-root /root/codex/le4/isolated3/data --yes --autostart off --command off --skills off --skill-copies off --no-browser --manifest /root/codex/le4/isolated3/install-manifest.json
