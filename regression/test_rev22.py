"""Regression tests for reliability revision 2.2 (2026-09-23 audit).

Each test reproduces a defect measured against the live sources, or pins a new contract.
Offline: every network call is simulated.
"""
import io
import json
import math
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

import collector
import research
import schema
import scoring
import storage
import watchdog

H = schema.H
M = schema.MINUTE
M5 = 5 * M
START = schema.ms('2026-01-01T00:00:00Z')


def fake_binance(stamps, interval, step):
    """Simulate /futures/data paging. Measured 2026-09-22: the taker endpoint filters endTime on
    the interval close (t + step <= endTime); ratio and OI endpoints filter on the stamp."""
    def get(url, **_):
        end = int(url.split('endTime=')[1])
        rows = [t for t in stamps if (t + step if interval else t) <= end][-500:]
        return [{'timestamp': t, 'buySellRatio': '1', 'buyVol': '2', 'sellVol': '2'} for t in rows], None
    return get


class TakerPaginationTests(unittest.TestCase):
    def run_backfill(self, name, interval):
        now = START + 1300 * M5
        stamps = [START + i * M5 for i in range(1300)]
        with patch.object(collector, 'NOW', now), patch.object(collector, 'get', side_effect=fake_binance(stamps, interval, M5)):
            rows, err, _ = collector.binance_futures_data(name, 'x', '5m', ['buySellRatio', 'buyVol', 'sellVol'], None)
        return rows, err

    def test_interval_endpoint_pages_without_gaps(self):
        rows, err = self.run_backfill('binance_takerlongshortRatio_5m', True)
        got = [r['t'] for r in rows]
        self.assertIsNone(err)
        self.assertEqual(got, list(range(got[0], got[-1] + M5, M5)))   # contiguous: no row lost per page
        self.assertEqual(len(got), 1300)                                   # every closed interval

    def test_snapshot_endpoint_pages_without_gaps_or_duplicates(self):
        rows, err = self.run_backfill('binance_topLongShortPositionRatio_5m', False)
        got = [r['t'] for r in rows]
        self.assertIsNone(err)
        self.assertEqual(got, list(range(got[0], got[-1] + M5, M5)))


