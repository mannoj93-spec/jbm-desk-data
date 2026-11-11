# Market source quality and the prospective options pilot

## Operational checks

`market_study_ops.py check` is read-only. `report` writes the health reports and the separate
hash-chained `streams/market-studies/source-quality/events.jsonl` diagnostic journal. Neither changes
historical bars, predictions, outcome scores, eligibility or the identities of v1 and state v2.

A source incident requires at least five consecutive one-minute BTC, ETH or SOL perpetual bars with
identical positive OHLC prices, zero volume and explicitly zero trades. Missing counts do not mean
zero. Gaps and price changes break a run; a subsequent bar with trades and volume records recovery.
The incident keeps the exact bar hash, observed availability, first detection time, and recovery
updates. BTC spot and mark closes at the last affected minute provide cross-feed differences when
available. The cause stays unknown: flat last-trade bars alone do not establish an exchange outage.
The health JSON lists intersecting BTC state and paired outcome windows, including dependent arms;
these annotations do not remove scores or create independent samples. Unresolved incidents alert;
recovered incidents remain visible as warnings. First detection is never backdated to source time.

Options health has separate capture and 7d/30d usability counts. Two missed captures trigger the
continuity alert. A horizon below 80% usability over at least six closed opportunities generates a
quality warning, even after it recovers. These are operational thresholds, not relaxed quote filters.
The legacy joint-usability summary remains for compatibility. A loss/recovery of eligibility does
not count as an expiry roll; the roll counter compares each horizon's last known usable expiry pair.

`state_score_verifier.py` checks the existing publication bindings, then reproduces each cached v2
outcome path, bar hash, Brier losses, primary difference and event label at its recorded scoring
cutoff. Health and CI fail on mismatches, including a numerically altered score whose journal has
been rehashed. The external verifier leaves the registered v2 implementation unchanged.

`health.py` reads service-watch and study-watch jobs from the latest completed main-branch recovery
run, even when another job failed. The check step's completion determines its 45-minute heartbeat;
the step result is separate. Setup, skipped checks, no runner, or unavailable job evidence never
count as a successful check. Native schedule diagnostics and external-trigger arrival diagnostics
remain separately labeled. A failed check without finding annotations is reported as a failed check,
not a proven collector outage.

## Options expiry-selection pilot

This is a new capability study, not a revision to v1. Code, frozen dependencies and
[`protocol.json`](../research_tools/options_pilot/protocol.json) are hashed in a separate registration
under `streams/market-studies/options-v2/`. The workflow publishes registration, confirms the exact
registration and implementation on main, and activates at the following UTC hour. Merge alone is
not activation. Changes to its identity after registration require another version and launch clock.

Each scheduled UTC hour shares one first-observed source capture between two arms:

- **Nearest listed:** the existing nearest-expiry bracketing and frozen leg-selection implementation.
- **Nearest eligible:** nearest eligible expiry on each side of the target, under exactly the same
  frozen leg filters. Expiries stay between 1 and 45 days; maximum bracket span is 14 days for 7d and
  35 days for 30d. These caps are fixed before launch. No extrapolation or later substitute capture.

Both arms use the existing total-variance interpolation and delta, quote, age, spread and OI rules.
The pilot changes expiry selection, not the frozen leg algorithm. Diagnostic quality flags in the
v1 per-leg report can be stricter than that historical algorithm; neither is silently rewritten.

Source capture and selection must occur before the hour ends. Missing closed hours stay in the
scheduled denominator; successful later captures never backfill them. A raw source artifact,
expiry-candidate decisions, chosen instruments and results are content-addressed and retained.
Reports replay selection from those artifacts and validate journal chains. The report shows both
usable, gained, lost, neither, and missing captures separately for each horizon; RR25 differences
are reported only for joint usable captures. Maturity spans accompany usability gains.

