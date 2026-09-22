# Validation record — reliability revision 2.1

Validated locally on 2026-09-22 with Python 3.12.14.
GitHub workflows select Python 3.12. The project uses the standard library at runtime.

| Check | Result |
|---|---|
| Numerical fixture checks | 25 passed |
| Offline regression tests | 50 passed |
| Python module compilation | Passed |
| Bash persistence script syntax | Passed |
| All four workflow YAML files | Parsed; queue guards checked |
| Registration-only CLI in an empty isolated project | Passed |
| Report generation against supplied data | Passed |
| Original stored data byte comparison | All 49 data files unchanged |

The regression suite exercises malformed/nested schemas; non-finite numbers; default
start times; empty/gapped/duplicate prices; missing and partial predicate series; close-time
semantics; flat leans; race bounds; retryable scoring; retained evidence; tampered evidence;
immutable forecast inputs; strict registration timing; dependency registration; corrupted
state; failed atomic replacement; idempotent appends; partial/failed/page-capped history;
DVOL grids; point-in-time views; mature episodes; push exhaustion; owner checks; and
acknowledgement ordering. A failed forecast is isolated from another valid forecast.

The generated report explicitly identifies the supplied taker-series gaps, three legacy
DVOL duplicates, current snapshot errors in the supplied capture, and the absence of GitHub
runner evidence. Original report copies are preserved under reports/legacy/.

## Scope limits

No live exchange requests, GitHub workflow executions, remote repository updates, or
notification deliveries were performed during this revision. External availability,
exchange response semantics, Actions permissions, and deployment must be checked on your
runner. Mocked network/process failures validate local handling, not live service behavior.
YAML parsing does not replace GitHub's workflow validator. This is a reviewed reliability
revision, not a claim of audited trading performance or guaranteed production uptime.

## Reproduce

```sh
python test_fixtures.py
python -m unittest discover -s regression -v
python report.py --days 7
```

If registered forecasts have matured, report generation may fetch exchange prices. The
fixture and regression commands run offline. See README.md for installation and migration.
