"""Regression cases from the October 23 audit; all writes are disposable fixtures."""
import copy
import datetime as dt
import io
import json
import math
from pathlib import Path
import socket
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'regression'), str(ROOT / 'desk')]
import feasibility as F
from research_tools import evidence_contract as E, evaluator_service as ES, research_api as RA
import test_rev229 as R
import test_rev230 as T
import test_rev212 as L
import range_job as J


class AttemptAvailabilityTests(unittest.TestCase):
    def test_real_budget_card_does_not_block_report_or_claim_zero_events(self):
        card = json.loads((ROOT / 'regression/fixtures/lab_budget_card.json').read_text())
        # Retained verbatim from 27ce3dd6, H1 at 2026-10-23T12:01Z.
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = base / 'research/evidence/v2/H1@fixture.json'
            path.parent.mkdir(parents=True)
            (path.parent.parent / 'index.json').write_text(json.dumps({'designs': {'H1': {'current': 'fixture'}}}))
            for status in ('not run', 'error'):
                with self.subTest(status=status):
                    path.write_text(json.dumps(dict(card, status=status)))
                    doc = F.build(base)
                    row = doc['lab'][0]
                    self.assertEqual(row['limiting_factor'], 'evaluation unavailable')
                    self.assertIsNone(row['time_to_checkpoint'])
                    self.assertNotIn('episodes_prospective', row)
                    self.assertNotIn('calendar_exposure', row)
                    self.assertIn('budget 1200 s exhausted', F.markdown(doc))
                    self.assertTrue(doc['streams'])
            path.write_text('{}')
            self.assertIn('unreadable', F.build(base)['lab'][0]['note'])

    def test_budget_exhaustion_is_nonzero_and_preserves_invalid_attempt_metadata(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict('os.environ', {'LAB_BUDGET': '-1'}):
            base = L.new_repo(tmp)
            rc, output, _ = L.lab_run(base, L.T0 + L.DAY, L.World())
            self.assertEqual(rc, 1)
            card = json.loads(next((base / 'research/evidence/v2').glob('*.json')).read_text())
            self.assertEqual(card['status'], 'not run')
            self.assertFalse(card['publication']['evaluation_valid'])
            self.assertIn('not run', output)

    def test_slow_account_design_runs_after_independent_designs(self):
        from lab import run as runner
        from lab import experiments as X
        designs = [dict(L.the_design(mod), id=name) for name, mod in
                   [('B9', 'account_behavior'), ('H9', 'deleveraging'), ('A9', 'flow_absorption')]]
        seen = []
        def attempt(lab, design, *args, **kwargs):
            seen.append(design['id'])
            raise RuntimeError('synthetic detector failure')
        with tempfile.TemporaryDirectory() as tmp, patch.object(X, 'design_files', return_value=designs), \
                patch.object(X, 'load_design', side_effect=lambda x: x), \
                patch.object(X, 'attach_version', side_effect=lambda b, d: d), \
                patch.object(X, 'run_design', side_effect=attempt), patch('sys.stdout', io.StringIO()):
            self.assertEqual(runner.main(['update', '--base', tmp, '--no-write', '--now', str(L.T0)]), 1)
        self.assertEqual(seen, ['H9', 'A9', 'B9'])


class FrozenExperimentTests(unittest.TestCase):
    def test_checkpoint_watermark_and_discovery_edits_are_refused(self):
        with tempfile.TemporaryDirectory() as shared, tempfile.TemporaryDirectory() as private:
            clock = R.Clock(T.T0 + 50 * T.H)
            researcher = RA.ResearchAPI(shared, T.shifted_provider(), 'researcher',
                                       {'kind': 'human', 'id': 'fixture'}, clock)
            service = ES.Service(shared, private, T.shifted_provider(), clock)
            researcher.open_experiment('X1', 'SYN', E.epoch_ms(T.T0 + 48 * T.H),
                                       {'checkpoints_n': [100]}, 'open')
            cand = researcher.register('X1', T.SPEC, 'register')
            service.handle({'op': 'anchor'})
            clock.t = T.T0 + 60 * T.H
            req = {'op': 'evaluate', 'experiment': 'X1', 'candidate_sha256': cand['candidate_sha256']}
            self.assertEqual(service.handle(dict(req, request_id='before'))['released'], [])
            path = Path(shared) / 'experiments/X1.json'
            frozen = json.loads(path.read_text())
            edits = [dict(frozen, disclosure={'checkpoints_n': [1]}),
                     dict(frozen, disclosure={'checkpoints_n': [100], 'label_watermark_min': 0}),
                     dict(frozen, discovery_cutoff_utc=E.iso(clock()))]
            for i, edited in enumerate(edits):
                path.write_text(json.dumps(edited))
                self.assertIn('frozen hypothesis', service.handle(dict(req, request_id=f'edited-{i}'))['refused'])
                self.assertEqual(service.api.ledger.verify(), [])
            path.write_text(json.dumps(frozen))
            clock.t = T.T0 + 100 * T.H
            released = service.handle(dict(req, request_id='valid'))['released']
            self.assertEqual([r['checkpoint_n'] for r in released], [100])
            # Removing the convenience copy cannot reset the policy or lose its definition.
            path.unlink()
            self.assertEqual(service.api._exp('X1'), frozen)
            with self.assertRaisesRegex(RA.Refused, 'another definition'):
                researcher.open_experiment('X1', 'SYN', E.epoch_ms(T.T0 + 48 * T.H),
                                           {'checkpoints_n': [1]}, 'reopen')
            self.assertEqual(service.api._exp('X1'), frozen)


class ServiceBoundaryTests(unittest.TestCase):
    def test_invalid_shapes_identifiers_and_missing_fields_are_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            svc = ES.Service(Path(tmp) / 'shared', Path(tmp) / 'private', lambda *a: {}, lambda: E.epoch_ms(T.T0))
            bad = [[], None, 1, {}, {'op': 'evaluate'}, {'op': 'released', 'experiment': '../private',
                   'candidate_sha256': 'a' * 64}, {'op': 'released', 'experiment': 'X1', 'candidate_sha256': '../x'},
                   {'op': 'evaluate', 'experiment': 'X1', 'candidate_sha256': 'a' * 64, 'request_id': []}]
            for req in bad:
                with self.subTest(req=req):
                    self.assertIn('error', svc.handle(req))
            self.assertIn('version', svc.handle({'op': 'ping'}))

    def test_bad_connections_do_not_kill_or_indefinitely_block_next_client(self):
        # A real local socket: malformed JSON, missing fields, oversized/stalled requests,
        # and an unexpected handler error must all be isolated from the next ping.
        with tempfile.TemporaryDirectory(prefix='ev-', dir='/tmp') as tmp:
            sock = str(Path(tmp) / 's')
            svc = ES.Service(Path(tmp) / 'shared', Path(tmp) / 'private', lambda *a: {}, lambda: E.epoch_ms(T.T0))
            original = svc.handle
            def handle(req):
                if req == {'op': 'fixture-failure'}:
                    raise RuntimeError('private detail must not escape')
                return original(req)
            svc.handle = handle
            errors = []
            def run():
                try:
                    ES.serve(svc, sock, max_requests=6, request_timeout=0.15, max_request_bytes=128)
                except Exception as exc:
                    errors.append(exc)
            worker = threading.Thread(target=run, daemon=True)
            worker.start()
            deadline = time.monotonic() + 5
            while not Path(sock).exists() and not errors and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertFalse(errors)
            for raw in (b'[]\n', b'{"op":"evaluate"}\n', b'x' * 129, b'{', b'{"op":"fixture-failure"}\n'):
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                    client.settimeout(2)
                    client.connect(sock)
                    client.sendall(raw)
                    reply = client.recv(4096)
                    self.assertIn(b'error', reply)
                    self.assertNotIn(b'private detail', reply)
            self.assertIn('version', ES.Client(sock).call({'op': 'ping'}))
            worker.join(3)
            self.assertFalse(worker.is_alive())
            self.assertFalse(errors)


class ReplayEquivalenceTests(unittest.TestCase):
    def test_only_finite_float_feature_roundoff_is_permitted(self):
        a = {'bars': [{'close': 80000.0}], 'decision_utc': '2026-10-01T00:00Z',
             'features': {'4h': {'b0': -3.0, 'count': 1, 'start_utc': '2026-10-01T00:20Z'}}}
        b = copy.deepcopy(a)
        b['features']['4h']['b0'] = math.nextafter(-3.0, 0)
        self.assertTrue(J.replay_bundle_matches(a, b))
        variants = []
        for value in (-3.001, float('nan'), float('inf'), -3, True):
            c = copy.deepcopy(a); c['features']['4h']['b0'] = value; variants.append(c)
        c = copy.deepcopy(a); c['bars'][0]['close'] += 1e-8; variants.append(c)
        c = copy.deepcopy(a); c['features']['4h']['start_utc'] = '2026-10-01T00:21Z'; variants.append(c)
        c = copy.deepcopy(a); c['features']['4h'].pop('count'); variants.append(c)
        for c in variants:
            self.assertFalse(J.replay_bundle_matches(a, c))


if __name__ == '__main__':
    unittest.main()
