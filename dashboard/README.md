# JBM Research Desk

A read-only, terminal-inspired dashboard for the existing research pipeline. Near-black surfaces,
amber navigation, tabular numbers, and compact panels give the desk a finance-oriented hierarchy.
The optional light theme and saved page/chart selections stay in the browser.

## Local preview

From the repository root, with Python 3.12 or newer:

```sh
python scripts/build_dashboard.py
python -m http.server 8765 --bind 127.0.0.1 --directory .dashboard-build
```

Open http://localhost:8765. There is no dependency install, API key, database, or frontend build tool.
The browser reads only the generated `data.json` alongside the static assets. Do not open `index.html`
with `file://`; use the HTTP preview so browser modules and the snapshot can load.

## Views

- **Overview:** actual recorded BTC prices, descriptive model comparisons, expiring forecast monitor,
  research watchlist, and review items. The chart aggregates stored minute bars into hourly OHLC;
  missing hours are not filled and partial hours remain labeled in the tooltip.
- **Range forecasts:** full-window range quantiles and their decision-close USD equivalents. These
  are range magnitudes, not upper/lower price targets or remaining-range estimates.
- **Research lab:** current-version evidence cards only, search/status filters, checkpoint progress,
  and an accessible detail dialog. Required integrity and publication validity stay distinct.
- **Data health:** searchable source coverage, sortable availability, report-cutoff statuses, and
  observation ages recomputed on the viewer's clock.
- **Paper desk:** actual PS1 lifecycle and evidence status, with B2/B1 paired comparisons. No invented
  P&L series or simulated results are created by the dashboard.
- **Reports & audit:** commit-pinned reports and an exportable SHA-256 source manifest.

CSV exports follow the active view and filters. Negative numbers and spreadsheet formula prefixes
are escaped in CSV so source labels cannot execute formulas. No missing numeric value is shown as zero.

## Publishing with GitHub Pages

1. Merge the dashboard pull request.
2. In repository **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source.
3. Run **Research dashboard** from Actions if the initial run happened before Pages was enabled.
4. The project URL is `https://mannoj93-spec.github.io/jbm-desk-data/`.

The workflow validates pull requests without deploying them. On main it publishes after relevant
research workflows, on dashboard code changes, every 30 minutes as a fallback, or manually.
It never writes to the source repository, collectors, registrations, scores, or research state.
Existing production workflows are unchanged. Workflow completion builds always check out trusted main;
they do not consume triggering workflow artifacts or execute PR code with deployment permissions.

The public build contains summaries of already-public repository data. This is a snapshot dashboard,
not a streaming terminal. Refresh reloads the latest published snapshot; publication may lag a
collector run. A failed build leaves the last deployed snapshot in place, with its original timestamps.

## Data contract and safety of interpretation

`scripts/build_dashboard.py` reads one checkout and copies the static assets into `.dashboard-build/`.
It preserves structured report values, keeps only current research versions from the evidence index,
and records each source hash plus the checkout commit. The coverage report currently has no JSON twin;
its named Markdown tables are parsed strictly. A changed or missing table fails the build instead of
publishing misleading empty values. The dashboard does not change research version hashes.

Forecast availability is checked against the report expiry, each row's valid-until timestamp and
window end on every clock tick. Unknown clocks/expiry metadata cannot produce a current label.
Clocks are named, aged on the viewer's clock and judged one by one (repo 2.23; `CLOCKS` in `model.js`, the same
table as the skill's runbook D2): stream reports are stale after 8 h by generation; the companion's observation cutoff
(latest included outcome-window end) after 12 h; PS1's after 8 h while collecting (null before launch is expected,
not a failure); research evidence by its cards' observation cutoffs after 12 h, never by the index update or the
build time. The range report keeps its exact expiry. The paper view shows PS1 integrity state, ledger-row accounting
and excluded decisions, and the companion's integrity and withheld horizons; withheld or unavailable states are
exported to CSV as such, and an available interval is shown even without explanatory text.

A refresh is staged: the candidate snapshot is validated field by field and rendered in every view before it
replaces the last good one, so a failed or malformed refresh leaves the previous snapshot usable and the failure flag
stays on screen across navigation until a refresh succeeds. Actions run on node24 (setup-node v6, upload-pages-artifact
v5, deploy-pages v5); upload-pages-artifact v5 excludes dotfiles, so `.nojekyll` is not uploaded (Pages deployments
from Actions do not run Jekyll). Workflow success remains **unverified** with a link to Actions:
a successful dashboard build is not evidence of upstream workflow success.

## Checks

```sh
python -m unittest regression.test_dashboard -v
node --test dashboard/model.test.mjs
node --check dashboard/app.js
```

Browser QA should cover all six views at desktop/mobile widths, theme persistence, search/filter,
CSV download, keyboard modal dismissal, stale/expired states, and fetch failure/retry. The project
uses no third-party client libraries or remote font requests.
