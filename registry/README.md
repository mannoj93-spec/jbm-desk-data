# Forecast registry

Copy `_TEMPLATE.json`, set future UTC dates, and choose a new ID. Run:

```sh
python intake.py --check registry/your-forecast.json
```

Phone intake fills a missing start with the next five-minute boundary. Files committed
directly must supply start and instrument. All routes use `schema.py`; check mode also
requires the start to be in the future.

The collector freezes exact bytes in `registry/frozen/` and indexes them in
`state/forecast_manifest.json`. Registration must be strictly earlier than start.
An edited or deleted source file does not change the registered forecast. IDs are
write-once. `scores.jsonl` and `evidence/` retain completed results and observations.
Do not manually modify frozen files, receipts, scores, or manifests.

Missing data remains unscorable and retryable. A price interval is `[start, horizon)`.
Snapshot series (ratios, OI) are read at their stamp; interval series (taker volume, candles,
DVOL) at their close — see `schema.SERIES_KIND` and the root README. Machine predicates support
only fixed-cadence names and fields in `schema.SERIES`. `range` events take q10/q50/q90 of
ln(high/low) over the forecast window. Manual predicates carry only type/name.
Settled funding predicates are not implemented.

Automated forecasts (desk range stream, repo 2.15): `range-rc1d-*` are registered by
`desk/range_job.py` as one batch per 4H close through `registration.register_batch`, with `start` at
least five minutes after preparation. Registration (the manifest entry) is local; prospective
eligibility also needs the publication confirmation in `state/range_publications.jsonl` before the
window starts. Read them through `desk/range_reader.py` or `reports/range_status.json`, never by listing
this folder: a file here is not a registration. `range` events may carry `point` (the loss-bearing
forecast under `desk/range_contract.py`); `range-b2-*` records (2.14) have none and are scored on q50.
Archival acceptance and scoring eligibility are distinct: a late record is kept and labelled, not scored.

Public issues are public before validation. The schema is not a private-information filter.
See the root README for limits, score semantics, legacy migration, and operating instructions.
