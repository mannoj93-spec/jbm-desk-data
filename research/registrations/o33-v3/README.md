# O33 v3 — public freeze record

O33 tests whether the desk's registered in-thread calls beat a matched naive baseline (crypto-desk package
`queue.md` O33). v3, opened by the operator on Oct 7 2026, gives every containment call its own matched baseline:
each bound in issue-time σ multiples, the exact minutes from the last closed 1m bar at issue to the graded close,
and windows from the trailing 730 days of Binance USD-M 1m closes ending at the issue (`desk_calls.matched_baseline_v3`).
A declared secondary - time of day, weekend class and scheduled-release matching - is reported beside it and never
replaces it. The paired statistic and claim thresholds are unchanged (weekly blocks, seed 33, >= 60 units in >= 20
weeks with a 95 % interval excluding zero).

`registration.json` holds the full specification, its sha256 (also pinned in `test_desk_calls.py`), the module and
test bytes' sha256 and the freeze rule. **The freeze time is this record's first push to `main`.** Only calls whose
registry receipt is later count; earlier calls are never v3 evidence. Any change is v4.

Practical notes: the archive publishes a day's 1m file the next day, so a call's baseline is computed at scoring
time from data up to its issue minute; retrieval errors reduce usable windows and are never filled. The release
calendar covers CPI, NFP, PPI and FOMC only.

Verify: `python -m unittest test_desk_calls` in this folder with the package's `jbm_archive.py` and
`jbm_measure.py` on the path, and `sha256sum desk_calls.py test_desk_calls.py` against `registration.json`.
