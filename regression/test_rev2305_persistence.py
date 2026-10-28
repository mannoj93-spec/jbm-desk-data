"""Repo 2.30.5: persistence from a shallow (depth-1) checkout after main received a merge commit.

The collector checks out main at depth 1. On Oct 26 2026 three collector runs (40251817627, 40327143379,
40414468575) started minutes before a pull-request merge; their pushes were rejected because main had advanced, and
the plain `git fetch` that followed tried to download the merged branch's whole history past the shallow boundary
(1.5 GB, unfinished after 150 s in a reproduction against the real repository), timed out twice at 45 s and lost
the push. These tests build the same shape locally: a long origin history, a depth-1 working clone, and a merge on
origin whose second parent forks below the working clone's shallow boundary. They drive the real script.
"""
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_rev230_persistence as base  # noqa: E402  (module import: its own test class is not collected twice)

REAL_GIT, git = base.REAL_GIT, base.git

HISTORY = 60          # commits on origin before the working clone is taken (more than PERSIST_FETCH_DEPTH below the fork)


class ShallowMergePersistenceTests(base.PersistenceRepairTests):
    def setUp(self):
        super().setUp()
        d = Path(self.tmp.name)
        # a long history on origin, then a side branch forked from an old commit (below a depth-1 boundary)
        for i in range(HISTORY):
            (self.other / 'data').mkdir(exist_ok=True)
            (self.other / f'data/h{i}.jsonl').write_text(f'{{"h": {i}}}\n' * 50)
            git(self.other, 'add', '.')
            git(self.other, '-c', 'user.name=o', '-c', 'user.email=o@o', 'commit', '-q', '-m', f'history {i}')
        git(self.other, 'push', '-q', 'origin', 'main')
        self.fork = git(self.other, 'rev-parse', 'HEAD~10')
        self.root = git(self.other, 'rev-list', '--max-parents=0', 'HEAD')
        # the collector's checkout: depth 1 at the current tip (file:// so the depth is honoured)
        self.work = d / 'shallow'
        subprocess.run([REAL_GIT, 'clone', '-q', '--depth=1', '--branch', 'main', f'file://{self.origin}',
                        str(self.work)], check=True, capture_output=True)
        self.assertEqual(git(self.work, 'rev-list', '--count', 'HEAD'), '1')
        git(self.other, 'pull', '-q', '--ff-only', 'origin', 'main')
        self.init = git(self.origin, 'rev-parse', 'main')

    def merge_side_branch_on_origin(self):
        """A pull request branched from an old commit, merged into main with a merge commit."""
        git(self.other, 'checkout', '-q', '-b', 'feature', self.fork)
        (self.other / 'docs').mkdir(exist_ok=True)
        (self.other / 'docs/feature.md').write_text('feature\n')
        git(self.other, 'add', '.')
        git(self.other, '-c', 'user.name=o', '-c', 'user.email=o@o', 'commit', '-q', '-m', 'feature')
        git(self.other, 'checkout', '-q', 'main')
        git(self.other, '-c', 'user.name=o', '-c', 'user.email=o@o', 'merge', '-q', '--no-ff', '-m',
            'Merge pull request', 'feature')
        git(self.other, 'push', '-q', 'origin', 'main')
        return git(self.other, 'rev-parse', 'HEAD')

    def test_push_after_a_merge_lands_without_fetching_the_history(self):
        merge = self.merge_side_branch_on_origin()
        self.collect()
        r = self.run_push()
        self.assert_landed_once(r)
        self.assertIn('stage=push attempt=1 result=failed class=rejected', r.stdout)
        self.assertEqual(git(self.origin, 'rev-parse', 'main~1'), merge)            # our commit sits on the merge
        self.assertEqual(git(self.origin, 'show', 'main:docs/feature.md'), 'feature')
        # the checkout stayed shallow: an unbounded fetch walks the merged branch down to the first commit
        root_present = subprocess.run([REAL_GIT, '-C', str(self.work), 'cat-file', '-e', self.root]).returncode == 0
        self.assertFalse(root_present, 'the fetch downloaded the merged branch history down to the root commit')
        self.assertTrue((self.work / '.git/shallow').exists())

    def test_landed_push_with_later_commits_on_top_is_confirmed_by_read_back(self):
        """An uncertain push that did land, followed by another writer's commit: the bounded read-back still sees
        our commit in the remote's ancestry (a depth-1 read-back would not, and would push again)."""
        self.merge_side_branch_on_origin()
        git(self.work, 'fetch', '-q', '--depth=1', 'origin', 'main')
        git(self.work, 'reset', '-q', '--hard', 'FETCH_HEAD')
        git(self.work, 'update-ref', 'refs/remotes/origin/main', 'FETCH_HEAD')
        self.collect()
        self.faults('push 1 lost', 'fetch 1 advance')
        r = self.run_push()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('stage=verify result=remote-contains-head', r.stdout)
        self.assertEqual(self.count('push'), 1)
        self.assertEqual(self.remote_log().count('Update desk data'), 1)

    def test_conflict_after_a_merge_still_stops_with_data_retained(self):
        self.merge_side_branch_on_origin()
        (self.other / 'data/a.jsonl').write_text('{"row": "theirs"}\n')
        git(self.other, '-c', 'user.name=o', '-c', 'user.email=o@o', 'commit', '-q', '-am', 'their edit')
        git(self.other, 'push', '-q', 'origin', 'main')
        theirs = git(self.origin, 'rev-parse', 'main')
        self.collect('{"row": "ours"}\n', 'data/a.jsonl')
        r = self.run_push()
        self.assert_not_confirmed(r, 'conflict', 'rebase')
        self.assertEqual(git(self.origin, 'rev-parse', 'main'), theirs)
        self.assertEqual((self.work / 'data/a.jsonl').read_text(), '{"row": "ours"}\n')


# the inherited full-clone scenarios run again here from the shallow checkout
if __name__ == '__main__':
    unittest.main()
