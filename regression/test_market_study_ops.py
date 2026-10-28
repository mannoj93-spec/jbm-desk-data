"""Operational changes must recover missing work without rewriting prospective evidence."""
import datetime as dt
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import recovery as R
import market_study_ops as O
from research_tools.market_studies import core as K
from regression.test_recovery import gh, t, Opener


class RecoveryStudies(unittest.TestCase):
    def test_native_and_recovery_share_slot_and_main_only_dedup(self):
        now = t('2026-10-25T12:12:00Z')
        self.assertEqual(R.study_plan(now, {})[0][:2], ('studies', '2026-10-25T12:00:00Z'))
        for event in ['schedule', 'workflow_run', 'workflow_dispatch']:
            self.assertEqual(R.study_plan(now, {'studies':[gh('2026-10-25T12:01:00Z', event=event)]}), [])
        self.assertTrue(R.study_plan(now, {'studies':[gh('2026-10-25T12:01:00Z', branch='pr')]}))

    def test_pre_source_success_does_not_suppress_range_followup(self):
        now = t('2026-10-25T12:19:00Z'); anchor = t('2026-10-25T12:17:00Z')
        self.assertTrue(R.study_plan(now, {'studies':[gh('2026-10-25T12:15:00Z')]}, after=anchor))
        self.assertEqual(R.study_plan(now, {'studies':[gh('2026-10-25T12:18:00Z', status='queued')]}, after=anchor), [])

    def test_failed_or_stalled_retries_are_bounded(self):
        now = t('2026-10-25T12:12:00Z')
        title = R.title('Market studies', '2026-10-25T12:00:00Z')
        dead = gh('2026-10-25T12:01:00Z', conclusion='failure', title=title)
        stalled = gh('2026-10-25T12:02:00Z', status='queued', title=title)
        self.assertTrue(R.study_plan(now, {'studies':[dead]}))
        self.assertTrue(R.study_plan(now, {'studies':[stalled]}))
        self.assertEqual(R.study_plan(now, {'studies':[dead,stalled]}), [])
        self.assertTrue(R.study_plan(t('2026-10-25T12:27:00Z'), {'studies':[dead,stalled]}))

    def test_dispatch_has_recovery_lineage_and_chain_lists_only_studies(self):
        o = Opener()
        R.list_runs('o/r','tok',opener=o,keys={'studies'})
        self.assertEqual(len(o.calls),1)
        self.assertIn('market-studies.yml/runs',o.calls[0][1])
        r=R.dispatch('o/r','tok',[('studies','slot','why')],'42:external:43',opener=o)
        self.assertTrue(r[0]['ok'])
        self.assertEqual(json.loads(o.calls[-1][2])['inputs']['origin'],'42:external:43')

    def test_recovered_range_fast_path_uses_source_deadline(self):
        now=dt.datetime.now(dt.timezone.utc); slot=R.decision(now)
        src={'available_ms':int((now-dt.timedelta(minutes=1)).timestamp()*1000),
             'document':{'start_utc':R.iso(now+dt.timedelta(minutes=7))}}
        env={'GITHUB_TOKEN':'test','GITHUB_REPOSITORY':'o/r'}
        with patch.dict('os.environ',env), patch('research_tools.market_studies.experiments.source',return_value=src), \
             patch.object(R,'list_runs',return_value={'studies':[]}), patch.object(R,'dispatch',return_value=[{'ok':True}]) as dispatch:
            self.assertEqual(R.main(['recovery.py','study-chain','--slot',R.iso(slot)]),0)
            self.assertEqual(dispatch.call_args.args[2][0][0],'studies')
            src['document']['start_utc']=R.iso(now-dt.timedelta(minutes=1))
            dispatch.reset_mock()
            self.assertEqual(R.main(['recovery.py','study-chain','--slot',R.iso(slot)]),0)
            dispatch.assert_not_called()


