import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "Config/Grafana/Dashboards/Performance/PlatformContainerMetricsDashboard.json"
UPDATE_SCRIPT = ROOT / "Scripts/UpdatePlatformZabbixStatus.sh"


class PlatformContainerMetricsDashboardContractTest(unittest.TestCase):
    def test_dashboard_consulta_metricas_de_contenedores_en_victoriametrics(self):
        Dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8"))
        Source = DASHBOARD.read_text(encoding="utf-8")

        self.assertEqual("platform-container-metrics", Dashboard["uid"])
        self.assertEqual("Platform Containers Metrics", Dashboard["title"])
        self.assertIn('"uid": "VictoriaMetrics"', Source)
        for SeriesName in [
            "platform_container_up",
            "platform_container_cpu_percent",
            "platform_container_memory_used_bytes",
            "platform_container_memory_percent",
            "platform_container_network_input_bytes",
            "platform_container_network_output_bytes",
            "platform_container_block_input_bytes",
            "platform_container_block_output_bytes",
        ]:
            self.assertIn(SeriesName, Source)

    def test_script_publica_metricas_en_victoriametrics(self):
        Script = UPDATE_SCRIPT.read_text(encoding="utf-8")

        self.assertIn("api/v1/import/prometheus", Script)
        self.assertIn("PlatformMetrics.prom", Script)
        self.assertIn("platform_container_cpu_percent", Script)
        self.assertIn("platform_container_memory_used_bytes", Script)
        self.assertIn("platform_container_up", Script)


if __name__ == "__main__":
    unittest.main()
