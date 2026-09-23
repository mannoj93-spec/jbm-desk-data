"""Simple predictive baseline, estimated on earlier data only (lab-2.0).

Every labelled observation (event or control) gets the same three baseline features, computed
as-of its decision time from the stored BTCUSDT perp bars and the settled funding series:
  prior_ret_60m_aligned  direction x ln(last close / open 60 minutes earlier), last bar available
  prior_rv_60m           sqrt(sum of squared 1-minute log returns over those 60 minutes)
  funding_aligned        direction x the latest settled 8h funding rate available (positive =
                         the position would have been paying)
An observation missing any of them is excluded from the baseline analysis and counted; it is
never filled.

Model: ordinary least squares y ~ 1 + features, fitted on CONTROL observations (both directions)
whose labels had matured - exit_t <= the start of the UTC day of the observation being predicted.
So every prediction is out-of-sample in time and never sees an outcome that ended after the
decision it predicts; the fit is refreshed once per UTC day. A prediction needs >= MIN_TRAIN
training rows, otherwise the baseline is "unidentifiable" for that observation. Added value is
measured on residuals (y - prediction): test residuals versus reference residuals (for a control
reference, the controls' own out-of-sample residuals).
"""
import math

from lab import stats
from lab.common import DAY, MINUTE

FEATURES = ("prior_ret_60m_aligned", "prior_rv_60m", "funding_aligned")
MIN_TRAIN = 40


def features_at(bars, known_funding, t_decision, direction):
    """Baseline features using only bars and funding available by t_decision (None if any is missing)."""
    last = (t_decision // MINUTE) * MINUTE - MINUTE
    while last in bars and bars[last]["avail"] > t_decision:   # newest bar not yet available: step back
        last -= MINUTE
    seq = [bars.get(last - k * MINUTE) for k in range(59, -1, -1)]
    if any(b is None or b["avail"] > t_decision for b in seq):
        return None
    closes = [seq[0]["o"]] + [b["c"] for b in seq]
    ret = math.log(closes[-1] / closes[0])
    rv = math.sqrt(sum(math.log(b / a) ** 2 for a, b in zip(closes, closes[1:])))
    f = known_funding.latest(t_decision, t_decision) if known_funding else None
    if f is None:
        return None
    return {"prior_ret_60m_aligned": direction * ret, "prior_rv_60m": rv, "funding_aligned": direction * f[1]}


class Baseline:
    """Out-of-sample predictions from controls with matured labels."""
    def __init__(self, controls, features=FEATURES):
        # controls: list of dicts with entry_t, exit_t, y and the feature keys
        self.rows = sorted((c for c in controls if all(c.get(k) is not None for k in features)),
                           key=lambda c: c["exit_t"])
        self.features, self.cache = features, {}

    def predict(self, obs):
        if any(obs.get(k) is None for k in self.features):
            return None, "missing baseline input"
        day = obs["entry_t"] // DAY * DAY
        if day not in self.cache:
            train = [c for c in self.rows if c["exit_t"] <= day]
            beta = None
            if len(train) >= MIN_TRAIN:
                beta = stats.ols([[1.0] + [c[k] for k in self.features] for c in train], [c["y"] for c in train])
            self.cache[day] = (beta, len(train))
        beta, n = self.cache[day]
        if beta is None:
            return None, f"unidentifiable ({n} matured control labels before this day; needs {MIN_TRAIN})"
        return beta[0] + sum(b * obs[k] for b, k in zip(beta[1:], self.features)), None
