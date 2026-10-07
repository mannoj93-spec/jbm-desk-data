"""Extract fenced code blocks from the appendix into source/original/ (content between fences + final newline)."""
import re, sys, os
src, outdir = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
blocks = re.findall(r"^## ([^\n]+)\n\n```[a-z]*\n(.*?)\n```$", text, flags=re.S | re.M)
names = {"SPEC.md (verbatim; its \"~00:50Z\" header is wrong — the file time is 00:42:10Z)": "SPEC.md",
         "fetch.py": "fetch.py", "run.py": "run.py", "run2.py": "run2.py", "run3.py": "run3.py",
         "run4.py": "run4.py", "manifest.py": "manifest.py",
         "Printed output — run.py, run2.py, run3.py (as saved)": "printed_run123.txt",
         "Printed output — run4.py (post hoc)": "printed_run4.txt"}
seen = []
for head, body in blocks:
    fn = names[head]
    with open(os.path.join(outdir, fn), "w", encoding="utf-8", newline="") as f:
        f.write(body + "\n")
    seen.append(fn)
print(seen, len(seen))
assert sorted(seen) == sorted(names.values())
