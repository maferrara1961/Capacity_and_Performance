import unittest

from Tests.Contract.GrafanaDatasourceContractTest import DashboardPath


class EnterpriseExecutiveDashboardContractTest(unittest.TestCase):
    def test_dashboard_ejecutivo_enterprise_declara_paneles_requeridos(self):
        PathValue = DashboardPath("EnterpriseExecutiveDashboard.json")
        self.assertTrue(PathValue.exists())
        Text = PathValue.read_text(encoding="utf-8")
        for Expected in [
            "Enterprise Executive Dashboard",
            "Technology Health Score",
            "Capacity Score",
            "Monitoring Confidence",
            "Risk Heat Map",
            "Top 10 Riesgos",
            "SIN EVIDENCIA",
            "CapacityPostgreSQL",
            "\"name\": \"AssessmentRunId\"",
        ]:
            self.assertIn(Expected, Text)


if __name__ == "__main__":
    unittest.main()
