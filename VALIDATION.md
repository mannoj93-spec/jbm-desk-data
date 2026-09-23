# Validation record — collection cadence revision 2.6.1

Validated 2026-09-23 with Python 3.11 (container) against live sources; GitHub workflows select
Python 3.12. Runtime uses the standard library only. Rows below the 2.6 block are the record of
earlier revisions and are kept as they were.

| Check (2.6.1) | Result |
|---|---|
| Offline regression tests (`regression/`) | 124 passed; numerical fixtures 25 passed; 3 consecutive full runs, no flakes |
| Stalled Binance, snapshot stage only, fake clock (the review's case) | 2.6: 5 Binance attempts, 0 other requests, 0/17 books in 120 s. 2.6.1: 1 Binance attempt, 27 other requests, 14/17 books (all non-Binance) in 20 s; 7 requests skipped by the open circuit |
| Same stall inside a full run (`main()`) | 14/17 books; history stopped at its stage limit; forward books attempted |
| New and strengthened tests run against 2.6 (`62e51cc`) | 6 fail or error, as intended |
| Watchdog, 0/17 books with history intact | 2.6: exit 0 "healthy". 2.6.1: exit 2 "no open-interest book collected (0/17)"; 1/17 stays exit 0 with warnings |
| Live routine run under 2.6.1, scratch copy (16:49Z) | 17/17 books, no circuit opened; options and HL complete (7 Hyperliquid 429s on the container IP, retried and recorded); 169 s |

| Check (2.6) | Result |
|---|---|
| Numerical fixture checks (`test_fixtures.py`) | 25 passed |
| Offline regression tests (`regression/`) | 119 passed (50 from 2.1, 37 in `test_rev22.py`, 32 in `test_rev26.py`); 5 consecutive full runs, no flakes |
| `test_rev26.py` run against 2.5.1 code and workflows (`bcccf14`) | 26 of 32 fail or error, as intended; the 6 that pass pin behaviour 2.5.1 already had (native resolution, successful push, cadence arithmetic) |
| Simulated sustained outage of every venue, fake clock, 600 s budget | Run ends at 600.0 s, record written with every failure and `deadline_reached`; 14-minute job leaves 3.0 minutes for persistence and the recovery artifact |
| Simulated stall of one venue (Binance), fake clock | History stops at its 240 s stage limit; snapshot and forward books still run (2.5: history took all 600 s, snapshot skipped) |
| Hung remote, `PERSIST_BUDGET_S=8` | `commit_push.sh` exits 1 in under 20 s with "remote persistence not confirmed" (unbounded: four 30 s pushes plus rebases) |
| Live routine run under 2.6, scratch copy (15:58Z) | 17/17 books; options complete, 847 strikes; HL complete 200/200 in 82 s; 281 requests, 0 rate-limited; 154 s; stages: series 39 s, liquidations 17 s (daily probe), snapshot 15 s, forward 82 s |
| Report and watchdog on the live copy | Hourly period judged against hourly slots (16/16, upper bound); local run excluded from scheduled figures; watchdog healthy, warns that the newest run was local |
| `SHA256SUMS` | Covers code, docs, workflows, `cadence.json` and templates; data, state and reports change every run |
| Deployment (GitHub, 2026-09-23) | Workflows `90fce23` (16:06:13Z, the start of the 15-minute period in `cadence.json`), persistence script `2d12847`, test update `9327896`, code and docs `e3ff93a`, new tests `d98b842`. Tree verified byte-for-byte against `SHA256SUMS` after fetch. Regression and numerical fixtures runs #15–#19 all green, one per push |
| Manual collection on GitHub (run 35887308099, 16:14Z, manual deployment check) | `collector-2.6`, `trigger: workflow_dispatch`; 17/17 books; options and HL complete; 285 requests, 0 rate-limited; 104 s (series 36, liquidations 13 with the daily probe, snapshot 11, forward 44); committed as `8afc250` |
| Manual watchdog on GitHub (run 35887689676, 16:17Z) | Exit 0 "collector healthy" on the last pre-2.6 scheduled run (15:22Z); warning that the newest run was manual and not counted as scheduled; sparse checkout worked |
| Weekly report on GitHub (run 35887705789, 16:17Z) | Report 2.3 committed as `622a65f`: hourly period 16/16 slots (upper bound, trigger unrecorded), 15/15 intervals covered; 15-minute period listed with no slot yet due |
| First scheduled 15-minute run (run 35888255376, 16:22 slot) | Process start 16:22:51Z; `trigger: schedule`, cron recorded; 17/17 books; options and HL complete; no probe (already done that UTC day); 110 s; committed as `feee7c8`. The 16:07 slot, one minute after the workflow commit, did not run |

| Check (2.5.1 and earlier) | Result |
|---|---|
| Numerical fixture checks (`test_fixtures.py`) | 25 passed |
| `SHA256SUMS` | Now covers code, docs, workflows and templates only; data, state and reports change every hour |
| Offline regression tests (`regression/`) | 87 passed (50 from 2.1, 37 in `test_rev22.py`); 5 consecutive full runs, no flakes |
| 2.5.1 late-byte tests run against 2.5 (`9090fba`) | 503 case fails (2.30 s), as intended; 200 case passes on both |
| Live run under 2.5.1, scratch copy | 17/17 books; options and HL complete; no errors; 159 s |
| 2.5 slow-response tests run against 2.4 (`f6fa022`) | 3 trickle tests fail, as intended; prompt response passes on both |
| Local trickling server, 1.2 s budget | Body and headers: 1.20 s, rejected (2.4: 3.45 s and 3.57 s, accepted) |
| Live run under 2.5, scratch copy | 17/17 books; options complete; HL complete 200/200 in 97 s; no errors; 155 s |
| 2.4 outage tests run against 2.3 (`22d2c65`) | 6 of 6 fail or error, as intended |
| Simulated outage, fake clock, 2.4 | Hyperliquid only: 27 requests, 5.0 min. Every venue: 38 requests, 20.0 min, run record written (2.3: 400 requests / 190 min and 576 / 285 min) |
| Live run under 2.4, scratch copy | 17/17 books; options complete 850/850; HL degraded 3/200 on HTTP 429, then complete 200/200 in 93 s with the backoff |
| 2.3 tests run against `ed45dd2` | 9 of 23 in `test_rev22.py` fail or error, as intended |
| The 13 collector, scoring and schema tests run against the 2.1 code | 11 fail or error, as intended; the 2 that pass pin behaviour 2.1 already had |
| Live hourly run, updated collector, scratch copy of the repo | 17/17 books, 849 option strikes with OI, 29 HL BTC positions in top 200, no errors, 147 s |
| Live taker backfill with the pagination fix | 5m: 17 missing rows recovered, 0 gaps; 1h: 1 recovered, 0 gaps |
| Report generation on the live copy | Passed; retired books labelled, not alerted |
| Watchdog against the deployed repository data | "collector healthy" |
| Live hourly run under 2.3, scratch copy (00:45Z) | 17/17 books; options complete, 850/850 rows valid; HL complete, 200/200 accounts, 29 BTC positions; 160 s |
| End-to-end forecast, scratch copy | Registered before start, frozen, scored on 180 live 1m bars, evidence hash verified, idempotent; all seven event types formatted |
| First GitHub backfill under 2.2 (00:01Z, 434 s) | Taker 5m and 1h: 0 gaps in the repository. Found the 4xx-boundary regression fixed in 2.2.1 |

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

At the time of writing one scheduled 15-minute run has been observed; sustained scheduled
execution at this cadence (delays, dropped slots, queueing behind intake and report) is measured
by the weekly report from here on, not established by this record. Backlog pruning under an outage
and the watchdog's stale and failing states are verified offline only. Live endpoint behaviour is
dated and can change. This is a reliability revision, not a claim of forecasting skill.

## Reproduce

```sh
python test_fixtures.py
python -m unittest discover -s regression -v
python collector.py          # live; writes into this checkout
python report.py --days 7
```
