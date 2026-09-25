# Operations and research reference

Detailed operation of the collector, forecasts, scoring, storage and the research lab. Moved here
unchanged from the README in revision 2.13; start at the [README](../README.md). Release history is in
[CHANGELOG.md](../CHANGELOG.md), test and deployment evidence in [VALIDATION.md](../VALIDATION.md).

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
| Research lab (`research.yml`) | Every 6 hours at :41 (00:41 UTC also runs a 60-day reconstruction); manual | Versioned events, outcomes, experiments and evidence cards, `reports/research.md`, `reports/skill_proposals.md`, and the coverage refresh of `reports/latest.md`; computes without the write lock, merges into a fresh checkout and commits through `repo-write` |
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
snapshots cannot be taken later. Inside the snapshot stage each source has its own 15-second cap,
and a venue whose request times out or cannot connect is skipped for the rest of that stage, so one
stalled venue costs only its own books (2.6.1).
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
latest scheduled run lost critical data (the Binance share series, or the whole snapshot: no
open-interest book collected), and passes
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

**2.7 storage.** One routine run now stores about 97 KB of text: options 36 KB (schema 2),
Hyperliquid account sample 36 KB, v1 BTC position map 5 KB, snapshot 6 KB, 1-minute price batches
7 KB (five series, 15 bars each), run record 3.5 KB, enrichment 2 KB; plus the hourly option
quote record (68 KB). That is roughly 11 MB a day and 330 MB a month before git compression -
about 2.7 times the 2.6 rate. Reversible reductions: `OPTIONS_SCHEMA=1` (drops the panel, the
quote records and the listing log) and `HL_SAMPLING_POLICY=v1` (drops the account sample and
enrichment). The research lab adds well under 1 MB a day. Move closed months to dedicated storage
before the repository approaches 1 GB.

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

## Research lab (lab-2.2, revisions 2.8-2.10)

```sh
python -m lab.run update                         # as-of replay over stored data
python -m lab.run update --reconstruct-days 60   # plus an exploratory historical reconstruction
python -m lab.run update --no-write              # compute and print only
python -m lab.run update --now MS                # reproduce a past cutoff (read-only)
python scripts/repro_integrity.py [CODE_ROOT]    # the 2.7 review's reproductions, before/after
python scripts/repro_integrity_29.py [CODE_ROOT] # the 2.8 review's reproductions, before/after
python scripts/replay_controls_210.py CODE DATA CUTOFF_MS   # hourly controls, before/after (read-only)
python scripts/repro_controls_211.py [CODE_ROOT]            # 2.10 review: cutoff and authority, before/after
python scripts/repro_publication_212.py [CODE_ROOT]         # 2.11 review: publication gate and canonical merge, before/after
```

**Evaluation versions.** A design (`lab/designs/*.json`) is evaluated under a version id that
binds the design file to the semantic implementation: detector module, labels and costs,
baseline, evaluation rules, evidence attribution and the collector constants the inputs depend on
(`lab/versioning.py`; docstring-free AST hashes, so comment and documentation edits and data
commits never start a new version, while any logic change does). The first run that sees a
version stamps its clock in `state/lab_registrations.json`, never rewritten.

**Decisions are as-of replays.** Every input is used only from its availability; a late required
input delays the decision and more than 60 minutes of delay excludes it; optional inputs
(funding, spot flow, spreads) are used only if already available. Decision time = latest required
input + 60 s ASSUMED processing - an assumption, not a measurement: the lab runs every 6 hours.
The first lab run that computes a decision freezes it (`t_persisted`); later data never changes a
frozen decision, and a decision that appears only after its time was already covered is a late
replay, excluded from evaluation. Episodes of frozen decisions are formed in the order the
decisions became known, so a decision learned later can join an episode but never displace its
head. Time fields are defined in `lab/asof.py`.

**Phases.** `reanalysis` (decisions before registration, re-read under the current logic),
`evaluation` (frozen decisions after registration) and `exploratory` (history fetched later).
Only evaluation can promote.

