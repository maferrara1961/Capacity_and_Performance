import json
import unittest
from pathlib import Path


DashboardDirectory = Path("Config/Grafana/Dashboards")


def LoadDashboard(FileName: str) -> dict:
    return json.loads((DashboardDirectory / FileName).read_text(encoding="utf-8"))


def DashboardText(FileName: str) -> str:
    return json.dumps(LoadDashboard(FileName))


def PanelTitles(Dashboard: dict) -> set[str]:
    return {Panel["title"] for Panel in Dashboard.get("panels", [])}


def PanelByTitle(Dashboard: dict, Title: str) -> dict:
    for Panel in Dashboard.get("panels", []):
        if Panel.get("title") == Title:
            return Panel
    raise AssertionError(f"panel no encontrado: {Title}")


class GrafanaDatasourceContractTest(unittest.TestCase):
    def test_datasources_tienen_uid_estable(self):
        Text = Path("Config/Grafana/Datasources/Datasources.yml").read_text(encoding="utf-8")
        self.assertIn("uid: VictoriaMetrics", Text)
        self.assertIn("uid: CapacityPostgreSQL", Text)
        self.assertIn("deleteDatasources:", Text)
        self.assertIn("prune: true", Text)
        self.assertIn("orgId: 1", Text)
        self.assertIn("sslmode: disable", Text)

    def test_paneles_sql_usan_postgresql_explicito(self):
        for DashboardPath in DashboardDirectory.glob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Panel in Dashboard.get("panels", []):
                HasSql = any("rawSql" in Target for Target in Panel.get("targets", []))
                if HasSql:
                    self.assertEqual(Panel["datasource"]["uid"], "CapacityPostgreSQL", DashboardPath.name)

    def test_paneles_prometheus_usan_victoriametrics_explicito(self):
        for DashboardPath in DashboardDirectory.glob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Panel in Dashboard.get("panels", []):
                HasPrometheus = any("expr" in Target for Target in Panel.get("targets", []))
                if HasPrometheus:
                    self.assertEqual(Panel["datasource"]["uid"], "VictoriaMetrics", DashboardPath.name)

    def test_provider_apunta_a_directorio_de_json_separado(self):
        Provider = Path("Config/Grafana/DashboardProviders/Provisioning.yml").read_text(encoding="utf-8")
        self.assertIn("path: /etc/grafana/dashboards", Provider)

    def test_kpis_requeridos_tienen_cobertura_en_dashboards(self):
        Text = "\n".join(DashboardText(Path.name) for Path in DashboardDirectory.glob("*.json"))
        Required = [
            "AverageUtilization",
            "PeakUtilization",
            "P95Utilization",
            "MonthlyGrowthRate",
            "HeadroomAvailable",
            "Forecast30Days",
            "Forecast60Days",
            "Forecast90Days",
            "DaysToSaturation",
            "BaselineDelta",
        ]
        for Field in Required:
            self.assertIn(Field, Text)

    def test_dashboard_paneles_declaran_proposito_o_descripcion(self):
        for DashboardPath in DashboardDirectory.glob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Panel in Dashboard.get("panels", []):
                self.assertTrue(Panel.get("description"), f"{DashboardPath.name}: {Panel.get('title')}")


if __name__ == "__main__":
    unittest.main()
