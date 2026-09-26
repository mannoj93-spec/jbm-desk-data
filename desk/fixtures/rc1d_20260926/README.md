# Fixture: the first two production RC1D batches (Sep 26 2026, 04:00Z and 08:00Z)

Byte copies of the six registered forecasts (frozen and source files), their manifest entries, attempt rows and
publication rows, taken from `main` at 365ff99. Immutable test data: the reader's as-of tests run against this
copy, never against the growing production registry. `test_asof.py` also checks, ID by ID, that these bytes
still equal the production registry's (hash and replay compatibility), when a repository checkout is present.
