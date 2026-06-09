import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class StackInterconnectionContractTest(unittest.TestCase):
    def test_grafana_datasources_usan_nombres_reales_de_contenedor(self):
        Datasources = (ROOT / "Config/Grafana/Datasources/Datasources.yml").read_text(encoding="utf-8")
        self.assertIn("http://capacity-performance-victoriametrics:8428", Datasources)
        self.assertIn("capacity-performance-postgresql:5432", Datasources)
        self.assertNotIn("url: http://victoriametrics:8428", Datasources)
        self.assertNotIn("url: postgresql:5432", Datasources)

    def test_manifiesto_podman_usa_imagenes_actuales(self):
        Manifest = (ROOT / "Config/PodmanStack.yml").read_text(encoding="utf-8")
        ExpectedImages = [
            "localhost/capacity-performance-postgresql:latest",
            "localhost/capacity-performance-victoriametrics:latest",
            "localhost/capacity-performance-zabbix-server:latest",
            "localhost/capacity-performance-zabbix-web:latest",
            "localhost/capacity-performance-grafana:latest",
            "localhost/capacity-performance-capacity-engine:latest",
        ]
        for Image in ExpectedImages:
            self.assertIn(Image, Manifest)

    def test_zabbix_web_declara_dependencias_operativas(self):
        Common = (ROOT / "Scripts/StackCommon.sh").read_text(encoding="utf-8")
        self.assertIn("ZBX_SERVER_HOST=${PROJECT_NAME}-zabbix-server", Common)
        self.assertIn("DB_SERVER_HOST=${PROJECT_NAME}-postgresql", Common)


if __name__ == "__main__":
    unittest.main()
