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

Use `python -m research_tools.options_pilot prepare|confirm|collect|report` only through the
main-branch workflow (the production guard enforces this). Test fixtures use temporary roots and
fake public responses. No private API, order placement or trading credential is needed. Do not
promote a feature based only on improved usability: horizons and repeated contracts are dependent,
and predictive validity requires a separately registered experiment.