class Diagnostics(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.slot=100*K.DAY
        reg=K.register(self.base,self.slot-K.HOUR)
        K.Journal(self.base,'activation').add('v1',{'registration_sha':reg['sha256'],'confirmed_ms':self.slot-K.HOUR,
                                                  'first_slot':self.slot,'commit':'main'})

    def forecast(self,kind='state',slot=None,confirmed=True,state='ready',late=False):
        slot=self.slot if slot is None else slot
        d={'study':kind,'slot':slot,'prepared_ms':slot+K.MIN,'deadline_ms':slot+25*K.MIN,
           'state':state,'end_ms':slot+270*K.MIN}
        f=K.Journal(self.base,'forecasts').add(f'{kind}-{slot}',d)
        if confirmed:
            stamp=slot+(26 if late else 2)*K.MIN
            K.Journal(self.base,'confirmations').add(f['id'],{'forecast_sha':f['sha256'],'confirmed_ms':stamp,
                                                      'eligible':state=='ready' and not late,'commit':'main'})
        return f

    def test_reader_does_not_create_a_registration(self):
        with tempfile.TemporaryDirectory() as tmp:
            x=O.build(tmp,self.slot)
            self.assertTrue(x['alerts']);self.assertEqual(list(Path(tmp).iterdir()),[])

    def test_open_deadlines_do_not_count_as_misses(self):
        x=O.build(self.base,self.slot+20*K.MIN)
        self.assertEqual(x['studies']['state']['due'],0)
        self.assertIsNone(x['studies']['state']['coverage'])
        self.assertEqual(x['studies']['paired']['due'],0)

    def test_pending_outcome_is_success_not_a_miss_or_zero_score(self):
        self.forecast()
        x=O.build(self.base,self.slot+40*K.MIN)['studies']['state']
        self.assertEqual((x['successful'],x['due'],x['pending_outcomes'],x['overdue_scores']),(1,1,1,0))
        self.assertEqual(x['coverage'],1)

    def test_late_and_unconfirmed_have_distinct_states(self):
        self.forecast(late=True)
        self.forecast(slot=self.slot+K.HOUR,confirmed=False)
        x=O.build(self.base,self.slot+2*K.HOUR)['studies']['state']
        self.assertEqual(x['states'],{'late-publication':1,'unconfirmed':1})
        self.assertEqual(x['consecutive_misses'],2)

    def test_absent_pilots_never_count_as_successful_capture(self):
        K.Journal(self.base,'stress').add(str(self.slot),{'slot':self.slot,'state':'missed'})
        x=O.build(self.base,self.slot+2*K.HOUR)
        s=x['pilots']['stress'];self.assertEqual(s['successful'],0);self.assertGreater(s['due'],0)
        self.assertIn('missed',s['states']);self.assertIn('no-run',s['states'])

    def test_pausing_suppresses_collection_alerts_but_not_integrity(self):
        (self.base/K.STREAM/'paused.json').write_text('{}')
        x=O.build(self.base,self.slot+2*K.HOUR)
        self.assertEqual(x['alerts'],[])
        p=self.base/K.STREAM/'activation.jsonl';p.write_text(p.read_text().replace('main','altered'))
        x=O.safe_build(self.base,self.slot+2*K.HOUR)
        self.assertEqual(x['integrity'],'failed');self.assertTrue(x['alerts'])

    def test_binding_corruption_withholds_diagnostics(self):
        f=self.forecast()
        K.Journal(self.base,'scores').add(f['id'],{'forecast_sha':'wrong','confirmation_sha':'wrong'})
        x=O.safe_build(self.base,self.slot+K.HOUR)
        self.assertEqual(x['integrity'],'failed');self.assertEqual(x['studies'],{})

    def test_range_waiting_for_source_is_not_integrity_failure(self):
        x=O.build(self.base,self.slot+K.HOUR)
        self.assertIsNone(x['studies']['range']['opportunities'][0]['source_confirmed_ms'])

    def test_shared_entry_sensitivity_preserves_primary_population(self):
        def pair(entry,value):
            return ({'study':'paired','entries':{'combined_synchronized_clock':entry,'perp_original_clock':entry,
                                                'perp_synchronized_clock':entry}}, {'primary_difference':value})
        x=O.paired_diagnostics([pair(0,1),pair(0,3),pair(K.HOUR,8)])
        self.assertEqual(x['scored_forecasts'],3);self.assertEqual(x['unique_entries'],2)
        self.assertEqual(x['entry_grouped_mean_difference'],5)
        self.assertEqual(x['largest_disjoint_60m_subset'],2);self.assertEqual(x['equal_entry_clock_share'],1)

    def test_live_identity_remains_exactly_registered(self):
        root=Path(__file__).resolve().parents[1]
        reg=K.Journal(root,'registration').get('v1')
        self.assertEqual(K.identity(),reg['data']['identity'])
        before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/K.STREAM).glob('*.jsonl')}
        # V2 scoring follows the v1 report in the workflow; that report's timestamp can predate a new score.
        x=O.safe_build(root,K.U.clock_ms())
        self.assertEqual(x['integrity'],'ok')
        self.assertEqual(before,{p:hashlib.sha256(p.read_bytes()).hexdigest() for p in before})



