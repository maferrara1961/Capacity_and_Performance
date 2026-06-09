import json
import os
from pathlib import Path
import subprocess

from CapacityEngine.Domain.SyntheticData import TestLoad


class SyntheticPostgreSqlAdapter:
    def __init__(self, DataDir: str | None = None) -> None:
        self.DataDir = Path(DataDir or os.environ.get("SYNTHETIC_DATA_DIR", ".capacity-test-data"))
        self.DataPath = self.DataDir / "TestLoads.json"

    def LoadStore(self) -> dict:
        if not self.DataPath.exists():
            return {"Loads": {}, "Datasets": {}}
        return json.loads(self.DataPath.read_text(encoding="utf-8"))

    def SaveStore(self, Store: dict) -> None:
        self.DataDir.mkdir(parents=True, exist_ok=True)
        self.DataPath.write_text(json.dumps(Store, indent=2, sort_keys=True), encoding="utf-8")

    def SaveDataset(self, Dataset: dict) -> None:
        Store = self.LoadStore()
        LoadId = Dataset["Load"]["LoadId"]
        if LoadId in Store["Loads"] and Store["Loads"][LoadId]["Status"] != "Deleted":
            raise ValueError("el identificador de lote ya existe")
        if os.environ.get("STACK_DRY_RUN", "0") != "1":
            self.ExecuteSql(self.BuildLoadSql(Dataset))
        Store["Loads"][LoadId] = Dataset["Load"]
        Store["Datasets"][LoadId] = Dataset
        self.SaveStore(Store)

    def ListLoads(self, Status: str | None = None) -> list[TestLoad]:
        Store = self.LoadStore()
        Loads = [TestLoad.FromDict(Value) for Value in Store["Loads"].values() if Value.get("Status") != "Deleted"]
        if Status:
            Loads = [Load for Load in Loads if Load.Status == Status]
        return sorted(Loads, key=lambda Load: Load.CreatedAt)

    def GetDataset(self, LoadId: str) -> dict | None:
        return self.LoadStore()["Datasets"].get(LoadId)

    def DeleteLoad(self, LoadId: str) -> int:
        Store = self.LoadStore()
        Dataset = Store["Datasets"].pop(LoadId, None)
        if LoadId in Store["Loads"]:
            Store["Loads"][LoadId] = TestLoad.FromDict(Store["Loads"][LoadId]).WithStatus("Deleted").ToDict()
        self.SaveStore(Store)
        if os.environ.get("STACK_DRY_RUN", "0") != "1":
            self.ExecuteSql(self.BuildDeleteSql(LoadId))
        return self.CountRecords(Dataset)

    def DeleteAll(self) -> tuple[int, int]:
        Store = self.LoadStore()
        LoadIds = [LoadId for LoadId, Load in Store["Loads"].items() if Load.get("IsTestData") and Load.get("Status") != "Deleted"]
        RecordCount = 0
        for LoadId in LoadIds:
            RecordCount += self.CountRecords(Store["Datasets"].pop(LoadId, None))
            Store["Loads"][LoadId] = TestLoad.FromDict(Store["Loads"][LoadId]).WithStatus("Deleted").ToDict()
        self.SaveStore(Store)
        if os.environ.get("STACK_DRY_RUN", "0") != "1":
            for LoadId in LoadIds:
                self.ExecuteSql(self.BuildDeleteSql(LoadId))
        return len(LoadIds), RecordCount

    def CountRecords(self, Dataset: dict | None) -> int:
        if not Dataset:
            return 0
        return sum(len(Value) for Key, Value in Dataset.items() if Key != "Load" and isinstance(Value, list)) + 1

    def HasData(self, LoadId: str | None = None) -> bool:
        if os.environ.get("STACK_DRY_RUN", "0") != "1":
            return self.HasRemoteData(LoadId)
        if LoadId:
            return self.GetDataset(LoadId) is not None
        return bool(self.ListLoads())

    def HasRemoteData(self, LoadId: str | None = None) -> bool:
        Where = ""
        if LoadId:
            SafeLoadId = LoadId.replace("'", "''")
            Where = f" where LoadId = '{SafeLoadId}'"
        Sql = f"select exists(select 1 from TestLoad{Where});"
        Result = self.ExecuteSqlQuery(Sql)
        return Result.lower() in {"t", "true", "1"}

    def SyncZabbixInventory(self, Hosts: list[dict]) -> tuple[int, int]:
        if os.environ.get("STACK_DRY_RUN", "0") != "1":
            self.ExecuteSql(self.BuildZabbixInventorySyncSql(Hosts))
        return len(Hosts), 0

    def BuildZabbixInventorySyncSql(self, Hosts: list[dict]) -> str:
        Lines = [
            (Path("Sql/Schema/001_Catalog.sql")).read_text(encoding="utf-8"),
            "begin;",
        ]
        HostNames = []
        for Host in Hosts:
            HostName = Host["HostName"]
            HostNames.append(HostName)
            Status = Host.get("Status", "OK")
            ResourceType = Host.get("Type", "Server") or "Server"
            Notes = Host.get("Notes", "")
            Lines.append(
                "insert into MonitoredResource (ResourceId, ResourceType, Name, Platform, CapacityUnit, TotalCapacity, Status) values "
                f"({self.Q(HostName)}, {self.Q(ResourceType)}, {self.Q(HostName)}, {self.Q('ZabbixInventory')}, "
                f"{self.Q('Percent')}, 100, {self.Q(Status)}) "
                "on conflict (ResourceId) do update set "
                "ResourceType = excluded.ResourceType, "
                "Name = excluded.Name, "
                "Platform = excluded.Platform, "
                "CapacityUnit = excluded.CapacityUnit, "
                "TotalCapacity = excluded.TotalCapacity, "
                "Status = excluded.Status;"
            )
            Lines.append(
                "insert into Baseline (BaselineId, ResourceId, MetricName, PeriodStart, PeriodEnd, AverageValue, P95Value, PeakValue) values "
                f"({self.Q('ZabbixInventory-' + HostName)}, {self.Q(HostName)}, {self.Q('Inventory')}, now(), now(), 0, 0, 0) "
                "on conflict (BaselineId) do update set PeriodEnd = now(), AverageValue = 0, P95Value = 0, PeakValue = 0;"
            )
            if Notes:
                Lines.append(f"-- inventory notes {self.Q(HostName)}: {self.Q(Notes)}")
        if HostNames:
            Values = ", ".join(self.Q(HostName) for HostName in HostNames)
            Lines.append(f"delete from Baseline where BaselineId like 'ZabbixInventory-%' and ResourceId not in ({Values});")
            Lines.append(f"delete from MonitoredResource where Platform = 'ZabbixInventory' and ResourceId not in ({Values});")
        else:
            Lines.append("delete from Baseline where BaselineId like 'ZabbixInventory-%';")
            Lines.append("delete from MonitoredResource where Platform = 'ZabbixInventory';")
        Lines.append("commit;")
        return "\n".join(Lines)

    def ExecuteSql(self, Sql: str) -> None:
        PodmanBin = os.environ.get("PODMAN_BIN", "podman")
        Container = os.environ.get("POSTGRES_CONTAINER", "capacity-performance-postgresql")
        Command = [PodmanBin, "exec", "-i", Container, "psql", "-U", "capacity", "-d", "capacity", "-v", "ON_ERROR_STOP=1"]
        Result = subprocess.run(Command, input=Sql, text=True, capture_output=True)
        if Result.returncode != 0:
            raise RuntimeError(f"PostgreSQL rechazo la carga sintetica: {Result.stderr.strip()}")

    def ExecuteSqlQuery(self, Sql: str) -> str:
        PodmanBin = os.environ.get("PODMAN_BIN", "podman")
        Container = os.environ.get("POSTGRES_CONTAINER", "capacity-performance-postgresql")
        Command = [PodmanBin, "exec", "-i", Container, "psql", "-U", "capacity", "-d", "capacity", "-tAc", Sql]
        Result = subprocess.run(Command, text=True, capture_output=True)
        if Result.returncode != 0:
            raise RuntimeError(f"PostgreSQL rechazo la validacion sintetica: {Result.stderr.strip()}")
        return Result.stdout.strip()

    def BuildLoadSql(self, Dataset: dict) -> str:
        Lines = [
            (Path("Sql/Schema/001_Catalog.sql")).read_text(encoding="utf-8"),
            (Path("Sql/Schema/002_CapacityOutputs.sql")).read_text(encoding="utf-8"),
            (Path("Sql/Schema/003_TestDataLoads.sql")).read_text(encoding="utf-8"),
            self.BuildEnterpriseSchemaSql(),
        ]
        Load = Dataset["Load"]
        Lines.append(
            "insert into TestLoad (LoadId, ScenarioProfile, RequestedVolume, CreatedAt, FinishedAt, Status, "
            "GeneratedServiceCount, GeneratedResourceCount, GeneratedMetricSampleCount, GeneratedKpiCount, "
            "GeneratedForecastCount, GeneratedRiskCount, GeneratedRecommendationCount, ErrorMessage, IsTestData) "
            f"values ({self.Q(Load['LoadId'])}, {self.Q(Load['ScenarioProfile'])}, {self.Q(Load['RequestedVolume'])}, "
            f"{self.Q(Load['CreatedAt'])}, {self.Q(Load['FinishedAt'])}, {self.Q(Load['Status'])}, "
            f"{Load['GeneratedServiceCount']}, {Load['GeneratedResourceCount']}, {Load['GeneratedMetricSampleCount']}, "
            f"{Load['GeneratedKpiCount']}, {Load['GeneratedForecastCount']}, {Load['GeneratedRiskCount']}, "
            f"{Load['GeneratedRecommendationCount']}, {self.Q(Load['ErrorMessage'])}, true) "
            "on conflict (LoadId) do update set Status = excluded.Status;"
        )
        for Service in Dataset["Services"]:
            Lines.append(
                "insert into Service (ServiceId, Name, Owner, Criticality, Status) values "
                f"({self.Q(Service['ServiceId'])}, {self.Q(Service['Name'])}, {self.Q(Service['Owner'])}, "
                f"{self.Q(Service['Criticality'])}, {self.Q(Service['Status'])}) on conflict (ServiceId) do nothing;"
            )
        for Index, Service in enumerate(Dataset["Services"], start=1):
            ApplicationId = f"{Load['LoadId']}-Application-{Index}"
            Lines.append(
                "insert into Application (ApplicationId, ServiceId, Name, Environment, HealthStatus, EndToEndPerformanceStatus) values "
                f"({self.Q(ApplicationId)}, {self.Q(Service['ServiceId'])}, {self.Q('Aplicacion Sintetica ' + str(Index))}, "
                f"{self.Q('Demo')}, {self.Q(Service['Status'])}, {self.Q(Service['Status'])}) on conflict (ApplicationId) do nothing;"
            )
        for Resource in Dataset["Resources"]:
            Lines.append(
                "insert into MonitoredResource (ResourceId, ResourceType, Name, Platform, CapacityUnit, TotalCapacity, Status) values "
                f"({self.Q(Resource['ResourceId'])}, {self.Q(Resource['ResourceType'])}, {self.Q(Resource['Name'])}, "
                f"{self.Q(Resource['Platform'])}, {self.Q(Resource['CapacityUnit'])}, {Resource['TotalCapacity']}, {self.Q(Resource['Status'])}) "
                "on conflict (ResourceId) do nothing;"
            )
        for Index, Resource in enumerate(Dataset["Resources"], start=1):
            ServiceIndex = (Index - 1) % len(Dataset["Services"])
            Service = Dataset["Services"][ServiceIndex]
            ApplicationId = f"{Load['LoadId']}-Application-{ServiceIndex + 1}"
            Lines.append(
                "insert into ServiceResourceMap (MapId, ServiceId, ApplicationId, ResourceId, Role, ImpactWeight) values "
                f"({self.Q(Load['LoadId'] + '-Map-' + str(Index))}, {self.Q(Service['ServiceId'])}, {self.Q(ApplicationId)}, "
                f"{self.Q(Resource['ResourceId'])}, {self.Q(Resource['ResourceType'])}, 50) on conflict (MapId) do nothing;"
            )
        for Kpi in Dataset["Kpis"]:
            Lines.append(
                "insert into CapacityKpi (CapacityKpiId, LoadId, ResourceId, MetricName, CalculatedAt, WindowStart, WindowEnd, "
                "AverageUtilization, PeakUtilization, P95Utilization, MonthlyGrowthRate, HeadroomAvailable, BaselineDelta) values "
                f"({self.Q(Kpi['KpiId'])}, {self.Q(Kpi['LoadId'])}, {self.Q(Kpi['ResourceId'])}, {self.Q(Kpi['MetricName'])}, {self.Q(Kpi['CalculatedAt'])}, "
                f"{self.Q(Kpi['CalculatedAt'])}, {self.Q(Kpi['CalculatedAt'])}, {Kpi['AverageUtilization']}, {Kpi['PeakUtilization']}, "
                f"{Kpi['P95Utilization']}, {Kpi['MonthlyGrowthRate']}, {Kpi['HeadroomAvailable']}, 0) on conflict (CapacityKpiId) do nothing;"
            )
        for Forecast in Dataset["Forecasts"]:
            Lines.append(
                "insert into ForecastResult (ForecastResultId, LoadId, ResourceId, MetricName, CalculatedAt, Forecast30Days, Forecast60Days, "
                "Forecast90Days, Forecast180Days, Forecast365Days, DaysToSaturation, Confidence) values "
                f"({self.Q(Forecast['ForecastId'])}, {self.Q(Forecast['LoadId'])}, {self.Q(Forecast['ResourceId'])}, {self.Q(Forecast['MetricName'])}, "
                f"{self.Q(Forecast['CalculatedAt'])}, {Forecast['Forecast30Days']}, {Forecast['Forecast60Days']}, "
                f"{Forecast['Forecast90Days']}, {Forecast['Forecast180Days']}, {Forecast['Forecast365Days']}, "
                f"{Forecast['DaysToSaturation']}, {self.Q(Forecast['Confidence'])}) "
                "on conflict (ForecastResultId) do nothing;"
            )
        for Risk in Dataset["Risks"]:
            Lines.append(
                "insert into RiskAssessment (RiskAssessmentId, ScopeType, ScopeId, OverallRisk, Reason, CalculatedAt) values "
                f"({self.Q(Risk['RiskAssessmentId'])}, {self.Q(Risk['ScopeType'])}, {self.Q(Risk['ScopeId'])}, "
                f"{self.Q(Risk['OverallRisk'])}, {self.Q(Risk['Reason'])}, {self.Q(Risk['CalculatedAt'])}) "
                "on conflict (RiskAssessmentId) do nothing;"
            )
        for Recommendation in Dataset["Recommendations"]:
            Lines.append(
                "insert into Recommendation (RecommendationId, RiskAssessmentId, ScopeType, ScopeId, Priority, Action, Reason, Status) values "
                f"({self.Q(Recommendation['RecommendationId'])}, {self.Q(Recommendation['RiskAssessmentId'])}, {self.Q(Recommendation['ScopeType'])}, "
                f"{self.Q(Recommendation['ScopeId'])}, {self.Q(Recommendation['Priority'])}, {self.Q(Recommendation['Action'])}, "
                f"{self.Q(Recommendation['Reason'])}, {self.Q(Recommendation['Status'])}) on conflict (RecommendationId) do nothing;"
            )
        self.AppendEnterpriseLoadSql(Lines, Dataset)
        return "\n".join(Lines)

    def BuildEnterpriseSchemaSql(self) -> str:
        return """
create table if not exists EnterpriseTechnologyDomain (
  DomainId text primary key,
  LoadId text not null,
  Name text not null,
  Description text not null,
  Status text not null
);
create table if not exists EnterpriseTechnologyComponent (
  ComponentId text primary key,
  LoadId text not null,
  ComponentName text not null,
  TechnologyType text not null,
  DomainId text not null,
  DomainName text not null,
  Version text not null,
  Vendor text not null,
  Environment text not null,
  BusinessServiceId text,
  Owner text not null,
  SupportStatus text not null,
  LifecycleStatus text not null,
  LicenseStatus text not null default 'Unknown',
  ComplianceStatus text not null default 'Unknown',
  BacklevelStatus text not null default 'Unknown',
  EndOfSupportDate date,
  EvidenceState text not null
);
alter table EnterpriseTechnologyComponent add column if not exists LicenseStatus text not null default 'Unknown';
alter table EnterpriseTechnologyComponent add column if not exists ComplianceStatus text not null default 'Unknown';
alter table EnterpriseTechnologyComponent add column if not exists BacklevelStatus text not null default 'Unknown';
alter table EnterpriseTechnologyComponent add column if not exists EndOfSupportDate date;
create table if not exists EnterpriseEvidenceRecord (
  EvidenceId text primary key,
  LoadId text not null,
  SourceSystem text not null,
  EvidenceType text not null,
  ComponentId text,
  BusinessServiceId text,
  ObservedAt timestamptz not null,
  FreshnessStatus text not null,
  EvidenceState text not null,
  EvidenceReference text not null
);
create table if not exists EnterpriseScoreAssessment (
  ScoreAssessmentId text primary key,
  LoadId text not null,
  AssessmentRunId text not null,
  ScoreType text not null,
  ScopeType text not null,
  ScopeId text not null,
  ScoreValue numeric not null,
  Classification text not null,
  EvidenceState text not null,
  CalculatedAt timestamptz not null
);
create table if not exists EnterpriseRiskRegistryEntry (
  RiskId text primary key,
  LoadId text not null,
  RiskCategory text not null,
  Severity text not null,
  Impact text not null,
  AffectedTechnologyId text not null,
  AffectedServiceId text,
  RecommendedAction text not null,
  Owner text not null,
  EvidenceState text not null,
  Status text not null
);
create table if not exists EnterpriseRecommendation (
  RecommendationId text primary key,
  LoadId text not null,
  RiskId text not null,
  Priority text not null,
  Action text not null,
  Rationale text not null,
  DecisionOwner text not null,
  Status text not null
);
"""

    def AppendEnterpriseLoadSql(self, Lines: list[str], Dataset: dict) -> None:
        for Domain in Dataset.get("EnterpriseDomains", []):
            Lines.append(
                "insert into EnterpriseTechnologyDomain (DomainId, LoadId, Name, Description, Status) values "
                f"({self.Q(Domain['DomainId'])}, {self.Q(Domain['LoadId'])}, {self.Q(Domain['Name'])}, {self.Q(Domain['Description'])}, {self.Q(Domain['Status'])}) "
                "on conflict (DomainId) do nothing;"
            )
        for Component in Dataset.get("EnterpriseComponents", []):
            Lines.append(
                "insert into EnterpriseTechnologyComponent (ComponentId, LoadId, ComponentName, TechnologyType, DomainId, DomainName, Version, Vendor, Environment, BusinessServiceId, Owner, SupportStatus, LifecycleStatus, LicenseStatus, ComplianceStatus, BacklevelStatus, EndOfSupportDate, EvidenceState) values "
                f"({self.Q(Component['ComponentId'])}, {self.Q(Component['LoadId'])}, {self.Q(Component['ComponentName'])}, {self.Q(Component['TechnologyType'])}, "
                f"{self.Q(Component['DomainId'])}, {self.Q(Component['DomainName'])}, {self.Q(Component['Version'])}, {self.Q(Component['Vendor'])}, "
                f"{self.Q(Component['Environment'])}, {self.Q(Component['BusinessServiceId'])}, {self.Q(Component['Owner'])}, {self.Q(Component['SupportStatus'])}, "
                f"{self.Q(Component['LifecycleStatus'])}, {self.Q(Component['LicenseStatus'])}, {self.Q(Component['ComplianceStatus'])}, "
                f"{self.Q(Component['BacklevelStatus'])}, {self.Q(Component['EndOfSupportDate'])}, {self.Q(Component['EvidenceState'])}) "
                "on conflict (ComponentId) do update set "
                "SupportStatus = excluded.SupportStatus, "
                "LifecycleStatus = excluded.LifecycleStatus, "
                "LicenseStatus = excluded.LicenseStatus, "
                "ComplianceStatus = excluded.ComplianceStatus, "
                "BacklevelStatus = excluded.BacklevelStatus, "
                "EndOfSupportDate = excluded.EndOfSupportDate, "
                "EvidenceState = excluded.EvidenceState;"
            )
        for Evidence in Dataset.get("EnterpriseEvidence", []):
            Lines.append(
                "insert into EnterpriseEvidenceRecord (EvidenceId, LoadId, SourceSystem, EvidenceType, ComponentId, BusinessServiceId, ObservedAt, FreshnessStatus, EvidenceState, EvidenceReference) values "
                f"({self.Q(Evidence['EvidenceId'])}, {self.Q(Evidence['LoadId'])}, {self.Q(Evidence['SourceSystem'])}, {self.Q(Evidence['EvidenceType'])}, "
                f"{self.Q(Evidence['ComponentId'])}, {self.Q(Evidence['BusinessServiceId'])}, {self.Q(Evidence['ObservedAt'])}, {self.Q(Evidence['FreshnessStatus'])}, "
                f"{self.Q(Evidence['EvidenceState'])}, {self.Q(Evidence['EvidenceReference'])}) on conflict (EvidenceId) do nothing;"
            )
        for Score in Dataset.get("EnterpriseScores", []):
            Lines.append(
                "insert into EnterpriseScoreAssessment (ScoreAssessmentId, LoadId, AssessmentRunId, ScoreType, ScopeType, ScopeId, ScoreValue, Classification, EvidenceState, CalculatedAt) values "
                f"({self.Q(Score['ScoreAssessmentId'])}, {self.Q(Score['LoadId'])}, {self.Q(Score['AssessmentRunId'])}, {self.Q(Score['ScoreType'])}, "
                f"{self.Q(Score['ScopeType'])}, {self.Q(Score['ScopeId'])}, {Score['ScoreValue']}, {self.Q(Score['Classification'])}, "
                f"{self.Q(Score['EvidenceState'])}, {self.Q(Score['CalculatedAt'])}) on conflict (ScoreAssessmentId) do nothing;"
            )
        for Risk in Dataset.get("EnterpriseRiskRegistry", []):
            Lines.append(
                "insert into EnterpriseRiskRegistryEntry (RiskId, LoadId, RiskCategory, Severity, Impact, AffectedTechnologyId, AffectedServiceId, RecommendedAction, Owner, EvidenceState, Status) values "
                f"({self.Q(Risk['RiskId'])}, {self.Q(Risk['LoadId'])}, {self.Q(Risk['RiskCategory'])}, {self.Q(Risk['Severity'])}, {self.Q(Risk['Impact'])}, "
                f"{self.Q(Risk['AffectedTechnologyId'])}, {self.Q(Risk['AffectedServiceId'])}, {self.Q(Risk['RecommendedAction'])}, {self.Q(Risk['Owner'])}, "
                f"{self.Q(Risk['EvidenceState'])}, {self.Q(Risk['Status'])}) on conflict (RiskId) do nothing;"
            )
        for Recommendation in Dataset.get("EnterpriseRecommendations", []):
            Lines.append(
                "insert into EnterpriseRecommendation (RecommendationId, LoadId, RiskId, Priority, Action, Rationale, DecisionOwner, Status) values "
                f"({self.Q(Recommendation['RecommendationId'])}, {self.Q(Recommendation['LoadId'])}, {self.Q(Recommendation['RiskId'])}, "
                f"{self.Q(Recommendation['Priority'])}, {self.Q(Recommendation['Action'])}, {self.Q(Recommendation['Rationale'])}, "
                f"{self.Q(Recommendation['DecisionOwner'])}, {self.Q(Recommendation['Status'])}) on conflict (RecommendationId) do nothing;"
            )

    def BuildDeleteSql(self, LoadId: str) -> str:
        Prefix = self.Q(f"{LoadId}%")
        Exact = self.Q(LoadId)
        return "\n".join(
            [
                f"delete from Recommendation where RecommendationId like {Prefix};",
                f"delete from EnterpriseRecommendation where LoadId = {Exact};",
                f"delete from EnterpriseRiskRegistryEntry where LoadId = {Exact};",
                f"delete from EnterpriseScoreAssessment where LoadId = {Exact};",
                f"delete from EnterpriseEvidenceRecord where LoadId = {Exact};",
                f"delete from EnterpriseTechnologyComponent where LoadId = {Exact};",
                f"delete from EnterpriseTechnologyDomain where LoadId = {Exact};",
                f"delete from RiskAssessment where RiskAssessmentId like {Prefix};",
                f"delete from ForecastResult where ForecastResultId like {Prefix};",
                f"delete from CapacityKpi where CapacityKpiId like {Prefix};",
                f"delete from ServiceResourceMap where MapId like {Prefix};",
                f"delete from Application where ApplicationId like {Prefix};",
                f"delete from MonitoredResource where ResourceId like {Prefix};",
                f"delete from Service where ServiceId like {Prefix};",
                f"delete from TestDataRecordMap where LoadId = {Exact};",
                f"delete from TestLoad where LoadId = {Exact};",
            ]
        )

    def Q(self, Value: str) -> str:
        return "'" + str(Value).replace("'", "''") + "'"
