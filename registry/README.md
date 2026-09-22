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

Public issues are public before validation. The schema is not a private-information filter.
See the root README for limits, score semantics, legacy migration, and operating instructions.
