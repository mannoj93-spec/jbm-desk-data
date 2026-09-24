# Research-integrity revision 2.9 (lab-2.1) — 2026-09-23

Response to the review of 2.8 (commit `c9fff86`). The default branch was inspected first: from
`c9fff86` to the start of this work only automated data commits had landed, so all three issues
applied to the running code. Each was reproduced on `c9fff86` with `scripts/repro_integrity_29.py`
(runs against any code tree) before it was fixed. The collector is unchanged (`collector-2.7`):
schedule, budgets, source isolation, serialized writes, watchdog and request limits are untouched,
and no stored observation, cohort, frozen decision or earlier evidence file is rewritten.

| # | Issue (reproduced on c9fff86) | Fix | Tests (`regression/test_rev29.py`) |
|---|---|---|---|
| 1 | The first 100 test observations gave `retired`; appending 100 later ones gave `supported` at the same n=100 look (the look reused the first 100 outcomes but took the long share, reference, severity and controls from the whole sample) | A verdict exists only as a recorded checkpoint. Cutoff C = the earliest time the look's n retained test observations were known (outcome available and decision frozen); test, reference or controls, direction mix, severity, blocks, baseline training rows and predictions, data quality and the family's variant count are all bounded by C. The manifest (every input row and prediction, criteria, cutoff, version), its sha256, the checks and the verdict are appended to `research/v2/<design>/<version>/checkpoints.jsonl` once and never recomputed; later data is audited against it (drift, with what differs) but cannot change it. Pending = n not yet known. A correction is a new evaluation version (automatic on any semantic change), which leaves the old records in place | `CheckpointTests`: n=100 verdict unchanged after appending (also via a single run with all 200); later direction flips, severities, outcomes, controls and appended controls leave the manifest hash identical; delayed outcomes move the cutoff and stay out; exact boundaries; freeze time; pending; quality window; later looks use their own additional observations and cutoffs; idempotent repeat runs; multiplicity as of the cutoff; drift reported not rewritten; new version keeps the old record; tampered manifests fail verification; skill proposals quote a verified checkpoint only. `CheckpointMergeTests` |
| 2 | Funding first observed at 10:00 changed whether a 09:45 option event (inputs complete 09:47) existed: the z-score history stamped every feature with the option record's time | Each history feature carries its own availability (rr25: the option record's `observed_at`; funding: its snapshot's `observed_at`). The window is the last `z_window` earlier records already observed at the decision; within it a funding value counts only if its snapshot was observed by then, otherwise it is missing (never filled) and the 70% coverage rule applies; funding with no snapshot time is unknown | `OptionsAvailabilityTests`: 10:00 funding cannot change the 09:47 event (existence, direction, features, eligibility; quote-qualified and mark-only); it is used by the 10:00 decision; exact cutoff (equal counts, +1 ms does not); missing funding stays missing and can fail coverage; a delayed current snapshot delays the decision; late records and later records do not revise the event |
| 3 | A baseline trained on 60-minute control outcomes predicted the 30, 240 and 480-minute outcomes | One OLS model per horizon, trained only on same-horizon control labels whose `label_available` (new on every label: the latest availability of the bars it read) was no later than the prediction's UTC day and, at a checkpoint, its cutoff; cache keyed by (horizon, day, cutoff). Each outcome is routed to its horizon's model; each summary reports the model's training target, training rows, identifiable share and unidentified reasons; a horizon without enough labels is unidentifiable and its comparison withheld (never borrowed from another horizon). A single model for a multi-horizon design is refused | `HorizonBaselineTests`: horizon-specific outcomes give ~0 residuals at 30/60/240 (2.8: +47.7 and +33.4 bp); training rows same-horizon and known by the bound; a control that ended before the day but was available after it is excluded; missing 480-minute labels stay unidentifiable; the primary-horizon checkpoint uses its own model and is blocked, not rescued, when that model is unidentifiable |

