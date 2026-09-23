"""Point-in-time access to the collector's stored datasets for the lab.

Everything returned carries `avail`: the earliest instant the value could have been used live,
i.e. max(time the collector wrote it, time the value was knowable at the source). A cutoff hides
anything not yet available. Nothing is back-dated to its event time.
"""
from pathlib import Path
import json
import os
import time
import urllib.request

from lab.common import DAY, MINUTE, PROCESSING_LATENCY_MS, digest, read_json, read_rows
from schema import PRICE_SERIES, known_time


class Store:
    def __init__(self, base, cutoff=None):
        self.base = Path(base)
        self.cutoff = cutoff if cutoff is not None else int(time.time() * 1000)
        self._cache = {}

    def _rows(self, pattern):
        if pattern not in self._cache:
            rows = []
            for p in sorted(self.base.glob(pattern)):
                rows.extend(read_rows(p))
            self._cache[pattern] = rows
        return self._cache[pattern]

    def _stamped(self, pattern):
        return sorted((r for r in self._rows(pattern) if r.get("observed_at") is not None
                       and r["observed_at"] <= self.cutoff), key=lambda r: r["t"])

    # ---- prices -------------------------------------------------------------------------------
    def bars(self, name):
        """{open_time: bar} for a PRICE_SERIES name; bar['avail'] = max(close, observed_at)."""
        if name not in PRICE_SERIES:
            raise ValueError(name)
        out = {}
        for batch in self._rows(f"data/prices/{name}/*.jsonl"):
            seen = batch.get("observed_at")
            if seen is None:
                continue
            for bar in batch["bars"]:
                row = dict(zip(batch["fields"], bar))
                row["avail"] = max(seen, bar[0] + MINUTE)
                if row["avail"] <= self.cutoff and bar[0] not in out:
                    out[bar[0]] = row
        return out

    def batches(self, name):
        """(first_bar, last_bar, observed_at, sha) per stored batch: the input-arrival record."""
        return [(b["t"], b["t_last"], b["observed_at"], digest(b["bars"]))
                for b in self._rows(f"data/prices/{name}/*.jsonl") if b.get("observed_at") is not None]

    # ---- other datasets ----------------------------------------------------------------------
    def snaps(self):
        return self._stamped("data/snap/*.jsonl")

    def series(self, name):
        out = {}
        for r in self._rows(f"data/series/{name}/*.jsonl"):
            seen = r.get("observed_at")
            if seen is None:
                continue
            avail = max(seen, known_time(name, r["t"])) if name != "binance_funding_settled" else max(seen, r["t"])
            if avail <= self.cutoff:
                out.setdefault((r["t"], r.get("sym")), dict(r, avail=avail))
        return [out[k] for k in sorted(out, key=lambda k: (k[0], str(k[1])))]

    def funding_events(self, sym="BTCUSDT"):
        """Settled funding (8h rate, positive = longs pay) for cost attribution; not a signal input."""
        return [(r["t"], r["f"]["funding_settled_8h"]) for r in self.series("binance_funding_settled")
                if r.get("sym") == sym and r["f"].get("funding_settled_8h") is not None]

    def options(self):
        return self._stamped("data/options/deribit_btc/*.jsonl")

    def option_quotes(self):
        return self._stamped("data/options/deribit_btc_quotes/*.jsonl")

    def hl_accounts(self):
        cohort = read_json(self.base / "state/hl_cohort_fixed_v2.json", None)
        fixed = [m[0] for m in cohort["members"]] if cohort and cohort.get("selected_by_run", 0) <= self.cutoff else []
        out = []
        for rec in self._stamped("data/hl_accounts/*.jsonl"):
            ids = {f"F{i}": a for i, a in enumerate(fixed)}
            ids.update({f"R{j}": a for j, a in enumerate(rec.get("rotating", {}).get("members", []))})
            out.append(dict(rec, address_of=ids))
        return out

    def hl_enrich(self):
        return self._stamped("data/hl_enrich/*.jsonl")

    def okx_insurance(self):
        return self._stamped("data/okx_insurance/*.jsonl")

    def liq_orders(self):
        rows = {}
        for r in self._rows("data/liq/orders/*.jsonl"):
            seen = r.get("observed_at")
            if seen is None:
                continue
            avail = max(seen, r["t"])
            if avail <= self.cutoff:
                rows.setdefault((r["t"], r.get("posSide"), r.get("side"), r.get("sz_contracts"), r.get("bkPx")),
                                dict(r, avail=avail))
        return sorted(rows.values(), key=lambda r: r["t"])

    def runs(self):
        return self._stamped("data/runs/*.jsonl")


# ---- historical reconstruction ------------------------------------------------------------------
HISTORY_URL = {
    "binance_klines_1m_BTCUSDT_perp": "https://www.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1m",
    "binance_klines_1m_BTCUSDT_spot": "https://www.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m",
    "binance_klines_1m_ETHUSDT_perp": "https://www.binance.com/fapi/v1/klines?symbol=ETHUSDT&interval=1m",
    "binance_klines_1m_SOLUSDT_perp": "https://www.binance.com/fapi/v1/klines?symbol=SOLUSDT&interval=1m",
}
FIELDS = ["t", "o", "h", "l", "c", "v", "qv", "n", "tbv", "tbqv"]


def fetch_history(name, start, end, opener=None, pause=0.15):
    """Closed 1-minute bars [start, end) from Binance's public history, for exploratory
    reconstruction only. Returns ({t: bar}, sha256 of the canonical bar list). Each bar's `avail`
    is ASSUMED (close + processing latency) and labelled as such by callers."""
    opener = opener or (lambda url: urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "jbm-lab/1"}), timeout=30))
    cache_dir = Path(os.environ.get("LAB_CACHE", Path(__file__).resolve().parent.parent / ".lab-cache"))
    cache = cache_dir / f"{name}-{start}-{end}.json"
    if cache.exists():
        bars = json.loads(cache.read_text())
    else:
        bars, cursor = [], start
        limit = 1000 if name.endswith("_spot") else 1500
        while cursor < end:
            url = f"{HISTORY_URL[name]}&startTime={cursor}&endTime={end - 1}&limit={limit}"
            with opener(url) as resp:
                page = json.loads(resp.read())
            if not page:
                break
            for k in page:
                t = int(k[0])
                if t + MINUTE <= end:
                    bars.append([t, float(k[1]), float(k[2]), float(k[3]), float(k[4]), float(k[5]), float(k[7]),
                                 int(k[8]), float(k[9]), float(k[10])])
            cursor = int(page[-1][0]) + MINUTE
            time.sleep(pause)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(bars))
    out = {}
    for b in bars:
        row = dict(zip(FIELDS, b))
        row["avail"] = b[0] + MINUTE + PROCESSING_LATENCY_MS
        out[b[0]] = row
    return out, digest(bars)


def history_window(days, now=None):
    now = now or int(time.time() * 1000)
    end = now // DAY * DAY
    return end - days * DAY, end
