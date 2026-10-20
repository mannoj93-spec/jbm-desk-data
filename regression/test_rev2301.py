"""Repo 2.30.1: post-merge records - O33 v3.1 correction 1's effective record and its check."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("o33_manifest", ROOT / "scripts/o33_v31_manifest.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


class CorrectionEffectiveTests(unittest.TestCase):
    def test_recorded_first_main_evidence(self):
        e = json.loads((ROOT / "research/registrations/o33-v3.1-correction-1/effective.json").read_text())
        self.assertEqual((e["effective_utc"], e["evidence"]["merge_commit"], e["evidence"]["pull_request"]),
                         ("2026-10-20T12:14:00Z", "d26ab3295091290a4f1a84bba5c9531c609613ba", 48))
        self.assertEqual(M.check(), [])

    def test_inconsistent_record_is_reported(self):
        e = json.loads((ROOT / "research/registrations/o33-v3.1-correction-1/effective.json").read_text())
        e["effective_utc"] = "2026-10-20T12:00:00Z"                       # not the activity record's time
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "effective.json"
            p.write_text(json.dumps(e))
            self.assertTrue(M._effective_problems(p, "o33-v3.1-correction-1"))


if __name__ == "__main__":
    unittest.main()
