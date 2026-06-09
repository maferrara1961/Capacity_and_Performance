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
                self.assertIn("var-LoadId=${LoadId}", LinkText)
                self.assertIn("var-HostName", LinkText)

    def test_dashboard_tecnico_filtra_por_host_y_servicio(self):
        Dashboard = json.loads((DashboardDirectory / "TechnicalPerformanceDashboard.json").read_text(encoding="utf-8"))
        Text = json.dumps(Dashboard)
        Variables = {Variable["name"] for Variable in Dashboard.get("templating", {}).get("list", [])}

        self.assertEqual("technical-performance", Dashboard.get("uid"))
        self.assertIn("HostName", Variables)
        self.assertIn("ServiceId", Variables)
        self.assertIn('host_name=~\\"${HostName:regex}\\"', Text)
        self.assertIn("${ServiceId:regex}", Text)


if __name__ == "__main__":
    unittest.main()
