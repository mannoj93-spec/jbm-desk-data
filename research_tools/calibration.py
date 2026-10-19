"""Calibration diagnostics for new evaluation versions (calibration-1.0.0, repo 2.29; brief section 15).

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

VERSION = "calibration-1.0.0"


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


def block_bootstrap_ci(xs, blocks, alpha, B=2000, seed=1, min_blocks=20, min_tail_draws=1):
    """Percentile interval of the mean, resampling whole blocks. blocks: a block id per observation."""
    groups = {}
    for x, b in zip(xs, blocks):
        groups.setdefault(b, []).append(x)
    keys = sorted(groups)
    if len(keys) < min_blocks:
        return {"state": "insufficient-blocks", "blocks": len(keys), "min_blocks": min_blocks, "n": len(xs)}
    res = resolution(B, alpha, 1, 1)
    if res["expected_tail_draws"] < min_tail_draws:
        return {"state": "insufficient-resolution", "resolution": res, "blocks": len(keys), "n": len(xs)}
    rnd = random.Random(seed)
    means = []
    for _ in range(B):
        tot, n = 0.0, 0
        for _ in keys:
            g = groups[keys[rnd.randrange(len(keys))]]
            tot += sum(g)
            n += len(g)
        means.append(tot / n)
    return {"state": "ok", "mean": sum(xs) / len(xs), "lo": _pct(means, alpha / 2), "hi": _pct(means, 1 - alpha / 2),
            "blocks": len(keys), "n": len(xs), "resolution": res}


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
