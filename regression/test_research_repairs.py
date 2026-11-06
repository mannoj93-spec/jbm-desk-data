"""Regression coverage for reviewed source repair, strict replay and isolated health failures."""
import copy
import datetime as dt
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import range_source_repair as R
import options_pilot_report as P
import market_study_ops as O
from replay_precision import matches
from regression import test_options_pilot as pilot_fixture
from regression.test_options_pilot import capture
from regression import test_market_study_ops as ops_fixture
from research_tools.options_pilot import study as S, core as K


class Precision(unittest.TestCase):
    def test_cross_runtime_roundoff_only_at_explicit_iv_fields(self):
        expected = S.compare(capture())
        rounded = copy.deepcopy(expected)
        for candidate in rounded['candidates'].values():
            if candidate['pair']:
                for name in ('call_iv', 'put_iv'):
                    candidate['pair'][name] += 7e-15
        self.assertTrue(P.selection_matches(expected, rounded))
        for field, value in [('call_iv', .51), ('call_K', 80000.00000000001), ('F', 80000.00000000001)]:
            bad = copy.deepcopy(expected)
            pair = next(c['pair'] for c in bad['candidates'].values() if c['pair'])
            pair[field] = value
            self.assertFalse(P.selection_matches(expected, bad))
        bad = copy.deepcopy(expected);bad['horizons']['7']['nearest-eligible']['value'] += 1e-10
        self.assertFalse(P.selection_matches(expected, bad))
        for invalid in [True, float('nan'), float('inf'), '0.5']:
            self.assertFalse(matches(.5, invalid, lambda p: True))
        self.assertFalse(matches({'a':1}, {'a':True}, lambda p: False))

    def test_adapter_replays_unchanged_captures_and_rejects_tampering(self):
        f = pilot_fixture.Pilot();f.setUp();self.addCleanup(f.doCleanups);f.activate()
        with patch.object(S, 'Store') as store:
            store.return_value.option_quotes.return_value=[f.cap]
            S.collect(f.base, f.slot+20*K.MIN, clock=lambda:f.slot+20*K.MIN)
        original = K.Journal(f.base,'observations').rows[0]
        artifact = S.read_artifact(f.base,original['data']['artifact'])
        for v in artifact['selection']['candidates'].values():
            if v['pair']: v['pair']['call_iv'] += 7e-15
        ref = S.artifact(f.base,artifact)
        path=f.base/K.STREAM/'observations.jsonl';path.unlink()
        K.Journal(f.base,'observations').add(original['id'],dict(original['data'],artifact=ref))
        self.assertEqual(P.report(f.base,f.slot+K.HOUR)['captured'],1)
        with self.assertRaisesRegex(ValueError,'reproduction'):S.report(f.base,f.slot+K.HOUR)
        artifact['selection']['horizons']['7']['nearest-eligible']['instruments'][0]='changed'
        ref=S.artifact(f.base,artifact);path.unlink()
        K.Journal(f.base,'observations').add(original['id'],dict(original['data'],artifact=ref))
        with self.assertRaisesRegex(ValueError,'reproduction'):P.report(f.base,f.slot+K.HOUR)


class HealthIsolation(unittest.TestCase):
    setUp = ops_fixture.Diagnostics.setUp
    forecast = ops_fixture.Diagnostics.forecast

    def test_pilot_failure_keeps_other_verified_components_and_source_incidents(self):
        self.forecast()
        with patch.object(O,'options_pilot_health', side_effect=ValueError('bad pilot')), \
             patch.object(O,'state_v2_health') as state:
            out=O.safe_build(self.base,self.slot+K.HOUR)
        self.assertEqual(out['integrity'],'failed')
        self.assertIn('state',out['studies'])
        self.assertIn('source_quality',out)
        self.assertEqual(out['components']['options_expiry']['integrity'],'failed')
        self.assertEqual(out['components']['source_quality']['integrity'],'ok')
        state.assert_called_once()
        self.assertIn('bad pilot',O.markdown(out))

    def test_failed_component_partial_output_is_discarded(self):
        def fail(base,now,out):
            out['studies']['fake']={'unverified':True}
            raise ValueError('broken')
        with patch.object(O,'v1_health',side_effect=fail):
            out=O.build(self.base,self.slot+K.HOUR)
        self.assertNotIn('fake',out['studies'])
        self.assertIn('source_quality',out)
        self.assertEqual(out['integrity'],'failed')

    def test_stale_report_clock_is_not_replaced_by_health_clock(self):
        (self.base/'reports').mkdir()
        (self.base/'reports/options_expiry_pilot.json').write_text(json.dumps({'generated_ms':self.slot}))
        out=O.build(self.base,self.slot+2*K.HOUR)
        f=out['report_freshness']['options_expiry']
        self.assertEqual((f['state'],f['last_success_ms']),('stale',self.slot))