**Before / after** (`python scripts/repro_integrity_29.py [tree]`): #1 `retired` -> `supported` on
c9fff86 after appending, `retired` / `retired` on 2.9 with the n=100 checkpoint recorded (p_long 0.0);
#2 the 09:45 event present with small future funding and absent with large future funding on c9fff86,
identical on 2.9 for both policies; #3 mean 30/240-minute test residuals +47.7 / +33.4 bp and the
480-minute baseline "identifiable" with no 480-minute controls on c9fff86, 0.0 / 0.0 bp and
unidentifiable on 2.9.

**Other changes.** `summarize` takes a baseline per horizon; `status` reads recorded checkpoints
only (a terminal record that fails re-verification yields `blocked`, never a verdict) (the pass's data state no longer gates promotion; the in-window quality check does, and the
pass state stays on the card); a checkpoint verdict of `blocked` shows as status `blocked`.
`scripts/merge_research.py` never adds a second record for a look already in the checkout.
Evidence cards carry `checkpoints` (records without the per-row manifest, `verified`, pending,
drift); the index records `superseded_by` for superseded versions; `reports/skill_proposals.md`
proposes only from a supported checkpoint whose manifest re-verifies and quotes that checkpoint.

**Hardening from an adversarial review of the first 2.9 draft** (each with a regression in
`test_rev29.py`): (a) episodes of the primary prospective pass are built in the order decisions
became known (`events.collapse_as_known`), so a decision frozen after a cutoff can join an episode
but never displaces a known head or removes a known observation (`KnowledgeOrderTests`); (b) an
option control's only required input is its option record, so a late or missing funding snapshot
no longer moves, delays or drops a control; (c) the first stored freeze of a decision wins when
frozen decisions are loaded, and `merge_research.py` keys frozen-decision lines by
`decision_key`; (d) `label_available` also covers the settled funding a label attributes (as
`(t, rate, avail)`), a label whose window contains a settlement time the funding series has not
reached is immature rather than completed without it, and the spread snapshot used for costs must
have been observed by the decision; (e) `verify_checkpoint` also checks record/manifest
consistency (n rows, cutoff, every row known by the cutoff, adjusted alpha, look schedule, and
against the design: n per look, version, horizon, sign); the sha256 is tamper-evident, not a
signature; (f) the family's variant count at a cutoff includes current versions only if
registered by then; (g) a checkpoint already stored by another writer is re-read and used.

**Test-suite date dependency found at deployment.** The first regression run on main after the
merge (00:02Z on 2026-09-24) failed in the unchanged 2.7 test
`test_stream.ConnectionTests.test_bybit_gap_resubscribes_and_disconnect_recorded`: the service
files each gap under the UTC day of its own time (the update-id jump under its message time,
2026-09-23; the disconnect under the wall clock), while the test read only today's partition, so
it could pass only on 2026-09-23. It fails identically on `c9fff86` after midnight. The test now
reads both days; `stream/` is unchanged.

**Migration.** `lab-2.1` changes the semantic code, so the first lab-2.1 run registers a new
evaluation version for every design; the lab-2.0 versions are marked `retired (superseded)` with
`superseded_by`, and their registrations, cards, experiment and ledger rows stay byte-for-byte. No
lab-2.0 version had a frozen evaluation decision or a completed look (no `research/v2/<design>/`
directory existed), so no verdict needed re-deriving. Recomputations of data collected before the
new registration are labelled `reanalysis`.

**Versions.** `lab-2.1-2026-09-23`; collector and report unchanged. Tests: 266 regression tests
(238 kept; 28 in `test_rev29.py`; four 2.8 promotion tests in `test_lab.py` and the summaries in
`test_integrity.py` were ported to the checkpoint and per-horizon interfaces with the same intent,
none removed; the one assertion that an `insufficient_data` pass cannot promote became an
assertion that incomplete labels inside the checkpoint window block it; the synthetic funding
series of `test_costs_direction_and_funding` gained a zero settlement at 08:00 so it reaches the
end of its 8-hour window) plus 25 numerical fixtures.

