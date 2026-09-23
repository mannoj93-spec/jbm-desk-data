"""Research lab entry point.

  python -m lab.run update                       prospective pass over the collector's stored data
  python -m lab.run update --reconstruct-days 60 also an exploratory historical reconstruction
                                                 (public Binance 1-minute history for BTC perp/spot,
                                                 ETH, SOL; cached under LAB_CACHE, never committed)
  python -m lab.run update --no-write            compute and print; write nothing

Writes (unless --no-write): research/events, research/outcomes (idempotent), research/experiments
(one compact row per design per run), research/ledger/variants.jsonl (every variant, null results
included), research/evidence/cards/*.json, reports/research.md, reports/skill_proposals.md and the
design registration clock state/lab_registered.json. Budget: LAB_BUDGET seconds (default 900); a
design not reached inside the budget is reported as not run, never silently dropped. A module
that raises is reported as an error on its card; the others still run and are written.
Never places trades, registers forecasts, or edits skill files.
"""
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

from lab import evidence, experiments
from lab.common import LAB_VERSION, ROOT, append, code_hash, iso, read_dir
from lab.data import Store, fetch_history, history_window

MODULES = {"flow_absorption": "lab.modules.flow_absorption", "account_behavior": "lab.modules.accounts",
           "liq_exposure": "lab.modules.liq_exposure", "twap_lifecycle": "lab.modules.twap",
           "liquidity_recovery": "lab.modules.liquidity", "options_disagreement": "lab.modules.options_disagreement",
           "cross_asset": "lab.modules.cross_asset", "deleveraging": "lab.modules.deleveraging"}
RECON_SERIES = ("binance_klines_1m_BTCUSDT_perp", "binance_klines_1m_BTCUSDT_spot",
                "binance_klines_1m_ETHUSDT_perp", "binance_klines_1m_SOLUSDT_perp")
INPUT_DIRS = ("data/prices", "data/snap", "data/series/binance_funding_settled", "data/options", "data/hl_accounts",
              "data/hl_enrich", "data/okx_insurance", "data/liq/orders", "state/hl_cohort_fixed_v2.json")


class Lab:
    def __init__(self, base, now, write=True):
        self.base, self.now, self.write = Path(base), now, write
        self.store = Store(base, cutoff=now)
        self.code = code_hash()
        self.history, self.history_sha = {}, {}


def input_hashes(base, cutoff_note):
    """sha256 per input dataset (over relative paths and bytes, sorted): with the commit, this pins
    exactly what the run read."""
    out = {}
    for rel in INPUT_DIRS:
        p = Path(base) / rel
        files = [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file()) if p.exists() else []
        h = hashlib.sha256()
        for f in files:
            h.update(f.relative_to(base).as_posix().encode() + b"\0" + f.read_bytes() + b"\0")
        out[rel] = {"files": len(files), "sha256": h.hexdigest() if files else None}
    out["_note"] = cutoff_note
    return out


