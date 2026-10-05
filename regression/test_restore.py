"""restore_failed_run (repo 2.26): a failed-push collector artifact is verified by digest, only rows whose identity
the repository lacks are kept, byte-identical, outside the live files, with an append-only receipt; superseded rows,
the live files and the cadence records are untouched; reruns are idempotent; a wrong digest is refused."""
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import restore_failed_run as R   # noqa: E402


def zipped(files):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for k, v in files.items():
            z.writestr(k, v)
    return buf.getvalue()


class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        (self.base / "data/snap").mkdir(parents=True)
        (self.base / "data/prices/x").mkdir(parents=True)
        (self.base / "data/runs").mkdir(parents=True)
        self.live_snap = '{"t": 1}\n'
        (self.base / "data/snap/2026-10.jsonl").write_text(self.live_snap)
        (self.base / "data/prices/x/2026-10.jsonl").write_text('{"t": 5, "o": 2, "observed_at": 9}\n')
        (self.base / "data/runs/2026-10.jsonl").write_text('{"t": 1, "mode": "routine"}\n')
        self.archive = zipped({"data/snap/2026-10.jsonl": '{"t": 1}\n{"t": 2, "books": 17}\n',
                               "data/prices/x/2026-10.jsonl": '{"t": 5, "o": 2, "observed_at": 3}\n',
                               "data/runs/2026-10.jsonl": '{"t": 1, "mode": "routine"}\n{"t": 2, "mode": "routine", "run_id": "9"}\n',
                               "state/checkpoints.json": "{}"})
        self.zip = self.base / "a.zip"
        self.zip.write_bytes(self.archive)
        self.sha = hashlib.sha256(self.archive).hexdigest()

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, sha=None):
        return subprocess.run([sys.executable, str(ROOT / "scripts/restore_failed_run.py"), "--zip", str(self.zip),
                               "--sha256", sha or self.sha, "--run", "9", "--artifact", "77", "--base", str(self.base)],
                              capture_output=True, text=True)

    def test_only_missing_identities_are_kept_outside_the_live_files(self):
        r = self.run_cli()
        self.assertEqual(r.returncode, 0, r.stderr)
        kept = self.base / "data/restored/collector-9/data/snap/2026-10.jsonl"
        self.assertEqual(kept.read_text(), '{"t": 2, "books": 17}\n')                     # byte-identical row
        self.assertFalse((self.base / "data/restored/collector-9/data/prices/x/2026-10.jsonl").exists())  # superseded
        self.assertEqual((self.base / "data/snap/2026-10.jsonl").read_text(), self.live_snap)            # live untouched
        self.assertEqual((self.base / "data/runs/2026-10.jsonl").read_text(), '{"t": 1, "mode": "routine"}\n')
        self.assertTrue((self.base / "data/restored/collector-9/data/runs/2026-10.jsonl").exists())     # evidence only
        rec = [json.loads(l) for l in (self.base / "data/restored/receipts.jsonl").read_text().splitlines()]
        self.assertEqual(len(rec), 1)
        self.assertEqual((rec[0]["run_id"], rec[0]["artifact_sha256"], rec[0]["observed_from_ms"]), ("9", self.sha, 2))
        self.assertIn("not available on time", rec[0]["rule"])
        superseded = {f["path"]: f["superseded"] for f in rec[0]["files"]}
        self.assertEqual(superseded["data/prices/x/2026-10.jsonl"], 1)

    def test_rerun_is_idempotent_and_a_wrong_digest_is_refused(self):
        self.run_cli()
        self.run_cli()
        self.assertEqual((self.base / "data/restored/collector-9/data/snap/2026-10.jsonl").read_text().count("\n"), 1)
        self.assertEqual(len((self.base / "data/restored/receipts.jsonl").read_text().splitlines()), 1)
        r = self.run_cli(sha="0" * 64)
        self.assertEqual(r.returncode, 1)
        self.assertIn("refused", r.stderr)

    def test_restored_tree_is_not_a_lab_input_or_a_cadence_record(self):
        sys.path.insert(0, str(ROOT))
        sys.path.insert(0, str(ROOT / "lab"))
        import run as lab_run   # noqa: E402
        self.assertFalse(any(d.startswith("data/restored") for d in lab_run.INPUT_DIRS))
        import watchdog
        self.run_cli()
        self.assertEqual([r["t"] for r in watchdog.load_runs(self.base)], [1])


if __name__ == "__main__":
    unittest.main()