class AdditionalDiagnostics(unittest.TestCase):
    setUp = Diagnostics.setUp
    forecast = Diagnostics.forecast
    def test_scoring_backlog_survives_rolling_window(self):
        self.forecast()
        x=O.build(self.base,self.slot+2*K.DAY)
        self.assertEqual(x['studies']['state']['overdue_scores'],1)
        self.assertTrue(any('scores overdue' in a for a in x['alerts']))

    def test_successful_pilot_capture_is_separate_from_missing_records(self):
        K.Journal(self.base,'stress').add(str(self.slot),{'slot':self.slot,'state':'ok',
                  'raw':[{'received_ms':self.slot+K.MIN}]})
        K.Journal(self.base,'stress').add(str(self.slot+30*K.MIN),{'slot':self.slot+30*K.MIN,'state':'missed'})
        s=O.build(self.base,self.slot+70*K.MIN)['pilots']['stress']
        self.assertEqual((s['due'],s['successful'],s['coverage']),(2,1,.5))

    def test_option_artifact_tampering_is_detected(self):
        import gzip
        p=self.base/K.STREAM/'option_legs'/'capture.json.gz';p.parent.mkdir()
        p.write_bytes(gzip.compress(b'[]'))
        with self.assertRaisesRegex(ValueError,'hash mismatch'):
            O.options_diagnostics(self.base,[{'data':{'legs_file':str(p.relative_to(self.base)),'legs_sha':'wrong'}}])

