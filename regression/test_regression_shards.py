"""The regression shard split (scripts/run_regression_shard.py, repo 2.30.10): complete, disjoint, deterministic."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_regression_shard", ROOT / "scripts/run_regression_shard.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)


class Fake:
    """Stands in for a test case: only its class identity matters to the split."""


def cases(module, names, per_class=3):
    out = []
    for n in names:
        cls = type(n, (Fake,), {"__module__": module})
        out += [cls() for _ in range(per_class)]
    return out


class SplitTests(unittest.TestCase):
    def setUp(self):
        self.tests = (cases("test_acceptance", ["A", "B", "C", "D", "E"]) + cases("test_health", ["H1", "H2"])
                      + cases("regression.test_acceptance", ["P"]) + cases("unittest.loader", ["_FailedTest"], 1))

    def test_every_test_is_in_exactly_one_shard_for_any_count(self):
        for count in (1, 2, 3, 4, 7):
            parts = S.shards(self.tests, count)
            self.assertEqual(len(parts), count)
            self.assertEqual(sorted(map(id, self.tests)), sorted(id(t) for p in parts for t in p), count)

    def test_slow_classes_are_spread_and_everything_else_runs_last(self):
        parts = S.shards(self.tests, 3)
        mods = [{type(t).__module__ for t in p} for p in parts]
        self.assertTrue(all(m <= {"test_acceptance", "regression.test_acceptance"} for m in mods[:2]))
        self.assertEqual(mods[2], {"test_health", "unittest.loader"})          # an import failure fails the last shard
        self.assertEqual([len(p) for p in parts[:2]], [9, 9])                  # six slow classes, three each
        self.assertEqual(len({type(t) for t in parts[0]} & {type(t) for t in parts[1]}), 0)   # a class is never split

    def test_one_shard_is_the_whole_suite_and_the_split_is_deterministic(self):
        self.assertEqual(S.shards(self.tests, 1), [self.tests])
        owners = [S.owner(t) for t in self.tests]
        self.assertEqual(S.assign(owners, 3), S.assign(list(reversed(owners)), 3))
        for bad in (0, -1, True, 2.0, "3"):
            with self.assertRaises(ValueError):
                S.assign(owners, bad)

    def test_bad_arguments_run_nothing(self):
        for argv in (["x"], ["x", "3", "3"], ["x", "-1", "3"], ["x", "a", "b"]):
            self.assertEqual(S.main(argv), 2)


if __name__ == "__main__":
    unittest.main()
