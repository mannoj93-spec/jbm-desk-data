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
        x=O.safe_build(root,json.loads((root/'reports/market_studies.json').read_text())['generated_ms'])
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

if __name__=='__main__':unittest.main()
