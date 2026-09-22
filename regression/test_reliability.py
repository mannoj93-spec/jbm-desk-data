import copy
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import collector
import intake
import process_issues
import registration
import report
import research
import schema
import scoring
import storage

H = schema.H
M = schema.MINUTE
START = schema.ms('2026-01-01T00:00:00Z')


def forecast(kind='touch'):
    events = {
        'touch': {'type':'touch','dir':'up','level':110,'p':.8,'p_class':'prior'},
        'terminal': {'type':'terminal','dir':'above','level':100,'p':.5,'p_class':'model'},
        'race': {'type':'race','a':{'dir':'up','level':110},'b':{'dir':'down','level':90},'p':.6,'p_class':'model'},
        'interval': {'type':'interval','lo':90,'hi':110,'coverage':.9},
        'lean': {'type':'lean','direction':'down'},
        'predicate': {'type':'predicate','series':'high','op':'>','value':110,'by_utc':schema.iso(START+H)},
        'range': {'type':'range','q10':.05,'q50':.1,'q90':.2},
    }
    return {'id':'test-forecast','instrument':schema.INSTRUMENT,'reference_price':100,
            'start_utc':schema.iso(START),'horizon_utc':schema.iso(START+H),'events':[events[kind]]}


def bars():
    return [(START+i*M,105.,95.,100.) for i in range(60)]


class SchemaTests(unittest.TestCase):
    def test_all_supported_types(self):
        for kind in schema.EVENT_KEYS:
            self.assertEqual(schema.validate(forecast(kind)),[])

    def test_empty_race_legs(self):
        fc=forecast('race');fc['events'][0]['a']={}
        self.assertTrue(schema.validate(fc))

    def test_private_nested_field(self):
        fc=forecast('race');fc['events'][0]['a']['account_size']=1000
        self.assertTrue(schema.validate(fc))

    def test_default_start_before_validation(self):
        now=START+M;fc=forecast();fc.pop('start_utc');fc['horizon_utc']=schema.iso(now+M)
        fc=schema.prepare(fc,now)
        self.assertEqual(schema.ms(fc['start_utc']),START+5*M)
        self.assertTrue(schema.validate(fc,now))

    def test_nonfinite_numbers(self):
        for x in (float('nan'),float('inf'),True):
            fc=forecast();fc['reference_price']=x
            self.assertTrue(schema.validate(fc))

    def test_wrong_types_do_not_crash(self):
        for events in ([None],{},['text']):
            fc=forecast();fc['events']=events
            self.assertTrue(schema.validate(fc))
        self.assertTrue(schema.validate([]))

    def test_naive_or_unaligned_dates_rejected(self):
        for timestamp in ('2026-01-01T00:00:00','2026-01-01T00:00:30Z'):
            fc=forecast();fc['start_utc']=timestamp
            self.assertTrue(schema.validate(fc))

    def test_ambiguous_predicate_deadline(self):
        fc=forecast('predicate');fc['events'][0]['at_utc']=schema.iso(START+H)
        self.assertTrue(schema.validate(fc))

    def test_path_or_unknown_series_rejected(self):
        for series in ('series:../state:c','series:unknown:c','series:okx_mark_1h:private'):
            fc=forecast('predicate');fc['events'][0]['series']=series
            self.assertTrue(schema.validate(fc))

    def test_json_nonfinite_rejected(self):
        with self.assertRaises(ValueError):intake.extract('{"x":NaN}')


