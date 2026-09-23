# Reliability revision 2.5 — 2026-09-23

From the review of 2.4: the deadline capped the socket timeout, but a socket timeout limits each
blocking operation, not the request. Reproduced on a local server with a 1.2-second budget:

| Server behaviour | 2.4 | 2.5 |
|---|---|---|
| Body sent one byte every 70 ms | 3.45 s, response accepted | 1.20 s, rejected: deadline |
| Headers sent one byte every 50 ms | 3.57 s, response accepted | 1.20 s, rejected: deadline |
| DNS lookup stalled 3 s (no socket exists yet) | not bounded | 1.2 s, rejected: deadline |

- **Whole-request limit.** `fetch()` runs each request in a daemon worker thread and waits for it
  only until the deadline, covering DNS, connection, TLS, headers, body, and HTTP error bodies.
  On expiry it shuts the socket down to release the worker, discards any late result, and the
  request counts as failed. Bodies are read in `read1` chunks with a deadline check between them,
  so the worker also stops itself.
- **Monotonic deadlines.** The run and Hyperliquid deadlines use `time.monotonic()`; a wall-clock
  step can no longer lengthen or shorten them. Stored timestamps stay on wall-clock UTC.
- **README** now states what the limit covers and what it does not (local writes after the
  deadline; the workflow's commit and push; an abandoned thread's lifetime).
- Tests: `SlowResponseTests` uses real sockets on 127.0.0.1 — trickled body, trickled headers,
  trickled 503 body, stalled DNS, and a prompt response that must still succeed. The three trickle
  tests fail on 2.4. The fake-clock helper now patches the clock only inside `with`, after a
  failing test in development left it installed for the tests that followed.

# Reliability revision 2.4 — 2026-09-23

From the review of 2.3: the Hyperliquid map had no time limit. Measured on a simulated clock where
every request hangs for its full timeout:

| Simulated outage | 2.3 | 2.4 |
|---|---|---|
| Hyperliquid only | 400 requests, 190 min | 27 requests, 5.0 min, stopped at its budget |
| Every venue, whole hourly run | 576 requests, 285 min | 38 requests, 20.0 min, run record written |

The workflow kills the job at 30 minutes and persists only after the collector exits, so 2.3 could
lose the whole hour's data in a long outage.

- **Run-wide budget.** `get()` starts no request after the run deadline (20 minutes, or
  `COLLECTOR_BUDGET_S`) and caps each socket timeout and retry pause by the time remaining; every
  later stage fails fast and the run record is still written, leaving about 10 minutes for the
  commit and push.
- **Hyperliquid budget.** The map has 300 seconds (a normal map takes 70–120 s), 10-second request
  timeouts, and stops as soon as failures reach half the accounts, when the map could no longer be
  stored. Accounts not reached are listed as `not attempted: deadline` or `not attempted: rejection
  inevitable`; each snapshot records `stopped`, `elapsed_s` and `rate_limited`.
- **Rate limits.** A live run hit HTTP 429 on 3 of 200 accounts (the audit container's IP, after
  repeated runs). A 429 now gets one retry after a 5-second backoff inside the budget; the next
  live map was complete (200/200, 93 s).
- Tests: 7 in `OutageBudgetTests`; the 6 that predate the 429 change all fail on 2.3.

# Reliability revision 2.3 — 2026-09-23

From the external review of `ed45dd2`. Each item has a regression test that fails on `ed45dd2`
(9 of 23 tests in `test_rev22.py` fail or error there; all 73 tests pass here).

- **Range median error, named for its scale.** The review read `abs_log_error` (|ln q50 − ln
  realized|) as a mistake for |q50 − realized|. Both are legitimate on different scales: runbook
  E2 fits its baselines on ln lr ("B1 HAR-range — OLS on logs") and names "mean absolute error of
  ln range" as the primary loss, which is the log-scale figure; the lr-scale figure is what a
  reader of q50 in ln(H/L) units expects. The old field name let either reading pass. Now:
  `abs_error_lr` (|q50 − realized|), `abs_error_log_lr` (E2 primary), and `qlike` (E2 secondary).
  No range forecast had been scored. `scoring-2.2`.
