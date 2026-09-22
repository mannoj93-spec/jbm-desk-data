"""Research context: explicit point-in-time views and conservative episode classification.

Custom Python tests are trusted repository code, not sandboxed or formally audited.
Post-registration does not mean proven free of look-ahead or statistically independent.
"""
import importlib.util
from pathlib import Path
from schema import H, SERIES, num
from scoring import fetch_bars
from storage import append_unique, digest, read_json, read_rows
from registration import test_hash


class Ctx:
    def __init__(self, base, registered, now, cutoff=None):
        self.base = Path(base)
        self.registered = registered
        self.now = now
        self.cutoff = now if cutoff is None else min(cutoff, now)

    def as_of(self, decision_ms):
        if not isinstance(decision_ms, int) or decision_ms > self.cutoff:
            raise ValueError("as_of must not exceed the current view cutoff")
        return Ctx(self.base, self.registered, self.now, decision_ms)

    def _rows(self, pattern):
        return [r for p in sorted(self.base.glob(pattern)) for r in read_rows(p)]

    def series(self, name):
        if name not in SERIES:
            raise ValueError("point-in-time views support fixed-cadence registered series only")
        step = SERIES[name][0]
        unique = {}
        for row in self._rows(f"data/series/{name}/*.jsonl"):
            # Legacy rows have no verified completion/availability stamp. Fail closed.
            seen = row.get("observed_at")
            if seen is not None and max(seen, row["t"] + step) <= self.cutoff:
                unique.setdefault(row["t"], row)
        return [unique[t] for t in sorted(unique)]

    def snaps(self):
        return sorted((r for r in self._rows("data/snap/*.jsonl")
                       if r.get("observed_at") is not None and r["observed_at"] <= self.cutoff), key=lambda r: r["t"])

    def liq_orders(self):
        unique = {}
        for row in self._rows("data/liq/orders/*.jsonl"):
            seen = row.get("observed_at")
            if seen is not None and max(row["t"], seen, row["first_seen"]) <= self.cutoff:
                key = (row["t"], row.get("posSide"), row.get("side"), row.get("sz_contracts"), row.get("bkPx"))
                unique.setdefault(key, row)
        return sorted(unique.values(), key=lambda r: r["t"])

    def klines_1h(self, start, end):
        # Historical market prices: event-time cut only, not a claim about arrival time.
        stop = min(end, self.cutoff) // H * H
        if start >= stop:
            return []
        if start % H:
            raise ValueError("hourly price start must align to UTC hour")
        return [{"t": t, "h": h, "l": l, "c": c} for t, h, l, c in fetch_bars(start, stop, H)]


def classify(episodes, registered, now, horizon_h):
    post, insample, rejected, seen = [], [], [], set()
    for episode in episodes:
        if not isinstance(episode, dict):
            rejected.append("episode must be an object")
            continue
        decision = episode.get("t_decision")
        outcome_at = episode.get("outcome_at")
        cutoff = episode.get("input_cutoff")
        key = (episode.get("group"), decision)
        if (episode.get("group") not in ("cond", "base") or not isinstance(decision, int)
            or isinstance(decision, bool) or not isinstance(outcome_at, int) or not isinstance(cutoff, int)
            or cutoff > decision or decision > now or outcome_at > now
            or outcome_at < decision + horizon_h * H or not num(episode.get("outcome"))):
            rejected.append("invalid, immature, or future-input episode")
            continue
        if key in seen:
            rejected.append("duplicate group/decision episode")
            continue
        seen.add(key)
        (post if registered is not None and decision >= registered else insample).append(episode)
    return post, insample, rejected


def summarize(episodes):
    from formulas import wilson
    out = {}
    for group in ("cond", "base"):
        values = [r["outcome"] for r in episodes if r["group"] == group]
        if not values:
            continue
        summary = {"n": len(values), "mean": sum(values) / len(values)}
        if all(x in (0, 1) for x in values):
            summary["wilson95_descriptive"] = wilson(sum(values), len(values))
        out[group] = summary
    return out


def run_tests(base, now, report_version):
    base = Path(base)
    stamps = read_json(base / "state/registered.json", {})
    records, alerts = [], []
    for path in sorted((base / "tests").glob("*.py")):
        if path.name.startswith("_"):
            continue
        rel, h = path.relative_to(base).as_posix(), test_hash(base, path)
        rat = stamps.get(rel + "@" + h)
        try:
            spec = importlib.util.spec_from_file_location("desk_test_" + h, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            meta = mod.META
            required = ("id", "hypothesis", "condition_def", "decision_time", "outcome_def", "baseline_def", "episode_collapse")
            if not all(isinstance(meta.get(k), str) and meta[k].strip() for k in required):
                raise ValueError("complete frozen test design required in META")
            if not num(meta.get("horizon_h")) or meta["horizon_h"] <= 0:
                raise ValueError("positive horizon_h required")
            result = mod.run(Ctx(base, rat, now))
            if not isinstance(result, dict) or not isinstance(result.get("episodes"), list):
                raise ValueError("run must return an episodes list")
            post, insample, rejected = classify(result["episodes"], rat, now, meta["horizon_h"])
            if rejected:
                alerts.append(f"{rel}: excluded {len(rejected)} invalid/immature/duplicate episodes")
            rec = {"id": meta["id"], "file": rel, "design_sha256": h, "registered": rat,
                   "run": now, "report_version": report_version, "post_registration": summarize(post),
                   "in_sample": summarize(insample), "n_post_registration": len(post),
                   "n_in_sample": len(insample), "n_rejected": len(rejected),
                   "episodes": post + insample, "meta": meta, "notes": result.get("notes", ""),
                   "assurance": "post-registration only; custom code and independence not audited"}
            append_unique(base / "tests/results.jsonl", [rec], lambda r: (r.get("file"), r.get("design_sha256"), r["run"]))
            records.append(rec)
        except Exception as exc:
            alerts.append(f"{rel}: test failed: {type(exc).__name__}: {exc}")
    return records, alerts
