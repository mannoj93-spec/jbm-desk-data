"""The release manifest: a changed covered file fails, the refreshed release passes, data stays out (repo 2.23)."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check_checksums', ROOT / 'scripts/check_checksums.py')
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)


class ChecksumTests(unittest.TestCase):
    def repo(self, d):
        d = Path(d)
        for rel, text in {'README.md': 'a', 'desk/x.py': 'b', 'dashboard/app.js': 'c', 'data/p.jsonl': 'd',
                          'streams/s.jsonl': 'e', 'registry/README.md': 'f', 'registry/r-1.json': 'g',
                          'desk/deployments.jsonl': 'h', 'desk/research/o21/original/run.py': 'i'}.items():
            (d / rel).parent.mkdir(parents=True, exist_ok=True)
            (d / rel).write_text(text)
        subprocess.run(['git', 'init', '-q', str(d)], check=True)
        subprocess.run(['git', '-C', str(d), 'add', '.'], check=True)
        return d

    def test_scope_excludes_data_logs_and_nested_manifests(self):
        with tempfile.TemporaryDirectory() as d:
            d = self.repo(d)
            self.assertEqual(K.scope(d), ['README.md', 'dashboard/app.js', 'desk/x.py', 'registry/README.md'])

    def test_changed_covered_file_fails_and_refreshed_release_passes(self):
        with tempfile.TemporaryDirectory() as d:
            d = self.repo(d)
            K.refresh(d)
            self.assertEqual(K.check(d), [])
            (d / 'dashboard/app.js').write_text('changed')
            self.assertEqual(K.check(d), ['hash mismatch: dashboard/app.js'])
            (d / 'data/p.jsonl').write_text('collector appends never fail the release check')
            self.assertEqual(K.check(d), ['hash mismatch: dashboard/app.js'])
            K.refresh(d)
            self.assertEqual(K.check(d), [])

    def test_unlisted_and_stale_entries_fail(self):
        with tempfile.TemporaryDirectory() as d:
            d = self.repo(d)
            K.refresh(d)
            (d / 'desk/new.py').write_text('x')
            subprocess.run(['git', '-C', str(d), 'add', 'desk/new.py'], check=True)
            self.assertIn('in scope but not listed: desk/new.py', K.check(d))
            (d / 'SHA256SUMS').write_text((d / 'SHA256SUMS').read_text() + '0' * 64 + '  data/p.jsonl\n')
            self.assertIn('listed but out of scope: data/p.jsonl', K.check(d))

    def test_malformed_or_duplicate_lines_are_refused(self):
        with self.assertRaises(ValueError):
            K.parse('nothash  a\n')
        with self.assertRaises(ValueError):
            K.parse(('0' * 64 + '  a\n') * 2)

    def test_this_checkout_verifies(self):
        self.assertEqual(K.check(ROOT), [])


if __name__ == '__main__':
    unittest.main()
