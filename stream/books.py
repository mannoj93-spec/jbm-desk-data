"""Order-book reconstruction with explicit gap detection.

Each book reports `valid`. Anything that breaks continuity sets valid = False and records a gap;
the caller must resynchronise (Deribit: re-subscribe for a new snapshot; Bybit: re-subscribe, a
snapshot follows; Hyperliquid pushes whole snapshots, so only time gaps exist). While a book is
invalid nothing is sampled from it: a missing interval is recorded as missing, never as a quiet
book. Displayed liquidity only; nothing here infers hidden liquidity or intent from cancellations.
"""


class Book:
    def __init__(self, venue, instrument):
        self.venue, self.instrument = venue, instrument
        self.bids, self.asks = {}, {}
        self.valid = False
        self.last_ts = None
        self.gaps = []                         # (t_ms, reason)

    def invalidate(self, t, reason):
        if self.valid:
            self.gaps.append((t, reason))
        self.valid = False
        self.bids, self.asks = {}, {}

    def top(self, band_bp=10.0):
        """(bid, ask, mid, bid_depth, ask_depth) within band_bp of mid, or None if unusable."""
        if not self.valid or not self.bids or not self.asks:
            return None
        bid, ask = max(self.bids), min(self.asks)
        if bid >= ask:
            return None                        # crossed book: treat as unusable, never sample it
        mid = (bid + ask) / 2
        lo, hi = mid * (1 - band_bp / 1e4), mid * (1 + band_bp / 1e4)
        return (bid, ask, mid, sum(q for p, q in self.bids.items() if p >= lo),
                sum(q for p, q in self.asks.items() if p <= hi))


class DeribitBook(Book):
    """book.{instrument}.{interval}: first message is a full snapshot (type "snapshot"), then changes
    with change_id / prev_change_id. prev_change_id must equal the last change_id (Deribit docs)."""
    def __init__(self, instrument):
        super().__init__("deribit", instrument)
        self.change_id = None

    def apply(self, data):
        t = data.get("timestamp")
        kind = data.get("type")
        if kind == "snapshot" or (self.change_id is None and "prev_change_id" not in data):
            self.bids, self.asks = {}, {}
        elif not self.valid:
            return "ignored_until_snapshot"
        elif data.get("prev_change_id") != self.change_id:
            if data.get("change_id") is not None and self.change_id is not None and data["change_id"] <= self.change_id:
                return "duplicate_or_stale"
            self.invalidate(t, f"change_id gap: prev {data.get('prev_change_id')} != last {self.change_id}")
            self.change_id = None
            return "gap"
        for side, levels in (("bids", data.get("bids") or []), ("asks", data.get("asks") or [])):
            book = self.bids if side == "bids" else self.asks
            for action, price, amount in levels:
                if action == "delete" or amount == 0:
                    book.pop(price, None)
                else:
                    book[price] = amount
        self.change_id = data.get("change_id")
        self.valid, self.last_ts = True, t
        return "applied"


class BybitBook(Book):
    """orderbook.{depth}.{symbol}: snapshot then deltas; size "0" deletes; u == 1 means a service
    restart (reset from this message); a new snapshot resets the book. `u` must increase: a repeat
    or lower u is a duplicate/out-of-order message and is dropped; a jump by more than one is
    treated as a possible gap and the book is invalidated until the next snapshot."""
    def __init__(self, instrument):
        super().__init__("bybit", instrument)
        self.u = None

    def apply(self, msg):
        data, kind, t = msg.get("data") or {}, msg.get("type"), msg.get("ts")
        u = data.get("u")
        if kind == "snapshot" or u == 1:
            self.bids, self.asks = {}, {}
        elif not self.valid:
            return "ignored_until_snapshot"
        elif self.u is not None and u is not None and u <= self.u:
            return "duplicate_or_stale"
        elif self.u is not None and u is not None and u != self.u + 1:
            self.invalidate(t, f"update id jump {self.u} -> {u}")
            self.u = None
            return "gap"
        for side, levels in (("b", data.get("b") or []), ("a", data.get("a") or [])):
            book = self.bids if side == "b" else self.asks
            for price, size in levels:
                p, q = float(price), float(size)
                if q == 0:
                    book.pop(p, None)
                else:
                    book[p] = q
        self.u, self.valid, self.last_ts = u, True, t
        return "applied"


class HyperliquidBook(Book):
    """l2Book pushes whole snapshots (20 levels). The docs give a 0.5 s minimum spacing; measured on
    2026-09-23 from this environment the pushes arrived every ~5.0-5.5 s, so a 1-second sample of a
    Hyperliquid book can be up to ~5.5 s old (book1s rows carry book_age_ms). A push older than or
    equal to the last is dropped; a silence longer than max_gap_ms (default 15 s, about three
    measured push intervals) is recorded as a gap."""
    def __init__(self, instrument, max_gap_ms=15000):
        super().__init__("hyperliquid", instrument)
        self.max_gap_ms = max_gap_ms

    def apply(self, data):
        t = data.get("time")
        if self.last_ts is not None and t is not None and t <= self.last_ts:
            return "duplicate_or_stale"
        if self.last_ts is not None and t is not None and t - self.last_ts > self.max_gap_ms:
            self.gaps.append((t, f"silence {t - self.last_ts} ms"))
        levels = data.get("levels") or [[], []]
        self.bids = {float(x["px"]): float(x["sz"]) for x in levels[0]}
        self.asks = {float(x["px"]): float(x["sz"]) for x in levels[1]}
        self.valid, self.last_ts = True, t
        return "applied"
