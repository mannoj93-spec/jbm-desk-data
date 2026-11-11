#!/usr/bin/env python3
"""run_regression_shard - run one shard of the regression suite (repo 2.30.10).

    python scripts/run_regression_shard.py INDEX COUNT [-v]

The suite is discovered exactly as `python -m unittest discover -s regression` discovers it and then split.
Every discovered test belongs to exactly one shard, so the shards together are the whole suite: a new test file
needs no list to be edited, and none can be dropped by a list going stale. Classes of the slow module (SLOW) are
dealt round-robin, in name order, across every shard but the last; everything else, including a module that
failed to import, runs in the last shard. COUNT=1 is the whole suite in one shard.

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
    owners = sorted(set(owners))
    if count == 1:
        return {o: 0 for o in owners}
    slow = [o for o in owners if o[0].split(".")[-1] in SLOW]
    out = {o: count - 1 for o in owners}
    for i, o in enumerate(slow):
        out[o] = i % (count - 1)
    return out


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
