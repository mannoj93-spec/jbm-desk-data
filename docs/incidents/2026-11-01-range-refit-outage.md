# Range forecasts lost at the November month boundary

Recorded 2026-11-11 from the repository's own records (`state/range_runs.jsonl`, `desk/inputs/`,
`research_tools/fixtures/november_2026_source_repair.json`) and from the provider's archive as read that day.

## What happened

Thirty-four consecutive production range decisions, 2026-11-01T00:00:00Z through 2026-11-06T12:00:00Z, published
no forecast. Every terminal run record for those decisions is `failed` with reason `refit failure`: the first run
of November ([41255702819](https://github.com/mannoj93-spec/jbm-desk-data/actions/runs/41255702819)) passed its
preflight and failed at the refit stage at 00:18:13Z, and the forecast stage was skipped. Forecasting resumed at the
2026-11-06T16:00:00Z decision (run
[42250164694](https://github.com/mannoj93-spec/jbm-desk-data/actions/runs/42250164694)), the first decision after
PR #62 merged at 16:09:21Z as `8f5a879a`.

The November fit needed a contiguous October history. The provider's October archive lacked the six BTCUSDT 4h bars
of 2026-10-28, and the frozen refit refuses an interior gap. The monthly October file retained in the repair
evidence carries `Last-Modified: Mon, 02 Nov 2026 09:34:38 GMT`, so for the first 33 hours of the outage the refit
was reading daily files and a live tail; that it failed from the first decision is consistent with the gap already
being present in the daily files, which the records do not state directly.

## Consequences

- The 34 decisions are missed and stay missed. Nothing was backfilled.
- The market studies that depend on the range forecast lost the same opportunities: at 2026-11-11T03:15Z the
  turnover and range-calibration studies stood at 68 and 62 on-time of 104. Turnover's first support review requires
  at least 80% execution coverage.
- The repair (repo 2.30.7) admitted only that gap, through constants in `range_source_repair.py`.

## Later evidence (2026-11-11)

Read from this repository's code against the live archive on 2026-11-11 at about 16:00Z:

- The provider has republished October. The monthly file now validates as `ok` with 186 bars and a matching
  checksum (`Last-Modified: Wed, 11 Nov 2026 10:50:21 GMT`, sha256 `dd6994c7...`; the retained file is
  `64c47c73...`). The daily 2026-10-28 file is `ok` with six bars (`Last-Modified: Wed, 11 Nov 2026 05:41:27 GMT`).
- All 186 bars of the retained, repaired October delta (`a681d33d...`) equal the republished archive on open, high,
  low, close, volume, taker-buy volume, close time and availability time: 0 field differences. The six bars taken
  from the API on November 6 are the bars the provider later published.
- November 1-10 daily files: `ok`, no missing 4h opens.

A provider file can be rewritten; the hash in the retained evidence identifies the bytes the November fit used and
does not depend on what the provider serves now.

## Changes (repo 2.30.8)

- The readiness check runs its real check every day (month to date; the whole previous month on days 1-3) instead
  of only around the boundary, so an interior gap is reported the day after it appears. Before this revision the
  check had run five times (Nov 7-11) and returned `outside-month-boundary-window` each time.
- Approved gaps are listed in `research_tools/source_repairs.json`; the repair code takes its dates from the entry.
  A new gap of the same shape needs captured evidence and a reviewed registry entry, not new code.
- `range-repair-capture.yml` captures that evidence from a phone and pushes it to a review branch.

## Not established

- Why the provider's October files lacked the bars, and when the daily file first became complete.
- Whether a repair can be staged before the gap month's monthly archive is published. The approved rule requires
  the checksum-matched monthly file; October's was published about 33.5 hours after the month ended, so a gap in a
  future month still costs the decisions between the month start and that publication plus review.
