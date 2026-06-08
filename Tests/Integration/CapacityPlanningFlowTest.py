import unittest

from CapacityEngine.Scheduler.DailyCapacityRun import RunDailyCapacity


class CapacityPlanningFlowTest(unittest.TestCase):
    def test_daily_run_produces_planning_fields(self):
        Run = RunDailyCapacity()
        Kpi = Run.Kpis[0]
        Forecast = Run.Forecasts[0]
        self.assertIsNotNone(Kpi.MonthlyGrowthRate)
        self.assertIsNotNone(Forecast.Forecast60Days)


if __name__ == "__main__":
    unittest.main()
