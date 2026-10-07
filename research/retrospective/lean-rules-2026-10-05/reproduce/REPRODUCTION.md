# Reproduction record — lean-rule backtest (Oct 5–6 2026)

Retrospective reproduction of `claude/backtest-lean-rules-2026-10-05.md` using the code and printed
outputs in `claude/backtest-lean-rules-2026-10-05-appendix.md`. This checks that the appendix code,
run on re-fetched inputs whose hashes match the appendix, prints the appendix outputs. It is not an
independent re-derivation of the method and does not validate the method itself.

## Environment
- Run date (UTC): fetch 2026-10-07T19:25:38Z → 19:27:46Z; run.py–run4.py 19:28:29Z → 19:29:17Z
  (`fetch_started_utc.txt`, `run_times_utc.txt`).
- Python 3.13.16 (main, Oct 1 2026) [GCC 13.3.0], Linux x86_64, glibc 2.39. Stdlib only.
- Package: crypto-desk 12.4.11 (SKILL.md header), release family 12.4, release.json repo 2.27,
  folder `/root/in29/crypto-desk`. Modules (sha256 equal to release.json):
  - `jbm_archive.py` archive-12.0.0 `35966ae62f21ad4ceee3020dd3792c19c20b803afa37e8dd5dd4dd359a8b0428`
  - `jbm_measure.py` measure-11.1.0 `22197d79bfa1e6ecc257547e25f5154e90713c34d1dfcc595981ad280996af4e`
  - The original fetch imported from a 12.4.10 mount; the 12.4.11 changelog states modules were
    unchanged 12.4.10 → 12.4.11. The k4h rows embed `code_version` "archive-12.0.0", and the k4h hash
    matched (below), consistent with that.
- Package folder verified unchanged after all runs (per-file sha256 listing before/after identical;
  no `__pycache__` written).

## Inputs (sha256 vs appendix)
| file | reproduced sha256 | appendix | result |
|---|---|---|---|
| k4h.json (14,814 bars) | 1e7d2245…391e615 | 1e7d2245…391e615 | MATCH as fetched, no truncation |
| metrics.json (734 days: 727 ok, 7 incomplete; 211,387 rows) | cefa919b…e66ebb | cefa919b…e66ebb | MATCH as fetched |
| funding.json as fetched (7,416 settlements, last 2026-10-07T16:00Z) | f43e9dc1…cf1cf1 | 7382cc20…ec738f | MISMATCH (newer settlements appended) |
| funding.json truncated to first 7,411 (last 2026-10-06T00:00:00.003Z) | 7382cc20…ec738f | 7382cc20…ec738f | MATCH |
| funding.json truncated to fundingTime ≤ 2026-10-06T00:41:43Z (original fetch time) | 7382cc20…ec738f | same | MATCH (same 7,411 rows) |
| funding.json truncated to fundingTime ≤ 2026-10-04T23:59:59Z (7,407 rows) | 8b9ba5bb…eccc68 | 7382cc20… | MISMATCH |

Funding method: the fetched list was re-dumped with the same `json.dump(fr, open(path,'w'))` call
(a re-dump of the full list reproduced the fetched file's bytes exactly); rows were not altered,
only trailing settlements dropped. The five dropped settlements are 2026-10-06T08:00Z through
2026-10-07T16:00Z (`funding_truncation/result.txt`). The original funding file therefore ran through
the Oct 6 00:00Z settlement, not Oct 4 — consistent with its 00:41:43Z Oct 6 fetch time. The runs
used the 7,411-row file (`reproduce/data/funding.json`). k4h needed no truncation (the fetch is
bounded to 2026-10-04 and returned exactly 14,814 bars).

## Outputs (diff vs appendix printed blocks; only trailing whitespace normalized)
| script | lines | result |
|---|---|---|
| run.py | 9/9 | byte-identical |
| run2.py | 71/71 | byte-identical |
| run3.py | 15/15 | 14 identical; 1 differs (below) |
| run4.py | 50/50 | byte-identical |

The only differing line (run3.py line 1, a diagnostic):
```
< max rel diff hand sigma vs jm.sd_c2c (sampled): 3.9755014737176005e-16
> max rel diff hand sigma vs jm.sd_c2c (sampled): 3.3383960067337674e-16
```
Both are at machine precision; the check it reports (hand sigma equals `jm.sd_c2c`) holds either
way. The cause is not established; a different Python version in the original thread (float
summation / `statistics.stdev` internals) is a plausible explanation. The original Python version
was not recorded. Diffs: `reproduce/diffs/*.diff`.

Sensitivity (not the reproduction): with the untruncated 7,416-row funding file, the only output
change was run.py's header `funding 7411` → `funding 7416`; all other lines of run–run4 were
identical, including U7 (its window ends Oct 4) (`sensitivity_untruncated_funding/`).

## Reported figures
| figure | source | result |
|---|---|---|
| Primary table (V0–V3, full and 24M) | run.py | reproduces exactly |
| Pre-specified secondary grid; Q1; "What S-04 removed" | run2.py | reproduces exactly |
| F11 | run4 P1 block | reproduces exactly |
| F12 | run4 P2 block | reproduces exactly |
| P3 (V0 vs V1 at 1σ/2σ) | run4 P3 block | reproduces exactly |
| U5 (naive containment percent bands) | run3 naive containment | reproduces exactly |
| U6 (Parkinson 6-bar incl. issue bar) | run4 U6 block | reproduces exactly |
| U7 (funding distribution) | run4 U7 block | reproduces exactly |
| Wilson 21/27 [59.2, 89.4] | run4 last line | reproduces exactly |
| run3 park6 threshold rows and shares | run3 | reproduces exactly |

Note: the main note's "a literal 300 points binds on 39% and 56% of bars" is not printed by any
script in the appendix, so it was not reproduced. The 59%/55% and 97%/94% binding shares are
arithmetic on reproduced counts (8,588/14,447; 2,425/4,392; 1,052/1,089; 342/363).
`manifest.py` was copied (sys.path changed) but not run; `data_manifest.json` was not reproduced.

## Limitations
- Inputs are re-fetched bytes. Provider files can be rewritten; a hash match shows equality with
  the bytes that were hashed after the original runs, not with an archived copy of the original
  inputs. The original input files are not stored in the project.
- `data_manifest.json` (sha256 23293deb…) came from a later re-fetch (01:09Z) and is not stored
  here; it records file sets and states, not the bytes the runs read.
- Funding has only a derived-file hash (no provider checksum; API, not archive). The match required
  dropping five later settlements; the cut point was chosen to test the original count/fetch time,
  and the Oct 4 23:59:59Z cut does not match.
- The scripts are unversioned thread code (runbook requirement 131), reproduced as published, not
  reviewed for correctness here.
- `source/*.md` were saved by transcribing the Projects tool's `project_read` response; the Projects
  tool exposes no content hash to check against. The extracted code and printed blocks are
  self-consistent (the code reproduces the printed outputs byte-for-byte except the line above),
  which is evidence those parts were transcribed faithfully; the prose sections have no such check.
- Original Python version unknown; this run used 3.13.16.
