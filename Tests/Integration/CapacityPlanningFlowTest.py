import unittest

from CapacityEngine.Application.SyntheticDataService import SyntheticDataService
from CapacityEngine.Scheduler.DailyCapacityRun import RunDailyCapacity


class CapacityPlanningFlowTest(unittest.TestCase):
    def test_daily_run_produces_planning_fields(self):
        Run = RunDailyCapacity()
        Kpi = Run.Kpis[0]
        Forecast = Run.Forecasts[0]
        self.assertIsNotNone(Kpi.MonthlyGrowthRate)
        self.assertIsNotNone(Forecast.Forecast60Days)

    def test_mixed_profile_feeds_planning_fields(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("PlanningMixed001", "mixed", "small", 90, 1)
        self.assertTrue(Dataset["Services"])
        self.assertTrue(Dataset["Resources"])
        self.assertTrue(any(Kpi["HeadroomAvailable"] >= 0 for Kpi in Dataset["Kpis"]))
        self.assertTrue(any("Forecast90Days" in Forecast for Forecast in Dataset["Forecasts"]))


if __name__ == "__main__":
    unittest.main()
