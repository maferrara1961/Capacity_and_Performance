import unittest

from CapacityEngine.Scheduler.DailyCapacityRun import RunDailyCapacity


class ExecutiveCapacityFlowTest(unittest.TestCase):
    def test_daily_run_feeds_executive_outputs(self):
        Run = RunDailyCapacity()
        self.assertEqual(Run.ProcessedResourceCount, 1)
        self.assertTrue(Run.Forecasts[0].Forecast90Days >= Run.Forecasts[0].Forecast30Days)


if __name__ == "__main__":
    unittest.main()
