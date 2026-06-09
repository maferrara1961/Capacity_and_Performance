import unittest

from CapacityEngine.Application.SyntheticDataService import SyntheticDataService
from CapacityEngine.Scheduler.DailyCapacityRun import RunDailyCapacity


class ExecutiveCapacityFlowTest(unittest.TestCase):
    def test_daily_run_feeds_executive_outputs(self):
        Run = RunDailyCapacity()
        self.assertEqual(Run.ProcessedResourceCount, 1)
        self.assertTrue(Run.Forecasts[0].Forecast90Days >= Run.Forecasts[0].Forecast30Days)

    def test_critical_synthetic_data_feeds_executive_decision_state(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("ExecutiveCritical001", "critical", "small", 90, 1)
        self.assertTrue(any(Risk["OverallRisk"] == "Critical" for Risk in Dataset["Risks"]))
        self.assertTrue(all(Forecast["DaysToSaturation"] <= 90 for Forecast in Dataset["Forecasts"]))
        self.assertTrue(any(Recommendation["Priority"] == "High" for Recommendation in Dataset["Recommendations"]))


if __name__ == "__main__":
    unittest.main()
