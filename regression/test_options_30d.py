"""Maturity experiment has a genuinely separate rule, clock, denominator and immutable evidence."""
import copy
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from desk import stream_util as U
from research_tools.options_30d import study as S, core as K
from research_tools.options_pilot import core as OLD
from regression.test_options_pilot import response
import options_capture_timing as T


def capture():
    now=U.ms(U.parse('2026-11-05T21:00:00Z'))
    cap={'t':now,'observed_at':now,'t_event_min':now-1000,
         'fields':['instrument','mark_iv','bid_price_btc','ask_price_btc','open_interest_btc','source_ts_offset_ms'],
         'underlying_v2':{},'rows':[]}
    for code in ['13NOV26','27NOV26','25DEC26','29JAN27']:
        cap['underlying_v2'][code]=['BTC',80000,0]
        years=(S.O.expiry_ms(code)-now)/(365.25*K.DAY)
        for side,z in [('C',.67448975),('P',-.67448975)]:
            strike=round(80000*math.exp(z*.5*math.sqrt(years)+.5*.5**2*years))
            mid=S.O.black76(80000,strike,years,.5,side=='C')/80000
            cap['rows'].append([f'BTC-{code}-{strike}-{side}',50,mid*.98,mid*1.02,10,0])
    return cap


class Maturity(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.cap=capture();self.slot=self.cap['observed_at']
        K.register(self.base,self.slot-K.HOUR)

    def remote(self,base,paths):
        return 'main-proof',{str(p):((K.ROOT if str(p) in K.identity() else self.base)/p).read_bytes() for p in paths}

    def activate(self):
        K.confirm(self.base,clock=lambda:self.slot-K.MIN,fetch=self.remote)

    def test_wider_maturity_recovers_bracket_with_same_leg_filters(self):
        before=copy.deepcopy(self.cap);r=S.compare(self.cap)['horizons']['30']
        self.assertEqual(r['eligible-45d']['state'],'no-eligible-bracket')
        self.assertEqual(r['eligible-90d']['state'],'ok')
        self.assertEqual(r['eligible-90d']['expiries'],['27NOV26','25DEC26'])
        self.assertEqual(r['eligible-90d']['span_days'],28)
        self.assertEqual(self.cap,before)
        for row in self.cap['rows']:
            if '25DEC26' in row[0]:row[4]=1
        self.assertNotEqual(S.compare(self.cap)['horizons']['30']['eligible-90d']['state'],'ok')

    def test_no_extrapolation_and_same_span_cap(self):
        self.cap['underlying_v2'].pop('25DEC26')
        self.assertEqual(S.compare(self.cap)['horizons']['30']['eligible-90d']['state'],'bracket-too-wide')
        self.cap['underlying_v2'].pop('29JAN27')
        self.assertEqual(S.compare(self.cap)['horizons']['30']['eligible-90d']['state'],'no-eligible-bracket')

    def test_separate_clock_no_historical_pooling_and_no_backfill(self):
        self.assertIsNone(K.activation(self.base));self.activate()
        self.assertEqual(K.activation(self.base)['first_slot'],self.slot)
        self.assertFalse((self.base/OLD.STREAM).exists())
        with patch.object(S,'Store') as store:
            store.return_value.option_quotes.return_value=[self.cap]
            S.collect(self.base,self.slot+20*K.MIN,clock=lambda:self.slot+20*K.MIN)
            S.collect(self.base,self.slot+30*K.MIN,clock=lambda:self.slot+30*K.MIN)
        out=S.report(self.base,self.slot+K.HOUR)
        self.assertEqual((out['closed'],out['captured']),(1,1))
        self.assertEqual(out['horizons']['30']['paired']['gained'],1)
        self.assertEqual(len(K.Journal(self.base,'observations').rows),1)
        S.write(self.base,self.slot+K.HOUR)
        with patch.object(S,'Store') as store:
            store.return_value.option_quotes.return_value=[dict(self.cap,observed_at=self.slot+K.HOUR)]
            S.collect(self.base,self.slot+2*K.HOUR,clock=lambda:self.slot+2*K.HOUR)
        out=S.report(self.base,self.slot+2*K.HOUR)
        self.assertEqual((out['closed'],out['captured']),(2,1))
        self.assertEqual(out['horizons']['30']['missing_capture'],1)

    def test_new_package_and_previous_package_are_both_bound_on_main(self):
        def wrong(base,paths):
            sha,files=self.remote(base,paths);files['research_tools/options_30d/study.py']=b'wrong';return sha,files
        with self.assertRaisesRegex(ValueError,'Implementation not on main'):
            K.confirm(self.base,clock=lambda:self.slot,fetch=wrong)
        self.assertTrue(set(OLD.identity()) < set(K.identity()))
        self.assertEqual(OLD.identity(),OLD.Journal(OLD.ROOT,'registration').get('options-v2')['data']['identity'])

    def test_collector_budget_skip_and_missing_record_are_explicit(self):
        from types import SimpleNamespace
        source=self.base/'data/options/deribit_btc_quotes/2026-11-05.jsonl'
        source.parent.mkdir(parents=True);source.write_text(json.dumps(self.cap)+'\n')
        saved=[]
        collector=SimpleNamespace(BASE=str(self.base),NOW=self.slot,day=lambda t:'2026-11-05',
            DEADLINE=0,STAGE_DEADLINE=None,SOURCE_DEADLINE=None,
            append_rows=lambda directory,rows,**kwargs:saved.extend(rows))
        with patch.object(T,'capture') as unused:
            result=T.collect(collector)
            unused.assert_not_called()
        self.assertEqual(result['state'],'budget-skipped')
        self.assertEqual(saved[0]['source_ms'],self.slot)
        self.assertEqual(T.report(self.base,self.slot+100)['missing_book_records'],1)
        path=self.base/'data'/T.DIRECTORY/'2026-11-05.jsonl';path.parent.mkdir(parents=True)
        saved[0]['observed_at']=self.slot+50;path.write_text(json.dumps(saved[0])+'\n')
        out=T.report(self.base,self.slot+100)
        self.assertEqual(out['missing_book_records'],0)
        self.assertEqual(out['states'],{'budget-skipped':1})

    def test_immediate_diagnostic_books_keep_actual_later_clock_and_replay(self):
        from urllib.parse import parse_qs,urlparse
        now=self.slot+100
        def get(url):return response(parse_qs(urlparse(url).query)['instrument_name'][0],now)
        times=iter([now,now,now+20,now+21])
        row=T.capture(self.cap,get=get,clock=lambda:next(times))
        row['observed_at']=now+22
        source=self.base/'data/options/deribit_btc_quotes/2026-11-05.jsonl'
        source.parent.mkdir(parents=True);source.write_text(json.dumps(self.cap)+'\n')
        path=self.base/'data'/T.DIRECTORY/'2026-11-05.jsonl';path.parent.mkdir(parents=True)
        path.write_text(json.dumps(row)+'\n')
        out=T.report(self.base,now+100)
        self.assertEqual(out['usable'],out['expected']);self.assertGreater(out['usable'],0)
        self.assertEqual(out['source_to_book_ms']['median'],110)
        row['books']['quotes'][0]['bid_size']=999
        path.write_text(json.dumps(row)+'\n')
        with self.assertRaisesRegex(ValueError,'reproduction'):T.report(self.base,now+100)


if __name__=='__main__':unittest.main()
