#!/usr/bin/env bash
# Serialize callers with repo-write. Never report success without a successful push.
set -euo pipefail
message=${COMMIT_MESSAGE:-"Update desk data"}
git config user.name collector-bot
git config user.email collector-bot@users.noreply.github.com
for path in "$@"; do
  if [ -e "$path" ] || [ -n "$(git ls-files -- "$path")" ]; then
    git add -- "$path"
  fi
done
if ! git diff --cached --quiet; then
  git commit -m "$message"
fi
branch=$(git symbolic-ref --short HEAD)
for attempt in 1 2 3 4; do
  if git push origin "HEAD:$branch"; then
    exit 0
  fi
  if [ "$attempt" -eq 4 ]; then
    break
  fi
  if ! git pull --rebase origin "$branch"; then
    git rebase --abort || true
    echo "Rebase failed; data retained locally, remote persistence not confirmed." >&2
    exit 1
  fi
  sleep "$attempt"
done
echo "Push failed after four attempts; remote persistence not confirmed." >&2
exit 1
