import json
import unittest

from Tests.Contract.GrafanaDatasourceContractTest import LoadDashboard


class EnterpriseOperationalDashboardContractTest(unittest.TestCase):
    def test_dashboard_operativo_expone_tendencias_forecast_y_top_consumers(self):
        Dashboard = LoadDashboard("EnterpriseOperationalDashboard.json")
        Text = json.dumps(Dashboard)

        self.assertEqual("Enterprise Operational Trends Dashboard", Dashboard["title"])
        self.assertIn("Top Consumers Enterprise", Text)
        self.assertIn("Forecast 30 90 180 365", Text)
        self.assertIn("Frescura de Evidencia", Text)
        self.assertIn("technology_domain", Text)
        self.assertIn("business_service", Text)
        self.assertIn('"name": "MetricName"', Text)
        self.assertIn("CPU,RAM,Storage,StorageIO,NetworkIO", Text)
        self.assertIn("${MetricName:regex}", Text)
        self.assertIn("CapacityKpi", Text)
        self.assertIn("ForecastResult", Text)
        self.assertIn("LoadIdCalculado", Text)
        self.assertIn("c.LoadId = k.LoadIdCalculado", Text)
        self.assertIn("k.LoadIdCalculado ~", Text)
        self.assertIn('load_id=~\\"${LoadId:regex}\\"', Text)


if __name__ == "__main__":
    unittest.main()
