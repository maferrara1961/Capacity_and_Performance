import json
import unittest
from pathlib import Path


DashboardDirectory = Path("Config/Grafana/Dashboards")


def DashboardPaths() -> list[Path]:
    return sorted(DashboardDirectory.rglob("*.json"))


def DashboardPath(FileName: str) -> Path:
    Matches = [PathValue for PathValue in DashboardPaths() if PathValue.name == FileName]
    if len(Matches) != 1:
        raise AssertionError(f"dashboard no encontrado o duplicado: {FileName}")
    return Matches[0]


def LoadDashboard(FileName: str) -> dict:
    return json.loads(DashboardPath(FileName).read_text(encoding="utf-8"))


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
        self.assertIn("database: capacity", Text)
        self.assertIn("postgresVersion: 1600", Text)
        self.assertIn("sslmode: disable", Text)

    def test_grafana_usa_postgresql_como_base_operacional(self):
        Common = Path("Scripts/StackCommon.sh").read_text(encoding="utf-8")
        self.assertIn("GF_DATABASE_TYPE=postgres", Common)
        self.assertIn("GF_DATABASE_HOST=${PROJECT_NAME}-postgresql:5432", Common)
        self.assertIn("GF_DATABASE_NAME=grafana", Common)
        self.assertIn("GF_DATABASE_USER=capacity", Common)
        self.assertIn("GF_DATABASE_SSL_MODE=disable", Common)
        self.assertNotIn("capacity-performance-grafana-data:/var/lib/grafana", Common)

    def test_paneles_sql_usan_postgresql_explicito(self):
        for DashboardPath in DashboardPaths():
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Panel in Dashboard.get("panels", []):
                HasSql = any("rawSql" in Target for Target in Panel.get("targets", []))
                if HasSql:
                    self.assertEqual(Panel["datasource"]["uid"], "CapacityPostgreSQL", DashboardPath.name)

    def test_paneles_prometheus_usan_victoriametrics_explicito(self):
        for DashboardPath in DashboardPaths():
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Panel in Dashboard.get("panels", []):
                HasPrometheus = any("expr" in Target for Target in Panel.get("targets", []))
                if HasPrometheus:
                    self.assertEqual(Panel["datasource"]["uid"], "VictoriaMetrics", DashboardPath.name)

    def test_provider_apunta_a_directorio_de_json_separado(self):
        Provider = Path("Config/Grafana/DashboardProviders/Provisioning.yml").read_text(encoding="utf-8")
        self.assertIn("folder: Capacity", Provider)
        self.assertIn("folder: Performance", Provider)
        self.assertIn("folder: Risk & Compliance", Provider)
        self.assertIn("path: /etc/grafana/dashboards/Capacity", Provider)
        self.assertIn("path: /etc/grafana/dashboards/Performance", Provider)
        self.assertIn("path: /etc/grafana/dashboards/RiskAndCompliance", Provider)
        self.assertIn("disableDeletion: false", Provider)
        self.assertIn("prune: true", Provider)

    def test_existe_un_solo_dashboard_tecnico_provisionado(self):
        TechnicalDashboards = []
        for DashboardPath in DashboardPaths():
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            if Dashboard.get("uid") == "technical-performance" or Dashboard.get("title") == "Technical Performance Dashboard":
                TechnicalDashboards.append(DashboardPath.name)

        self.assertEqual(["TechnicalPerformanceDashboard.json"], TechnicalDashboards)

    def test_dashboards_estan_separados_por_carpeta_funcional(self):
        Expected = {
            "Capacity": {
                "ExecutiveCapacityDashboard.json",
                "CapacityPlanningDashboard.json",
                "EnterpriseOperationalDashboard.json",
            },
            "Performance": {
                "TechnicalPerformanceDashboard.json",
                "ApplicationDashboard.json",
                "PlatformContainerMetricsDashboard.json",
            },
            "RiskAndCompliance": {
                "EnterpriseExecutiveDashboard.json",
                "EnterpriseGovernanceDashboard.json",
                "EnterpriseLicenseComplianceDashboard.json",
                "EnterpriseSoftwareBacklevelDashboard.json",
            },
        }

        for FolderName, FileNames in Expected.items():
            Found = {PathValue.name for PathValue in (DashboardDirectory / FolderName).glob("*.json")}
            self.assertEqual(FileNames, Found)

    def test_script_limpia_duplicados_tecnicos_en_grafana(self):
        Script = Path("Scripts/CleanupGrafanaDashboards.sh").read_text(encoding="utf-8")

        self.assertIn("Technical Performance Dashboard", Script)
        self.assertIn("technical-performance", Script)
        self.assertIn("uid <> '${GRAFANA_UID}'", Script)
        self.assertIn("--confirmar", Script)

    def test_kpis_requeridos_tienen_cobertura_en_dashboards(self):
        Text = "\n".join(PathValue.read_text(encoding="utf-8") for PathValue in DashboardPaths())
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
        for DashboardPath in DashboardPaths():
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Panel in Dashboard.get("panels", []):
                self.assertTrue(Panel.get("description"), f"{DashboardPath.name}: {Panel.get('title')}")

    def test_dashboards_incluyen_ayuda_visible_para_interpretacion(self):
        for DashboardPath in DashboardPaths():
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            HelpPanels = [Panel for Panel in Dashboard.get("panels", []) if Panel.get("title") == "Como leer este dashboard"]
            self.assertTrue(HelpPanels, DashboardPath.name)
            Content = HelpPanels[0].get("options", {}).get("content", "")
            self.assertIn("Que muestra", Content)
            self.assertIn("Como interpretarlo", Content)
            self.assertIn("Accion sugerida", Content)

    def test_dashboards_tienen_filtro_de_lote(self):
        for DashboardPath in DashboardPaths():
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            Variables = Dashboard.get("templating", {}).get("list", [])
            LoadVariables = [Variable for Variable in Variables if Variable.get("name") == "LoadId"]
            self.assertTrue(LoadVariables, DashboardPath.name)
            Variable = LoadVariables[0]
            if DashboardPath.name == "PlatformContainerMetricsDashboard.json":
                self.assertEqual("custom", Variable.get("type"), DashboardPath.name)
                self.assertIn("Infraestructura", Variable.get("query", ""), DashboardPath.name)
                continue
            if DashboardPath.name == "TechnicalPerformanceDashboard.json":
                self.assertFalse(Variable.get("includeAll"), DashboardPath.name)
            else:
                self.assertTrue(Variable.get("includeAll"), DashboardPath.name)
                self.assertEqual(Variable.get("allValue"), ".*", DashboardPath.name)
            self.assertIn("TestLoad", Variable.get("query", ""), DashboardPath.name)
            self.assertIn("Infraestructura", Variable.get("query", ""), DashboardPath.name)

    def test_paneles_filtran_por_lote(self):
        for DashboardPath in DashboardPaths():
            Text = DashboardPath.read_text(encoding="utf-8")
            self.assertIn("LoadId", Text, DashboardPath.name)
            if "TechnicalPerformance" in DashboardPath.name or "Application" in DashboardPath.name or "CapacityPlanning" in DashboardPath.name:
                self.assertIn('load_id=~\\"${LoadId:regex}\\"', Text, DashboardPath.name)
            self.assertIn("${LoadId:regex}", Text, DashboardPath.name)

    def test_dashboard_tecnico_incluye_lote_infraestructura(self):
        Text = DashboardPath("TechnicalPerformanceDashboard.json").read_text(encoding="utf-8")

        self.assertIn("Infraestructura", Text)
        self.assertIn("capacity-performance-postgresql", Text)
        self.assertIn("capacity-performance-grafana", Text)
        self.assertIn("capacity-performance-capacity-engine", Text)

    def test_dashboard_tecnico_expone_average_y_top_consumers(self):
        Dashboard = LoadDashboard("TechnicalPerformanceDashboard.json")
        AveragePanel = PanelByTitle(Dashboard, "Average Peak P95")
        TopPanel = PanelByTitle(Dashboard, "Top Consumers And Outliers")
        self.assertIn("AverageUtilization", AveragePanel["targets"][0]["rawSql"])
        self.assertIn("AverageUtilization", TopPanel["targets"][0]["rawSql"])
        self.assertIn("P95Utilization", TopPanel["targets"][0]["rawSql"])

    def test_dashboards_muestran_hostname_congruente_con_zabbix(self):
        RequiredDashboards = [
            "ExecutiveCapacityDashboard.json",
            "TechnicalPerformanceDashboard.json",
            "CapacityPlanningDashboard.json",
            "ApplicationDashboard.json",
        ]
        for FileName in RequiredDashboards:
            Text = DashboardText(FileName)
            self.assertIn("HostName", Text, FileName)
            self.assertIn("MonitoredResource", Text, FileName)
        PrometheusText = DashboardText("TechnicalPerformanceDashboard.json") + DashboardText("ApplicationDashboard.json")
        self.assertIn("{{host_name}}", PrometheusText)


if __name__ == "__main__":
    unittest.main()
