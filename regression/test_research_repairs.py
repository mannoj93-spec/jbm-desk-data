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

    def month_rows(self):
        return R.replay_evidence(self.evidence)['bars']

    def test_readiness_reports_exact_missing_times_without_mutation(self):
        now=dt.datetime(2026,10,31,22,tzinfo=R.UTC)
        rows=[b for b in self.month_rows() if b['open_utc'] < '2026-10-31T00:00:00Z']
        other=['2026-10-14T08:00:00Z','2026-10-14T12:00:00Z']
        out=R.readiness(now,span=lambda *args:('incomplete',[b for b in rows if b['open_utc'] not in other],[{'state':'incomplete'}]))
        self.assertEqual(out['state'],'blocked');self.assertEqual(out['missing_4h_opens'],other)
        self.assertEqual(out['unapproved_interior_4h_opens'],other)
        # The one registered gap is reported, and is no longer a blocker once its evidence is approved.
        out=R.readiness(now,span=lambda *args:('incomplete',[b for b in rows if b['open_utc'] not in R.GAP],[{'state':'incomplete'}]))
        self.assertEqual(out['state'],'ready-approved-repair');self.assertEqual(out['missing_4h_opens'],R.GAP)
        self.assertEqual(out['unapproved_interior_4h_opens'],[])
        both=[b for b in rows if b['open_utc'] not in R.GAP+other]
        self.assertEqual(R.readiness(now,span=lambda *args:('incomplete',both,[{'state':'incomplete'}]))['state'],'blocked')

    def test_readiness_checks_every_day_not_only_the_month_boundary(self):
        calls=[]
        rows=[dict(b,open_utc=b['open_utc'].replace('2026-10','2026-11')) for b in self.month_rows()]
        def span(first,last,interval):
            calls.append((first,last,interval))
            return 'ok',[b for b in rows if first.isoformat() <= b['open_utc'][:10] <= last.isoformat()],[{'state':'ok'}]
        out=R.readiness(dt.datetime(2026,11,15,22,37,tzinfo=R.UTC),span=span)
        self.assertEqual(calls,[(dt.date(2026,11,1),dt.date(2026,11,14),'4h')])
        self.assertEqual((out['state'],out['from_utc'],out['through_utc_exclusive'],out['missing_4h_opens']),
                         ('ready','2026-11-01T00:00:00Z','2026-11-15T00:00:00Z',[]))
        # Days 1-3 assess the whole previous month, which the refit at the month start needs.
        calls.clear();R.readiness(dt.datetime(2026,12,2,22,37,tzinfo=R.UTC),span=span)
        self.assertEqual(calls,[(dt.date(2026,11,1),dt.date(2026,11,30),'4h')])
        gap=['2026-11-07T04:00:00Z']
        out=R.readiness(dt.datetime(2026,11,9,tzinfo=R.UTC),
                        span=lambda f,l,i:('incomplete',[b for b in rows if b['open_utc']<'2026-11-09' and b['open_utc'] not in gap],
                                           [{'state':'ok'}]*6+[{'state':'incomplete'}]+[{'state':'ok'}]))
        self.assertEqual((out['state'],out['unapproved_interior_4h_opens']),('blocked',gap))

    def test_readiness_separates_an_unpublished_tail_from_a_gap(self):
        rows=[dict(b,open_utc=b['open_utc'].replace('2026-10','2026-11')) for b in self.month_rows()]
        now=dt.datetime(2026,11,15,22,37,tzinfo=R.UTC)
        def run(keep,states,state='missing'):
            return R.readiness(now,span=lambda f,l,i:(state,[b for b in rows if b['open_utc']<'2026-11-15' and keep(b['open_utc'])],
                                                     [{'state':x} for x in states]))
        out=run(lambda t:t<'2026-11-14',['ok']*13+['missing'])
        self.assertEqual(out['state'],'ready-unpublished-tail')
        self.assertEqual(len(out['unpublished_tail_4h_opens']),6);self.assertEqual(out['unapproved_interior_4h_opens'],[])
        # A partial final day, a missing file before a published one, too long a tail and a failed retrieval all block.
        self.assertEqual(run(lambda t:t<'2026-11-14T12',['ok']*13+['incomplete'],'incomplete')['state'],'blocked')
        self.assertEqual(run(lambda t:not t.startswith('2026-11-10'),['ok']*9+['missing']+['ok']*4)['state'],'blocked')
        self.assertEqual(run(lambda t:t<'2026-11-11',['ok']*10+['missing']*4)['state'],'blocked')
        out=run(lambda t:t<'2026-11-14',['ok']*13+['retrieval_error'],'retrieval_error')
        self.assertEqual((out['state'],out['inadmissible_states']),('blocked',['retrieval_error']))
        self.assertEqual(run(lambda t:True,['ok']*13+['malformed'],'malformed')['state'],'blocked')

    def test_as_of_option_rehearses_without_changing_anything(self):
        import io, contextlib
        seen=[]
        def fake(now=None,span=None):
            seen.append(now);return {'state':'ready'}
        with patch.object(R,'readiness',fake), patch('sys.argv',['x','readiness','--as-of','2026-11-02T22:37:00Z']), \
             contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as done:
            R.main()
        self.assertEqual((seen,done.exception.code),([dt.datetime(2026,11,2,22,37,tzinfo=R.UTC)],0))

    def test_registry_admits_only_the_approved_shape(self):
        self.assertEqual([(s.gap_month,s.fit_month,s.gap) for s in R.approved()],[('2026-10','2026-11',R.GAP)])
        for first,bars in [('2026-10-28T00:00:00Z',7),('2026-10-28T00:00:00Z',0),('2026-10-28T00:00:00Z',True),
                           ('2026-10-28T02:00:00Z',1),('2026-10-01T20:00:00Z',1),('2026-10-31T00:00:00Z',1),
                           ('2026-10-30T04:00:00Z',6)]:
            with self.assertRaises(ValueError,msg=(first,bars)):R.Spec(first,bars)
        s=R.Spec('2026-12-30T20:00:00Z',1)
        self.assertEqual((s.fit_month,s.month_bars,R.J._iso(s.api_start),R.J._iso(s.api_end)),
                         ('2027-01',186,'2026-12-29T20:00:00Z','2027-01-01T00:00:00Z'))
        entry=json.loads(R.REGISTRY.read_text())['repairs'][0]
        with tempfile.TemporaryDirectory() as tmp:
            reg=Path(tmp)/'r.json'
            for doc in [{'schema':'other','repairs':[]},{'schema':R.REGISTRY_SCHEMA,'repairs':[entry,dict(entry,gap_first_open_utc='2026-10-14T00:00:00Z')]},
                        {'schema':R.REGISTRY_SCHEMA,'repairs':[{k:v for k,v in entry.items() if k!='evidence_file_sha256'}]}]:
                reg.write_text(json.dumps(doc))
                with self.assertRaises(ValueError):R.approved(reg)

    def test_another_approved_gap_uses_the_same_rules(self):
        import base64
        e=self.evidence
        def get(url):
            r=e['responses'][url];return base64.b64decode(r['raw_base64']),r['headers']
        _,raw_rows,prov=R.A.fetch_url(R.A.kline_url('4h','2026-10'),get,True,None,R.A.KLINE_COLS)
        spec=R.Spec('2026-10-14T08:00:00Z',3)
        def api(rows):
            return json.dumps([[r[c] for c in R.A.KLINE_COLS] for r in rows
                               if R.J._ms(spec.api_start) <= int(r['open_time']) < R.J._ms(spec.api_end)]).encode()
        full=self.month_rows()
        archive=[b for b in full if b['open_utc'] not in spec.gap]
        report={'prov':{'checksum_status':'match','sha256':prov['sha256']}}
        rows,repair=R.repaired_bars('incomplete',archive,report,api(raw_rows),spec)
        self.assertEqual((len(rows),repair['filled'],repair['overlap_checked']),(186,spec.gap,12))
        self.assertEqual(R.missing(rows,spec.start,spec.end),[])
        filled=[r for r in rows if r['open_utc'] in spec.gap]
        self.assertTrue(all(r['source_role']=='approved-interior-repair' for r in filled))
        for k in ('open','high','low','close','volume','taker_buy_volume'):
            self.assertEqual([r[k] for r in filled],[b[k] for b in full if b['open_utc'] in spec.gap])
        # The same archive under the October entry, a second hole, a changed neighbour and a short API window are refused.
        with self.assertRaisesRegex(ValueError,'approved gap'):R.repaired_bars('incomplete',archive,report,api(raw_rows))
        with self.assertRaisesRegex(ValueError,'approved gap'):R.repaired_bars('incomplete',archive[:-1],report,api(raw_rows),spec)
        changed=[dict(r) for r in raw_rows]
        i=next(n for n,r in enumerate(changed) if int(r['open_time'])==R.J._ms(spec.api_start))
        changed[i]['close']=str(float(changed[i]['close'])+1)
        with self.assertRaisesRegex(ValueError,'overlap'):R.repaired_bars('incomplete',archive,report,api(changed),spec)
        with self.assertRaises(ValueError):R.repaired_bars('incomplete',archive,report,api(raw_rows[:i+5]+raw_rows[i+6:]),spec)
        with self.assertRaisesRegex(ValueError,'approved gap'):
            R.repaired_bars('incomplete',archive,dict(prov=dict(report['prov'],checksum_status='mismatch')),api(raw_rows),spec)

    def test_registered_repair_reproduces_the_delta_on_main_and_pins_its_evidence(self):
        import shutil
        main=[p.name for p in (R.ROOT/'desk/inputs/refit').glob('*.json.gz') if R.J.read_blob(p)[1]['month']=='2026-11']
        now=R.J.R._t(self.evidence['captured_utc'])+dt.timedelta(seconds=1)
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);(base/'desk/inputs/refit').mkdir(parents=True)
            for p in (R.ROOT/'desk/inputs/refit').glob('*.json.gz'):
                if p.name not in main:shutil.copy(p,base/'desk/inputs/refit'/p.name)
            self.assertEqual(R.J.history_chain(base)[0][-1]['open_utc'],'2026-09-30T20:00:00Z')
            entry=json.loads(R.REGISTRY.read_text())
            bad=Path(tmp)/'registry.json'
            bad.write_text(json.dumps(dict(entry,repairs=[dict(entry['repairs'][0],evidence_file_sha256='0'*64)])))
            with self.assertRaisesRegex(ValueError,'approved hash'):R.prepare(base,now,registry=bad)
            self.assertEqual([p.name for p in (base/'desk/inputs/refit').glob('*.json.gz')],
                             [p.name for p in (R.ROOT/'desk/inputs/refit').glob('*.json.gz') if p.name not in main])
            with patch.object(R.A,'load_klines_span') as fetch:
                self.assertEqual(R.prepare(base,now),{'state':'ready-for-frozen-refit','month':'2026-11'})
                fetch.assert_not_called()
            self.assertEqual(sorted(p.name for p in (base/'desk/inputs/refit').glob('*.json.gz')),
                             sorted(p.name for p in (R.ROOT/'desk/inputs/refit').glob('*.json.gz')))
            self.assertEqual(sorted(p.name for p in (base/'desk/inputs/source-repairs').glob('*.json.gz')),
                             sorted(p.name for p in (R.ROOT/'desk/inputs/source-repairs').glob('*.json.gz')))

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
