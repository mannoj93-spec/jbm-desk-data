"""The dashboard must not mutate evidence, select retired cards, or fake missing data."""
import importlib.util
import json
import re
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_dashboard', ROOT / 'scripts/build_dashboard.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DashboardTests(unittest.TestCase):
    def test_asset_urls_change_with_code_and_dependency_but_stay_stable_for_same_bytes(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / 'source', Path(tmp) / 'site'
            shutil.copytree(ROOT / 'dashboard', source)
            output.mkdir()

            def build_assets():
                module.write_assets(source, output)
                index = (output / 'index.html').read_text()
                app = re.search(r'src="(app\.[a-f0-9]+\.js)"', index).group(1)
                style = re.search(r'href="(styles\.[a-f0-9]+\.css)"', index).group(1)
                dependency = re.search(r"from './(model\.[a-f0-9]+\.js)'", (output / app).read_text()).group(1)
                for filename in (app, style, dependency):
                    self.assertTrue((output / filename).is_file())
                return app, style, dependency

            first = build_assets()
            self.assertEqual(first, build_assets())
            with (source / 'model.js').open('a') as file:
                file.write('\n// dependency update\n')
            second = build_assets()
            self.assertNotEqual(first[0], second[0])
            self.assertEqual(first[1], second[1])
            self.assertNotEqual(first[2], second[2])
            with (source / 'styles.css').open('a') as file:
                file.write('\n/* style update */\n')
            third = build_assets()
            self.assertNotEqual(second[1], third[1])
            self.assertEqual(second[0], third[0])
            with (source / 'app.js').open('a') as file:
                file.write('\n// interface update\n')
            fourth = build_assets()
            self.assertNotEqual(third[0], fourth[0])
            self.assertEqual(third[2], fourth[2])

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
            # 2.23: research clocks come from the cards' cutoff_ms, the index's 'updated' is named as such
            self.assertEqual(payload['schema'], 'jbm-dashboard/2')
            self.assertNotIn('generated_utc', payload['research'])
            cuts = sorted(c['cutoff_utc'] for c in payload['research']['designs'] if c['cutoff_utc'])
            self.assertEqual((payload['research']['oldest_cutoff_utc'], payload['research']['source_cutoff_utc']),
                             (cuts[0], cuts[-1]) if cuts else (None, None))
            self.assertEqual(payload['research']['index_updated_utc'], module.utc(index['updated']))
            self.assertEqual(payload['paper'], json.loads((ROOT / 'reports/paper_ps1.json').read_text()))
            self.assertEqual(payload['companion'], json.loads((ROOT / 'reports/companion_b1.json').read_text()))
            # 2.24: the operational health report is carried as written, or null when it does not exist yet
            hp = ROOT / 'reports/health.json'
            self.assertEqual(payload['ops'], json.loads(hp.read_text()) if hp.exists() else None)
            # Optional release records preserve source states, including service-pass / certification-insufficient.
            developments = payload['developments']
            self.assertIn('# ' + developments['release']['title'], (ROOT / 'CHANGELOG.md').read_text())
            for protocol in developments['protocols']:
                original = json.loads((ROOT / protocol['source']).read_text())
                self.assertEqual(protocol['status'], original['status'])
                self.assertEqual(protocol['effective_utc'], module.utc(original.get('effective_utc')))
            acceptance = developments['acceptance']
            original = json.loads((ROOT / acceptance['source']).read_text())
            self.assertEqual(acceptance['verdict'], original['verdict'])
            self.assertEqual(acceptance['service_verdict'], original['service_verdict'])
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


class DevelopmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.sources = []

    def write(self, path, value):
        target = self.base / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value))
        return target

    def summary(self):
        return module.developments(self.base, lambda path: self.sources.append(str(path.relative_to(self.base))))

    @staticmethod
    def acceptance(version, verdict, start='2026-10-07', end='2026-10-08', evaluated='2026-10-12'):
        return {'checker': f'acceptance-{version}', 'verdict': verdict, 'service_verdict': 'pass',
                'reason': 'Service targets met; independent timer receipts incomplete.',
                'clocks': {'window': [start + 'T00:00:00Z', end + 'T00:00:00Z'],
                           'evaluated_utc': evaluated + 'T12:00:00Z'}}

    def test_missing_optional_records_stay_unknown(self):
        self.assertEqual(self.summary(), {'release': None, 'catalog': None, 'protocols': [], 'acceptance': None})
        self.assertEqual(self.sources, [])

    def test_prepared_protocol_and_catalog_keep_their_own_meanings(self):
        protocol_path = 'research/registrations/dir1-prepared/protocol.json'
        self.write(protocol_path, {'id': 'DIR1', 'status': 'prepared', 'effective_utc': None})
        pilot_path = 'stream/pilot_e1.json'
        self.write(pilot_path, {'id': 'E1-pilot-1', 'status': 'prepared; not commissioned'})
        catalog_path = 'research_tools/catalog.json'
        self.write(catalog_path, {'schema': 'desk-data-catalog/1', 'version': 'catalog-1.0.0',
                                 'as_of_utc': '2026-10-19T18:00:00Z', 'datasets': [{}, {}],
                                 'feature_families': [{'id': 'flow', 'status': 'supported'},
                                                      {'id': 'books', 'status': 'gated: uncommissioned'}]})
        result = self.summary()
        self.assertEqual([p['status'] for p in result['protocols']], ['prepared', 'prepared; not commissioned'])
        self.assertTrue(all(p['effective_utc'] is None for p in result['protocols']))
        self.assertEqual(result['catalog']['dataset_count'], 2)
        self.assertEqual(result['catalog']['feature_families'][1]['status'], 'gated: uncommissioned')
        self.assertEqual(set(self.sources), {protocol_path, pilot_path, catalog_path})

    def test_latest_window_preserves_result_of_record_beside_newer_audit(self):
        self.write('docs/acceptance/results/2026-10-06/result-acceptance-3.0.0.json',
                   self.acceptance('3.0.0', 'pass', start='2026-10-06', end='2026-10-07'))
        folder = 'docs/acceptance/results/2026-10-07/'
        self.write(folder + 'result-acceptance-3.0.0.json', self.acceptance('3.0.0', 'insufficient'))
        self.write(folder + 'supplementary-acceptance-3.9.0.json', self.acceptance('3.9.0', 'insufficient'))
        self.write(folder + 'supplementary-acceptance-3.10.0.json',
                   self.acceptance('3.10.0', 'pass', evaluated='2026-10-14'))
        result = self.summary()['acceptance']
        self.assertEqual(result['verdict'], 'insufficient')
        self.assertEqual(result['service_verdict'], 'pass')
        self.assertEqual(result['checker'], 'acceptance-3.0.0')
        self.assertEqual(result['supplementary']['checker'], 'acceptance-3.10.0')
        self.assertEqual(result['supplementary']['verdict'], 'pass')
        self.assertEqual(len(self.sources), 4)

    def test_mismatched_audit_window_is_rejected(self):
        folder = 'docs/acceptance/results/2026-10-07/'
        self.write(folder + 'result-acceptance-3.0.0.json', self.acceptance('3.0.0', 'insufficient'))
        self.write(folder + 'supplementary-acceptance-3.3.0.json',
                   self.acceptance('3.3.0', 'pass', start='2026-10-06'))
        with self.assertRaisesRegex(ValueError, 'does not match'):
            self.summary()

    def test_malformed_optional_record_is_not_presented_as_missing(self):
        self.write('research/registrations/dir1-prepared/protocol.json', {'id': 'DIR1', 'status': None})
        with self.assertRaisesRegex(ValueError, 'protocol status'):
            self.summary()

    def test_release_revision_survives_a_presentation_entry(self):
        (self.base / 'CHANGELOG.md').write_text('# Dashboard refresh — 2026-10-19\n\n'
                                                '# Revision 2.29 (crypto-desk 12.4.20) — 2026-10-19\n')
        result = self.summary()['release']
        self.assertEqual(result['revision'], '2.29')
        self.assertEqual(result['date'], '2026-10-19')
        self.assertEqual(self.sources, ['CHANGELOG.md'])


if __name__ == '__main__':
    unittest.main()