# Research-integrity revision 2.8 (lab-2.0) — 2026-09-23

Response to the review of 2.7 (commit `900d0b1`). The default branch was inspected first: from
`900d0b1` to the start of this work only automated data commits had landed, so every finding
applied to the running code. Each was reproduced on `900d0b1` with `scripts/repro_integrity.py`
(runs against any code tree) before it was fixed. The collector is unchanged (still
`collector-2.7`): schedule, budgets, source isolation, serialized writes, recovery artifacts,
watchdog, the fixed/rotating account policy, the six-hour ranking cache and request limits are
untouched, and no stored observation, checkpoint, frozen forecast or lab-1.0 output is rewritten.

| # | Finding (reproduced on 900d0b1) | Fix | Tests |
|---|---|---|---|
| 2 | Two events an hour apart whose inputs arrive together enter at the same bar, yet counted as 2 independent observations at 30 and 60 min | Thinning on actual label intervals `[entry_t, exit_t)`; dependence blocks (overlap or same UTC day, across groups) drive the bootstrap; firings / episodes / scorable / retained / blocks reported separately; nothing called independent | `test_integrity.OverlapTests` (identical entry, partial overlap, touching boundaries, all four horizons, delayed batch, outage catch-up, opposite directions, cross-group blocks, outcome-blind selection) |
| 3 | A prior BTC bar delayed 49 min left a module G event dated 48 min before that input existed (the check used only the final bar) | Every module computes `t_inputs` over every required input (windows, prior sigma/return windows, threshold and volume history, marks, cohort records, insurance rows); > 60 min of delay excludes; optional inputs (funding, spot, spreads) only if already available; decisions frozen at the first lab run (`t_persisted`), late replays excluded from evaluation; the 60 s processing time is labelled an assumption | `AvailabilityTests` (G delayed/excluded, funding as-of, A prior bar and optional spot, C mark), `FreezeTests` (recomputation cannot alter a frozen decision; late replay excluded) |
| 4 | 7 of 8 designs had no baseline predictors, so "supported" needed no added value; registration keyed on design JSON only | Out-of-sample baseline for every design (OLS on prior return, volatility, aligned funding, fitted on controls matured before each UTC day); unidentifiable baseline or quality blocks promotion; severity comparability for event references; Bonferroni over variants x 4 scheduled looks; evaluation versions bind design + semantic code + data dependencies; versioned namespaces for events, outcomes, registrations and cards | `VersionTests` (code-only change = new version; docstring, comment, README and data edits = same; superseded evidence stays), `test_lab.ExperimentTests` (promotion, blocking, multiplicity, severity) |
| 5 | Ledger query 0-80 min with a deposit at minute 5 labelled a 60-75 min transition "confirmed transfer" | Per-transaction filtering to `(t0, t1]`, account/coin/side matching, `liquidatedPositions` and `liquidatedUser` checks, explicit covered / partial / failed / not_attempted / unchecked states, knowledge at decision vs later confirmation (`lab/hlevidence.py`) | `AttributionTests` |
| 6 | 1-2 ms of timing jitter turned 3 liquidity events and 1 control into 0 and 0 | Nearest-second slots within 250 ms, deterministic duplicate resolution, 2 s freshness, 5 s availability; gaps and missing or stale seconds still fail coverage | `StreamTimingTests` (Recorder -> LocalStore -> module; exact vs jittered identical; missing, stale, sequence gap) |
| 7 | All 12 panel quotes stale changed only counters; the event was unchanged | Descriptive mark-IV surface separated from a quote-qualified signal: the 25-delta legs of the ~7-day expiry must be fresh, two-sided, uncrossed, within 10% spread, > 1 day to expiry and have mark IV inside the quotes; failures regroup events as `*_ineligible`; unobserved quality stays unknown; a mark-only variant is labelled descriptive and never promotable | `OptionQualityTests` |
| 8 | `reports/latest.md` was report 2.3 from 16:17Z after the 2.7 deployment | `report.py --coverage-only` refreshed every 6 hours by the Research lab workflow; every report states generation time, input cutoff, versions and per-dataset freshness; outputs merged into a fresh checkout without rewinding newer content (`scripts/merge_research.py`) | `PersistenceTests` |

