# JBM desk data — collection cadence revision 2.6

A small, standard-library Python project that preserves public crypto-market history,
registers forecasts before their start, and produces reviewable research reports.
It does not trade or change a skill package automatically.

Revision 2.2 (2026-09-23) follows the first live deployment and an audit against the live
sources: it fixes two pagination defects that lost rows, corrects the timestamp meaning of
snapshot series, adds the forward-only books the desk's requirement 50 names (Deribit per-strike
option OI and the Hyperliquid position map), adds range and interval scores, retires two dead
books, and adds a watchdog. Revision 2.6 moves the collector from hourly to every 15 minutes
and reworks its time budget, queueing, health figures and watchdog around that cadence.
See [CHANGELOG.md](CHANGELOG.md) and [VALIDATION.md](VALIDATION.md).

**Deployed** on GitHub Actions since 2026-09-22 23:24Z (first run `runner: github`); hourly until
the 15-minute schedule took effect (the time is in `cadence.json`).

## Quick start / upgrade

1. Replace the repository's code, `scripts/`, documentation, and `.github/workflows/` with
   this release. Preserve newer live `data/`, `state/`, `registry/`, and `tests/` contents:
   the bundled data is the original snapshot, not a replacement for subsequently collected history.
2. Run locally with Python 3.12:

   ```sh
   python test_fixtures.py
   python -m unittest discover -s regression -v
   python collector.py --register-only
   python report.py --days 7
   ```

   A real registered forecast whose horizon has elapsed requires exchange access for scoring.
   Numerical fixtures and regression tests require no network or credentials.
3. Review changes, commit, and push. The workflows request the repository permissions they
   need. Repository or organization policy must permit Actions to write contents and issues.
4. Run **Collector** (formerly *Hourly collector*) manually without backfill. Check its source errors, latest timestamps,
   and remote commit. Then run **Weekly report**. Live exchange availability and GitHub execution
   must be verified in your repository; local tests do not establish either.
5. If a retained interval is missing, manually run the collector with **backfill** enabled.
   Backfill revisits the source's retained history and skips already stored identities.
   It cannot recover observations the source has already discarded.

Python's standard library is sufficient. There are no exchange keys or trading credentials.
The GitHub workflows use the repository's scoped `GITHUB_TOKEN` for commits and issues.

## Scheduled work

| Workflow | Trigger | Purpose |
|---|---|---|
| Collector (`collect.yml`, formerly *Hourly collector*) | Every 15 minutes at :07, :22, :37, :52 UTC; manual; manual backfill | Preserve history, snapshots, liquidations, forward books and registration records |
| Forecast intake | Owner's forecast issues opened/edited/reopened; hourly :37 recovery; manual | Validate, freeze, persist, then acknowledge a forecast |
| Weekly report | Monday 00:30 UTC; manual | Coverage, errors, forecast scores, research summaries, review candidates |
| Collector watchdog | Every 30 minutes at :17 and :47 UTC; manual | Fails (so GitHub emails the owner) when the collector is stale or missing, or running but failing |
| Regression and numerical fixtures | Code/workflow pushes and pull requests; manual | Arithmetic fixtures and offline failure-path regression tests |

**Queueing.** Every writing job (collector, backfill, forecast intake, weekly report) holds
`repo-write`, set at job level with `queue: max`: writes are serialized and up to 100 jobs wait
their turn, so intake and report work is not dropped behind collector runs. It is not an
unlimited queue. Scheduled collector runs additionally share a workflow-level group with GitHub's
default queue: one running and at most one pending, a newer pending run replacing the older one.
During an outage or a long backfill, obsolete scheduled runs are therefore cancelled while still
pending instead of piling up; nothing that is running is cancelled, so persistence always
finishes. Manual and backfill runs have their own groups and are never cancelled by the schedule.
The hourly intake recovery pass revisits open forecast issues missed by event delivery or
queueing. A repository owned by an organization needs an explicit authorized-user policy before
phone intake can be used: the default accepts only an individual repository owner's login.

**Time budget of a routine run.** Network work ends 10 minutes into the run
(`COLLECTOR_BUDGET_S=600`), on `time.monotonic()`. Inside it, history series may use 40%,
liquidations 15% and the snapshot 20%; the forward books get the rest, and the Hyperliquid map at
most 5 minutes of it. History and liquidations are checkpointed and recover on the next run;
snapshots cannot be taken later, so one stalled venue can no longer cost every venue its snapshot.
The limit covers each whole request: DNS lookup, connection, headers and body. A request still
unfinished at the deadline is abandoned and counted as failed, never accepted late; unreached
work is recorded as such. The collection step is limited to 11 minutes, persistence (commit and
push, with rebase retries) to 100 seconds by `scripts/commit_push.sh`, and the job to 14 minutes,
inside the 15-minute slot. Time spent waiting for `repo-write` does not count against the job
limit. Backfill keeps a separate 30-minute budget in a 45-minute job. An abandoned request may
keep its background thread until its socket times out or the process exits; its result is
discarded. A normal routine run takes 1.5–2.5 minutes.

