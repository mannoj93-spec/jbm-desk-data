# desk/ — the crypto desk's range forecaster

The automated half of the crypto-desk skill package. It forecasts the size of the next move in BTC,
not its direction, and registers every forecast before its window opens. Release identity (package,
contract, module hashes, calendar, routing, deployment evidence) lives in one file: `release.json`,
written and checked by `make_release.py`.

| File | What it is |
|---|---|
| `range_model.py` | The model, **range-11.1.0**, byte-frozen at the O21 specification `ae6aa254c786…`. Never edited; a new model is a new specification. |
| `range_contract.py` | **The forecast contract** shared by evaluation, registration, reading and scoring: window rule, calendar terms, point (the OLS value, never the residual median), quantiles, baseline, coherence (reported, not applied), losses, maturity-bounded splits, fit validation, input admissibility. Contracts `RC1` (what O21 evaluated) and `RC1D` (the automated prospective variant). |
| `range_job.py` | `refit` · `forecast` · `confirm` · `status` · `replay <id>` (below). |
| `range_reader.py` | The reading contract: resolves the manifest, verifies frozen bytes, returns `valid-current`, `stale`, `missing`, `unregistered`, `ineligible` or `integrity-failed`; writes `reports/range_status.json`. |
| `jbm_archive.py`, `jbm_measure.py` | The desk's validated loaders and measurement functions (archive-12.0.0, measure-11.1.0). |
| `releases_2020_2026.csv` | Sourced CPI/NFP/PPI/FOMC release times through Dec 2026 (actual times; schedule vintages not retained). |
| `fits/YYYY-MM.json` | One fit per month, validated before every use (`range_contract.validate_fit`). Monthly parameters; not the contract. |
| `inputs/` | Retained, content-addressed input bundles: one per forecast decision (`inputs/YYYY-MM/`), one delta per refit (`inputs/refit/`). |
| `research/` | O21's retained inputs, original results, and the 12.0 reanalysis (`o21_reanalysis.py replay|reanalysis`). |
| `test_*.py`, `fixtures/` | Offline tests; also run by `regression/test_desk_range.py` and before every forecast. |

**Contract RC1D (what gets registered).** At each 4H close D, inputs are cut at D (closed bars; DVOL
at its candle close). The window starts at S, the first five-minute boundary at least five minutes after
the forecast was prepared, and runs S→S+h for h = 4h, 24h, 72h; the calendar terms describe that window.
Three forecasts `range-rc1d-<h>-<D>`, each with a B2 event and a B0 persistence event carrying `point`
(the loss-bearing forecast, lr units) and `q10/q50/q90`. RC1D has no historical evaluation: O21's result
belongs to RC1 (window starting at D). The difference is the few minutes of offset and the calendar terms.

**Registration is one transaction.** `forecast` validates the whole batch against one freeze time, writes
the frozen bytes, then the manifest in one atomic write (the commit point), then the source files
(rolled forward from frozen bytes if lost). Any failure before the commit point removes what it wrote.
Every attempt is logged in `state/range_attempts.jsonl` (`skipped`, `failed`, `abandoned`, `prepared`,
`frozen`, `published`, `published-late`, `unconfirmed`); a decision whose earlier attempt recorded a window
is never retried, so no window moves. **Eligibility** needs two things before S: the local freeze and the
remote confirmation (`confirm`: `git fetch`, the manifest entries and hashes on `origin/main`), recorded in
`state/range_publications.jsonl`. The workflow's code commit is not the publication commit; both are recorded.

**Reading.** A thread reads `reports/range_status.json` (or runs `range_reader.py` on a clone). Only
`valid-current` is citable, as a full-window forecast with its ID and window — never as a forecast of the
remaining range once the window has started.

**Scoring.** `scoring.py` (scoring-2.3) scores RC1D events with `range_contract.losses` on the point, and
only if publication was confirmed before the window started. Legacy 2.14 records (`range-b2-*`) are scored
on q50 as registered and are never cited as current.
