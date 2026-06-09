import json
import unittest
from pathlib import Path


class EnterpriseOperationalDashboardContractTest(unittest.TestCase):
    def test_dashboard_operativo_expone_tendencias_forecast_y_top_consumers(self):
        Dashboard = json.loads(Path("Config/Grafana/Dashboards/EnterpriseOperationalDashboard.json").read_text(encoding="utf-8"))
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
        self.assertIn('load_id=~\\"${LoadId:regex}\\"', Text)


if __name__ == "__main__":
    unittest.main()