class DeploymentDiagnostics(unittest.TestCase):
    setUp = Diagnostics.setUp
    forecast = Diagnostics.forecast

    def deployment(self, start):
        (self.base/'market_study_ops.json').write_text(json.dumps({'schema':'market-study-operations/1',
            'deployment':{'label':'Recovery', 'started_utc':O.U.iso_ms(start), 'commit':'a'*40}}))

    def test_new_success_clears_alarm_before_closure_without_erasing_misses(self):
        self.forecast('range',state='missed')
        self.forecast('range',slot=self.slot+4*K.HOUR,state='missed')
        self.forecast('range',slot=self.slot+8*K.HOUR)
        self.deployment(self.slot+K.HOUR)
        x=O.build(self.base,self.slot+8*K.HOUR+20*K.MIN)
        r=x['studies']['range']
        self.assertEqual((r['due'],r['successful'],r['consecutive_misses']),(2,0,2))
        self.assertEqual((r['pending_successful'],r['active_consecutive_misses']),(1,0))
        self.assertTrue(r['recovered_before_close'])
        self.assertFalse(any(a.startswith('range:') for a in x['alerts']))
        self.assertEqual(x['deployment']['studies']['range']['due'],1)
        later=O.build(self.base,self.slot+8*K.HOUR+31*K.MIN)['studies']['range']
        self.assertEqual((later['due'],later['successful'],later['pending_successful']),(3,1,0))

    def test_unconfirmed_or_late_success_cannot_clear_alarm(self):
        self.forecast('range',state='missed')
        self.forecast('range',slot=self.slot+4*K.HOUR,state='missed')
        self.forecast('range',slot=self.slot+8*K.HOUR,late=True)
        r=O.build(self.base,self.slot+8*K.HOUR+28*K.MIN)['studies']['range']
        self.assertEqual(r['active_consecutive_misses'],2)
        self.assertEqual(r['pending_successful'],0)

    def test_liquidation_streak_counts_capture_times_in_both_periods(self):
        closed=[{'slot':self.slot,'state':'missed','success_ms':None} for _ in range(4)]
        r=O.capture_coverage(closed,[],self.slot,grouped=True)
        self.assertEqual((r['due'],r['consecutive_misses'],r['active_consecutive_misses']),(4,1,1))
        pending=[{'slot':self.slot+K.HOUR,'state':'ok','success_ms':self.slot+K.HOUR}]
        r=O.capture_coverage(closed,pending,self.slot,grouped=True)
        self.assertEqual((r['due'],r['successful'],r['active_consecutive_misses']),(4,0,0))

    def test_deployment_outlives_rolling_window_and_respects_exact_boundary(self):
        self.deployment(self.slot+1)
        for i in range(3):
            self.forecast(slot=self.slot+i*K.HOUR)
        x=O.build(self.base,self.slot+26*K.HOUR)
        self.assertEqual(x['studies']['state']['successful'],1)
        self.assertEqual(x['deployment']['studies']['state']['successful'],2)
        self.assertEqual(x['deployment']['started_ms'],self.slot+1)

    def test_depth_uses_recorded_age_and_retains_reasons_and_missingness(self):
        rows=[({'data':{'study':'state','slot':self.slot,'state':'abstained','reasons':['stale depth'],
                      'row':{'inputs':{'sources':{'depth':{'age_s':1867,'state':'stale'}}}}}},None),
              ({'data':{'study':'state','slot':self.slot+K.HOUR,'state':'missed'}},None)]
        x=O.depth_diagnostics(rows,self.slot,self.slot+K.HOUR)
        self.assertEqual((x['forecasts'],x['abstained'],x['missing_depth_age']),(2,1,1))
        self.assertEqual(x['depth_age_minutes']['n'],1)
        self.assertAlmostEqual(x['depth_age_minutes']['median'],1867/60)
        self.assertEqual(x['abstention_reasons'],{'stale depth':1})

    def test_selected_options_use_recorded_expiries_strikes_and_separate_horizons(self):
        import gzip
        def leg(expiry, strike, side, spread):
            return {'instrument':f'BTC-{expiry}-{strike}-{side}', 'relative_spread':spread,
                    'quote_age_ms':4000, 'delta_distance':.02, 'size_state':'not-in-source','reasons':[]}
        legs=[leg(e,k,s,v) for e,k,v in [('A',100,.01),('B',200,.03),('C',300,.05)] for s in ['C','P']]
        legs.append({**leg('A',999,'C',.9),'reasons':['wide']})
        d={'expiries':{e:{'state':'ok','pair':{'call_K':k,'put_K':k}} for e,k in [('A',100),('B',200),('C',300)]},
           'rr25_7d':{'state':'ok','expiries':['A','B']},'rr25_30d':{'state':'ok','expiries':['B','C']}}
        raw=json.dumps(legs).encode();p=self.base/K.STREAM/'option_legs'/'test.json.gz';p.parent.mkdir()
        p.write_bytes(gzip.compress(raw));d.update(legs_file=str(p.relative_to(self.base)),legs_sha=hashlib.sha256(raw).hexdigest())
        x=O.options_diagnostics(self.base,[{'data':d}])
        self.assertEqual(x['legs'],7)
        selected=x['selected_by_horizon']
        self.assertEqual(selected['rr25_7d']['legs'],4)
        self.assertEqual(selected['rr25_7d']['relative_spread']['median'],.02)
        self.assertEqual(selected['rr25_30d']['relative_spread']['median'],.04)
        self.assertEqual(selected['rr25_7d']['size_states'],{'not-in-source':4})
        d['rr25_7d']['expiries']=['A','A']
        self.assertEqual(len(O.selected_options(d,legs,'rr25_7d')),2)
        with self.assertRaisesRegex(ValueError,'missing or ambiguous'):
            O.selected_options(d,legs+[legs[0]],'rr25_7d')
        with self.assertRaisesRegex(ValueError,'missing or ambiguous'):
            O.selected_options(d,legs[1:],'rr25_7d')
        d['rr25_7d']={'state':'unusable'}
        self.assertEqual(O.selected_options(d,legs,'rr25_7d'),[])

if __name__=='__main__':unittest.main()