class ScoringTests(unittest.TestCase):
    def test_empty_bars_never_false(self):
        with self.assertRaises(scoring.Unscorable):scoring.score(forecast(),[],lambda name:[])

    def test_gap_and_duplicates_rejected(self):
        for data in (bars()[:-1],bars()[:20]+bars()[21:],[bars()[0]]+bars()[:-1]):
            with self.assertRaises(scoring.Unscorable):scoring.score(forecast(),data,lambda name:[])

    def test_missing_series_never_false(self):
        fc=forecast('predicate');fc['events'][0]['series']='series:okx_mark_1h:c'
        with self.assertRaises(scoring.Unscorable):scoring.score(fc,bars(),lambda name:[])

    def test_series_scored_at_close_not_open(self):
        fc=forecast('predicate');fc['events'][0].update(series='series:okx_mark_1h:c',value=99)
        result,evidence=scoring.score(fc,bars(),lambda name:[{'t':START,'f':{'c':100}}])
        self.assertEqual(result[0]['outcome'],1)
        self.assertEqual(evidence['predicate_observations'][0]['observations'][0][0],START+H)

    def test_partial_predicate_series_rejected_even_if_hit(self):
        fc=forecast('predicate');fc['horizon_utc']=schema.iso(START+2*H);fc['events'][0].update(series='series:okx_mark_1h:c',by_utc=schema.iso(START+2*H),value=99)
        data=bars()+[(t+H,h,l,c) for t,h,l,c in bars()]
        with self.assertRaises(scoring.Unscorable):scoring.score(fc,data,lambda name:[{'t':START,'f':{'c':100}}])

    def test_equal_price_is_flat(self):
        result,_=scoring.score(forecast('lean'),bars(),lambda name:[])
        self.assertEqual(result[0]['outcome'],'flat')

    def test_terminal_above_is_strict(self):
        result,_=scoring.score(forecast('terminal'),bars(),lambda name:[])
        self.assertEqual(result[0]['outcome'],0)

    def test_same_minute_race_has_both_score_bounds(self):
        data=bars();data[0]=(START,115,85,100)
        result,_=scoring.score(forecast('race'),data,lambda name:[])
        self.assertEqual(result[0]['outcome'],'bound')
        self.assertEqual(len(result[0]['brier']),2)
        self.assertEqual(len(result[0]['log_score']),2)

    def test_invalidation_is_separate_from_lean(self):
        fc=forecast('lean');fc['events'][0]['invalidation']={'level':99,'dir':'above','basis':'close_1h'}
        result,_=scoring.score(fc,bars(),lambda name:[])
        self.assertEqual(result[0]['outcome'],'flat')
        self.assertEqual(result[0]['invalidated_at'],START+H)

    def test_error_or_empty_http_response(self):
        for raw in (b'[]',b'{"code":-1}',b'[[0]]'):
            with self.assertRaises(scoring.Unscorable):
                scoring.fetch_bars(START,START+H,opener=lambda *a,**kw:io.BytesIO(raw),pause=lambda _:None)

    def test_fetched_price_coverage(self):
        raw=json.dumps([[t,100,h,l,c] for t,h,l,c in bars()]).encode()
        actual=scoring.fetch_bars(START,START+H,opener=lambda *a,**kw:io.BytesIO(raw),pause=lambda _:None)
        self.assertEqual(actual,bars())


