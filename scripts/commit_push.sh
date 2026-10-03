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
# Push credential (repo 2.25). With DESK_DEPLOY_KEY set (the repository secret holding the private half of a
# write deploy key), push over SSH with that key: deploy keys are the only actor the main-branch ruleset lets
# bypass its required release check, so data writes keep landing while every other change needs a checked pull
# request. Without it, push with the workflow token exactly as before (no ruleset may require the check then).
# GitHub's SSH host keys come from https://api.github.com/meta over HTTPS; if they cannot be read, nothing is
# pushed rather than trusting an unverified host. DESK_PUSH_URL overrides the SSH remote (tests only).
remote=origin
if [ -n "${DESK_DEPLOY_KEY:-}" ]; then
  sshdir=$(mktemp -d)
  trap 'rm -rf "$sshdir"' EXIT
  printf '%s\n' "$DESK_DEPLOY_KEY" > "$sshdir/key"
  chmod 600 "$sshdir/key"
  if [ -z "${DESK_PUSH_URL:-}" ]; then
    if ! python3 - "$sshdir/known_hosts" <<'PY'
import json, sys, urllib.request
with urllib.request.urlopen("https://api.github.com/meta", timeout=20) as r:
    keys = json.load(r)["ssh_keys"]
open(sys.argv[1], "w").write("".join(f"github.com {k}\n" for k in keys))
PY
    then
      echo "Could not read GitHub's SSH host keys; nothing pushed; remote persistence not confirmed." >&2
      exit 1
    fi
  fi
  export GIT_SSH_COMMAND="ssh -i $sshdir/key -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=$sshdir/known_hosts"
  remote=${DESK_PUSH_URL:-"git@github.com:${GITHUB_REPOSITORY:?GITHUB_REPOSITORY unset}.git"}
  echo "persistence: deploy key"
else
  echo "persistence: workflow token"
fi
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
  if bounded git push "$remote" "HEAD:$branch"; then
    if [ "$remote" != origin ]; then
      bounded git fetch --quiet origin "$branch" || true   # refresh origin/<branch> for later persistence checks
    fi
    exit 0
  fi
  if [ "$attempt" -eq 4 ] || [ "$(left)" -lt 5 ]; then
    break
  fi
  if ! bounded git pull --rebase "$remote" "$branch"; then
    git rebase --abort || true
    echo "Rebase failed; data retained locally, remote persistence not confirmed." >&2
    exit 1
  fi
  sleep "$attempt"
done
echo "Push failed after $attempt attempts in $((SECONDS - started)) s; remote persistence not confirmed." >&2
exit 1
