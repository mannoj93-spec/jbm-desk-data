"""Regression tests for collector revision 2.6: 15-minute cadence and operational reliability.

Pins: the cadence transition (hourly history is not reported as three runs in four missing),
scheduled execution kept apart from snapshot coverage, delayed and manual runs, the watchdog's
three states, the routine run's time budget against the workflow's limits, bounded persistence,
the once-a-day liquidation boundary probe, run provenance, and rate-limit accounting.
Offline: every network call is simulated.
"""
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import cadence
import collector
import report
import schema
import storage
import watchdog
try:
    from test_rev22 import FakeClock, fake_binance              # unittest discover -s regression
except ImportError:
    from regression.test_rev22 import FakeClock, fake_binance

ROOT = Path(__file__).resolve().parent.parent
H = schema.H
M = schema.MINUTE
M5 = 5 * M
T0 = schema.ms('2026-01-01T00:00:00Z')          # hourly schedule starts
T1 = T0 + 10 * H                                   # 15-minute schedule starts
QUARTER = [7, 22, 37, 52]


def write_cadence(base, switch=T1):
    storage.atomic_json(Path(base) / 'cadence.json', {'periods': [
        {'from': '2026-01-01T00:00:00Z', 'minutes': [7], 'cron': '7 * * * *'},
        {'from': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(switch / 1000)), 'minutes': QUARTER,
         'cron': '7,22,37,52 * * * *'}]})


def run(t, trigger='schedule', **extra):
    rec = {'t': t, 'mode': 'routine', 'runner': 'github', 'trigger': trigger, 'critical_ok': True,
           'errors': {}, 'series': {}, 'liq': {}, 'snap': {'books_ok': 2, 'books': 2, 'failed': {}},
           'forward': {}, 'elapsed_s': 95.0, 'http': {'requests': 300, 'rate_limited': 0, 'rate_limited_by_host': {}}}
    rec.update(extra)
    return rec


def legacy(t):
    return {'t': t, 'mode': 'hourly', 'runner': 'github', 'critical_ok': True, 'errors': {}, 'series': {},
            'liq': {}, 'snap': {'books_ok': 2, 'books': 2}, 'elapsed_s': 100.0}


def snap(t, ok=True):
    return {'t': t, 'oi': {'a': {'st': 'ok'}, 'b': {'st': 'ok' if ok else 'error', 'err': 'HTTP 503'}}}


def store(base, runs=(), snaps=()):
    if runs:
        storage.append_unique(Path(base) / 'data/runs/2026-01.jsonl', list(runs), lambda r: (r['t'], r.get('trigger')))
    if snaps:
        storage.append_unique(Path(base) / 'data/snap/2026-01.jsonl', list(snaps), lambda r: r['t'])


def health(base, now):
    runs_all = sorted(storage.read_rows(Path(base) / 'data/runs/2026-01.jsonl'), key=lambda r: r['t'])
    snaps = sorted(storage.read_rows(Path(base) / 'data/snap/2026-01.jsonl'), key=lambda r: r['t'])
    since = now - 7 * 24 * H
    runs = [r for r in runs_all if since <= r['t'] <= now and cadence.is_routine(r)]
    return report.collection_health(runs_all, runs, snaps, cadence.load(base), since, now)


def table_rows(lines):
    return [l for l in lines if l.startswith('| 2026')]


class CadenceArithmeticTests(unittest.TestCase):
    def test_slots_follow_the_cadence_in_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_cadence(tmp)
            periods = cadence.load(tmp)
        self.assertEqual(len(cadence.slots(periods, T0, T1)), 10)                  # hourly at :07
        self.assertEqual(len(cadence.slots(periods, T1, T1 + 2 * H)), 8)           # four an hour
        self.assertEqual(len(cadence.slots(periods, T0, T1 + 2 * H)), 18)
        self.assertEqual((cadence.interval_minutes(periods, T1 - 1), cadence.interval_minutes(periods, T1)), (60, 15))
        self.assertEqual(cadence.slots(periods, T1, T1 + H)[:2], [T1 + 7 * M, T1 + 22 * M])

    def test_repository_cadence_matches_the_workflow_schedule(self):
        periods = cadence.load(ROOT)
        cron = re.search(r"cron: '([^']+)'", (ROOT / '.github/workflows/collect.yml').read_text()).group(1)
        self.assertEqual(cron, '7,22,37,52 * * * *')
        self.assertEqual(periods[-1][2], cron)
        self.assertEqual(periods[-1][1], QUARTER)
        self.assertEqual(periods[0][1], [7])                                      # the hourly history is kept


