"""Adversarial prospective-clock, paired-population, and accounting regressions."""
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from desk import stream_util as U, paper_ps1 as P
from research_tools.market_studies import core as K, models as M, collectors as C, experiments as X, report as R


class MarketTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.slot = 100 * K.DAY
        self.reg = K.register(self.base, self.slot - K.HOUR)

    def activate(self):
        K.Journal(self.base, 'activation').add('v1', {'registration_sha': self.reg['sha256'], 'confirmed_ms': self.slot-K.HOUR,
                                                   'first_slot': self.slot, 'commit': 'test-main'})

    def forecast(self, kind='turnover', extra=None, time=None):
        d = {'study': kind, 'slot': self.slot, 'prepared_ms': self.slot+K.MIN,
             'deadline_ms': self.slot+90*K.MIN, 'state': 'ready', 'weights': {'B2': .5, 'VOL': .4}}
        d.update(extra or {})
        r = K.Journal(self.base, 'forecasts').add(kind+'-'+str(self.slot), d)
        t = self.slot+2*K.MIN if time is None else time
        c = K.Journal(self.base, 'confirmations').add(r['id'], {'forecast_sha': r['sha256'], 'confirmed_ms': t,
                                                             'eligible': d['prepared_ms'] <= t < d['deadline_ms'], 'commit': 'main'})
        return r,c

    def quote(self, t=None, price=100):
        t = self.slot+3*K.MIN if t is None else t
        return {'source':'https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=20',
                't_sent_ms':t,'t_received_ms':t+100,'last_update_id':1, 'retrieval':P.LIVE,
                'bids':[[str(price-.01-i*.01),'10000'] for i in range(5)],
                'asks':[[str(price+.01+i*.01),'10000'] for i in range(5)]}

    def response(self, obj, sent=None, received=None):
        raw=json.dumps(obj)
        return {'url':'fixture','sent_ms':self.slot+1 if sent is None else sent,
                'received_ms':self.slot+100 if received is None else received, 'state':'ok','raw':raw,
                'raw_sha':hashlib.sha256(raw.encode()).hexdigest()}

    def bars_response(self, lag=0, buy=75):
        bars=[[t,'100','101','99','100','100',t+K.MIN-1,'0',10,str(buy)]
              for t in range(self.slot-5*K.MIN,self.slot,K.MIN)]
        return self.response(bars,received=self.slot+100+lag)

    def remote(self, base, paths):
        files={}
        for path in paths:
            local=(K.ROOT if str(path) in K.identity() else self.base)/path
            files[str(path)]=local.read_bytes() if local.exists() else None
        return 'verified-main',files

    def test_registration_is_not_activation_or_launch(self):
        self.assertIsNone(K.activation(self.base))
        out=R.build(self.base,self.slot)
        self.assertEqual(out['studies']['turnover']['results']['status'],'not launched')
        self.assertFalse(K.Journal(self.base,'launches').rows)

    def test_confirm_uses_observation_clock_and_next_hour(self):
        K.confirm(self.base,clock=lambda:self.slot+1234,fetch=self.remote)
        self.assertEqual(K.activation(self.base)['first_slot'],self.slot+K.HOUR)
        self.assertEqual(K.activation(self.base)['confirmed_ms'],self.slot+1234)

    def test_registration_missing_from_main_refuses(self):
        def missing(base,paths):
            commit,files=self.remote(base,paths);files[str(K.STREAM/'registration.jsonl')]=b'';return commit,files
        with self.assertRaisesRegex(ValueError,'Registration not on main'):
            K.confirm(self.base,clock=lambda:self.slot,fetch=missing)
        self.assertIsNone(K.activation(self.base))

    def test_implementation_must_be_on_main(self):
        def changed(base,paths):
            commit,files=self.remote(base,paths);files[next(iter(K.identity()))]=b'altered';return commit,files
        with self.assertRaisesRegex(ValueError,'Implementation not on main'):
            K.confirm(self.base,clock=lambda:self.slot,fetch=changed)

    def test_protocol_drift_refuses(self):
        with patch.object(K,'identity',return_value={'changed':'hash'}):
            with self.assertRaisesRegex(ValueError,'identity drift'):
                K.register(self.base,self.slot)

    def test_journal_atomic_idempotent_and_immutable(self):
        j=K.Journal(self.base,'test');r=j.add('a',{'value':1});j.add('a',{'value':1})
        self.assertEqual(len(j.rows),1)
        with self.assertRaisesRegex(ValueError,'rewrite'):
            j.add('a',{'value':2})
        self.assertEqual(K.Journal(self.base,'test').get('a'),r)

    def test_journal_corruption_refuses(self):
        j=K.Journal(self.base,'test');j.add('a',{'value':1})
        j.path.write_text(j.path.read_text().replace('"value":1','"value":2'))
        with self.assertRaisesRegex(ValueError,'Corrupt'):
            K.Journal(self.base,'test')

    def test_late_confirmation_excludes_forecast(self):
        self.activate();r,c=self.forecast(time=self.slot+91*K.MIN)
        self.assertFalse(c['data']['eligible'])
        X.execute(self.base,clock=lambda:self.slot+92*K.MIN,fetch_quote=lambda url:self.fail('late quote requested'))
        self.assertFalse(K.Journal(self.base,'executions').rows)

    def test_changed_confirmation_binding_refuses(self):
        self.activate();r,c=self.forecast()
        p=K.Journal(self.base,'confirmations').path;p.unlink()
        K.Journal(self.base,'confirmations').add(r['id'],dict(c['data'],forecast_sha='wrong'))
        with self.assertRaisesRegex(ValueError,'changed after publication'):
            K.verified(self.base)

    def test_training_artifact_must_be_on_main(self):
        self.activate()
        f=K.Journal(self.base,'fits').add('state-fit',{'cutoff':self.slot})
        d={'study':'state','slot':self.slot,'state':'ready','prepared_ms':self.slot,'deadline_ms':self.slot+K.HOUR,
           'fit':{'id':f['id'],'sha256':f['sha256']}}
        K.Journal(self.base,'forecasts').add('state-test',d)
        def nofit(base,paths):
            c,fs=self.remote(base,paths);fs[str(K.STREAM/'fits.jsonl')]=b'';return c,fs
        with self.assertRaisesRegex(ValueError,'Training artifact not on main'):
            K.confirm(self.base,clock=lambda:self.slot+K.MIN,fetch=nofit)

    def test_eight_arms_once_and_independent_bands(self):
        self.activate();self.forecast()
        X.execute(self.base,clock=lambda:self.slot+3*K.MIN,fetch_quote=lambda url:self.quote())
        X.execute(self.base,clock=lambda:self.slot+4*K.MIN,fetch_quote=lambda url:self.fail('duplicate quote'))
        prior,es=X.turnover_chain(self.base)
        self.assertEqual(len(es),1);self.assertEqual(len(prior),8)
        d={'slot':self.slot+4*K.HOUR,'weights':{'B2':.575,'VOL':.475}}
        nextrows=X.simulate(d,self.quote(self.slot+4*K.HOUR+3*K.MIN),prior)
        self.assertGreater(nextrows['stressed/B2_05']['notional'],0)
        self.assertEqual(nextrows['stressed/B2_10']['notional'],0)

    def test_quote_before_confirmation_cannot_execute(self):
        self.activate();self.forecast()
        X.execute(self.base,clock=lambda:self.slot+3*K.MIN,fetch_quote=lambda url:self.quote(self.slot+K.MIN))
        self.assertFalse(K.Journal(self.base,'executions').rows)
        self.assertEqual(len(K.Journal(self.base,'quote_attempts').rows),1)

    def test_tampered_account_row_refuses_reproduction(self):
        self.activate();self.forecast();X.execute(self.base,clock=lambda:self.slot+3*K.MIN,fetch_quote=lambda url:self.quote())
        j=K.Journal(self.base,'executions');r=j.rows[0];j.path.unlink()
        r['data']['arms']['ordinary/B2_05']['cash_after']+=1
        K.Journal(self.base,'executions').add(r['id'],r['data'])
        with self.assertRaisesRegex(ValueError,'do not reproduce'):
            X.turnover_chain(self.base)

    def test_open_interval_cost_excluded_and_gap_duration(self):
        d={'slot':self.slot,'weights':{'B2':.5,'VOL':.4}}
        a=X.simulate(d,self.quote(),{})
        b=X.simulate(dict(d,slot=self.slot+8*K.HOUR),self.quote(self.slot+8*K.HOUR+3*K.MIN,105),a)
        out=R.turnover_summary([{'data':{'arms':a}},{'data':{'arms':b}}],3)
        arm=out['arms']['ordinary/B2_05']
        self.assertEqual(arm['elapsed_hours'],8)
        self.assertEqual(arm['cost_closed_usdt'],a['ordinary/B2_05']['cost_vs_mid'])
        self.assertAlmostEqual(out['coverage'],2/3)

    def test_interval_score_penalizes_width_and_misses(self):
        self.assertEqual(M.interval_score(1,3,2),2)
        self.assertEqual(M.interval_score(0,4,2),4)
        self.assertEqual(M.interval_score(1,3,4),12)

    def test_calibration_keeps_point_and_quantile_order(self):
        e={'q10':1,'q50':2,'q90':3,'point':2.2}
        out=M.calibrated(e,{'state':'ready','lower_offset':5,'upper_offset':-5})
        self.assertEqual(out,{'q10':2,'q50':2,'q90':2,'point':2.2})

    def test_range_fit_excludes_late_known_and_unmatured(self):
        cutoff=100*K.DAY
        scores={'range-rc1d-24h-ok':{'horizon':cutoff-1,'scored':cutoff-1},
                'range-rc1d-24h-late':{'horizon':cutoff-1,'scored':cutoff},
                'range-rc1d-24h-future':{'horizon':cutoff,'scored':cutoff-1}}
        outcome={'eligible':True,'score_sha256':'s','realized':2,'scored_ms':cutoff-1}
        doc={'events':[{'name':'B2','q10':1,'q90':3}]}
        with patch.object(M.B,'_rc1d_scores',return_value=scores),patch.object(M.B,'rc1d_outcome',return_value=outcome) as f,patch.object(M.U,'rc1d_record',return_value=(doc,{'sha256':'f'},None)):
            fit=M.range_fit(self.base,cutoff)
        self.assertEqual(f.call_count,1);self.assertEqual(fit['state'],'warmup');self.assertEqual(len(fit['members']),1)

    def test_complete_outcome_path_and_availability_required(self):
        bars={self.slot+i*K.MIN:{'o':100.,'h':102.,'l':99.,'c':101.,'avail':self.slot+(i+1)*K.MIN} for i in range(3)}
        self.assertIsNotNone(M.price_outcome(bars,self.slot,3,self.slot+4*K.MIN))
        self.assertIsNone(M.price_outcome(bars,self.slot,3,self.slot+3*K.MIN))
        del bars[self.slot+K.MIN]
        self.assertIsNone(M.price_outcome(bars,self.slot,3,self.slot+4*K.MIN))

    def test_logistic_fit_is_finite_deterministic_with_constant_feature(self):
        rows=[{'features':{'x':i%2,'constant':1},'label':{'y':i%2}} for i in range(30)]
        fit=M.logistic_fit(rows,['x','constant'])
        self.assertEqual(fit,M.logistic_fit(rows,['x','constant']))
        self.assertGreater(M.predict(fit,{'x':1,'constant':1}),M.predict(fit,{'x':0,'constant':1}))
        self.assertTrue(0<M.predict(fit,{'x':1e12,'constant':1})<1)

    def test_pair_preserves_two_clocks_and_three_arms(self):
        cap=C.pair_capture(self.slot,get=lambda url:self.bars_response(1500 if '/api/v3/' in url else 0))
        d=X.paired_forecast(cap)
        self.assertEqual(cap['receipt_gap_ms'],1500);self.assertEqual(d['state'],'ready')
        self.assertEqual(len(d['probabilities']),3)
        self.assertEqual(d['probabilities']['perp_original_clock'],d['probabilities']['perp_synchronized_clock'])
        self.assertGreaterEqual(d['entries']['perp_synchronized_clock'],d['entries']['perp_original_clock'])

    def test_join_timeout_is_not_neutral_signal(self):
        cap=C.pair_capture(self.slot,get=lambda url:self.bars_response(6000 if '/api/v3/' in url else 0))
        self.assertEqual(cap['state'],'join-timeout')
        d=X.paired_forecast(cap);self.assertEqual(d['state'],'abstained');self.assertNotIn('probabilities',d)

    def test_pair_rejects_missing_or_misaligned_bar(self):
        raw=self.bars_response();obj=json.loads(raw['raw']);obj[1][0]=obj[0][0]
        cap=C.pair_capture(self.slot,get=lambda url:self.response(obj))
        self.assertEqual(cap['state'],'source-unavailable')

    def test_neutral_flow_is_valid_and_included(self):
        cap=C.pair_capture(self.slot,get=lambda url:self.bars_response(buy=50))
        d=X.paired_forecast(cap);self.assertEqual(d['state'],'ready')
        self.assertEqual(set(d['probabilities'].values()),{.5})

    def test_raw_response_tamper_rejected(self):
        r=self.response({'value':1});r['raw']='{}'
        with self.assertRaisesRegex(ValueError,'changed'):
            C.payload(r)

    def test_empty_liquidation_page_is_unknown_not_zero(self):
        r=C.liquidation_capture(self.slot,0,get=lambda url:self.response({'code':'0','data':[]}))
        self.assertEqual(r['state'],'coverage-unknown');self.assertIsNone(r['total_contracts']);self.assertFalse(r['eligible'])

    def test_liquidation_coverage_and_revision_signal(self):
        rows=[{'ts':str(self.slot-10*K.MIN),'sz':'1500','bkPx':'100','posSide':'long','side':'sell'},
              {'ts':str(self.slot-2*K.HOUR),'sz':'1','bkPx':'100','posSide':'short','side':'buy'}]
        r=C.liquidation_capture(self.slot,6,get=lambda url:self.response({'code':'0','data':[{'details':rows}]}))
        self.assertEqual(r['total_contracts'],1500);self.assertEqual(r['signal'],1);self.assertTrue(r['eligible'])

    def test_liquidation_page_cap_preserves_unknown(self):
        n=[0]
        def get(url):
            n[0]+=1
            d={'ts':str(self.slot-n[0]*K.MIN),'sz':'1','bkPx':'100','posSide':'long','side':'sell'}
            return self.response({'code':'0','data':[{'details':[d]}]})
        r=C.liquidation_capture(self.slot,18,get)
        self.assertEqual(n[0],20);self.assertIsNone(r['total_contracts']);self.assertEqual(r['reason'],'page-cap')

    def test_stress_unknown_rating_and_staleness_not_zeros(self):
        def get(url):
            return self.response({'symbol':'BTCUSDT','adlRisk':'unknown','updateTime':self.slot}) if 'symbolAdl' in url else self.response({'symbols':['BTCUSDT'],'assets':[{'asset':'USDT','marginBalance':'2','updateTime':self.slot}]})
        r=C.stress_capture(self.slot,get);self.assertEqual(r['state'],'unavailable');self.assertIsNone(r['risk'])

    def test_stress_shared_pool_is_preserved(self):
        def get(url):
            return self.response({'symbol':'BTCUSDT','adlRisk':'LOW','updateTime':self.slot}) if 'symbolAdl' in url else self.response({'symbols':['BTCUSDT','ETHUSDT'],'assets':[{'asset':'USDT','marginBalance':'2','updateTime':self.slot}]})
        r=C.stress_capture(self.slot,get);self.assertEqual(r['state'],'ok');self.assertEqual(len(r['pool_symbols']),2)

    def test_no_confidence_interval_from_few_observations(self):
        r=R.paired_summary([.1,None,-.2],42)
        self.assertIsNone(r['ci90']);self.assertEqual(r['paired'],2)

    def test_production_guard_rejects_local_and_pr(self):
        with patch.dict(os.environ,{'GITHUB_ACTIONS':'true','GITHUB_REPOSITORY':'mannoj93-spec/jbm-desk-data','GITHUB_REF':'refs/pull/1/merge'}):
            with self.assertRaisesRegex(RuntimeError,'main-branch'):
                K.production()

    def test_missing_current_range_source_is_retried_until_deadline(self):
        self.activate()
        fit={'id':'fit','sha256':'fake','data':{'state':'warmup'}}
        fakepanel={'t':self.slot,'features':{},'fstate':{},'event':False}
        with patch.object(M,'daily_fit',return_value=fit),patch.object(X,'source',return_value=None),patch.object(M,'state_panel',return_value=[fakepanel]),patch.object(C,'pair_capture',return_value={'state':'source-unavailable'}):
            X.prepare(self.base,clock=lambda:self.slot+20*K.MIN)
        self.assertIsNone(K.Journal(self.base,'forecasts').get(f'turnover-{self.slot}'))
        self.assertIsNone(K.Journal(self.base,'forecasts').get(f'range-{self.slot}'))
        self.assertEqual(len(K.Journal(self.base,'attempts').rows),2)
        with patch.object(M,'daily_fit',return_value=fit),patch.object(M,'state_panel',return_value=[fakepanel]),patch.object(C,'pair_capture',return_value={'state':'source-unavailable'}):
            X.prepare(self.base,clock=lambda:self.slot+100*K.MIN)
        self.assertEqual(K.Journal(self.base,'forecasts').get(f'turnover-{self.slot}')['data']['state'],'missed')

    def test_missed_history_never_reconstructed_as_forecasts(self):
        self.activate()
        fit={'id':'fit','sha256':'fake','data':{'state':'warmup'}}
        row={'features':{},'fstate':{}}
        with patch.object(M,'daily_fit',return_value=fit),patch.object(X,'source',return_value=None) as src,patch.object(M,'state_panel',return_value=[row]),patch.object(C,'pair_capture',return_value={'state':'source-unavailable'}):
            X.prepare(self.base,clock=lambda:self.slot+4*K.HOUR+26*K.MIN)
        r=K.Journal(self.base,'forecasts').get(f'turnover-{self.slot}')
        self.assertEqual(r['data']['state'],'missed')
        self.assertTrue(all(call.args[1] > self.slot for call in src.call_args_list))

    def test_outcome_scores_are_paired_and_reproducible(self):
        self.activate()
        r,c=self.forecast('state',extra={'entry':self.slot+30*K.MIN,'probabilities':{'baseline':.5,'full':.8},'row':{'event':False}})
        bars={self.slot+(30+i)*K.MIN:{'o':100.,'h':102.,'l':99.,'c':101.,'avail':self.slot+(31+i)*K.MIN} for i in range(240)}
        out=X.score_record(self.base,r,self.slot+5*K.HOUR,bars,{})
        self.assertAlmostEqual(out['primary_difference'],.04-.25)
        self.assertEqual(out['outcome']['y'],1)
        del bars[self.slot+60*K.MIN]
        self.assertIsNone(X.score_record(self.base,r,self.slot+5*K.HOUR,bars,{}))

    def test_paired_scoring_waits_for_all_three_arms(self):
        self.activate()
        cap=C.pair_capture(self.slot,get=lambda url:self.bars_response())
        d=X.paired_forecast(cap)
        d['entries']['perp_original_clock']-=K.MIN
        r,c=self.forecast('paired',extra=d)
        entry=d['entries']['perp_synchronized_clock']
        bars={entry+i*K.MIN:{'o':100.,'h':102.,'l':99.,'c':101.,'avail':entry+(i+1)*K.MIN} for i in range(60)}
        self.assertIsNone(X.score_record(self.base,r,entry+2*K.HOUR,bars,{}))
        bars[entry-K.MIN]={'o':100.,'h':102.,'l':99.,'c':101.,'avail':entry}
        out=X.score_record(self.base,r,entry+2*K.HOUR,bars,{})
        self.assertEqual(set(out['horizons']),{'15','60'})
        self.assertEqual(len(out['horizons']['60']),3)

    def test_options_size_missing_is_explicit_and_filters_unchanged(self):
        before=C.O.filters_sha256()
        now=U.ms(U.parse('2026-10-24T00:00:00Z'))
        cap={'observed_at':now,'t_event_min':now-1000,'fields':['instrument','open_interest_btc','mark_iv','bid_price_btc','ask_price_btc','source_ts_offset_ms'],
             'rows':[['BTC-30OCT26-80000-P',2,50,.01,.02,0]],'underlying_v2':{'30OCT26':['BTC',80000,0]}}
        q=C.options_quality(cap)
        self.assertEqual(q['legs'][0]['size_state'],'not-in-source')
        self.assertIn('low-oi',q['legs'][0]['reasons'])
        self.assertIn('wide',q['legs'][0]['reasons'])
        self.assertEqual(before,C.O.filters_sha256())

    def test_insurance_error_not_reported_as_zero_balance(self):
        def get(url):
            return self.response({'symbol':'BTCUSDT','adlRisk':'LOW','updateTime':self.slot}) if 'symbolAdl' in url else self.response({'symbols':['BTCUSDT'],'assets':[{'asset':'USDT','marginBalance':'NaN','updateTime':self.slot}]})
        r=C.stress_capture(self.slot,get)
        self.assertEqual(r['state'],'unavailable');self.assertIsNone(r['assets'])

    def test_bounded_transport_timeout_is_explicit_missing(self):
        import subprocess
        from research_tools.market_studies import network
        with patch.object(network.subprocess,'run',side_effect=subprocess.TimeoutExpired('fetch',12)):
            r=network.fetch('https://example.invalid')
        self.assertEqual(r['state'],'request-error');self.assertIsNone(r['raw'])

    def test_only_new_writer_paths_authorized(self):
        writers=json.loads((K.ROOT/'scripts/writers.json').read_text())['writers']['market-studies']
        self.assertEqual(writers['allow'],['streams/market-studies/','reports/market_studies.json','reports/market_studies.md'])


if __name__=='__main__':
    unittest.main()