class SourceRepair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence=json.loads(R.EVIDENCE.read_text())

    def test_retained_raw_bytes_reproduce_complete_month_and_approved_overlap(self):
        delta=R.replay_evidence(self.evidence)
        self.assertEqual(len(delta['bars']),186)
        self.assertEqual(delta['source_repair']['overlap_checked'],12)
        self.assertEqual(delta['source_repair']['filled'],R.GAP)
        self.assertEqual(delta['dvol_admissibility']['state'],'ok')
        self.assertEqual(R.missing(delta['bars'],R.START,R.END),[])

    def test_rejects_changed_raw_response_and_future_retrieval(self):
        for mutate in [lambda e:e['responses'][R.API_URL].update(raw_base64='e30='),
                       lambda e:e['responses'][R.API_URL].update(received_utc='2099-01-01T00:00:00Z')]:
            bad=copy.deepcopy(self.evidence);mutate(bad)
            with self.assertRaises((ValueError,RuntimeError)):R.replay_evidence(bad)

    def test_rejects_another_gap_overlap_change_and_partial_api(self):
        e=self.evidence
        import base64
        def get(url):
            r=e['responses'][url];return base64.b64decode(r['raw_base64']),r['headers']
        state,bars,report=R.A.load_klines('2026-10',opener=get)
        raw=get(R.API_URL)[0]
        for wrong in [bars[1:], bars+[dict(bars[0])]]:
            with self.assertRaises(ValueError):R.repaired_bars(state,wrong,report,raw)
        values=json.loads(raw);values[0][5]=str(float(values[0][5])+1)
        with self.assertRaisesRegex(ValueError,'overlap'):R.repaired_bars(state,bars,report,json.dumps(values).encode())
        with self.assertRaises(ValueError):R.repaired_bars(state,bars,report,json.dumps(values[1:]).encode())

    def test_readiness_reports_exact_missing_times_without_mutation(self):
        now=dt.datetime(2026,10,31,22,tzinfo=R.UTC)
        delta=R.replay_evidence(self.evidence)
        rows=[b for b in delta['bars'] if b['open_utc'] < '2026-10-31T00:00:00Z' and b['open_utc'] not in R.GAP]
        out=R.readiness(now,span=lambda *args:('incomplete',rows,[{'state':'incomplete'}]))
        self.assertEqual(out['state'],'blocked');self.assertEqual(out['missing_4h_opens'],R.GAP)
        with patch.object(R.A,'load_klines_span') as fetch:
            out=R.readiness(dt.datetime(2026,11,15,tzinfo=R.UTC))
            self.assertEqual(out['state'],'outside-month-boundary-window');fetch.assert_not_called()

    def test_preparation_is_idempotent_and_preserves_prior_fits(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            shutil.copytree(R.ROOT/'desk/inputs/refit',base/'desk/inputs/refit')
            now=R.J.R._t(self.evidence['captured_utc'])+dt.timedelta(seconds=1)
            R.prepare(base,now)
            before={p:p.read_bytes() for p in (base/'desk/inputs').rglob('*.gz')}
            R.prepare(base,now)
            self.assertEqual(before,{p:p.read_bytes() for p in (base/'desk/inputs').rglob('*.gz')})
            bars,dvol,links=R.J.history_chain(base)
            self.assertEqual(bars[-1]['open_utc'],'2026-10-31T20:00:00Z')
            self.assertFalse((base/'registry').exists())
            self.assertFalse((base/'desk/fits').exists())


if __name__=='__main__':unittest.main()