Qualifications. Finding 3 reproduces at 48 minutes with the repository's own synthetic
construction (the review reported 49; the mechanism is identical). Finding 7 is a policy gap, not
evidence that the mark-IV values were stale: mark IV is collected independently of the panel and is
still reported, now labelled descriptive. Hyperliquid spot transfers are stored by the collector
only as counts without times, so they cannot be attributed to an interval; they do not move perp
margin and are excluded from transfer attribution.

**Migration.** The first lab-2.0 run registers a new evaluation version for every design
(`state/lab_registrations.json`); lab-1.0 registrations (`state/lab_registered.json`) and outputs
(`research/evidence/cards`, `research/experiments`, `research/ledger`) are kept byte-for-byte,
marked legacy in `research/evidence/index.json`, and never written again. Design files moved to
`version: 2` (baseline block, `min_retained_observations`, `min_dependence_blocks`). No lab-1.0
decision had been persisted (no module had prospective events), so nothing needed reinterpreting.
Recomputations of data collected before registration are labelled `reanalysis`, never evaluation.

**Versions.** `lab-2.0-2026-09-23`, `report-2.5-2026-09-23`; collector unchanged. Tests: 238
regression tests (200 kept, 3 added to `test_lab.py`, 35 in `test_integrity.py`; eight 2.7
lab tests were adapted to the new APIs with the same intent, none removed) plus 25 numerical fixtures.

# Research-data revision 2.7 — 2026-09-23

Adds the data and the machinery to look for testable trading advantages and to review changes to
the desk's skill files against evidence. It is additive: no stored observation, checkpoint,
frozen forecast, score or provenance field is rewritten, every new record is versioned, and each
new collection path can be switched back without a code change. The 15-minute schedule, stage
budgets, serialized writes, deadline handling, recovery artifacts, dedup and watchdog behaviour
are unchanged; the six-hour ranking cache and the 200-account Hyperliquid budget are kept.

**Collector (`collector-2.7`)**

- *Deribit options, schema 2* (`optionsbook.py`). The per-run record keeps the schema-1 fields
  (`[instrument, OI, mark IV]` rows, `underlying`) and adds: zero-OI instruments by name, listed
  instruments absent from the summary, past-expiry names, instrument metadata status, the
  per-expiry underlying (`underlying_v2`), estimated delivery price, and a 12-ticker quote panel
  (expiries near 2/7/30 days, call/put at Black-76 delta 0.50/0.25). Full quotes (bid, ask, mark,
  last, rolling-24h volume in BTC and USD, source time offset) go to a separate hourly record
  `options/deribit_btc_quotes`; listing changes to `options/deribit_btc_listing`. Rolling 24h
  volume is labelled as such and never presented as interval volume; null bid/ask means no resting
  order, zero OI is listed, not omitted. Revert: `OPTIONS_SCHEMA=1`.
- *Hyperliquid sampling policy `hl-sample-v2`* (`hlsample.py`). Same 200-request budget: a fixed
  cohort of 100 (the top 100 of the first ranking seen under v2, frozen with its selection time,
  ranking hash and member hash in `state/hl_cohort_fixed_v2.json`, never re-selected), 90 rotating
  accounts from the top 1,000 (cursor in state), and at most 10 enrichment requests (fills, ledger,
  TWAP history; weight-capped at 400). Every sampled account is recorded as ok_btc / ok_flat /
  ok_other / failed / not_attempted, with margin summary and BTC/ETH/SOL positions, in
  `hl_accounts/`; enrichment results in `hl_enrich/`. No account is selected by later performance.
  The v1 BTC position record is still written (with `sampling_policy`). Revert:
  `HL_SAMPLING_POLICY=v1`.
