#!/bin/bash
set -euo pipefail
E=/home/user/wt/h3real.env
git -C /home/user/vibecomfy worktree remove "$E/vibecomfy"
python3 - <<'PYCLEAN'
import shutil
from pathlib import Path
p=Path('/home/user/wt/h3real.env')
assert p.name == 'h3real.env' and p.parent == Path('/home/user/wt')
shutil.rmtree(p)
PYCLEAN
test ! -e "$E"
printf 'temporary environment removed\n'
git -C /home/user/wt/h3real rev-parse HEAD
git --no-optional-locks -C /home/user/wt/h3real status --porcelain
printf 'repository status command complete\n'
df -h /home
