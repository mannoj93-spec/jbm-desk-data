"""Simple predictive baseline, estimated on earlier data only (lab-2.0; one model per horizon since lab-2.1).

Every labelled observation (event or control) gets the same three baseline features, computed
as-of its decision time from the stored BTCUSDT perp bars and the settled funding series:
  prior_ret_60m_aligned  direction x ln(last close / open 60 minutes earlier), last bar available
  prior_rv_60m           sqrt(sum of squared 1-minute log returns over those 60 minutes)
  funding_aligned        direction x the latest settled 8h funding rate available (positive =
                         the position would have been paying)
An observation missing any of them is excluded from the baseline analysis and counted; it is
never filled.

Model: ordinary least squares y ~ 1 + features, one model PER OUTCOME HORIZON, fitted on CONTROL
observations (both directions) labelled at that same horizon whose labels were AVAILABLE
(label_available: the latest availability of the bars the label read) no later than the start of
the UTC day of the observation being predicted, and no later than an optional cutoff (a
checkpoint's). A control frozen by a lab run (t_persisted; the hourly controls of modules B, C and
F, revision 2.10) is known only from that run on, like the checkpoint's reference rows, so a
selection made after a cutoff never trains that cutoff's baseline. Every prediction is therefore out-of-sample in time, never sees an outcome that was
not yet known, and never borrows a model trained on another horizon. The fit is cached per
(horizon, UTC day, cutoff). A prediction needs >= MIN_TRAIN training rows, otherwise the baseline
is "unidentifiable" for that observation and the comparison at that horizon is withheld. Added
value is measured on residuals (y - prediction): test residuals versus reference residuals (for a
control reference, the controls' own out-of-sample residuals).
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
    """Out-of-sample predictions for ONE horizon from controls whose same-horizon labels were known."""
    def __init__(self, controls, features=FEATURES, horizon=None):
        # controls: list of dicts with entry_t, exit_t, label_available, y and the feature keys, all
        # labelled at `horizon`
        self.horizon, self.features, self.cache = horizon, features, {}
        rows = []
        for c in controls:
            if all(c.get(k) is not None for k in features) and c.get("y") is not None:
                known = c.get("label_available")
                known = known if known is not None else c["exit_t"] + MINUTE
                rows.append(dict(c, _known=max(known, c.get("t_persisted") or 0)))   # frozen controls: once selected
        self.rows = sorted(rows, key=lambda c: c["_known"])

    def training(self, day, cutoff=None):
        bound = day if cutoff is None else min(day, cutoff)
        return [c for c in self.rows if c["_known"] <= bound], bound

    def predict(self, obs, cutoff=None):
        if any(obs.get(k) is None for k in self.features):
            return None, "missing baseline input"
        day = obs["entry_t"] // DAY * DAY
        key = (self.horizon, day, cutoff)
        if key not in self.cache:
            train, bound = self.training(day, cutoff)
            beta = None
            if len(train) >= MIN_TRAIN:
                beta = stats.ols([[1.0] + [c[k] for k in self.features] for c in train], [c["y"] for c in train])
            self.cache[key] = (beta, len(train))
        beta, n = self.cache[key]
        if beta is None:
            return None, (f"unidentifiable ({n} {self.horizon}-minute control labels known before this day; "
                          f"needs {MIN_TRAIN})")
        return beta[0] + sum(b * obs[k] for b, k in zip(beta[1:], self.features)), None

    def describe(self, cutoff=None):
        """What the model is; with a cutoff, only rows known by then are counted (a checkpoint's view)."""
        n = len(self.rows) if cutoff is None else sum(1 for c in self.rows if c["_known"] <= cutoff)
        return {"horizon_min": self.horizon, "target": f"ret_net of controls at {self.horizon} minutes",
                "predictors": list(self.features),
                ("training_rows_available" if cutoff is None else "training_rows_known_by_cutoff"): n,
                "method": "OLS; training rows known (label_available) before each UTC day"}


def build(labelled, horizons):
    """{horizon: Baseline} from the control observations of a labelled pass, same-horizon labels only."""
    out = {}
    for h in horizons:
        rows = []
        for e, labs, bf in labelled:
            if not e["group"].startswith("control") or not bf:
                continue
            v = labs.get(h) or labs.get(str(h))
            if v and v["status"] == "complete":
                rows.append(dict(bf, entry_t=v["entry_t"], exit_t=v["exit_t"], y=v["ret_net"],
                                 label_available=v.get("label_available"), t_persisted=e.get("t_persisted")))
        out[h] = Baseline(rows, horizon=h)
    return out
