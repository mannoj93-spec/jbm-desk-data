import sys, json, datetime as dt, time
sys.path.insert(0, "/home/claude/pkg/crypto-desk")
import range_model as R
open_holdout = sys.argv[1] == "holdout"
k = json.load(open("/home/claude/o21/klines_4h.json")); d = json.load(open("/home/claude/o21/dvol_1h.json"))
rel = R.load_calendar("/home/claude/pkg/crypto-desk/data/releases_2020_2026.csv")
t0 = time.time()
panel = R.build_panel(k["rows"], rel, d["rows"])
print("panel", {h: len(v) for h, v in panel.items()}, round(time.time() - t0, 1), "s")
res = R.run_o21(panel, open_holdout=open_holdout)
res["run_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
res["data"] = {"klines_state": k["state"], "klines_files": len(k["manifest"]),
               "klines_manifest_sha256": [m["sha256"] for m in k["manifest"]],
               "dvol_state": d["state"], "dvol_sha256": d["report"]["sha256"], "calendar_events": len(rel)}
out = "/home/claude/o21/o21_" + ("holdout" if open_holdout else "validation") + ".json"
json.dump(res, open(out, "w"), indent=1, default=str)
print("wrote", out, round(time.time() - t0, 1), "s")