**Health.** `cadence.json` lists every schedule the collector has run under. The weekly report
judges each period against its own cadence, so the hourly period is not counted as missing three
runs in four, and it keeps two figures apart:

- *Scheduled execution*: runs the scheduler started (`trigger: schedule` in the run record)
  against the nominal slots that have passed. Manual runs never count. Starts are counted, not
  matched to slots: GitHub starts scheduled jobs late by an unrecorded amount (minutes is common,
  longer under load) and sometimes drops them, so a start time does not say which slot it served.
  Run records before 2.6 do not record their trigger; for that period the report shows an upper
  bound.
- *Snapshot coverage*: slot intervals that hold at least one stored snapshot, whatever started the
  run. This is the data actually held.

It also reports the actual intervals between runs and between snapshots, runtime percentiles,
runs that reached the budget, and rate-limit incidents by host, and it groups failures by source
(count, first and last run, latest message) so a persistent fault stays visible without burying
everything else. History series keep their native 5-minute and hourly resolution: the run cadence
only changes how often the checkpoints are advanced, and row identities are deduplicated.

**Watchdog timing.** The watchdog runs every 30 minutes and reads the stored run records. It
fails with exit 1 when no run that the schedule could have started is younger than
`WATCHDOG_STALE_MIN` minutes (default 90, six slots; set the repository variable
`WATCHDOG_STALE_MIN` or pass it to a manual run). A recent manual run does not reset this, so a dead
schedule is not hidden by a manual check. It fails with exit 2 when runs are arriving but the
latest scheduled run lost critical data (the Binance share series or the snapshot), and passes
with warnings when sources failed, books were degraded or requests were rate limited. Ninety
minutes tolerates ordinary scheduling delays and the odd dropped run; a collector that stops is
reported about 90–120 minutes after its last run, plus any delay in starting the watchdog. The
watchdog runs on the same Actions scheduler, so a platform-wide scheduling outage silences both;
that case still surfaces only at the weekly report or by looking. External uptime monitoring
remains a future addition.

## Forecasts from a phone

Open an issue titled `forecast ...`, with the JSON forecast as its body or in a single
JSON code block. Only the repository owner is accepted. Invalid issues stay open; edit
the body to retry. The bot closes a valid issue only after registration and `git push`
succeed. If acknowledgement fails after a successful push, reconciliation uses the saved
receipt to complete it without changing the original registration time.

Use `registry/_TEMPLATE.json` as a schema example. Set future dates and a new ID before use.
Without `start_utc`, intake uses the next five-minute boundary. Specify an explicit later
start if that leaves too little time for the job to run. All times require explicit UTC
and whole minutes. Forecast horizons are limited to 31 days and 100 events.

**Issues and repository contents are public.** Field validation rejects unexpected keys;
it cannot recognize private account information embedded in allowed prose. Do not include
positions, balances, account IDs, or private desk notes. Information is public as soon as
an issue is submitted, before the bot can validate it.

Directly committed registry files use the same schema and are frozen on the collector's
first sighting. Their registration must precede their start. Run registration locally
only for development; GitHub records label the registering commit.

## Scoring contract

- Empty, gapped, duplicated, malformed, or non-finite price data cannot produce a score.
  Incomplete forecasts remain retryable. One unscorable forecast does not prevent other
  valid forecasts from being scored.
- Price bars cover `[start, horizon)` exactly. Terminal “above” and “below” are strict
  comparisons. A flat lean is reported as `flat`, not a win for either direction.
- Same-minute race ties retain both log-score and Brier bounds. Log probabilities use a
  documented `1e-4` clip; Brier scores use the original probability.
- Predicates read each series by what its stamp means (`schema.SERIES_KIND`, measured live
  2026-09-22). **Snapshot** series — the Binance account/position ratios, Binance OI and the OKX
  account ratio — describe the value *as of* the stamp: `at_utc 06:00Z` reads the row stamped
  06:00. **Interval** series — Binance taker volumes, OKX mark/index candles, DVOL — describe
  `[stamp, stamp + step)` and are read at their close: `at_utc 06:00Z` reads the row stamped
  05:00 for an hourly series. `by_utc` requires every expected observation after start through
  the deadline. (2.1 read every series at its close, so a snapshot predicate was scored one
  interval late — an hour for the `_1h` series; no forecast had been registered.)
