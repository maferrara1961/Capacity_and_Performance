import json
import unittest
from pathlib import Path


class ExecutiveDashboardContractTest(unittest.TestCase):
    def test_dashboard_contains_risk_forecast_and_recommendation_panels(self):
        Data = json.loads(Path("Config/Grafana/Dashboards/ExecutiveCapacityDashboard.json").read_text())
        Titles = {Panel["title"] for Panel in Data["panels"]}
        self.assertIn("Overall Capacity State", Titles)
        self.assertIn("Forecast 30/60/90 Days", Titles)
        self.assertIn("Recommendations", Titles)


if __name__ == "__main__":
    unittest.main()
