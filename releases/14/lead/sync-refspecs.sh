#!/bin/bash
# Keep fetch refspecs to main plus local branches that still exist on origin.
cd /home/user/astrid-dev || exit 1
git config --unset-all remote.origin.fetch
git config --add remote.origin.fetch +refs/heads/main:refs/remotes/origin/main
for b in $(git for-each-ref --format='%(refname:short)' refs/heads/); do
  [ "$b" = main ] && continue
  if git ls-remote --exit-code --heads origin "$b" >/dev/null 2>&1; then
    git config --add remote.origin.fetch "+refs/heads/$b:refs/remotes/origin/$b"
  else
    [ "$(git branch --show-current)" = "$b" ] || git branch -D -q "$b"
  fi
done
git fetch -q --prune origin