- `range` events forecast lr = ln(max high ÷ min low) over `[start, horizon)` as quantiles
  q10/q50/q90 (runbook E2's target). Scores: realized lr; whether it fell inside q10–q90; pinball
  loss per quantile; `abs_error_lr` = |q50 − realized| in lr units; `abs_error_log_lr` =
  |ln q50 − ln realized|, E2's primary loss (its baselines are fitted on ln lr); and QLIKE on
  range², E2's secondary loss. The report prints each by name.
- `interval` events also carry the interval (Winkler) score: width plus 2/α times any miss.
- Only the fixed-cadence series and fields listed in `schema.SERIES` are machine-scored.
  Variable-cadence settled funding is collected but is not a supported predicate input.
- Each completed forecast retains its frozen input SHA-256, scorer version, full normalized
  price bars, predicate observations used, and an evidence hash. Evidence is stored before
  the append-only score record that refers to it.
- Manual predicates stay labeled `manual`; no truth value is inferred.

## Registration and provenance

`state/forecast_manifest.json` indexes exact-byte forecast snapshots in `registry/frozen/`.
Deleting or editing the visible registry file does not remove the frozen forecast from the
scoring queue. Reusing an ID with different bytes is rejected; create a new ID instead.
Scores key on ID plus full forecast hash. Legacy score files are preserved and flagged for
manual migration rather than silently rescored.

New data rows carry `code_version`, `code_commit`, and `observed_at` (the time the completed
fetch is written). Research views admit a row only after both `observed_at` and its knowledge
time: stamp + 5 minutes for snapshot series (the desk's M-01, verified on the Binance archive),
the interval close for interval series. Existing observations retain their original bytes and provenance.
We do not invent availability timestamps for legacy rows. Three legacy DVOL duplicate
rows remain in the supplied snapshot; reports count unique timestamps and disclose them.

These controls provide a reproducible workflow, not a tamper-proof external registry.
Anyone with repository write access can change the code and state. Protect the default
branch and review changes according to your operating policy.

## History recovery and storage

Backward history fetches are staged. A failed page, pagination stall, or page cap does not
advance that series' checkpoint. Retry resumes from the previous successful checkpoint.
Corrupt state fails visibly instead of resetting. Writes are atomic per file, and row
identities are deduplicated so a process interrupted between data and checkpoint writes
can retry safely. Files are not one cross-file database transaction; a consistent remote
Git commit is the persisted collection boundary.

Unexpected source gaps remain visible in reports. If a checkpoint has fallen outside
source retention, use an explicit backfill after reviewing the gap. A measured HTTP 400
boundary is tolerated only during Binance backfill after older data has been received;
other failures retain the prior checkpoint.

Forward-only books use daily files so each routine commit rewrites a small file:
`data/options/deribit_btc/YYYY-MM-DD.jsonl` (every BTC option with non-zero OI: instrument, OI in
BTC, mark IV; underlying price per expiry; about 30 KB per run) and
`data/hl_positions/btc/YYYY-MM-DD.jsonl` (BTC positions of the top 200 Hyperliquid accounts by
account value, with liquidation price and cross/isolated leverage; the ranking is refreshed every
six hours from the ~40 MB leaderboard and cached in `state/checkpoints.json`). Every snapshot
carries `status`: `complete`, or `degraded` with the failing accounts (`failed`) or excluded
option rows (`excluded`) named. A response without the documented structure counts as failed —
`{}` is never an empty account. Half or more accounts failing, or over 5% of option rows
invalid, stores nothing and records the run as failed.

At the 15-minute cadence one routine run stores about 44 KB of text (options 31 KB, Hyperliquid
map 5 KB, snapshot 5 KB, run record 3 KB; about 12 KB gzipped), roughly 4 MB a day and 125 MB a
month before git compression, on top of history series and liquidations, which do not grow with
the cadence. Watch repository size; see the limitations in CHANGELOG 2.6.

Monthly JSONL files retain first observations. Source revisions do not overwrite them.
This release does not implement general revision history for every exchange series.
Liquidation retention and later appearance of orders are tracked separately.

Storage growth depends on activity, snapshot size, forecasts, and retained scoring evidence.
The former “0.5 MB/day, fine for years” estimate is not a capacity guarantee. Monitor repository
size and move long-lived history/evidence to dedicated storage if needed.

## Research tests and skill revisions

Numerical/software regressions live in `regression/`. Prospective research designs live in
`tests/` and use the interface in `tests/_template.py`.

The report says **post-registration**, not “clean.” The framework checks decision time,
input cutoff, outcome maturity, and duplicate group/decision episodes. Use
`ctx.as_of(decision_ms)` for point-in-time inputs. New collection data is eligible only
after its `observed_at` time and interval close. Legacy observations without an availability
stamp are excluded from these views. Historical prices use an event-time cutoff and do
not establish historical API availability.

Test registration fingerprints include the test file and root Python modules. Changes to
those dependencies restart its registration clock. Custom imports, custom data access,
statistical independence, and the test's actual logic still require review. Arbitrary
repository Python is trusted code, not a sandbox. Counts and descriptive intervals do not
establish an edge or authorize a skill change.

`skillcheck.py` is a mechanical checker for an external four-file skill package. It does not
install or edit skills. Review weekly report candidates against the package before adopting
any conclusion. No trading-performance claims are made by this release.
