"""Deterministic scoring, strict observation coverage, and evidence retention."""
import datetime as dt
import hashlib
import math
from pathlib import Path
import time
import urllib.request
from schema import H, MINUTE, SERIES, ms, num, observed_time, predicate_step, validate
from storage import atomic_json, digest, loads, read_json, read_rows

VERSION = "scoring-2.1"


class Unscorable(ValueError):
    """Missing/invalid observations; retry later, never turn missing data into false."""


def check_bars(bars, start, end, step=MINUTE):
    if start % step or end % step or start >= end:
        raise Unscorable("price window must use complete aligned intervals")
    expected = (end - start) // step
    if len(bars) != expected:
        raise Unscorable(f"incomplete price coverage: {len(bars)}/{expected} bars")
    for i, bar in enumerate(bars):
        if len(bar) != 4 or bar[0] != start + i * step:
            raise Unscorable("duplicate, missing, or out-of-order price timestamp")
        if not all(num(x) and x > 0 for x in bar[1:]) or not bar[2] <= bar[3] <= bar[1]:
            raise Unscorable("invalid OHLC values")
    return bars


def fetch_bars(start, end, step=MINUTE, opener=None, pause=time.sleep):
    opener = opener or urllib.request.urlopen
    interval = {MINUTE: "1m", H: "1h"}[step]
    out, cursor = [], start
    max_pages = (end - start) // (step * 1500) + 2
    for _ in range(max_pages):
        if cursor >= end:
            break
        url = (f"https://www.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval={interval}"
               f"&startTime={cursor}&endTime={end - 1}&limit=1500")
        js = None
        for attempt in range(3):
            try:
                with opener(urllib.request.Request(url, headers={"User-Agent": "jbm-report/2"}), timeout=25) as response:
                    js = loads(response.read())
                break
            except Exception as exc:
                if attempt == 2:
                    raise Unscorable(f"price fetch failed: {exc}") from exc
                pause(1 + attempt)
        if not isinstance(js, list) or not js:
            raise Unscorable("price source returned empty data or an error object")
        try:
            page = [(int(k[0]), float(k[2]), float(k[3]), float(k[4])) for k in js]
        except (TypeError, ValueError, IndexError) as exc:
            raise Unscorable("malformed price response") from exc
        if page[0][0] != cursor or page[-1][0] >= end:
            raise Unscorable("price response does not cover requested boundaries")
        out.extend(page)
        cursor = page[-1][0] + step
        pause(.15)
    return check_bars(out, start, end, step)


def hit(bar, level, direction):
    return bar[1] >= level if direction == "up" else bar[2] <= level


def closes_every(bars, every):
    return [(b[0] + MINUTE, b[3]) for b in bars if (b[0] + MINUTE) % every == 0]


