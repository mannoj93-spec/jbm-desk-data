"""Regressions for revision 2.10: hourly comparison observations (controls) of the collection-based
modules B, C and F (lab/controls.py), reviewed at commit 934bb25 (2.9 / lab-2.1).

Up to 2.9 a collection record became a control only if its run started before minute 15 of the UTC
hour; GitHub starts the nominal :07 run later than that most hours, so on 2026-09-24 00:00-15:31
UTC 59 successful runs gave each module two controls. Tests named `*_common_api` drive only
`module.run(lab, params)`, which exists in both versions, and fail on the reviewed code. Offline;
synthetic data only; write tests use temporary directories.
"""
import io
import json
import random
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from lab import evidence, experiments, outcomes, versioning
try:
    from lab import controls
except ImportError:                        # the reviewed code (2.9) has no policy module
    controls = None
NEW = controls is not None
new_only = unittest.skipUnless(NEW, "2.10 interface")
from lab.asof import ASSUMED_PROCESSING_MS
from lab.common import H, MINUTE
from lab.modules import accounts, liq_exposure, options_disagreement

ROOT = Path(__file__).resolve().parents[1]
T0 = 1_790_208_000_000                     # 2026-09-24 00:00 UTC
S = 1000
ACC = ["account_id", "state", "reason", "clearinghouse_time_offset_ms", "account_value", "total_ntl_pos",
       "total_margin_used", "total_raw_usd", "cross_account_value", "cross_maintenance_margin_used", "withdrawable",
       "n_positions", "other_n", "other_long_ntl", "other_short_ntl", "other_margin_used", "other_unrealized_pnl"]
PARAMS = {"liq_exposure": {"distance_pct": 2.0, "min_notional_usd": 1e12},
          "account_behavior": {"min_accounts": 99},
          "options_disagreement": {"z": 2.0, "z_window": 30, "min_records": 10}}
MODS = {"liq_exposure": liq_exposure, "account_behavior": accounts, "options_disagreement": options_disagreement}


