# desk/ — the crypto desk's range forecaster

This folder is the automated half of the crypto-desk skill package (11.2). It forecasts the size of
the next move in BTC, not its direction, and registers every forecast before its window opens so the
record cannot be hand-picked.

| File | What it is |
|---|---|
| `range_model.py` | The range model, **range-11.1.0**. Must hash to the frozen O21 specification `ae6aa254c786…`; `range_job.py` refuses to fit or forecast otherwise. |
| `jbm_archive.py`, `jbm_measure.py` | The desk's validated loaders (Binance archive, 4H klines, DVOL) and measurement functions. |
| `releases_2020_2026.csv` | Sourced CPI / NFP / PPI / FOMC release times (UTC), through Dec 2026. Refresh before it runs out. |
| `range_job.py` | `refit` (monthly), `forecast` (every 4H close), `summary` (writes `reports/range.md`). |
| `fits/YYYY-MM.json` | One frozen fit per month: coefficients fitted on every target that closed before the month began. Never rewritten. |
| `test_*.py`, `fixtures/` | Offline tests (also run by `regression/test_desk_range.py` and before every forecast). |

**What gets registered.** For each 4H close, three forecasts — `range-b2-{4h,24h,72h}-<close>` —
each with two `range` events on the same window: the B2 model and the B0 persistence baseline.
Both are scored by `scoring.py` in the weekly report, so skill against persistence is measured
prospectively on identical windows. The window starts at the next five-minute boundary after
registration (the registry rule), a few minutes after the close the model was trained on; the offset
is written into each forecast's note, and a run more than an hour after the close does not forecast.

**What the model is.** B2: a regression of the log of the log range on recent ranges (last bar, 6,
42 and 180 bars), the weekend share of the window, the number of scheduled releases inside it, and
DVOL-implied volatility. In its one frozen test (O21: fit to Sep 2024, select on the next year, then
one never-fitted year) it beat persistence by 18% at 4h, 17% at 24h and 11% at 72h in mean absolute
log error, with 10–90 bands covering 81–85%. Its status is *exploratory, holdout-consistent*; these
registered forecasts are how it can earn more. It is never a direction or a probability of a touch.

**Changing it.** Any change to `range_model.py` breaks the frozen hash by design: a new model is a
new specification, tested and frozen again, with a new hash here and a new version in the skill
package. The skill package's copies of these modules must carry the same versions.
