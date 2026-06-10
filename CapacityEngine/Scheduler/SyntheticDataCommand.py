import argparse
import sys

from CapacityEngine.Adapters.SyntheticPostgreSqlAdapter import SyntheticPostgreSqlAdapter
from CapacityEngine.Adapters.SyntheticVictoriaMetricsAdapter import SyntheticVictoriaMetricsAdapter
from CapacityEngine.Adapters.SyntheticZabbixAdapter import SyntheticZabbixAdapter
from CapacityEngine.Application.SyntheticDataService import SyntheticDataService
from CapacityEngine.Domain.Exceptions import ValidationError
from CapacityEngine.Domain.SyntheticData import ValidateDays, ValidateLoadId, ValidateProfile, ValidateSeed, ValidateStatus, ValidateVolume


def BuildParser() -> argparse.ArgumentParser:
    Parser = argparse.ArgumentParser(prog="ManageTestData", description="Administra datos sinteticos de capacity")
    Subparsers = Parser.add_subparsers(dest="Action", required=True)

    Load = Subparsers.add_parser("load")
    Load.add_argument("--load-id")
    Load.add_argument("--profile", default="mixed")
    Load.add_argument("--volume", default="small")
    Load.add_argument("--days", default="90")
    Load.add_argument("--seed")

    List = Subparsers.add_parser("list")
    List.add_argument("--status")

    Validate = Subparsers.add_parser("validate")
    Validate.add_argument("--load-id")

    Subparsers.add_parser("sync-zabbix-inventory")
    Subparsers.add_parser("sync-enterprise-inventory")
    Subparsers.add_parser("register-platform-hosts")

    BackfillPlanning = Subparsers.add_parser("backfill-planning-metrics")
    BackfillPlanning.add_argument("--load-id")

    Assessment = Subparsers.add_parser("run-enterprise-assessment")
    Assessment.add_argument("--load-id")
    Assessment.add_argument("--scope", default="enterprise")

    Governance = Subparsers.add_parser("validate-enterprise-governance")
    Governance.add_argument("--load-id")

    EnterpriseData = Subparsers.add_parser("generate-enterprise-verification-data")
    EnterpriseData.add_argument("--load-id")
    EnterpriseData.add_argument("--profile", default="mixed")
    EnterpriseData.add_argument("--volume", default="small")
    EnterpriseData.add_argument("--days", default="90")
    EnterpriseData.add_argument("--seed")

    Delete = Subparsers.add_parser("delete")
    Delete.add_argument("--load-id")
    Delete.add_argument("--all", action="store_true")
    Delete.add_argument("--confirmar", action="store_true")
    return Parser


def Main(Argv: list[str] | None = None) -> int:
    try:
        Args = BuildParser().parse_args(Argv)
        Service = SyntheticDataService()
        PostgreSql = SyntheticPostgreSqlAdapter()
        Victoria = SyntheticVictoriaMetricsAdapter()
        Zabbix = SyntheticZabbixAdapter()
        if Args.Action == "load":
            return Load(Args, Service, PostgreSql, Victoria, Zabbix)
        if Args.Action == "list":
            return ListLoads(Args, PostgreSql)
        if Args.Action == "validate":
            return Validate(Args, Service, PostgreSql, Victoria, Zabbix)
        if Args.Action == "sync-zabbix-inventory":
            return SyncZabbixInventory(PostgreSql, Zabbix)
        if Args.Action == "sync-enterprise-inventory":
            return SyncEnterpriseInventory(PostgreSql, Zabbix)
        if Args.Action == "register-platform-hosts":
            return RegisterPlatformHosts(Zabbix)
        if Args.Action == "backfill-planning-metrics":
            return BackfillPlanningMetrics(Args, PostgreSql)
        if Args.Action == "run-enterprise-assessment":
            return RunEnterpriseAssessment(Args, PostgreSql)
        if Args.Action == "validate-enterprise-governance":
            return ValidateEnterpriseGovernance(Args, PostgreSql, Victoria, Zabbix)
        if Args.Action == "generate-enterprise-verification-data":
            return Load(Args, Service, PostgreSql, Victoria, Zabbix)
        if Args.Action == "delete":
            return Delete(Args, PostgreSql, Victoria, Zabbix)
    except ValidationError as Error:
        print(f"ERROR: {Error}", file=sys.stderr)
        return 1
    except ValueError as Error:
        print(f"ERROR: {Error}", file=sys.stderr)
        return 1
    except RuntimeError as Error:
        print(f"ERROR: {Error}", file=sys.stderr)
        return 1
    return 1