def run_(t, lag=100 * S, mark_lag=None, mark=True, funding=True, fund=1e-4, szi=1.0):
    """One collection run: source time t, account/option records observed at t+lag, the snapshot
    (Hyperliquid mark and funding) at t+mark_lag."""
    mark_lag = lag if mark_lag is None else mark_lag
    acct = {"t": t, "observed_at": t + lag, "address_of": {"F0": "0xa"}, "account_fields": ACC, "policy": "hl-sample-v2",
            "accounts": [["F0", "ok_btc", None, 0, 1e6, 0, 0, 0, 1e6, 1e4, 0, 1, 0, 0, 0, 0, 0]],
            "positions": [["F0", "BTC", szi, 100.0, 50.0, "cross", 5, 1e5, -3e4, 1e4, 0, 40]], "flat": []}
    snap = {"t": t, "observed_at": t + mark_lag,
            "oi": {"hyperliquid": {"st": "ok", "mark": 100.0}} if mark else {},
            "binance_usdt_prem": {"st": "ok", "funding_live_predicted_8h": fund} if funding else {"st": "error"}}
    opt = {"t": t, "t_event": t, "observed_at": t + lag, "rows": [], "underlying": {}, "panel_fields": [], "panel": [],
           "rr": 0.1 * ((t // MINUTE) % 3)}
    return acct, snap, opt


class Store:
    """Collected records visible at `cutoff` (observed_at <= cutoff), like lab.data.Store."""
    def __init__(self, runs, cutoff, bars=None, order=None):
        vis = lambda r: r["observed_at"] <= cutoff
        self._acct = sorted((a for a, _, _ in runs if vis(a)), key=lambda r: r["t"])
        self._snap = sorted((s for _, s, _ in runs if vis(s)), key=lambda r: r["t"])
        self._opt = sorted((o for _, _, o in runs if vis(o)), key=lambda r: r["t"])
        self._bars = bars or {}

    def hl_accounts(self):
        return [dict(r) for r in self._acct]

    def snaps(self):
        return [dict(r) for r in self._snap]

    def options(self):
        return [dict(r) for r in self._opt]

    def hl_enrich(self):
        return []

    def bars(self, name):
        return self._bars


def lab_(runs, now, ctx=None, bars=None):
    return type("L", (), {"store": Store(runs, now, bars), "code": "c", "now": now, "control_context": ctx})()


def module_controls(module, runs, now, ctx=None, bars=None):
    mod = MODS[module]
    with patch.object(options_disagreement, "surface", lambda rec: {"rr25_7d": rec["rr"]}), \
            patch.object(options_disagreement, "panel_quality", lambda rec: {"rr25_7d_quotes": "unknown"}):
        p = mod.run(lab_(runs, now, ctx, bars), PARAMS[module])["passes"][0]
    return p["controls"], p["coverage"].get("comparison")


def hourly_runs(hours, minutes, lag=100 * S):
    return [run_(T0 + h * H + m * MINUTE + 17 * S, lag) for h in range(hours) for m in minutes]


class HourlySelectionTests(unittest.TestCase):
    def test_late_collections_give_one_control_per_hour_common_api(self):
        runs = hourly_runs(6, (16, 29, 42, 55))                    # nominal :07 started at :16
        for module in MODS:
            ctl, _ = module_controls(module, runs, T0 + 6 * H + 30 * MINUTE)
            hours = [c["t_inputs"] // H * H for c in ctl]
            self.assertEqual(hours, [T0 + h * H for h in range(6)], module)     # 2.9: none at all
            for c in ctl:
                self.assertEqual(c["t_available"], c["t_inputs"] + ASSUMED_PROCESSING_MS)
                self.assertGreaterEqual(c["t_inputs"], c["t_event"])
                self.assertGreater(c["t_available"], c["t_inputs"] // H * H)     # never re-dated to the hour

    def test_collections_at_16_29_and_59_common_api(self):
        for minute in (16, 29, 59):
            runs = [run_(T0 + h * H + minute * MINUTE, 30 * S) for h in range(3)]
            for module in ("liq_exposure", "options_disagreement"):
                ctl, diag = module_controls(module, runs, T0 + 3 * H + 30 * MINUTE)
                self.assertEqual(len(ctl), 3, (module, minute))
                self.assertEqual([c["t_event"] for c in ctl], [r[0]["t"] for r in runs])
                if NEW:
                    self.assertEqual(diag["closed_hours_with_candidates_but_no_control"], [])

    def test_earliest_availability_wins_ties_are_deterministic_and_order_free_common_api(self):
        t = T0 + 2 * H
        runs = [run_(t + 30 * MINUTE, 5 * S), run_(t + 20 * MINUTE, 10 * MINUTE + 5 * S),   # same availability
                run_(t + 40 * MINUTE, 5 * S)]
        ctl, _ = module_controls("liq_exposure", runs, t + H)
        self.assertEqual(len(ctl), 1)
        self.assertEqual(ctl[0]["t_event"], t + 20 * MINUTE)                    # tie -> earlier source time
        for seed in range(5):
            shuffled = runs[:]
            random.Random(seed).shuffle(shuffled)
            self.assertEqual([c["event_id"] for c in module_controls("liq_exposure", shuffled, t + H)[0]],
                             [c["event_id"] for c in ctl])

    def test_missing_first_input_uses_the_next_and_empty_hours_stay_empty_common_api(self):
        t = T0 + 5 * H
        runs = [run_(t + 16 * MINUTE, mark=False), run_(t + 29 * MINUTE), run_(t + 2 * H + 20 * MINUTE)]
        ctl, diag = module_controls("liq_exposure", runs, t + 3 * H + MINUTE)
        self.assertEqual([c["t_event"] for c in ctl], [t + 29 * MINUTE, t + 2 * H + 20 * MINUTE])
        if not NEW:
            return
        missing = dict((h, why) for h, why in diag["missing_closed_hours"])
        self.assertIn(t + H, missing)                                           # nothing carried into it
        self.assertEqual(diag["closed_hours_with_candidates_but_no_control"], [])
        only_bad = [run_(t + 16 * MINUTE, mark=False)]
        ctl, diag = module_controls("liq_exposure", only_bad, t + H + MINUTE)
        self.assertEqual(ctl, [])
        self.assertIn("missing same-run Hyperliquid mark", dict(diag["missing_closed_hours"])[t])

    def test_missing_options_funding_does_not_suppress_a_control_common_api(self):
        runs = [run_(T0 + h * H + 20 * MINUTE, funding=False) for h in range(4)]
        ctl, _ = module_controls("options_disagreement", runs, T0 + 4 * H + MINUTE)
        self.assertEqual(len(ctl), 4)
        self.assertTrue(all(c["features"]["funding_pred_8h"] is None for c in ctl))
        late = [run_(T0 + h * H + 20 * MINUTE, mark_lag=3 * H) for h in range(4)]   # funding observed hours later
        self.assertEqual([c["t_available"] for c in module_controls("options_disagreement", late, T0 + 8 * H)[0]],
                         [c["t_available"] for c in ctl])

    def test_midnight_and_boundary_crossing_common_api(self):
        day_end = T0 + 24 * H
        runs = [run_(day_end - 90 * S, 120 * S),              # source 23:58:30, inputs 00:00:30 -> next day's 00:00
                run_(day_end + 10 * H - 60 * S, 30 * S)]      # inputs 09:59:30, decision 10:00:30 -> bucket 09:00
        ctl, _ = module_controls("liq_exposure", runs, day_end + 11 * H)
        by_hour = {c["t_inputs"] // H * H: c for c in ctl}
        self.assertEqual(sorted(by_hour), [day_end, day_end + 9 * H])
        a = by_hour[day_end]
        self.assertEqual((a["t_event"], a["t_inputs"], a["t_available"]), (day_end - 90 * S, day_end + 30 * S, day_end + 90 * S))
        b = by_hour[day_end + 9 * H]
        self.assertEqual(b["t_available"], day_end + 10 * H + 30 * S)          # decision lands in the next hour
        entry = outcomes.label(b["t_available"], 1, {}, day_end + 20 * H, (30,))
        self.assertTrue(all(v["status"] == "immature" for v in entry.values()))   # no bars; nothing invented
        self.assertGreaterEqual(-(-b["t_available"] // MINUTE) * MINUTE, b["t_inputs"] + ASSUMED_PROCESSING_MS)

    @new_only
    def test_inputs_too_late_are_excluded_not_redated(self):
        runs = [run_(T0 + 20 * MINUTE, 61 * MINUTE)]                            # beyond LATE_INPUT_MAX_MS
        ctl, diag = module_controls("options_disagreement", runs, T0 + 3 * H)
        self.assertEqual(ctl, [])
        self.assertIn("late_inputs", dict(diag["missing_closed_hours"])[T0 + H])


class FreezeAndCutoffTests(unittest.TestCase):
    @new_only
    def test_historical_cutoff_and_late_arrival_cannot_displace(self):
        t = T0 + 3 * H
        runs = [run_(t + 30 * MINUTE, 60 * S)]
        ctx = {"frozen": {}, "last_cutoff": None, "new": []}
        first, _ = module_controls("liq_exposure", runs, t + 45 * MINUTE, ctx)
        self.assertEqual(len(ctx["new"]), 1)
        frozen = {r["control_hour"]: r for r in ctx["new"]}
        # an older source time, with EARLIER availability, committed only now (after that run)
        late = runs + [run_(t + 10 * MINUTE, 60 * S)]
        again, _ = module_controls("liq_exposure", late, t + 2 * H, {"frozen": frozen, "last_cutoff": t + 45 * MINUTE})
        self.assertEqual([c["event_id"] for c in again], [c["event_id"] for c in first])
        # a cutoff before the freeze does not see the later decision; since 2.11 the provisional
        # candidate it would compute (t+10) differs from what was stored later, so the slot is
        # withheld rather than evaluated with the losing record
        past, diag = module_controls("liq_exposure", late, t + 25 * MINUTE, {"frozen": frozen, "last_cutoff": None})
        self.assertEqual(past, [])
        self.assertIn("differs", dict(diag["withheld_stored"])[t])
        same, diag = module_controls("liq_exposure", runs, t + 40 * MINUTE, {"frozen": frozen, "last_cutoff": None})
        self.assertEqual([c["t_event"] for c in same], [t + 30 * MINUTE])      # same identity: provisional
        self.assertEqual(diag["selection_states"], {"provisional": 1})

    def test_future_prices_funding_and_labels_leave_selections_unchanged_common_api(self):
        runs = hourly_runs(4, (18, 33))
        base, _ = module_controls("options_disagreement", runs, T0 + 5 * H)
        bars = {T0 + i * MINUTE: {"t": T0 + i * MINUTE, "o": 100 + i, "h": 101 + i, "l": 99 + i, "c": 100 + i,
                                  "avail": T0 + (i + 1) * MINUTE} for i in range(300)}
        later = runs + [run_(T0 + 4 * H + 18 * MINUTE, fund=0.5)]            # a later funding shock
        for module in ("options_disagreement", "liq_exposure", "account_behavior"):
            a, _ = module_controls(module, runs, T0 + 5 * H)
            b, _ = module_controls(module, later, T0 + 5 * H, bars=bars)
            self.assertEqual([c["event_id"] for c in b[:len(a)]], [c["event_id"] for c in a], module)
        self.assertTrue(base)

    @new_only
    def test_incomplete_outcome_never_swaps_the_control(self):
        """Selection reads no outcome: labels are computed later by experiments.label_all."""
        src = (ROOT / "lab/controls.py").read_text()
        for word in ("label", "ret_net", "outcome", "baseline", "status"):
            self.assertNotIn(f'["{word}"]', src)

    @new_only
    def test_persisted_selection_is_first_wins_and_merge_keeps_it(self):
        d = {"id": "C1", "_version": "ev-x"}
        rec = {"control_policy": controls.POLICY, "control_hour": T0, "t_event": T0 + 1, "t_persisted": 5}
        other = dict(rec, t_event=T0 + 2, t_persisted=9)
        with tempfile.TemporaryDirectory() as base:
            self.assertEqual(controls.persist_selections(base, d, [rec]), 1)
            p = controls.controls_dir(base, d) / "2026-09.jsonl"
            b1 = p.read_bytes()
            self.assertEqual(controls.persist_selections(base, d, [rec, other]), 0)     # repeat / concurrent run
            self.assertEqual(p.read_bytes(), b1)
            self.assertEqual(controls.load_selections(base, d)[T0]["t_event"], T0 + 1)
            sys.path.insert(0, str(ROOT / "scripts"))
            import merge_research
            with tempfile.TemporaryDirectory() as inc:
                q = Path(inc) / p.relative_to(base)
                q.parent.mkdir(parents=True)
                q.write_text(json.dumps(other, sort_keys=True) + "\n")
                with patch("sys.stdout", io.StringIO()), patch("sys.stderr", io.StringIO()):
                    merge_research.main(inc, base)
            self.assertEqual(p.read_bytes(), b1)

    @new_only
    def test_repeat_runs_are_idempotent_through_the_lab_plumbing(self):
        runs = hourly_runs(3, (21, 44))
        ctx = {"frozen": {}, "last_cutoff": None, "new": []}
        a, _ = module_controls("account_behavior", runs, T0 + 3 * H, ctx)
        frozen = {r["control_hour"]: r for r in ctx["new"]}
        ctx2 = {"frozen": frozen, "last_cutoff": T0 + 3 * H, "new": []}
        b, diag = module_controls("account_behavior", runs, T0 + 3 * H, ctx2)
        self.assertEqual(ctx2["new"], [])
        self.assertEqual(a, b)
        self.assertEqual(diag["frozen_selected"], len(b))


class ReviewHardeningTests(unittest.TestCase):
    """Findings of an adversarial review of the first 2.10 draft."""
    @new_only
    def test_a_control_selected_after_a_cutoff_never_trains_that_cutoffs_baseline(self):
        from lab import baseline as baseline_mod
        C = T0 + 30 * H
        rows = []
        for k in range(50):
            t = T0 + k * 20 * MINUTE
            e = {"group": "control_long", "t_persisted": C + 6 * H, "t_available": t}
            lab_ = {60: {"status": "complete", "entry_t": t, "exit_t": t + H, "label_available": t + H + MINUTE,
                         "ret_net": 0.001 * (k % 3)}}
            bf = {"prior_ret_60m_aligned": 0.001 * (k % 7), "prior_rv_60m": 0.002 + 0.0001 * (k % 5),
                  "funding_aligned": 0.0001 * (k % 3)}
            rows.append((e, lab_, bf))
        bl = baseline_mod.build(rows, [60])[60]
        obs = dict(rows[0][2], entry_t=C + 2 * DAY)
        self.assertEqual(len(bl.training(C + 3 * DAY, cutoff=C)[0]), 0)       # draft: all 50
        self.assertIsNone(bl.predict(obs, cutoff=C)[0])
        self.assertEqual(len(bl.training(C + 3 * DAY)[0]), 50)                 # known once selected

    @new_only
    def test_selections_are_stored_at_selection_time_when_writing(self):
        with tempfile.TemporaryDirectory() as base:
            d = {"id": "C1", "_version": "ev-y"}
            ctx = {"frozen": {}, "last_cutoff": None, "new": [], "design": d}
            lab = lab_(hourly_runs(2, (20,)), T0 + 2 * H, ctx)
            lab.base, lab.write = base, True
            with patch.object(options_disagreement, "surface", lambda rec: {"rr25_7d": rec["rr"]}):
                liq_exposure.run(lab, PARAMS["liq_exposure"])
            self.assertEqual(sorted(controls.load_selections(base, d)), [T0, T0 + H])
            lab.write = False                                                   # read-only runs store nothing
            with tempfile.TemporaryDirectory() as other:
                lab.base = other
                liq_exposure.run(lab, PARAMS["liq_exposure"])
                self.assertFalse(controls.controls_dir(other, d).exists())

    @new_only
    def test_a_stored_selection_without_a_time_is_never_used(self):
        runs = [run_(T0 + 30 * MINUTE)]
        bogus = {T0: {"control_policy": controls.POLICY, "control_hour": T0, "t_event": 1, "t_available": 2,
                      "t_inputs": 1, "event_id": "x"}}
        ctl, diag = module_controls("liq_exposure", runs, T0 + H, {"frozen": bogus, "last_cutoff": None})
        self.assertEqual(ctl, [])                                   # 2.11: withheld, never silently replaced
        self.assertIn("malformed", dict(diag["withheld_stored"])[T0])
        ctl, _ = module_controls("liq_exposure", runs, T0 + H)
        self.assertTrue(ctl[0]["hour_closed_at_selection"])


DAY = 24 * H


class DiagnosticsAndVersionTests(unittest.TestCase):
    @new_only
    def test_closed_partial_missing_and_delay(self):
        runs = [run_(T0 + 20 * MINUTE), run_(T0 + 2 * H + 15 * MINUTE), run_(T0 + 3 * H + 5 * MINUTE)]
        _, d = module_controls("options_disagreement", runs, T0 + 3 * H + 30 * MINUTE)
        self.assertEqual((d["hours_covered"], d["closed_hours"], d["partial_hour"]), (4, 3, T0 + 3 * H))
        self.assertEqual(d["selected"], 3)
        self.assertEqual([h for h, _ in d["missing_closed_hours"]], [T0 + H])
        self.assertEqual(d["delay_from_hour_to_availability_min"]["min"], round(5 + 100 / 60, 1))

    @new_only
    def test_accounting_separates_immaturity_and_thinning_from_collection(self):
        e = lambda t: {"group": "control_long", "t_available": t, "live_status": None, "t_persisted": t}
        lab_ = lambda st, a, b: {60: {"status": st, "entry_t": a, "exit_t": b} if st == "complete" else {"status": st}}
        labelled = [(e(T0), lab_("complete", T0, T0 + H), {"x": 1}),
                    (e(T0 + 30 * MINUTE), lab_("complete", T0 + 30 * MINUTE, T0 + 90 * MINUTE), None),
                    (e(T0 + 2 * H), lab_("incomplete", 0, 0), {"x": 1}),
                    (e(T0 + 5 * H), lab_("immature", 0, 0), {"x": 1})]
        d = {"outcome": {"horizons_min": [60], "primary_horizon": 60}}
        acc = evidence.control_accounting(d, {"registered": T0 - H}, labelled, T0 + 5 * H)
        self.assertEqual(acc["by_horizon"]["60"]["evaluation"],
                         {"selected": 4, "mature": 3, "incomplete": 1, "scorable": 2, "retained": 1, "baseline_usable": 1})

    @new_only
    def test_helper_is_hashed_into_b_c_f_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            for rel in ["lab", "schema.py", "enrich.py", "hlsample.py", "optionsbook.py", "stream"]:
                src = ROOT / rel
                (shutil.copytree(src, Path(tmp, rel), ignore=shutil.ignore_patterns("__pycache__")) if src.is_dir()
                 else shutil.copy(src, Path(tmp, rel)))
            ver = lambda: {p.stem: versioning.version_id(versioning.components(tmp, experiments.load_design(p)))
                           for p in experiments.design_files(tmp)}
            v0 = ver()
            p = Path(tmp, "lab/controls.py")
            src = p.read_text()
            p.write_text(src.replace(f'POLICY = "{controls.POLICY}"', 'POLICY = "hourly-x"'))
            self.assertNotEqual(p.read_text(), src)
            v1 = ver()
            changed = sorted(k for k in v0 if v0[k] != v1[k])
            self.assertEqual(changed, ["B1-underwater-adds", "C1-liquidation-cluster", "F1-options-perp-disagreement"])

    @new_only
    def test_report_labels_and_horizon_rule(self):
        import report
        self.assertNotIn("lab-2.0)", (ROOT / "report.py").read_text())
        card = {"design": "X", "evaluation_version": "ev", "status": "exploratory", "status_reason": "r", "module": "m",
                "condition": "q?", "primary_horizon_min": 60, "min_retained_observations": 100, "passes": {},
                "horizons": {"primary_min": 60, "secondary_min": [30], "rule": evidence.HORIZON_RULE},
                "comparison_coverage": {"policy": {"policy": evidence.BAR_BASED}, "by_horizon": None,
                                        "decision_timing": None}}
        text = evidence.report([card], T0, {"cutoff": T0, "code_sha256": "0" * 12})
        self.assertIn("primary 60 min (decides status and proposals); secondary 30 min (descriptive only)", text)
        self.assertIn("secondary horizons are descriptive", evidence.skill_proposals([card], T0))
        self.assertTrue(report.REPORT_VERSION.startswith("report-2.6"))


if __name__ == "__main__":
    unittest.main()
