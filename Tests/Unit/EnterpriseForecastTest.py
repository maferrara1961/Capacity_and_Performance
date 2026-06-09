import unittest

from CapacityEngine.Application.EnterpriseForecastService import EnterpriseForecastService
from CapacityEngine.Domain.EnterpriseConstants import EvidenceState, ForecastConfidence


class EnterpriseForecastTest(unittest.TestCase):
    def test_forecast_completo_con_evidencia_suficiente(self):
        Service = EnterpriseForecastService()
        Forecast = Service.BuildForecast("Run1", "Component1", "CPU", [float(Value) for Value in range(1, 91)])

        self.assertEqual(EvidenceState.AVAILABLE, Forecast.EvidenceState)
        self.assertEqual(ForecastConfidence.HIGH, Forecast.Confidence)
        self.assertIsNotNone(Forecast.Forecast30Days)
        self.assertIsNotNone(Forecast.Forecast90Days)
        self.assertIsNotNone(Forecast.Forecast180Days)
        self.assertIsNotNone(Forecast.Forecast365Days)

    def test_forecast_largo_no_se_calcula_con_evidencia_insuficiente(self):
        Service = EnterpriseForecastService()
        Forecast = Service.BuildForecast("Run1", "Component1", "CPU", [10.0, 11.0, 12.0])

        self.assertEqual(EvidenceState.INCOMPLETE, Forecast.EvidenceState)
        self.assertEqual(ForecastConfidence.LOW, Forecast.Confidence)
        self.assertIsNone(Forecast.Forecast365Days)


if __name__ == "__main__":
    unittest.main()
