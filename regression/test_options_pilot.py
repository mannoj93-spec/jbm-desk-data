"""Prospective paired expiry decisions and later, separately clocked book diagnostics."""
import copy
import hashlib
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from desk import stream_util as U
from research_tools.options_pilot import core as K, study as S
from research_tools.options_pilot.__main__ import paused
from research_tools.market_studies import core as V1
from research_tools.state_v2 import core as V2


def capture():
    now = U.ms(U.parse('2026-10-27T12:00:00Z'))
    cap = {'observed_at': now, 't_event_min': now-1000,
           'fields': ['instrument','mark_iv','bid_price_btc','ask_price_btc','open_interest_btc','source_ts_offset_ms'],
           'underlying_v2': {}, 'rows': []}
    for code in ['30OCT26','31OCT26','6NOV26','20NOV26','27NOV26']:
        cap['underlying_v2'][code] = ['BTC',80000,0]
        T = (S.O.expiry_ms(code)-now)/(365.25*K.DAY)
        for side, z in [('C',.67448975), ('P',-.67448975)]:
            strike = round(80000*math.exp(z*.5*math.sqrt(T)+.5*.5**2*T))
            mid = S.O.black76(80000,strike,T,.5,side=='C')/80000
            cap['rows'].append([f'BTC-{code}-{strike}-{side}',50,mid*.98,mid*1.02,1 if code=='31OCT26' else 10,0])
    return cap


def response(instrument, now, **fields):
    raw = json.dumps({'result': {'instrument_name':instrument,'state':'open','timestamp':now,
                                'best_bid_price':.01,'best_ask_price':.011,'best_bid_amount':2,
                                'best_ask_amount':3, **fields}})
    return {'state':'ok','sent_ms':now,'received_ms':now+10,'raw':raw,'raw_sha':hashlib.sha256(raw.encode()).hexdigest()}


