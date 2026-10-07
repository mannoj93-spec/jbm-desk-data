# Requirements

- Python: run with CPython 3.13.16. Uses `X | None` annotations in jbm_archive (fine on older 3.x because
  of `from __future__ import annotations`); 3.11+ recommended (fromisoformat with "+00:00").
  The original thread's Python version was not recorded.
- Dependencies: Python standard library only (json, math, bisect, random, datetime, collections,
  statistics, hashlib, urllib, zipfile, csv, io, concurrent.futures). No third-party packages.
- Package modules: /root/in29/crypto-desk (crypto-desk 12.4.11): jbm_archive.py
  (archive-12.0.0, sha256 35966ae6…0428), jbm_measure.py (measure-11.1.0, sha256 22197d79…af4e).
- Network for fetch.py only: data.binance.vision (klines, metrics archives) and www.binance.com
  (fapi/v1/fundingRate). run.py–run4.py are offline.
- Run from a data directory containing k4h.json, metrics.json, funding.json:
  `python3 -B -E -s /root/research/lean-rules-2026-10-05/reproduce/<script>.py`.
- Helper scripts written for this reproduction (not thread code): tools/extract.py (appendix code
  blocks → source/original/), tools/funding_truncate.py (funding truncation test).
