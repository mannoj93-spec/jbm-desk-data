"""Regression tests for reliability revision 2.2 (2026-09-23 audit).

Each test reproduces a defect measured against the live sources, or pins a new contract.
Offline: every network call is simulated.
"""
import io
import json
import math
import os
import socket
import threading
import time
from pathlib import Path
import tempfile
import unittest
import urllib.error
from contextlib import ExitStack, contextmanager
from unittest.mock import patch

import collector
import research
import schema
import scoring
import report
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

    def test_backfill_boundary_400_with_reason_still_ends_history(self):
        # Found on the first GitHub backfill of 2.2: the detailed 400 no longer equalled "HTTP 400".
        page = [{'timestamp': i * M5, 'sumOpenInterest': '1', 'sumOpenInterestValue': '1'} for i in range(500, 1000)]
        boundary = (None, "HTTP 400 (binance code -1130: parameter 'endTime' is invalid.)")
        with patch.object(collector, 'NOW', 1000 * M5), patch.object(collector, 'get', side_effect=[(page, None), boundary]):
            rows, err, _ = collector.binance_futures_data('binance_openInterestHist_5m', 'openInterestHist', '5m',
                                                          ['sumOpenInterest', 'sumOpenInterestValue'], None)
        self.assertIsNone(err)
        self.assertEqual(len(rows), 500)

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
        # Median error in the forecast's own units (review of ed45dd2): |q50 - realized|.
        self.assertAlmostEqual(result[0]['abs_error_lr'], abs(.1 - realized), 9)
        # runbook E2's primary loss is on ln(lr), the scale its baselines are fitted on; kept, renamed.
        self.assertAlmostEqual(result[0]['abs_error_log_lr'], abs(math.log(.1) - math.log(realized)), 9)
        x = (realized / .1) ** 2
        self.assertAlmostEqual(result[0]['qlike'], x - math.log(x) - 1, 9)
        self.assertAlmostEqual(result[0]['pinball']['q50'], .5 * abs(realized - .1), 9)
        self.assertNotIn('abs_log_error', result[0])

    def test_range_quantiles_must_be_ordered(self):
        self.assertTrue(schema.validate(self.base({'type': 'range', 'q10': .2, 'q50': .1, 'q90': .3})))
        self.assertTrue(schema.validate(self.base({'type': 'range', 'q10': 0, 'q50': .1, 'q90': .3})))

    def test_interval_score(self):
        fc = self.base({'type': 'interval', 'lo': 101, 'hi': 110, 'coverage': .8})
        bars = [(START + i * M, 105., 95., 100.) for i in range(60)]
        result, _ = scoring.score(fc, bars, lambda n: [])
        self.assertFalse(result[0]['inside'])
        self.assertAlmostEqual(result[0]['interval_score'], 9 + (2 / .2) * 1, 6)



class RangeReportTests(unittest.TestCase):
    def test_range_line_shows_every_score_and_never_bare_none(self):
        fc = {'id': 'range-report', 'instrument': schema.INSTRUMENT, 'reference_price': 100,
              'start_utc': schema.iso(START), 'horizon_utc': schema.iso(START + H),
              'events': [{'name': '1h range', 'type': 'range', 'q10': .05, 'q50': .1, 'q90': .2}]}
        bars = [(START + i * M, 105., 95., 100.) for i in range(60)]
        result, _ = scoring.score(fc, bars, lambda n: [])
        line = report.format_event(result[0])
        for part in ('realized ln(H/L) 0.10008', 'inside q10-q90: True', 'pinball', '|q50 - realized| 0.00008',
                     '(E2 primary)', 'QLIKE'):
            self.assertIn(part, line)
        self.assertNotEqual(line.rstrip('.').split(': ', 1)[1], 'None')

    def test_interval_line_shows_score(self):
        line = report.format_event({'name': 'iv', 'type': 'interval', 'inside': False, 'nominal': .8,
                                    'realized': 100.0, 'interval_score': 19.0})
        self.assertIn('interval score 19.00', line)


def hl_board(n=200):
    return {'leaderboardRows': [{'ethAddress': f'0x{i:040x}', 'accountValue': str(1000 - i)} for i in range(n)]}