**Sample accounting.** Per group and horizon: raw firings, collapsed episodes, scorable labels,
retained observations (deterministic thinning on actual label intervals `[entry_t, exit_t)`, so
two decisions entering at the same bar count once) and dependence blocks (overlapping intervals
or the same UTC day, across groups). Intervals resample blocks. Nothing is called independent.

**Comparison observations (controls).** Bar-based modules (A, D, G, H) take one control per
whole-hour bar close. The collection-based modules (B accounts, C liquidation exposure, F options)
take one per UTC hour of required-input availability (`lab/controls.py`, policy
`hourly-first-available-1`): the candidate whose required inputs (C: account observation and the
same run's mark; F: the option record only, never funding; B: both account observations) became
available earliest, ties by source time then input key; decision time = that availability + 60 s
assumed processing, never re-dated to the hour; the existing late-input exclusion applies; an hour
without an eligible candidate has no control and a recorded reason. The first lab run freezes each
hour's control (`research/v2/<design>/<version>/controls/`, first record wins); later data,
reruns and merges never replace it, a stored selection is used only at cutoffs after it was made,
and a frozen control counts as known (for checkpoints and baseline training) only from then.
Since 2.11 a candidate or stored control is usable only when its inputs and its decision (inputs
+ 60 s) - and for a stored one its persistence - are within the cutoff; otherwise the hour is
`pending_processing` or the record is withheld (never rewritten or replaced). A writing run appends
its proposals under a lock, reads the stored records back and uses those (a proposal that lost is
`superseded`); a read-only run writes nothing and marks its own selections `provisional`.
Controls are validated before labelling, the labelled controls are compared with the stored ones
(fingerprints), and any unresolved conflict or mismatch is a RESEARCH INTEGRITY FAILURE in the
report that makes the lab exit 1; `scripts/merge_research.py` rejects an incoming batch computed
from a losing selection or checkpoint (exit 3, nothing merged).
Since 2.12 that integrity check is a precondition of evaluation (`experiments.input_integrity`,
run after labelling and before anything is written): a design using hourly controls whose check
fails or is incomplete is **blocked** - no frozen decision, outcome or checkpoint is written (a
recorded "supported" checkpoint is shown as history and cannot override it), its watermark is not
advanced so a later valid run evaluates the same decisions as new, no proposal is made, and its
card names the reasons and the last valid result. Bar-based designs report `not_required`. All
evaluation writes of a design happen only after every variant has run without error.
`evidence.publication` is the one publication decision (card, report, proposals, summary); the lab
writes it per design in `--summary lab-summary.json` (schema `lab_summary/2`: design, evaluation
version, cutoff, validation status and reasons, publication decision), and the persist job's merge
refuses (exit 4, nothing merged) a batch whose rows, cards, index, reports or watermarks are
missing, stale or contradict it. Merge equality is canonical JSON (key order and whitespace
ignored; values, array order and types significant), so reformatted copies of stored records
neither conflict nor duplicate.
Cards and `reports/research.md` show comparison coverage: hours covered, eligible and selected,
missing hours with reasons, delay after the hour, closed versus partial hours, and per horizon the
controls selected / mature / scorable / retained / baseline-usable. Only the design's primary
horizon decides status and proposals; secondary horizons are descriptive.

**Checkpoints.** A verdict is only ever produced at a scheduled look (1, 1.5, 2, 3 x the
minimum), from a precisely bounded dataset: cutoff C = the earliest time at which the look's n
retained test observations were known (outcome available per `label_available`, and decision
frozen). The reference or controls, the test group's direction mix, severity, dependence blocks,
baseline training rows and predictions, data quality and the family's variant count are all as of
C, so later observations cannot enter. The look's manifest (every input row and prediction, the
criteria, cutoff and version), its sha256, the checks and the verdict are appended once to
`research/v2/<design>/<version>/checkpoints.jsonl` and never recomputed; each run re-checks the
record against current data and reports drift (what differs) without changing it. A look whose n
observations are not yet known is pending. Correcting a completed checkpoint takes a new
evaluation version, which keeps the old records.

