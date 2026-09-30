#!/usr/bin/env python3
"""release.json drift check (crypto-desk 12.0): modules, calendar, frozen spec and manifest hash agree.
12.4: generation identity - the forecast job records the manifest's package, in its own release family, and
every production forecast's package label agrees with its job version or is covered by a provenance correction."""
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


class TestGenerationIdentity(unittest.TestCase):
    JOB = DESK / "range_job.py"

    @unittest.skipUnless((DESK / "range_job.py").exists(), "the forecast job lives in the repository only")
    def test_literal_or_mismatched_package_is_refused(self):
        import shutil
        import tempfile
        tmp = Path(tempfile.mkdtemp())
        try:
            for f in ("release.json", "range_job.py"):
                shutil.copy(DESK / f, tmp / f)
            doc = json.loads((DESK / "release.json").read_text())
            self.assertEqual(M._generation_identity(tmp, doc), [])
            src = self.JOB.read_text()
            # the 12.3 defect: a typed package beside a newer job version
            (tmp / "range_job.py").write_text(src.replace("PACKAGE = release_package()", 'PACKAGE = "crypto-desk 12.2"'))
            self.assertIn("range_job.py: PACKAGE is a literal; it must be read from release.json",
                          M._generation_identity(tmp, doc))
            (tmp / "range_job.py").write_text(src)
            self.assertTrue(any("release family" in p for p in M._generation_identity(tmp, dict(doc, package="crypto-desk 9.9"))))
        finally:
            shutil.rmtree(tmp)

    def test_family_parser(self):
        self.assertEqual((M._family("range-job-12.4.0"), M._family("crypto-desk 12.4"), M._family(None)), ("12.4", "12.4", None))

    @unittest.skipUnless((DESK.parent / "state/forecast_manifest.json").exists(), "needs the repository's registry")
    def test_production_labels_agree_or_are_corrected(self):
        base = DESK.parent
        rows = [json.loads(x) for x in (DESK / "provenance_corrections.jsonl").read_text().splitlines() if x.strip()]
        for r in rows:
            self.assertTrue({"event", "field", "recorded_as", "correct_value", "selector", "revision"} <= set(r), r)
        m = json.loads((base / "state/forecast_manifest.json").read_text())
        corrected, bad = 0, []
        for fid, e in sorted(m.items()):
            if not fid.startswith("range-rc1d-"):
                continue
            doc = json.loads((base / e["frozen"]).read_bytes())
            job = doc["code_version"].split(" / ")[-1]
            if M._family(doc.get("package")) == M._family(job):
                continue
            if any(r["field"] == "package" and job == r["selector"]["code_version_endswith"]
                   and doc.get("package") == r["selector"]["field_value"] for r in rows):
                corrected += 1
                continue
            bad.append(f"{fid}: {doc.get('package')} vs {job}")
        self.assertEqual(bad, [])
        listed = rows[0]["listed"]["ids"]
        self.assertTrue(all(i in m for i in listed))       # every listed record exists and is covered by the rule
        self.assertGreaterEqual(corrected, len(listed))


@unittest.skipUnless((DESK / "check_package.py").exists(), "the startup runner ships in the skill folder")
class TestStartupRunner(unittest.TestCase):
    """12.4: an early failing test file followed by a passing one leaves the startup result nonzero (the 12.3
    shell loop exited 0); counts are reported separately."""

    def test_early_failure_then_success_stays_failed(self):
        import shutil
        import subprocess
        import tempfile
        sys.path.insert(0, str(DESK))
        import check_package as P
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "test_a.py").write_text("import unittest\nclass T(unittest.TestCase):\n    def test_x(self):\n"
                                           "        self.fail('boom')\n    @unittest.skip('s')\n    def test_y(self):\n"
                                           "        pass\nunittest.main()\n")
            (tmp / "test_b.py").write_text("import unittest\nclass T(unittest.TestCase):\n    def test_z(self):\n"
                                           "        pass\nunittest.main()\n")
            res = P.run_tests(tmp, ["test_a.py", "test_b.py"])
            self.assertEqual([r["passed"] for r in res], [False, True])
            self.assertEqual(P.totals(res), "tests: 2 files, 1 passed; executed 3, failed 1, errors 0, skipped 1; "
                                            "failing files: test_a.py")
            loop = subprocess.run(["bash", "-c", "for t in test_*.py; do python3 $t; done"], cwd=tmp,
                                  capture_output=True)
            self.assertEqual(loop.returncode, 0)          # the 12.3 documented loop hides the failure
        finally:
            shutil.rmtree(tmp)


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
            with self.assertRaises(ValueError):          # retained.RetainedError: missing input, named
                O.load_inputs()
        finally:
            O.O21 = saved
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main(verbosity=1)
