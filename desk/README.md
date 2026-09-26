# desk/ — the crypto desk's range forecaster

The automated half of the crypto-desk skill package. It forecasts the size of the next move in BTC,
not its direction, and registers every forecast before its window opens. Release identity (package,
contract, module and artifact hashes, calendar, routing, stream start) lives in `release.json`, written and
checked by `make_release.py`; verified deployment events are appended to `deployments.jsonl`.

| File | What it is |
|---|---|
| `range_model.py` | The model, **range-11.1.0**, byte-frozen at the O21 specification `ae6aa254c786…`. Never edited; a new model is a new specification. |
| `range_contract.py` | **The forecast contract** shared by evaluation, registration, reading and scoring: window rule, calendar terms, point (the OLS value, never the residual median), quantiles, baseline, coherence (reported, not applied), losses, maturity-bounded splits, fit validation, input admissibility. Contracts `RC1` (what O21 evaluated) and `RC1D` (the automated prospective variant). |
| `range_job.py` | `refit` · `forecast` · `confirm` · `score` (hourly, `range-score.yml`) · `status` · `replay <id>` (below). |
| `range_reader.py` | The reading contract, **as of** a time (12.2): only records whose decision, preparation, registration and publication confirmation are at or before `now` are readable; the newest governs; verifies frozen bytes and the strict RC1D checks, applies the shared `range_contract.eligibility`; returns `valid-current`, `stale`, `missing`, `unregistered`, `ineligible` or `integrity-failed` — never raises. A forecast expires at decision + 4h + 75 min, capped at its window end; `revalidate(result, now)` applies the same rule to a cached result, and returns `unavailable` before the record existed. Writes `reports/range_status.json` (generation and expiry time, due vs current decisions, run failures, per-horizon scoring states). |
| `range_ops.py`, `range_monitor.py` | The run lifecycle log (`state/range_runs.jsonl`: stage, outcome, reason for every run, including failures before forecasting) and the read-only stream monitor (`range-monitor.yml`). Both stdlib only and independent of the forecasting code. |
| `retained.py` | Verified access to retained bytes: the O21 root inputs (manifest-checked, shared by replay and the refit chain) and calendar versions by content hash (current file, `calendars/`, or Git history). |
| `jbm_archive.py`, `jbm_measure.py` | The desk's validated loaders and measurement functions (archive-12.0.0, measure-11.1.0). |
| `releases_2020_2026.csv`, `calendars/` | Sourced CPI/NFP/PPI/FOMC release times through Dec 2026 (actual times; announcement vintages not retained). Every version a forecast used is kept as `calendars/<sha256>.csv`. |
| `fits/YYYY-MM.json` | One fit per month, validated before every use (`range_contract.validate_fit`). Monthly parameters; not the contract. |
| `inputs/` | Retained, content-addressed input bundles: one per forecast decision (`inputs/YYYY-MM/`), one delta per refit (`inputs/refit/`). |
| `research/` | O21's retained inputs, original results, the 12.0 reanalysis and its 12.1 Holm addendum (`o21_reanalysis.py replay|reanalysis|verify`). `verify` (12.2) is a gate with two separate checks: exact integrity of the stored artifacts against their recorded hashes, and numerical equivalence of a fresh rerun — summary and every row, per value within abs/rel 1e-9, categorical values exact; rerun serialization hashes are reported, not required; exit 1 integrity, 2 numerical. The reanalysis reproduces the preserved ten-test procedure; the complete thirteen-comparison family in the addendum is the declared family for a future study, not a new result on these data. |
| `release.json`, `deployments.jsonl` | Release identity (versions, hashes, contract, calendar, artifacts, routing, stream start), checked by `make_release.py`; the append-only log of verified deployment events. Live health is `reports/range_status.json`. |
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
remaining range once the window has started — and only while now < its `valid_until_utc` on the reader's own
clock. The file states its `generated_utc` and `status_expires_utc`.

**Scoring.** `scoring.py` (scoring-2.5) scores RC1D events with `range_contract.losses` on the point, and
only if registration and publication confirmation both preceded the window start (`range_contract.eligibility`,
shared with the reader). Range forecasts are scored hourly (`range-score.yml`) once their window has ended plus
a five-minute buffer, from complete Binance BTCUSDT perpetual 1m coverage retained as evidence; missing data
stays pending. Legacy 2.14 records (`range-b2-*`) are scored
on q50 as registered and are never cited as current.

**Monthly fit (12.1).** The history is the retained chain (the O21 root, hash-verified, plus every refit delta,
each verified before any is used) and the days since. Only an unpublished *trailing* archive segment is filled,
from closed, validated live bars that must match the archive on an overlap of up to six bars; an interior gap, a
conflicting overlap, a malformed or unclosed bar, or an unavailable live source stops the refit. The filled tail's
provenance is kept in the delta.

