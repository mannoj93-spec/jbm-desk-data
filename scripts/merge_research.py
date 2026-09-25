#!/usr/bin/env python3
"""Merge research outputs computed on an earlier checkout into the current checkout (research.yml).

The lab computes without the repository-write lock, so by the time its outputs are persisted the
checkout may hold newer commits. This merge never loses or rewinds newer content:
  *.jsonl under research/            line union: existing lines kept in order, new lines appended
  research/v2/**/checkpoints.jsonl   the same, except that a look already recorded in the checkout
                                     is never recorded again (the first completed record stands)
  Conflict rule (2.11): if an incoming control selection or checkpoint has a key that already
  holds a different record in the checkout, the incoming batch was computed from a losing record;
  NOTHING is merged, the conflict is printed and the script exits 3 (the persist job fails
  visibly; committed selections, checkpoints and evidence stand).
  research/v2/<design>/<version>/controls/*.jsonl
                                     the same, keyed by (control_policy, control_hour): the first
                                     stored hourly control selection stands
  research/v2/<design>/<version>/events/*.jsonl
                                     the same, keyed by decision_key: a frozen decision already in
                                     the checkout is never recorded a second time
  state/lab_registrations.json       existing keys never changed; new keys added
  state/lab_run_state.json           per key, the entry with the later last_cutoff wins
  research/evidence/**/*.json,       replaced only if the incoming file is at least as new
  reports/research.md,               (generated_at field, or the "Generated <time>" line)
  reports/skill_proposals.md
  reports/latest.md                  replaced only if its input cutoff AND generation time are not
                                     older than the file already in the checkout
Usage: merge_research.py INCOMING_DIR REPO_DIR
"""
import json
from pathlib import Path
import re
import shutil
import sys

STAMP = re.compile(r"Generated (\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}Z)")
CUTOFF = re.compile(r"Input cutoff: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}Z)")


def stamp(path):
    if not path.exists():
        return ""
    text = path.read_text()
    if path.suffix == ".json":
        try:
            return str(json.loads(text).get("generated_at") or json.loads(text).get("updated") or "")
        except ValueError:
            return ""
    m = STAMP.search(text)
    return m.group(1).replace(" ", "T") if m else ""


def merge_jsonl(src, dst, key=None):
    old = dst.read_text().splitlines() if dst.exists() else []
    seen = set(old)
    add = [l for l in src.read_text().splitlines() if l.strip() and l not in seen]
    if key is not None:                              # one record per key; existing records win
        have = {key(json.loads(l)) for l in old if l.strip()}
        keep = []
        for l in add:
            k = key(json.loads(l))
            if k not in have:
                have.add(k)
                keep.append(l)
        add = keep
    if add:
        dst.parent.mkdir(parents=True, exist_ok=True)
        with open(dst, "a") as fh:
            if old and not dst.read_text().endswith("\n"):
                fh.write("\n")
            fh.write("\n".join(add) + "\n")
    return len(add)


def conflicts(incoming, repo):
    """Keyed records the incoming batch would lose: an incoming control selection or checkpoint whose
    key already holds a DIFFERENT record in the checkout. The incoming evidence, checkpoints and
    reports were computed from the losing record, so they must not be published beside the winner."""
    keyed = {"controls": lambda x: (x.get("control_policy"), x.get("control_hour")),
             "checkpoints.jsonl": lambda x: x.get("look")}
    out = []
    for src in sorted(incoming.rglob("*.jsonl")):
        r = src.relative_to(incoming).as_posix()
        kind = "checkpoints.jsonl" if src.name == "checkpoints.jsonl" else src.parent.name
        dst = repo / r
        if not r.startswith("research/v2/") or kind not in keyed or not dst.exists():
            continue
        have = {}
        for line in dst.read_text().splitlines():
            if line.strip():
                have.setdefault(keyed[kind](json.loads(line)), set()).add(line)
        for line in src.read_text().splitlines():
            if line.strip():
                k = keyed[kind](json.loads(line))
                if k in have and line not in have[k]:       # a legacy duplicate already present is no conflict
                    out.append(f"{r} key {k}")
    return out


def main(incoming, repo):
    incoming, repo = Path(incoming), Path(repo)
    log = []
    bad = conflicts(incoming, repo)
    if bad:
        # Nothing from this batch is merged: the committed selections, checkpoints and evidence stand,
        # and the next (serialized) lab run recomputes from the stored winners.
        print("RECONCILIATION CONFLICT - incoming research outputs rejected, nothing merged:\n  "
              + "\n  ".join(bad), file=sys.stderr)
        return 3
    for src in sorted(incoming.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(incoming)
        dst = repo / rel
        r = rel.as_posix()
        if r.startswith("research/") and src.name == "checkpoints.jsonl":
            log.append(f"{r}: +{merge_jsonl(src, dst, key=lambda x: x.get('look'))} checkpoint records")
        elif r.startswith("research/v2/") and src.parent.name == "controls" and src.suffix == ".jsonl":
            log.append(f"{r}: +{merge_jsonl(src, dst, key=lambda x: (x.get('control_policy'), x.get('control_hour')))}"
                       " control selections")
        elif r.startswith("research/v2/") and src.parent.name == "events" and src.suffix == ".jsonl":
            log.append(f"{r}: +{merge_jsonl(src, dst, key=lambda x: x.get('decision_key'))} frozen decisions")
        elif r.startswith("research/") and src.suffix == ".jsonl":
            log.append(f"{r}: +{merge_jsonl(src, dst)} lines")
        elif r == "state/lab_registrations.json":
            cur = json.loads(dst.read_text()) if dst.exists() else {}
            new = {k: v for k, v in json.loads(src.read_text()).items() if k not in cur}
            cur.update(new)
            dst.write_text(json.dumps(cur, indent=1, sort_keys=True))
            log.append(f"{r}: +{len(new)} registrations")
        elif r == "state/lab_run_state.json":
            cur = json.loads(dst.read_text()) if dst.exists() else {}
            for k, v in json.loads(src.read_text()).items():
                if k not in cur or (v.get("last_cutoff") or 0) >= (cur[k].get("last_cutoff") or 0):
                    cur[k] = v
            dst.write_text(json.dumps(cur, indent=1, sort_keys=True))
            log.append(f"{r}: merged")
        elif r == "reports/latest.md":
            def key(p):
                if not p.exists():
                    return ("", "")
                m = CUTOFF.search(p.read_text())
                return (m.group(1) if m else "", stamp(p))
            if key(src) >= key(dst):
                shutil.copyfile(src, dst)
                log.append(f"{r}: replaced")
            else:
                log.append(f"{r}: kept newer existing file")
        elif r.startswith(("research/evidence/", "reports/")):
            if stamp(src) >= stamp(dst):
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
                log.append(f"{r}: replaced")
            else:
                log.append(f"{r}: kept newer existing file")
    print("\n".join(log))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
