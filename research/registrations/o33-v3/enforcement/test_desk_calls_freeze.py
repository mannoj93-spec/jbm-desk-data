"""Tests for desk_calls_freeze: the frozen v3 bytes and constants, and the freeze-time cohort gate."""
import unittest

import desk_calls as D
import desk_calls_freeze as F


class FreezeTests(unittest.TestCase):
    def test_module_bytes_and_constants_are_the_frozen_ones(self):
        self.assertEqual(F.frozen_ok(), [])

    def test_a_changed_constant_is_detected(self):
        saved = D.V3_LOOKBACK_DAYS
        D.V3_LOOKBACK_DAYS = 1095                     # what a fresh-context run showed slipping past the spec pin
        try:
            self.assertIn("V3_LOOKBACK_DAYS = 1095, frozen 730", F.frozen_ok())
        finally:
            D.V3_LOOKBACK_DAYS = saved

    def test_cohort_gate_at_the_freeze_second(self):
        self.assertEqual(F.v3_cohort("2026-10-07T23:07:55Z"), "pre-freeze")
        self.assertEqual(F.v3_cohort("2026-10-07T23:07:56Z"), "pre-freeze")      # strictly after the freeze
        self.assertEqual(F.v3_cohort("2026-10-07T23:07:57Z"), "v3")
        self.assertEqual(F.v3_cohort("2026-10-07T22:00:00Z"), "pre-freeze")      # registration_status alone said eligible
        self.assertEqual(F.v3_cohort(None), "unregistered")
        self.assertEqual(D.registration_status({"version": 1}, "2026-10-07T22:00:00Z", True)[0], "eligible")


if __name__ == "__main__":
    unittest.main()
