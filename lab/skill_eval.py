"""Compare the current trading-skill files with a proposed revision, against the evidence cards.

  python -m lab.skill_eval --current DIR --revision DIR [--cases FILE] [--out DIR]
  python -m lab.skill_eval ... --live --model MODEL      (optional; needs ANTHROPIC_API_KEY)

Offline mode (deterministic, no network, the default):
  1. file diff      sha256 of every *.md / *.py / *.json file on each side; lines added/removed
  2. case checks    each case in the cases file (default lab/skill_eval_cases.json) states
                    patterns the skill text must / must not contain; scored for both sides
  3. evidence audit every sentence of the revision that names a design (id, module or title
                    from research/evidence/cards) is checked against the card's status: wording
                    such as "supported", "demonstrated", "validated", "edge", "proven" next to a
                    design that is not "supported" is an OVERCLAIM; a revision that drops a
                    caveat the current text had is reported as a regression
Live mode (optional): sends each case's `prompt` to the Anthropic Messages API with the skill text
as the system prompt, once per side, and applies the case's `response_must` / `response_must_not`
patterns to the replies. Without ANTHROPIC_API_KEY it reports "live evaluation not run" and
produces nothing else; no live result is ever synthesised.

Privacy: skill files, prompts and outputs are private. Everything is written to --out (default
~/.jbm-skill-eval), which must be OUTSIDE this repository; the tool refuses a path inside it. It
never modifies either skill directory.
"""
import argparse
import datetime as dt
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import urllib.request

from lab.common import ROOT

CLAIM_WORDS = re.compile(r"\b(supported|demonstrated|validated|proven|edge|reliable signal|works)\b", re.I)
CAVEAT_WORDS = re.compile(r"\b(exploratory|insufficient|not demonstrated|unvalidated|under prospective evaluation|"
                          r"hypothesis|no demonstrated edge|descriptive)\b", re.I)
TEXT_EXT = {".md", ".txt", ".py", ".json", ".yaml", ".yml"}


def skill_files(root):
    root = Path(root)
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*"))
            if p.is_file() and p.suffix in TEXT_EXT}


def text_of(files):
    return "\n".join(b.decode("utf-8", "replace") for k, b in sorted(files.items()) if k.endswith((".md", ".txt")))


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}|\n[-*] ", text) if s.strip()]


def load_cards(base):
    """Current evidence per design: lab-2.0 versioned cards named current in research/evidence/
    index.json; designs without one fall back to the legacy lab-1.0 card (research/evidence/cards)."""
    cards = {}
    base = Path(base)
    for p in sorted((base / "research/evidence/cards").glob("*.json")):
        c = json.loads(p.read_text())
        cards[c["design"]] = c
    index = base / "research/evidence/index.json"
    if index.exists():
        for design, entry in json.loads(index.read_text()).get("designs", {}).items():
            p = base / "research/evidence/v2" / f"{design}@{entry.get('current')}.json"
            if p.exists():
                cards[design] = json.loads(p.read_text())
    return cards


def design_names(card):
    names = {card["design"].lower(), card["module"].lower(), card["module"].replace("_", " ").lower()}
    head = card["design"].split("-", 1)
    if len(head) == 2:
        names.add(head[1].replace("-", " ").lower())
    return {n for n in names if len(n) >= 6}


def evidence_audit(text, cards):
    findings = []
    for s in sentences(text):
        low = s.lower()
        for did, c in cards.items():
            if any(n in low for n in design_names(c)):
                claim = CLAIM_WORDS.search(s)
                negated = re.search(r"\b(not|no|never|un)\w*\s+(yet\s+)?(" + (claim.group(0) if claim else "x") + r")", s, re.I)
                if claim and not negated and c.get("status") != "supported":
                    findings.append({"kind": "overclaim", "design": did, "card_status": c.get("status"),
                                     "word": claim.group(0), "sentence": s[:300]})
                elif claim or CAVEAT_WORDS.search(s):
                    findings.append({"kind": "consistent", "design": did, "card_status": c.get("status"),
                                     "sentence": s[:300]})
    return findings


def run_cases(text, cases):
    out = {}
    for case in cases:
        misses = [p for p in case.get("must", []) if not re.search(p, text, re.I | re.M)]
        hits = [p for p in case.get("must_not", []) if re.search(p, text, re.I | re.M)]
        out[case["id"]] = {"pass": not misses and not hits, "missing": misses, "forbidden_present": hits}
    return out


def diff_files(cur, rev):
    rows = []
    for name in sorted(set(cur) | set(rev)):
        a, b = cur.get(name), rev.get(name)
        if a == b:
            continue
        al = a.decode("utf-8", "replace").splitlines() if a is not None else []
        bl = b.decode("utf-8", "replace").splitlines() if b is not None else []
        d = list(difflib.unified_diff(al, bl, lineterm="", n=0))
        rows.append({"file": name, "status": "added" if a is None else "removed" if b is None else "modified",
                     "lines_added": sum(1 for l in d if l.startswith("+") and not l.startswith("+++")),
                     "lines_removed": sum(1 for l in d if l.startswith("-") and not l.startswith("---"))})
    return rows


