import json
import unittest
from pathlib import Path


class TechnicalDashboardContractTest(unittest.TestCase):
    def test_dashboard_contains_metric_and_threshold_panels(self):
        Data = json.loads(Path("Config/Grafana/Dashboards/TechnicalPerformanceDashboard.json").read_text())
        Text = json.dumps(Data)
        self.assertIn("CPU", Text)
        self.assertIn("P95Utilization", Text)
        self.assertIn("Threshold Breaches", Text)


if __name__ == "__main__":
    unittest.main()
