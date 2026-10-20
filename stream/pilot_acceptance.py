"""E1 pilot acceptance (pilot-acceptance-1.1.0, repo 2.30; 1.0.0 was repo 2.29): evaluate a recorder data directory
against the criteria declared in stream/pilot_e1.json BEFORE the pilot ran.

1.1.0 (Oct 19 2026 review, F7). 1.0.0 passed a directory with partial records on two days, complete derived seconds
on a third, no record at all for the day between, a manifest entry pointing at a missing raw object and a
caller-supplied eligible_shocks=25, with zero verified partitions. It derived its days from the files it found,
skipped missing files with an exists() check and trusted the shock count. Now:

  window      expected coverage comes from the explicit pilot start/end and the scoped books, never from the files
              present: every expected second of every day (partial boundary days pro rata) is accounted for, so an
              absent day or hour is a shortfall, not an omission.
  objects     every manifest entry is re-read (locally, or through the backend's restore when the local copy is
              gone) and must match its bytes and sha256; an expected raw partition missing from the manifest or
              unrecoverable is unverifiable and its seconds are ineligible; local closed partitions absent from
              the manifest are reported.
  derived     a 1-second sample is eligible only if it sits under its own venue/instrument path, its book is fresh
              (book_age_ms), its hour's raw partition is verified and replays (stream/books.py) to the same mid
              (fabricated or mis-attributed samples fail), no gap covers it and the hour has clock-offset evidence
              within clock_offset_ms_max (derived/clock, written by the recorder from Deribit public/get_time).
  shocks      counted from the retained evidence: mid-move triggers on scoped books with a verified capture and
              complete history and recovery windows (shock_window_min each side). A number passed on the command
              line is recorded as a claim and ignored.
  stopping    the registered rule: the evidence target ends the window early when reached; otherwise the declared
              duration. Stop conditions (bytes over budget two days running, a day below the floor share, three
              consecutive unverifiable partitions) are checked.
  verdict     pass only when every rule is met on every scoped book and the evidence target is reached; fail on any
              violated rule or stop condition; inconclusive when rules are met but the target is not; invalid when the
              window is not declared. Unverifiable evidence never passes.

    python -m stream.pilot_acceptance STREAM_DATA_DIR --start 2026-11-01T00:00:00Z --end 2026-11-15T00:00:00Z
Nothing here runs the recorder; E1 stays uncommissioned.
"""
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stream import books as B  # noqa: E402

VERSION = "pilot-acceptance-1.1.0"
BOOK_CHANNELS = {"deribit": "book.{inst}.100ms", "bybit": "orderbook.50.{inst}"}
HOUR_MS = 3_600_000
DAY_MS = 86_400_000


def _ms(x):
    return int(dt.datetime.fromisoformat(str(x).replace("Z", "+00:00")).timestamp() * 1000)


def _iso(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _day_hour(ms):
    d = dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc)
    return d.strftime("%Y-%m-%d"), d.strftime("%H")


def _decode(key, data):
    text = gzip.decompress(data).decode() if key.endswith(".gz") else data.decode()
    return [json.loads(x) for x in text.splitlines() if x.strip()]


class Objects:
    """Manifest-verified reads: local file, else the backend's copy (restore); bytes and sha256 must match."""

    def __init__(self, root, backend=None):
        self.root, self.backend = Path(root), backend
        self.manifest, self.problems = {}, []
        for p in sorted((self.root / "manifest").glob("*.jsonl")):
            for m in _decode(p.name, p.read_bytes()):
                if m.get("key") in self.manifest and self.manifest[m["key"]] != m:
                    self.problems.append(f"manifest lists {m['key']} twice with different content")
                self.manifest[m.get("key")] = m
        self.cache = {}

    def get(self, key):
        """(bytes, state): state ok | unlisted | missing | wrong-size | wrong-hash."""
        if key in self.cache:
            return self.cache[key]
        m = self.manifest.get(key)
        if m is None:
            out = (None, "unlisted")
        else:
            p = self.root / key
            data = p.read_bytes() if p.exists() else None
            if data is None and self.backend is not None:
                try:
                    data = self.backend.get(key)
                except Exception:                                      # noqa: BLE001 - unrecoverable is a state
                    data = None
            if data is None:
                out = (None, "missing")
            elif len(data) != int(m.get("bytes") or -1):
                out = (None, "wrong-size")
            elif hashlib.sha256(data).hexdigest() != m.get("sha256"):
                out = (None, "wrong-hash")
            else:
                out = (data, "ok")
        self.cache[key] = out
        return out


