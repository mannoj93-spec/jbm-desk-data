"""Narrow, absolute-only tolerance for explicitly enumerated derived floating fields."""
import math

ABS_TOL = 1e-12


def matches(expected, actual, tolerant, path=()):
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and expected.keys() == actual.keys()
                and all(matches(v, actual[k], tolerant, path + (k,)) for k, v in expected.items()))
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(expected) == len(actual)
                and all(matches(v, a, tolerant, path + (i,)) for i, (v, a) in enumerate(zip(expected, actual))))
    if tolerant(path):
        return (type(expected) in (int, float) and type(actual) in (int, float)
                and math.isfinite(expected) and math.isfinite(actual)
                and math.isclose(expected, actual, rel_tol=0, abs_tol=ABS_TOL))
    # Do not let True pass as 1, or NaN pass via container identity shortcuts.
    return type(expected) is type(actual) and expected == actual
