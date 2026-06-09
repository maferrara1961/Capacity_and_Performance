import json
import unittest
from pathlib import Path


class GrafanaDatasourceContractTest(unittest.TestCase):
    def test_datasources_tienen_uid_estable(self):
        Text = Path("Config/Grafana/Datasources/Datasources.yml").read_text()
        self.assertIn("uid: VictoriaMetrics", Text)
        self.assertIn("uid: CapacityPostgreSQL", Text)
        self.assertIn("deleteDatasources:", Text)
        self.assertIn("prune: true", Text)
        self.assertIn("orgId: 1", Text)
        self.assertIn("sslmode: disable", Text)

    def test_paneles_sql_usan_postgresql_explicito(self):
        for DashboardPath in Path("Config/Grafana/Dashboards").glob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text())
            for Panel in Dashboard.get("panels", []):
                Targets = Panel.get("targets", [])
                HasSql = any("rawSql" in Target for Target in Targets)
                if HasSql:
                    self.assertEqual(Panel["datasource"]["uid"], "CapacityPostgreSQL", DashboardPath.name)

    def test_paneles_prometheus_usan_victoriametrics_explicito(self):
        Dashboard = json.loads(Path("Config/Grafana/Dashboards/TechnicalPerformanceDashboard.json").read_text())
        PrometheusPanels = [Panel for Panel in Dashboard["panels"] if any("expr" in Target for Target in Panel.get("targets", []))]
        self.assertTrue(PrometheusPanels)
        for Panel in PrometheusPanels:
            self.assertEqual(Panel["datasource"]["uid"], "VictoriaMetrics")

    def test_provider_apunta_a_directorio_de_json_separado(self):
        Provider = Path("Config/Grafana/DashboardProviders/Provisioning.yml").read_text()
        self.assertIn("path: /etc/grafana/dashboards", Provider)


if __name__ == "__main__":
    unittest.main()
