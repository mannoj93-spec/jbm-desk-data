"""Repo 2.30 persistence retry repair, exercised through the real scripts/commit_push.sh.

Run 39333253907 (Oct 19 2026, 22:15 UTC): main advanced, the push was rejected, the `git pull --rebase` that followed
hung in fetch-pack until its 60 s cap, `git rebase --abort` failed ("no rebase in progress") and the job exited with
budget unused, so the collected data never reached main. Each test below builds a disposable origin (a local bare
repository), a working clone and a second clone that advances main, and puts a `git` shim first on PATH that passes
every command to the real git except the faults a test injects (by subcommand and call number). Nothing is mocked
inside the script itself.
"""
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/commit_push.sh'
REAL_GIT = shutil.which('git')

SHIM = r'''#!/usr/bin/env bash
real=__REAL__
d=__DIR__
sub=$1
n=$(( $(cat "$d/count_$sub" 2>/dev/null || echo 0) + 1 ))
echo "$n" > "$d/count_$sub"
mode=$(awk -v s="$sub" -v n="$n" '$1==s && ($2==n || $2=="*") {print $3; exit}' "$d/faults" 2>/dev/null)
case "$mode" in
  disconnect) echo "error: RPC failed; curl 92 HTTP/2 stream 5 was not closed cleanly: CANCEL (err 8)" >&2
              echo "fatal: fetch-pack: unexpected disconnect while reading sideband packet" >&2; exit 128 ;;
  hang)       exec sleep 300 ;;
  auth)       echo "ERROR: Permission to owner/repo.git denied to deploy key" >&2
              echo "fatal: Could not read from remote repository." >&2; exit 128 ;;
  lost)       "$real" "$@" >/dev/null 2>&1
              echo "fatal: the remote end hung up unexpectedly" >&2; exit 128 ;;
  landhang)   "$real" "$@" >/dev/null 2>&1; exec sleep 300 ;;
  dropped)    echo "fatal: the remote end hung up unexpectedly" >&2; exit 128 ;;
  advance)    "$d/advance.sh" >/dev/null 2>&1 ;;
esac
exec "$real" "$@"
'''

ADVANCE = r'''#!/usr/bin/env bash
set -e
cd __OTHER__
n=$(( $(cat __DIR__/advances 2>/dev/null || echo 0) + 1 ))
echo "$n" > __DIR__/advances
mkdir -p docs
echo "unrelated maintained-source change $n" >> docs/unrelated.md
__REAL__ add docs/unrelated.md
__REAL__ -c user.name=other -c user.email=o@o commit -q -m "unrelated source change $n"
__REAL__ push -q origin main
'''


def git(cwd, *args, check=True):
    return subprocess.run([REAL_GIT, '-C', str(cwd), *args], check=check, capture_output=True, text=True).stdout.strip()


class PersistenceRepairTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.origin, self.work, self.other, self.shim = d / 'origin.git', d / 'work', d / 'other', d / 'shim'
        subprocess.run([REAL_GIT, 'init', '-q', '--bare', '-b', 'main', str(self.origin)], check=True)
        subprocess.run([REAL_GIT, 'clone', '-q', str(self.origin), str(self.work)], check=True, capture_output=True)
        git(self.work, 'checkout', '-q', '-b', 'main')
        (self.work / 'data').mkdir()
        (self.work / 'data/a.jsonl').write_text('{"row": 0}\n')
        git(self.work, '-c', 'user.name=t', '-c', 'user.email=t@t', 'add', '.')
        git(self.work, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-q', '-m', 'init')
        git(self.work, 'push', '-q', 'origin', 'main')
        subprocess.run([REAL_GIT, 'clone', '-q', str(self.origin), str(self.other)], check=True, capture_output=True)
        self.shim.mkdir()
        sub = {'__REAL__': REAL_GIT, '__DIR__': str(self.shim), '__OTHER__': str(self.other)}
        for name, text in (('git', SHIM), ('advance.sh', ADVANCE)):
            for k, v in sub.items():
                text = text.replace(k, v)
            (self.shim / name).write_text(text)
            (self.shim / name).chmod(0o755)
        (self.shim / 'faults').write_text('')
        self.tmpdir = d / 'tmp'
        self.tmpdir.mkdir()
        self.init = git(self.origin, 'rev-parse', 'main')

    def tearDown(self):
        self.tmp.cleanup()

    # helpers ------------------------------------------------------------------------------------------------------
    def faults(self, *lines):
        (self.shim / 'faults').write_text(''.join(line + '\n' for line in lines))

    def count(self, sub):
        p = self.shim / f'count_{sub}'
        return int(p.read_text()) if p.exists() else 0

    def collect(self, text='{"row": 1}\n', name='data/b.jsonl'):
        (self.work / name).write_text(text)

    def run_push(self, *paths, budget='60', fetch_cap='8', **env):
        e = {k: v for k, v in os.environ.items() if k not in ('DESK_DEPLOY_KEY', 'DESK_PUSH_URL')}
        e.update(TMPDIR=str(self.tmpdir), PERSIST_BUDGET_S=budget, PERSIST_FETCH_CAP_S=fetch_cap,
                 DESK_WRITER='collector', PATH=f"{self.shim}:{os.environ['PATH']}")
        e.update(env)
        started = time.monotonic()
        r = subprocess.run(['bash', str(SCRIPT), *(paths or ('data',))], cwd=self.work, env=e,
                           capture_output=True, text=True, timeout=240)
        r.took = time.monotonic() - started
        return r

    def remote_log(self):
        return git(self.origin, 'log', '--format=%s', 'main').splitlines()

    def assert_not_confirmed(self, r, cls, stage):
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(f'NOT CONFIRMED class={cls} stage={stage}', r.stderr)
        self.assertIn('remote persistence not confirmed', r.stderr)
        self.assertNotIn('CONFIRMED stage=push', r.stdout)
        self.assertNotIn('no rebase in progress', r.stderr.lower())
        self.assertEqual(list(self.tmpdir.iterdir()), [])                      # temporary files removed

    def assert_landed_once(self, r):
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('persistence: CONFIRMED', r.stdout)
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), git(self.work, 'rev-parse', 'HEAD'))
        self.assertEqual(self.remote_log().count('Update desk data'), 1)       # one logical data change
        self.assertEqual(git(self.origin, 'show', 'main:data/b.jsonl'), '{"row": 1}')
        self.assertEqual(list(self.tmpdir.iterdir()), [])

    # the incident and its neighbours --------------------------------------------------------------------------------
    def test_incident_replay_rejected_push_then_hung_fetch_then_success(self):
        """The 22:15 sequence: remote advanced by an unrelated source change, first fetch hangs to its cap,
        the retry succeeds, the rebase is local, the data lands once on top of the unrelated change."""
        self.collect()
        self.faults('push 1 advance', 'fetch 1 hang')
        r = self.run_push(budget='60', fetch_cap='6')
        self.assert_landed_once(r)
        self.assertIn('stage=push attempt=1 result=failed class=rejected', r.stdout)
        self.assertIn('stage=fetch attempt=1 result=failed class=timeout', r.stdout)
        self.assertIn('stage=fetch attempt=2 result=ok', r.stdout)
        self.assertEqual(git(self.origin, 'show', 'main:docs/unrelated.md'), 'unrelated maintained-source change 1')
        self.assertEqual(self.remote_log()[:2], ['Update desk data', 'unrelated source change 1'])

    def test_transient_disconnect_on_fetch_is_retried(self):
        self.collect()
        self.faults('push 1 advance', 'fetch 1 disconnect')
        r = self.run_push()
        self.assert_landed_once(r)
        self.assertIn('stage=fetch attempt=1 result=failed class=transport', r.stdout)
        self.assertEqual(self.count('fetch'), 2)

    def test_real_conflict_stops_with_data_retained(self):
        (self.other / 'data/a.jsonl').write_text('{"row": "theirs"}\n')
        git(self.other, '-c', 'user.name=o', '-c', 'user.email=o@o', 'commit', '-q', '-am', 'their edit')
        git(self.other, 'push', '-q', 'origin', 'main')
        theirs = git(self.origin, 'rev-parse', 'main')
        self.collect('{"row": "ours"}\n', 'data/a.jsonl')
        r = self.run_push()
        self.assert_not_confirmed(r, 'conflict', 'rebase')
        self.assertIn('stage=rebase result=conflict', r.stdout)
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), theirs)       # nothing forced over their change
        self.assertEqual(git(self.work, 'log', '-1', '--format=%s'), 'Update desk data')   # our commit kept
        self.assertEqual((self.work / 'data/a.jsonl').read_text(), '{"row": "ours"}\n')
        gd = self.work / '.git'
        self.assertFalse((gd / 'rebase-merge').exists() or (gd / 'rebase-apply').exists())

    def test_push_authentication_failure_is_not_retried(self):
        self.collect()
        self.faults('push * auth')
        r = self.run_push()
        self.assert_not_confirmed(r, 'auth', 'push')
        self.assertEqual(self.count('push'), 1)
        self.assertEqual(self.count('fetch'), 0)
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), self.init)

    def test_fetch_authentication_failure_is_not_retried(self):
        self.collect()
        self.faults('push 1 advance', 'fetch * auth')
        r = self.run_push()
        self.assert_not_confirmed(r, 'auth', 'fetch')
        self.assertEqual(self.count('fetch'), 1)

    def test_writer_violation_in_staged_changes(self):
        self.collect()
        (self.work / 'scripts').mkdir()
        (self.work / 'scripts/x.py').write_text('print(1)\n')
        r = self.run_push('data', 'scripts')
        self.assertEqual(r.returncode, 1)
        self.assertIn('Push guard refused the staged changes', r.stderr)
        self.assertEqual(self.count('push'), 0)
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), self.init)

    def test_writer_violation_in_an_outgoing_commit(self):
        (self.work / 'notes.md').write_text('x\n')
        git(self.work, '-c', 'user.name=t', '-c', 'user.email=t@t', 'add', 'notes.md')
        git(self.work, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-q', '-m', 'stray')
        self.collect()
        r = self.run_push()
        self.assertEqual(r.returncode, 1)
        self.assertIn('Push guard refused an outgoing commit', r.stderr)
        self.assertEqual(self.count('push'), 0)

    def test_exhausted_budget_on_hung_fetches(self):
        self.collect()
        self.faults('push 1 advance', 'fetch * hang')
        r = self.run_push(budget='24', fetch_cap='5')
        self.assertEqual(r.returncode, 1)
        self.assertIn('class=budget-after-timeout stage=fetch', r.stderr)
        self.assertLess(r.took, 45)
        self.assertGreaterEqual(self.count('fetch'), 2)                       # retried while budget allowed
        self.assertNotIn(git(self.work, 'rev-parse', 'HEAD'), git(self.origin, 'rev-list', 'main'))

    def test_two_advances_then_success(self):
        self.collect()
        self.faults('push 1 advance', 'push 2 advance')
        r = self.run_push()
        self.assert_landed_once(r)
        self.assertIn('CONFIRMED stage=push attempt=3', r.stdout)

    def test_remote_that_keeps_advancing_is_reported_not_forced(self):
        self.collect()
        self.faults('push * advance')
        r = self.run_push()
        self.assert_not_confirmed(r, 'rejected', 'push')
        self.assertIn('push failed after 4 attempts', r.stderr)
        self.assertEqual(self.count('push'), 4)
        self.assertNotIn('Update desk data', self.remote_log())

    def test_push_landed_but_response_lost_is_confirmed_by_read_back(self):
        self.collect()
        self.faults('push 1 lost')
        r = self.run_push()
        self.assert_landed_once(r)
        self.assertIn('stage=verify result=remote-contains-head', r.stdout)
        self.assertEqual(self.count('push'), 1)

    def test_push_dropped_before_landing_is_retried_after_read_back(self):
        self.collect()
        self.faults('push 1 dropped')
        r = self.run_push()
        self.assert_landed_once(r)
        self.assertIn('stage=verify result=remote-lacks-head', r.stdout)
        self.assertEqual(self.count('push'), 2)
        self.assertEqual(self.count('fetch'), 1)                              # the read-back tip is reused

    def test_hung_push_whose_update_landed_is_confirmed(self):
        """A push that is killed at its cap may still have updated the remote; the read-back decides."""
        self.collect()
        self.faults('push 1 landhang')
        r = self.run_push(budget='60', PERSIST_PUSH_CAP_S='6')
        self.assert_landed_once(r)
        self.assertIn('stage=push attempt=1 result=failed class=timeout', r.stdout)
        self.assertIn('stage=verify result=remote-contains-head', r.stdout)


if __name__ == '__main__':
    unittest.main()
