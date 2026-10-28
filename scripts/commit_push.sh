#!/usr/bin/env bash
# Serialize callers with repo-write. Never report success without a successful push.
# PERSIST_BUDGET_S bounds the whole persistence loop (default 240 s): each network step gets at most the time
# left, so a hung remote cannot run persistence past the workflow's job limit.
#
# Repo 2.30 (persistence retry repair). Run 39333253907 (Oct 19 2026, 22:15 UTC) lost its data push: the first push
# was rejected because main had advanced, the `git pull --rebase` that followed hung in fetch-pack until the 60 s
# cap, `git rebase --abort` then failed because no rebase had started, and the job exited with about 38 s of budget
# unused. Synchronisation is now three separate stages, each classified and logged:
#   fetch   bounded, read-only; transport failures (timeouts, disconnects, resets, DNS) are retried within the
#           budget; authentication, permission, missing-repository and host-key failures stop at once.
#   rebase  local only, onto the fetched tip. A content conflict stops with the data retained locally; a rebase
#           is aborted only when one is actually in progress.
#   push    a rejection because the remote advanced leads back to fetch + rebase; a transport failure leaves the
#           outcome uncertain, so the remote is read back and the push counts only if the remote tip is HEAD or
#           descends from it; an authentication or ruleset refusal stops at once.
# Repo 2.30.5 (shallow fetch). The collector checks out main at depth 1. A plain `git fetch` of a main that had
# just received a merge commit walked the merged branch's history past the shallow boundary and downloaded the
# whole repository history (1.5 GB, unfinished after 150 s in a reproduction; Oct 26 runs 40251817627,
# 40327143379, 40414468575 each timed out twice at 45 s and lost their push). Fetches are now bounded in depth
# (PERSIST_FETCH_DEPTH, default 10: enough for the read-back to see later commits on top of ours; the real Oct 26
# merge fetched at depth 10 in 7 s and 14 MB), and the
# rebase replays only this job's commits (`--onto <fetched tip> <previous tip>`), which needs no shared history
# with the fetched tip.
# Nothing is ever force-pushed. The writer guard runs on the staged changes and on every outgoing commit before
# each push (so again after every rebase). The last line printed says whether remote persistence was confirmed.
set -euo pipefail
# Writer identity (repo 2.25). DESK_WRITER names this caller's entry in scripts/writers.json; scripts/push_guard.py
# refuses anything that is not one of its documented outputs - in the staged changes before committing and in every
# outgoing commit before each push, re-checked after a rebase. Unset or unknown: nothing is committed or pushed.
writer=${DESK_WRITER:-}
if [ -z "$writer" ]; then
  echo "DESK_WRITER is unset: no documented outputs to check against; nothing committed or pushed." >&2
  exit 1
