import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from CapacityEngine.Adapters.SyntheticPostgreSqlAdapter import SyntheticPostgreSqlAdapter
from CapacityEngine.Adapters.SyntheticVictoriaMetricsAdapter import SyntheticVictoriaMetricsAdapter
from CapacityEngine.Adapters.SyntheticZabbixAdapter import SyntheticZabbixAdapter
from CapacityEngine.Application.SyntheticDataService import SyntheticDataService


ROOT = Path(__file__).resolve().parents[2]


def RunManage(*Args):
    Env = os.environ.copy()
    Env["SYNTHETIC_DATA_DIR"] = tempfile.mkdtemp(prefix="synthetic-contract-")
    Env["STACK_DRY_RUN"] = "1"
    return subprocess.run(["bash", "Scripts/ManageTestData.sh", *Args], cwd=ROOT, env=Env, text=True, capture_output=True)


class SyntheticDataCliContractTest(unittest.TestCase):
    def test_load_imprime_resumen_en_castellano(self):
        Result = RunManage("load", "--profile", "mixed", "--volume", "small", "--load-id", "DemoLoad001")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("INFO: carga sintetica completada", Result.stdout)
        self.assertIn("lote: DemoLoad001", Result.stdout)
        self.assertIn("servicios:", Result.stdout)
        self.assertIn("recomendaciones:", Result.stdout)

    def test_rechaza_profile_invalido(self):
        Result = RunManage("load", "--profile", "invalido")
        self.assertNotEqual(Result.returncode, 0)
        self.assertIn("perfil no permitido", Result.stderr)

    def test_delete_all_requiere_confirmacion(self):
        Result = RunManage("delete", "--all")
        self.assertNotEqual(Result.returncode, 0)
        self.assertIn("--confirmar", Result.stderr)

    def test_validate_imprime_herramientas(self):
        Result = RunManage("validate")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("Grafana", Result.stdout)
        self.assertIn("VictoriaMetrics", Result.stdout)
        self.assertIn("PostgreSQL", Result.stdout)
        self.assertIn("Zabbix hosts/items sinteticos", Result.stdout)

    def test_postgresql_sql_incluye_tablas_de_dashboard(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("SqlDemo001", "mixed", "small", 30, 1)
        Sql = SyntheticPostgreSqlAdapter().BuildLoadSql(Dataset)
        self.assertIn("insert into CapacityKpi", Sql)
        self.assertIn("insert into ForecastResult", Sql)
        self.assertIn("insert into RiskAssessment", Sql)
        self.assertIn("insert into Recommendation", Sql)
        self.assertIn("insert into Service", Sql)
        self.assertIn("Servicio Sintetico SqlDemo001 1", Sql)

    def test_nombres_sinteticos_son_unicos_por_lote(self):
        First = SyntheticDataService().BuildSyntheticDataset("NameDemo001", "mixed", "small", 30, 1)
        Second = SyntheticDataService().BuildSyntheticDataset("NameDemo002", "mixed", "small", 30, 1)
        self.assertNotEqual(First["Services"][0]["Name"], Second["Services"][0]["Name"])
        self.assertNotEqual(First["Resources"][0]["Name"], Second["Resources"][0]["Name"])

    def test_victoriametrics_import_usa_formato_prometheus(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("VmDemo001", "mixed", "small", 30, 1)
        Adapter = SyntheticVictoriaMetricsAdapter()
        self.assertEqual(Adapter.NormalizeMetricName("CPU"), "synthetic_cpu")
        self.assertEqual(Adapter.NormalizeMetricName("Network IOPS"), "synthetic_network_iops")
        FirstSample = Dataset["Samples"][0]
        self.assertIsInstance(Adapter.TimestampMillis(FirstSample["ObservedAt"]), int)
        Payload = Adapter.BuildImportPayload(Dataset["Samples"])
        self.assertIn('"__name__": "synthetic_cpu"', Payload)
        self.assertIn('"load_id": "VmDemo001"', Payload)
        self.assertIn('"timestamps": [', Payload)

    def test_zabbix_adapter_define_items_de_capacity(self):
        Adapter = SyntheticZabbixAdapter()
        self.assertEqual(Adapter.ItemKey("CPU"), "capacity.synthetic[cpu]")
        self.assertEqual(Adapter.ItemKey("Network IOPS"), "capacity.synthetic[network_iops]")

    def test_zabbix_latest_samples_por_recurso_y_metrica(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("ZbxDemo001", "mixed", "small", 30, 1)
        Latest = SyntheticZabbixAdapter().LatestSamplesByResourceAndMetric(Dataset["Samples"])
        ResourceId = Dataset["Resources"][0]["ResourceId"]
        self.assertIn("CPU", Latest[ResourceId])
        self.assertEqual(Latest[ResourceId]["CPU"]["LoadId"], "ZbxDemo001")

    def test_script_de_lotes_de_verificacion_existe(self):
        Script = ROOT / "Scripts" / "GenerateVerificationBatches.sh"
        self.assertTrue(Script.exists())
        self.assertIn("RunLoad critical", Script.read_text())
        self.assertIn("delete --load-id", Script.read_text())


if __name__ == "__main__":
    unittest.main()