- *Enrichment stage* (`enrich.py`, 10% of the budget, after forward books, failures isolated):
  closed 1-minute bars for Binance USD-M BTCUSDT (last and mark), spot BTCUSDT, ETHUSDT and
  SOLUSDT perps as batch records in `data/prices/<series>/` (checkpointed, first observation
  wins, malformed pages rejected); OKX BTC-USDT swap insurance fund rows (balance plus every
  bankruptcy-loss, ADL and liquidation-deposit row newer than the last) in `okx_insurance/`.
- *Cross-asset snapshot sources*: Hyperliquid and Binance ETH and SOL mark, funding (with its
  interval) and OI in base and quote units.

**Research lab (`lab/`, `lab-1.0`)** - a separate package, run by the new *Research lab* workflow
every 6 hours (compute without the write lock; commit through `repo-write`).

- Layers with provenance: events (with their feature records), outcomes, experiments, a variants
  ledger that keeps null results, and evidence cards. Every record carries `t_event`,
  `t_first_observed` and `t_available`; historical reconstructions are labelled as such.
- Outcome labels at 30 m, 1 h, 4 h, 8 h: return, range, MFE/MAE, realised volatility, and net
  return after an explicit cost model (`costs-1`: fees and slippage are stated assumptions,
  spread from the nearest depth snapshot, funding from settled rates). Entry is the first bar at
  or after availability; immature and incomplete labels are never stored or filled.
- Episodes are collapsed; scheduled controls give baselines; test-minus-reference intervals use a
  day-block bootstrap; outcomes are thinned to non-overlapping windows. Designs are frozen by hash
  and registered on first sight; only episodes after registration can move a design toward
  "supported". Statuses: exploratory, under prospective evaluation, supported, retired.
- Eight modules (A flow absorption, B account behaviour, C liquidation exposure, D TWAP lifecycle,
  E liquidity recovery, F options/perp disagreement, G cross-asset, H exchange deleveraging), each
  reporting available / insufficient_data / unavailable with the reason.
- `reports/research.md` and `reports/skill_proposals.md`; a change to the skill files is proposed
  only for a supported design. `lab/skill_eval.py` compares a current and a revised skill offline
  (case checks and an evidence audit that flags overclaims); live comparison is optional, needs
  an API key, and writes only outside the repository.

**Streaming service (`stream/`, `stream-1.0`)** - implemented, tested and live-smoke-tested, not
deployed: Deribit, Bybit and Hyperliquid books, trades and forced-flow messages with sequence
checks, gap log, heartbeat, rolling pre/post capture buffer, hourly controls, gzip partitions and
an optional S3-compatible durable copy. Needs an always-on host (see `stream/README.md`).

**Report** `report-2.4`: section 3c covers the new datasets and the lab's last run.

**Fixes found while testing this revision.** Module H could judge a 5-minute liquidation bucket
before the bucket had closed; it is now judged at max(first observation, bucket close). Module D
could value a TWAP with a later price; it now uses only bars available at first observation.

**Tests**: 76 new (`test_rev27.py` 20, `test_lab.py` 30, `test_stream.py` 26); the full suite is
200 tests plus 25 numerical fixtures, offline, about 20 s.

# Collection cadence revision 2.6.1 — 2026-09-23

From the review of 2.6 (commit `62e51cc`), two failure cases found by simulated faults; neither
occurred in a deployed run.

**One stalled venue could still cost every venue its snapshot.** The 2.6 stage limit kept time
for the snapshot stage but did not isolate venues inside it. Binance is requested first; with every
Binance request stalled, the 120 s stage made 5 Binance attempts, 0 requests to any other venue,
and stored 0/17 books (reproduced). Two controls now apply to snapshot sources:

- Each source has its own time cap (`SNAP_SOURCE_S` = 15 s; a normal source answers in under 2 s).
- A host whose request failed at the transport level on every attempt (timeout, reset, DNS) is
  skipped for the rest of the snapshot stage ("circuit open"), so its other sources fail at once.
  HTTP error statuses and malformed bodies are fast and do not open the circuit. The circuit is
  limited to the snapshot stage, so one Hyperliquid account timing out still cannot reject the
  200-account map, and it resets each run.

Same simulation under 2.6.1: 1 Binance attempt, 27 requests to other venues, 14/17 books
collected (every non-Binance book), stage done in 20 s. Run records add `circuit_open` (hosts) and
`http.circuit_skipped`.

**A total snapshot loss was reported healthy.** With history intact and 0/17 books, the watchdog
exited 0 with warnings. `cadence.failure_summary` now treats a run with no open-interest book as
critical (watchdog exit 2, "no open-interest book collected (0/17)"; counted in the report's
critical line). A partly degraded snapshot stays a warning. The collector's own exit code is
unchanged: it still fails the workflow only when the critical Binance share series fails.

**Tests**: 5 new, 1 strengthened (`regression/test_rev26.py`). The stalled-venue tests now supply
valid answers for every other venue and require all 14 unaffected books to be collected, not
merely attempted. 6 of the new or strengthened tests fail or error on 2.6.

# Collection cadence revision 2.6 — 2026-09-23

The collector runs every 15 minutes (`7,22,37,52 * * * *`) instead of hourly. This revision is
about cadence and operational reliability only: no forecast, scoring rule, trading rule or stored
observation changes, and every existing data file, checkpoint, frozen forecast, score and provenance
field is kept as it was.

**Schedule and time budget**

- `collect.yml` keeps its file name, so the workflow's run history and dispatch URL carry over;
  its display name is now **Collector**. Manual runs and backfill are unchanged.
- Routine run: 10-minute network budget (`COLLECTOR_BUDGET_S=600`), collection step limit 11
  minutes, persistence bounded at 100 s, job limit 14 minutes. Backfill keeps its own budget:
  30 minutes of network, 35-minute step, 45-minute job. The previous 20-minute budget inside a
  30-minute job would not fit a 15-minute slot.
- Stage limits inside a routine run (shares of the budget): history series 40%, liquidations 15%,
  snapshot 20%, forward books the rest. History and liquidations are checkpointed and recover next
  run; snapshots and forward books cannot be fetched later. In simulation under 2.5, one stalled
  venue (Binance) spent the whole budget on history and left 0 s for the 17-book snapshot; under
  2.6 history stops at 240 s and the snapshot and forward books still run.
- `scripts/commit_push.sh` bounds its whole push/rebase loop (`PERSIST_BUDGET_S`, 100 s for the
  collector, 240 s default) and gives each network step at most the time left, so a hung remote
  cannot run persistence past the job limit. Success still requires a successful push.
- The daily liquidation boundary probe keys on the UTC day it last succeeded
  (`state/checkpoints.json: liq_probe_day`) instead of the 00Z hour, which at the new cadence
  would have paged the full feed four times; a failed probe is retried on the next run.