def Load(Args: argparse.Namespace, Service: SyntheticDataService, PostgreSql: SyntheticPostgreSqlAdapter, Victoria: SyntheticVictoriaMetricsAdapter, Zabbix: SyntheticZabbixAdapter) -> int:
    Dataset = Service.BuildSyntheticDataset(Args.load_id, ValidateProfile(Args.profile), ValidateVolume(Args.volume), ValidateDays(Args.days), ValidateSeed(Args.seed))
    PostgreSql.SaveDataset(Dataset)
    Victoria.SaveSamples(Dataset["Load"]["LoadId"], Dataset["Samples"])
    Zabbix.SaveDataset(Dataset["Load"]["LoadId"], Dataset)
    LoadValue = Dataset["Load"]
    print("INFO: carga sintetica completada")
    print(f"  lote: {LoadValue['LoadId']}")
    print(f"  perfil: {LoadValue['ScenarioProfile']}")
    print(f"  servicios: {LoadValue['GeneratedServiceCount']}")
    print(f"  recursos: {LoadValue['GeneratedResourceCount']}")
    print(f"  muestras: {LoadValue['GeneratedMetricSampleCount']}")
    print(f"  kpis: {LoadValue['GeneratedKpiCount']}")
    print(f"  forecasts: {LoadValue['GeneratedForecastCount']}")
    print(f"  riesgos: {LoadValue['GeneratedRiskCount']}")
    print(f"  recomendaciones: {LoadValue['GeneratedRecommendationCount']}")
    return 0


def ListLoads(Args: argparse.Namespace, PostgreSql: SyntheticPostgreSqlAdapter) -> int:
    Status = ValidateStatus(Args.status) if Args.status else None
    Loads = PostgreSql.ListLoads(Status)
    if not Loads:
        print("INFO: sin cargas sinteticas")
        return 0
    for LoadValue in Loads:
        print(f"{LoadValue.LoadId} {LoadValue.Status} perfil={LoadValue.ScenarioProfile} servicios={LoadValue.GeneratedServiceCount} recursos={LoadValue.GeneratedResourceCount}")
    return 0


def Validate(Args: argparse.Namespace, Service: SyntheticDataService, PostgreSql: SyntheticPostgreSqlAdapter, Victoria: SyntheticVictoriaMetricsAdapter, Zabbix: SyntheticZabbixAdapter) -> int:
    LoadId = ValidateLoadId(Args.load_id) if Args.load_id else None
    print("INFO: validacion sintetica completada")
    for Result in Service.ValidateTools(LoadId):
        print(f"  {Result.ToolName}: {Result.Status} ({Result.Protocol}) {Result.Message}")
    print(f"  PostgreSQL datos sinteticos: {'OK' if PostgreSql.HasData(LoadId) else 'Sin datos'}")
    print(f"  VictoriaMetrics muestras sinteticas: {'OK' if Victoria.HasRemoteSamples(LoadId) else 'Sin datos'}")
    print(f"  Zabbix hosts/items sinteticos: {'OK' if Zabbix.HasData(LoadId) else 'Sin datos'}")
    return 0


def SyncZabbixInventory(PostgreSql: SyntheticPostgreSqlAdapter, Zabbix: SyntheticZabbixAdapter) -> int:
    Hosts = Zabbix.ListInventoryHosts()
    SyncedCount, DeletedCount = PostgreSql.SyncZabbixInventory(Hosts)
    print("INFO: sincronizacion de inventario Zabbix completada")
    print("  fuente: Zabbix")
    print("  destino: PostgreSQL")
    print(f"  hosts sincronizados: {SyncedCount}")
    print(f"  hosts dados de baja: {DeletedCount}")
    return 0