fi
guard=$(dirname "$0")/push_guard.py
message=${COMMIT_MESSAGE:-"Update desk data"}
budget=${PERSIST_BUDGET_S:-240}
fetch_cap=${PERSIST_FETCH_CAP_S:-45}   # per fetch attempt, so a hung fetch leaves room to retry within the budget
fetch_depth=${PERSIST_FETCH_DEPTH:-10} # history fetched per attempt; never unbounded in a shallow checkout (2.30.5)
push_cap=${PERSIST_PUSH_CAP_S:-60}     # per push attempt (as before)
started=$SECONDS
sshdir=""
work=""
cleanup() {
  if [ -n "$sshdir" ]; then rm -rf "$sshdir"; fi
  if [ -n "$work" ]; then rm -rf "$work"; fi
}
trap cleanup EXIT
work=$(mktemp -d)
errf=$work/stderr
left() { echo $(( budget - (SECONDS - started) )); }
bounded() {   # bounded CAP CMD...: run a network git command within the remaining budget, at most CAP seconds
  local cap=$1 t
  shift
  t=$(left)
  if [ "$t" -gt "$cap" ]; then t=$cap; fi
  if [ "$t" -lt 5 ]; then
    echo "Persistence budget spent; remote persistence not confirmed." >&2
    return 124
  fi
  timeout --kill-after=5 "$t" "$@"
}
log() { echo "persistence: $*"; }
not_confirmed() {   # not_confirmed CLASS STAGE DETAIL: the final line for every failure
  echo "persistence: NOT CONFIRMED class=$1 stage=$2 after $((SECONDS - started)) s - $3; data retained locally, remote persistence not confirmed." >&2
  exit 1
}
# classify RC STDERR-FILE -> timeout | transport | auth | refused | rejected | conflict | unclassified
classify() {
  local rc=$1 f=$2
  if [ "$rc" -eq 124 ] || [ "$rc" -eq 137 ]; then echo timeout; return; fi
  if grep -qiE 'host key verification failed|permission denied|publickey|authentication failed|could not read (username|password)|returned error: 40[13]|repository not found|denied to|invalid username' "$f"; then
    echo auth; return
  fi
  if grep -qiE 'GH006|GH013|protected branch|pre-receive hook declined|push declined|rule violations' "$f"; then
    echo refused; return
  fi
  if grep -qiE '\[rejected\]|non-fast-forward|fetch first|stale info|\(fetch first\)' "$f"; then
    echo rejected; return
  fi
  if grep -qiE 'unexpected disconnect|connection reset|early eof|rpc failed|hung up|could not resolve|timed out|connection refused|broken pipe|ssh: connect to host|kex_exchange_identification|remote end|returned error: 5[0-9][0-9]|gnutls|ssl_read|tls|transfer closed|operation too slow|network is unreachable' "$f"; then
    echo transport; return
  fi
  echo unclassified
}
run_logged() {   # run_logged CAP CMD...: bounded command, stderr captured to $errf and echoed; returns its status
  local rc=0
  : > "$errf"
  bounded "$@" 2>"$errf" || rc=$?
  if [ -s "$errf" ]; then cat "$errf" >&2; fi
  return "$rc"
}
sha_like() { [[ "$1" =~ ^[0-9a-f]{40}$ ]]; }
rebase_in_progress() {
  local gd
  gd=$(git rev-parse --git-dir 2>/dev/null) || return 1
  [ -n "$gd" ] && { [ -d "$gd/rebase-merge" ] || [ -d "$gd/rebase-apply" ]; }
}
# Push credential (repo 2.25). With DESK_DEPLOY_KEY set (the repository secret holding the private half of a
# write deploy key), push over SSH with that key: deploy keys are the only actor the main-branch ruleset lets
# bypass its required release check, so data writes keep landing while every other change needs a checked pull
# request. Without it, push with the workflow token exactly as before (no ruleset may require the check then).
# GitHub's SSH host keys come from https://api.github.com/meta over HTTPS (scripts/github_host_keys.py); if no
# trustworthy keys can be read within the budget, nothing is pushed rather than trusting an unverified host. DESK_PUSH_URL overrides the SSH remote and
# DESK_META_URL the host-key source (tests only).
remote=origin
if [ -n "${DESK_DEPLOY_KEY:-}" ]; then
  sshdir=$(mktemp -d)
  printf '%s\n' "$DESK_DEPLOY_KEY" > "$sshdir/key"
  chmod 600 "$sshdir/key"
  if [ -z "${DESK_PUSH_URL:-}" ] || [ -n "${DESK_META_URL:-}" ]; then   # tests set DESK_META_URL to exercise this path
    # Repo 2.26: authenticated (the job's token), retried within this budget, validated and reused within the job
    # (scripts/github_host_keys.py). At most 40 s of the budget, leaving the rest for the push itself.
    keys_budget=$(left); if [ "$keys_budget" -gt 40 ]; then keys_budget=40; fi
    if ! python3 "$(dirname "$0")/github_host_keys.py" "$sshdir/known_hosts" --budget "$keys_budget"; then
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
if ! python3 "$guard" --writer "$writer" staged; then
  echo "Push guard refused the staged changes; nothing committed or pushed." >&2
  exit 1
fi
if ! git diff --cached --quiet; then
  git commit -m "$message"
fi
branch=$(git symbolic-ref --short HEAD)
# The last remote tip this job knows: the checkout's origin/<branch>, then FETCH_HEAD after each fetch.
if ! base=$(git rev-parse --verify -q "refs/remotes/origin/$branch"); then
  echo "No origin/$branch to compare outgoing commits with; nothing pushed." >&2
  exit 1
fi

