import json
import unittest
from pathlib import Path


class EnterpriseGovernanceDashboardContractTest(unittest.TestCase):
    def test_dashboard_de_gobierno_expone_inventario_y_riesgo(self):
        Dashboard = json.loads(Path("Config/Grafana/Dashboards/EnterpriseGovernanceDashboard.json").read_text(encoding="utf-8"))
        Text = json.dumps(Dashboard)

        self.assertEqual("Enterprise Governance Dashboard", Dashboard["title"])
        self.assertIn("Inventario Tecnologico", Text)
        self.assertIn("Lifecycle y Compliance", Text)
        self.assertIn("Confianza de Monitoreo", Text)
        self.assertIn("EnterpriseTechnologyComponent", Text)
        self.assertIn("EnterpriseRiskRegistryEntry", Text)
        self.assertIn('"name": "LoadId"', Text)
        self.assertIn('"allValue": ".*"', Text)


if __name__ == "__main__":
    unittest.main()
