# Validation record — reliability revision 2.2

Validated 2026-09-23 with Python 3.11 (container) against live sources; GitHub workflows select
Python 3.12. Runtime uses the standard library only.

| Check | Result |
|---|---|
| Numerical fixture checks (`test_fixtures.py`) | 25 passed |
| `SHA256SUMS` | Now covers code, docs, workflows and templates only; data, state and reports change every hour |
| Offline regression tests (`regression/`) | 64 passed (50 from 2.1, 14 new in `test_rev22.py`) |
| The 13 collector, scoring and schema tests run against the 2.1 code | 11 fail or error, as intended; the 2 that pass pin behaviour 2.1 already had |
| Live hourly run, updated collector, scratch copy of the repo | 17/17 books, 849 option strikes with OI, 29 HL BTC positions in top 200, no errors, 147 s |
| Live taker backfill with the pagination fix | 5m: 17 missing rows recovered, 0 gaps; 1h: 1 recovered, 0 gaps |
| Report generation on the live copy | Passed; retired books labelled, not alerted |
| Watchdog against the deployed repository data | "collector healthy" |

## Measurements behind the changes (live, 2026-09-22 23:30Z)

- Binance `/futures/data`, `endTime = X − 1`: taker returns up to X − 10m; ratio and OI endpoints up
  to X − 5m. The 1h ratio and OI rows equal the 5m rows at the same stamp. Taker 1h `buyVol` at T
  equals the sum of the twelve 5m rows from T (within 0.1%).
- Stored taker gaps: 17 × 5m at 500-row spacing from 2026-08-24 04:50Z; each present at the source.
- OKX liquidation feed: 50 of 2,493 stored timestamps carry two orders; `after = ts + 1` returns the
  boundary pair again, `after = ts` does not.
- OKX account ratio: the row stamped 23:00 was returned at 23:35.
- Bitget BTCUSD coin-margined perpetual: code 40309, "The symbol has been removed".
- BitMEX `/instrument/active`: XBT_USDT Delisted, XBT_USDC Unlisted; no open XBT perpetual.
- Deribit `get_book_summary_by_currency` (BTC options): 972 instruments, 849 with OI; ~30 KB compact.
- Hyperliquid leaderboard: 46,876 rows, 39 MB; `clearinghouseState` ~0.33 s per call.

## Scope limits

The workflow change (watchdog) and the new collector have not yet run on GitHub at the time of
writing; the first Actions run after this commit is the deployment check. Live endpoint behaviour
is dated and can change. This is a reliability revision, not a claim of forecasting skill.

## Reproduce

```sh
python test_fixtures.py
python -m unittest discover -s regression -v
python collector.py          # live; writes into this checkout
python report.py --days 7
```
