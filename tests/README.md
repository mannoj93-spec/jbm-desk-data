# Prospective research tests

This directory is for frozen research designs, not the software regression suite.
Copy `_template.py` to a new ID and supply a complete design. The collector registers
a fingerprint of that file plus root Python modules.

Results append to `results.jsonl`. They are labeled post-registration or in-sample;
no code path labels arbitrary custom Python as proven free of future-data leakage.
Outcome maturity, declared input cutoff, and duplicate group/decision checks are mandatory.
Use `ctx.as_of(t_decision)` for signal inputs. Availability stamps are required; legacy
rows are not silently granted historical availability. Review custom data access and
statistical independence separately.