GOOD_ACCOUNT = {'marginSummary': {'accountValue': '500'}, 'assetPositions': [
    {'position': {'coin': 'BTC', 'szi': '-2', 'entryPx': '75000', 'liquidationPx': '135000',
                  'leverage': {'type': 'cross', 'value': 5}, 'positionValue': '170000',
                  'unrealizedPnl': '-20000', 'marginUsed': '34000'}}]}


class ForwardValidationTests(unittest.TestCase):
    """Cases reproduced in the review of ed45dd2."""

    def run_hl(self, account):
        def get(url, body=None, **_):
            return (hl_board(), None) if url == collector.HL_LEADERBOARD else account(body['user'])
        with tempfile.TemporaryDirectory() as tmp, patch.object(collector, 'BASE', tmp), \
             patch.object(collector, 'NOW', START), patch.object(collector, 'get', side_effect=get):
            try:
                out = collector.collect_hl_positions({})
            except RuntimeError as exc:
                out = {'raised': str(exc)}
            path = Path(tmp) / 'data/hl_positions/btc/2026-01-01.jsonl'
            rows = storage.read_rows(path) if path.exists() else []
        return out, rows

    def test_empty_object_is_a_failed_account_not_an_empty_one(self):
        first = f'0x{0:040x}'
        out, rows = self.run_hl(lambda user: ({}, None) if user == first else (GOOD_ACCOUNT, None))
        self.assertEqual(out['status'], 'degraded')
        self.assertEqual(out['accounts_failed'], 1)
        self.assertIn('degraded', out['err'])
        self.assertEqual(rows[0]['status'], 'degraded')
        self.assertEqual(rows[0]['failed'][0][0], first)
        self.assertEqual(len(rows[0]['positions']), 199)

    def test_half_failed_is_not_stored(self):
        out, rows = self.run_hl(lambda user: (None, 'HTTP 500') if int(user, 16) % 2 else (GOOD_ACCOUNT, None))
        self.assertIn('100/200', out['raised'])
        self.assertEqual(rows, [])

    def test_all_good_is_complete(self):
        out, rows = self.run_hl(lambda user: (GOOD_ACCOUNT, None))
        self.assertEqual((out['status'], out['err'], rows[0]['status']), ('complete', None, 'complete'))

    def test_malformed_btc_position_fails_the_account(self):
        bad = {'marginSummary': {'accountValue': '1'}, 'assetPositions': [{'position': {'coin': 'BTC', 'szi': '1'}}]}
        with self.assertRaises(ValueError):
            collector.hl_account(bad)
        null_liq = json.loads(json.dumps(GOOD_ACCOUNT))
        null_liq['assetPositions'][0]['position']['liquidationPx'] = None     # documented: no liquidation price
        self.assertIsNone(collector.hl_account(null_liq)[1][0][3])

    def deribit(self, rows):
        with tempfile.TemporaryDirectory() as tmp, patch.object(collector, 'BASE', tmp), \
             patch.object(collector, 'NOW', START), patch.object(collector, 'get', return_value=({'result': rows}, None)):
            try:
                out = collector.collect_deribit_options()
            except ValueError as exc:
                out = {'raised': str(exc)}
            path = Path(tmp) / 'data/options/deribit_btc/2026-01-01.jsonl'
            stored = storage.read_rows(path) if path.exists() else []
        return out, stored

    @staticmethod
    def option(strike, iv=40.0):
        row = {'instrument_name': f'BTC-24SEP26-{strike}-C', 'open_interest': 10, 'underlying_price': 86000.0,
               'creation_timestamp': START}
        if iv is not None:
            row['mark_iv'] = iv
        return row

    def test_missing_mark_iv_is_excluded_and_degrades(self):
        rows = [self.option(80000 + 100 * i) for i in range(40)] + [self.option(99000, iv=None)]
        out, stored = self.deribit(rows)
        self.assertEqual((out['status'], out['with_oi'], out['excluded']), ('degraded', 40, 1))
        self.assertIn('degraded', out['err'])
        self.assertEqual(stored[0]['excluded'], [['BTC-24SEP26-99000-C', 'mark_iv']])
        self.assertNotIn('BTC-24SEP26-99000-C', {r[0] for r in stored[0]['rows']})

    def test_many_invalid_rows_are_not_stored(self):
        rows = [self.option(80000 + 100 * i) for i in range(10)] + [self.option(99000, iv=None)]
        out, stored = self.deribit(rows)
        self.assertIn('not stored', out['raised'])
        self.assertEqual(stored, [])