class TempProject(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        for name in ('registry','state','tests','data'): (self.base/name).mkdir()
        self.addCleanup(self.tmp.cleanup)

    def freeze(self,fc=None,now=START-M):
        fc=fc or forecast()
        path=self.base/'registry/test.json';storage.atomic_json(path,fc)
        registration.register(self.base,now)
        return path


class PersistenceTests(TempProject):
    def test_atomic_idempotent_append(self):
        path=self.base/'rows.jsonl';key=lambda r:r['t']
        self.assertEqual(storage.append_unique(path,[{'t':1,'x':1}],key),1)
        self.assertEqual(storage.append_unique(path,[{'t':1,'x':2},{'t':2,'x':2}],key),1)
        self.assertEqual(storage.read_rows(path),[{'t':1,'x':1},{'t':2,'x':2}])

    def test_corrupt_state_never_silently_reset(self):
        path=self.base/'state/checkpoints.json';path.write_text('{bad')
        with patch.object(collector,'STATE',str(path)):
            with self.assertRaises(ValueError):collector.load_state()
        self.assertEqual(path.read_text(),'{bad')

    def test_failed_atomic_replace_preserves_old_file(self):
        path=self.base/'state.json';storage.atomic_json(path,{'v':1})
        with patch('storage.os.replace',side_effect=OSError('disk')):
            with self.assertRaises(OSError):storage.atomic_json(path,{'v':2})
        self.assertEqual(storage.read_json(path),{'v':1})

    def test_registration_survives_deletion_and_edit(self):
        path=self.freeze();old=list(registration.forecasts(self.base))[0]
        fc=forecast();fc['events'][0]['level']=120;storage.atomic_json(path,fc)
        new,errors=registration.register(self.base,START+H)
        self.assertTrue(errors)
        path.unlink()
        self.assertEqual(list(registration.forecasts(self.base))[0],old)

    def test_frozen_hash_checked(self):
        self.freeze();_,entry=list(registration.forecasts(self.base))[0]
        (self.base/entry['frozen']).write_text('{}')
        with self.assertRaises(ValueError):list(registration.forecasts(self.base))

    def test_scores_retry_then_persist_evidence_once(self):
        self.freeze()
        records,new,pending,alerts=scoring.score_registry(self.base,START+2*H,'test',fetch=lambda a,b:[])
        self.assertEqual(records,[]);self.assertTrue(alerts);self.assertEqual(pending,1)
        records,new,pending,alerts=scoring.score_registry(self.base,START+2*H,'test',fetch=lambda a,b:bars())
        self.assertEqual(len(new),1);self.assertFalse(alerts)
        evidence=storage.read_json(self.base/new[0]['evidence'])
        self.assertEqual(storage.digest(evidence),new[0]['evidence_sha256'])
        records,new,_,_=scoring.score_registry(self.base,START+3*H,'test',fetch=lambda a,b:self.fail('must not refetch'))
        self.assertEqual(len(records),1);self.assertEqual(new,[])

    def test_tampered_score_evidence_is_flagged_not_rescored(self):
        self.freeze()
        records,_,_,_=scoring.score_registry(self.base,START+2*H,'test',fetch=lambda a,b:bars())
        (self.base/records[0]['evidence']).write_text('{}')
        records,new,_,alerts=scoring.score_registry(self.base,START+3*H,'test',fetch=lambda a,b:self.fail('no silent rescore'))
        self.assertEqual(records[0]['status'],'evidence integrity error')
        self.assertEqual(new,[]);self.assertTrue(alerts)

    def test_one_bad_forecast_does_not_block_other_scores(self):
        self.freeze()
        fc=forecast();fc['id']='second-forecast'
        storage.atomic_json(self.base/'registry/second.json',fc)
        registration.register(self.base,START-M)
        with patch('scoring.score',side_effect=[scoring.Unscorable('missing'),scoring.score(forecast(),bars(),lambda name:[])]):
            records,new,pending,alerts=scoring.score_registry(self.base,START+2*H,'test',fetch=lambda a,b:bars())
        self.assertEqual(len(new),1);self.assertEqual(pending,1);self.assertTrue(alerts)

    def test_registration_at_start_is_late(self):
        self.freeze(now=START)
        records,_,_,_=scoring.score_registry(self.base,START+2*H,'test',fetch=lambda a,b:self.fail('late must not fetch'))
        self.assertTrue(records[0]['status'].startswith('late'))

    def test_corrupt_observations_not_silently_ignored(self):
        fc=forecast('predicate');fc['events'][0]['series']='series:okx_mark_1h:c';self.freeze(fc)
        path=self.base/'data/series/okx_mark_1h/x.jsonl';path.parent.mkdir(parents=True);path.write_text('{broken')
        records,_,_,alerts=scoring.score_registry(self.base,START+2*H,'test',fetch=lambda a,b:bars())
        self.assertEqual(records,[]);self.assertTrue(alerts)

    def test_dependency_change_restarts_test_registration(self):
        test=self.base/'tests/example.py';test.write_text('META={}\n')
        dependency=self.base/'formulas.py';dependency.write_text('x=1\n')
        registration.register(self.base,START)
        old=registration.test_hash(self.base,test)
        dependency.write_text('x=2\n');registration.register(self.base,START+H)
        new=registration.test_hash(self.base,test)
        self.assertNotEqual(old,new)
        self.assertEqual(storage.read_json(self.base/'state/registered.json')['tests/example.py@'+new],START+H)

    def test_append_collector_rows_provenance_and_no_duplicates(self):
        with patch.object(collector,'BASE',str(self.base)):
            row={'t':START,'f':{'c':100},'r':START}
            self.assertEqual(collector.append_rows('series/test',[row]),1)
            self.assertEqual(collector.append_rows('series/test',[row]),0)
        row=storage.read_rows(self.base/'data/series/test/2026-01.jsonl')[0]
        self.assertIn('observed_at',row);self.assertIn('code_version',row)


class CollectorTests(unittest.TestCase):
    def test_failed_backwards_page_does_not_advance(self):
        page=[{'timestamp':i*collector.M5,'longAccount':'.6'} for i in range(500,1000)]
        with patch.object(collector,'NOW',1000*collector.M5),patch.object(collector,'get',side_effect=[(page,None),(None,'HTTP 500')]):
            rows,error,calls=collector.binance_futures_data('test','ep','5m',['longAccount'],100*collector.M5)
        self.assertEqual(rows,[]);self.assertEqual(error,'HTTP 500')

    def test_backfill_does_not_mask_transient_failure(self):
        page=[{'timestamp':i*collector.M5,'longAccount':'.6'} for i in range(500,1000)]
        with patch.object(collector,'NOW',1000*collector.M5),patch.object(collector,'get',side_effect=[(page,None),(None,'HTTP 500')]):
            rows,error,_=collector.binance_futures_data('test','ep','5m',['longAccount'],None)
        self.assertEqual(rows,[]);self.assertEqual(error,'HTTP 500')

    def test_complete_history_filters_forming_rows(self):
        page=[{'timestamp':i*collector.M5,'longAccount':'.6'} for i in range(98,101)]
        with patch.object(collector,'NOW',100*collector.M5),patch.object(collector,'get',return_value=(page,None)):
            rows,error,_=collector.binance_futures_data('test','ep','5m',['longAccount'],98*collector.M5)
        self.assertEqual([r['t'] for r in rows],[99*collector.M5]);self.assertIsNone(error)

    def test_okx_partial_page_discards_checkpoint_candidate(self):
        data={'data':[[START,'100','101','99','100','1']]}
        with patch.object(collector,'NOW',START+H),patch.object(collector,'get',side_effect=[(data,None),(None,'HTTP 500')]):
            rows,error,_=collector.okx_backward('/x?a=b',collector.okx_candle,START-H,5)
        self.assertEqual(rows,[]);self.assertEqual(error,'HTTP 500')

    def test_okx_page_cap_does_not_advance(self):
        with patch.object(collector,'NOW',START+H),patch.object(collector,'get',return_value=({'data':[[START,'100','101','99','100','1']]},None)):
            rows,error,_=collector.okx_backward('/x?a=b',collector.okx_candle,START-H,1)
        self.assertEqual(rows,[]);self.assertIn('page cap',error)

    def test_dvol_dedup_and_grid_validation(self):
        page={'result':{'data':[[START+i*H,100,101,99,100] for i in (0,0,1)]}}
        with patch.object(collector,'NOW',START+2*H),patch.object(collector,'get',return_value=(page,None)):
            rows,error=collector.deribit_dvol(START-H)
        self.assertEqual(len(rows),2);self.assertIsNone(error)
        page['result']['data']=page['result']['data'][:1]
        with patch.object(collector,'NOW',START+2*H),patch.object(collector,'get',return_value=(page,None)):
            rows,error=collector.deribit_dvol(START-H)
        self.assertEqual(rows,[]);self.assertIn('incomplete',error)

    def test_collect_series_failure_retains_checkpoint(self):
        name='binance_globalLongShortAccountRatio_5m'
        state={'series':{name:START}}
        with patch.object(collector,'binance_futures_data',return_value=([], 'HTTP 500',2)), \
             patch.object(collector,'binance_funding',return_value=([],None)), \
             patch.object(collector,'okx_backward',return_value=([],None,1)), \
             patch.object(collector,'get',return_value=({'data':[]},None)), \
             patch.object(collector,'deribit_dvol',return_value=([],None)):
            self.assertFalse(collector.collect_series(state))
        self.assertEqual(state['series'][name],START)

    def test_missing_oi_not_healthy(self):
        self.assertEqual(collector.snap_source('test',lambda:{'oi_btc':None})['st'],'error')


class ResearchTests(TempProject):
    def test_point_in_time_filters_arrival_and_close(self):
        path=self.base/'data/series/okx_mark_1h/2026-01.jsonl'
        storage.append_unique(path,[{'t':START,'f':{'c':100},'observed_at':START+H+M},
                                    {'t':START-H,'f':{'c':100}}],lambda r:r['t'])
        ctx=research.Ctx(self.base,START,START+3*H)
        self.assertEqual(ctx.as_of(START+H).series('okx_mark_1h'),[])
        self.assertEqual(len(ctx.as_of(START+2*H).series('okx_mark_1h')),1)

    def test_maturity_cutoff_and_duplicates(self):
        row={'t_decision':START,'input_cutoff':START,'outcome_at':START+H,'group':'cond','outcome':1}
        future=dict(row,t_decision=START+2*H,outcome_at=START+3*H)
        leakage=dict(row,input_cutoff=START+M)
        post,insample,rejected=research.classify([row,row,future,leakage],START-M,START+2*H,1)
        self.assertEqual(len(post),1);self.assertEqual(len(rejected),3)

    def test_price_context_does_not_extend_past_cutoff(self):
        ctx=research.Ctx(self.base,START,START+3*H).as_of(START+H+M)
        with patch('research.fetch_bars',return_value=[]) as fetch:
            ctx.klines_1h(START,START+3*H)
            fetch.assert_called_once_with(START,START+H,H)


class WorkflowTests(TempProject):
    def test_all_pushes_fail_means_nonzero(self):
        bindir=self.base/'bin';bindir.mkdir()
        fake=bindir/'git';fake.write_text('#!/bin/sh\ncase "$1" in\n push) exit 1;;\n symbolic-ref) echo main;;\n diff) exit 0;;\nesac\nexit 0\n');fake.chmod(0o755)
        sleep=bindir/'sleep';sleep.write_text('#!/bin/sh\nexit 0\n');sleep.chmod(0o755)
        result=subprocess.run(['bash',str(Path('scripts/commit_push.sh').resolve())],env=dict(os.environ,PATH=str(bindir)+':'+os.environ['PATH']),capture_output=True)
        self.assertNotEqual(result.returncode,0)

    def test_push_success(self):
        bindir=self.base/'bin';bindir.mkdir()
        fake=bindir/'git';fake.write_text('#!/bin/sh\nif [ "$1" = symbolic-ref ]; then echo main; fi\nexit 0\n');fake.chmod(0o755)
        result=subprocess.run(['bash',str(Path('scripts/commit_push.sh').resolve())],env=dict(os.environ,PATH=str(bindir)+':'+os.environ['PATH']),capture_output=True)
        self.assertEqual(result.returncode,0)

    def test_issue_not_closed_when_push_fails(self):
        issue={'number':1,'title':'forecast','body':json.dumps(forecast()),'author':{'login':'owner'}}
        with patch('process_issues.subprocess.run',side_effect=subprocess.CalledProcessError(1,'push')),patch('process_issues.gh') as gh,patch('process_issues.comment') as comment:
            with self.assertRaises(subprocess.CalledProcessError):process_issues.process(issue,self.base,'owner',START-M)
        gh.assert_not_called();comment.assert_not_called()

    def test_issue_acknowledgement_after_successful_push(self):
        issue={'number':1,'title':'forecast','body':json.dumps(forecast()),'author':{'login':'owner'}}
        calls=[]
        with patch('process_issues.subprocess.run',side_effect=lambda *a,**k:calls.append('push')),patch('process_issues.gh',side_effect=lambda *a:calls.append('close')),patch('process_issues.comment',side_effect=lambda *a:calls.append('comment')):
            process_issues.process(issue,self.base,'owner',START-M)
        self.assertEqual(calls,['push','comment','close'])

    def test_nonowner_is_ignored(self):
        with patch('process_issues.gh') as gh:
            process_issues.process({'number':1,'title':'forecast','author':{'login':'stranger'}},self.base,'owner',START)
            gh.assert_not_called()

    def test_coverage_never_exceeds_100_percent(self):
        runs=[{'t':START+7*M+i*1000} for i in range(3)]
        covered,expected=report.run_coverage(runs,START,START+H)
        self.assertLessEqual(covered,expected)


if __name__=='__main__':unittest.main()
