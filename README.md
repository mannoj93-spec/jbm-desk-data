# JBM desk data — reliability revision 2.1

A small, standard-library Python project that preserves public crypto-market history,
registers forecasts before their start, and produces reviewable research reports.
It does not trade or change a skill package automatically.

This revision addresses scoring, checkpoint recovery, forecast validation, persistence,
research labeling, and monitoring defects in the supplied project. See [CHANGELOG.md](CHANGELOG.md)
and [VALIDATION.md](VALIDATION.md).

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
4. Run **Hourly collector** manually without backfill. Check its source errors, latest timestamps,
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
| Hourly collector | Hourly at :07 UTC; manual | Preserve history, snapshots, liquidations, and registration records |
| Forecast intake | Owner's forecast issues opened/edited/reopened; hourly :37 recovery; manual | Validate, freeze, persist, then acknowledge a forecast |
| Weekly report | Monday 00:30 UTC; manual | Coverage, errors, forecast scores, research summaries, review candidates |
| Regression and numerical fixtures | Code/workflow pushes and pull requests; manual | Arithmetic fixtures and offline failure-path regression tests |

Writing workflows share `repo-write` with `queue: max`. This allows up to 100 pending
runs; it is not an unlimited queue. The hourly recovery pass revisits open forecast
issues missed by event delivery or queueing. A repository owned by an organization
needs an explicit authorized-user policy before phone intake can be used: the default
accepts only an individual repository owner's login.

Scheduled jobs can be delayed. An absent collector is not detected instantly: Actions
failures and the weekly report are the current monitoring channels. A stopped or disabled
report cannot notify you about itself; external uptime monitoring is a future addition.

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
- Predicates use **interval closing times**. A stored hourly row stamped 05:00 is eligible
  as a completed interval at 06:00. `at_utc` requires that exact completed interval;
  `by_utc` requires all expected completed intervals after start through the deadline.
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
fetch is written). Existing observations retain their original bytes and provenance.
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
