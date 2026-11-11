"""Research clocks cannot be restarted by accident (repo 2.30.10).

Two identities decide whether a prospective record continues: a market study's registered implementation identity
(research_tools/*/core.py identity(): a drift makes the study refuse to run) and a lab design's evaluation version
(lab/versioning.py: a new version starts a new clock and retires the evidence gathered so far). Both were only
discovered at run time, after a merge. These tests make the release gate say so first.

The lab version hashes `ast.dump` output, which differs between Python minor versions: under 3.13 every design
gets a different version from the one 3.12 registered. So the interpreter is part of the identity, and the
workflows' pin is guarded here too.
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PINNED = (3, 12)                      # the interpreter every workflow installs, and the one the versions were registered under
STUDIES = ("market_studies", "state_v2", "options_pilot", "options_30d")


class MarketStudyIdentity(unittest.TestCase):
    def test_every_registered_study_identity_matches_this_tree(self):
        seen = 0
        for name in STUDIES:
            core = __import__(f"research_tools.{name}.core", fromlist=["core"])
            for row in core.Journal(ROOT, "registration").rows:
                registered = row["data"].get("identity")
                if not isinstance(registered, dict):
                    continue
                seen += 1
                current = core.identity()
                drift = sorted(k for k in set(registered) | set(current) if registered.get(k) != current.get(k))
                self.assertEqual(drift, [], f"{name} [{row['id']}]: these files differ from the registered identity. "
                                 "The study would refuse to run ('identity drift: new version/clock required'). "
                                 "Revert the change, or register a new protocol version in a new directory.")
        self.assertGreaterEqual(seen, 4, "expected the four registered studies' identities in streams/market-studies")


class LabEvaluationVersions(unittest.TestCase):
    def test_workflows_pin_the_interpreter_the_versions_were_registered_under(self):
        pins = {}
        for wf in sorted((ROOT / ".github/workflows").glob("*.yml")):
            for v in re.findall(r"python-version:\s*['\"]?([0-9.]+)", wf.read_text()):
                pins.setdefault(v, []).append(wf.name)
        self.assertEqual(sorted(pins), ["%d.%d" % PINNED],
                         "Every workflow must install Python %d.%d: lab evaluation versions hash ast.dump output, which "
                         "changes between minor versions, so another interpreter restarts every lab clock. %r"
                         % (PINNED + (pins,)))

    @unittest.skipUnless(sys.version_info[:2] == PINNED,
                         "evaluation versions are only comparable under Python %d.%d (ast.dump differs)" % PINNED)
    def test_current_evaluation_versions_are_the_registered_ones(self):
        from lab import experiments
        index = json.loads((ROOT / "research/evidence/index.json").read_text())["designs"]
        ops = json.loads((ROOT / "research_lab_ops.json").read_text())
        declared = {(c["design"], c["new_version"]) for c in ops.get("version_changes", [])}
        for path in experiments.design_files(ROOT):
            d = experiments.attach_version(ROOT, experiments.load_design(path))
            current = (index.get(d["id"]) or {}).get("current")
            if current is None:
                continue                                  # a design that has never run has no clock to restart
            self.assertTrue(d["_version"] == current or (d["id"], d["_version"]) in declared,
                            f"{d['id']}: this tree computes {d['_version']}, the registered current version is {current}. "
                            "Merging would start a new prospective clock and retire the evidence gathered so far. If that "
                            "is intended, declare it under version_changes in research_lab_ops.json (design, new_version, "
                            "reason).")


if __name__ == "__main__":
    unittest.main()