def ask(model, system, prompt, key, opener=urllib.request.urlopen):
    body = json.dumps({"model": model, "max_tokens": 800, "system": system,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST",
                                 headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                                          "content-type": "application/json"})
    with opener(req, timeout=120) as resp:
        js = json.loads(resp.read())
    return "".join(part.get("text", "") for part in js.get("content", []))


def live(cases, cur_text, rev_text, model, key, opener=urllib.request.urlopen):
    out = {}
    for case in cases:
        if not case.get("prompt"):
            continue
        res = {}
        for side, system in (("current", cur_text), ("revision", rev_text)):
            try:
                reply = ask(model, system, case["prompt"], key, opener)
            except Exception as exc:
                res[side] = {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}
                continue
            miss = [p for p in case.get("response_must", []) if not re.search(p, reply, re.I | re.M)]
            bad = [p for p in case.get("response_must_not", []) if re.search(p, reply, re.I | re.M)]
            res[side] = {"status": "ok", "pass": not miss and not bad, "missing": miss, "forbidden_present": bad,
                         "reply": reply}
        out[case["id"]] = res
    return out


def evaluate(current, revision, cases, cards):
    cur, rev = skill_files(current), skill_files(revision)
    ct, rt = text_of(cur), text_of(rev)
    cc, rc = run_cases(ct, cases), run_cases(rt, cases)
    ca, ra = evidence_audit(ct, cards), evidence_audit(rt, cards)
    regressions = [k for k in cc if cc[k]["pass"] and not rc[k]["pass"]]
    fixed = [k for k in cc if not cc[k]["pass"] and rc[k]["pass"]]
    return {
        "schema": "skill_eval/1",
        "files": {"current": {k: hashlib.sha256(v).hexdigest() for k, v in cur.items()},
                  "revision": {k: hashlib.sha256(v).hexdigest() for k, v in rev.items()}},
        "diff": diff_files(cur, rev),
        "cases": {"current": cc, "revision": rc, "regressions": regressions, "fixed": fixed},
        "evidence_audit": {"cards": {k: c.get("status") for k, c in cards.items()},
                           "current_overclaims": [f for f in ca if f["kind"] == "overclaim"],
                           "revision_overclaims": [f for f in ra if f["kind"] == "overclaim"],
                           "revision_consistent_mentions": sum(1 for f in ra if f["kind"] == "consistent")},
        "verdict": ("revision introduces overclaims" if [f for f in ra if f["kind"] == "overclaim"] else
                    "revision regresses checks" if regressions else "no regression found by offline checks"),
    }


def markdown(r):
    L = [f"# Skill evaluation ({r['generated_at']})", "", f"Verdict (offline): **{r['verdict']}**", "",
         "## Changed files", ""]
    L += [f"- {d['file']}: {d['status']} (+{d['lines_added']} / -{d['lines_removed']})" for d in r["diff"]] or ["- none"]
    L += ["", "## Case checks", "", "| Case | Current | Revision |", "|---|---|---|"]
    for k in r["cases"]["current"]:
        L.append(f"| {k} | {'pass' if r['cases']['current'][k]['pass'] else 'FAIL'} | "
                 f"{'pass' if r['cases']['revision'][k]['pass'] else 'FAIL'} |")
    L += ["", "## Evidence audit", ""]
    for f in r["evidence_audit"]["revision_overclaims"]:
        L.append(f"- OVERCLAIM ({f['design']} is {f['card_status']}): \"{f['word']}\" in: {f['sentence']}")
    if not r["evidence_audit"]["revision_overclaims"]:
        L.append("- no overclaim found in the revision")
    L += ["", "## Live evaluation", "", r["live"]["status"]]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--current", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--cases", default=str(ROOT / "lab/skill_eval_cases.json"))
    ap.add_argument("--base", default=str(ROOT), help="repository holding research/evidence/cards")
    ap.add_argument("--out", default=str(Path.home() / ".jbm-skill-eval"))
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--model", default=None)
    a = ap.parse_args(argv)
    out = Path(a.out).expanduser().resolve()
    if out == ROOT.resolve() or ROOT.resolve() in out.parents:
        print("refusing to write private evaluation output inside the repository", file=sys.stderr)
        return 2
    cases = json.loads(Path(a.cases).read_text())["cases"]
    r = evaluate(a.current, a.revision, cases, load_cards(a.base))
    r["generated_at"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not a.live:
        r["live"] = {"status": "live evaluation not requested"}
    elif not key or not a.model:
        r["live"] = {"status": "live evaluation not run: " + ("ANTHROPIC_API_KEY not set" if not key else "--model not given")}
    else:
        cur_t, rev_t = text_of(skill_files(a.current)), text_of(skill_files(a.revision))
        r["live"] = {"status": f"live evaluation run with {a.model}", "results": live(cases, cur_t, rev_t, a.model, key)}
    out.mkdir(parents=True, exist_ok=True)
    stamp = r["generated_at"].replace(":", "")
    (out / f"skill_eval_{stamp}.json").write_text(json.dumps(r, indent=1, sort_keys=True))
    (out / f"skill_eval_{stamp}.md").write_text(markdown(r))
    print(json.dumps({"verdict": r["verdict"], "out": str(out), "live": r["live"]["status"],
                      "regressions": r["cases"]["regressions"],
                      "overclaims": len(r["evidence_audit"]["revision_overclaims"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
