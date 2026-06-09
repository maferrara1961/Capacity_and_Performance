import unittest
from pathlib import Path


class ArchitectureDocumentContractTest(unittest.TestCase):
    def test_architecture_documenta_tools_comunicacion_y_bases(self):
        Text = Path("ARCH.md").read_text(encoding="utf-8")
        for Expected in [
            "Herramientas",
            "Comunicacion Interna",
            "Subsistemas",
            "Bases de Datos y Persistencia",
            "PostgreSQL",
            "VictoriaMetrics",
            "ZabbixServer",
            "ZabbixWeb",
            "Grafana",
            "CapacityEngine",
            "capacity-performance-net",
            "SRV-#####",
        ]:
            self.assertIn(Expected, Text)


if __name__ == "__main__":
    unittest.main()
