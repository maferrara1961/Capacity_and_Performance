import unittest

from CapacityEngine.Scheduler.DailyCapacityRun import RunDailyCapacity


class CapacityEngineContractTest(unittest.TestCase):
    def test_successful_run_produces_required_outputs(self):
        Run = RunDailyCapacity()
        self.assertEqual(Run.Status, "Succeeded")
        self.assertEqual(len(Run.Kpis), 1)
        self.assertEqual(len(Run.Forecasts), 1)
        self.assertEqual(len(Run.Risks), 1)
        self.assertGreaterEqual(len(Run.Recommendations), 1)


if __name__ == "__main__":
    unittest.main()
