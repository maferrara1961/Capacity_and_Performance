import unittest

from Tests.Contract.GrafanaDatasourceContractTest import DashboardText, LoadDashboard, PanelByTitle, PanelTitles


class ExecutiveDashboardContractTest(unittest.TestCase):
    def test_dashboard_contains_decision_panels(self):
        Dashboard = LoadDashboard("ExecutiveCapacityDashboard.json")
        Titles = PanelTitles(Dashboard)
        Expected = {
            "Overall Capacity State",
            "Top 5 Capacity Risks",
            "Forecast 30/60/90 Days",
            "Capacity Used Vs Headroom",
            "Recommendations",
        }
        self.assertTrue(Expected.issubset(Titles))

    def test_dashboard_prioriza_decision_no_metricas_crudas(self):
        Dashboard = LoadDashboard("ExecutiveCapacityDashboard.json")
        Text = DashboardText("ExecutiveCapacityDashboard.json")
        self.assertIn("OverallRisk", Text)
        self.assertIn("Forecast30Days", Text)
        self.assertIn("Forecast60Days", Text)
        self.assertIn("Forecast90Days", Text)
        self.assertIn("HeadroomAvailable", Text)
        self.assertIn("Action", Text)
        self.assertNotIn("synthetic_latency", Text)

    def test_paneles_ejecutivos_tienen_proposito(self):
        Dashboard = LoadDashboard("ExecutiveCapacityDashboard.json")
        self.assertIn("decision", PanelByTitle(Dashboard, "Overall Capacity State")["description"].lower())
        self.assertIn("top 5", PanelByTitle(Dashboard, "Top 5 Capacity Risks")["description"].lower())
        self.assertIn("missing data", DashboardText("ExecutiveCapacityDashboard.json").lower())


if __name__ == "__main__":
    unittest.main()
