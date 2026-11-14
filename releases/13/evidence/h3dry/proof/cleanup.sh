#!/bin/bash
set -euo pipefail
E=/home/user/wt/h3live.env
git -C /home/user/vibecomfy worktree remove "$E/vibecomfy"
rm -rf -- "$E"
test ! -e "$E"
printf 'temporary environment removed\n'
git -C /home/user/wt/h3live rev-parse HEAD
git --no-optional-locks -C /home/user/wt/h3live status --porcelain
printf 'repository status command complete\n'
df -h /home
