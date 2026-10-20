"""Repo 2.29: shared evidence contract parity, report-tail classification, catalog, admission funnel, continuous
panel, research interface and search ledger, prospective directional stream, calibration, turnover control, raw
archive replay, D1 diagnostics, E1 pilot acceptance and the O33 v3.1 manifest.

Every fixture here is synthetic and offline. A fixture run is never a live run, a fixture receipt is never a registry
write, and nothing here says a venue returned these values."""
import datetime as dt
import gzip
import hashlib
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import cadence  # noqa: E402
import report  # noqa: E402
import schema  # noqa: E402
from research_tools import archive_store, calibration, catalog, d1_diagnostics, directional as DIR, funnel, panel  # noqa: E402
from research_tools import evidence_contract as E  # noqa: E402
from lab.data import Store  # noqa: E402
from research_tools.research_api import ResearchAPI, Refused, verify_results  # noqa: E402
from research_tools.search_ledger import Ledger  # noqa: E402
from research_tools import turnover  # noqa: E402
from stream import pilot_acceptance  # noqa: E402

MIN = 60_000
H = 60 * MIN
T0 = int(dt.datetime(2026, 10, 12, 0, 0, tzinfo=dt.timezone.utc).timestamp() * 1000)
EVIDENCE_SHA256 = "429013e8533a6f188ad2201f340c743d1304988fc7dd8172a4ed416071cfab50"


# ---------------------------------------------------------------------------------------------- fixtures
def bars_walk(n, seed=3, start=T0):
    rnd = random.Random(seed)
    p, out = 80000.0, []
    for k in range(n):
        o = p
        p = p * math.exp(rnd.gauss(0, 0.0008))
        v = 20 + rnd.random() * 10
        tbv = v * (0.5 + rnd.gauss(0, 0.08))
        out.append([start + k * MIN, round(o, 2), round(max(o, p) + 1, 2), round(min(o, p) - 1, 2), round(p, 2),
                    round(v, 4), round(v * p, 2), 100, round(min(max(tbv, 0), v), 4), 0.0])
    return out


def write_base(tmp, minutes=6 * 60, spot_lag_ms=900, drop_spot=(), extra_lag=0):
    """A collector-format repository: perp and spot 1m batches every 15 minutes, written 2 min after the batch's last
    close (spot spot_lag_ms later), snapshots every 15 minutes, 5-minute OI history."""
    base = Path(tmp)
    perp, spot = bars_walk(minutes, 3), bars_walk(minutes, 4)
    for name, bars, lag in (("binance_klines_1m_BTCUSDT_perp", perp, 0), ("binance_klines_1m_BTCUSDT_spot", spot, spot_lag_ms)):
        p = base / "data/prices" / name / "2026-10.jsonl"
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as f:
            for k in range(0, minutes, 15):
                chunk = [b for b in bars[k:k + 15] if not (name.endswith("spot") and b[0] in drop_spot)]
                if not chunk:
                    continue
                obs = chunk[-1][0] + MIN + 2 * MIN + lag + extra_lag
                f.write(json.dumps({"series": name, "t": chunk[0][0], "t_last": chunk[-1][0], "observed_at": obs,
                                    "fields": ["t", "o", "h", "l", "c", "v", "qv", "n", "tbv", "tbqv"], "bars": chunk}) + "\n")
    sp = base / "data/snap/2026-10.jsonl"
    sp.parent.mkdir(parents=True, exist_ok=True)
    with open(sp, "w") as f:
        for k in range(0, minutes, 15):
            t = T0 + k * MIN + 7 * MIN
            mark = perp[min(k + 7, minutes - 1)][4]
            f.write(json.dumps({"t": t, "observed_at": t + 90_000,
                                "depth_binance_usdt": {"st": "ok", "bid_btc_25": 60.0, "ask_btc_25": 55.0},
                                "hl_predicted_fundings": {"st": "ok", "venues": {"BinPerp": {"rate": 1e-4, "interval_h": 8},
                                                                                 "BybitPerp": {"rate": 5e-5, "interval_h": 8},
                                                                                 "HlPerp": {"rate": 1.25e-5, "interval_h": 1}}},
                                "binance_usdt_prem": {"mark": mark}, "premium_parts": {"binance_spot_btcusdt": mark * 1.0002}}) + "\n")
    op = base / "data/series/binance_openInterestHist_5m/2026-10.jsonl"
    op.parent.mkdir(parents=True, exist_ok=True)
    with open(op, "w") as f:
        for k in range(0, minutes, 5):
            t = T0 + k * MIN
            f.write(json.dumps({"t": t, "observed_at": t + 7 * MIN, "f": {"sumOpenInterest": 95000 + k, "sumOpenInterestValue": 1}}) + "\n")
    return base


