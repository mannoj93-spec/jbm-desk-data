"""State v1 abstentions are a warning only while state-v2 forecast the same hours (market_study_ops, proposed 2.30.13)."""
import unittest

import market_study_ops as M


def opp(slot, state="abstained", recorded=True):
    return {"slot": slot, "state": state, "recorded": recorded, "forecast_state": state if recorded else None}


class Superseded(unittest.TestCase):
    def test_recorded_abstentions_covered_by_v2_are_superseded(self):
        self.assertTrue(M.state_v1_superseded([opp(1), opp(2)], {1, 2, 3}))

    def test_anything_else_still_alerts(self):
        v2 = {1, 2, 3}
        self.assertFalse(M.state_v1_superseded([], v2))                                   # nothing missed: nothing to excuse
        self.assertFalse(M.state_v1_superseded([opp(1), opp(2, "no-run", recorded=False)], v2))   # v1 did not run
        self.assertFalse(M.state_v1_superseded([opp(1), opp(2, "late-publication")], v2))  # v1 ran and was late
        self.assertFalse(M.state_v1_superseded([opp(1), opp(4)], v2))                      # v2 missed that hour too
        self.assertFalse(M.state_v1_superseded([opp(1), opp(2)], set()))                   # v2 absent, paused or unreadable

    def test_only_the_state_study_can_be_excused(self):
        src = open(M.__file__).read()
        self.assertEqual(src.count("if kind == 'state' and state_v1_superseded("), 1)
        self.assertIn("out['alerts'].append(f'{kind}: {n} consecutive closed opportunities missed')", src)


if __name__ == "__main__":
    unittest.main()