Selected contracts from both arms and horizons are deduplicated (at most 16 per hour). The pilot
requests the public Deribit [`get_order_book`](https://docs.deribit.com/api-reference/market-data/public-get_order_book)
endpoint at depth 1 with at most four concurrent requests. Each request has the existing 12-second
hard process timeout; batches over 60 seconds are marked late. Source captures more than 15 minutes
old skip book requests explicitly. Missing sizes remain null; zero size is recorded only when
actually supplied by the venue. Wrong instruments, stale/future timestamps, closed markets,
one-sided/crossed prices and invalid sizes are unusable. Raw responses, source/request/receipt
clocks, source-to-book lag, and amount/price units are retained. Books are later observations and
never change the original eligibility or RR25 result.

Reports are generated at `reports/options_expiry_pilot.md` and `.json`; health shows the pilot's
activation, collection heartbeat and closed capture coverage. `streams/market-studies/options-v2/paused.json`
pauses its collection; the existing global `streams/market-studies/v1/paused.json` also applies.
Verification and reporting continue while paused. Missed hourly opportunities remain visible.

Use `python -m research_tools.options_pilot prepare|confirm|collect` and `python options_pilot_report.py` only through the
main-branch workflow (the production guard enforces this). Test fixtures use temporary roots and
fake public responses. No private API, order placement or trading credential is needed. Do not
promote a feature based only on improved usability: horizons and repeated contracts are dependent,
and predictive validity requires a separately registered experiment.

## November repair and portable replay

`range_source_repair.py refit` is the range workflow's operational entry point. The forecasting code,
model specification, prior fits and prospective decisions are unchanged. The reviewed source bundle
`research_tools/fixtures/november_2026_source_repair.json` retains the October archive ZIP and provider
checksum, historical API response, DVOL responses, response hashes, headers and actual retrieval clocks.
It admits only the six missing BTCUSDT four-hour bars on October 28, 2026 (the first registry entry). All 12 neighboring bars must
match archive OHLC, volume, taker-buy volume and clocks exactly; malformed, duplicate, conflicting or
incomplete replacements are rejected. The existing DVOL contract still applies. Raw evidence and the
complete October training delta are retained as content-addressed files before the frozen November
refit runs. This repairs historical training inputs; it does not manufacture forecasts for missed slots.

The **Range source readiness (daily)** workflow (repo 2.30.8) checks closed archive history every day: the
current month through yesterday, and the whole previous month on days 1-3. It lists missing bar timestamps and
separates four results: `ready`; `ready-unpublished-tail` (only whole trailing days, at most three, are not yet
published - the frozen refit fills such a tail from closed live bars); `ready-approved-repair` (the only holes are
gaps listed in the registry); and `blocked` (an unapproved interior gap, a partial day, a missing file before a
published one, or any file state other than ok, missing or incomplete - a failed retrieval blocks, it never
passes). Only `blocked` fails the workflow. It has read-only permissions and never fills a gap. A manual run takes
an `as_of` time for a rehearsal and reads the ref it was dispatched on. The normal refit also prints missing
timestamps before passing control to the existing archive/tail admission rules.

Approved gaps live in `research_tools/source_repairs.json` (repo 2.30.8). An entry names the first missing 4h open
and the number of bars, and pins its evidence file by sha256. The approved shape is fixed in code: at most six
consecutive bars, at least one day inside a single month, the checksum-matched monthly archive complete except for
that gap, and six exact-match API bars on each side. Anything else is refused. To add a gap: run **Range source
repair evidence capture** with the gap's first open and bar count; it captures and replays the evidence and pushes
it to a `repair-evidence/...` branch, never to main. Read the evidence, then add the registry entry by pull
request - that merge is the approval. Evidence can only be captured after the provider publishes the gap month's
monthly file (October 2026's appeared about 33.5 hours after the month ended), so the forecasts between the month
start and the merged repair are still lost. Record: `docs/incidents/2026-11-01-range-refit-outage.md`.

The existing expiry pilot now reports through `python options_pilot_report.py`. Its frozen preparation,
collection and confirmation modules remain unchanged. Replay allows absolute error at most `1e-12`,
with no relative tolerance, only for candidate call/put implied volatilities. State v2 replay applies the
same bound only to Brier losses and their primary difference. Keys, types, raw hashes, outcome paths,
timestamps, eligibility, chosen contracts, rounded RR25 and book values remain exact. Nonfinite values,
booleans masquerading as numbers, material changes and additional/missing fields fail verification.

Health verifies v1, state v2, each separate options pilot, immediate-book diagnostics and source quality
as independent components. Failure discards that component's partial output and keeps overall integrity
failed; other verified sections still refresh. Source incidents persist when their own verification
succeeds. Published-report freshness shows each last successful report clock separately from the current
health clock, so a new health report cannot conceal stale results.

## Separate 30-day maturity experiment

[`research_tools/options_30d/protocol.json`](../research_tools/options_30d/protocol.json) compares
**nearest eligible expiries within 45 days** against **nearest eligible expiries within 90 days**, only
for the 30-day target. Both arms use the same frozen leg filters, total-variance interpolation and a
35-day maximum span. There is no extrapolation. For example, November 27 and December 25 bracket a
30-day target in early November, but the latter lies beyond the original 45-day limit.

This is a feasibility test designed after seeing earlier coverage, not a retrospective confirmation.
Its `streams/market-studies/options-30d-v1/` registration binds its own implementation, shared frozen
dependencies and numerical tolerance. It starts at the next UTC hour after registration and exact code
are observed on main. Earlier captures cannot enter its denominator. The original 7d/30d pilot continues
unchanged and its observations are never pooled with this one. Both controls use the first capture of
each scheduled hour; missed hours, gains, losses, joint usability and spans remain visible.

The workflow runs `python -m research_tools.options_30d prepare|confirm|collect|report` with the main-only
production guard. Reports are `reports/options_30d_pilot.md` and `.json`. Its own
`streams/market-studies/options-30d-v1/paused.json`, or the global v1 pause, stops collection while
verification and reporting continue. Merge permits registration; the activation record proves launch.

## Timing and evidence progress

After saving each hourly options source, the collector captures the union of selected contracts from
both pilot definitions before moving to slower forward sources. These additional diagnostics live in
`data/options/selected_contract_books/`, separate from both pilots' original book measurements. They
retain the exact source capture and hash, selection clock, raw book responses and request/receipt clocks.
They use the same 16-contract, four-worker, 12-second-request and 60-second-batch limits. A collector
with less than 65 seconds of remaining stage/run budget records a skip. Errors remain visible in the
ordinary options capture, and health counts source captures without book records. Collection failures
do not discard the already saved source quotes.

Health reports selected, attempted and usable books, missing/budget-skipped records, and median/p90
source-to-book delay. The original pilot also collects earlier in the studies workflow and reports
lag quantiles. These remain later measurements: even a faster book cannot prove size at an earlier
source quote timestamp. No latency prediction experiment or subminute performance claim is launched.
The paired-flow minute-clock equality and overlapping-window diagnostics explain that limitation.

State v2 health shows scored observations against the frozen 1,680-observation minimum for intervals,
168-observation block equivalents, and its 180-day review date. Block equivalents are not independent
samples or a reason to retune. Neither reaching the interval threshold nor an early ranking promotes a model.