class FakeClock:
    """Simulated sustained outage: every request hangs for its full socket timeout."""
    def __init__(self):
        self.t, self.requests = 1_000_000.0, 0

    def time(self):
        return self.t

    def sleep(self, seconds):
        self.t += max(0.0, seconds)

    def hang(self, req, timeout=None, **_):
        self.requests += 1
        self.t += timeout
        raise socket.timeout('timed out')

    def patches(self, budget=None):
        budget = getattr(collector, 'RUN_BUDGET_S', 1200) if budget is None else budget
        # Deadlines are on time.monotonic() from 2.5 (time.time() before); the fake drives both.
        return self._patched(budget)

    @contextmanager
    def _patched(self, budget):
        # Entered only by `with`, so a failing test can never leave the fake clock installed.
        with ExitStack() as stack:
            for cm in (patch('collector.time.monotonic', self.time), patch('collector.time.time', self.time),
                       patch('collector.time.sleep', self.sleep),
                       patch('collector.urllib.request.urlopen', side_effect=self.hang),
                       patch.object(collector, 'DEADLINE', self.t + budget, create=True)):
                stack.enter_context(cm)
            yield


def cached_top(n=200):
    return {'hl_top': {'t': collector.NOW, 'addresses': [f'0x{i:040x}' for i in range(n)],
                       'min_account_value': 1.0, 'rank_basis': 'test'}}


class OutageBudgetTests(unittest.TestCase):
    """2.3 made 400 Hyperliquid requests in a sustained outage (~190 simulated minutes) and a full
    all-venue outage ran ~285 simulated minutes; the workflow kills the job at 30."""

    def test_hl_sustained_outage_stops_at_its_budget(self):
        clock = FakeClock()
        with clock.patches(), tempfile.TemporaryDirectory() as tmp, patch.object(collector, 'BASE', tmp):
            start = clock.t
            with self.assertRaises(RuntimeError) as ctx:
                collector.collect_hl_positions(cached_top())
        self.assertLessEqual(clock.t - start, getattr(collector, 'HL_BUDGET_S', 300) + 1)
        self.assertLess(clock.requests, 40)
        self.assertIn('stopped: deadline', str(ctx.exception))

    def test_fast_failures_stop_once_rejection_is_inevitable(self):
        calls = []
        def get(url, body=None, **_):
            calls.append(body['user'])
            return None, 'HTTP 503'
        with tempfile.TemporaryDirectory() as tmp, patch.object(collector, 'BASE', tmp), \
             patch.object(collector, 'get', side_effect=get):
            with self.assertRaises(RuntimeError) as ctx:
                collector.collect_hl_positions(cached_top())
        self.assertEqual(len(calls), 100)                  # 100 of 200 failed: the rest cannot save the map
        self.assertIn('rejection inevitable', str(ctx.exception))

    def test_deadline_with_most_accounts_done_stores_a_degraded_map(self):
        clock = FakeClock()
        def get(url, body=None, **_):
            clock.t += getattr(collector, 'HL_BUDGET_S', 300) / 150    # the budget runs out after 150 accounts
            return GOOD_ACCOUNT, None
        with patch('collector.time.monotonic', clock.time), patch('collector.time.time', clock.time), \
             patch.object(collector, 'get', side_effect=get), \
             tempfile.TemporaryDirectory() as tmp, patch.object(collector, 'BASE', tmp), patch.object(collector, 'NOW', START):
            out = collector.collect_hl_positions(cached_top())
            row = storage.read_rows(Path(tmp) / 'data/hl_positions/btc/2026-01-01.jsonl')[0]
        self.assertEqual((out['status'], out['stopped'], out['accounts_failed']), ('degraded', 'deadline', 50))
        self.assertEqual(row['failed'][0][1], 'not attempted: deadline')
        self.assertEqual(len(row['positions']), 150)

    def test_rate_limited_account_is_retried_after_a_backoff(self):
        seen = []
        def get(url, body=None, **_):
            seen.append(body['user'])
            return (None, 'HTTP 429') if seen.count(body['user']) == 1 and len(seen) == 1 else (GOOD_ACCOUNT, None)
        with tempfile.TemporaryDirectory() as tmp, patch.object(collector, 'BASE', tmp), \
             patch.object(collector, 'NOW', START), patch.object(collector, 'get', side_effect=get), \
             patch('collector.time.sleep') as sleep:
            out = collector.collect_hl_positions(cached_top())
        self.assertEqual((out['status'], out['rate_limited'], len(seen)), ('complete', 1, 201))
        sleep.assert_called_once()

    def test_get_issues_no_request_after_the_run_deadline(self):
        clock = FakeClock()
        with clock.patches(budget=0):
            js, err = collector.get('https://example.invalid')
        self.assertEqual((js, clock.requests), (None, 0))
        self.assertIn('deadline', err)

    def test_get_caps_timeout_and_retry_pause_at_the_deadline(self):
        clock = FakeClock()
        with clock.patches(budget=30):
            start = clock.t
            collector.get('https://example.invalid')        # 4 tries of 25 s + pauses would be 126 s
        self.assertLessEqual(clock.t - start, 30)

    def test_full_outage_run_finishes_inside_the_workflow_limit_and_keeps_its_record(self):
        clock = FakeClock()
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'registry').mkdir()
            storage.atomic_json(Path(tmp) / 'state/checkpoints.json', {'series': {}, 'liq_last_ts': None})
            with clock.patches(), patch.object(collector, 'BASE', tmp), \
                 patch.object(collector, 'STATE', str(Path(tmp) / 'state/checkpoints.json')), \
                 patch.dict(collector.RUN, {'series': {}, 'liq': {}, 'snap': {}, 'errors': {}}), \
                 patch('sys.stdout', io.StringIO()):
                start = clock.t
                with self.assertRaises(SystemExit):
                    collector.main()
                runs = list((Path(tmp) / 'data/runs').glob('*.jsonl'))
        budget = getattr(collector, 'RUN_BUDGET_S', 1200)
        self.assertLessEqual(clock.t - start, budget + 60)
        self.assertLess(budget + 60, 30 * 60)                      # the workflow's timeout-minutes
        self.assertEqual(len(runs), 1)



