#!/usr/bin/env python3
"""Merge research outputs computed on an earlier checkout into the current checkout (research.yml).

The lab computes without the repository-write lock, so by the time its outputs are persisted the
checkout may hold newer commits. This merge never loses or rewinds newer content:
  *.jsonl under research/            line union: existing lines kept in order (their original
                                     bytes), new records appended; a record is "already present"
                                     when its CANONICAL JSON (parsed, object keys sorted at every
                                     depth, no insignificant whitespace) equals an existing line's,
                                     so a reformatted copy is neither appended nor rewritten
  research/v2/**/checkpoints.jsonl   the same, except that a look already recorded in the checkout
                                     is never recorded again (the first completed record stands)
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

Two checks run BEFORE anything is written; if either fails NOTHING is merged:
  Conflict (2.11, canonical equality 2.12), exit 3: an incoming control selection or checkpoint
    whose key already holds a record in the checkout must canonically equal the checkout's FIRST
    (authoritative) record for that key; the first incoming record for a key must be that same
    record; one batch may not carry two different records for one key. Values, array order,
    strings versus numbers and every metadata field are significant; no numerical tolerance. A
    legacy duplicate already in the checkout, repeated verbatim, is no conflict, but a new record
    can never be matched against it.
  Publication gate (2.12), exit 4: research outputs are published only with the lab's
    machine-readable summary (INCOMING/lab-summary.json, schema lab_summary/2) and only where they
    agree with it: every design entry internally consistent (validation status, publication
    decision, status, the single cutoff); a design whose evaluation is not valid (failed, incomplete
    or missing required integrity, error, not run) contributes no new checkpoint, frozen decision or
    outcome row and no advanced watermark; every changed card, the index, the research report and
    the skill proposals match the summary's design, evaluation version, cutoff and publication
    decision (a proposal only for a proposal-eligible design); every design of the summary brings its
    card, and the index and both reports are present, so no older promotion output stays current;
    every research row parses. Missing, stale or contradictory metadata blocks the batch. The failed attempt's own diagnostics (its blocked card, report and
    the control selections it stored) are published, so the latest failure stays visible.
Usage: merge_research.py INCOMING_DIR REPO_DIR
"""
import json
from pathlib import Path
import re
import shutil
import sys

STAMP = re.compile(r"Generated (\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}Z)")
CUTOFF = re.compile(r"Input cutoff: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}Z)")
PROPOSAL = re.compile(r"^## (\S+) @ (\S+)\s*$", re.M)
SUMMARY = "lab-summary.json"
SUMMARY_SCHEMA = "lab_summary/2"
VALID_INTEGRITY = ("passed", "not_required")
KEYED = {"controls": lambda x: (x.get("control_policy"), x.get("control_hour")),
         "checkpoints.jsonl": lambda x: x.get("look")}


def _no_dupes(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError(f"duplicate object key in {keys}")
    return dict(pairs)


def _finite(text):
    x = float(text)
    if x in (float("inf"), float("-inf")):
        raise ValueError(f"number {text} is out of range")         # 1e400 and 2e400 must not compare equal
    return x


def canon(line):
    """Deterministic canonical form of one JSON record: object keys sorted at every depth, no
    insignificant whitespace; array order, value types (1 vs 1.0 vs "1", -0.0) and all fields
    preserved; numbers compare as the IEEE doubles the lab writes (no tolerance). A record that is
    not a JSON object, has a duplicated object key, or a number out of double range has no single
    meaning and is rejected (ValueError)."""
    obj = json.loads(line, object_pairs_hook=_no_dupes, parse_float=_finite)
    if not isinstance(obj, dict):
        raise ValueError("record is not a JSON object")
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=True)


