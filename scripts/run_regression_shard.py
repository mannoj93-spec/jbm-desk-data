#!/usr/bin/env python3
"""run_regression_shard - run one shard of the regression suite (repo 2.30.10).

    python scripts/run_regression_shard.py INDEX COUNT [-v]

The suite is discovered exactly as `python -m unittest discover -s regression` discovers it and then split.
Every discovered test belongs to exactly one shard, so the shards together are the whole suite: a new test file
needs no list to be edited, and none can be dropped by a list going stale. Test classes are dealt round-robin
across all shards in name order, the classes of the slow module (SLOW) first so they are spread evenly; a module
that failed to import is dealt like any class and fails the shard it lands in. COUNT=1 is the whole suite.
(2.30.10 put everything but the slow module in the last shard; measured in CI that shard took 10 minutes beside
3 and 1.5, so 2.30.12 deals every class.)

The split is checked before anything runs (the shards are disjoint and their union is the discovery); a failed
check exits 2 without running a test. Prints `shard I/N: K of TOTAL tests` first. Exit 1 when a test fails.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLOW = ("test_acceptance",)


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def owner(test):
    """(module, class) a test is assigned by; a loader failure has no class of its own."""
    cls = type(test)
    return cls.__module__, cls.__qualname__


def assign(owners, count):
    """{owner: shard index} for the distinct owners. Deterministic in the owners' names only."""
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise ValueError("shard count must be a positive integer")
    owners = sorted(set(owners), key=lambda o: (o[0].split(".")[-1] not in SLOW, o))
    return {o: i % count for i, o in enumerate(owners)}


def shards(tests, count):
    """The tests split into `count` lists, checked: disjoint, and together exactly `tests`."""
    plan = assign([owner(t) for t in tests], count)
    out = [[] for _ in range(count)]
    for t in tests:
        out[plan[owner(t)]].append(t)
    if sum(len(s) for s in out) != len(tests) or {id(t) for s in out for t in s} != {id(t) for t in tests}:
        raise RuntimeError("shard split lost or duplicated a test")
    return out


def main(argv):
    try:
        index, count = int(argv[1]), int(argv[2])
        if not 0 <= index < count:
            raise ValueError
    except (IndexError, ValueError):
        print(__doc__, file=sys.stderr)
        return 2
    tests = list(flatten(unittest.defaultTestLoader.discover(str(ROOT / "regression"))))
    try:
        mine = shards(tests, count)[index]
    except (RuntimeError, ValueError) as exc:
        print(f"shard split failed: {exc}", file=sys.stderr)
        return 2
    print(f"shard {index}/{count}: {len(mine)} of {len(tests)} tests", flush=True)
    result = unittest.TextTestRunner(verbosity=2 if "-v" in argv[3:] else 1).run(unittest.TestSuite(mine))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
