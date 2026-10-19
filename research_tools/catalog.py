"""The data and provenance catalog (catalog-1.0.0, repo 2.29): research_tools/catalog.json is the machine-readable record of every
stored dataset and feature family - source, instrument, units, cadence, event semantics, availability clocks,
revision behaviour, missingness, retention, quality checks, storage, recoverability and whether raw bytes are kept.

  validate(catalog)        problems ([] = valid): required fields, known instruments, feature inputs that exist
  measure(base, catalog)   for each dataset with a path: files, rows, first/last observed_at (a measured line beside the
                           declared one; nothing here is inferred)
Run: python -m research_tools.catalog [--measure]
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from storage import read_rows  # noqa: E402

VERSION = "catalog-1.0.0"
REQUIRED = ("id", "path", "source", "availability")
FAMILY_REQUIRED = ("id", "module", "status", "inputs")


def load(path=None):
    return json.loads(Path(path or Path(__file__).with_name("catalog.json")).read_text())


def validate(cat):
    probs = []
    if cat.get("schema") != "desk-data-catalog/1":
        probs.append(f"schema {cat.get('schema')!r}")
    ids = set()
    insts = {i["id"] for i in cat.get("instruments", [])}
    for d in cat.get("datasets", []):
        for f in REQUIRED:
            if not d.get(f):
                probs.append(f"{d.get('id')}: {f} missing")
        if d.get("instrument") and d["instrument"] not in insts and not d["instrument"].endswith(("ETHUSDT-perp", "SOLUSDT-perp")):
            probs.append(f"{d['id']}: instrument {d['instrument']} not in the instrument table")
        if "raw_bytes_retained" not in d and d.get("id") not in ("runs",):
            probs.append(f"{d.get('id')}: raw_bytes_retained not stated")
        if "event time" in str(d.get("availability", "")).lower() and "never" not in str(d.get("availability")).lower():
            probs.append(f"{d['id']}: availability defined from event time")
        ids.add(d["id"])
    for fam in cat.get("feature_families", []):
        for f in FAMILY_REQUIRED:
            if not fam.get(f):
                probs.append(f"family {fam.get('id')}: {f} missing")
        for i in fam.get("inputs", []):
            if i.split(".")[0] not in ids:
                probs.append(f"family {fam['id']}: input {i} is not a catalogued dataset")
    return probs


def measure(base=ROOT, cat=None):
    cat = cat or load()
    base = Path(base)
    out = {}
    for d in cat["datasets"]:
        pat = d["path"]
        if "{" in pat or pat.startswith("STREAM_DATA_DIR") or "*" not in pat or pat.startswith("data/hl_*"):
            out[d["id"]] = {"state": "not measured here (pattern outside the repository or composite)"}
            continue
        files = sorted(base.glob(pat))
        n, first, last = 0, None, None
        for p in files[-3:]:
            for r in read_rows(p):
                n += 1
                o = r.get("observed_at")
                o = int(o) if isinstance(o, (int, str)) and str(o).isdigit() else None
                if o is not None:
                    first = o if first is None else min(first, o)
                    last = o if last is None else max(last, o)
        out[d["id"]] = {"files": len(files), "rows_in_last_3_files": n, "first_observed_ms_last_3_files": first,
                        "last_observed_ms": last}
    return out


if __name__ == "__main__":
    c = load()
    p = validate(c)
    print(json.dumps({"version": VERSION, "problems": p, "measured": measure() if "--measure" in sys.argv else None},
                     indent=1))
    sys.exit(1 if p else 0)