class CollectionHealthTests(unittest.TestCase):
    def test_hourly_history_is_not_reported_as_three_quarters_missing(self):
        now = T1 + 2 * H + 20 * M        # 11:52 due, 12:07 not yet (20-minute grace)
        with tempfile.TemporaryDirectory() as tmp:
            write_cadence(tmp)
            store(tmp, [legacy(T0 + h * H + 7 * M) for h in range(10)]
                       + [run(T1 + h * H + m * M) for h in range(2) for m in QUARTER],
                  [snap(T0 + h * H + 7 * M) for h in range(10)] + [snap(T1 + h * H + m * M) for h in range(2) for m in QUARTER])
            lines, alerts = health(tmp, now)
        hourly, quarter = table_rows(lines)
        self.assertIn('slots with a run: 10/10', hourly)
        self.assertIn('| 10 |', hourly)
        self.assertIn('| 8 | 8 (100%)', quarter)
        self.assertIn('8/8 slot intervals', quarter)
        self.assertEqual([a for a in alerts if 'missing' in a.lower() or 'stale' in a.lower()], [])

    def test_delayed_scheduled_runs_still_count_and_are_not_assigned_slots(self):
        now = T1 + 2 * H + 20 * M
        with tempfile.TemporaryDirectory() as tmp:
            write_cadence(tmp)
            # Every start 13 minutes late: the run for :52 starts at :05 of the next hour.
            starts = [T1 + h * H + m * M + 13 * M for h in range(2) for m in QUARTER]
            store(tmp, [run(t) for t in starts], [snap(t) for t in starts])
            lines, _ = health(tmp, now)
        quarter = table_rows(lines)[-1]
        self.assertIn('| 8 | 8 (100%)', quarter)
        self.assertTrue(any('Actual interval between scheduled starts' in l and 'median 15.0' in l for l in lines))

    def test_dropped_runs_show_in_scheduled_execution(self):
        now = T1 + 2 * H + 20 * M        # 11:52 due, 12:07 not yet (20-minute grace)
        with tempfile.TemporaryDirectory() as tmp:
            write_cadence(tmp)
            starts = [T1 + h * H + m * M + 2 * M for h in range(2) for m in QUARTER][:-2]   # last two dropped
            store(tmp, [run(t) for t in starts], [snap(t) for t in starts])
            lines, _ = health(tmp, now)
        quarter = table_rows(lines)[-1]
        self.assertIn('| 8 | 6 (75%)', quarter)
        self.assertIn('6/8 slot intervals', quarter)

    def test_manual_runs_fill_coverage_but_never_scheduled_execution(self):
        now = T1 + 2 * H + 20 * M        # 11:52 due, 12:07 not yet (20-minute grace)
        with tempfile.TemporaryDirectory() as tmp:
            write_cadence(tmp)
            sched = [T1 + h * H + m * M + 2 * M for h in range(2) for m in QUARTER]
            gone = sched.pop(3)                                    # the scheduler drops one slot
            manual = [gone + 5 * M] + [T1 + i * M for i in (9, 10, 11, 12)]   # a manual run fills it; four more
            store(tmp, [run(t) for t in sched] + [run(t, 'workflow_dispatch') for t in manual],
                  [snap(t) for t in sched + manual])
            lines, _ = health(tmp, now)
        quarter = table_rows(lines)[-1]
        self.assertIn('| 8 | 7 (88%)', quarter)                   # manual runs do not inflate it
        self.assertIn('8/8 slot intervals', quarter)              # but the data is held
        self.assertIn('workflow_dispatch 5', lines[0])

    def test_degraded_snapshots_and_source_failures_stay_visible_and_aggregate(self):
        now = T1 + 2 * H + 20 * M        # 11:52 due, 12:07 not yet (20-minute grace)
        with tempfile.TemporaryDirectory() as tmp:
            write_cadence(tmp)
            starts = [T1 + h * H + m * M for h in range(2) for m in QUARTER]
            failing = {'books_ok': 1, 'books': 2, 'failed': {'b': 'HTTP 503'}}
            store(tmp, [run(t, snap=failing) for t in starts[:6]] + [run(t) for t in starts[6:]],
                  [snap(t, ok=False) for t in starts[:6]] + [snap(t) for t in starts[6:]])
            lines, alerts = health(tmp, now)
        self.assertIn('| 6/8 |', table_rows(lines)[-1])
        grouped = [a for a in alerts if a.startswith('snapshot b')]
        self.assertEqual(len(grouped), 1)                          # one alert for six runs, not six
        self.assertIn('6/8 routine run(s)', grouped[0])
        self.assertIn('absent from the latest run', grouped[0])

    def test_rate_limits_runtime_and_budget_hits_are_reported(self):
        now = T1 + 2 * H
        with tempfile.TemporaryDirectory() as tmp:
            write_cadence(tmp)
            limited = {'requests': 300, 'rate_limited': 3, 'rate_limited_by_host': {'api.hyperliquid.xyz': 3}}
            store(tmp, [run(T1 + 7 * M, http=limited, elapsed_s=610.0, deadline_reached=True), run(T1 + 22 * M)],
                  [snap(T1 + 7 * M)])
            lines, alerts = health(tmp, now)
        self.assertTrue(any('api.hyperliquid.xyz 3' in l for l in lines))
        self.assertTrue(any('max 610' in l and '1 run(s) reached the network budget' in l for l in lines))
        self.assertTrue(any('rate limit api.hyperliquid.xyz' in a for a in alerts))
        self.assertTrue(any('reached the network budget' in a for a in alerts))

    def test_stale_collector_is_alerted_at_the_configured_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_cadence(tmp)
            store(tmp, [run(T1 + 7 * M), run(T1 + 100 * M, 'workflow_dispatch')], [snap(T1 + 7 * M)])
            _, alerts = health(tmp, T1 + 7 * M + 91 * M)
            self.assertTrue(any(a.startswith('Collector stale') for a in alerts))   # manual run does not reset it
            with patch.dict(os.environ, {'WATCHDOG_STALE_MIN': '120'}):
                _, alerts = health(tmp, T1 + 7 * M + 91 * M)
            self.assertFalse(any(a.startswith('Collector stale') for a in alerts))

    def test_full_report_builds_across_the_transition(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_cadence(tmp)
            store(tmp, [legacy(T0 + 7 * M), run(T1 + 7 * M)], [snap(T0 + 7 * M), snap(T1 + 7 * M)])
            (Path(tmp) / 'registry').mkdir()
            text = report.build(Path(tmp), T1 + H)
        self.assertIn('## 1. Collection health', text)
        self.assertIn('`7,22,37,52 * * * *`', text)
        self.assertIn('`7 * * * *`', text)


class WatchdogStateTests(unittest.TestCase):
    def check(self, runs, now, stale_min=90):
        with tempfile.TemporaryDirectory() as tmp:
            store(tmp, runs)
            return watchdog.check(tmp, now, stale_min)

    def test_missing_collector(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(watchdog.check(tmp, T1, 90)[0], 1)
        result = self.check([run(T1, 'workflow_dispatch')], T1 + M)
        self.assertEqual(result[0], 1)                            # manual runs are not the schedule
        self.assertIn('missing', result[1])

    def test_stale_after_the_limit_and_not_before(self):
        self.assertEqual(self.check([run(T1)], T1 + 89 * M)[0], 0)
        code, message = self.check([run(T1)], T1 + 91 * M)
        self.assertEqual(code, 1)
        self.assertIn('stale', message)
        self.assertEqual(self.check([run(T1)], T1 + 91 * M, stale_min=120)[0], 0)   # configurable

    def test_recent_manual_run_does_not_hide_a_dead_schedule(self):
        result = self.check([run(T1), run(T1 + 100 * M, 'workflow_dispatch')], T1 + 101 * M)
        self.assertEqual(result[0], 1)
        self.assertTrue(any('manual' in w for w in result.warnings))

    def test_running_but_failing_is_distinguished_from_stale(self):
        bad = run(T1 + 15 * M, critical_ok=False,
                  series={'binance_globalLongShortAccountRatio_5m': {'err': 'HTTP 503'}})
        code, message = self.check([run(T1), bad], T1 + 20 * M)
        self.assertEqual(code, 2)
        self.assertIn('running but failing', message)

    def test_source_failures_warn_without_failing(self):
        degraded = run(T1 + 15 * M, snap={'books_ok': 16, 'books': 17, 'failed': {'kraken': 'HTTP 502'}},
                       forward={'hl_positions': {'err': 'degraded: 3/200 accounts failed'}})
        result = self.check([run(T1), degraded], T1 + 20 * M)
        self.assertEqual(result[0], 0)
        self.assertTrue(any('snapshot kraken' in w for w in result.warnings))
        self.assertTrue(any('forward book hl_positions' in w for w in result.warnings))

    def test_pre_26_hourly_records_count_during_the_transition(self):
        self.assertEqual(self.check([legacy(T1)], T1 + 30 * M)[0], 0)

    def test_run_files_are_all_read_whatever_their_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            storage.append_unique(Path(tmp) / 'data/runs/2026-02.jsonl', [run(T1 - 30 * 24 * H)], lambda r: r['t'])
            storage.append_unique(Path(tmp) / 'data/runs/2026-01.jsonl', [run(T1)], lambda r: r['t'])
            self.assertEqual(watchdog.check(tmp, T1 + 10 * M, 90)[0], 0)

    def test_stale_limit_below_one_slot_is_refused(self):
        with patch.dict(os.environ, {'WATCHDOG_STALE_MIN': '10'}):
            with self.assertRaises(ValueError):
                cadence.stale_minutes()
        with patch.dict(os.environ, {'WATCHDOG_STALE_MIN': ''}):
            self.assertEqual(cadence.stale_minutes(), 90)

    def test_watchdog_schedule_and_limit_in_workflow(self):
        text = (ROOT / '.github/workflows/watchdog.yml').read_text()
        self.assertIn("cron: '17,47 * * * *'", text)
        self.assertIn("vars.WATCHDOG_STALE_MIN || '90'", text)


def workflow(name):
    return (ROOT / '.github/workflows' / name).read_text()


def pair(pattern, text):
    """(backfill, routine) from `inputs.backfill && X || Y`."""
    m = re.search(pattern + r"\$\{\{ inputs\.backfill && '?(\d+)'? \|\| '?(\d+)'? \}\}", text)
    return int(m.group(1)), int(m.group(2))


class WorkflowBudgetTests(unittest.TestCase):
    SETUP_MIN = 1          # checkout + setup-python, measured ~20-40 s on the hosted runner

    def test_routine_run_fits_inside_fifteen_minutes_with_persistence_reserved(self):
        text = workflow('collect.yml')
        job_backfill, job_routine = pair(r"    timeout-minutes: ", text)
        step_backfill, step_routine = pair(r"        timeout-minutes: ", text)
        budget_backfill, budget_routine = pair(r"COLLECTOR_BUDGET_S: ", text)
        persist_min = int(re.search(r"always\(\)\n        timeout-minutes: (\d+)", text).group(1))
        persist_budget = int(re.search(r"PERSIST_BUDGET_S: '(\d+)'", text).group(1))
        self.assertLess(job_routine, 15)
        self.assertEqual(budget_routine, 600)                                 # 10-minute network budget
        self.assertLessEqual(budget_routine + 60, step_routine * 60)          # writing after the deadline
        self.assertLessEqual(persist_budget + 15, persist_min * 60)
        self.assertLessEqual(self.SETUP_MIN + step_routine + persist_min, job_routine)
        self.assertGreaterEqual(job_routine * 60 - budget_routine - self.SETUP_MIN * 60, 180)   # minutes kept for persistence
        self.assertGreater(budget_backfill, budget_routine)
        self.assertLessEqual(budget_backfill + 60, step_backfill * 60)
        self.assertLessEqual(self.SETUP_MIN + step_backfill + persist_min, job_backfill)

    def test_writers_share_one_job_level_queue_and_scheduled_backlog_is_pruned(self):
        collect = workflow('collect.yml')
        head, jobs = collect.split('\njobs:\n')
        self.assertIn("github.event_name == 'schedule' && 'scheduled'", head)
        self.assertNotIn('queue: max', head)                        # default queue: one pending, newer replaces older
        self.assertIn('cancel-in-progress: false', head)
        for name in ('collect.yml', 'intake.yml', 'report.yml'):
            text = workflow(name)
            top, body = text.split('\njobs:\n')
            self.assertNotIn('repo-write', top, name)                # job level, so skipped jobs never queue
            self.assertRegex(body, r"concurrency:\n      group: repo-write\n      queue: max\n      cancel-in-progress: false", name)

    def test_manual_and_backfill_inputs_are_preserved(self):
        text = workflow('collect.yml')
        self.assertIn('workflow_dispatch:', text)
        self.assertIn('backfill:', text)
        self.assertIn('args+=(--backfill)', text)
        self.assertIn('if: always()', text)


class OutageCompletionTests(unittest.TestCase):
    def full_outage(self, tmp, budget):
        clock = FakeClock()
        (Path(tmp) / 'registry').mkdir()
        storage.atomic_json(Path(tmp) / 'state/checkpoints.json', {'series': {}, 'liq_last_ts': None})
        fresh = {'series': {}, 'liq': {}, 'snap': {}, 'errors': {},
                 'http': {'requests': 0, 'failed': 0, 'rate_limited': 0, 'rate_limited_by_host': {}, 'deadline_skipped': 0}}
        with clock.patches(budget), patch.object(collector, 'BASE', tmp), \
             patch.object(collector, 'STATE', str(Path(tmp) / 'state/checkpoints.json')), \
             patch.dict(collector.RUN, fresh), patch('sys.stdout', io.StringIO()):
            start = clock.t
            with self.assertRaises(SystemExit):
                collector.main()
            record = storage.read_rows(next((Path(tmp) / 'data/runs').glob('*.jsonl')))[0]
        return clock.t - start, clock.requests, record

    def test_sustained_outage_finishes_inside_the_budget_and_leaves_time_to_persist(self):
        text = workflow('collect.yml')
        _, job_routine = pair(r"    timeout-minutes: ", text)
        _, budget = pair(r"COLLECTOR_BUDGET_S: ", text)
        persist_min = int(re.search(r"always\(\)\n        timeout-minutes: (\d+)", text).group(1))
        with tempfile.TemporaryDirectory() as tmp:
            took, requests, record = self.full_outage(tmp, budget)
        self.assertLessEqual(took, budget + 30)
        self.assertGreater(requests, 0)
        self.assertTrue(record['deadline_reached'])
        self.assertFalse(record['critical_ok'])
        self.assertIn('deadline reached', json.dumps(record))                 # failures recorded, not lost
        self.assertGreater(record['http']['deadline_skipped'], 0)
        left = job_routine * 60 - WorkflowBudgetTests.SETUP_MIN * 60 - took
        self.assertGreaterEqual(left, persist_min * 60)                        # persistence still has its window


    def test_one_hung_venue_cannot_cost_every_venue_its_snapshot(self):
        clock = FakeClock()
        def fetch(req, timeout, stop):
            clock.requests += 1
            if 'binance' in req.full_url:
                clock.t += timeout
                raise TimeoutError('timed out')
            clock.t += 0.2
            return b'{}'
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'registry').mkdir()
            storage.atomic_json(Path(tmp) / 'state/checkpoints.json', {'series': {}, 'liq_last_ts': None})
            fresh = {'series': {}, 'liq': {}, 'snap': {}, 'errors': {}, 'forward': {},
                     'http': {'requests': 0, 'failed': 0, 'rate_limited': 0, 'rate_limited_by_host': {}, 'deadline_skipped': 0}}
            with clock.patches(600), patch.object(collector, 'fetch', side_effect=fetch), \
                 patch.object(collector, 'BASE', tmp), patch.object(collector, 'BACKFILL', False), \
                 patch.object(collector, 'RUN_BUDGET_S', 600), \
                 patch.object(collector, 'STATE', str(Path(tmp) / 'state/checkpoints.json')), \
                 patch.dict(collector.RUN, fresh), patch('sys.stdout', io.StringIO()):
                with self.assertRaises(SystemExit):
                    collector.main()
                record = storage.read_rows(next((Path(tmp) / 'data/runs').glob('*.jsonl')))[0]
                snapped = list((Path(tmp) / 'data/snap').glob('*.jsonl'))
        self.assertLessEqual(record['stage_s']['series'], 0.40 * 600 + 1)
        self.assertIn('series', record['stage_limited'])
        self.assertEqual(len(snapped), 1)                                   # the snapshot was still taken
        self.assertGreater(record['snap']['books_ok'] + len(record['snap']['failed']), 0)
        for name, status in record['forward'].items():                      # forward books were attempted
            self.assertNotIn('deadline reached', str(status.get('err')), name)


class PersistenceBudgetTests(unittest.TestCase):
    def test_hung_remote_cannot_hold_persistence_past_its_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / 'git'
            fake.write_text('#!/usr/bin/env bash\ncase "$1" in\n  push|pull) sleep 30 ;;\n'
                            '  symbolic-ref) echo main ;;\n  *) exit 0 ;;\nesac\n')
            fake.chmod(0o755)
            env = dict(os.environ, PATH=f"{tmp}:{os.environ['PATH']}", PERSIST_BUDGET_S='8')
            started = time.monotonic()
            proc = subprocess.run(['bash', str(ROOT / 'scripts/commit_push.sh'), 'data'], cwd=tmp, env=env,
                                  capture_output=True, text=True, timeout=60)
            took = time.monotonic() - started
        self.assertEqual(proc.returncode, 1)
        self.assertLess(took, 20)                                              # four 30 s pushes would be 120+
        self.assertIn('remote persistence not confirmed', proc.stderr)

    def test_successful_push_still_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / 'git'
            fake.write_text('#!/usr/bin/env bash\ncase "$1" in\n  symbolic-ref) echo main ;;\n  *) exit 0 ;;\nesac\n')
            fake.chmod(0o755)
            env = dict(os.environ, PATH=f"{tmp}:{os.environ['PATH']}")
            proc = subprocess.run(['bash', str(ROOT / 'scripts/commit_push.sh'), 'data'], cwd=tmp, env=env,
                                  capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)


def liq_page(ts):
    return {'data': [{'details': [{'ts': str(t), 'posSide': 'long', 'side': 'sell', 'sz': '1', 'bkPx': '60000'}
                                  for t in ts]}]}


class LiquidationProbeTests(unittest.TestCase):
    def run_liq(self, tmp, st, now):
        calls = []
        def get(url, **_):
            calls.append(url)
            return (liq_page([now - 60_000, now - 2 * H]) if 'after=' not in url else {'data': []}), None
        with patch.object(collector, 'BASE', tmp), patch.object(collector, 'NOW', now), \
             patch.object(collector, 'BACKFILL', False), patch.object(collector, 'get', side_effect=get), \
             patch.dict(collector.RUN, {'liq': {}}):
            collector.collect_liq(st)
            return dict(collector.RUN['liq']), calls

    def test_boundary_probe_runs_once_per_utc_day_not_every_quarter_hour(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = {'series': {}, 'liq_last_ts': T1 - H}
            probes = [self.run_liq(tmp, st, T0 + i * 15 * M)[0]['probe'] for i in range(4)]   # 00:00-00:45
            later = self.run_liq(tmp, st, T0 + 13 * H)[0]['probe']
            next_day = self.run_liq(tmp, st, T0 + 24 * H + 7 * M)[0]['probe']
            bounds = storage.read_rows(Path(tmp) / 'data/liq/boundary/2026-01.jsonl')
        self.assertEqual(probes, [True, False, False, False])
        self.assertFalse(later)
        self.assertTrue(next_day)
        self.assertEqual(len(bounds), 2)

    def test_failed_probe_is_retried_on_the_next_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = {'series': {}, 'liq_last_ts': T0 - H}
            with patch.object(collector, 'BASE', tmp), patch.object(collector, 'NOW', T0 + 7 * M), \
                 patch.object(collector, 'get', return_value=(None, 'HTTP 503')), patch.dict(collector.RUN, {'liq': {}}):
                collector.collect_liq(st)
            self.assertNotIn('liq_probe_day', st)
            self.assertTrue(self.run_liq(tmp, st, T0 + 22 * M)[0]['probe'])


class ProvenanceAndAccountingTests(unittest.TestCase):
    def run_record(self, env, *args):
        code = 'import collector, json; print(json.dumps(collector.RUN))'
        env = {k: v for k, v in os.environ.items() if not k.startswith(('GITHUB_', 'COLLECTOR_', 'SCHEDULE_'))} | env
        out = subprocess.run([sys.executable, '-c', code, *args], cwd=ROOT, env=env, capture_output=True, text=True, check=True)
        return json.loads(out.stdout)

    def test_trigger_schedule_and_budget_are_recorded(self):
        rec = self.run_record({'GITHUB_ACTIONS': 'true', 'GITHUB_EVENT_NAME': 'schedule',
                               'SCHEDULE_CRON': '7,22,37,52 * * * *', 'GITHUB_RUN_ID': '42', 'COLLECTOR_BUDGET_S': '600'})
        self.assertEqual((rec['mode'], rec['trigger'], rec['schedule'], rec['run_id'], rec['budget_s']),
                         ('routine', 'schedule', '7,22,37,52 * * * *', '42', 600))
        manual = self.run_record({'GITHUB_ACTIONS': 'true', 'GITHUB_EVENT_NAME': 'workflow_dispatch'})
        self.assertEqual((manual['trigger'], manual['schedule']), ('workflow_dispatch', None))
        self.assertFalse(cadence.schedule_evidence(dict(manual, t=0)))
        local = self.run_record({})
        self.assertEqual((local['trigger'], local['budget_s']), ('local', 600))
        backfill = self.run_record({}, '--backfill')
        self.assertEqual((backfill['mode'], backfill['budget_s']), ('backfill', 1800))

    def test_rate_limits_are_counted_by_host(self):
        fresh = {'requests': 0, 'failed': 0, 'rate_limited': 0, 'rate_limited_by_host': {}, 'deadline_skipped': 0}
        with patch.dict(collector.RUN, {'http': fresh}), \
             patch.object(collector, 'fetch', side_effect=collector.HTTPFailure(429, b'{}')), \
             patch('collector.time.sleep'):
            js, err = collector.get('https://api.hyperliquid.xyz/info', tries=2)
            counts = dict(collector.RUN['http'])
        self.assertEqual(err, 'HTTP 429')
        self.assertEqual((counts['requests'], counts['rate_limited']), (2, 2))
        self.assertEqual(counts['rate_limited_by_host'], {'api.hyperliquid.xyz': 2})

    def test_okx_rate_limit_body_is_counted(self):
        fresh = {'requests': 0, 'failed': 0, 'rate_limited': 0, 'rate_limited_by_host': {}, 'deadline_skipped': 0}
        with patch.dict(collector.RUN, {'http': fresh}), \
             patch.object(collector, 'fetch', return_value=b'{"code": "50011", "msg": "Too Many Requests"}'):
            collector.get('https://www.okx.com/api/v5/x')
            self.assertEqual(collector.RUN['http']['rate_limited_by_host'], {'www.okx.com': 1})


class NativeResolutionTests(unittest.TestCase):
    def test_quarter_hour_runs_keep_native_5m_and_1h_rows_without_duplicates(self):
        stamps5 = [T0 + i * M5 for i in range(24 * 12)]
        stamps1 = [T0 + i * H for i in range(24)]
        with tempfile.TemporaryDirectory() as tmp, patch.object(collector, 'BASE', tmp):
            ck = {}
            for now in (T0 + 10 * H + 7 * M, T0 + 10 * H + 22 * M, T0 + 10 * H + 37 * M, T0 + 10 * H + 52 * M,
                        T0 + 11 * H + 7 * M):
                for name, stamps, step in (('binance_topLongShortPositionRatio_5m', stamps5, M5),
                                           ('binance_topLongShortPositionRatio_1h', stamps1, H)):
                    with patch.object(collector, 'NOW', now), \
                         patch.object(collector, 'get', side_effect=fake_binance([t for t in stamps if t <= now], False, step)):
                        rows, err, _ = collector.binance_futures_data(name, 'x', '5m' if step == M5 else '1h',
                                                                      ['buySellRatio'], ck.get(name))
                    self.assertIsNone(err)
                    if rows:
                        collector.append_rows(f'series/{name}', rows)
                        ck[name] = rows[-1]['t']
            five = [r['t'] for r in storage.read_rows(Path(tmp) / 'data/series/binance_topLongShortPositionRatio_5m/2026-01.jsonl')]
            hour = [r['t'] for r in storage.read_rows(Path(tmp) / 'data/series/binance_topLongShortPositionRatio_1h/2026-01.jsonl')]
        self.assertEqual(len(five), len(set(five)))
        self.assertEqual(five, list(range(five[0], five[-1] + M5, M5)))             # every 5m stamp, once
        self.assertEqual(hour, list(range(hour[0], hour[-1] + H, H)))               # hourly stays hourly
        self.assertEqual(hour[-1], T0 + 11 * H)


if __name__ == '__main__':
    unittest.main()
