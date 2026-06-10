import json
import unittest

from Tests.Contract.GrafanaDatasourceContractTest import LoadDashboard


class EnterpriseGovernanceDashboardContractTest(unittest.TestCase):
    def test_dashboard_de_gobierno_expone_inventario_y_riesgo(self):
        Dashboard = LoadDashboard("EnterpriseGovernanceDashboard.json")
        Text = json.dumps(Dashboard)

        self.assertEqual("Enterprise Governance Dashboard", Dashboard["title"])
        self.assertIn("Inventario Tecnologico", Text)
        self.assertIn("Lifecycle y Compliance", Text)
        self.assertIn("Confianza de Monitoreo", Text)
        self.assertIn("EnterpriseTechnologyComponent", Text)
        self.assertIn("EnterpriseRiskRegistryEntry", Text)
        self.assertIn('"name": "LoadId"', Text)
        self.assertIn('"allValue": ".*"', Text)

    def test_dashboard_de_gobierno_expone_semaforos_iniciales(self):
        Dashboard = LoadDashboard("EnterpriseGovernanceDashboard.json")
        Text = json.dumps(Dashboard)
        Panels = {Panel["title"]: Panel for Panel in Dashboard["panels"]}

        for Title in [
            "Semaforo Inventario",
            "Semaforo Ciclo de Vida / Compliance",
            "Semaforo Confianza de Monitoreo",
        ]:
            self.assertIn(Title, Panels)
            self.assertEqual("stat", Panels[Title]["type"])
            self.assertEqual("percent", Panels[Title]["fieldConfig"]["defaults"]["unit"])
            self.assertIn("thresholds", Panels[Title]["fieldConfig"]["defaults"])

        self.assertIn("InventarioPct", Text)
        self.assertIn("InventarioDetalle", Text)
        self.assertIn("CicloVidaCompliancePct", Text)
        self.assertIn("CicloVidaComplianceDetalle", Text)
        self.assertIn("ConfianzaMonitoreoPct", Text)
        self.assertIn("ConfianzaMonitoreoDetalle", Text)
        self.assertIn("OkCount || '/' || TotalCount", Text)
        self.assertIn("EnterpriseTechnologyComponent", Text)
        self.assertIn("EnterpriseEvidenceRecord", Text)
        self.assertIn("ComplianceStatus = 'Compliant'", Text)
        self.assertIn("EvidenceState = 'Available'", Text)


if __name__ == "__main__":
    unittest.main()
