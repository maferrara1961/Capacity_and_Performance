import json
import unittest
from pathlib import Path


DashboardDirectory = Path("Config/Grafana/Dashboards")


class GrafanaDrilldownContractTest(unittest.TestCase):
    def test_paneles_no_texto_tienen_links_de_drilldown(self):
        for DashboardPath in DashboardDirectory.glob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Panel in Dashboard.get("panels", []):
                if Panel.get("type") == "text":
                    continue
                Links = Panel.get("fieldConfig", {}).get("defaults", {}).get("links", [])
                self.assertTrue(Links, f"{DashboardPath.name}: {Panel.get('title')}")
                LinkText = json.dumps(Links)
                self.assertIn("/d/technical-performance/technical-performance-dashboard", LinkText)
                self.assertIn("var-HostName", LinkText)

                if Panel.get("type") == "timeseries":
                    self.assertIn("var-LoadId=${__field.labels.load_id}", LinkText)
                    self.assertIn("var-HostName=${__field.labels.host_name}", LinkText)
                    self.assertIn("var-ServiceId=${__field.labels.business_service_id}", LinkText)
                    self.assertNotIn("${__data.fields.HostName}${__field.labels.host_name}", LinkText)
                else:
                    self.assertIn("var-LoadId=${LoadId}", LinkText)
                    self.assertIn("var-HostName=${__data.fields.HostName}", LinkText)

    def test_dashboards_tienen_rango_default_de_30_dias(self):
        for DashboardPath in DashboardDirectory.glob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))

            self.assertEqual({"from": "now-30d", "to": "now"}, Dashboard.get("time"), DashboardPath.name)

    def test_dashboard_tecnico_filtra_por_host_y_servicio(self):
        Dashboard = json.loads((DashboardDirectory / "TechnicalPerformanceDashboard.json").read_text(encoding="utf-8"))
        Text = json.dumps(Dashboard)
        Variables = {Variable["name"] for Variable in Dashboard.get("templating", {}).get("list", [])}

        self.assertEqual("technical-performance", Dashboard.get("uid"))
        self.assertIn("HostName", Variables)
        self.assertIn("ServiceId", Variables)
        self.assertIn('host_name=~\\"${HostName:regex}\\"', Text)
        self.assertIn('business_service_id=~\\"${ServiceId:regex}\\"', Text)
        self.assertIn("${ServiceId:regex}", Text)

    def test_dashboard_tecnico_muestra_average_y_tendencia_del_rango(self):
        Dashboard = json.loads((DashboardDirectory / "TechnicalPerformanceDashboard.json").read_text(encoding="utf-8"))
        Text = json.dumps(Dashboard)
        TimeSeriesPanels = [Panel for Panel in Dashboard.get("panels", []) if Panel.get("type") == "timeseries"]

        self.assertTrue(TimeSeriesPanels)
        for Panel in TimeSeriesPanels:
            PanelText = json.dumps(Panel)
            self.assertIn("avg_over_time", PanelText, Panel.get("title"))
            self.assertIn("predict_linear", PanelText, Panel.get("title"))
            self.assertIn("$__range", PanelText, Panel.get("title"))
            self.assertIn("average rango", PanelText, Panel.get("title"))
            self.assertIn("tendencia rango", PanelText, Panel.get("title"))

    def test_series_temporales_muestran_host_no_lote_demo_en_leyenda(self):
        for DashboardPath in DashboardDirectory.glob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Panel in Dashboard.get("panels", []):
                if Panel.get("type") != "timeseries":
                    continue
                for Target in Panel.get("targets", []):
                    Legend = Target.get("legendFormat", "")
                    self.assertIn("{{host_name}}", Legend, f"{DashboardPath.name}: {Panel.get('title')}")
                    self.assertNotIn("{{load_id}}", Legend, f"{DashboardPath.name}: {Panel.get('title')}")


if __name__ == "__main__":
    unittest.main()