- **Report formatting.** Scored events print per type: range events show realized ln(H/L),
  q10–q90 coverage, pinball losses, both median errors and QLIKE (2.2 printed `None`); interval
  events show the interval score. `report-2.2`.
- **Forward-book validation.** A Hyperliquid response without `marginSummary.accountValue` and an
  `assetPositions` list is a failed account (`{}` was stored as an account with no positions);
  a malformed BTC position fails its account; any failure marks the snapshot `degraded`, names
  the addresses, and reports an error; half or more failing (100 of 200 had passed with
  `err: null`) stores nothing. A Deribit option with OI but no positive mark IV or underlying, or a
  malformed name, is excluded and named, and the snapshot is `degraded`; over 5% invalid stores
  nothing. `collector-2.3`. The live run under 2.3 was complete: 850 of 850 option rows and 200 of
  200 accounts valid.
- **End-to-end scoring exercised** on live prices in a scratch copy: a synthetic forecast with all
  seven event types was registered before its start, frozen, scored on 180 Binance 1m bars,
  evidence hash-verified, and not rescored on a second pass. Not committed to the public registry.

# Reliability revision 2.2.1 — 2026-09-23

- The first GitHub backfill under 2.2 failed `binance_openInterestHist_5m` with
  `HTTP 400 (binance code -1130: parameter 'endTime' is invalid.)`: 2.2 began appending the venue's
  reason to 4xx errors, and the measured old-history boundary was matched as exactly `"HTTP 400"`.
  It now matches the prefix. Hourly runs were unaffected (they stop at the checkpoint first); no
  stored row was lost. Test: `test_backfill_boundary_400_with_reason_still_ends_history`.
- The same backfill closed every taker gap: 5m and 1h taker history now have 0 missing intervals.

# Reliability revision 2.2 — 2026-09-23

Audit of the deployed 2.1 repository against the live sources. Every defect below was measured,
reproduced by a regression test that fails on 2.1 (`regression/test_rev22.py`), and fixed.

## Data loss

- **Taker history lost one row per 500-row page.** Binance's taker endpoint filters `endTime` on
  the interval close; the ratio and OI endpoints filter on the stamp. Paging with
  `endTime = oldest − 1` skipped `oldest − step` on every taker page: 17 missing 5m intervals and
  1 missing 1h interval in the stored history, each exactly 500 rows apart. Paging is now
  endpoint-aware. A live backfill with the fix recovered all 18 rows; the oldest ages out of
  Binance's ~30-day window around 2026-09-23 04:50Z, so run one manual backfill after deploying.
- **Liquidation pages could drop the second order of a same-millisecond pair.** OKX `after`
  returns records strictly earlier than the given ts; ~2% of stored timestamps (50 of 2,493)
  carry two orders. Pages now re-request the boundary millisecond and deduplicate by key.
- **One unexpected response aborted the rest of the history run.** An exception inside any series
  block (for example a missing `fundingRate` key) skipped every later series that hour. Each
  series is now isolated; its error is recorded and the others proceed.

## Meaning of timestamps

