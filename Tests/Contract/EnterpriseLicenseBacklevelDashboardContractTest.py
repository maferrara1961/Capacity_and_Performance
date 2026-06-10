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
        self.assertIn("EvidenceReference", Text)
        self.assertIn("Abrir evidencia en Zabbix", Text)
        self.assertIn("http://163.176.224.55:8080", Text)
        self.assertIn("EnterpriseEvidenceRecord", Text)
        self.assertIn('"name": "LoadId"', Text)
        self.assertIn('"allValue": ".*"', Text)
        self.assertIn("${LoadId:regex}", Text)
        self.assertNotIn("technical-performance", Text)
        self.assertNotIn("localhost:8080", Text)
        self.assertNotIn("ZabbixBaseUrl", Text)

    def test_dashboard_backlevel_existe_y_filtra_por_lote(self):
        Dashboard = LoadDashboard("EnterpriseSoftwareBacklevelDashboard.json")
        Text = json.dumps(Dashboard)

        self.assertEqual("Enterprise Software Backlevel Dashboard", Dashboard["title"])
        self.assertIn("BacklevelStatus", Text)
        self.assertIn("EndOfSupportDate", Text)
        self.assertIn("LifecycleStatus", Text)
        self.assertIn("EnterpriseTechnologyComponent", Text)
        self.assertIn("EvidenceReference", Text)
        self.assertIn("EvidencePath", Text)
        self.assertIn("Abrir evidencia en Zabbix", Text)
        self.assertIn("ZabbixBaseUrl", Text)
        self.assertIn("EnterpriseEvidenceRecord", Text)
        self.assertIn('"name": "LoadId"', Text)
        self.assertIn('"allValue": ".*"', Text)
        self.assertIn("${LoadId:regex}", Text)
        self.assertNotIn("technical-performance", Text)
        self.assertNotIn("localhost:8080", Text)

    def test_dashboards_de_riesgo_no_tienen_links_genericos_a_technical(self):
        for DashboardName in [
            "EnterpriseExecutiveDashboard.json",
            "EnterpriseGovernanceDashboard.json",
            "EnterpriseLicenseComplianceDashboard.json",
            "EnterpriseSoftwareBacklevelDashboard.json",
        ]:
            Text = json.dumps(LoadDashboard(DashboardName))

            self.assertNotIn("technical-performance", Text, DashboardName)


if __name__ == "__main__":
    unittest.main()
