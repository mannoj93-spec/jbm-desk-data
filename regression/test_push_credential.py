"""commit_push.sh push credential (repo 2.25): with DESK_DEPLOY_KEY the data push goes to the SSH remote using the
deploy key (here a local bare repository stands in through DESK_PUSH_URL), the key never outlives the run, and
origin/<branch> is refreshed for the persistence check; without it the workflow-token path is unchanged."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/commit_push.sh'


def git(cwd, *args):
    return subprocess.run(['git', '-C', str(cwd), *args], check=True, capture_output=True, text=True).stdout.strip()


class PushCredentialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.origin, self.ssh, self.work = d / 'origin.git', d / 'ssh.git', d / 'work'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'main', str(self.origin)], check=True)
        subprocess.run(['git', 'clone', '-q', str(self.origin), str(self.work)], check=True, capture_output=True)
        git(self.work, 'checkout', '-q', '-b', 'main')
        (self.work / 'data').mkdir()
        (self.work / 'data/a.jsonl').write_text('{}\n')
        git(self.work, '-c', 'user.name=t', '-c', 'user.email=t@t', 'add', '.')
        git(self.work, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-q', '-m', 'init')
        git(self.work, 'push', '-q', 'origin', 'main')
        # the "SSH remote" is the same repository reached another way, as GitHub's SSH endpoint is
        os.symlink(self.origin, self.ssh)
        (self.work / 'data/b.jsonl').write_text('{"x": 1}\n')
        self.tmpdir = d / 'tmp'
        self.tmpdir.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_push(self, **env):
        e = {k: v for k, v in os.environ.items() if k not in ('DESK_DEPLOY_KEY', 'DESK_PUSH_URL')}
        e.update(TMPDIR=str(self.tmpdir), PERSIST_BUDGET_S='60', DESK_WRITER='collector')
        e.update(env)
        return subprocess.run(['bash', str(SCRIPT), 'data'], cwd=self.work, env=e, capture_output=True, text=True)

    def test_without_the_key_the_workflow_token_path_is_unchanged(self):
        r = self.run_push()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('persistence: workflow token', r.stdout)
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), git(self.work, 'rev-parse', 'HEAD'))

    def test_with_the_key_it_pushes_to_the_ssh_remote_and_removes_the_key(self):
        r = self.run_push(DESK_DEPLOY_KEY='-----BEGIN OPENSSH PRIVATE KEY-----\ntest\n-----END OPENSSH PRIVATE KEY-----',
                          DESK_PUSH_URL=str(self.ssh))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('persistence: deploy key', r.stdout)
        head = git(self.work, 'rev-parse', 'HEAD')
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), head)
        self.assertEqual(git(self.work, 'rev-parse', 'origin/main'), head)          # refreshed for check_persisted
        self.assertEqual(list(self.tmpdir.iterdir()), [])                           # key directory removed
        self.assertNotIn('BEGIN OPENSSH', r.stdout + r.stderr)                      # key never printed

    def test_with_the_key_an_unreachable_remote_fails_and_still_removes_the_key(self):
        r = self.run_push(DESK_DEPLOY_KEY='k', DESK_PUSH_URL=str(Path(self.tmp.name) / 'missing.git'), PERSIST_BUDGET_S='12')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('remote persistence not confirmed', r.stderr)
        self.assertEqual(list(self.tmpdir.iterdir()), [])

    def test_every_persistence_step_passes_the_key_and_nothing_else_does(self):
        import re
        with_key = 0
        for wf in sorted((ROOT / '.github/workflows').glob('*.yml')):
            text = "\n".join(l.split(' #')[0] for l in wf.read_text().splitlines() if not l.strip().startswith('#'))
            head, _, body = text.partition('\njobs:')
            self.assertNotIn('DESK_DEPLOY_KEY', head, f'{wf.name}: workflow-level key')
            for step in re.split(r'\n {6}- ', body)[1:]:
                pushes = 'commit_push.sh' in step or 'process_issues.py' in step
                has_key = 'DESK_DEPLOY_KEY: ${{ secrets.DESK_DEPLOY_KEY }}' in step
                self.assertEqual(pushes, has_key, f'{wf.name}: {step[:60]}')
                # repo 2.25: every persistence step names its writer (scripts/writers.json)
                self.assertEqual(pushes, bool(re.search(r'\n\s*DESK_WRITER: [a-z-]+', step)), f'{wf.name}: {step[:60]}')
                with_key += has_key
        self.assertEqual(with_key, 10)   # 2.27: + the collector's yield-receipt persistence step

if __name__ == '__main__':
    unittest.main()
