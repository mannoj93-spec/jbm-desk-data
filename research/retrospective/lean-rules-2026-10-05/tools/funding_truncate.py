"""Truncation test for funding.json. Reads the fetched file, writes candidate truncations with the
same json.dump call as fetch.py (json.dump(fr, open(path,'w')), default separators), prints hashes.
Rows are not altered; only trailing settlements are dropped."""
import json, hashlib, sys, datetime as dt
src, outdir = sys.argv[1], sys.argv[2]
fr = json.load(open(src))
target = "7382cc208ebd9ed9f9f566c57180545faee1adacd7d523e836581ec2efec738f"
def ms(s): return int(dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() * 1000)
cands = {
    "count_7411": fr[:7411],
    "le_2026-10-04T23:59:59Z": [x for x in fr if x["fundingTime"] <= ms("2026-10-04T23:59:59Z")],
    "le_2026-10-06T00:41:43Z_orig_fetch_time": [x for x in fr if x["fundingTime"] <= ms("2026-10-06T00:41:43Z")],
}
# sanity: re-dump of the full fetched list reproduces the fetched file bytes
full = json.dumps(fr)
print("re-dump of full fetched list identical to file bytes:", full == open(src).read())
for k, v in cands.items():
    p = f"{outdir}/funding.{k}.json"
    json.dump(v, open(p, "w"))
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    last = dt.datetime.fromtimestamp(v[-1]["fundingTime"] / 1000, dt.timezone.utc).isoformat()
    print(f"{k:42} n={len(v)} last={last} sha256={h} match={h == target}")
print("dropped (beyond 7411):")
for x in fr[7411:]:
    print(" ", dt.datetime.fromtimestamp(x["fundingTime"] / 1000, dt.timezone.utc).isoformat(), x)