class TricklingServer:
    """A local HTTP server that sends its response one byte at a time. Every byte resets a socket
    timeout, so only a limit on the whole request can stop it (review of 2.4: 3.01 s taken and the
    response accepted against a 1.2 s budget)."""

    def __init__(self, phase, status=200, delay=0.07):
        self.phase, self.status, self.delay = phase, status, delay
        self.body = json.dumps({'ok': 1, 'pad': 'x' * 40}).encode()
        self.sock = socket.socket()
        self.sock.bind(('127.0.0.1', 0))
        self.sock.listen(8)
        self.url = f'http://127.0.0.1:{self.sock.getsockname()[1]}/x'
        threading.Thread(target=self.serve, daemon=True).start()

    def serve(self):
        while True:
            try:
                conn, _ = self.sock.accept()
            except OSError:
                return
            try:
                conn.recv(65536)
                reason = {200: b'OK', 503: b'Service Unavailable'}[self.status]
                head = b'HTTP/1.1 %d %s\r\nContent-Type: application/json\r\nContent-Length: %d\r\n\r\n' % (
                    self.status, reason, len(self.body))
                slow, fast = (head, self.body) if self.phase == 'headers' else (b'', head)
                conn.sendall(fast if self.phase != 'headers' else b'')
                for chunk in (slow, self.body if self.phase != 'headers' else b''):
                    for byte in chunk:
                        conn.sendall(bytes([byte]))
                        time.sleep(self.delay)
                if self.phase == 'headers':
                    conn.sendall(self.body)
            except OSError:
                pass
            finally:
                conn.close()

    def close(self):
        self.sock.close()