def _lines(path):
    return [l for l in path.read_text().splitlines() if l.strip()] if path.exists() else []


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
    old = _lines(dst)
    seen = {canon(l) for l in old}
    add = []
    for l in _lines(src):
        c = canon(l)
        if c not in seen:                            # equivalent formatting is the same record
            seen.add(c)
            add.append(l)
    if key is not None:                              # one record per key; existing records win
        have = {key(json.loads(l)) for l in old}
        keep = []
        for l in add:
            k = key(json.loads(l))
            if k not in have:
                have.add(k)
                keep.append(l)
        add = keep
    if add:
        dst.parent.mkdir(parents=True, exist_ok=True)
        raw = dst.read_text() if dst.exists() else ""
        with open(dst, "a") as fh:
            if raw and not raw.endswith("\n"):
                fh.write("\n")
            fh.write("\n".join(add) + "\n")
    return len(add)


def _kind(rel):
    """(design, version, kind) of a research/v2 per-version row file, else None."""
    parts = rel.split("/")
    if len(parts) == 5 and parts[:2] == ["research", "v2"] and parts[4] == "checkpoints.jsonl":
        return parts[2], parts[3], "checkpoints"
    if len(parts) == 6 and parts[:2] == ["research", "v2"] and parts[4] in ("controls", "events", "outcomes") \
            and parts[5].endswith(".jsonl"):
        return parts[2], parts[3], parts[4]
    return None


def conflicts(incoming, repo):
    """Keyed records the incoming batch would lose (see the module docstring). The incoming evidence,
    checkpoints and reports were computed from the losing record, so they must not be published."""
    out = []
    for src in sorted(incoming.rglob("*.jsonl")):
        r = src.relative_to(incoming).as_posix()
        kind = "checkpoints.jsonl" if src.name == "checkpoints.jsonl" else src.parent.name
        if not r.startswith("research/v2/") or kind not in KEYED:
            continue
        key = KEYED[kind]
        try:
            first, present = {}, set()
            for line in _lines(repo / r):
                c = canon(line)
                present.add(c)
                first.setdefault(key(json.loads(line)), c)
            inc_first = {}
            for line in _lines(src):
                c = canon(line)
                k = key(json.loads(line))
                if k in inc_first and inc_first[k] != c and c not in present:
                    out.append(f"{r} key {k}: two different records in the incoming batch")
                inc_first.setdefault(k, c)
                if k in first and c not in present:
                    out.append(f"{r} key {k}: differs from the stored record")
            for k, c in inc_first.items():
                if k in first and first[k] != c and f"{r} key {k}: differs from the stored record" not in out:
                    out.append(f"{r} key {k}: the batch's first record is not the stored (first) record")
        except (ValueError, AttributeError, TypeError) as exc:
            out.append(f"{r}: unreadable record ({exc})")
    return out


def _load_summary(incoming):
    p = incoming / SUMMARY
    if not p.exists():
        return None, f"{SUMMARY} missing: no publication metadata for these research outputs"
    try:
        s = json.loads(p.read_text())
    except ValueError as exc:
        return None, f"{SUMMARY} unreadable ({exc})"
    if not isinstance(s, dict) or s.get("schema") != SUMMARY_SCHEMA or not isinstance(s.get("designs"), dict) \
            or not isinstance(s.get("cutoff_ms"), int) or not s.get("t"):
        return None, f"{SUMMARY} is not a {SUMMARY_SCHEMA} summary (schema, cutoff or designs missing)"
    return s, None


