# Lean-rule backtest, 2026-10-05 - retained bundle (retrospective exploration)

Class: retrospective exploration (E-01 "exploratory"), not a registered prospective test. The spec
(`source/original/SPEC.md`) was written in the thread before results; that ordering is the thread's own statement and is
not independently timestamped.

## What is here

| Path | Content |
|---|---|
| `source/backtest-lean-rules-2026-10-05.md`, `...-appendix.md` | the project note and appendix as read from the Claude project (transcribed; the project exposes no content hash) |
| `source/original/` | spec, fetch/run scripts and printed outputs extracted from the appendix (`tools/extract.py`) |
| `reproduce/` | the same scripts with only the `sys.path` line changed (`CHANGES.md`); outputs, diffs, run times, `REPRODUCTION.md` |
| `reproduce/data/*.json.gz` | the inputs the reproduction read (gzip -9n; uncompressed sha256 in `MANIFEST.json`) |
| `reproduce/funding_truncation/` | the untruncated funding fetch and the truncation test result |
| `reproduce/sensitivity_untruncated_funding/` | outputs with the 7,416-row funding file |
| `MANIFEST.json` | module, input and per-file sha256; bootstrap seeds (run.py 7, run4.py 11) |
| `replay.py` | offline replay (below) |

Costs, exclusions and parameters are those in the spec and scripts: 10 bp round trip, N = 24, T = 0.353% of price,
24 h horizon, weekly block bootstrap (B = 2000), OI ok-days only (7 incomplete metric days excluded), Binance OI as a
labelled stand-in for cross-venue OI.

## Status

Reproduced on 2026-10-07 (19:25-19:29Z) from re-fetched inputs whose sha256 equal the appendix's: F11, F12, P3, U5, U6,
U7, the primary table, the secondary grid and the Wilson 21/27 line reproduce exactly; one run3 diagnostic line differs
at machine precision (3.98e-16 vs 3.34e-16). This shows the appendix code, run on those bytes, prints the appendix
outputs. It is not an independent re-derivation of the method, and it does not validate the method.

Limitations kept (detail in `reproduce/REPRODUCTION.md`):

- The original input files were not archived. A hash match shows equality with the bytes hashed after the original runs;
  the later archive re-fetch manifest (`data_manifest.json`, 01:09Z) records file sets, not the bytes the runs read.
- Funding has only a derived-file hash (API, no provider checksum). It matches only after dropping the five settlements
  published after the original fetch (first 7,411 rows, through 2026-10-06T00:00Z); a cut at 2026-10-04T23:59:59Z does
  not match.
- The scripts are unversioned thread code (runbook requirement 131), reproduced as published, not reviewed.
- "A literal 300 points binds on 39% and 56% of bars" is not printed by any script and was not reproduced.
- Original Python version unknown; the reproduction used CPython 3.13.16, standard library only.

Correction to the note (2026-10-07): its sentence calling the thread's 21/27 containment record "indistinguishable from
the naive rate" overstated a non-result. The record reads: no demonstrated outperformance; the calls are unregistered
and a properly matched comparison is not yet available. The original note is kept unchanged under `source/`.

## Replay

```
python research/retrospective/lean-rules-2026-10-05/replay.py            # uses this repository's desk/ modules
python research/retrospective/lean-rules-2026-10-05/replay.py --pkg <crypto-desk package dir>
```

Verifies module and input hashes, runs run.py-run4.py offline on the retained inputs and compares every output line;
prints `REPLAY MATCH` and exits 0, or shows the diff and exits 1. Re-fetching (`reproduce/fetch.py`) needs network
access to data.binance.vision and www.binance.com and will return newer funding rows.