def _new_book(venue, inst):
    return B.DeribitBook(inst) if venue == "deribit" else B.BybitBook(inst)


def _replay(book, venue, inst, raw_rows):
    """Apply one hour's raw book messages, in receive order, to a book carried across hours. Returns
    [(r_ms, mid_before, mid_after)] and the number of messages naming another instrument (wrong book identity)."""
    out, bad = [], 0
    for rec in sorted(raw_rows, key=lambda x: x.get("r", 0)):
        js = json.loads(rec["m"])
        data = ((js.get("params") or {}).get("data") or {}) if venue == "deribit" else js
        name = data.get("instrument_name") if venue == "deribit" else (js.get("data") or {}).get("s")
        if name != inst:
            bad += 1
            continue
        before = book.top()
        book.apply(data)
        after = book.top()
        out.append((rec["r"], before[2] if before else None, after[2] if after else None))
    return out, bad


def evaluate(root, criteria, start_utc=None, end_utc=None, backend=None, eligible_shocks=None):
    root = Path(root)
    out = {"version": VERSION, "criteria": criteria.get("id"), "findings": [], "unverifiable": [], "books": {}}
    if start_utc is None or end_utc is None:
        out.update(verdict="invalid", findings=["no declared pilot window (start and end): coverage cannot be expected"])
        return out
    start, end = _ms(start_utc), _ms(end_utc)
    max_days = criteria.get("duration_days", 14)
    if not start < end or end - start > max_days * DAY_MS:
        out.update(verdict="invalid", findings=[f"window must be 0 < end - start <= {max_days} days"])
        return out
    if eligible_shocks is not None:
        out["claimed_shocks_ignored"] = eligible_shocks
    c = criteria["completeness"]
    W = criteria.get("shock_window_min", 30) * 60_000
    target = criteria.get("evidence_target_shocks", 20)
    objs = Objects(root, backend)
    out["unverifiable"] += objs.problems
    hours = list(range(start // HOUR_MS * HOUR_MS, end, HOUR_MS))

    # gaps, clock evidence and triggers are the recorder's logs (derived/gaps, derived/clock, derived/triggers)
    gaps = []
    for p in sorted((root / "derived" / "gaps").glob("*.jsonl")):
        gaps += _decode(p.name, p.read_bytes())
    clock = {}
    for p in sorted((root / "derived" / "clock").glob("*.jsonl")):
        for s in _decode(p.name, p.read_bytes()):
            h = s["t"] // HOUR_MS * HOUR_MS
            clock.setdefault(h, []).append(abs(float(s["offset_ms"])))
    clock_ok = {}
    for h in hours:
        xs = clock.get(h)
        if not xs:
            clock_ok[h] = "clock-unverified (no offset sample in the hour)"
        elif max(xs) > c["clock_offset_ms_max"]:
            clock_ok[h] = f"clock offset {max(xs):.0f} ms > {c['clock_offset_ms_max']} ms"
        else:
            clock_ok[h] = "ok"
    bad_clock = sorted({v for v in clock_ok.values() if v != "ok"})
    out["clock_hours_unusable"] = sum(1 for v in clock_ok.values() if v != "ok")
    eligible = {}
    consecutive_bad, worst_run = 0, 0
    for venue, inst in criteria["scope"]["venues_instruments"]:
        key = f"{venue}/{inst}"
        secs = set()
        ch = BOOK_CHANNELS.get(venue, "{inst}").format(inst=inst)
        book_gaps = [(g.get("start") or g.get("end"), g.get("end") or g.get("start")) for g in gaps
                     if g.get("venue") == "service" or (g.get("venue") == venue and g.get("instrument") in (None, inst))]
        prefix = f"raw/{venue}/{ch}/"
        listed = sorted(_ms(f"{k.split('/')[-2]}T{k.split('/')[-1][:2]}:00:00Z") for k in objs.manifest
                        if str(k).startswith(prefix))
        first = min([h for h in listed if h < start] + [hours[0]])
        book = _new_book(venue, inst)
        for h in range(first, end, HOUR_MS):                              # replay from the recording's start
            day, hh = _day_hour(h)
            rk = f"raw/{venue}/{ch}/{day}/{hh}.jsonl.gz"
            dk = f"derived/book1s/{venue}/{inst}/{day}/{hh}.jsonl.gz"
            raw, rst = objs.get(rk)
            if h < start:
                if rst == "ok":
                    _replay(book, venue, inst, _decode(rk, raw))
                else:
                    book = _new_book(venue, inst)                          # state lost until a new snapshot
                continue
            der, dst = objs.get(dk)
            if rst != "ok":
                book = _new_book(venue, inst)
            if rst == "ok" and dst != "ok":
                _replay(book, venue, inst, _decode(rk, raw))                # keep the book current
            if rst != "ok" or dst != "ok":
                consecutive_bad += 1
                worst_run = max(worst_run, consecutive_bad)
                if rst != "ok":
                    out["unverifiable"].append(f"{rk}: {rst}")
                if dst != "ok":
                    out["unverifiable"].append(f"{dk}: {dst}")
                continue
            consecutive_bad = 0
            if clock_ok[h] != "ok":
                _replay(book, venue, inst, _decode(rk, raw))                # keep the book current
                continue
            carried = book.top()
            steps, wrong_id = _replay(book, venue, inst, _decode(rk, raw))
            steps = [(h - 1, carried[2] if carried else None, carried[2] if carried else None)] + steps
            if wrong_id:
                out["findings"].append(f"{rk}: {wrong_id} message(s) for another instrument (wrong book identity)")
                continue
            rs = [s[0] for s in steps]
            mismatched = 0
            import bisect
            for row in _decode(dk, der):
                t = int(row["t"])
                if not (h <= t < h + HOUR_MS) or not (start <= t < end):
                    continue
                age = row.get("book_age_ms")
                if age is None or age > c["max_book_age_ms"]:
                    continue
                i = bisect.bisect_right(rs, t)
                if i == 0:
                    mismatched += 1
                    continue
                _, before, after = steps[i - 1]
                if row.get("mid") not in (after, before):
                    mismatched += 1
                    continue
                if any(g0 is not None and g1 is not None and g0 <= t <= g1 for g0, g1 in book_gaps):
                    continue
                secs.add(int(round(t / 1000)))
            if mismatched:
                out["findings"].append(f"{dk}: {mismatched} sample(s) not reproducible from the raw messages "
                                       "(fabricated or mis-attributed derived data); the hour is not eligible")
                secs -= set(range(h // 1000, (h + HOUR_MS) // 1000))
        eligible[key] = secs
    if bad_clock:
        out["unverifiable"].append("hours without usable clock evidence: " + "; ".join(bad_clock))

    # shocks from the retained evidence; the registered stopping rule
    def share(key, a, b):
        n = max(1, (b - a) // 1000)
        return sum(1 for s in eligible[key] if a // 1000 <= s < b // 1000) / n

    shocks = []
    for p in sorted((root / "derived" / "triggers").glob("*.jsonl")):
        for tr in _decode(p.name, p.read_bytes()):
            if tr.get("kind") != "trigger":
                continue
            bk = str((tr.get("detail") or {}).get("key", "")).replace(":", "/", 1)
            t = int(tr["t"])
            if bk not in eligible or not (start + W <= t <= end - W):
                continue
            ck = f"captures/{tr['capture_id'][:10]}/{tr['capture_id']}.jsonl.gz"
            _, cst = objs.get(ck)
            hist, rec = share(bk, t - W, t), share(bk, t, t + W)
            ok = cst == "ok" and hist >= c["eligible_second_share_min"] and rec >= c["eligible_second_share_min"]
            shocks.append({"t_utc": _iso(t), "book": bk, "capture": cst, "history_share": round(hist, 4),
                           "recovery_share": round(rec, 4), "eligible": ok})
    good = sorted((s for s in shocks if s["eligible"]), key=lambda s: s["t_utc"])
    eval_end = end
    if len(good) >= target:
        eval_end = min(end, _ms(good[target - 1]["t_utc"]) + W)
        out["stopped_early_utc"] = _iso(eval_end)
    out["shocks"] = {"candidates": len(shocks), "eligible": len(good), "target": target, "rejected":
                     [s for s in shocks if not s["eligible"]][:20]}

    # completeness per book and day over [start, eval_end)
    day0 = start // DAY_MS * DAY_MS
    by_day_bytes = {}
    for k, m in objs.manifest.items():
        d = str(k).split("/")[-2] if str(k).count("/") >= 2 else None
        if d and d[:4].isdigit():
            by_day_bytes[d] = by_day_bytes.get(d, 0) + int(m.get("bytes") or 0)
    stop = []
    for key, secs in eligible.items():
        days = {}
        d = day0
        while d < eval_end:
            a, b = max(d, start), min(d + DAY_MS, eval_end)
            if b > a:
                sh = share(key, a, b)
                days[_day_hour(d)[0]] = {"expected_seconds": (b - a) // 1000, "eligible_share": round(sh, 5)}
                if sh < c["eligible_second_share_min"]:
                    out["findings"].append(f"{key} {_day_hour(d)[0]}: eligible share {sh:.4f} < {c['eligible_second_share_min']}")
                if sh < criteria.get("stop_share_floor", 0.80) and (b - a) >= DAY_MS:
                    stop.append(f"{key} {_day_hour(d)[0]}: eligible share below the stop floor")
            d += DAY_MS
        out["books"][key] = days
    for d in sorted({_day_hour(h)[0] for h in hours}):
        seq = sum(1 for g in gaps if _day_hour(int(g.get("end") or g.get("start") or 0))[0] == d
                  and g.get("venue") != "service" and "restart" not in str(g.get("reason")))
        rst = sum(1 for g in gaps if _day_hour(int(g.get("end") or g.get("start") or 0))[0] == d
                  and (g.get("venue") == "service" or "restart" in str(g.get("reason"))))
        if seq > c["sequence_gaps_per_day_max"]:
            out["findings"].append(f"{d}: sequence/other gaps {seq} > {c['sequence_gaps_per_day_max']}")
        if rst > c["restart_gaps_per_day_max"]:
            out["findings"].append(f"{d}: restarts {rst} > {c['restart_gaps_per_day_max']}")
    over = [d for d in sorted(by_day_bytes) if by_day_bytes[d] > criteria["resources"]["raw_bytes_per_day_max"]]
    if any(_ms(f"{a}T00:00:00Z") + DAY_MS == _ms(f"{b}T00:00:00Z") for a, b in zip(over, over[1:])):
        stop.append("raw bytes over budget on two consecutive days")
    if worst_run >= 3:
        stop.append(f"{worst_run} consecutive partitions unverifiable")
    out.update(bytes_per_day=by_day_bytes, stop_conditions=stop, evaluated_window=[start_utc, _iso(eval_end)],
               partitions_verified=sum(1 for v in objs.cache.values() if v[1] == "ok"))
    if stop or out["findings"]:
        verdict = "fail"
    elif out["unverifiable"]:
        verdict = "fail"                                                # unverifiable evidence never passes
    elif len(good) < target:
        verdict = "inconclusive"
    else:
        verdict = "pass"
    out["verdict"] = verdict
    return out


def _main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(prog="stream.pilot_acceptance")
    ap.add_argument("root")
    ap.add_argument("--criteria", default=str(Path(__file__).with_name("pilot_e1.json")))
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--shocks", type=int, help="ignored: a claimed count is not evidence (recorded as a claim)")
    a = ap.parse_args(argv)
    r = evaluate(a.root, json.loads(Path(a.criteria).read_text()), a.start, a.end, eligible_shocks=a.shocks)
    print(json.dumps(r, indent=1, default=str))
    return {"pass": 0, "inconclusive": 3, "fail": 1}.get(r["verdict"], 2)


if __name__ == "__main__":
    sys.exit(_main())
