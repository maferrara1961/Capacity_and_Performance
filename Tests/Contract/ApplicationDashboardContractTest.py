import json
import unittest
from pathlib import Path


class ApplicationDashboardContractTest(unittest.TestCase):
    def test_dashboard_contains_health_infrastructure_and_dependencies(self):
        Data = json.loads(Path("Config/Grafana/Dashboards/ApplicationDashboard.json").read_text())
        Titles = {Panel["title"] for Panel in Data["panels"]}
        self.assertIn("Application Health", Titles)
        self.assertIn("Associated Infrastructure", Titles)
        self.assertIn("Critical Dependencies", Titles)


if __name__ == "__main__":
    unittest.main()