class AbstentionCounts(unittest.TestCase):
    def test_closed_recorded_abstained_and_missing_have_explicit_denominators(self):
        rows = [{'slot':i, 'state':s, 'recorded':s!='no-run', 'forecast_state':s,
                 'eligible_forecast':s=='ok', 'success_ms':i if s=='ok' else None}
                for i,s in enumerate(['ok','abstained','no-run','warmup','abstained','ok','missed'])]
        x=O.study_coverage(rows,[],0)
        self.assertEqual((x['due'],x['recorded'],x['eligible_forecasts'],x['abstained']),(7,6,2,2))
        self.assertEqual(x['abstention_rate'],2/6)
        out={'warnings':[]};O.abstention_warning(out,'state',x)
        self.assertEqual(len(out['warnings']),1)
        self.assertEqual(O.study_coverage(rows,[],4)['recorded'],3)
        out={'warnings':[]};O.abstention_warning(out,'state',O.study_coverage(rows,[],4))
        self.assertEqual(out['warnings'],[])
        empty=O.study_coverage([],rows,0)
        self.assertEqual(empty['due'],0);self.assertIsNone(empty['abstention_rate'])

    def test_v2_reader_does_not_register_or_pool_with_v1(self):
        from research_tools.state_v2 import core as V
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);now=100*K.DAY
            out={'studies':{},'depth_diagnostics':{},'warnings':[],'alerts':[]}
            O.state_v2_health(base,now,out)
            self.assertEqual(list(base.iterdir()),[])
            reg=V.register(base,now-K.HOUR)
            V.Journal(base,'activation').add('state-v2',{'registration_sha':reg['sha256'],
                'confirmed_ms':now-K.HOUR,'first_slot':now,'commit':'main'})
            V.Journal(base,'forecasts').add('state-'+str(now),{'study':'state','slot':now,
                'state':'abstained','prepared_ms':now+K.MIN,'deadline_ms':now+25*K.MIN,'reasons':['no-eligible-depth']})
            O.state_v2_health(base,now+40*K.MIN,out)
            x=out['studies']['state_v2']
            self.assertEqual((x['due'],x['recorded'],x['eligible_forecasts'],x['abstained']),(1,1,0,1))
            self.assertFalse((base/K.STREAM).exists())
            self.assertEqual(out['depth_diagnostics']['state_v2_last_24h']['abstained'],1)

class OptionsContinuity(unittest.TestCase):
    setUp = Diagnostics.setUp
    def test_collection_success_survives_five_low_oi_hours(self):
        for i in range(8):
            t=self.slot+i*K.HOUR+K.MIN
            K.Journal(self.base,'options').add(str(t),{'observed_at':t,
                'rr25_7d':{'state':'ok' if i<3 else 'low-oi'},'rr25_30d':{'state':'ok'}})
        with patch.object(O,'options_diagnostics',return_value={}):
            x=O.build(self.base,self.slot+8*K.HOUR+O.GRACE)
        o=x['pilots']['options']
        self.assertEqual(o['capture']['successful'],8)
        self.assertEqual(o['horizons']['rr25_7d']['successful'],3)
        self.assertEqual(o['horizons']['rr25_30d']['successful'],8)
        self.assertFalse(any(a.startswith('options:') for a in x['alerts']))
        self.assertTrue(any('quality warning' in a for a in x['warnings']))

    def test_unavailable_and_recovered_are_not_expiry_rolls(self):
        import gzip
        from desk import stream_util as U
        p=self.base/K.STREAM/'option_legs'/'legs.json.gz';p.parent.mkdir(parents=True)
        raw=U.canonical([]);p.write_bytes(gzip.compress(raw))
        rows=[]
        for state,pair in [('ok',['A','B']),('low-oi',[]),('ok',['A','B']),('ok',['B','C'])]:
            rows.append({'data':{'legs_file':str(p.relative_to(self.base)),'legs_sha':hashlib.sha256(raw).hexdigest(),
                        'expiries':{},'rr25_7d':{'state':state,'expiries':pair},'rr25_30d':{'state':'unusable'}}})
        with patch.object(O,'selected_options',return_value=[]):
            d=O.options_diagnostics(self.base,rows)
        self.assertEqual(d['bracketing_expiry_changes'],1)
        self.assertEqual(d['eligibility_transitions_by_horizon']['rr25_7d'],2)
