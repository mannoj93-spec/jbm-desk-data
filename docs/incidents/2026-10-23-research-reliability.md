# Research reliability corrections — October 23, 2026

## Production trigger

Research-streams runs including 39988894950 failed preflight after a lab run exhausted its 1,200-second budget.
The retained H1 card at commit 27ce3dd61a2dfdc719cf59b83c327bcd55a34245 legitimately omitted complete-evaluation
fields. Feasibility indexed registered_at, and the source identity test indexed dependencies. Both crashed,
preventing independent paper/companion stages from running. The original card is retained as a regression fixture.

An unavailable attempt now retains its reason without counts, rates or ETA. Earlier last_valid_result data is never
promoted into the current attempt. PS1's protocol, calibration and source-integrity gates remain enabled.
The lab schedules the slow account scan last and has 2,400 seconds of budget within a 50-minute job. This mitigates
the observed runtime; it is not a hard per-design timeout. If a scan grows beyond that headroom, the job may still
need separate per-design workers. No detector cache or rule change has been hidden from evaluation versioning.

## Evaluator and replay

The evaluator reads the verified hypothesis object before using disclosure settings. A modified convenience copy
is refused. Hash-chain/anchor limitations are unchanged: deploying the evaluator under a separate OS identity is
still required for a genuine researcher/evaluator boundary; this patch does not commission that service.

Requests are limited to 65,536 bytes and five seconds of total receive time, with per-connection error isolation.
Only simple experiment identifiers and SHA-256 candidate identifiers can reach result paths.

RC1D replay accepts a maximum 1e-12 relative/absolute difference only for finite floating-point feature values.
Input bytes are still verified by SHA-256; non-feature metadata, keys/types, forecast events and both window ends
remain exact. The returned replay metadata distinguishes exact and numerical matches. No retained bundle is edited.

## Recovered observations

| Run | Artifact | Verified SHA-256 | Absent rows preserved | Superseded rows |
|---|---|---|---:|---:|
| 39420444969 | 12263109593 | 91fc688c6ebd932a252ba1e64fb34f5d1ef5c4a18250e48e4f0ec4c327807dc7 | 8 | 29 |
| 39980548198 | 12513437522 | c3d107aa85cd15344f2b46d50ce9d88e334071232144eb5bf4398f9c780910ff | 7 | 56 |

The existing restore tool compared archive rows against base 3343e123, preserved absent observations byte-for-byte
under data/restored/collector-<run>/, and appended receipts. It did not restore working state or overwrite live rows.
These remain late recoveries, excluded from live inputs and historical coverage. Original ZIPs were also downloaded
locally before their October 27 and October 30 expiry dates.

## Validation

- Python 3.12.14 on macOS: 90 final research API/evaluator regressions passed (one OS-user isolation test skipped
  because the process is not root); 406 desk regressions passed (one skipped), plus both replay tests after adding
  the numerical-boundary case. The earlier 119-test API/publication/integrity run also passed (one skipped).
- Local persistence-shell testing was stopped because GNU timeout is unavailable on macOS; Ubuntu CI is required
  for the complete suite. No local full-suite pass is claimed.
- Production replay on base 3343e123: 474/474 forecasts pass; 465 exact rebuilt bundles, nine with float roundoff.
- All eight lab evaluation versions match the baseline. The reviewed code-identity fixture records the runner-only
  source change separately from evaluation identities.
- Full Ubuntu regression validation runs through the PR's required release dependency. Local results and final CI
  status are reported on the pull request; this document does not claim a production deployment or restored cadence.

No new experiment was registered. Account-detector optimization, new data feeds and experiment variants still require
an explicit version/protocol change. Existing data gaps were not backdated or filled with synthetic observations.
