"""Regressions for revision 2.13 (evidence completeness of a publication), reviewed at 16cb49f (2.12).

A valid run reaches a real supported checkpoint (100 retained / 20 blocks) through lab.run.main;
its compute output is handed to the persist job's merge (scripts/merge_research.py) exactly as the
research workflow does, and then damaged: a dependency the card and proposal rely on is removed,
truncated, altered or contradicted. The merge must reject before any write, unless the dependency is
already present and identical in the destination. Helpers come from test_rev212 (synthetic inputs,
real lab, evidence and merge code). Tests named `*_common_api` fail on 16cb49f.
"""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_rev212 as t                                     # noqa: E402

NEW = hasattr(t.merge_research, "completeness_problems")
new_only = unittest.skipUnless(NEW, "2.13 interface")
REL = f"research/v2/{t.DID}/{t.VER}"
CARD = f"research/evidence/v2/{t.KEY}.json"


class CompletenessTests(unittest.TestCase):
    NOW_B = t.BoundaryTests.NOW_B

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        world, self.repo, a = t.BoundaryTests().scenario(self.tmp, malformed=False)
        rc, err, self.inc = t.compute(self.tmp, self.repo, self.NOW_B, world, "b")
        self.assertEqual(rc, 0, err)
        card = json.loads(Path(self.inc, CARD).read_text())
        self.assertEqual(card["status"], "supported")                   # a real supported 100/20 checkpoint
        self.assertEqual(card["checkpoints"]["records"][0]["n"], 100)
        self.assertIn(f"## {t.DID} @ {t.VER}", Path(self.inc, "reports/skill_proposals.md").read_text())

    def tearDown(self):
        self._tmp.cleanup()

    def variant(self, name, mutate):
        d = self.tmp / f"case-{name}"
        shutil.copytree(self.inc, d)
        mutate(d)
        return d

    def rejected(self, name, mutate, code=4):
        before = t.snapshot(self.repo)
        rc, err = t.merge(self.variant(name, mutate), self.repo)
        self.assertIn(rc, code if isinstance(code, tuple) else (code,), f"{name}: {err}")
        self.assertEqual(t.snapshot(self.repo), before, name)          # no partial mutation
        return err

    def new_control_file(self, d):
        stored = {p.name for p in Path(self.repo, REL, "controls").glob("*.jsonl")}
        return sorted(Path(d, REL, "controls").glob("*.jsonl"))[-1], stored

    def test_the_complete_handoff_publishes_preserved(self):
        rc, err = t.merge(self.inc, self.repo)
        self.assertEqual(rc, 0, err)
        self.assertEqual(t.cps_of(self.repo)[1]["verdict"], "supported")
        self.assertIn(f"## {t.DID} @ {t.VER}", Path(self.repo, "reports/skill_proposals.md").read_text())

    def test_a_missing_checkpoint_file_is_rejected_common_api(self):
        self.rejected("no-checkpoint", lambda d: Path(d, REL, "checkpoints.jsonl").unlink())   # 16cb49f: exit 0

    def test_missing_control_files_are_rejected_common_api(self):
        self.rejected("no-controls", lambda d: shutil.rmtree(Path(d, REL, "controls")))          # 16cb49f: exit 0

    def test_missing_or_truncated_rows_are_rejected_common_api(self):
        def drop_control_rows(d):
            p, _ = self.new_control_file(d)
            lines = p.read_text().splitlines()
            p.write_text("\n".join(lines[:-3]) + "\n")
        def cut_mid_line(d):
            p = Path(d, REL, "checkpoints.jsonl")
            p.write_text(p.read_text()[:-200])
        def drop_events(d):
            shutil.rmtree(Path(d, REL, "events"))
        self.rejected("control-rows", drop_control_rows)
        self.rejected("truncated-checkpoint", cut_mid_line, code=(3, 4))     # unreadable: caught by either gate
        self.rejected("no-events", drop_events)

    @new_only
    def test_incorrect_hashes_are_rejected(self):
        def alter_checkpoint(d):
            p = Path(d, REL, "checkpoints.jsonl")
            rec = json.loads(p.read_text())
            rec["completed_at"] += 0                                     # same content, re-serialized
            rec["checks"]["blocks"]["value"] += 1                        # a changed record
            p.write_text(json.dumps(rec) + "\n")
        def alter_control(d):
            p, _ = self.new_control_file(d)
            lines = p.read_text().splitlines()
            r = json.loads(lines[-1])
            r["features"] = {"severity": 2.0}
            p.write_text("\n".join(lines[:-1] + [json.dumps(r, sort_keys=True)]) + "\n")
        def declared(d, fn):
            for rel in ("lab-summary.json", CARD):
                obj = json.loads(Path(d, rel).read_text())
                inv = obj["designs"][t.DID]["inventory"] if rel == "lab-summary.json" else obj["evidence_inventory"]
                fn(inv)
                Path(d, rel).write_text(json.dumps(obj))
        def wrong_record_sha(d):
            declared(d, lambda inv: inv["checkpoints"][0].update(record_sha256="0" * 64))
        def wrong_control_fp(d):
            declared(d, lambda inv: inv["controls"].update(fingerprint="0" * 64))
        for name, fn in (("checkpoint-content", alter_checkpoint), ("control-content", alter_control),
                         ("declared-record-sha", wrong_record_sha), ("declared-control-fp", wrong_control_fp)):
            self.rejected(name, fn)

    @new_only
    def test_the_inventory_itself_is_required(self):
        def no_inventory(d):
            for rel, path in (("lab-summary.json", ("designs", t.DID, "inventory")), (CARD, ("evidence_inventory",))):
                obj = json.loads(Path(d, rel).read_text())
                o = obj
                for k in path[:-1]:
                    o = o[k]
                o[path[-1]] = None
                Path(d, rel).write_text(json.dumps(obj))
        self.assertIn("evidence inventory missing", self.rejected("no-inventory", no_inventory))

    def test_dependencies_already_present_and_identical_are_accepted_common_api(self):
        rc, err = t.merge(self.inc, self.repo)
        self.assertEqual(rc, 0, err)
        before = t.snapshot(self.repo)
        d = self.variant("already-present", lambda d: (Path(d, REL, "checkpoints.jsonl").unlink(),
                                                       shutil.rmtree(Path(d, REL, "controls"))))
        rc, err = t.merge(d, self.repo)
        self.assertEqual(rc, 0, err)
        self.assertEqual(t.snapshot(self.repo), before)                # nothing rewritten or duplicated

    def test_a_conflicting_stored_winner_is_rejected_common_api(self):
        p, stored = self.new_control_file(self.inc)
        rec = json.loads(p.read_text().splitlines()[-1])
        other = dict(rec, t_event=rec["t_event"] + 1, control_key="other-writer")
        dst = Path(self.repo, REL, "controls", p.name)
        with open(dst, "a") as fh:
            fh.write(json.dumps(other, sort_keys=True) + "\n")
        self.rejected("conflict", lambda d: None, code=3)


if __name__ == "__main__":
    unittest.main()