def _entry_problems(name, e, cut):
    probs = []
    pub, val = e.get("publication"), e.get("validation")
    if not isinstance(pub, dict) or not isinstance(val, dict) or not isinstance(pub.get("evaluation_valid"), bool) \
            or not isinstance(pub.get("proposal_eligible"), bool) or not e.get("version"):
        return [f"{name}: publication metadata incomplete (version, validation or publication decision missing)"]
    valid, vstat, st = pub["evaluation_valid"], val.get("status"), e.get("status")
    if e.get("design") != name or pub.get("design") != name or pub.get("evaluation_version") != e["version"]:
        probs.append(f"{name}: design / evaluation version disagree between the entry and its publication decision")
    if e.get("cutoff_ms") != cut or pub.get("cutoff_ms") != cut:
        probs.append(f"{name}: stale publication metadata (cutoff differs from the run's {cut})")
    if val.get("required") and not e.get("integrity"):
        probs.append(f"{name}: required research integrity result missing")
    if e.get("integrity") and e["integrity"].get("status") != vstat:
        probs.append(f"{name}: integrity result and validation status disagree")
    if (pub.get("validation") or {}).get("status") != vstat:
        probs.append(f"{name}: publication decision records a different validation status")
    if valid != (vstat in VALID_INTEGRITY and st not in ("error", "not run")):
        probs.append(f"{name}: evaluation_valid={valid} contradicts validation {vstat} / status {st}")
    if not valid and st in ("supported", "retired"):
        probs.append(f"{name}: status {st} from an evaluation that is not valid")
    if pub["proposal_eligible"] and not (valid and st == "supported" and pub.get("proposal_checkpoint")):
        probs.append(f"{name}: proposal eligibility without a valid supported evaluation")
    return probs


