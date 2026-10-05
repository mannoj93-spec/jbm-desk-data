"""Range monitor incident aging on a fixed clock (repo 2.26; no monitor code change). Production example: the
October 4 16:00Z decision was missed; monitor runs 37253599060 (01:59Z) and 37270401324 (06:01Z) correctly failed on
it; at 09:15Z the due-decision window advanced past it (12 h lookback anchored to last_due, 75-minute grace) and run
37293942955 (10:02Z) passed. These fixtures are synthetic; they prove the mechanism, not any future run."""
import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "desk")):
    if p not in sys.path:
        sys.path.insert(0, p)
import range_monitor as M   # noqa: E402
import health as H          # noqa: E402

UTC = dt.timezone.utc
MISSED = "2026-10-04T16:00:00Z"


def t(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def iso(d):
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


class Fixture:
    """Decisions from Oct 4 00:00Z to `upto`, each published by an eligible production attempt except `missing`."""
    def __init__(self, d, upto, missing=(MISSED,), status_at=None, current_state="valid-current", backlog=False):
        self.d = Path(d)
        for sub in ("state", "reports", "registry", "desk"):
            (self.d / sub).mkdir(parents=True, exist_ok=True)
        (self.d / "desk/release.json").write_text(json.dumps({"range_stream_start_utc": "2026-09-26T04:00:00Z"}))
        att, pubs, manifest = [], [], {}
        k = t("2026-10-04T00:00:00Z")
        while k <= t(upto):
            key = iso(k)
            if key not in missing:
                a = f"{key}#{int(k.timestamp())}"
                att.append({"attempt": a, "decision_utc": key, "state": "published", "run": {"production": True}})
                start = int((k + dt.timedelta(minutes=20)).timestamp() * 1000)
                pubs.append({"attempt": a, "eligible": True, "start_ms": start})
                if backlog and key == "2026-10-04T20:00:00Z":
                    manifest[f"range-rc1d-4h-{k:%Y%m%dT%H%MZ}"] = {"attempt": a}
            k += dt.timedelta(hours=4)
        self.rows("state/range_attempts.jsonl", att)
        self.rows("state/range_publications.jsonl", pubs)
        (self.d / "state/forecast_manifest.json").write_text(json.dumps(manifest))
        gen = t(status_at or upto) + dt.timedelta(minutes=30)
        cur = {h: {"state": current_state, "id": f"range-rc1d-{h}", "valid_until_utc": iso(gen + dt.timedelta(hours=30))}
               for h in ("4h", "24h", "72h")}
        (self.d / "reports/range_status.json").write_text(json.dumps(
            {"generated_utc": iso(gen), "status_expires_utc": iso(gen + dt.timedelta(hours=3)), "current": cur}))

    def rows(self, rel, rows):
        (self.d / rel).write_text("".join(json.dumps(r) + "\n" for r in rows))


class AgingTests(unittest.TestCase):
    def check(self, now, **kw):
        with tempfile.TemporaryDirectory() as d:
            Fixture(d, kw.pop("upto", "2026-10-05T08:00:00Z"), **kw)
            return M.check(d, t(now))

    def test_old_miss_is_active_at_the_inclusive_boundary_then_historical(self):
        # 09:14Z: 74 min after 08:00 -> last_due 04:00, window 16:00 (inclusive) .. 04:00 -> the miss is active
        problems, info = self.check("2026-10-05T09:14:00Z", status_at="2026-10-05T08:00:00Z")
        self.assertEqual(info["decisions"][MISSED], "absent")
        self.assertTrue(any(MISSED in p for p in problems), problems)
        # 09:15Z: the window advances to 20:00 .. 08:00; with every other check healthy the monitor is green
        problems, info = self.check("2026-10-05T09:15:00Z", status_at="2026-10-05T08:00:00Z")
        self.assertEqual(problems, [])
        self.assertNotIn(MISSED, info["decisions"])

    def test_the_miss_stays_in_the_historical_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            Fixture(d, "2026-10-05T08:00:00Z")
            norm, _ = H.range_decisions(d, t("2026-10-05T10:02:00Z"))          # health keeps a 72 h lookback
            self.assertEqual(norm[MISSED], "absent")
            self.assertEqual(norm["2026-10-05T08:00:00Z"], "published")

    def test_a_recent_missing_decision_still_fails(self):
        problems, _ = self.check("2026-10-05T09:20:00Z", missing=(MISSED, "2026-10-05T08:00:00Z"),
                                 status_at="2026-10-05T08:00:00Z")
        self.assertTrue(any("2026-10-05T08:00:00Z" in p for p in problems))

    def test_an_aged_first_failure_does_not_clear_an_ongoing_outage(self):
        # nothing published after the first miss: the first miss ages out, the outage does not
        out = tuple(iso(t(MISSED) + dt.timedelta(hours=4 * i)) for i in range(5))
        problems, _ = self.check("2026-10-05T09:15:00Z", missing=out, status_at="2026-10-04T12:00:00Z")
        self.assertTrue(any(p.startswith("runs:") for p in problems))
        self.assertTrue(any(p.startswith("publication:") for p in problems))
        self.assertTrue(any(p.startswith("freshness:") for p in problems))

    def test_freshness_integrity_and_backlog_fail_independently_of_aging(self):
        p1, _ = self.check("2026-10-05T09:15:00Z", status_at="2026-10-05T04:00:00Z")
        self.assertTrue(any(p.startswith("freshness:") for p in p1), p1)
        p2, _ = self.check("2026-10-05T09:15:00Z", status_at="2026-10-05T08:00:00Z", current_state="integrity-failed")
        self.assertTrue(any("integrity-failed" in p for p in p2), p2)
        p3, _ = self.check("2026-10-05T09:15:00Z", status_at="2026-10-05T08:00:00Z", backlog=True)
        self.assertTrue(any(p.startswith("scoring:") for p in p3), p3)

    def test_later_duplicate_triggers_do_not_rewrite_outcomes(self):
        with tempfile.TemporaryDirectory() as d:
            f = Fixture(d, "2026-10-05T08:00:00Z")
            # a late native run for an already published decision leaves only a lifecycle row (range_job returns
            # "existing" without an attempt); a late run for the missed decision records a stale skip
            f.rows("state/range_runs.jsonl", [{"decision_utc": "2026-10-05T08:00:00Z", "event": "schedule",
                                               "run_id": "9", "stage": "run", "outcome": "success"}])
            att = (Path(d) / "state/range_attempts.jsonl").read_text()
            (Path(d) / "state/range_attempts.jsonl").write_text(att + json.dumps(
                {"attempt": f"{MISSED}#late", "decision_utc": MISSED, "state": "skipped", "run": {"production": True},
                 "reason": "stale decision (3.10h > 1.0h)"}) + "\n")
            norm, _ = H.range_decisions(d, t("2026-10-05T10:02:00Z"))
            self.assertEqual(norm["2026-10-05T08:00:00Z"], "published")
            self.assertTrue(norm[MISSED].startswith("missed"))                  # a late refusal completes nothing


if __name__ == "__main__":
    unittest.main()
