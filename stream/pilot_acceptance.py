"""E1 pilot acceptance (pilot-acceptance-1.0.0, repo 2.29): evaluate a recorder data directory against the criteria
declared in stream/pilot_e1.json BEFORE the pilot ran. Uptime is not success: the verdict counts eligible seconds
(valid, fresh books), sequence gaps, restarts, storage growth and verified partitions, per scoped book and day.

    python -m stream.pilot_acceptance STREAM_DATA_DIR [--criteria stream/pilot_e1.json] [--shocks N]
Verdict: pass | fail | inconclusive, with every figure it used. Nothing here runs the recorder.
"""
import gzip
import hashlib
import json
from pathlib import Path
import sys

VERSION = "pilot-acceptance-1.0.0"


def _rows(p):
    op = gzip.open if str(p).endswith(".gz") else open
    with op(p, "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def evaluate(root, criteria, eligible_shocks=0):
    root = Path(root)
    c = criteria["completeness"]
    out = {"version": VERSION, "criteria": criteria["id"], "books": {}, "days": set(), "problems": []}
    for venue, inst in criteria["scope"]["venues_instruments"]:
        base = root / "derived" / "book1s" / venue / inst
        per_day = {}
        for p in sorted(base.glob("*/*.jsonl.gz")):
            day = p.parent.name
            d = per_day.setdefault(day, {"seconds": set(), "stale": 0})
            for r in _rows(p):
                age = r.get("book_age_ms")
                if age is None or age > c["max_book_age_ms"]:
                    d["stale"] += 1
                    continue
                d["seconds"].add(int(round(r["t"] / 1000)))
        out["books"][f"{venue}/{inst}"] = {day: {"eligible_seconds": len(v["seconds"]), "share": round(len(v["seconds"]) / 86400, 5),
                                                 "stale_rows": v["stale"]} for day, v in per_day.items()}
        out["days"] |= set(per_day)
    gaps = {}
    for p in sorted((root / "derived" / "gaps").glob("*.jsonl")):
        for g in _rows(p):
            k = (p.stem, "restart" if "restart" in str(g.get("reason")) or g.get("venue") == "service" else "sequence/other")
            gaps[k] = gaps.get(k, 0) + 1
    out["gaps"] = {f"{d}:{k}": n for (d, k), n in sorted(gaps.items())}
    by_day_bytes, verified, bad = {}, 0, 0
    for p in sorted((root / "manifest").glob("*.jsonl")):
        for m in _rows(p):
            by_day_bytes[p.stem] = by_day_bytes.get(p.stem, 0) + int(m.get("bytes") or 0)
            f = root / m["key"]
            if f.exists():
                if hashlib.sha256(f.read_bytes()).hexdigest() == m.get("sha256"):
                    verified += 1
                else:
                    bad += 1
    out.update(bytes_per_day=by_day_bytes, partitions_verified=verified, partitions_hash_mismatch=bad)
    full_days = sorted(out.pop("days"))[1:-1]          # first and last days are partial by construction
    fails = []
    for book, days in out["books"].items():
        for d in full_days:
            sh = days.get(d, {"share": 0.0})["share"]
            if sh < c["eligible_second_share_min"]:
                fails.append(f"{book} {d}: eligible share {sh} < {c['eligible_second_share_min']}")
    for d in full_days:
        if gaps.get((d, "sequence/other"), 0) > c["sequence_gaps_per_day_max"]:
            fails.append(f"{d}: sequence/other gaps {gaps[(d, 'sequence/other')]} > {c['sequence_gaps_per_day_max']}")
        if gaps.get((d, "restart"), 0) > c["restart_gaps_per_day_max"]:
            fails.append(f"{d}: restarts {gaps[(d, 'restart')]}")
        if by_day_bytes.get(d, 0) > criteria["resources"]["raw_bytes_per_day_max"]:
            fails.append(f"{d}: bytes {by_day_bytes[d]} over budget")
    if bad:
        fails.append(f"{bad} partition(s) fail their manifest hash")
    if not full_days:
        verdict = "inconclusive"
        fails.append("no full day recorded")
    elif fails:
        verdict = "fail"
    elif eligible_shocks < 20:
        verdict = "inconclusive"
    else:
        verdict = "pass"
    out.update(full_days=full_days, eligible_shocks=eligible_shocks, findings=fails, verdict=verdict)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    crit = Path(__file__).with_name("pilot_e1.json")
    shocks = 0
    if "--criteria" in args:
        crit = Path(args[args.index("--criteria") + 1])
    if "--shocks" in args:
        shocks = int(args[args.index("--shocks") + 1])
    print(json.dumps(evaluate(args[0], json.loads(crit.read_text()), shocks), indent=1, default=str))
