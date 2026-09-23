#!/usr/bin/env bash
# Serialize callers with repo-write. Never report success without a successful push.
# PERSIST_BUDGET_S bounds the whole push/rebase loop (default 240 s): each network step gets at
# most the time left, so a hung remote cannot run persistence past the workflow's job limit.
set -euo pipefail
message=${COMMIT_MESSAGE:-"Update desk data"}
budget=${PERSIST_BUDGET_S:-240}
started=$SECONDS
left() { echo $(( budget - (SECONDS - started) )); }
bounded() {   # run a network git command within the remaining budget (cap 60 s per attempt)
  local t
  t=$(left)
  if [ "$t" -gt 60 ]; then t=60; fi
  if [ "$t" -lt 5 ]; then
    echo "Persistence budget spent; remote persistence not confirmed." >&2
    return 124
  fi
  timeout --kill-after=5 "$t" "$@"
}
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
  if bounded git push origin "HEAD:$branch"; then
    exit 0
  fi
  if [ "$attempt" -eq 4 ] || [ "$(left)" -lt 5 ]; then
    break
  fi
  if ! bounded git pull --rebase origin "$branch"; then
    git rebase --abort || true
    echo "Rebase failed; data retained locally, remote persistence not confirmed." >&2
    exit 1
  fi
  sleep "$attempt"
done
echo "Push failed after $attempt attempts in $((SECONDS - started)) s; remote persistence not confirmed." >&2
exit 1
