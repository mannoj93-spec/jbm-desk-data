"""Push guard (repo 2.25): scripts/commit_push.sh commits and pushes only the writer's documented outputs
(scripts/writers.json). Reproduces the 2.24.1 defect - an unrelated staged source file was committed and pushed with
the data - and covers already-committed changes, rebases, deletions, maintained files, content-addressed calendars,
missing or unknown writers and credential cleanup on refusal. Every repository here is a disposable fixture."""
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/commit_push.sh'
ID = ['-c', 'user.name=t', '-c', 'user.email=t@t']


def git(cwd, *args):
    return subprocess.run(['git', '-C', str(cwd), *args], check=True, capture_output=True, text=True).stdout.strip()


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.origin, self.work, self.other = d / 'origin.git', d / 'work', d / 'other'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'main', str(self.origin)], check=True)
        subprocess.run(['git', 'clone', '-q', str(self.origin), str(self.work)], check=True, capture_output=True)
        git(self.work, 'checkout', '-q', '-b', 'main')
        for rel, text in {'data/a.jsonl': '{}\n', 'collector.py': 'print(1)\n', 'registry/README.md': 'r\n',
                          'state/checkpoints.json': '{}\n', 'reports/health.json': '{}\n',
                          '.github/workflows/collect.yml': 'name: c\n'}.items():
            (self.work / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.work / rel).write_text(text)
        git(self.work, *ID, 'add', '.')
        git(self.work, *ID, 'commit', '-q', '-m', 'init')
        git(self.work, 'push', '-q', 'origin', 'main')
        self.keytmp = d / 'tmp'
        self.keytmp.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def push(self, *paths, writer='collector', **env):
        e = {k: v for k, v in os.environ.items() if k not in ('DESK_DEPLOY_KEY', 'DESK_PUSH_URL', 'DESK_WRITER')}
        e.update(TMPDIR=str(self.keytmp), PERSIST_BUDGET_S='60')
        if writer is not None:
            e['DESK_WRITER'] = writer
        e.update(env)
        return subprocess.run(['bash', str(SCRIPT), *paths], cwd=self.work, env=e, capture_output=True, text=True)

    def remote_files(self):
        return set(git(self.origin, 'ls-tree', '-r', '--name-only', 'main').split('\n'))

    def remote_diff(self, before):
        return set(filter(None, git(self.origin, 'diff', '--name-only', before, 'main').split('\n')))


