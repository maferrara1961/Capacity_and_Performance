import unittest

from Tests.Contract.GrafanaDatasourceContractTest import DashboardText, LoadDashboard, PanelTitles


class TechnicalDashboardContractTest(unittest.TestCase):
    def test_dashboard_contains_metric_and_threshold_panels(self):
        Dashboard = LoadDashboard("TechnicalPerformanceDashboard.json")
        Titles = PanelTitles(Dashboard)
        Expected = {
            "CPU Utilization",
            "RAM Utilization",
            "Storage Utilization",
            "IOPS And Network",
            "Latency Throughput Errors",
            "Saturation",
            "Average Peak P95",
            "Top Consumers And Outliers",
            "Threshold Breaches",
        }
        self.assertTrue(Expected.issubset(Titles))

    def test_dashboard_cubre_metricas_tecnicas_requeridas(self):
        Text = DashboardText("TechnicalPerformanceDashboard.json")
        for Expected in [
            "synthetic_cpu",
            "synthetic_ram",
            "synthetic_storage",
            "synthetic_iops",
            "synthetic_network",
            "synthetic_latency",
            "synthetic_throughput",
            "synthetic_errors",
            "synthetic_saturation",
            "P95Utilization",
        ]:
            self.assertIn(Expected, Text)

    def test_dashboard_incluye_top_consumers_y_contexto(self):
        Text = DashboardText("TechnicalPerformanceDashboard.json")
        self.assertIn("Top Consumers And Outliers", Text)
        self.assertIn("ResourceId", Text)
        self.assertIn("ServiceId", Text)
        self.assertIn('"name": "Environment"', Text)
        self.assertIn("${Environment:regex}", Text)
        self.assertIn('environment=~\\"${Environment:regex}\\"', Text)
        self.assertIn("OverallRisk", Text)


if __name__ == "__main__":
    unittest.main()