def publication_problems(incoming, repo):
    """Reasons the incoming research outputs may not be published (see the module docstring)."""
    payload = [p for p in incoming.rglob("*") if p.is_file()
               and (p.relative_to(incoming).as_posix().startswith("research/")
                    or p.relative_to(incoming).as_posix() in ("reports/research.md", "reports/skill_proposals.md",
                                                               "state/lab_run_state.json",
                                                               "state/lab_registrations.json"))]
    if not payload:
        return []
    summ, err = _load_summary(incoming)
    if err:
        return [err]
    cut, D = summ["cutoff_ms"], summ["designs"]
    probs = []
    for name, e in sorted(D.items()):
        probs += _entry_problems(name, e if isinstance(e, dict) else {}, cut)
    if probs:
        return probs
    valid = {n: e["publication"]["evaluation_valid"] for n, e in D.items()}
    for src in sorted(incoming.rglob("*.jsonl")):          # every row the merge would read must parse
        if src.relative_to(incoming).as_posix().startswith("research/"):
            for n, line in enumerate(_lines(src), 1):
                try:
                    canon(line)
                except ValueError as exc:
                    probs.append(f"{src.relative_to(incoming).as_posix()} line {n}: unreadable record ({exc})")
    if probs:
        return probs
    for src in sorted(incoming.rglob("*.jsonl")):
        rel = src.relative_to(incoming).as_posix()
        k = _kind(rel)
        if k is None:
            continue
        design, version, kind = k
        present = {canon(l) for l in _lines(repo / rel)}
        new = [json.loads(l) for l in _lines(src) if canon(l) not in present]
        if not new:
            continue
        e = D.get(design)
        if e is None or e["version"] != version:
            probs.append(f"{rel}: {len(new)} new {kind} rows for {design}@{version}, which this run's summary does not cover")
        elif kind != "controls" and not valid[design]:
            probs.append(f"{rel}: {len(new)} new {kind} rows for {design}@{version}, whose evaluation is blocked")
        elif kind == "checkpoints" and any(r.get("design") != design or r.get("version") != version
                                           or r.get("completed_at") != cut for r in new):
            probs.append(f"{rel}: new checkpoint records do not match {design}@{version} at the run's cutoff")
    cards_dir = incoming / "research/evidence/v2"
    current = {f"research/evidence/v2/{n}@{e['version']}.json": n for n, e in D.items()}
    for rel, name in sorted(current.items()):              # every design of the run brings its card
        if not (incoming / rel).exists():
            probs.append(f"{rel}: missing from the batch; the summary covers {name}@{D[name]['version']}")
    for src in sorted(cards_dir.glob("*.json")) if cards_dir.exists() else []:
        rel = src.relative_to(incoming).as_posix()
        dst = repo / rel
        if rel not in current and dst.exists() and dst.read_bytes() == src.read_bytes():
            continue                                       # an unchanged card of another version
        try:
            c = json.loads(src.read_text())
        except ValueError:
            probs.append(f"{rel}: unreadable card")
            continue
        e = D.get(c.get("design")) if isinstance(c, dict) else None
        if e is None or e["version"] != c.get("evaluation_version") or rel not in current:
            probs.append(f"{rel}: card for a design version this run's summary does not cover (stale)")
            continue
        if c.get("cutoff_ms") != cut:
            probs.append(f"{rel}: card cutoff {c.get('cutoff_ms')} differs from the run's {cut} (stale)")
        if c.get("status") != e["status"]:
            probs.append(f"{rel}: card status {c.get('status')} contradicts the summary's {e['status']}")
        if json.dumps(c.get("publication"), sort_keys=True) != json.dumps(e["publication"], sort_keys=True):
            probs.append(f"{rel}: card publication decision contradicts the summary")
        if json.dumps(c.get("research_integrity"), sort_keys=True) != json.dumps(e.get("integrity"), sort_keys=True):
            probs.append(f"{rel}: card research integrity contradicts the summary")
    idx = incoming / "research/evidence/index.json"
    for rel in ("research/evidence/index.json", "reports/research.md", "reports/skill_proposals.md"):
        if D and not (incoming / rel).exists():
            probs.append(f"{rel}: missing from the batch (an older copy must not stay current)")
    if idx.exists():
        try:
            designs = json.loads(idx.read_text()).get("designs") or {}
            for name, e in D.items():
                ent = designs.get(name) or {}
                v = (ent.get("versions") or {}).get(e["version"]) or {}
                if ent.get("current") != e["version"] or v.get("status") != e["status"] \
                        or v.get("evaluation_valid") != valid[name]:
                    probs.append(f"research/evidence/index.json: {name} entry contradicts the summary")
        except (ValueError, AttributeError, TypeError):
            probs.append("research/evidence/index.json: unreadable")
    for rel in ("reports/research.md", "reports/skill_proposals.md"):
        src = incoming / rel
        if not src.exists():
            continue
        if stamp(src) != summ["t"]:
            probs.append(f"{rel}: generated {stamp(src) or 'n/a'}, not at the run's cutoff {summ['t']} (stale)")
        if rel.endswith("skill_proposals.md"):
            named = set(PROPOSAL.findall(src.read_text()))
            eligible = {(n, e["version"]) for n, e in D.items() if e["publication"]["proposal_eligible"]}
            for n, v in sorted(named - eligible):
                probs.append(f"{rel}: proposes a change for {n}@{v}, which is not proposal-eligible")
            for n, v in sorted(eligible - named):
                probs.append(f"{rel}: omits the proposal-eligible {n}@{v}")
    rs = incoming / "state/lab_run_state.json"
    if rs.exists():
        try:
            cur = json.loads((repo / "state/lab_run_state.json").read_text()) if (repo / "state/lab_run_state.json").exists() else {}
            for key, v in json.loads(rs.read_text()).items():
                if v == cur.get(key):
                    continue
                name, _, version = key.partition("@")
                e = D.get(name)
                if (v.get("last_cutoff") or 0) > cut:
                    probs.append(f"state/lab_run_state.json: {key} watermark after the run's cutoff")
                elif e is not None and e["version"] == version and not valid[name] \
                        and (v.get("last_cutoff") or 0) > ((cur.get(key) or {}).get("last_cutoff") or 0):
                    probs.append(f"state/lab_run_state.json: watermark advanced for blocked {key}")
        except (ValueError, AttributeError, TypeError):
            probs.append("state/lab_run_state.json: unreadable")
    return probs


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
    blocked = publication_problems(incoming, repo)
    if blocked:
        print("PUBLICATION BLOCKED - research outputs do not match the lab's publication metadata, nothing merged:\n  "
              + "\n  ".join(blocked), file=sys.stderr)
        return 4
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
