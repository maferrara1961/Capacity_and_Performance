from datetime import UTC, datetime, timedelta
import unittest

from CapacityEngine.Application.CapacityCalculator import CapacityCalculator
from CapacityEngine.Domain.Constants import MetricName
from CapacityEngine.Domain.Entities import MetricSample


class CapacityCalculatorTest(unittest.TestCase):
    def setUp(self):
        self.Calculator = CapacityCalculator()

    def test_average_peak_p95_headroom_growth_and_saturation(self):
        Values = [10, 20, 30, 40, 95]
        self.assertEqual(self.Calculator.Average(Values), 39)
        self.assertEqual(self.Calculator.Peak(Values), 95)
        self.assertEqual(self.Calculator.P95(Values), 95)
        self.assertEqual(self.Calculator.Headroom(100, 95), 5)
        self.assertEqual(round(self.Calculator.MonthlyGrowthRate(50, 75), 2), 50.0)
        self.assertEqual(self.Calculator.DaysToSaturation(75, 5, 100), 5)

    def test_build_kpi_and_forecast(self):
        Now = datetime.now(UTC)
        Samples = [
            MetricSample("S1", "R1", MetricName.CPU, Now - timedelta(days=1), 50, "Percent", "Test"),
            MetricSample("S2", "R1", MetricName.CPU, Now, 90, "Percent", "Test"),
        ]
        Kpi = self.Calculator.BuildKpi("K1", Samples, 95, PreviousAverage=50)
        Forecast = self.Calculator.BuildForecast("F1", Kpi, 95)
        self.assertEqual(Kpi.ResourceId, "R1")
        self.assertEqual(Kpi.PeakUtilization, 90)
        self.assertEqual(Forecast.Forecast30Days, 98)


if __name__ == "__main__":
    unittest.main()
