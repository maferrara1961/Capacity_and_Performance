import unittest

from Tests.Contract.GrafanaDatasourceContractTest import DashboardText, LoadDashboard, PanelTitles


class ApplicationDashboardContractTest(unittest.TestCase):
    def test_dashboard_contains_health_infrastructure_and_dependencies(self):
        Dashboard = LoadDashboard("ApplicationDashboard.json")
        Titles = PanelTitles(Dashboard)
        Expected = {
            "Application Health",
            "Associated Infrastructure",
            "Critical Dependencies",
            "End To End Performance",
            "Service Capacity Risk",
        }
        self.assertTrue(Expected.issubset(Titles))

    def test_dashboard_expone_contexto_de_servicio(self):
        Text = DashboardText("ApplicationDashboard.json")
        self.assertIn("ServiceId", Text)
        self.assertIn("ApplicationId", Text)
        self.assertIn("ResourceId", Text)
        self.assertIn('"name": "Environment"', Text)
        self.assertIn("${Environment:regex}", Text)
        self.assertIn('environment=~\\"${Environment:regex}\\"', Text)
        self.assertIn("ImpactWeight", Text)
        self.assertIn("OverallRisk", Text)


if __name__ == "__main__":
    unittest.main()