class Pilot(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.cap=capture();self.slot=self.cap['observed_at']
        K.register(self.base,self.slot-K.HOUR)

    def remote(self,base,paths):
        return 'main-proof', {str(p): ((K.ROOT if str(p) in K.identity() else self.base)/p).read_bytes() for p in paths}

    def activate(self):
        K.confirm(self.base,clock=lambda:self.slot-K.MIN,fetch=self.remote)

    def test_control_low_oi_while_alternate_recovers_same_filters(self):
        selected=S.compare(self.cap)['horizons']
        self.assertIn('low-oi',selected['7']['nearest-listed']['state'])
        a=selected['7']['nearest-eligible']
        self.assertEqual(a['expiries'],['30OCT26','6NOV26']);self.assertEqual(a['state'],'ok')
        self.assertEqual(len(a['instruments']),4)
        self.assertEqual(selected['30']['nearest-listed'],selected['30']['nearest-eligible'])
        self.assertEqual(self.cap,capture())

    def test_no_extrapolation_and_predeclared_span_cap(self):
        for code in ['30OCT26','31OCT26','6NOV26']:
            self.cap['underlying_v2'].pop(code)
        self.assertEqual(S.compare(self.cap)['horizons']['7']['nearest-eligible']['state'],'no-eligible-bracket')
        self.cap=capture();self.cap['underlying_v2'].pop('6NOV26')
        self.assertEqual(S.compare(self.cap)['horizons']['7']['nearest-eligible']['state'],'bracket-too-wide')

    def test_own_registration_code_confirmation_and_frozen_identities(self):
        self.assertIsNone(K.activation(self.base));self.activate()
        self.assertEqual(K.activation(self.base)['first_slot'],self.slot)
        self.assertFalse((self.base/V1.STREAM).exists())
        for core,key in [(V1,'v1'),(V2,'state-v2')]:
            self.assertEqual(core.identity(),core.Journal(core.ROOT,'registration').get(key)['data']['identity'])
        def wrong(base,paths):
            sha,files=self.remote(base,paths);files['research_tools/options_pilot/study.py']=b'wrong';return sha,files
        with self.assertRaisesRegex(ValueError,'Implementation not on main'):
            K.confirm(self.base,clock=lambda:self.slot,fetch=wrong)
        (self.base/V1.STREAM).mkdir(parents=True);(self.base/V1.STREAM/'paused.json').write_text('{}')
        self.assertTrue(paused(self.base))

    def test_books_keep_missing_sizes_and_wrong_clocks_unavailable(self):
        instrument='BTC-30OCT26-81000-C';now=self.slot+100
        good=S.book_result(instrument,response(instrument,now),self.slot)
        self.assertEqual((good['bid_size'],good['ask_size']),(2,3))
        for extra in [{'best_bid_amount':None},{'best_bid_amount':True},{'best_bid_amount':float('nan')},
                      {'instrument_name':'wrong'},{'timestamp':now-30001},{'best_bid_price':.012},{'state':'closed'}]:
            bad=S.book_result(instrument,response(instrument,now,**extra),self.slot)
            self.assertEqual(bad['state'],'unavailable');self.assertIsNone(bad['bid_size'])
        self.assertEqual(S.book_result(instrument,response(instrument,now,best_bid_amount=0),self.slot)['bid_size'],0)

    def test_deduplicated_books_late_source_and_batch(self):
        selection=S.compare(self.cap);now=self.slot+100
        def get(url):
            from urllib.parse import parse_qs,urlparse
            return response(parse_qs(urlparse(url).query)['instrument_name'][0],now)
        b=S.books(selection,self.slot,get,clock=lambda:now)
        self.assertEqual(b['expected'],len(b['raw']));self.assertLessEqual(b['expected'],16)
        self.assertTrue(all(q['state']=='ok' for q in b['quotes']))
        with patch.object(S,'fetch') as unused:
            old=S.books(selection,self.slot,unused,clock=lambda:self.slot+16*K.MIN)
            unused.assert_not_called();self.assertEqual(old['state'],'source-too-old')
        clocks=iter([now,now+60001]);late=S.books(selection,self.slot,get,clock=lambda:next(clocks))
        self.assertEqual(late['state'],'late-batch');self.assertTrue(all(q['bid_size'] is None for q in late['quotes']))

    def test_book_replay_detects_rehashed_size_and_clock_changes(self):
        selection=S.compare(self.cap);now=self.slot+100
        def get(url):
            from urllib.parse import parse_qs,urlparse
            return response(parse_qs(urlparse(url).query)['instrument_name'][0],now)
        clocks=iter([now,now+20]);b=S.books(selection,self.slot,get,clock=lambda:next(clocks))
        S.verify_books(b,selection,self.slot,now)
        bad=copy.deepcopy(b);bad['quotes'][0]['bid_size']=1000
        with self.assertRaisesRegex(ValueError,'reproduction'):S.verify_books(bad,selection,self.slot,now)
        bad=copy.deepcopy(b);bad['ended_ms']=now+60001
        with self.assertRaisesRegex(ValueError,'completion'):S.verify_books(bad,selection,self.slot,now)

    def test_first_capture_shared_deadline_idempotence_and_replay(self):
        self.activate();newer=copy.deepcopy(self.cap);newer['observed_at']+=100
        with patch.object(S,'Store') as store:
            store.return_value.option_quotes.return_value=[newer,self.cap]
            S.collect(self.base,self.slot+20*K.MIN,clock=lambda:self.slot+20*K.MIN)
            S.collect(self.base,self.slot+30*K.MIN,clock=lambda:self.slot+30*K.MIN)
        rows=K.Journal(self.base,'observations').rows
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['data']['source_ms'],self.slot)
        report=S.report(self.base,self.slot+K.HOUR)
        self.assertEqual((report['closed'],report['captured']),(1,1))
        self.assertEqual(report['horizons']['7']['paired']['gained'],1)
        self.assertEqual(report['books']['attempted'],0) # old source: no late substitute book
        S.write(self.base,self.slot+K.HOUR)
        ref=rows[0]['data']['artifact'];a=S.read_artifact(self.base,ref)
        a['selection']['horizons']['7']['nearest-eligible']['value']=99
        newref=S.artifact(self.base,a)
        # Rehashing the journal cannot hide a numerical mutation.
        path=self.base/K.STREAM/'observations.jsonl';path.unlink()
        K.Journal(self.base,'observations').add(str(self.slot),dict(rows[0]['data'],artifact=newref))
        with self.assertRaisesRegex(ValueError,'reproduction'):S.report(self.base,self.slot+K.HOUR)

    def test_no_backfill_before_activation_or_after_deadline(self):
        self.activate()
        with patch.object(S,'Store') as store,patch.object(S,'books') as books:
            store.return_value.option_quotes.return_value=[self.cap]
            S.collect(self.base,self.slot+K.HOUR,clock=lambda:self.slot+K.HOUR)
            books.assert_not_called()
        r=S.report(self.base,self.slot+K.HOUR)
        self.assertEqual((r['closed'],r['captured']),(1,0))
        self.assertEqual(r['horizons']['7']['missing_capture'],1)


if __name__=='__main__': unittest.main()
