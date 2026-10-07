# Changes from source/original/ to reproduce/

Only `sys.path` lines were changed, to point at the versioned package 12.4.11 modules in
`/root/in29/crypto-desk` (jbm_archive.py archive-12.0.0, jbm_measure.py measure-11.1.0). No other
byte of any script was changed. Verify with `diff source/original/<f> reproduce/<f>`.

| file | line | original | reproduce |
|---|---|---|---|
| fetch.py | 2 | `sys.path.insert(0,'/mnt/skills/plugins/crypto-desk')` | `sys.path.insert(0,'/root/in29/crypto-desk')` |
| run3.py | 1 | `import sys; sys.path.insert(0,'/home/claude/pkg/crypto-desk')` | `import sys; sys.path.insert(0,'/root/in29/crypto-desk')` |
| run4.py | 3 | `import sys; sys.path.insert(0,'/home/claude/pkg/crypto-desk')` | `import sys; sys.path.insert(0,'/root/in29/crypto-desk')` |
| manifest.py | 2 | `sys.path.insert(0,'/home/claude/pkg/crypto-desk')` | `sys.path.insert(0,'/root/in29/crypto-desk')` |

run.py and run2.py: unchanged (no sys.path line).

Not a script change, but part of the run setup: `reproduce/data/funding.json` is the fetched file
truncated to its first 7,411 settlements (see REPRODUCTION.md, "Inputs"). The untruncated fetch is
kept at `reproduce/funding_truncation/funding.fetched_raw.json`.

Invocation (from inside `reproduce/data/`): `python3 -B -E -s /root/research/lean-rules-2026-10-05/reproduce/<script>.py`.
`-I` was not used because run2–run4 do `import run`, which needs the script directory on
`sys.path` (`-I` removes it); `-B -E -s` keeps bytecode out of the package folder and ignores
environment/user site paths. The data dir holds only the three JSON inputs (no .py files).