class SlowResponseTests(unittest.TestCase):
    """Real sockets on 127.0.0.1; each case sets a 1.2 s budget."""
    BUDGET = 1.2

    def run_get(self, server):
        now = time.monotonic() if collector.CODE_VERSION >= 'collector-2.5' else time.time()
        with patch.object(collector, 'DEADLINE', now + self.BUDGET, create=True), \
             patch.dict(os.environ, {'no_proxy': '127.0.0.1,localhost', 'NO_PROXY': '127.0.0.1,localhost'}):
            started = time.monotonic()
            js, err = collector.get(server.url, tries=1)
            return js, err, time.monotonic() - started

    def check_stopped(self, phase, status=200):
        server = TricklingServer(phase, status)
        self.addCleanup(server.close)
        js, err, took = self.run_get(server)
        self.assertLess(took, self.BUDGET + 0.3, f'{phase}: took {took:.2f}s')
        self.assertIsNone(js)                                   # never accepted after the deadline
        self.assertIn('deadline', err)

    def test_trickled_body_is_abandoned_at_the_deadline(self):
        self.check_stopped('body')

    def test_trickled_headers_are_abandoned_at_the_deadline(self):
        self.check_stopped('headers')

    def test_trickled_error_body_is_abandoned_at_the_deadline(self):
        self.check_stopped('body', status=503)

    def test_slow_dns_lookup_is_abandoned_at_the_deadline(self):
        # A resolver stall happens before any socket exists, so no socket timeout applies to it.
        real = socket.getaddrinfo
        def stalled(*args, **kwargs):
            time.sleep(3)
            return real(*args, **kwargs)
        server = TricklingServer('body', delay=0)
        self.addCleanup(server.close)
        with patch('socket.getaddrinfo', stalled):
            js, err, took = self.run_get(server)
        self.assertLess(took, self.BUDGET + 0.3)
        self.assertIsNone(js)
        self.assertIn('deadline', err)

    def late_byte_server(self, status):
        """Headers at once, one body byte 0.1 s before the deadline, then a 5 s stall (review of 2.5:
        a stalled 503 held the caller 2.11 s against 1.2 s, because the abort could not reach the
        socket under HTTPError and close() then waited behind the worker's receive)."""
        sock = socket.socket()
        sock.bind(('127.0.0.1', 0))
        sock.listen(4)
        self.addCleanup(sock.close)

        def serve():
            conn, _ = sock.accept()
            try:
                conn.recv(65536)
                reason = b'OK' if status == 200 else b'Service Unavailable'
                conn.sendall(b'HTTP/1.1 %d %s\r\nContent-Type: application/json\r\nContent-Length: 100\r\n\r\n'
                             % (status, reason))
                time.sleep(self.BUDGET - 0.1)
                conn.sendall(b'{')
                time.sleep(5)
            except OSError:
                pass
            finally:
                conn.close()
        threading.Thread(target=serve, daemon=True).start()
        return f'http://127.0.0.1:{sock.getsockname()[1]}/x'

    def check_released(self, status):
        before = {t for t in threading.enumerate() if t.name == 'collector-fetch'}
        url = self.late_byte_server(status)
        js, err, took = self.run_get(type('S', (), {'url': url})())
        self.assertLess(took, self.BUDGET + 0.15, f'{status}: took {took:.2f}s')
        self.assertIsNone(js)
        self.assertIn('deadline', err)
        # The shutdown reached the socket: the abandoned worker ends promptly, not at its timeout.
        workers = [t for t in threading.enumerate() if t.name == 'collector-fetch' and t not in before]
        for worker in workers:
            worker.join(0.5)
        self.assertFalse(any(w.is_alive() for w in workers), f'{status}: worker still blocked')

    def test_stalled_error_body_is_released_at_the_deadline(self):
        self.check_released(503)

    def test_stalled_body_is_released_at_the_deadline(self):
        self.check_released(200)

    def test_prompt_response_still_succeeds(self):
        server = TricklingServer('body', delay=0)
        self.addCleanup(server.close)
        js, err, took = self.run_get(server)
        self.assertEqual((js, err), ({'ok': 1, 'pad': 'x' * 40}, None))
        self.assertLess(took, 1.0)


class WatchdogTests(unittest.TestCase):
    def test_silent_collector_fails_and_fresh_one_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(watchdog.check(tmp, START)[0], 1)
            storage.append_unique(Path(tmp) / 'data/runs/2026-01.jsonl',
                                  [{'t': START, 'mode': 'hourly', 'runner': 'github'},
                                   {'t': START + 5 * H, 'mode': 'backfill'}], lambda r: r['t'])
            # 2.6: the limit is 90 minutes (WATCHDOG_STALE_MIN), not three hours.
            self.assertEqual(watchdog.check(tmp, START + 80 * schema.MINUTE)[0], 0)
            code, message = watchdog.check(tmp, START + 4 * H)   # a backfill run does not count as hourly
            self.assertEqual(code, 1)
            self.assertIn('silent', message)


if __name__ == '__main__':
    unittest.main()