class StampSemanticsTests(unittest.TestCase):
    def test_kinds(self):
        self.assertEqual(schema.SERIES_KIND['binance_topLongShortPositionRatio_1h'], 'snapshot')
        self.assertEqual(schema.SERIES_KIND['binance_openInterestHist_1h'], 'snapshot')
        self.assertEqual(schema.SERIES_KIND['binance_takerlongshortRatio_1h'], 'interval')
        self.assertEqual(schema.SERIES_KIND['okx_mark_1h'], 'interval')
        self.assertEqual(schema.known_time('binance_topLongShortPositionRatio_1h', START), START + 5 * M)
        self.assertEqual(schema.known_time('binance_takerlongshortRatio_1h', START), START + H)

    def test_snapshot_predicate_reads_the_row_stamped_at_the_deadline(self):
        fc = {'id': 'snap-pred', 'instrument': schema.INSTRUMENT, 'reference_price': 100,
              'start_utc': schema.iso(START), 'horizon_utc': schema.iso(START + H),
              'events': [{'type': 'predicate', 'series': 'series:binance_topLongShortPositionRatio_1h:longAccount',
                          'op': '<', 'value': .68, 'at_utc': schema.iso(START + H)}]}
        bars = [(START + i * M, 105., 95., 100.) for i in range(60)]
        rows = [{'t': START, 'f': {'longAccount': .70}}, {'t': START + H, 'f': {'longAccount': .66}}]
        result, _ = scoring.score(fc, bars, lambda name: rows)
        self.assertEqual(result[0]['value'], .66)      # 2.1 read the 00:00 row (.70) for a 01:00 deadline
        self.assertEqual(result[0]['outcome'], 1)

    def test_point_in_time_snapshot_admitted_at_stamp_plus_five_minutes(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = base / 'data/series/binance_topLongShortPositionRatio_1h/2026-01.jsonl'
            storage.append_unique(path, [{'t': START, 'f': {'longAccount': .6}, 'observed_at': START + 6 * M}], lambda r: r['t'])
            ctx = research.Ctx(base, START, START + 3 * H)
            self.assertEqual(ctx.as_of(START + 5 * M).series('binance_topLongShortPositionRatio_1h'), [])
            self.assertEqual(len(ctx.as_of(START + 6 * M).series('binance_topLongShortPositionRatio_1h')), 1)


class LiquidationPaginationTests(unittest.TestCase):
    def test_same_millisecond_pair_split_across_pages_is_kept(self):
        now = START + 2 * H
        # 150 orders, one per second, plus a second order sharing the 100th order's millisecond.
        orders = [{'ts': str(now - i * 1000), 'posSide': 'long', 'side': 'sell', 'sz': str(i + 1), 'bkPx': '100'}
                  for i in range(150)]
        orders.insert(100, {'ts': orders[99]['ts'], 'posSide': 'short', 'side': 'buy', 'sz': '999', 'bkPx': '101'})

        def get(url, **_):
            after = int(url.split('after=')[1]) if 'after=' in url else None
            page = [o for o in orders if after is None or int(o['ts']) < after][:100]
            return {'data': [{'details': page}]}, None
        st = {'liq_last_ts': now - H}
        with tempfile.TemporaryDirectory() as tmp, patch.object(collector, 'BASE', tmp), \
             patch.object(collector, 'NOW', now), patch.object(collector, 'BACKFILL', True), \
             patch.object(collector, 'get', side_effect=get), patch.dict(collector.RUN, {'liq': {}}):
            collector.collect_liq(st)
            stored = storage.read_rows(Path(tmp) / 'data/liq/orders' / (collector.month(now) + '.jsonl'))
            self.assertIsNone(collector.RUN['liq']['err'])
        self.assertEqual(len(stored), 151)
        self.assertIn(999.0, {r['sz_contracts'] for r in stored})


class IsolationTests(unittest.TestCase):
    def test_one_series_exception_does_not_stop_the_rest(self):
        calls = []
        with patch.object(collector, 'binance_futures_data', return_value=([], None, 1)), \
             patch.object(collector, 'binance_funding', side_effect=KeyError('fundingRate')), \
             patch.object(collector, 'okx_backward', side_effect=lambda *a, **k: calls.append('okx') or ([], None, 1)), \
             patch.object(collector, 'get', return_value=({'data': []}, None)), \
             patch.object(collector, 'deribit_dvol', side_effect=lambda *a: calls.append('dvol') or ([], None)), \
             patch.dict(collector.RUN, {'series': {}}):
            self.assertTrue(collector.collect_series({'series': {}}))
            self.assertIn('KeyError', collector.RUN['series']['binance_funding_settled']['err'])
        self.assertEqual(calls, ['okx', 'okx', 'okx', 'dvol'])

    def test_http_4xx_keeps_the_venue_reason(self):
        body = json.dumps({'code': '40309', 'msg': 'The symbol has been removed'}).encode()
        err = urllib.error.HTTPError('u', 400, 'Bad Request', {}, io.BytesIO(body))
        with patch('collector.urllib.request.urlopen', side_effect=err):
            js, reason = collector.get('https://example.invalid')
        self.assertIsNone(js)
        self.assertIn('40309', reason)
        self.assertIn('removed', reason)


class ForwardBooksTests(unittest.TestCase):
    def test_deribit_options_daily_file(self):
        res = {'result': [
            {'instrument_name': 'BTC-24SEP26-90000-C', 'open_interest': 179.2, 'mark_iv': 41.7, 'underlying_price': 86151.2, 'creation_timestamp': START},
            {'instrument_name': 'BTC-24SEP26-80000-P', 'open_interest': 0, 'mark_iv': 50.0, 'underlying_price': 86151.2, 'creation_timestamp': START}]}
        with tempfile.TemporaryDirectory() as tmp, patch.object(collector, 'BASE', tmp), \
             patch.object(collector, 'NOW', START + H), patch.object(collector, 'get', return_value=(res, None)):
            out = collector.collect_deribit_options()
            row = storage.read_rows(Path(tmp) / 'data/options/deribit_btc/2026-01-01.jsonl')[0]
        self.assertEqual(out['with_oi'], 1)
        self.assertEqual(row['rows'], [['BTC-24SEP26-90000-C', 179.2, 41.7]])
        self.assertEqual(row['zero_oi_omitted'], 1)
        self.assertEqual(row['underlying'], {'24SEP26': 86151.2})

    def test_hl_positions_keep_btc_only_and_cache_ranking(self):
        board = {'leaderboardRows': [{'ethAddress': f'0x{i:040x}', 'accountValue': str(1000 - i)} for i in range(250)]}
        state = {'marginSummary': {'accountValue': '500'}, 'assetPositions': [
            {'position': {'coin': 'BTC', 'szi': '-2', 'entryPx': '75000', 'liquidationPx': '135000',
                          'leverage': {'type': 'cross', 'value': 5}, 'positionValue': '170000',
                          'unrealizedPnl': '-20000', 'marginUsed': '34000'}},
            {'position': {'coin': 'ETH', 'szi': '10'}}]}
        seen = []
        def get(url, body=None, **_):
            seen.append(url)
            return (board, None) if url == collector.HL_LEADERBOARD else (state, None)
        st = {}
        with tempfile.TemporaryDirectory() as tmp, patch.object(collector, 'BASE', tmp), \
             patch.object(collector, 'NOW', START), patch.object(collector, 'get', side_effect=get):
            out = collector.collect_hl_positions(st)
            with patch.object(collector, 'NOW', START + H):
                collector.collect_hl_positions(st)
            rows = storage.read_rows(Path(tmp) / 'data/hl_positions/btc/2026-01-01.jsonl')
        self.assertEqual(out['positions'], collector.HL_TOP_N)
        self.assertEqual(seen.count(collector.HL_LEADERBOARD), 1)          # second run used the cached ranking
        self.assertEqual(rows[0]['positions'][0][4], 135000.0)
        self.assertEqual(rows[0]['positions'][0][5], 'cross')
        self.assertEqual(st['hl_top']['addresses'][0], f'0x{0:040x}')     # ranked by account value


class ScoreTypeTests(unittest.TestCase):
    def base(self, event):
        return {'id': 'score-types', 'instrument': schema.INSTRUMENT, 'reference_price': 100,
                'start_utc': schema.iso(START), 'horizon_utc': schema.iso(START + H), 'events': [event]}

    def test_range_event_scored_in_log_units(self):
        fc = self.base({'type': 'range', 'q10': .05, 'q50': .1, 'q90': .2})
        self.assertEqual(schema.validate(fc), [])
        bars = [(START + i * M, 105., 95., 100.) for i in range(60)]
        result, _ = scoring.score(fc, bars, lambda n: [])
        realized = math.log(105 / 95)
        self.assertAlmostEqual(result[0]['realized_ln_range'], realized, 9)
        self.assertTrue(result[0]['covered_80'])
        self.assertAlmostEqual(result[0]['abs_log_error'], abs(math.log(.1) - math.log(realized)), 9)
        self.assertAlmostEqual(result[0]['pinball']['q50'], .5 * abs(realized - .1), 9)

    def test_range_quantiles_must_be_ordered(self):
        self.assertTrue(schema.validate(self.base({'type': 'range', 'q10': .2, 'q50': .1, 'q90': .3})))
        self.assertTrue(schema.validate(self.base({'type': 'range', 'q10': 0, 'q50': .1, 'q90': .3})))

    def test_interval_score(self):
        fc = self.base({'type': 'interval', 'lo': 101, 'hi': 110, 'coverage': .8})
        bars = [(START + i * M, 105., 95., 100.) for i in range(60)]
        result, _ = scoring.score(fc, bars, lambda n: [])
        self.assertFalse(result[0]['inside'])
        self.assertAlmostEqual(result[0]['interval_score'], 9 + (2 / .2) * 1, 6)


class WatchdogTests(unittest.TestCase):
    def test_silent_collector_fails_and_fresh_one_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(watchdog.check(tmp, START)[0], 1)
            storage.append_unique(Path(tmp) / 'data/runs/2026-01.jsonl',
                                  [{'t': START, 'mode': 'hourly', 'runner': 'github'},
                                   {'t': START + 5 * H, 'mode': 'backfill'}], lambda r: r['t'])
            self.assertEqual(watchdog.check(tmp, START + 2 * H)[0], 0)
            code, message = watchdog.check(tmp, START + 4 * H)   # a backfill run does not count as hourly
            self.assertEqual(code, 1)
            self.assertIn('silent', message)


if __name__ == '__main__':
    unittest.main()