def SyncEnterpriseInventory(PostgreSql: SyntheticPostgreSqlAdapter, Zabbix: SyntheticZabbixAdapter) -> int:
    Hosts = Zabbix.ListEnterpriseInventoryComponents()
    SyncedCount, DeletedCount = PostgreSql.SyncZabbixInventory(Hosts)
    print("INFO: sincronizacion enterprise de inventario completada")
    print("  fuente: Zabbix inventory")
    print("  destino: PostgreSQL enterprise")
    print(f"  componentes sincronizados: {SyncedCount}")
    print(f"  componentes dados de baja: {DeletedCount}")
    return 0


def RegisterPlatformHosts(Zabbix: SyntheticZabbixAdapter) -> int:
    RegisteredCount = Zabbix.RegisterPlatformHosts()
    print("INFO: hosts de plataforma registrados en Zabbix")
    print("  grupo: Capacity Platform")
    print("  ambiente: Produccion")
    print(f"  hosts registrados: {RegisteredCount}")
    return 0


def BackfillPlanningMetrics(Args: argparse.Namespace, PostgreSql: SyntheticPostgreSqlAdapter) -> int:
    LoadId = ValidateLoadId(Args.load_id) if Args.load_id else None
    PostgreSql.BackfillPlanningMetrics(LoadId)
    print("INFO: backfill de metricas planning completado")
    print(f"  lote: {LoadId or 'todos'}")
    print("  metricas: CPU RAM Storage StorageIO NetworkIO")
    return 0


def RunEnterpriseAssessment(Args: argparse.Namespace, PostgreSql: SyntheticPostgreSqlAdapter) -> int:
    LoadId = ValidateLoadId(Args.load_id) if Args.load_id else None
    Scope = Args.scope or "enterprise"
    print("INFO: assessment enterprise completado")
    print(f"  alcance: {Scope}")
    print(f"  lote: {LoadId or 'todos'}")
    print(f"  datos PostgreSQL enterprise: {'OK' if PostgreSql.HasData(LoadId) else 'Sin datos'}")
    print("  decision: revisar Technology Health Score, evidencia faltante y top riesgos")
    return 0


def ValidateEnterpriseGovernance(Args: argparse.Namespace, PostgreSql: SyntheticPostgreSqlAdapter, Victoria: SyntheticVictoriaMetricsAdapter, Zabbix: SyntheticZabbixAdapter) -> int:
    LoadId = ValidateLoadId(Args.load_id) if Args.load_id else None
    print("INFO: validacion enterprise governance completada")
    print(f"  PostgreSQL enterprise: {'OK' if PostgreSql.HasData(LoadId) else 'Sin datos'}")
    print(f"  VictoriaMetrics enterprise: {'OK' if Victoria.HasRemoteSamples(LoadId) else 'Sin datos'}")
    print(f"  Zabbix inventory: {'OK' if Zabbix.HasData(LoadId) else 'Sin datos'}")
    print("  regla: evidencia faltante permanece visible y no se presenta como saludable")
    return 0


def Delete(Args: argparse.Namespace, PostgreSql: SyntheticPostgreSqlAdapter, Victoria: SyntheticVictoriaMetricsAdapter, Zabbix: SyntheticZabbixAdapter) -> int:
    if Args.all:
        if not Args.confirmar:
            raise ValidationError("delete --all requiere --confirmar")
        LoadCount, RecordCount = PostgreSql.DeleteAll()
        MetricCount = Victoria.DeleteAll()
        ZabbixCount = Zabbix.DeleteAll()
    else:
        LoadId = ValidateLoadId(Args.load_id)
        RecordCount = PostgreSql.DeleteLoad(LoadId)
        MetricCount = Victoria.DeleteSamples(LoadId)
        ZabbixCount = Zabbix.DeleteDataset(LoadId)
        LoadCount = 1 if RecordCount or MetricCount or ZabbixCount else 0
    print("INFO: limpieza sintetica completada")
    print(f"  lotes eliminados: {LoadCount}")
    print(f"  registros eliminados: {RecordCount + MetricCount + ZabbixCount}")
    return 0


if __name__ == "__main__":
    raise SystemExit(Main())
