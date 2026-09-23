"""Point-in-time (as-of) helpers shared by the modules.

Time fields on every lab record (lab-2.0), and what they mean:
  t_event           the market time the record describes (e.g. the close of a 5-minute window)
  t_first_observed  when the collector first wrote the earliest input the record uses (observed_at)
  t_inputs          dependency availability: the latest `avail` among EVERY input the computation read
                    (current window, prior volatility/return windows, rolling-threshold history,
                    snapshots, funding, cohort membership, ledger evidence). Missing times stay None.
  t_available       t_inputs + ASSUMED_PROCESSING_MS. An assumption about a live pipeline, never a
                    measurement: the lab runs every 6 hours, it does not execute live.
  t_persisted       the lab run (its data cutoff) that first computed and froze the decision. This is
                    the only measured decision time. t_persisted - t_available is the replay lag.
  label_available   (on outcome labels, lab-2.1) the latest `avail` of the bars a label read: when
                    the outcome was first knowable. A checkpoint counts an observation as known at
                    max(label_available, t_persisted).
Decisions are "as-of replays of collected inputs": the detector sees exactly the inputs whose
`avail` <= t_inputs. Required inputs that arrive late DELAY the decision; when the delay exceeds
LATE_INPUT_MAX_MS after t_event the decision is EXCLUDED (counted as late_inputs), because a signal
acted on hours late is a different signal. Optional inputs (funding, spread snapshots, spot flow)
are taken as the latest item already available when the required inputs were, so they can never
move a decision later or leak a later value into it.
"""
import bisect

ASSUMED_PROCESSING_MS = 60_000
LATE_INPUT_MAX_MS = 60 * 60_000
MINUTE = 60_000


class RangeMax:
    """Max of `avail` over index ranges of a minute grid, O(1) per query (sparse table).
    Missing entries are stored as 0 so they never raise the maximum; callers check required
    inputs for presence separately."""
    def __init__(self, values):
        self.n = len(values)
        self.table = [list(values)]
        k = 1
        while (1 << k) <= self.n:
            prev, half = self.table[-1], 1 << (k - 1)
            self.table.append([max(prev[i], prev[i + half]) for i in range(self.n - (1 << k) + 1)])
            k += 1

    def query(self, lo, hi):
        """max over [lo, hi); 0 for an empty range."""
        lo, hi = max(lo, 0), min(hi, self.n)
        if hi <= lo:
            return 0
        k = (hi - lo).bit_length() - 1
        row = self.table[k]
        return max(row[lo], row[hi - (1 << k)])


def grid(bars, start, end):
    """Minute grid [start, end): (times, bars-or-None, RangeMax over avail)."""
    ts = list(range(start, end, MINUTE))
    rows = [bars.get(t) for t in ts]
    return ts, rows, RangeMax([(r["avail"] if r else 0) for r in rows])


class Known:
    """A time series of (t, value, avail) for optional inputs. latest(t_max, known_by) returns the
    latest item with t <= t_max whose avail <= known_by (items with unknown avail are never used)."""
    def __init__(self, items, max_back=500):
        self.items = sorted(items, key=lambda x: x[0])
        self.ts = [x[0] for x in self.items]
        self.max_back = max_back

    def latest(self, t_max, known_by, min_t=None):
        i = bisect.bisect_right(self.ts, t_max)
        for j in range(i - 1, max(i - 1 - self.max_back, -1), -1):
            t, value, avail = self.items[j]
            if min_t is not None and t < min_t:
                return None
            if avail is not None and avail <= known_by:
                return self.items[j]
        return None


def latest_known(items, t_max, known_by):
    return Known(items).latest(t_max, known_by)


def decide(t_event, t_inputs):
    """(t_available, excluded_reason) for a decision whose required inputs were available at t_inputs."""
    if t_inputs is None:
        return None, "input availability unknown"
    t_inputs = max(t_inputs, t_event)
    if t_inputs - t_event > LATE_INPUT_MAX_MS:
        return None, "late_inputs"
    return t_inputs + ASSUMED_PROCESSING_MS, None