class PushGuardTests(Fixture):
    def test_reproduced_defect_unrelated_staged_source_is_refused(self):
        before = git(self.origin, 'rev-parse', 'main')
        (self.work / 'data/a.jsonl').write_text('{"x": 1}\n')
        (self.work / 'collector.py').write_text('print("changed")\n')
        git(self.work, 'add', 'collector.py')                      # unrelated, staged before the call
        r = self.push('data')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('collector.py: maintained by a revision', r.stderr)
        self.assertIn('nothing committed or pushed', r.stderr)
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), before)
        self.assertEqual(git(self.work, 'rev-parse', 'HEAD'), before)

    def test_already_committed_source_change_is_refused_before_pushing(self):
        before = git(self.origin, 'rev-parse', 'main')
        (self.work / '.github/workflows/collect.yml').write_text('name: changed\n')
        git(self.work, *ID, 'commit', '-qam', 'workflow change made earlier in the job')
        (self.work / 'data/a.jsonl').write_text('{"x": 2}\n')
        r = self.push('data')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('.github/workflows/collect.yml: maintained by a revision', r.stderr)
        self.assertIn('nothing pushed', r.stderr)
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), before)

    def test_documented_outputs_are_pushed(self):
        before = git(self.origin, 'rev-parse', 'main')
        (self.work / 'data/a.jsonl').write_text('{"x": 3}\n')
        (self.work / 'data/new/b.jsonl').parent.mkdir()
        (self.work / 'data/new/b.jsonl').write_text('{}\n')
        (self.work / 'state/checkpoints.json').write_text('{"s": 1}\n')
        (self.work / 'reports/health.json').write_text('{"h": 1}\n')
        r = self.push('data', 'state', 'reports/health.json')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.remote_diff(before), {'data/a.jsonl', 'data/new/b.jsonl', 'state/checkpoints.json',
                                                    'reports/health.json'})

    def test_another_writers_outputs_are_refused(self):
        (self.work / 'state/range_attempts.jsonl').write_text('{}\n')
        r = self.push('state')                                     # collector may not write the range stream's log
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('state/range_attempts.jsonl: not a documented output of this writer', r.stderr)
        self.assertEqual(self.push('state', writer='range').returncode, 0)

    def test_rebase_revalidates_against_the_new_remote_tip(self):
        # The remote advances while the job runs, including a reviewed source change pushed by someone else. After the
        # rebase only this job's own commits are outgoing, so the push succeeds; the source change is not blamed on it.
        subprocess.run(['git', 'clone', '-q', str(self.origin), str(self.other)], check=True, capture_output=True)
        (self.other / 'collector.py').write_text('print("reviewed revision")\n')
        (self.other / 'data/a.jsonl').write_text('{"other": 1}\n')
        git(self.other, *ID, 'commit', '-qam', 'merged revision')
        git(self.other, 'push', '-q', 'origin', 'main')
        (self.work / 'data/c.jsonl').write_text('{}\n')
        r = self.push('data')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('data/c.jsonl', self.remote_files())
        self.assertEqual(git(self.origin, 'show', 'main:collector.py'), 'print("reviewed revision")')

    def test_rebase_does_not_launder_a_bad_local_commit(self):
        subprocess.run(['git', 'clone', '-q', str(self.origin), str(self.other)], check=True, capture_output=True)
        (self.other / 'data/a.jsonl').write_text('{"other": 2}\n')
        git(self.other, *ID, 'commit', '-qam', 'concurrent data')
        git(self.other, 'push', '-q', 'origin', 'main')
        remote_tip = git(self.origin, 'rev-parse', 'main')
        (self.work / 'collector.py').write_text('print("local edit")\n')
        git(self.work, *ID, 'commit', '-qam', 'local source edit')
        r = self.push('data')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), remote_tip)

    def test_deletions_maintained_files_and_symlinks_are_refused(self):
        os.remove(self.work / 'data/a.jsonl')
        r = self.push('data')
        self.assertIn('data/a.jsonl: deletion', r.stderr)
        git(self.work, 'reset', '-q'); git(self.work, 'checkout', '-q', 'HEAD', '--', 'data/a.jsonl')
        (self.work / 'registry/README.md').write_text('edited\n')
        r = self.push('registry', writer='intake')
        self.assertIn('registry/README.md: maintained by a revision', r.stderr)
        git(self.work, 'reset', '-q'); git(self.work, 'checkout', '-q', 'HEAD', '--', 'registry/README.md')
        os.symlink('/etc/passwd', self.work / 'data/link')
        r = self.push('data')
        self.assertIn('data/link: not a regular file (mode 120000)', r.stderr)

    def test_calendar_copies_may_be_added_never_modified(self):
        name = 'desk/calendars/' + 'a' * 64 + '.csv'
        (self.work / name).parent.mkdir(parents=True)
        (self.work / name).write_text('x\n')
        self.assertEqual(self.push('desk/calendars', writer='range').returncode, 0)
        (self.work / name).write_text('y\n')
        r = self.push('desk/calendars', writer='range')
        self.assertIn('content-addressed file may only be added', r.stderr)
        git(self.work, 'reset', '-q'); git(self.work, 'checkout', '-q', 'HEAD', '--', name)
        (self.work / 'desk/calendars/notahash.csv').write_text('z\n')
        r = self.push('desk/calendars', writer='range')
        self.assertIn('desk/calendars/notahash.csv: not a documented output', r.stderr)

    def test_missing_or_unknown_writer_pushes_nothing(self):
        before = git(self.origin, 'rev-parse', 'main')
        (self.work / 'data/a.jsonl').write_text('{"x": 4}\n')
        r = self.push('data', writer=None)
        self.assertIn('DESK_WRITER is unset', r.stderr)
        r = self.push('data', writer='nobody')
        self.assertIn("writer 'nobody' is not listed", r.stderr)
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), before)

    def test_refusal_with_the_deploy_key_still_removes_it_and_never_prints_it(self):
        (self.work / 'collector.py').write_text('print("x")\n')
        git(self.work, 'add', 'collector.py')
        key = '-----BEGIN OPENSSH PRIVATE KEY-----\nsecret\n-----END OPENSSH PRIVATE KEY-----'
        r = self.push('data', DESK_DEPLOY_KEY=key, DESK_PUSH_URL=str(self.origin))
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(list(self.keytmp.iterdir()), [])
        self.assertNotIn('secret', r.stdout + r.stderr)


class PolicyTests(unittest.TestCase):
    """The policy covers what each workflow actually pushes, and grants no source access."""
    def setUp(self):
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        import push_guard
        self.g = push_guard
        self.policy = push_guard.load()

    def test_every_persistence_call_is_inside_its_writers_policy(self):
        seen = set()
        for wf in sorted((ROOT / '.github/workflows').glob('*.yml')):
            text = wf.read_text()
            for step in re.split(r'\n {6}- ', text)[1:]:
                m = re.search(r'DESK_WRITER: ([a-z-]+)', step)
                if not m:
                    continue
                writer = m.group(1)
                rule = self.policy[writer]
                self.assertEqual(rule['workflow'], f'.github/workflows/{wf.name}')
                seen.add(writer)
                call = re.search(r'commit_push\.sh ([^\n]+)', step)
                if not call:            # intake: process_issues.py calls commit_push.sh with registry and state
                    continue
                for arg in call.group(1).split():
                    covered = any(e == arg or e.startswith(arg.rstrip('/') + '/') or arg.startswith(e.rstrip('/') + '/')
                                  or (e.endswith('/') and arg == e.rstrip('/')) for e in rule['allow']) \
                        or any(re.search(p, arg + '/' + 'a' * 64 + '.csv') for p in rule.get('add_only', []))
                    self.assertTrue(covered, f'{wf.name}: {writer} pushes {arg}, not in its policy')
        self.assertEqual(seen, set(self.policy))

    def test_no_writer_may_touch_maintained_files(self):
        for path in ('collector.py', '.github/workflows/collect.yml', 'scripts/commit_push.sh', 'scripts/writers.json',
                     'desk/range_job.py', 'registry/README.md', 'SHA256SUMS', 'docs/OPERATIONS.md'):
            for writer, rule in self.policy.items():
                self.assertIsNotNone(self.g.allowed(rule, path, 'M', '100644'), f'{writer} may write {path}')


if __name__ == '__main__':
    unittest.main()
