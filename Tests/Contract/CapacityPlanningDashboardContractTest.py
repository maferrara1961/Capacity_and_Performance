import json
import unittest
from pathlib import Path


class CapacityPlanningDashboardContractTest(unittest.TestCase):
    def test_dashboard_contains_growth_exhaustion_and_headroom(self):
        Data = json.loads(Path("Config/Grafana/Dashboards/CapacityPlanningDashboard.json").read_text())
        Text = json.dumps(Data)
        self.assertIn("MonthlyGrowthRate", Text)
        self.assertIn("DaysToSaturation", Text)
        self.assertIn("HeadroomAvailable", Text)


if __name__ == "__main__":
    unittest.main()