**Promotion ("supported")** needs, at a recorded checkpoint, all of: at most 10% incomplete labels
among the test labels that ended by the cutoff; >= 100 retained test observations in >= 20 blocks;
a multiplicity-adjusted interval (alpha 0.10 / (variants tried in the family by the cutoff x 4
looks)) excluding zero in the declared direction; an out-of-sample baseline for the primary horizon
(OLS on prior 60-minute return, volatility and aligned funding, fitted on same-horizon controls
whose labels were available before each UTC day and before the cutoff) identifiable for >= 80% and
its residual difference excluding zero the same way; comparable event severity for event-group
references; and the same sign in both halves. A missing baseline or quality blocks promotion; a
wrong-side interval retires the version. Every horizon has its own baseline in the summaries, and
a horizon without enough same-horizon controls shows no baseline comparison. "Supported" is not a
claim of profitability, and a skill-change proposal is written only from a supported checkpoint
whose manifest re-verifies, quoting that checkpoint.

**Outputs** (all under the version namespace): `research/v2/<design>/<version>/events|outcomes/`,
`research/v2/<design>/<version>/checkpoints.jsonl`, `research/v2/<design>/<version>/controls/` (B, C, F),
`research/v2/experiments/`, `research/v2/ledger/`, `research/evidence/v2/<design>@<version>.json`,
`research/evidence/index.json` (current, superseded and legacy cards), `reports/research.md`,
`reports/skill_proposals.md`. The lab-1.0 outputs from 2.7 (`research/evidence/cards`,
`research/experiments`, `research/ledger`, `state/lab_registered.json`) are kept as recorded,
marked legacy in the index, and never written again.

**Reports.** The Research lab workflow also refreshes `reports/latest.md` every 6 hours
(`report.py --coverage-only`: coverage and dataset freshness, no forecast scoring). Every report
states its generation time, input cutoff, code versions and per-dataset freshness; the weekly
report still does the scoring. Outputs computed on an older checkout are merged
(`scripts/merge_research.py`) so a newer report or row is never overwritten.

**Module inputs and current limits.** A flow absorption and G cross-asset need 7 and 14 days of
stored 1-minute bars (collected from 2.7 on; reconstruction runs meanwhile). B account behaviour,
C liquidation exposure and D TWAP lifecycle use the Hyperliquid v2 sample; C is sampled exposure,
never market inventory. Transfers and liquidations are attributed transaction by transaction to
the transition interval (t0, t1], matched to account, coin and side, with explicit
partial/failed/unchecked coverage states (`lab/hlevidence.py`). E liquidity recovery needs the streaming service and reports
"unavailable" without it. F options/perp disagreement needs about two weeks of option records for
its z-scores (each history value is used only from its own availability: skew from the option
record, funding from its snapshot; a value not yet available is missing, never filled); its test group counts only quote-qualified events (the 25-delta legs of the ~7-day
expiry passed freshness, two-sided, spread, expiry and mark-inside-quotes checks), and a separately
labelled mark-only variant is descriptive and never promotable. H deleveraging uses OKX liquidations (bankruptcy prices) and the OKX insurance fund;
Bybit, Deribit and Binance deleveraging data are not available to the collector.

**Skill evaluation.** `python -m lab.skill_eval --current DIR --revision DIR` compares two skill
directories: file hashes and diff, the case checks in `lab/skill_eval_cases.json`, and an
evidence audit that flags any sentence calling a design supported, validated or an edge when its
card says otherwise. Add `--live --model MODEL` with `ANTHROPIC_API_KEY` set to also compare
replies to the cases' prompts; without a key it says so and does nothing else. Output goes to
`~/.jbm-skill-eval` (or `--out`), never inside the repository, and neither skill directory is
modified.

**Streaming service.** See [stream/README.md](../stream/README.md): what it records, how to run and
deploy it, measured resource use, and the infrastructure decision it is waiting for.

`skillcheck.py` is a mechanical checker for an external four-file skill package. It does not
install or edit skills. Review weekly report candidates against the package before adopting
any conclusion. No trading-performance claims are made by this release.