def git_commit(base):
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=base, capture_output=True, text=True,
                              timeout=10).stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def compact(result):
    ph = None
    rows = []
    for v in result.get("variants", []):
        rows.append({"name": v["name"], "passes": [
            {"basis": p["basis"], "state": p["state"], "firings": p["firings"], "episodes": p["episodes"],
             "immature": p["immature_labels"], "incomplete": p["incomplete_labels"]} for p in v["passes"]]})
    return {"t": result["t"], "design": result["design"], "design_sha256": result.get("design_sha256"),
            "status": result["status"], "status_reason": result["status_reason"], "variants": rows,
            "lab_version": LAB_VERSION, "code_sha256": result.get("code_sha256"), "error": result.get("error"),
            "seconds": result.get("seconds")}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["update"])
    ap.add_argument("--base", default=str(ROOT))
    ap.add_argument("--reconstruct-days", type=int, default=0)
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--designs", default="", help="comma-separated design ids (default: all)")
    ap.add_argument("--now", type=int, default=None, help="cutoff in ms (default: now); for reproduction")
    a = ap.parse_args(argv)
    t0 = time.monotonic()
    budget = float(os.environ.get("LAB_BUDGET", 900))
    now = a.now or int(time.time() * 1000)
    lab = Lab(a.base, now, write=not a.no_write)
    if a.reconstruct_days:
        start, end = history_window(a.reconstruct_days, now)
        for name in RECON_SERIES:
            try:
                lab.history[name], lab.history_sha[name] = fetch_history(name, start, end)
            except Exception as exc:            # reconstruction is optional; its failure is reported
                print(f"history {name}: {type(exc).__name__}: {exc}", file=sys.stderr)
    designs = [experiments.load_design(p) for p in experiments.design_files(a.base)]
    if a.designs:
        designs = [d for d in designs if d["id"] in a.designs.split(",")]
    registered = (experiments.register(a.base, designs, now) if lab.write else
                  {d["id"]: None for d in designs})
    commit = git_commit(a.base)
    hashes = input_hashes(a.base, f"cutoff {iso(now)}; records with observed_at after the cutoff are ignored")
    prior_ledger = read_dir(a.base, "research/ledger")
    results, ledger = [], []
    for d in designs:
        if time.monotonic() - t0 > budget:
            results.append({"t": now, "design": d["id"], "design_sha256": d["_sha256"], "status": "not run",
                            "status_reason": f"lab budget {budget:.0f} s exhausted", "variants": [],
                            "registered": registered.get(d["id"]), "code_sha256": lab.code})
            continue
        s0 = time.monotonic()
        try:
            mod = importlib.import_module(MODULES[d["module"]])
            res, led = experiments.run_design(lab, d, mod, registered.get(d["id"]), d.get("superseded_by") is not None)
        except Exception as exc:
            res, led = {"t": now, "design": d["id"], "design_sha256": d["_sha256"], "status": "error",
                        "status_reason": f"{type(exc).__name__}: {exc}", "variants": [],
                        "registered": registered.get(d["id"]), "code_sha256": lab.code,
                        "error": traceback.format_exc()[-1500:]}, []
        res["seconds"] = round(time.monotonic() - s0, 1)
        results.append(res)
        ledger.extend(led)
    cards = []
    for d, res in zip(designs, results):
        if not res.get("variants"):
            cards.append({"schema": evidence.CARD_SCHEMA, "design": d["id"], "module": d["module"], "family": d["family"],
                          "condition": d["question"], "status": res["status"], "status_reason": res["status_reason"],
                          "primary_horizon_min": d["outcome"]["primary_horizon"],
                          "min_independent_episodes": d["min_independent_episodes"], "passes": {},
                          "contradictory_evidence": [], "error": res.get("error"),
                          "multiple_testing": {"variants_tested_in_family": None}, "generated_at": iso(now)})
            continue
        fam = {(r["design_sha256"], r["variant"]) for r in prior_ledger + ledger if r["family"] == d["family"]}
        cards.append(evidence.card(d, res, len(fam), commit, hashes))
    meta = {"code_sha256": lab.code, "commit": commit, "seconds": round(time.monotonic() - t0, 1)}
    if lab.write:
        append(a.base, "research/experiments", [dict(compact(r), t_event=r["t"]) for r in results],
               key=lambda r: (r["t"], r["design"]))
        append(a.base, "research/ledger", [dict(r, t_event=r["t"]) for r in ledger],
               key=lambda r: (r["t"], r["design"], r["variant"], r["basis"]))
        evidence.write_cards(a.base, cards)
        (Path(a.base) / "reports").mkdir(exist_ok=True)
        (Path(a.base) / "reports/research.md").write_text(_report(cards, now, meta))
        (Path(a.base) / "reports/skill_proposals.md").write_text(evidence.skill_proposals(cards, now))
    summary = {"t": iso(now), "seconds": meta["seconds"], "commit": commit,
               "designs": {r["design"]: {"status": r["status"], "reason": r["status_reason"], "seconds": r.get("seconds"),
                                         "passes": [(p["basis"], p["state"], p["episodes"])
                                                    for v in r.get("variants", [])[:1] for p in v["passes"]]}
                           for r in results}}
    print(json.dumps(summary, indent=1))
    return 1 if any(r["status"] == "error" for r in results) else 0


def _report(cards, now, meta):
    full = [c for c in cards if "comparison" in c]
    text = evidence.report(full, now, meta)
    broken = [c for c in cards if "comparison" not in c]
    if broken:
        text += "\n## Designs not evaluated this run\n\n" + "\n".join(
            f"- {c['design']}: {c['status']} - {c['status_reason']}" for c in broken) + "\n"
    return text


if __name__ == "__main__":
    sys.exit(main())
