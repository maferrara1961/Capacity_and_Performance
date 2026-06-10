import json
import unittest

from Tests.Contract.GrafanaDatasourceContractTest import LoadDashboard


class EnterpriseLicenseBacklevelDashboardContractTest(unittest.TestCase):
    def test_dashboard_de_licencias_existe_y_filtra_por_lote(self):
        Dashboard = LoadDashboard("EnterpriseLicenseComplianceDashboard.json")
        Text = json.dumps(Dashboard)

        self.assertEqual("Enterprise License Compliance Dashboard", Dashboard["title"])
        self.assertIn("LicenseStatus", Text)
        self.assertIn("ComplianceStatus", Text)
        self.assertIn("EnterpriseTechnologyComponent", Text)
        self.assertIn('"name": "LoadId"', Text)
        self.assertIn('"allValue": ".*"', Text)
        self.assertIn("${LoadId:regex}", Text)

    def test_dashboard_backlevel_existe_y_filtra_por_lote(self):
        Dashboard = LoadDashboard("EnterpriseSoftwareBacklevelDashboard.json")
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
