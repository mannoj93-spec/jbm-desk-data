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
