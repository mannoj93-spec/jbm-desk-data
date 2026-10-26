"""A corrected feature must start a new clock and use identical train/predict selection."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from desk import stream_util as U
from research_tools import panel as P
from research_tools.market_studies import core as V1, models as OLD
from research_tools.state_v2 import core as K, models as M, study as S
from research_tools.state_v2.__main__ import main, paused


class Depth(unittest.TestCase):
    def setUp(self):
        self.t = 100 * K.DAY
        self.start, self.end = self.t - 32*K.MIN, self.t - 17*K.MIN

    def snap(self, age, avail_age=None, **fields):
        m = self.t - age*K.MIN
        a = self.t - (age if avail_age is None else avail_age)*K.MIN
        return (m, a, {'t': m, 'observed_at': a, 'depth_binance_usdt':
                      {'st': 'ok', 't_ret': m, 'bid_btc_25': 2., 'ask_btc_25': 3., **fields}})

    def select(self, items):
        row = {'inputs': {}}
        state, amount = M.depth(row, P._Avail(items), self.t, self.start, self.end)
        return state, amount, row

    def test_production_pattern_skips_stale_inside_window_for_fresh_aligned(self):
        items = [self.snap(31), self.snap(16), self.snap(1)]
        old = P._depth({'inputs': {}}, P._Avail(items), self.t, self.start, self.end)
        self.assertTrue(old[0].startswith('stale-depth'))
        state, amount, row = self.select(items)
        self.assertEqual((state, amount), ('ok', 5))
        self.assertEqual(row['inputs']['sources']['depth']['age_s'], 16*60)
        self.assertEqual(row['inputs']['depth_selection_v2']['selected']['distance_ms'], K.MIN)

    def test_unavailable_or_future_measured_never_used(self):
        for bad in [self.snap(16, avail_age=-1), self.snap(-1), self.snap(16, avail_age=17)]:
            self.assertIsNone(self.select([bad])[1])

    def test_invalid_or_too_small_candidates_do_not_shadow_good(self):
        for fields in [{'st':'error'}, {'bid_btc_25': None}, {'ask_btc_25': -1},
                       {'bid_btc_25': .1, 'ask_btc_25': .1}]:
            self.assertEqual(self.select([self.snap(20, **fields), self.snap(16)])[1], 5)

    def test_limits_are_not_relaxed_and_boundaries_are_inclusive(self):
        self.assertIsNone(self.select([self.snap(31), self.snap(1)])[1])
        self.assertEqual(self.select([self.snap(30)])[0], 'ok')
        self.assertEqual(self.select([self.snap(7)])[0], 'ok')
        self.assertIsNone(self.select([self.snap(6.999)])[1])

    def test_equal_distance_uses_newest_measurement_and_stable_hash_tie(self):
        a, b = self.snap(20), self.snap(19)
        for items in ([a,b], [b,a]):
            self.assertEqual(self.select(items)[2]['inputs']['sources']['depth']['age_s'], 19*60)
        a, b = self.snap(20, ask_btc_25=5), self.snap(20, ask_btc_25=7)
        self.assertEqual(self.select([a,b]), self.select([b,a]))

    def test_missing_or_no_eligible_book_retains_rejection_trace(self):
        state, amount, row = self.select([self.snap(31)])
        self.assertIn('stale', state)
        self.assertIsNone(amount)
        self.assertIsNone(row['inputs']['depth_selection_v2']['selected'])
        self.assertIn('source-missing', self.select([])[0])

    def test_correction_uses_unrounded_flow_and_does_not_mutate_v1_row(self):
        row = {'t':self.t, 'inputs': {'perp_window_end_utc':P.iso(self.end)},
               'features':{'flow_btc':.1235, 'depth_25bp_btc':999, 'flow_per_depth':999},
               'fstate':{'flow_btc':'ok'}, 'state':{}}
        class Store:
            def snaps(inner): return [self.snap(16)[2]]
            def bars(inner, _):
                return {t: {'tbv': .1234567, 'v':0} for t in range(self.start, self.end, K.MIN)}
        with patch.object(OLD, 'state_panel', return_value=[copy.deepcopy(row)]):
            out = M.state_panel(Store(), self.t, self.t+1)[0]
        self.assertEqual(out['features']['flow_per_depth'], round(15*2*.1234567/5,5))
        self.assertEqual(row['features']['flow_per_depth'],999)
        self.assertEqual(out['fstate']['flow_per_depth'],'ok')

    def test_bad_flow_is_never_repaired(self):
        row = {'fstate': {'flow_btc':'window-incomplete'}, 'features':{}, 'inputs':{}}
        with patch.object(OLD,'state_panel',return_value=[row]), patch.object(P,'_snap_items',return_value=[]), \
             patch.object(M,'depth') as depth:
            M.state_panel(type('Store',(),{'bars':lambda *_:{}})(),0,1)
            depth.assert_not_called()


class Publication(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.slot=100*K.DAY
        K.register(self.base,self.slot-K.HOUR)

    def remote(self, base, paths):
        ident=K.identity()
        return 'verified-main', {str(p): ((K.ROOT if str(p) in ident else self.base)/p).read_bytes()
                                if ((K.ROOT if str(p) in ident else self.base)/p).exists() else None for p in paths}

    def activate(self):
        K.confirm(self.base,clock=lambda:self.slot-K.MIN,fetch=self.remote)

    def forecast(self):
        fit=K.Journal(self.base,'fits').add('state-fit',{'cutoff':self.slot,'state':'ready'})
        f=K.Journal(self.base,'forecasts').add(f'state-{self.slot}',
            {'study':'state','slot':self.slot,'state':'ready','prepared_ms':self.slot+K.MIN,
             'deadline_ms':self.slot+25*K.MIN,'fit':{'id':fit['id'],'sha256':fit['sha256']},
             'entry':self.slot+30*K.MIN,'end_ms':self.slot+270*K.MIN,
             'probabilities':{'full':.7,'baseline':.5,'flow':.6,'positioning':.6},'row':{'event':False}})
        return f

    def test_independent_identity_directory_and_clock(self):
        self.assertFalse((self.base/V1.STREAM).exists())
        self.assertIsNone(K.activation(self.base))
        self.activate()
        self.assertEqual(K.activation(self.base)['first_slot'],self.slot)
        self.assertFalse(any(p.startswith('research_tools/state_v2') for p in V1.identity()))
        self.assertTrue(set(V1.identity()) < set(K.identity()))
        production=V1.Journal(V1.ROOT,'registration').get('v1')
        self.assertEqual(V1.identity(),production['data']['identity'])

    def test_unpublished_code_or_fit_cannot_confirm(self):
        self.activate();self.forecast()
        for name in ['research_tools/state_v2/models.py', str(K.STREAM/'fits.jsonl')]:
            def missing(base,paths):
                commit,files=self.remote(base,paths);files[name]=b'';return commit,files
            with self.assertRaises(ValueError): K.confirm(self.base,clock=lambda:self.slot+2*K.MIN,fetch=missing)
        self.assertFalse(K.Journal(self.base,'confirmations').rows)

    def test_late_publication_never_scores_and_no_v1_writes(self):
        self.activate();self.forecast()
        K.confirm(self.base,clock=lambda:self.slot+25*K.MIN,fetch=self.remote)
        self.assertFalse(K.verified(self.base)[0][1]['data']['eligible'])
        with patch.object(S,'Store') as store, patch.object(M,'price_outcome') as outcome:
            store.return_value.bars.return_value={};S.score(self.base,self.slot+K.DAY)
            outcome.assert_not_called()
        self.assertFalse((self.base/V1.STREAM).exists())

    def test_score_idempotent_and_report_keeps_missing_grid_positions(self):
        self.activate();f=self.forecast()
        K.confirm(self.base,clock=lambda:self.slot+2*K.MIN,fetch=self.remote)
        with patch.object(S,'Store') as store, patch.object(M,'price_outcome',return_value={'y':1}):
            store.return_value.bars.return_value={}
            S.score(self.base,self.slot+5*K.HOUR);S.score(self.base,self.slot+6*K.HOUR)
        self.assertEqual(len(K.Journal(self.base,'scores').rows),1)
        report=S.build(self.base,self.slot+6*K.HOUR)
        self.assertEqual((report['scheduled'], report['scored']),(7,1))
        self.assertIsNone(report['primary']['ci90'])
        self.assertAlmostEqual(report['primary']['mean_difference'],.09-.25)
        self.assertEqual(len(report['opportunities']),7)
        S.write(self.base,self.slot+6*K.HOUR)
        self.assertTrue((self.base/'reports/market_state_v2.md').exists())

    def test_forecast_binding_and_future_training_cutoff_refuse(self):
        self.activate();f=self.forecast()
        K.Journal(self.base,'confirmations').add(f['id'],{'forecast_sha':'wrong','confirmed_ms':self.slot+2*K.MIN,'eligible':True})
        with self.assertRaisesRegex(ValueError,'changed after publication'): K.verified(self.base)

    def test_prepare_records_missed_slots_without_backfilling_predictions(self):
        self.activate()
        fit={'id':'f','sha256':'hash','data':{'state':'ready','models':{}}}
        with patch.object(M,'daily_fit',return_value=fit), patch.object(S,'Store'), \
             patch.object(M,'state_panel') as panel:
            S.prepare(self.base,clock=lambda:self.slot+26*K.MIN)
            panel.assert_not_called()
        row=K.Journal(self.base,'forecasts').rows[0]['data']
        self.assertEqual(row['state'],'missed')
        self.assertNotIn('probabilities',row)
        self.assertFalse((self.base/V1.STREAM).exists())

    def test_future_training_cutoff_cannot_enter_forecast(self):
        self.activate()
        fit=K.Journal(self.base,'fits').add('future',{'cutoff':self.slot+K.DAY})
        K.Journal(self.base,'forecasts').add('state-'+str(self.slot),{'study':'state','slot':self.slot,
            'fit':{'id':fit['id'],'sha256':fit['sha256']}})
        with self.assertRaisesRegex(ValueError,'Training cutoff after forecast'):K.verified(self.base)

    def test_identity_drift_refuses(self):
        with patch.object(K,'identity',return_value={}):
            with self.assertRaisesRegex(ValueError,'identity drift'): K.register(self.base,self.slot)

    def test_mutations_require_production_and_pause_covers_both_versions(self):
        with patch.object(U,'run_meta',return_value={'production':False}):
            with self.assertRaises(RuntimeError):main(['prepare'])
        for stream in (V1.STREAM,K.STREAM):
            p=self.base/stream/'paused.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}')
            self.assertTrue(paused(self.base));p.unlink()

    def test_daily_fit_is_immutable_and_training_uses_corrected_panel(self):
        with patch.object(M,'state_panel',return_value=[]) as panel, patch.object(M,'Store') as store:
            store.return_value.bars.return_value={}
            fit=M.daily_fit(self.base,self.slot)
            self.assertEqual(fit['data']['state'],'warmup')
            M.daily_fit(self.base,self.slot+K.HOUR)
            self.assertEqual(panel.call_count,1)


if __name__ == '__main__':unittest.main()
