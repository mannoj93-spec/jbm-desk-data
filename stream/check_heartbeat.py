"""Exit non-zero when the streaming service's heartbeat is stale or a connection is down.

  python -m stream.check_heartbeat /var/lib/jbm-stream [--max-age 60] [--max-down 120]

Prints one JSON line (the verdict and the reasons). Suitable for a systemd timer, cron, or any
external monitor; it reads only heartbeat.json and never touches the data partitions.
"""
import argparse
import json
from pathlib import Path
import sys
import time


def check(root, max_age_s=60, max_down_s=120, now_ms=None):
    now_ms = now_ms if now_ms is not None else int(time.time() * 1000)
    p = Path(root) / "heartbeat.json"
    if not p.exists():
        return {"ok": False, "reasons": ["heartbeat.json missing: service never started here"]}
    hb = json.loads(p.read_text())
    reasons = []
    age = (now_ms - hb["t"]) / 1000
    if age > max_age_s:
        reasons.append(f"heartbeat {age:.0f} s old (limit {max_age_s})")
    for venue, c in (hb.get("connections") or {}).items():
        last = c.get("last_msg")
        silent = (now_ms - last) / 1000 if last else None
        if not c.get("connected") and (silent is None or silent > max_down_s):
            reasons.append(f"{venue}: disconnected, last message {'never' if silent is None else f'{silent:.0f} s ago'}")
        elif silent is not None and silent > max_down_s:
            reasons.append(f"{venue}: no message for {silent:.0f} s")
    fails = {k: v for k, v in (hb.get("counters") or {}).items() if k.startswith("upload_failures")}
    return {"ok": not reasons, "reasons": reasons, "heartbeat_age_s": round(age, 1), "version": hb.get("version"),
            "upload_failures": fails, "buffer_bytes": hb.get("buffer_bytes")}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--max-age", type=float, default=60)
    ap.add_argument("--max-down", type=float, default=120)
    a = ap.parse_args(argv)
    v = check(a.root, a.max_age, a.max_down)
    print(json.dumps(v, sort_keys=True))
    return 0 if v["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