**Queueing** (checked against GitHub's current concurrency documentation before the change)

- Scheduled collector runs share one workflow-level group with GitHub's default queue: at most one
  running and one pending, and a newer pending run cancels the older pending one. During an outage
  or a long backfill, obsolete scheduled runs are dropped instead of accumulating. Nothing running is
  ever cancelled. Manual and backfill runs have their own groups, so a scheduled run never cancels
  a manual check.
- Every repository writer (collector, backfill, forecast intake, weekly report) now takes
  `repo-write` at job level with `queue: max` (up to 100 waiting jobs), so writes stay serialized
  and intake and report work is never dropped behind collector runs. Job level also keeps a skipped
  intake job (an issue that is not a forecast) out of the queue.

**Provenance and health**

- Run records carry `mode: "routine"` (`"hourly"` in older records, still read as routine),
  `trigger` (`schedule`, `workflow_dispatch`, or `local`), the cron entry that fired, the Actions
  run id and attempt, the budget, per-stage seconds, stages cut by their limit, whether the budget
  was reached, and request accounting: requests, failures, deadline skips, and rate-limit
  incidents by host (HTTP 429/418 and OKX code 50011).
- `cadence.json` records every schedule the collector has run under. Health figures use the
  cadence in force at each moment, so the hourly period is not reported as three runs in four
  missing.
- The weekly report separates **scheduled execution** (scheduler starts counted against nominal
  slots; manual runs excluded; starts are never matched to slots, because GitHub's start delay is
  unrecorded) from **snapshot coverage** (slot intervals holding a stored snapshot, whatever started
  it). Pre-2.6 records do not say what started them, so their scheduled share is shown as an upper
  bound, not a count. It also reports actual intervals between runs and between snapshots, runtime
  percentiles, budget hits and rate limits, and groups alerts by source (count, first, last, latest
  message) instead of one line per run.
- Watchdog every 30 minutes (`17,47`), stale limit 90 minutes (`WATCHDOG_STALE_MIN`, repository
  variable or dispatch input). Exit 1: stale or missing, judged on runs the schedule could have
  started; a recent manual run does not hide a dead schedule. Exit 2: running but the latest
  scheduled run lost critical data. Exit 0 with warnings: source failures, degraded books or rate
  limits in recent runs. It checks out only `data/runs` and the code.

**Tests**: 32 new (`regression/test_rev26.py`): cadence transition, delayed, dropped and manual
runs, aggregation, watchdog states and threshold, workflow budgets and queues parsed from the YAML,
a sustained outage finishing inside the budget with the persistence window left, a single stalled
venue, bounded persistence against a hung remote, the once-a-day probe, provenance and rate-limit
accounting, and native 5m/1h resolution without duplicates across quarter-hour runs. One 2.5
watchdog assertion changed deliberately: a run 2 hours old is now stale (limit 90 minutes, was 3
hours).

**Limitations**

- Repository growth: about 44 KB of text per routine run (12 KB gzipped), roughly 125 MB a month
  in the working tree, mostly the Deribit option book. Git storage grows by the compressed
  amount, but every run checks out the full tree, so checkout time grows too. A later revision
  should compress or relocate the forward-only books; nothing here changes their format.
- GitHub may start scheduled runs late or skip them under load; the health figures report that
  rather than prevent it. Actions minutes are free for this public repository; a private copy
  would use about 8,600 billed minutes a month at this cadence.
- A manual run can wait behind a running scheduled run (one `repo-write` queue); it is never
  cancelled by one.

# Reliability revision 2.5.1 — 2026-09-23

From the review of 2.5: cleaning up an abandoned HTTP-error response could overrun the deadline.
`_abort()` looked for the socket at `resp.fp.raw._sock`, which is right for a normal response, but
an `HTTPError` wraps the response one level deeper, so the shutdown failed silently and the
following `close()` waited on the lock held by the worker's receive. Reproduced with a local server
that sends headers, one body byte 0.1 s before a 1.2 s deadline, then stalls:

| Status | 2.5 | 2.5.1 |
|---|---|---|
| 503 | 2.31 s, rejected | 1.20 s, rejected; worker released at once |
| 200 | 1.20 s, rejected | 1.20 s, rejected |

- `_find_socket()` follows `fp`/`raw`/`_sock` through any wrappers to the socket.
- `_abort()` only shuts the socket down. It no longer calls `close()` from the waiting thread, so
  cleanup cannot block even if a future wrapper hides the socket; the worker closes its own
  response once released, or ends at its socket timeout.
- Tests: two late-byte stall cases (503 and 200) assert the caller returns within 0.15 s of the
  deadline and that the abandoned worker finishes within 0.5 s, which only a shutdown that reached
  the socket achieves. The 503 case fails on 2.5.

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
