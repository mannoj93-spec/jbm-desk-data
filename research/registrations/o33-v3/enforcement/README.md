# O33 v3 — enforcement addendum (added after the freeze; does not change v3)

Fresh-context runs on package 12.4.13 found two gaps in how the freeze was enforced: the frozen-spec test pinned the
V3 text but not its numeric constants, and the "only receipts after the freeze count" rule existed only in text.
Neither changes v3. The frozen files in the parent folder are untouched (their sha256 in `registration.json` still
hold); these two files only check them:

- `desk_calls_freeze.py` (calls-freeze-1.0.0): `v3_cohort(receipt)` returns `v3` only for a registry receipt
  strictly after 2026-10-07T23:07:56Z; `frozen_ok()` compares `desk_calls.py` and `test_desk_calls.py` bytes and
  every V3 constant with the registered values.
- `test_desk_calls_freeze.py`: the frozen bytes and constants, a changed lookback detected, the gate at the freeze
  second and one second either side.

Run from a folder holding these with the parent folder's `desk_calls.py` and `test_desk_calls.py`.
