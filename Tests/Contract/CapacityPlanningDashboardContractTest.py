import unittest

from Tests.Contract.GrafanaDatasourceContractTest import DashboardText, LoadDashboard, PanelTitles


class CapacityPlanningDashboardContractTest(unittest.TestCase):
    def test_dashboard_contains_growth_exhaustion_and_headroom(self):
        Dashboard = LoadDashboard("CapacityPlanningDashboard.json")
        Titles = PanelTitles(Dashboard)
        Expected = {
            "Monthly Growth",
            "Exhaustion Date Estimate",
            "Headroom And Baseline",
            "Overprovisioned Resources",
            "Underprovisioned Resources",
            "Saturation Trend",
        }
        self.assertTrue(Expected.issubset(Titles))

    def test_dashboard_cubre_kpis_de_planificacion(self):
        Text = DashboardText("CapacityPlanningDashboard.json")
        for Expected in [
            "MonthlyGrowthRate",
            "DaysToSaturation",
            "HeadroomAvailable",
            "BaselineDelta",
            "Forecast30Days",
            "Forecast60Days",
            "Forecast90Days",
        ]:
            self.assertIn(Expected, Text)


if __name__ == "__main__":
    unittest.main()
