#!/usr/bin/env python3
"""skillcheck.py — mechanical consistency check for the crypto-desk package.

    python skillcheck.py /path/to/crypto-desk      # a folder holding the four files

Run by the skill thread on every build, before the package is presented; an ERROR blocks
the present (M-20: nothing reported as done without evidence). It catches the defect class
the audits kept finding by hand — version strings that disagree, a citation pointing at a
section that doesn't define the thing, IDs cited but never defined, the same figure carried
in two files. It does not judge content. WARN lines are for the thread to decide.
"""
import os
import re
import sys
from collections import defaultdict

FILES = ["SKILL.md", "runbook.md", "baserates.md", "cases.md"]


def sections(text):
    """{section id: body} for '## X. Title' / '## X Title' headers."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^## ([A-Z0-9]+)[.\s]", line)
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = m.group(1), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def main(root):
    errors, warns = [], []
    T = {}
    for f in FILES:
        p = os.path.join(root, f)
        if not os.path.exists(p):
            errors.append(f"{f}: missing — the package is four files, uploaded together")
            continue
        T[f] = open(p, encoding="utf-8").read()
    S = {f: sections(t) for f, t in T.items()}

    # 1. one package version across all four headers
    ver = {}
    for f, t in T.items():
        m = re.search(r"Package (\d+(?:\.\d+)*)", t[:1500])
        ver[f] = m.group(1) if m else None
        if not m:
            errors.append(f"{f}: no 'Package N.N' in the header")
    vs = {v for v in ver.values() if v}
    if len(vs) > 1:
        errors.append(f"package versions disagree across headers: {ver}")
    if "SKILL.md" in T:
        r = re.search(r"\*Rev (\d+(?:\.\d+)*)", T["SKILL.md"][:1500])
        if r and vs and r.group(1) not in vs:
            errors.append(f"SKILL.md Rev {r.group(1)} ≠ package {sorted(vs)}")
        d = re.search(r'^description:\s*"?(.*?)"?\s*$', T["SKILL.md"], re.M)
        if d and len(d.group(1)) > 1024:
            warns.append(f"frontmatter description is {len(d.group(1))} chars; review length and platform-specific requirements")

    # 2. file § section citations resolve
    cite = re.compile(r"`(SKILL|runbook|baserates|cases)\.md`\s*§\s?([A-Z0-9]+)")
    for f, t in T.items():
        for m in cite.finditer(t):
            tgt, sec = m.group(1) + ".md", m.group(2)
            if tgt in S and sec not in S[tgt]:
                ln = t[:m.start()].count("\n") + 1
                errors.append(f"{f}:{ln}: cites `{tgt}` §{sec}, which has no '## {sec}' header")

    # 3. requirement numbers cited under the section that defines them (runbook §F)
    fdef = set()
    if "runbook.md" in S and "F" in S["runbook.md"]:
        fdef = {int(n) for n in re.findall(r"\((\d{1,3})\)", S["runbook.md"]["F"])}
    req = re.compile(r"`runbook\.md`\s*§\s?([A-Z])[,\s]*(?:requirement\s*\(?|\()(\d{1,3})\)?")
    for f, t in T.items():
        for m in req.finditer(t):
            sec, n = m.group(1), int(m.group(2))
            if n in fdef and sec != "F":
                ln = t[:m.start()].count("\n") + 1
                errors.append(f"{f}:{ln}: requirement {n} cited as `runbook.md` §{sec}; it is defined in §F")
            elif n not in fdef:
                ln = t[:m.start()].count("\n") + 1
                errors.append(f"{f}:{ln}: requirement {n} cited but not defined in runbook §F")

    # 4. rule IDs cited anywhere are defined (bold) in SKILL.md
    defined = set(re.findall(r"\*\*([A-Z]-\d{2})\b", T.get("SKILL.md", "")))
    cited = defaultdict(set)
    for f, t in T.items():
        for i in re.findall(r"\b([AEMRS]-\d{2})\b", t):
            cited[i].add(f)
    for i in sorted(cited):
        if i not in defined:
            errors.append(f"rule {i} cited in {sorted(cited[i])} but not defined as **{i}** in SKILL.md")

    # 5. queue IDs cited anywhere exist in baserates §5
    q = S.get("baserates.md", {}).get("5", "")
    qdef = set(re.findall(r"\*\*(O\d{1,2})\b", q))
    for f, t in T.items():
        for i in sorted(set(re.findall(r"\b(O\d{1,2})\b", t))):
            if qdef and i not in qdef:
                errors.append(f"{f}: queue item {i} cited but not in baserates §5")

    # 6. single source: the same distinctive figure in more than one file
    fig = re.compile(r"(?:[−\-+]?\$[\d,]+(?:\.\d+)?|\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|\b\d+\.\d{2,}%)")
    where = defaultdict(set)
    for f, t in T.items():
        for x in fig.findall(t):
            where[x.replace("−", "-")].add(f)
    dup = sorted(((x, fs) for x, fs in where.items() if len(fs) > 1), key=lambda z: (-len(z[1]), z[0]))
    if dup:
        warns.append(f"{len(dup)} figures appear in more than one file (single-source check; some are legitimate "
                     "citations of the source row): " + "; ".join(f"{x} in {sorted(fs)}" for x, fs in dup[:15]))

    print(f"skillcheck — package {sorted(vs) or '?'} in {root}")
    for e in errors:
        print("ERROR ", e)
    for w in warns:
        print("WARN  ", w)
    print(f"{len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