# fetch_tip: bounded fetch of <branch> from the push remote, retried on transport failures within the budget.
# Sets $tip to the fetched commit. Returns 0 on success; on failure sets $fail_class and returns 1.
tip=""
fail_class=""
fetch_tip() {
  local n=0 rc cls
  while :; do
    n=$((n + 1))
    rc=0
    run_logged "$fetch_cap" git fetch --quiet --depth="$fetch_depth" "$remote" "$branch" || rc=$?
    if [ "$rc" -eq 0 ]; then
      tip=$(git rev-parse --verify -q FETCH_HEAD || true)
      log "stage=fetch attempt=$n result=ok tip=${tip:-unknown}"
      return 0
    fi
    cls=$(classify "$rc" "$errf")
    log "stage=fetch attempt=$n result=failed class=$cls rc=$rc"
    case "$cls" in
      auth|refused) fail_class=$cls; return 1 ;;
    esac
    if [ "$(left)" -lt 8 ]; then fail_class="budget-after-$cls"; return 1; fi
    sleep $(( n < 4 ? n : 4 ))
  done
}

# remote_has_head: after an uncertain push, read the remote back. 0 = the remote tip is HEAD or descends from it.
remote_has_head() {
  local head
  head=$(git rev-parse --verify -q HEAD || true)
  sha_like "$head" || return 1
  fetch_tip || return 2
  sha_like "$tip" || return 1
  if [ "$tip" = "$head" ] || git merge-base --is-ancestor "$head" "$tip" 2>/dev/null; then
    return 0
  fi
  return 1
}

confirmed() {
  if [ "$remote" != origin ]; then
    bounded 60 git fetch --quiet --depth="$fetch_depth" origin "$branch" || true   # refresh origin/<branch> for later checks
  fi
  log "CONFIRMED stage=push attempt=$attempt head=$(git rev-parse --verify -q HEAD || true) after $((SECONDS - started)) s"
  exit 0
}

# synchronize: fetch the remote tip and rebase local commits onto it. Exits (not confirmed) on a permanent failure.
# A tip fetched by the read-back a moment earlier is reused rather than fetched again.
synchronize() {
  if [ "$fresh" != 1 ] && ! fetch_tip; then
    not_confirmed "$fail_class" fetch "could not read origin/$branch"
  fi
  fresh=0
  local rc=0
  : > "$errf"
  git rebase --quiet --onto FETCH_HEAD "$base" 2>"$errf" || rc=$?   # only this job's commits (base..HEAD)
  if [ -s "$errf" ]; then cat "$errf" >&2; fi
  if [ "$rc" -ne 0 ]; then
    if rebase_in_progress; then
      git rebase --abort || true
      log "stage=rebase result=conflict (aborted; local commits restored)"
      not_confirmed conflict rebase "local commits conflict with origin/$branch"
    fi
    log "stage=rebase result=failed rc=$rc (no rebase in progress)"
    not_confirmed rebase-error rebase "rebase could not start"
  fi
  log "stage=rebase result=ok onto=${tip:-unknown}"
  base=$(git rev-parse FETCH_HEAD)
}

attempt=0
fresh=0
for attempt in 1 2 3 4; do
  if ! python3 "$guard" --writer "$writer" outgoing "$base"; then
    echo "Push guard refused an outgoing commit; nothing pushed." >&2
    exit 1
  fi
  rc=0
  run_logged "$push_cap" git push "$remote" "HEAD:$branch" || rc=$?
  if [ "$rc" -eq 0 ]; then
    confirmed
  fi
  cls=$(classify "$rc" "$errf")
  log "stage=push attempt=$attempt result=failed class=$cls rc=$rc"
  case "$cls" in
    auth|refused)
      not_confirmed "$cls" push "the remote refused the push; not retried" ;;
    rejected)
      ;;   # the remote advanced: fetch and rebase below
    *)     # timeout, transport or unclassified: the push may have landed, so read the remote back
      vr=0
      remote_has_head || vr=$?
      if [ "$vr" -eq 0 ]; then
        log "stage=verify result=remote-contains-head (push outcome was uncertain)"
        confirmed
      fi
      if [ "$vr" -eq 1 ] && sha_like "$tip"; then fresh=1; fi
      log "stage=verify result=$([ "$vr" -eq 2 ] && echo unreadable || echo remote-lacks-head)"
      ;;
  esac
  if [ "$attempt" -eq 4 ] || [ "$(left)" -lt 5 ]; then
    break
  fi
  synchronize
  sleep "$attempt"
done
not_confirmed "${cls:-unknown}" push "push failed after $attempt attempts"