def predicate(ev, bars, start, reader):
    series = ev.get("series")
    out = {"name": ev.get("name"), "type": "predicate", "series": series}
    if not series:
        return dict(out, outcome="manual"), []
    step = predicate_step(series)
    deadline = ms(ev.get("at_utc", ev.get("by_utc")))
    expected = [deadline] if "at_utc" in ev else list(range((start // step + 1) * step, deadline + 1, step))
    if not expected:
        raise Unscorable("no completed predicate intervals")
    if series in ("close_1h", "close_4h"):
        values = closes_every(bars, step)
    elif series in ("high", "low"):
        values = [(b[0] + MINUTE, b[1] if series == "high" else b[2]) for b in bars]
    else:
        _, name, field = series.split(":")
        # A snapshot row describes its stamp; an interval row describes its close (schema.SERIES_KIND).
        values = [(observed_time(name, r["t"]), r.get("f", {}).get(field)) for r in reader(name)]
    relevant = {}
    wanted = set(expected)
    for timestamp, value in values:
        if timestamp not in wanted:
            continue
        if not num(value):
            raise Unscorable(f"non-finite/missing predicate value: {series}")
        if timestamp in relevant and relevant[timestamp] != value:
            raise Unscorable(f"conflicting predicate observations: {series}")
        relevant[timestamp] = value
    if set(relevant) != wanted:
        raise Unscorable(f"incomplete predicate coverage: {series} {len(relevant)}/{len(expected)}")
    op, target = ev["op"], ev["value"]
    def matches(value):
        return {"<": value < target, ">": value > target, "<=": value <= target, ">=": value >= target}[op]
    evidence = [[t, relevant[t]] for t in expected]
    first = next((t for t in expected if matches(relevant[t])), None)
    out.update(outcome=int(first is not None), first=first)
    if "at_utc" in ev:
        out["value"] = relevant[deadline]
    return out, evidence


def score(fc, bars, reader):
    errors = validate(fc)
    if errors:
        raise ValueError("invalid forecast: " + "; ".join(errors))
    start, end = ms(fc["start_utc"]), ms(fc["horizon_utc"])
    # Even non-price forecasts retain complete price evidence; conservative uniform contract.
    check_bars(bars, start, end)
    results, predicate_evidence = [], []
    for ev in fc["events"]:
        kind = ev["type"]
        common = {"name": ev.get("name"), "type": kind}
        if kind == "predicate":
            result, evidence = predicate(ev, bars, start, reader)
            results.append(result)
            predicate_evidence.append({"event_index": len(results) - 1, "observations": evidence})
            continue
        if kind == "interval":
            y, lo, hi, alpha = bars[-1][3], ev["lo"], ev["hi"], 1 - ev["coverage"]
            # Winkler / Gneiting-Raftery interval score (lower is better), in price points.
            width_penalty = (hi - lo) + (2 / alpha) * max(0.0, lo - y) + (2 / alpha) * max(0.0, y - hi)
            results.append(dict(common, inside=lo <= y <= hi, nominal=ev["coverage"], realized=y,
                                interval_score=round(width_penalty, 8)))
            continue
        if kind == "range":
            realized = math.log(max(b[1] for b in bars) / min(b[2] for b in bars))
            q = {0.1: ev["q10"], 0.5: ev["q50"], 0.9: ev["q90"]}
            pinball = {f"q{int(k * 100)}": round(max(k * (realized - v), (k - 1) * (realized - v)), 10) for k, v in q.items()}
            result = dict(common, realized_ln_range=round(realized, 10), covered_80=ev["q10"] <= realized <= ev["q90"],
                          pinball=pinball)
            # runbook E2 primary loss: absolute error of ln(range), point forecast = median.
            result["abs_log_error"] = round(abs(math.log(ev["q50"]) - math.log(realized)), 10) if realized > 0 else None
            results.append(result)
            continue
        if kind == "lean":
            delta = bars[-1][3] - fc["reference_price"]
            result = dict(common, direction=ev["direction"], basis=ev.get("basis"),
                          outcome="flat" if delta == 0 else int((delta > 0) == (ev["direction"] == "up")),
                          return_pts=round(delta, 8))
            inv = ev.get("invalidation")
            if inv:
                every = H if inv["basis"] == "close_1h" else 4 * H
                result["invalidated_at"] = next((t for t, value in closes_every(bars, every)
                    if (value > inv["level"] if inv["dir"] == "above" else value < inv["level"])), None)
            results.append(result)
            continue
        if kind == "touch":
            outcome = int(any(hit(b, ev["level"], ev["dir"]) for b in bars))
        elif kind == "terminal":
            outcome = int(bars[-1][3] > ev["level"] if ev["dir"] == "above" else bars[-1][3] < ev["level"])
        else:
            a = next((i for i, b in enumerate(bars) if hit(b, ev["a"]["level"], ev["a"]["dir"])), None)
            b = next((i for i, bar in enumerate(bars) if hit(bar, ev["b"]["level"], ev["b"]["dir"])), None)
            outcome = "bound" if a is not None and a == b else int(a is not None and (b is None or a < b))
        p = ev["p"]
        clipped = min(max(p, 1e-4), 1 - 1e-4)
        result = dict(common, p=p, p_class=ev["p_class"], outcome=outcome, log_probability_clip=1e-4)
        if outcome == "bound":
            result.update(log_score=sorted([math.log(clipped), math.log(1 - clipped)]),
                          brier=sorted([p ** 2, (1 - p) ** 2]))
        else:
            result.update(log_score=math.log(clipped if outcome else 1 - clipped), brier=(p - outcome) ** 2)
        results.append(result)
    return results, {"price_bars": bars, "predicate_observations": predicate_evidence,
                     "price_source": "Binance BTCUSDT perpetual 1m klines", "timestamp_basis": "UTC milliseconds"}


def score_registry(base, now, report_version, fetch=fetch_bars):
    from registration import forecasts
    from storage import append_unique
    base = Path(base)
    records = read_rows(base / "registry/scores.jsonl")
    done = {(r["id"], r.get("forecast_sha256")) for r in records}
    legacy_ids = {r["id"] for r in records if not r.get("forecast_sha256")}
    new, alerts, pending = [], [], 0
    for index, rec in enumerate(records):
        if rec.get("status") != "scored":
            continue
        try:
            if not rec.get("evidence") or not rec.get("evidence_sha256"):
                raise ValueError("legacy score has no retained evidence")
            path = base / rec["evidence"]
            if path.resolve().parent != (base / "registry/evidence").resolve():
                raise ValueError("invalid evidence path")
            evidence = read_json(path)
            if digest(evidence) != rec["evidence_sha256"] or evidence.get("forecast_sha256") != rec.get("forecast_sha256"):
                raise ValueError("evidence hash or forecast reference mismatch")
        except (ValueError, TypeError, AttributeError, OSError) as exc:
            alerts.append(f"{rec['id']}: score evidence integrity error: {exc}; original record retained for review")
            records[index] = dict(rec, status="evidence integrity error")
    implementation_hash = digest({p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in sorted(Path(__file__).resolve().parent.glob("*.py"))})
    def reader(name):
        return [r for p in sorted((base / "data/series" / name).glob("*.jsonl")) for r in read_rows(p)]
    for fc, entry in forecasts(base):
        key = (fc["id"], entry["sha256"])
        if key in done:
            continue
        if fc["id"] in legacy_ids:
            alerts.append(f"{fc['id']}: legacy score needs manual migration; not overwritten or rescored")
            continue
        start, end, rat = ms(fc["start_utc"]), ms(fc["horizon_utc"]), entry["registered"]
        if rat >= start:
            status = "late registration — not scored"
            rec = {"id": fc["id"], "forecast_sha256": entry["sha256"], "registered": rat,
                   "start": start, "horizon": end, "status": status, "scored": now}
        elif end > now - 5 * MINUTE:
            pending += 1
            continue
        else:
            try:
                bars = fetch(start, end)
                events, evidence = score(fc, bars, reader)
                evidence.update(forecast_sha256=entry["sha256"], scoring_version=VERSION,
                                implementation_sha256=implementation_hash, retrieved_at=now)
                eh = digest(evidence)
                evidence_path = f"registry/evidence/{eh}.json"
                atomic_json(base / evidence_path, evidence)
                rec = {"id": fc["id"], "forecast_sha256": entry["sha256"], "registered": rat,
                       "start": start, "horizon": end, "scored": now, "status": "scored",
                       "code_version": fc.get("code_version"), "snapshot_hash": fc.get("snapshot_hash"),
                       "event_regime": fc.get("event_regime"), "report_version": report_version,
                       "scoring_version": VERSION, "implementation_sha256": implementation_hash,
                       "events": events, "evidence_sha256": eh, "evidence": evidence_path}
            except Exception as exc:
                alerts.append(f"{fc['id']}: unscorable; retry next report: {type(exc).__name__}: {exc}")
                pending += 1
                continue
        append_unique(base / "registry/scores.jsonl", [rec], lambda r: (r["id"], r.get("forecast_sha256")))
        records.append(rec)
        new.append(rec)
    return records, new, pending, alerts
