"""Calibration diagnostics for new evaluation versions (calibration-1.1.0, repo 2.30; 1.0.0 was repo 2.29).

1.1.0: one tail-draw policy. resolution() calls fewer than 10 expected draws per tail 'coarse', but
block_bootstrap_ci() accepted an interval with a single expected draw (default min_tail_draws=1). Both now use
MIN_TAIL_DRAWS = 10; a caller can still ask for less explicitly, and the result records the policy it used. The
bootstrap draws whole blocks with random.choices over precomputed block sums (same method, faster; the random stream
differs from 1.0.0, which no registered result used). The calibration of the proposed DIR1 evaluator itself is
research_tools/calibration_harness.py.

The frozen lab evaluation (lab/experiments.py) uses B = 2,000 bootstrap resamples and alpha = 0.10 / (variants x 4
looks). At 23 variants the adjusted two-sided tail holds 2000 x 0.10 / 92 / 2 ~ 1.09 expected resampled draws; at
100 variants ~0.25 - fewer than one draw, so the interval endpoint is a single order statistic or less. This module
diagnoses that and simulates false-positive behaviour; it does NOT change the frozen method (successors are
registered; any recalculation here is labelled supplementary).

  resolution(B, alpha, variants, looks)    expected draws in each adjusted tail and a verdict:
                                           ok (>= 10) | coarse (1-10) | insufficient (< 1)
  required_B(alpha, variants, looks, min_tail_draws=10)
  block_bootstrap_ci(xs, blocks, alpha, B, seed)   percentile CI resampling whole dependence blocks; returns
                                           'insufficient-resolution' instead of a number when the tail is too thin,
                                           and 'insufficient-blocks' below min_blocks
  null_false_positive(series, blocks, test, looks, sims, seed)   dependence-preserving null: circularly shift the
                                           signal against the outcomes by whole blocks (keeps each series'
                                           autocorrelation, breaks their link), apply the test at every look, and
                                           report the share of null runs declared at ANY look (the repeated-look
                                           false-positive rate) beside the nominal alpha.
More draws improve numerical resolution; they do not create independent market evidence. Block counts are reported
beside every result.
"""
import math
import random

VERSION = "calibration-1.1.0"
MIN_TAIL_DRAWS = 10


def resolution(B, alpha, variants, looks=4, two_sided=True):
    a = alpha / (variants * looks)
    tail = a / 2 if two_sided else a
    draws = B * tail
    verdict = "ok" if draws >= 10 else "coarse" if draws >= 1 else "insufficient"
    return {"B": B, "adjusted_alpha": a, "tail_probability": tail, "expected_tail_draws": round(draws, 4),
            "verdict": verdict}


def required_B(alpha, variants, looks=4, min_tail_draws=10, two_sided=True):
    tail = alpha / (variants * looks) / (2 if two_sided else 1)
    return int(math.ceil(min_tail_draws / tail))


def _pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = int(math.floor(k)), int(math.ceil(k))
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def block_bootstrap_ci(xs, blocks, alpha, B=2000, seed=1, min_blocks=20, min_tail_draws=MIN_TAIL_DRAWS):
    """Percentile interval of the mean, resampling whole blocks. blocks: a block id per observation."""
    groups = {}
    for x, b in zip(xs, blocks):
        groups.setdefault(b, []).append(x)
    keys = sorted(groups)
    if len(keys) < min_blocks:
        return {"state": "insufficient-blocks", "blocks": len(keys), "min_blocks": min_blocks, "n": len(xs)}
    res = resolution(B, alpha, 1, 1)
    if res["expected_tail_draws"] < min_tail_draws:
        return {"state": "insufficient-resolution", "resolution": res, "blocks": len(keys), "n": len(xs),
                "min_tail_draws": min_tail_draws}
    rnd = random.Random(seed)
    sums = [sum(groups[k]) for k in keys]
    cnts = [len(groups[k]) for k in keys]
    idx = range(len(keys))
    means = []
    for _ in range(B):
        pick = rnd.choices(idx, k=len(keys))
        means.append(sum(map(sums.__getitem__, pick)) / sum(map(cnts.__getitem__, pick)))
    return {"state": "ok", "mean": sum(xs) / len(xs), "lo": _pct(means, alpha / 2), "hi": _pct(means, 1 - alpha / 2),
            "blocks": len(keys), "n": len(xs), "resolution": res, "min_tail_draws": min_tail_draws}


def null_false_positive(signal, outcome, blocks, test, looks, sims=200, seed=7):
    """signal, outcome: aligned lists; blocks: block id per row (ordered). test(sig, out) -> True if 'declared'.
    looks: increasing sample sizes. Each null run circularly shifts the outcome series by a random whole number of
    blocks (at least one), so dependence within each series is kept and the cross link is broken."""
    rnd = random.Random(seed)
    starts = [i for i in range(len(blocks)) if i == 0 or blocks[i] != blocks[i - 1]]
    if len(starts) < 3:
        return {"state": "insufficient-blocks", "blocks": len(starts)}
    declared_any, declared_by_look = 0, [0] * len(looks)
    for _ in range(sims):
        k = starts[rnd.randrange(1, len(starts))]
        out = outcome[k:] + outcome[:k]
        hit = False
        for j, n in enumerate(looks):
            if n <= len(signal) and test(signal[:n], out[:n]):
                declared_by_look[j] += 1
                hit = True
        declared_any += hit
    return {"state": "ok", "sims": sims, "looks": list(looks), "false_positive_any_look": declared_any / sims,
            "false_positive_by_look": [x / sims for x in declared_by_look], "blocks": len(starts)}
