"""The dashboard must not mutate evidence, select retired cards, or fake missing data."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_dashboard', ROOT / 'scripts/build_dashboard.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DashboardTests(unittest.TestCase):
    def test_real_snapshot_preserves_current_evidence_and_forecasts(self):
        import hashlib
        paths = [ROOT / 'reports/range_status.json', ROOT / 'reports/latest.md', ROOT / 'research/evidence/index.json']
        before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        with tempfile.TemporaryDirectory() as tmp:
            payload = module.build(ROOT, Path(tmp) / 'site')
            expected = json.loads(paths[0].read_text())
            self.assertEqual(payload['range'], expected)
            index = json.loads(paths[2].read_text())
            for card in payload['research']['designs']:
                self.assertEqual(card['evaluation_version'], index['designs'][card['design']]['current'])
                self.assertTrue(card['source'].startswith('research/evidence/v2/'))
            self.assertEqual(payload['workflow']['status'], 'unverified')
            self.assertNotIn('null', payload['research']['statuses'])
            self.assertLess((Path(tmp) / 'site/data.json').stat().st_size, 1_000_000)
            for rel, digest in payload['sources'].items():
                self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), digest)
        self.assertEqual(before, {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})

    def test_coverage_rejects_changed_schema_instead_of_publishing_zeros(self):
        report = (ROOT / 'reports/latest.md').read_text()
        with self.assertRaises(ValueError):
            module.coverage(report.replace('| Source |', '| Changed |'))
        with self.assertRaises(ValueError):
            module.coverage(report.replace('Generated ', 'Built '))

    def test_missing_prices_stay_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = module.price_history(Path(tmp), lambda p: None)
        self.assertEqual(result['bars'], [])
        self.assertIsNone(result['latest'])
        self.assertIsNone(result['observed_utc'])

    def test_price_aggregation_uses_latest_observation_and_does_not_fill_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            folder = base / 'data/prices/binance_klines_1m_BTCUSDT_perp'
            folder.mkdir(parents=True)
            rows = [{'observed_at': 100, 'bars': [[0, 10, 12, 8, 11], [60000, 11, 15, 10, 14]]},
                    {'observed_at': 200, 'bars': [[60000, 11, 16, 9, 15], [7200000, 20, 22, 18, 21]]}]
            (folder / '2026-10.jsonl').write_text('\n'.join(json.dumps(r) for r in rows))
            result = module.price_history(base, lambda p: None)
        self.assertEqual(result['bars'], [[0, 10, 16, 8, 15, 2], [7200000, 20, 22, 18, 21, 1]])
        self.assertEqual(result['latest']['close'], 21)

    def test_refuses_to_overwrite_evidence(self):
        with self.assertRaises(ValueError):
            module.build(ROOT, ROOT / 'reports')
        with self.assertRaises(ValueError):
            module.build(ROOT, ROOT)


if __name__ == '__main__':
    unittest.main()
