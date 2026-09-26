#!/usr/bin/env python3
"""release.json drift check (crypto-desk 12.0): modules, calendar, frozen spec and manifest hash agree."""
import json
import sys
import unittest
from pathlib import Path

DESK = Path(__file__).resolve().parent
sys.path.insert(0, str(DESK))

import make_release as M      # noqa: E402
import range_contract as C    # noqa: E402


class TestRelease(unittest.TestCase):
    def test_no_drift(self):
        self.assertEqual(M.check(DESK), [])

    def test_contract_matches_code(self):
        doc = json.loads((DESK / "release.json").read_text())
        self.assertEqual((doc["contract"], doc["evaluated_contract"]), (C.contract_id("RC1D"), C.contract_id("RC1")))


@unittest.skipUnless((DESK / "research/o21").exists(), "O21 retained inputs live in the repository only")
class TestResearchRetention(unittest.TestCase):
    """O21 inputs are retained and verified before any replay; altered or missing inputs are detected."""

    def test_inputs_verify_and_tampering_is_detected(self):
        import gzip
        import shutil
        import tempfile
        sys.path.insert(0, str(DESK / "research"))
        import o21_reanalysis as O
        k, d = O.load_inputs()
        self.assertEqual((len(k["rows"]), len(d["rows"])), (14754, 48264))
        tmp = Path(tempfile.mkdtemp())
        saved = O.O21
        try:
            shutil.copytree(saved, tmp / "o21", ignore=shutil.ignore_patterns("reanalysis_*"))
            O.O21 = tmp / "o21"
            p = tmp / "o21/inputs/dvol_1h.json.gz"
            raw = gzip.decompress(p.read_bytes()).replace(b'"dvol": 84.88', b'"dvol": 84.89', 1)
            p.write_bytes(gzip.compress(raw))
            with self.assertRaises(ValueError):
                O.load_inputs()
            p.unlink()
            with self.assertRaises(FileNotFoundError):
                O.load_inputs()
        finally:
            O.O21 = saved
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main(verbosity=1)
