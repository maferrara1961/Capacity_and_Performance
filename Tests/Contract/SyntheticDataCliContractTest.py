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

    def test_sync_zabbix_inventory_imprime_resumen(self):
        RunManage("load", "--profile", "mixed", "--volume", "small", "--load-id", "SyncInventory001")
        Result = RunManage("sync-zabbix-inventory")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("sincronizacion de inventario Zabbix completada", Result.stdout)
        self.assertIn("fuente: Zabbix", Result.stdout)
        self.assertIn("destino: PostgreSQL", Result.stdout)

    def test_postgresql_sql_incluye_tablas_de_dashboard(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("SqlDemo001", "mixed", "small", 30, 1)
        Sql = SyntheticPostgreSqlAdapter().BuildLoadSql(Dataset)
        self.assertIn("insert into CapacityKpi", Sql)
        self.assertIn("insert into ForecastResult", Sql)
        self.assertIn("insert into RiskAssessment", Sql)
        self.assertIn("insert into Recommendation", Sql)
        self.assertIn("insert into Service", Sql)
        self.assertIn("insert into CapacityKpi (CapacityKpiId, LoadId", Sql)
        self.assertIn("-SubsistemaDefinido", Sql)
        self.assertIn("'SqlDemo001-Resource-1'", Sql)
        self.assertIn("'Revisar capacidad del host asociado", Sql)
        self.assertEqual(Dataset["Recommendations"][0]["ScopeId"], Dataset["Risks"][0]["ScopeId"])

    def test_postgresql_sincroniza_inventario_desde_zabbix(self):
        Hosts = [
            {
                "HostName": "SRV-12345",
                "VisibleName": "SRV-12345",
                "Status": "OK",
                "AssetTag": "Manual-1",
                "Type": "Server",
                "Os": "Linux",
                "Location": "Datacenter",
                "Notes": "Alta manual en Zabbix",
            }
        ]
        Sql = SyntheticPostgreSqlAdapter().BuildZabbixInventorySyncSql(Hosts)
        self.assertIn("Platform = excluded.Platform", Sql)
        self.assertIn("'ZabbixInventory'", Sql)
        self.assertIn("'SRV-12345'", Sql)
        self.assertIn("delete from MonitoredResource where Platform = 'ZabbixInventory'", Sql)

    def test_nombres_sinteticos_son_unicos_por_lote(self):
        First = SyntheticDataService().BuildSyntheticDataset("NameDemo001", "mixed", "small", 30, 1)
        Second = SyntheticDataService().BuildSyntheticDataset("NameDemo002", "mixed", "small", 30, 1)
        self.assertNotEqual(First["Services"][0]["Name"], Second["Services"][0]["Name"])
        self.assertNotEqual(First["Resources"][0]["Name"], Second["Resources"][0]["Name"])

    def test_recursos_usan_hosts_srv_aleatorios_con_inventario(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("SrvDemo001", "mixed", "small", 30, 1)
        HostNames = [Resource["Name"] for Resource in Dataset["Resources"]]
        self.assertEqual(len(HostNames), len(set(HostNames)))
        for Resource in Dataset["Resources"]:
            self.assertRegex(Resource["Name"], r"^SRV-[0-9]{5}$")
            self.assertEqual(Resource["Inventory"]["Alias"], Resource["Name"])
            self.assertEqual(Resource["Inventory"]["AssetTag"], f"SrvDemo001-{Dataset['Resources'].index(Resource) + 1}")

    def test_subsistemas_usan_hostname_mas_subsistema_definido(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("SubsystemDemo001", "mixed", "small", 30, 1)

        self.assertEqual(len(Dataset["Services"]), len(Dataset["Resources"]))
        for Resource, Service in zip(Dataset["Resources"], Dataset["Services"], strict=True):
            ExpectedSubsystem = f"{Resource['Name']}-SubsistemaDefinido"
            self.assertEqual(Service["ServiceId"], ExpectedSubsystem)
            self.assertEqual(Service["Name"], ExpectedSubsystem)

        FirstSample = Dataset["Samples"][0]
        self.assertEqual(FirstSample["BusinessServiceId"], f"{FirstSample['HostName']}-SubsistemaDefinido")
        self.assertEqual(FirstSample["BusinessService"], FirstSample["BusinessServiceId"])

        FirstComponent = Dataset["EnterpriseComponents"][0]
        self.assertEqual(FirstComponent["BusinessServiceId"], f"{FirstComponent['ComponentName']}-SubsistemaDefinido")

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
        self.assertIn('"host_name": "SRV-', Payload)
        self.assertIn('"timestamps": [', Payload)

    def test_zabbix_adapter_define_items_de_capacity(self):
        Adapter = SyntheticZabbixAdapter()
        self.assertEqual(Adapter.ItemKey("CPU"), "capacity.synthetic[cpu]")
        self.assertEqual(Adapter.ItemKey("Network IOPS"), "capacity.synthetic[network_iops]")
        self.assertTrue(Adapter.TriggerThresholds("CPU"))
        self.assertTrue(Adapter.TriggerThresholds("Saturation"))
        Inventory = Adapter.BuildZabbixInventory(
            {
                "ResourceId": "SrvDemo001-Resource-1",
                "ResourceType": "Server",
                "Name": "SRV-12345",
                "Inventory": {"AssetTag": "SrvDemo001-1", "Alias": "SRV-12345", "Type": "Server"},
            }
        )
        self.assertEqual(Inventory["name"], "SRV-12345")
        self.assertEqual(Inventory["asset_tag"], "SrvDemo001-1")

    def test_zabbix_host_name_visible_y_tecnico_usa_srv(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("ZbxSrv001", "mixed", "small", 30, 1)
        Resource = Dataset["Resources"][0]
        self.assertRegex(Resource["Name"], r"^SRV-[0-9]{5}$")
        self.assertNotEqual(Resource["Name"], Resource["ResourceId"])
        AdapterSource = (ROOT / "CapacityEngine" / "Adapters" / "SyntheticZabbixAdapter.py").read_text()
        self.assertIn('"host": Resource["Name"]', AdapterSource)
        self.assertIn("searchInventory", AdapterSource)

    def test_zabbix_latest_samples_por_recurso_y_metrica(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("ZbxDemo001", "mixed", "small", 30, 1)
        Latest = SyntheticZabbixAdapter().LatestSamplesByResourceAndMetric(Dataset["Samples"])
        ResourceId = Dataset["Resources"][0]["ResourceId"]
        self.assertIn("CPU", Latest[ResourceId])
        self.assertEqual(Latest[ResourceId]["CPU"]["LoadId"], "ZbxDemo001")

    def test_zabbix_adapter_expone_graficos_y_alertas_por_host(self):
        Adapter = SyntheticZabbixAdapter()
        self.assertTrue(hasattr(Adapter, "EnsureGraph"))
        self.assertTrue(hasattr(Adapter, "EnsureTriggers"))
        CpuThresholds = Adapter.TriggerThresholds("CPU")
        self.assertIn(("Warning", 2, 75), CpuThresholds)
        self.assertIn(("Critical", 4, 90), CpuThresholds)

    def test_zabbix_history_push_usa_itemid_y_todas_las_muestras(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("ZbxHistory001", "critical", "small", 30, 1)
        ItemIds = {
            (Sample["ResourceId"], Sample["MetricName"]): f"Item-{Sample['ResourceId']}-{Sample['MetricName']}"
            for Sample in Dataset["Samples"]
        }
        Payload = SyntheticZabbixAdapter().BuildHistoryPushPayload(Dataset["Samples"], ItemIds)
        self.assertEqual(len(Payload), len(Dataset["Samples"]))
        self.assertIn("itemid", Payload[0])
        self.assertNotIn("host", Payload[0])
        self.assertNotIn("key", Payload[0])

    def test_script_de_lotes_de_verificacion_existe(self):
        Script = ROOT / "Scripts" / "GenerateVerificationBatches.sh"
        self.assertTrue(Script.exists())
        self.assertIn("RunLoad critical", Script.read_text())
        self.assertIn("delete --load-id", Script.read_text())

    def test_script_de_sincronizacion_zabbix_existe(self):
        Script = ROOT / "Scripts" / "SyncZabbixInventory.sh"
        self.assertTrue(Script.exists())
        self.assertIn("sync-zabbix-inventory", Script.read_text())

    def test_script_de_lotes_historicos_genera_30_60_y_90_dias(self):
        Script = ROOT / "Scripts" / "GenerateHistoricalVerificationBatches.sh"
        Content = Script.read_text()
        self.assertTrue(Script.exists())
        self.assertIn("WINDOWS=\"${VERIFY_WINDOWS:-30 60 90}\"", Content)
        self.assertIn("--days \"$Days\"", Content)
        self.assertIn("${PREFIX}-${Days}d-${Profile}", Content)

    def test_perfiles_de_verificacion_requeridos_generan_datos(self):
        Service = SyntheticDataService()
        for Profile in ["normal", "warning", "critical", "mixed"]:
            Dataset = Service.BuildSyntheticDataset(f"Profile{Profile}001", Profile, "small", 30, 1)
            self.assertEqual(Dataset["Load"]["ScenarioProfile"], Profile)
            self.assertGreater(Dataset["Load"]["GeneratedMetricSampleCount"], 0)
            self.assertGreater(Dataset["Load"]["GeneratedKpiCount"], 0)

    def test_kpis_y_forecasts_generan_metricas_de_trend(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("TrendMetrics001", "mixed", "small", 30, 1)
        ExpectedMetrics = {"CPU", "RAM", "Storage", "StorageIO", "NetworkIO"}

        self.assertEqual(ExpectedMetrics, {Kpi["MetricName"] for Kpi in Dataset["Kpis"]})
        self.assertEqual(ExpectedMetrics, {Forecast["MetricName"] for Forecast in Dataset["Forecasts"]})
        self.assertTrue(all(Kpi["LoadId"] == "TrendMetrics001" for Kpi in Dataset["Kpis"]))

    def test_historia_sintetica_genera_muestras_diarias(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("HistoryDaily001", "mixed", "small", 30, 1)
        ResourceCount = Dataset["Load"]["GeneratedResourceCount"]
        MetricCount = 9
        ExpectedSamples = ResourceCount * MetricCount * 31
        self.assertEqual(Dataset["Load"]["GeneratedMetricSampleCount"], ExpectedSamples)
        self.assertEqual(len(Dataset["Samples"]), ExpectedSamples)


if __name__ == "__main__":
    unittest.main()