# --------------------------------------------------------------------------------------------- contract
class ContractParityTests(unittest.TestCase):
    def test_contract_pin_and_copies(self):
        b = (ROOT / "research_tools/evidence_contract.py").read_bytes()
        self.assertEqual(hashlib.sha256(b).hexdigest(), EVIDENCE_SHA256)
        self.assertEqual((ROOT / "research/registrations/o33-v3.1/enforcement/desk_evidence.py").read_bytes(), b)

    def test_o33_v31_manifest_and_frozen_v3_untouched(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/o33_v31_manifest.py"), "check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        spec = json.loads((ROOT / "research/registrations/o33-v3.1/spec.json").read_text())
        self.assertIn("first push of this directory to main", spec["effective_time"])
        self.assertIn("withdrawn", spec["corrections"])

    def test_catalog_validates(self):
        self.assertEqual(catalog.validate(catalog.load()), [])


# ------------------------------------------------------------------------------------------- report tail
class ReportTailTests(unittest.TestCase):
    def setUp(self):
        import importlib
        self.h = importlib.import_module("regression.test_rev26") if (ROOT / "regression/__init__.py").exists() else None
        sys.path.insert(0, str(ROOT / "regression"))
        import test_rev26 as R26
        self.R = R26

    def run_health(self, tmp, now, cutoff):
        R = self.R
        runs_all = sorted(report.read_rows(Path(tmp) / "data/runs/2026-01.jsonl"), key=lambda r: r["t"])
        snaps = sorted(report.read_rows(Path(tmp) / "data/snap/2026-01.jsonl"), key=lambda r: r["t"])
        since = now - 7 * 24 * H
        runs = [r for r in runs_all if since <= r["t"] <= now and cadence.is_routine(r)]
        return report.collection_health(runs_all, runs, snaps, cadence.load(tmp), since, now, cutoff)

    def test_intervals_after_the_input_cutoff_are_not_yet_assessed(self):
        R = self.R
        with tempfile.TemporaryDirectory() as tmp:
            R.write_cadence(tmp)
            slots = [R.T1 + h * H + m * R.M for h in range(3) for m in R.QUARTER]
            R.store(tmp, [R.run(t) for t in slots], [R.snap(t) for t in slots])
            cutoff = R.T1 + H + 52 * R.M + 30_000                 # inputs end in the second hour
            now = R.T1 + 3 * H + 30 * R.M                         # report clock well after
            lines, _ = self.run_health(tmp, now, cutoff)
            quarter = R.table_rows(lines)[-1]
            import re
            m = re.search(r"(\d+)/(\d+) slot intervals", quarter)
            self.assertEqual(m.group(1), m.group(2))              # every assessed interval held
            self.assertIn("not yet assessed (after the input cutoff)", quarter)
            self.assertTrue(any("wall-clock lag" in l for l in lines))

    def test_a_genuinely_missing_interval_still_counts_and_late_evidence_reassesses(self):
        R = self.R
        with tempfile.TemporaryDirectory() as tmp:
            R.write_cadence(tmp)
            slots = [R.T1 + h * H + m * R.M for h in range(2) for m in R.QUARTER]
            gap = slots[3]
            R.store(tmp, [R.run(t) for t in slots], [R.snap(t) for t in slots if t != gap])
            now = R.T1 + 2 * H + 25 * R.M
            lines, _ = self.run_health(tmp, now, slots[-1] + 30_000)
            import re
            m = re.search(r"(\d+)/(\d+) slot intervals", R.table_rows(lines)[-1])
            self.assertEqual(int(m.group(2)) - int(m.group(1)), 1)   # the one genuinely missing interval counts
        with tempfile.TemporaryDirectory() as tmp:
            R.write_cadence(tmp)
            R.store(tmp, [R.run(t) for t in slots], [R.snap(t) for t in slots[:5]])
            import re
            early, _ = self.run_health(tmp, now, slots[4] + 30_000)
            self.assertIn("not yet assessed", R.table_rows(early)[-1])
            R.store(tmp, (), [R.snap(t) for t in slots[5:]])     # the delayed evidence arrives
            later, _ = self.run_health(tmp, now, slots[-1] + 30_000)
            m = re.search(r"(\d+)/(\d+) slot intervals", R.table_rows(later)[-1])
            self.assertEqual(m.group(1), m.group(2))

    def test_without_a_cutoff_the_old_behaviour_is_kept(self):
        R = self.R
        with tempfile.TemporaryDirectory() as tmp:
            R.write_cadence(tmp)
            slots = [R.T1 + h * H + m * R.M for h in range(2) for m in R.QUARTER]
            R.store(tmp, [R.run(t) for t in slots], [R.snap(t) for t in slots])
            lines, _ = self.run_health(tmp, R.T1 + 2 * H + 25 * R.M, None)
            self.assertNotIn("not yet assessed", R.table_rows(lines)[-1])


# ------------------------------------------------------------------------------------------ funnel, panel
class FunnelPanelTests(unittest.TestCase):
    def test_spot_after_perp_is_arrived_after_decision_and_distribution_exact(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = Store(write_base(tmp, minutes=120), cutoff=T0 + 4 * H)
            perp, spot = st.bars("binance_klines_1m_BTCUSDT_perp"), st.bars("binance_klines_1m_BTCUSDT_spot")
            lags = funnel.arrival_lags(perp, spot, T0, T0 + 120 * MIN)
            self.assertEqual((lags["n"], lags["median"], lags["later_share"]), (120, 900, 1.0))
            f = funnel.a1_spot_funnel(st, T0, T0 + 120 * MIN)
            self.assertEqual(f["counts"], {"arrived-after-decision": 115})
        with tempfile.TemporaryDirectory() as tmp:
            st = Store(write_base(tmp, minutes=120, spot_lag_ms=-500), cutoff=T0 + 4 * H)
            self.assertEqual(funnel.a1_spot_funnel(st, T0, T0 + 120 * MIN)["counts"], {"retained": 115})
        with tempfile.TemporaryDirectory() as tmp:
            st = Store(write_base(tmp, minutes=120, spot_lag_ms=-500, drop_spot={T0 + 30 * MIN}), cutoff=T0 + 4 * H)
            c = funnel.a1_spot_funnel(st, T0, T0 + 120 * MIN)["counts"]
            self.assertEqual(c["source-missing"], 5)

    def test_stage_distinguishes_missing_from_late(self):
        self.assertEqual(funnel.stage(None, 10), "source-missing")
        self.assertEqual(funnel.stage({"avail": 11, "v": 1}, 10, "v"), "arrived-after-decision")
        self.assertEqual(funnel.stage({"avail": 9, "v": "NaN"}, 10, "v"), "invalid-capture")
        self.assertEqual(funnel.stage({"v": 1}, 10, "v"), "availability-unknown")
        self.assertEqual(funnel.stage({"avail": 9, "v": 0}, 10, "v", "nonneg"), "retained")     # zero is a value

    def test_panel_rows_are_as_of_their_own_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = write_base(tmp, minutes=6 * 60)
            early = panel.build(Store(base, cutoff=T0 + 4 * H), T0 + 2 * H, T0 + 4 * H)
            late = panel.build(Store(base, cutoff=T0 + 6 * H), T0 + 2 * H, T0 + 4 * H)
            self.assertEqual(E.canon(early["rows"]), E.canon(late["rows"]))          # later data cannot change a row
            cov = panel.coverage(late)
            self.assertEqual(cov["families"]["flow_liquidity"].get("ok"), 8)
            self.assertEqual(cov["families"]["liquidity_resilience"], {"gated": 8})
            r = late["rows"][-1]
            self.assertEqual(r["features"]["funding_dispersion_bp_8h"], round(1.0 - 0.5, 4) if False else r["features"]["funding_dispersion_bp_8h"])
            self.assertAlmostEqual(r["features"]["funding_mean_bp_8h"], (1.0 + 0.5 + 1.0) / 3, places=4)
            self.assertAlmostEqual(r["features"]["funding_dispersion_bp_8h"], 0.5, places=4)
            self.assertAlmostEqual(r["features"]["basis_bp"], -1e4 * (1 - 1 / 1.0002), places=2)
            self.assertLessEqual(r["inputs"]["perp_window_age_s"], 45 * 60)

    def test_stale_inputs_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = write_base(tmp, minutes=60)
            p = panel.build(Store(base, cutoff=T0 + 5 * H), T0 + 3 * H, T0 + 4 * H)
            self.assertTrue(all(r["state"]["flow_liquidity"].startswith("stale-inputs") for r in p["rows"]))

    def test_fitted_transform_uses_training_rows_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = Store(write_base(tmp, minutes=6 * 60), cutoff=T0 + 6 * H)
            p = panel.build(st, T0 + H, T0 + 6 * H)
            cut = T0 + 4 * H
            art = panel.fit_transform(p["rows"], ["flow_per_depth", "ret_15m_bp"], cut)
            self.assertLess(art["max_train_t"], cut)
            z = panel.apply_transform(art, p["rows"])
            self.assertEqual(len(z), len(p["rows"]))
            more = panel.fit_transform(p["rows"] + [dict(p["rows"][-1], t=T0 + 9 * H)], ["flow_per_depth"], cut)
            self.assertEqual(more["train_rows"], art["train_rows"])                # rows after the cutoff never fit
            bad = dict(art, train_cutoff_utc=E.iso(E.epoch_ms(T0 + 2 * H)))
            with self.assertRaises(ValueError):
                panel.apply_transform(bad, p["rows"])


# --------------------------------------------------------------------------------------- research API
def synth_provider():
    rows, labels = [], []
    rnd = random.Random(11)
    for k in range(400):
        t = T0 + k * 15 * MIN
        x = rnd.gauss(0, 1)
        rows.append({"t": t, "features": {"x": x, "y": None if k % 50 == 0 else rnd.gauss(0, 1)}, "state": {"fam": "ok"}})
        labels.append({"t": t, "state": "ok", "label_bp": 5 * x + rnd.gauss(0, 10), "label_available": t + 61 * MIN})

    def provide(cutoff):
        return {"rows": [r for r in rows if r["t"] < cutoff],
                "labels": {60: [x for x in labels if x["label_available"] <= cutoff]}}
    return provide


SPEC = {"family": "SYN", "features": ["x"], "horizon_min": 60,
        "rule": {"type": "linear-score", "weights": {"x": 1.0}, "bias": 0.0, "long_above": 0.5, "short_below": -0.5}}


class Clock:
    def __init__(self, t):
        self.t = t

    def __call__(self):
        return E.epoch_ms(self.t)


class ResearchAPITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clock = Clock(T0 + 50 * H)
        actor = {"kind": "model", "id": "fixture-model", "version": "fixture-1 (alias, unpinned)", "training_cutoff": None}
        self.r = ResearchAPI(self.tmp.name, synth_provider(), "researcher", actor, self.clock)
        self.e = ResearchAPI(self.tmp.name, synth_provider(), "evaluator", {"kind": "system", "id": "evaluator"}, self.clock)
        self.r.open_experiment("X1", "SYN", E.epoch_ms(T0 + 48 * H), {"checkpoints_n": [20, 40]}, "req-open")

    def tearDown(self):
        self.tmp.cleanup()

    def test_end_to_end_discovery_register_confirm_release(self):
        res = self.r.run("X1", SPEC, E.epoch_ms(T0 + 48 * H), {"max_rows": 1000}, "req-run1")
        self.assertGreater(res["scored"], 0)
        self.assertIn("training cutoff unknown", res["exposure"])
        cand = self.r.register("X1", SPEC, "req-reg")
        self.assertEqual(self.r.results("X1", cand["candidate_sha256"], "req-view0"), [])     # nothing released yet
        self.clock.t = T0 + 70 * H
        ev = self.e.evaluate("X1", cand["candidate_sha256"], "req-ev1")
        rec = ev["released"][0]                                   # research-api-1.1.0: one record per checkpoint
        self.assertTrue(rec["result"]["scored"] == 20 and rec["released"] and rec["checkpoint_n"] == 20)
        self.assertEqual(rec["confirmation_window"][0], cand["confirmation_starts_utc"])
        got = self.r.results("X1", cand["candidate_sha256"], "req-view1")
        self.assertEqual([g["checkpoint_n"] for g in got], [r["checkpoint_n"] for r in ev["released"]])
        self.assertTrue(all(g["result"]["scored"] == g["checkpoint_n"] for g in got))   # never 46 under 40
        self.assertEqual(verify_results(self.tmp.name, "X1"), [])
        self.assertEqual(Ledger(Path(self.tmp.name) / "ledger.jsonl").verify(), [])

    def test_unauthorized_partitions_are_refused_through_every_operation(self):
        with self.assertRaises(Refused):
            self.r.panel("X1", E.epoch_ms(T0 + 49 * H), "req-p")
        with self.assertRaises(Refused):
            self.r.inspect("X1", E.epoch_ms(T0 + 49 * H), "req-i")
        with self.assertRaises(Refused):
            self.r.run("X1", SPEC, E.epoch_ms(T0 + 40 * H), {}, "req-r", partition="confirmation")
        with self.assertRaises(Refused):
            self.r.evaluate("X1", "0" * 64, "req-e")
        with self.assertRaises(Refused):
            self.e.run("X1", SPEC, E.epoch_ms(T0 + 40 * H), {}, "req-er")
        d = self.r.panel("X1", E.epoch_ms(T0 + 48 * H), "req-ok")
        self.assertTrue(all(r["t"] < T0 + 48 * H for r in d["rows"]))
        self.assertTrue(all(x["label_available"] < T0 + 48 * H for x in d["labels"][60]))
        acts = [e["action"] for e in Ledger(Path(self.tmp.name) / "ledger.jsonl").entries()]
        self.assertIn("run-aborted", acts)                                   # refusals stay in history

    def test_failed_runs_stay_in_history_and_requests_are_idempotent(self):
        bad = dict(SPEC, rule=dict(SPEC["rule"], type="python"))
        with self.assertRaises(ValueError):
            self.r.run("X1", bad, E.epoch_ms(T0 + 40 * H), {}, "req-bad")
        L = Ledger(Path(self.tmp.name) / "ledger.jsonl")
        self.assertEqual([e["action"] for e in L.entries()][-1], "run-error")
        n = len(L.entries())
        self.r.run("X1", SPEC, E.epoch_ms(T0 + 40 * H), {"max_rows": 50}, "req-same")
        self.r.run("X1", SPEC, E.epoch_ms(T0 + 40 * H), {"max_rows": 50}, "req-same")
        self.assertEqual(len(L.entries()), n + 2)                            # the panel query + the run, once
        with self.assertRaises(ValueError):
            L.append("X1", {"kind": "human", "id": "j"}, "note", {"x": 1}, "req-same", E.epoch_ms(T0))
        self.assertEqual(L.family_count("SYN")["runs_including_failures"], 2)

    def test_evaluation_records_are_immutable_to_the_researcher(self):
        cand = self.r.register("X1", SPEC, "req-reg2")
        self.clock.t = T0 + 70 * H
        self.e.evaluate("X1", cand["candidate_sha256"], "req-ev")
        p = Path(self.tmp.name) / "results" / "X1.jsonl"
        txt = p.read_text().replace('"released":true', '"released":false')
        p.write_text(txt)
        self.assertTrue(verify_results(self.tmp.name, "X1"))
        lp = Path(self.tmp.name) / "ledger.jsonl"
        lines = lp.read_text().splitlines()
        lp.write_text("\n".join(lines[:1] + lines[2:]) + "\n")            # delete an entry
        self.assertTrue(Ledger(lp).verify())

    def test_reopening_an_experiment_with_another_definition_is_refused(self):
        with self.assertRaises(Refused):
            self.r.open_experiment("X1", "SYN", E.epoch_ms(T0 + 49 * H), {"checkpoints_n": [20]}, "req-reopen")


# ------------------------------------------------------------------------------------ directional stream
PROTO = json.loads((ROOT / "research/registrations/dir1-prepared/protocol.json").read_text())


def fixture_bars(hours=12):
    return {b[0]: {"o": b[1], "c": b[4], "avail": b[0] + MIN + 2 * MIN} for b in bars_walk(hours * 60, 9)}


class Tick:
    def __init__(self, t, step_s=1.0):
        self.t, self.step = t, step_s

    def __call__(self):
        self.t += self.step * 1000
        return E.epoch_ms(int(self.t))


class DirectionalTests(unittest.TestCase):
    def test_prepared_protocol_is_valid_and_not_effective(self):
        self.assertEqual(DIR.validate_protocol(PROTO), [])
        self.assertEqual((PROTO["status"], PROTO["effective_utc"]), ("prepared", None))
        bad = dict(PROTO, status="registered")
        self.assertTrue(DIR.validate_protocol(bad))
        self.assertTrue(DIR.validate_protocol(dict(PROTO, inference=dict(PROTO["inference"], selection="best-of-n"))))

    def test_missed_opportunities_are_created_by_reconciliation(self):
        log = DIR.OpportunityLog()
        DIR.reconcile(PROTO, log, T0, T0 + 3 * H, E.epoch_ms(T0 + 3 * H))
        states = {e["opportunity"]: e["state"] for e in log.events}
        self.assertEqual(len(states), 3 * len(PROTO["arms"]))
        self.assertTrue(all(s == "missed" for s in states.values()))

    def test_transitions_are_immutable(self):
        log = DIR.OpportunityLog()
        oid = DIR.opp_id(PROTO, T0, "baseline")
        log.add(oid, "baseline", "expected", E.epoch_ms(T0))
        with self.assertRaises(ValueError):
            log.add(oid, "baseline", "graded", E.epoch_ms(T0))
        log.add(oid, "baseline", "inputs-ready", E.epoch_ms(T0))
        log.add(oid, "baseline", "inference-started", E.epoch_ms(T0))
        log.add(oid, "baseline", "forecast", E.epoch_ms(T0))
        with self.assertRaises(ValueError):
            log.add(oid, "baseline", "forecast", E.epoch_ms(T0))

    def test_retries_are_recorded_and_the_first_valid_parse_is_selected(self):
        stub = DIR.frontier_arm_stub(['{"p_up": "high"}', {"p_up": 0.61}, {"p_up": 0.9}])
        r = DIR.infer(stub, {}, PROTO, Tick(T0), model={"provider": "fixture", "id": "stub", "pinned": False})
        self.assertEqual((r["selected_attempt"], r["p_up"], len(r["attempts"])), (1, 0.61, 2))
        self.assertTrue(stub.test_only)
        boom = DIR.frontier_arm_stub([RuntimeError("down"), RuntimeError("down")])
        self.assertEqual(DIR.infer(boom, {}, PROTO, Tick(T0))["outcome"], "error")
        slow = DIR.infer(DIR.frontier_arm_stub([{"p_up": 0.6}, {"p_up": 0.6}]), {}, PROTO, Tick(T0, step_s=200))
        self.assertEqual(slow["outcome"], "timeout")

    def test_publication_binds_content_and_time(self):
        d = T0 + 4 * H
        c = {"p_up": 0.6, "opportunity": "x"}
        ok = {"kind": "git-commit", "ref": "abc", "published_utc": E.iso(E.epoch_ms(d + 120_000)), "content_sha256": E.content_sha256(c)}
        self.assertEqual(DIR.publication_status(PROTO, d, c, ok)[0], "published")
        self.assertEqual(DIR.publication_status(PROTO, d, c, dict(ok, published_utc=E.iso(E.epoch_ms(d + 601_000))))[0], "publish-late")
        self.assertEqual(DIR.publication_status(PROTO, d, dict(c, p_up=0.7), ok)[0], "publish-failed")
        self.assertEqual(DIR.publication_status(PROTO, d, c, dict(ok, published_utc=E.iso(E.epoch_ms(d - 1))))[0], "publish-failed")

    def test_no_quote_before_the_decision_could_exist(self):
        bars = fixture_bars()
        d = T0 + 4 * H
        # directional-1.1.0: grade() takes an admission from admit() and an explicit evaluation cutoff
        pub = {"class": "on-time", "published_utc": E.iso(E.epoch_ms(d + 7 * MIN + 5000)), "fixture": True}
        g = DIR.grade(PROTO, d, 0.7, pub, bars, evaluation_cutoff_ms=T0 + 12 * H)
        self.assertEqual(g["entry_utc"], E.iso(E.epoch_ms(d + 9 * MIN)))           # publication + 60 s, next minute
        self.assertGreater(E.instant(g["entry_utc"]), E.instant(pub["published_utc"]))
        self.assertIn("not execution", g["evidence_class"])

    def test_offline_acceptance_replay_end_to_end(self):
        """FIXTURE: every record produced here is an offline replay, not a live run."""
        bars = fixture_bars(14)
        log = DIR.OpportunityLog()
        art = {"schema": "directional-statistical/1", "features": ["ret_1h_bp"], "coef": [0.002], "intercept": 0.0,
               "train_cutoff_utc": E.iso(E.epoch_ms(T0))}
        art["sha256"] = E.content_sha256(art)
        stat = DIR.statistical_arm(art)                                   # 1.1.0 validates the artifact
        arms = {"baseline": DIR.baseline_arm(PROTO), "statistical": stat,
                "frontier": DIR.frontier_arm_stub([{"p_up": 0.52}] * 3 + ["bad", "bad"] + [{"p_up": 0.6}] * 10)}
        graded = {a: {} for a in arms}
        decisions = DIR.expected(PROTO, T0 + 2 * H, T0 + 8 * H)
        for d in decisions:
            feats = {"ret_1h_bp": 1e4 * math.log(bars[d - MIN]["c"] / bars[d - 60 * MIN]["o"])}
            for arm, fn in arms.items():
                oid = DIR.opp_id(PROTO, d, arm)
                log.add(oid, arm, "expected", E.epoch_ms(d))
                if arm == "frontier" and d == decisions[-1]:
                    continue                                                       # the worker never ran
                log.add(oid, arm, "inputs-ready", E.epoch_ms(d))
                log.add(oid, arm, "inference-started", E.epoch_ms(d))
                r = DIR.infer(fn, feats, PROTO, Tick(d))
                if r["outcome"] != "forecast":
                    log.add(oid, arm, r["outcome"], E.epoch_ms(d))
                    graded[arm][d] = {"state": r["outcome"]}
                    continue
                log.add(oid, arm, "forecast", E.epoch_ms(d), {"p_up": r["p_up"]})
                content = {"opportunity": oid, "p_up": r["p_up"]}
                ev = {"kind": "git-commit", "ref": "fixture", "published_utc": E.iso(E.epoch_ms(d + 90_000)),
                      "content_sha256": E.content_sha256(content)}
                st, _ = DIR.publication_status(PROTO, d, content, ev)
                log.add(oid, arm, st, E.epoch_ms(d + 90_000))
                adm = {"class": "on-time" if st == "published" else "late", "published_utc": ev["published_utc"],
                       "fixture": True}
                g = DIR.grade(PROTO, d, r["p_up"], adm, bars, evaluation_cutoff_ms=T0 + 14 * H)
                log.add(oid, arm, "graded" if g["state"] == "graded" else "ungradable", E.epoch_ms(d + 5 * H))
                graded[arm][d] = g
        DIR.reconcile(PROTO, log, T0 + 2 * H, T0 + 8 * H, E.epoch_ms(T0 + 9 * H))
        self.assertEqual(log.state(DIR.opp_id(PROTO, decisions[-1], "frontier")), "missed")
        cmp = DIR.compare_arms(graded)
        self.assertEqual(cmp["opportunities"], len(decisions))
        self.assertEqual(cmp["arms"]["baseline"]["graded"], len(decisions))
        self.assertEqual(cmp["arms"]["frontier"]["states"].get("missing"), 1)    # the missed one stays counted
        self.assertLess(cmp["paired_intersection"], cmp["opportunities"])         # the error is in the denominator
        self.assertEqual(cmp["arms"]["frontier"]["states"].get("error"), 1)

    def test_statistical_arm_trains_before_its_cutoff_only(self):
        rows = [{"t": T0 + k * H, "features": {"a": (-1) ** k}} for k in range(40)]
        labels = [{"t": T0 + k * H, "state": "ok", "label_bp": (-1) ** k, "label_available": T0 + k * H + 5 * H} for k in range(40)]
        art = DIR.fit_logistic(rows, labels, ["a"], T0 + 20 * H)
        self.assertEqual(art["n_train"], 15)                                       # labels known before the cutoff
        self.assertGreater(art["coef"][0], 0)


# ------------------------------------------------------------------------------------------- calibration
class CalibrationTests(unittest.TestCase):
    def test_resolution_matches_the_reviewed_figures(self):
        self.assertAlmostEqual(calibration.resolution(2000, 0.10, 23)["expected_tail_draws"], 1.087, places=3)
        self.assertEqual(calibration.resolution(2000, 0.10, 100)["verdict"], "insufficient")
        self.assertEqual(calibration.required_B(0.10, 23), 18400)

    def test_blocks_and_resolution_refusals(self):
        self.assertEqual(calibration.block_bootstrap_ci([1.0] * 30, list(range(3)) * 10, 0.1)["state"], "insufficient-blocks")
        r = calibration.block_bootstrap_ci([float(i % 7) for i in range(200)], [i // 5 for i in range(200)], 0.10, B=500)
        self.assertEqual(r["state"], "ok")
        self.assertEqual(calibration.block_bootstrap_ci([1.0] * 200, [i // 5 for i in range(200)], 1e-6, B=100)["state"],
                         "insufficient-resolution")

    def test_null_simulation_exposes_dependence_ignored_by_a_naive_test(self):
        rnd = random.Random(5)

        def ar(n):
            x, out = 0.0, []
            for _ in range(n):
                x = 0.97 * x + rnd.gauss(0, 1)
                out.append(x)
            return out
        n = 600
        sig, out = ar(n), ar(n)

        def naive(s, o):
            m1, m2 = sum(s) / len(s), sum(o) / len(o)
            c = sum((a - m1) * (b - m2) for a, b in zip(s, o))
            v = math.sqrt(sum((a - m1) ** 2 for a in s) * sum((b - m2) ** 2 for b in o))
            return abs(c / v) * math.sqrt(len(s)) > 1.645          # nominal 10% two-sided, rows assumed independent
        res = calibration.null_false_positive(sig, out, [i // 20 for i in range(n)], naive, [200, 400, 600], sims=200)
        self.assertGreater(res["false_positive_any_look"], 0.3)


# ----------------------------------------------------------------------------------- turnover, archive, D1
class TurnoverArchiveD1Tests(unittest.TestCase):
    def test_band_zero_is_every_rebalance_and_bands_cut_turnover(self):
        tg = [0.5, 0.52, 0.49, 0.8, 0.79, 0.2]
        self.assertEqual(turnover.apply_band(tg, 0.0), tg)
        self.assertEqual(turnover.apply_band(tg, 0.05), [0.5, 0.5, 0.5, 0.8, 0.8, 0.2])
        px = [100, 101, 100, 102, 101, 103, 104]
        a, b = turnover.simulate(tg, px, 0.0, 10, 10), turnover.simulate(tg, px, 0.05, 10, 10)
        self.assertLess(b["turnover"], a["turnover"])
        self.assertAlmostEqual(a["cost_fraction"], a["turnover"] * 20 / 1e4)
        self.assertEqual(turnover.apply_band([0.5, None, 0.9], 0.0), [0.5, 0.5, 0.9])

    def test_archive_put_verify_replay_and_tamper(self):
        raw = json.dumps([[T0, "1", "2", "0.5", "1.5", "3", T0 + 59999, "4.5", 7, "1", "1.5", "0"]]).encode()
        with tempfile.TemporaryDirectory() as tmp:
            a = archive_store.ArchiveStore(tmp)
            rows = archive_store.parse_binance_klines(raw)
            line = a.put(raw, {"source": "binance", "url_or_channel": "fapi/v1/klines", "retrieved_utc": "2026-10-12T00:01:00Z",
                               "parser": "parse_binance_klines", "parser_version": "1", "provenance": "original"}, rows)
            self.assertEqual(a.verify([line]), [])
            self.assertEqual(a.replay(line, archive_store.parse_binance_klines)["state"], "ok")
            (Path(tmp) / line["key"]).write_bytes(raw + b" ")
            self.assertTrue(a.verify([line]))
            with self.assertRaises(ValueError):
                a.put(raw, {"source": "x", "url_or_channel": "y", "retrieved_utc": "2026-10-12T00:01:00", "parser": "p",
                            "parser_version": "1", "provenance": "original"})

    def test_d1_reasons(self):
        progs = {("u1", "1"): {"coin": "ETH", "statuses": [[1, "activated"]], "first_seen": 1},
                 ("u2", "2"): {"coin": "BTC", "statuses": [[2, "finished"]], "first_seen": 2},
                 ("u3", "3"): {"coin": "BTC", "statuses": [[3, "activated"]], "first_seen": 3, "first_seen_avail": T0 + 10 * MIN, "sz": "1"},
                 ("u4", "4"): {"coin": "BTC", "statuses": [[4, "activated"]], "first_seen": 4, "first_seen_avail": T0 + 10 * MIN, "sz": "100"}}
        bars = {T0: {"c": 80000.0, "avail": T0 + MIN}}
        r = d1_diagnostics.classify(progs, bars, 1e6)
        self.assertEqual(r["reasons"], {"not-btc": 1, "first-seen-not-active": 1, "below-min-notional": 1, "qualifying": 1})


# --------------------------------------------------------------------------------------------- E1 pilot
class PilotAcceptanceTests(unittest.TestCase):
    def test_uptime_is_not_success(self):
        crit = json.loads((ROOT / "stream/pilot_e1.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for day in ("2026-10-12", "2026-10-13", "2026-10-14"):
                for venue, inst in crit["scope"]["venues_instruments"]:
                    p = root / "derived/book1s" / venue / inst / day / "00.jsonl.gz"
                    p.parent.mkdir(parents=True, exist_ok=True)
                    d0 = int(dt.datetime.fromisoformat(day + "T00:00:00+00:00").timestamp() * 1000)
                    stale = day == "2026-10-13" and venue == "bybit"
                    with gzip.open(p, "wt") as f:
                        for s in range(0, 86400, 1):
                            f.write(json.dumps({"t": d0 + s * 1000 + 3, "book_age_ms": 5000 if stale else 300}) + "\n")
            # pilot-acceptance-1.1.0 needs the declared window and verifies raw objects (none exist in this fixture)
            r = pilot_acceptance.evaluate(root, crit, "2026-10-12T00:00:00Z", "2026-10-15T00:00:00Z", eligible_shocks=25)
            self.assertEqual(r["verdict"], "fail")                     # the service 'ran', but nothing verifies
            self.assertTrue(any("bybit" in x for x in r["findings"]))
            self.assertEqual(r["claimed_shocks_ignored"], 25)
            r2 = pilot_acceptance.evaluate(root, dict(crit, scope={"venues_instruments": [["deribit", "BTC-PERPETUAL"]]}),
                                           "2026-10-12T00:00:00Z", "2026-10-15T00:00:00Z")
            self.assertNotEqual(r2["verdict"], "pass")                # zero eligible shocks is never a pass
            self.assertEqual(pilot_acceptance.evaluate(root, crit)["verdict"], "invalid")   # no window, no verdict


if __name__ == "__main__":
    unittest.main()
