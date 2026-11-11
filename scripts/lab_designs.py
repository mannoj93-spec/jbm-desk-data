#!/usr/bin/env python3
"""lab_designs - the designs the scheduled lab runs (repo 2.30.10).

    python scripts/lab_designs.py            # comma-separated active design ids, for `lab.run --designs`
    python scripts/lab_designs.py --json     # active and parked, with the recorded reasons

Active = every design in lab/designs/ that research_lab_ops.json does not park. The lab's own code is unchanged:
`lab.run` already accepts `--designs`, and this only chooses its argument. A parked id that is not a design, a
duplicate, a malformed entry or an empty active list is an error (exit 2), never a silent "run everything" or
"run nothing".
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPS = "research_lab_ops.json"
SCHEMA = "research-lab-operations/1"


def parked(base=ROOT):
    """{design id: entry}. A missing file parks nothing; a file that is present must be valid."""
    path = Path(base) / OPS
    if not path.exists():
        return {}
    doc = json.loads(path.read_text())
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA or not isinstance(doc.get("parked"), list):
        raise ValueError(f"{OPS}: unknown schema or no 'parked' list")
    out = {}
    for e in doc["parked"]:
        if not (isinstance(e, dict) and all(isinstance(e.get(k), str) and e[k] for k in ("design", "decided", "by", "reason"))):
            raise ValueError(f"{OPS}: a parked entry needs design, decided, by and reason")
        if e["design"] in out:
            raise ValueError(f"{OPS}: {e['design']} is parked twice")
        out[e["design"]] = e
    return out


def design_ids(base=ROOT):
    return [json.loads(p.read_text())["id"] for p in sorted((Path(base) / "lab/designs").glob("*.json"))]


def active(base=ROOT):
    ids, off = design_ids(base), parked(base)
    unknown = sorted(set(off) - set(ids))
    if unknown:
        raise ValueError(f"{OPS}: parked design(s) not in lab/designs: {', '.join(unknown)}")
    out = [i for i in ids if i not in off]
    if not out:
        raise ValueError(f"{OPS}: every design is parked; the lab would run nothing")
    return out


def main(argv):
    try:
        act, off = active(), parked()
    except (ValueError, OSError, KeyError) as exc:
        print(f"lab designs: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"active": act, "parked": off}, indent=1, sort_keys=True) if "--json" in argv else ",".join(act))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