- **Snapshot series were scored one interval late.** Measured: the Binance 1h ratio and OI rows
  equal the 5m rows at the same stamp, and the OKX account-ratio row stamped T is published before
  T+1h — they are values *as of* the stamp. 2.1 read every series at stamp + step, so a predicate
  "top notional under 68% at 06Z" (the template's own example) was scored on the 05:00 value.
  `schema.SERIES_KIND` now classifies each series; predicates read snapshots at their stamp and
  intervals at their close; research views admit snapshots at stamp + 5 minutes (M-01) instead of
  stamp + 1 hour. Scoring version `scoring-2.1`. No forecast had been registered under 2.1.
- The hourly snapshot series are now collected once published (stamp + 5m) rather than an hour later.

## Forward-only books (desk requirement 50)

- Deribit per-strike BTC option open interest with mark IV, hourly, daily files.
- Hyperliquid position map: BTC positions of the top 200 accounts by account value, with
  liquidation price and leverage type; ranking cached six hours.
- Both are isolated from the critical path; failures are reported per run and in the weekly report.

## Sources

- Retired `bitget_COIN` (Bitget 40309 "The symbol has been removed") and `bitmex` (XBTUSD and
  XBTUSDT settled 2026-09-16; no XBT perpetual open). The report lists them as retired, not failing.
- 4xx responses now keep the venue's own error code and message.

## Scoring and monitoring

- `range` event type: q10/q50/q90 of ln(high/low) over the window — the desk's E2 target — scored
  by coverage, pinball loss, and absolute log error of the median.
- `interval` events carry the interval (Winkler) score.
- `watchdog.py` and the Collector watchdog workflow: fail when the last hourly run is over 3 hours old.
- The report adds a forward-books section and per-run forward-book alerts.

## Not changed, and open

- The repository and the crypto-desk skill (package 10.1, `baserates.md` §4) each describe a
  forecast registry: this repository's issue intake and the skill's registry artifact. One must be
  chosen as the place forecasts are registered and scored; this revision changes neither.
- Action versions (`checkout@v4`, `setup-python@v5`, `upload-artifact@v4`) are unchanged; no run
  annotation was available to show a deprecation.
- Bybit is unreachable from US runners (CloudFront 403); its funding stays via Hyperliquid's aggregator.

# Reliability revision 2.1 — 2026-09-22

## Correctness and recovery

- Complete aligned price coverage is required before scoring; missing history cannot
  count as a forecast loss or false predicate. Failed observations remain retryable.
- Price API responses, JSON numbers, nested event schemas, default start times,
  predicate cadence, and UTC alignment are validated.
- Terminal comparisons are strict; flat leans are separate; race ties include Brier bounds.
- Interval predicates use closing timestamps and require complete observation coverage.
- Failed backward pages, stalled cursors, and page caps preserve prior checkpoints.
- DVOL fetches use checked daily grids and deduplicate inclusive response boundaries.
- Per-file atomic persistence and row identity checks make retries safe without
  rewriting legacy observations. Corrupt state and JSON lines fail visibly.

## Audit trail

- Forecasts are frozen by full SHA-256 and indexed by a persistent manifest.
- Scores retain forecast/evidence hashes and normalized observations for reproduction.
- Deleting or editing a registry source cannot selectively remove its frozen forecast.
- New observations include code version, commit, and completed-fetch availability time.
- Research fingerprints include local root Python dependencies. Mature results are
  labeled post-registration; point-in-time helpers exclude unstamped legacy observations.

## Operations

- Shared workflows use explicit queueing and the current default branch checkout.
- Push retry exhaustion fails explicitly; forecast acknowledgement follows successful push.
- Intake supports edited/reopened issues and reconciles unprocessed open issues hourly.
- Recovery artifacts retain unpushed data on workflow failures for seven days.
- Reports disclose all recorded collection errors, source failures, gaps, duplicates,
  stale histories, missing deployment evidence, and test failures.
- Coverage uses distinct scheduled slots rather than counting extra manual runs as uptime.
- Software regressions now run on code/workflow pushes and pull requests.

## Compatibility and limits

- Preserve newer live data/state when installing this archive; its captured history is
  unchanged from the supplied ZIP. Legacy report copies are under reports/legacy/.
- Three duplicate DVOL records remain in legacy history and are explicitly reported.
- Predicates now refer to interval close times; review any old, unfrozen designs.
- Invalid legacy forecasts must be corrected under a new ID; old scores need explicit
  review and are not overwritten. No forecasts or research designs were registered in
  the supplied snapshot.
- Research episodes now require input_cutoff and outcome_at; the template documents this.
- A hash registry is not tamper-proof against repository writers. Free text in public
  issues is not privacy-filtered. Live API/GitHub execution has not been verified here.
- No autonomous trading, path model, CRPS, bootstrap uncertainty, or skill installation
  has been added. The original numerical formulas remain substantively unchanged.
