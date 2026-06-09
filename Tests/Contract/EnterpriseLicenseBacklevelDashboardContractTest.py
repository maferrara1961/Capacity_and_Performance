import json
import unittest
from pathlib import Path


class EnterpriseLicenseBacklevelDashboardContractTest(unittest.TestCase):
    def test_dashboard_de_licencias_existe_y_filtra_por_lote(self):
        Dashboard = json.loads(Path("Config/Grafana/Dashboards/EnterpriseLicenseComplianceDashboard.json").read_text(encoding="utf-8"))
        Text = json.dumps(Dashboard)

        self.assertEqual("Enterprise License Compliance Dashboard", Dashboard["title"])
        self.assertIn("LicenseStatus", Text)
        self.assertIn("ComplianceStatus", Text)
        self.assertIn("EnterpriseTechnologyComponent", Text)
        self.assertIn('"name": "LoadId"', Text)
        self.assertIn('"allValue": ".*"', Text)
        self.assertIn("${LoadId:regex}", Text)

    def test_dashboard_backlevel_existe_y_filtra_por_lote(self):
        Dashboard = json.loads(Path("Config/Grafana/Dashboards/EnterpriseSoftwareBacklevelDashboard.json").read_text(encoding="utf-8"))
        Text = json.dumps(Dashboard)

        self.assertEqual("Enterprise Software Backlevel Dashboard", Dashboard["title"])
        self.assertIn("BacklevelStatus", Text)
        self.assertIn("EndOfSupportDate", Text)
        self.assertIn("LifecycleStatus", Text)
        self.assertIn("EnterpriseTechnologyComponent", Text)
        self.assertIn('"name": "LoadId"', Text)
        self.assertIn('"allValue": ".*"', Text)
        self.assertIn("${LoadId:regex}", Text)


if __name__ == "__main__":
    unittest.main()
