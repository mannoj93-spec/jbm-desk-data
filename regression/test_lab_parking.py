"""Parked lab designs (research_lab_ops.json, scripts/lab_designs.py, feasibility.py; repo 2.30.10)."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("lab_designs", ROOT / "scripts/lab_designs.py")
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)
import feasibility as F   # noqa: E402

ENTRY = {"design": "B1", "decided": "2026-11-11", "by": "operator", "reason": "no episodes"}


class Selection(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        (self.base / "lab/designs").mkdir(parents=True)
        for i in ("A1", "B1", "C1"):
            (self.base / f"lab/designs/{i}.json").write_text(json.dumps({"id": i}))

    def ops(self, parked, schema=L.SCHEMA):
        (self.base / L.OPS).write_text(json.dumps({"schema": schema, "parked": parked}))

    def test_no_file_runs_everything_and_a_parked_design_is_left_out(self):
        self.assertEqual(L.active(self.base), ["A1", "B1", "C1"])
        self.ops([ENTRY])
        self.assertEqual(L.active(self.base), ["A1", "C1"])
        self.assertEqual(L.parked(self.base), {"B1": ENTRY})

    def test_bad_operations_files_fail_closed(self):
        cases = [[dict(ENTRY, design="Z9")],                          # not a design: a typo must not unpark silently
                 [ENTRY, ENTRY],                                        # twice
                 [{"design": "B1"}], [dict(ENTRY, reason="")], ["B1"],  # incomplete entries
                 [dict(ENTRY, design=i) for i in ("A1", "B1", "C1")]]   # nothing left to run
        for parked in cases:
            self.ops(parked)
            with self.assertRaises(ValueError, msg=parked):
                L.active(self.base)
        self.ops([ENTRY], schema="other")
        with self.assertRaises(ValueError):
            L.active(self.base)
        (self.base / L.OPS).write_text("{not json")
        with self.assertRaises(ValueError):
            L.active(self.base)

    def test_repository_file_parks_real_designs_and_the_lab_accepts_the_list(self):
        act, off = L.active(), L.parked()
        self.assertEqual(sorted(act + list(off)), sorted(L.design_ids()))
        self.assertTrue(act)
        from lab import run                                             # the lab's own option, unchanged
        src = Path(run.__file__).read_text()
        self.assertIn('ap.add_argument("--designs"', src)
        wf = (ROOT / ".github/workflows/research.yml").read_text()
        self.assertIn('designs="$(python scripts/lab_designs.py)"', wf)
        self.assertIn('--designs "$designs"', wf)


class Feasibility(unittest.TestCase):
    def test_a_parked_design_is_labelled_and_given_no_checkpoint_estimate(self):
        doc = F.build(ROOT)
        off = L.parked()
        rows = {r["id"]: r for r in doc["lab"]}
        self.assertTrue(set(off) <= set(rows))
        for i in off:
            self.assertEqual(rows[i]["parked"]["by"], off[i]["by"])
            self.assertNotIn("parked", rows[i]["limiting_factor"])      # the measured factor is kept (desk/test_streams.py)
            self.assertIsNone(rows[i].get("time_to_checkpoint"))
        for i in set(rows) - set(off):
            self.assertNotIn("parked", rows[i])
        text = F.markdown(doc)
        self.assertEqual(text.count("; parked |"), len(off))
        self.assertEqual(text.count("- **Parked** "), len([i for i in off if "calendar_exposure" in rows[i]]))

    def test_an_unreadable_operations_file_is_reported_not_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "research_lab_ops.json").write_text("{broken")
            self.assertIn("unreadable", F.parked_designs(tmp)["?"]["reason"])
            self.assertEqual(F.parked_designs(Path(tmp) / "nowhere"), {})


if __name__ == "__main__":
    unittest.main()
