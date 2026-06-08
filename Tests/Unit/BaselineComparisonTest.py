import unittest

from CapacityEngine.Application.CapacityCalculator import CapacityCalculator


class BaselineComparisonTest(unittest.TestCase):
    def test_baseline_delta(self):
        self.assertEqual(CapacityCalculator().BaselineDelta(50, 75), 25)


if __name__ == "__main__":
    unittest.main()
