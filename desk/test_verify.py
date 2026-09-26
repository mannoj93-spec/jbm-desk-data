#!/usr/bin/env python3
"""The O21 numerical-replay verifier as a gate (crypto-desk 12.2, repo 2.17): integrity (exact stored bytes) and
numerical equivalence (summary and rows, per value) are separate; a genuine failure exits nonzero.
The full rerun (~50 s) is exercised by CI (`o21_reanalysis.py verify`); these tests inject reruns.
Run: PYTHONDONTWRITEBYTECODE=1 python3 test_verify.py
"""
import copy
import gzip
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

DESK = Path(__file__).resolve().parent
O21 = DESK / "research/o21"
sys.path[:0] = [str(DESK / "research"), str(DESK), str(DESK.parent)]

try:
    import o21_reanalysis as V       # noqa: E402
    HAVE = (O21 / "reanalysis_12.0.json").exists()
except ImportError:
    HAVE = False


class TestCompare(unittest.TestCase):
    @unittest.skipUnless(HAVE, "needs desk/research")
    def test_per_value_tolerance_and_exact_categories(self):
        a = {"x": 1.0, "y": [1e-3, 2.0], "sel": "B2", "flag": True}
        ok = V.compare_values(a, {"x": 1.0 + 1e-12, "y": [1e-3 + 1e-13, 2.0], "sel": "B2", "flag": True})
        self.assertEqual((ok["violations"], ok["structural"], ok["categorical"], ok["values"]), ([], [], [], 3))
        bad = V.compare_values(a, {"x": 1.0 + 1e-6, "y": [1e-3, 2.0], "sel": "B1", "flag": True})
        self.assertEqual(len(bad["violations"]), 1)
        self.assertEqual(bad["categorical"], [".sel: 'B2' vs 'B1'"])
        miss = V.compare_values(a, {"x": 1.0, "y": [1e-3], "sel": "B2"})
        self.assertEqual(len(miss["structural"]), 2)                     # missing key and a shorter list
        # per value: a small number cannot hide behind a large one's relative scale
        self.assertEqual(len(V.compare_values([1e-3, 1e6], [1e-3 + 1e-8, 1e6])["violations"]), 1)


@unittest.skipUnless(HAVE, "needs desk/research")
class TestVerifyGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stored = json.loads((O21 / "reanalysis_12.0.json").read_text())
        cls.rows = json.loads(gzip.decompress((O21 / cls.stored["rows_file"]["path"]).read_bytes()))

    def rerun(self, mutate=None):
        def f(o21):
            s, r = copy.deepcopy(self.stored), copy.deepcopy(self.rows)
            s["rows_file"] = dict(s["rows_file"], sha256_uncompressed="f" * 64)   # rerun bytes differ: allowed
            s["code"] = {"range_contract": "contract-x"}
            if mutate:
                mutate(s, r)
            return s, r
        return f

    def num_path(self, rows):
        for i, row in enumerate(rows):
            for k, v in (row.items() if isinstance(row, dict) else []):
                if isinstance(v, float):
                    return i, k
        raise AssertionError("no float in rows")

    def test_tolerated_rounding_passes(self):
        def m(s, r):
            i, k = self.num_path(r)
            r[i][k] += 1e-12
        code, res = V.verify(rerun=self.rerun(m))
        self.assertEqual(code, 0, res)
        self.assertFalse(res["provenance"]["rerun_bytes_identical"])

    def test_material_change_fails(self):
        def m(s, r):
            i, k = self.num_path(r)
            r[i][k] *= 1.001
        code, res = V.verify(rerun=self.rerun(m))
        self.assertEqual((code, res["numerical"]["violation_counts"]["rows"]), (2, 1))

    def test_missing_row_fails(self):
        code, res = V.verify(rerun=self.rerun(lambda s, r: r.pop()))
        self.assertEqual(code, 2)
        self.assertEqual(res["numerical"]["violation_counts"]["structural"], 1)

    def test_changed_conclusion_fails(self):
        def m(s, r):
            h = sorted(s["horizons"])[0]
            s["horizons"][h]["selected_holm"] = "B0"
        self.assertEqual(V.verify(rerun=self.rerun(m))[0], 2)

    def test_altered_stored_bytes_fail_integrity(self):
        tmp = Path(tempfile.mkdtemp())
        shutil.copytree(O21, tmp / "o21")
        p = tmp / "o21" / self.stored["rows_file"]["path"]
        raw = bytearray(gzip.decompress(p.read_bytes()))
        raw[100] = ord("9") if raw[100] != ord("9") else ord("8")
        p.write_bytes(gzip.compress(bytes(raw)))
        code, res = V.verify(o21=tmp / "o21", rerun=self.rerun())
        self.assertEqual(code, 1)
        self.assertIn("stored rows", res["integrity"]["failures"][0])
        shutil.rmtree(tmp)

    def test_command_exit_status(self):
        saved = V.verify
        try:
            for code in (0, 1, 2):
                V.verify = lambda code=code: (code, {})
                self.assertEqual(V.main(["x", "verify"]), code)
        finally:
            V.verify = saved


if __name__ == "__main__":
    unittest.main(verbosity=1)
