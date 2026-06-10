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
            "localhost/capacity-performance-zabbix-agent:latest",
            "localhost/capacity-performance-grafana:latest",
            "localhost/capacity-performance-capacity-engine:latest",
        ]
        for Image in ExpectedImages:
            self.assertIn(Image, Manifest)

    def test_zabbix_web_declara_dependencias_operativas(self):
        Common = (ROOT / "Scripts/StackCommon.sh").read_text(encoding="utf-8")
        self.assertIn("ZBX_SERVER_HOST=${PROJECT_NAME}-zabbix-server", Common)
        self.assertIn("DB_SERVER_HOST=${PROJECT_NAME}-postgresql", Common)
        self.assertIn("POSTGRES_DB=capacity", Common)

    def test_postgresql_inicializa_base_grafana_y_validador_de_consistencia(self):
        InitSql = (ROOT / "Sql/Init/001_CreateGrafanaDatabase.sql").read_text(encoding="utf-8")
        Validator = (ROOT / "Scripts/ValidateDatabaseConsistency.sh").read_text(encoding="utf-8")
        self.assertIn("create database grafana", InitSql)
        self.assertIn("database:grafana", Validator)
        self.assertIn("EnterpriseTechnologyComponent", Validator)

    def test_zabbix_agent_levanta_licencias_y_backlevel(self):
        Common = (ROOT / "Scripts/StackCommon.sh").read_text(encoding="utf-8")
        Adapter = (ROOT / "CapacityEngine/Adapters/SyntheticZabbixAdapter.py").read_text(encoding="utf-8")
        UserParameters = (ROOT / "Config/ZabbixAgent/UserParameters.conf").read_text(encoding="utf-8")
        Containerfile = (ROOT / "ContainerImages/ZabbixAgent/Containerfile").read_text(encoding="utf-8")
        self.assertIn("ZabbixAgent", Common)
        self.assertIn("${PROJECT_NAME}-zabbix-agent", Common)
        self.assertIn("capacity.enterprise.fact[*]", UserParameters)
        self.assertIn("capacity.platform.status[*]", UserParameters)
        self.assertIn("capacity.platform.metric[*]", UserParameters)
        self.assertIn("ReadPlatformStatus.sh", Containerfile)
        self.assertIn("ReadPlatformMetric.sh", Containerfile)
        self.assertIn("LicenseStatus", Adapter)
        self.assertIn("BacklevelStatus", Adapter)
        self.assertIn('"type": 0', Adapter)

    def test_zabbix_agent_expone_estado_de_componentes_batch(self):
        Adapter = (ROOT / "CapacityEngine/Adapters/SyntheticZabbixAdapter.py").read_text(encoding="utf-8")
        Start = (ROOT / "Scripts/StartStack.sh").read_text(encoding="utf-8")
        Stop = (ROOT / "Scripts/StopStack.sh").read_text(encoding="utf-8")
        StatusScript = (ROOT / "Scripts/UpdatePlatformZabbixStatus.sh").read_text(encoding="utf-8")
        CronScript = (ROOT / "Scripts/InstallPlatformMetricsCron.sh").read_text(encoding="utf-8")
        Reader = (ROOT / "Config/ZabbixAgent/ReadPlatformStatus.sh").read_text(encoding="utf-8")
        MetricReader = (ROOT / "Config/ZabbixAgent/ReadPlatformMetric.sh").read_text(encoding="utf-8")

        self.assertIn("capacity.platform.status[{ServiceName}]", Adapter)
        self.assertIn("capacity.platform.metric[{ServiceName},{MetricName}]", Adapter)
        self.assertIn("EnsurePlatformMetricItems", Adapter)
        self.assertIn("EnsurePlatformGraph", Adapter)
        self.assertIn('"type": ItemType', Adapter)
        self.assertIn("ItemType = 0", Adapter)
        self.assertIn("UpdatePlatformZabbixStatus.sh", Start)
        self.assertIn("UpdatePlatformZabbixStatus.sh", Stop)
        self.assertIn("PlatformStatus.tsv", StatusScript)
        self.assertIn("PlatformMetrics.tsv", StatusScript)
        self.assertIn("stats --no-stream", StatusScript)
        self.assertIn("UpdatePlatformZabbixStatus.sh", CronScript)
        self.assertIn("CAPACITY_PLATFORM_METRICS_START", CronScript)
        self.assertIn("* * * * *", CronScript)
        self.assertIn("IsBatchService", StatusScript)
        self.assertIn("PlatformStatus.tsv", Reader)
        self.assertIn("PlatformMetrics.tsv", MetricReader)
        for MetricName in [
            "CpuPercent",
            "MemoryUsedBytes",
            "MemoryPercent",
            "NetworkInputBytes",
            "NetworkOutputBytes",
            "BlockInputBytes",
            "BlockOutputBytes",
        ]:
            self.assertIn(MetricName, Adapter)
            self.assertIn(MetricName, MetricReader)

    def test_zabbix_registra_componentes_productivos_de_plataforma(self):
        Adapter = (ROOT / "CapacityEngine/Adapters/SyntheticZabbixAdapter.py").read_text(encoding="utf-8")
        Script = (ROOT / "Scripts/RegisterPlatformHosts.sh").read_text(encoding="utf-8")
        Validator = (ROOT / "Scripts/ValidateStack.sh").read_text(encoding="utf-8")

        self.assertIn("Capacity Platform", Adapter)
        self.assertIn("Produccion", Adapter)
        for HostName in [
            "capacity-performance-postgresql",
            "capacity-performance-victoriametrics",
            "capacity-performance-zabbix-server",
            "capacity-performance-zabbix-web",
            "capacity-performance-zabbix-agent",
            "capacity-performance-grafana",
            "capacity-performance-capacity-engine",
        ]:
            self.assertIn(HostName, Adapter)
        self.assertIn("register-platform-hosts", Script)
        self.assertIn("RegisterPlatformHosts.sh", Validator)

    def test_grafana_monta_provisioning_desde_el_repositorio(self):
        Common = (ROOT / "Scripts/StackCommon.sh").read_text(encoding="utf-8")
        self.assertIn("${REPO_ROOT}/Config/Grafana/Datasources:/etc/grafana/provisioning/datasources:ro,Z", Common)
        self.assertIn("${REPO_ROOT}/Config/Grafana/DashboardProviders:/etc/grafana/provisioning/dashboards:ro,Z", Common)
        self.assertIn("${REPO_ROOT}/Config/Grafana/Dashboards:/etc/grafana/dashboards:ro,Z", Common)


if __name__ == "__main__":
    unittest.main()
