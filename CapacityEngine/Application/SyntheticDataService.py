from datetime import UTC, datetime, timedelta
import random

from CapacityEngine.Application.EnterpriseScoringService import EnterpriseScoringService
from CapacityEngine.Domain.EnterpriseConstants import EvidenceState
from CapacityEngine.Domain.SyntheticData import BuildToolValidationResult, TestLoad, ValidateDays, ValidateLoadId, ValidateProfile, ValidateSeed, ValidateVolume


class SyntheticDataService:
    VolumeScale = {"small": 3, "medium": 8, "large": 15}

    def GenerateLoadId(self) -> str:
        return f"Load{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"

    def BuildSyntheticDataset(self, LoadId: str | None, Profile: str, Volume: str, Days: int, Seed: int | None) -> dict:
        Profile = ValidateProfile(Profile)
        Volume = ValidateVolume(Volume)
        Days = ValidateDays(Days)
        Seed = ValidateSeed(Seed)
        LoadId = ValidateLoadId(LoadId or self.GenerateLoadId())
        Random = random.Random(f"{Seed}-{LoadId}" if Seed is not None else LoadId)
        ResourceCount = self.VolumeScale[Volume]
        ServiceCount = max(1, ResourceCount // 2)
        Load = TestLoad.Create(LoadId, Profile, Volume).WithStatus("Running")
        Services = self.BuildServices(LoadId, ServiceCount, Profile)
        Resources = self.BuildResources(LoadId, ResourceCount, Profile, Random)
        Samples = self.BuildSamples(LoadId, Services, Resources, Profile, Days, Random)
        Kpis = self.BuildKpis(LoadId, Resources, Profile, Random)
        Forecasts = self.BuildForecasts(LoadId, Resources, Profile, Random)
        Risks = self.BuildRisks(LoadId, Resources, Profile)
        Recommendations = self.BuildRecommendations(LoadId, Risks)
        Enterprise = self.BuildEnterpriseOutputs(LoadId, Services, Resources, Profile, Random)
        Load = Load.WithCounts(len(Services), len(Resources), len(Samples), len(Kpis), len(Forecasts), len(Risks), len(Recommendations)).WithStatus("Succeeded")
        return {
            "Load": Load.ToDict(),
            "Services": Services,
            "Resources": Resources,
            "Samples": Samples,
            "Kpis": Kpis,
            "Forecasts": Forecasts,
            "Risks": Risks,
            "Recommendations": Recommendations,
            **Enterprise,
        }

    def BuildServices(self, LoadId: str, Count: int, Profile: str) -> list[dict]:
        Criticalities = ["Low", "Medium", "High", "Critical"]
        return [
            {
                "ServiceId": f"{LoadId}-Service-{Index}",
                "LoadId": LoadId,
                "Name": f"Servicio Sintetico {LoadId} {Index}",
                "Owner": "CapacityLab",
                "Criticality": Criticalities[Index % len(Criticalities)],
                "Status": self.StatusFor(Profile),
                "IsTestData": True,
            }
            for Index in range(1, Count + 1)
        ]

    def BuildResources(self, LoadId: str, Count: int, Profile: str, Random: random.Random) -> list[dict]:
        Types = ["Server", "Database", "Storage", "Network", "Dependency"]
        UsedHostNumbers = set()
        Resources = []
        for Index in range(1, Count + 1):
            HostNumber = self.RandomHostNumber(Random, UsedHostNumbers)
            HostName = f"SRV-{HostNumber}"
            ResourceType = Types[(Index - 1) % len(Types)]
            Resources.append(
                {
                    "ResourceId": f"{LoadId}-Resource-{Index}",
                    "LoadId": LoadId,
                    "ResourceType": ResourceType,
                    "Name": HostName,
                    "Platform": "PodmanLab",
                    "CapacityUnit": "Percent",
                    "TotalCapacity": 100.0,
                    "Status": self.StatusFor(Profile),
                    "Inventory": self.BuildInventory(LoadId, HostName, ResourceType, Index),
                    "IsTestData": True,
                }
            )
        return Resources

    def RandomHostNumber(self, Random: random.Random, UsedHostNumbers: set[int]) -> int:
        while True:
            HostNumber = Random.randint(10000, 99999)
            if HostNumber not in UsedHostNumbers:
                UsedHostNumbers.add(HostNumber)
                return HostNumber

    def BuildInventory(self, LoadId: str, HostName: str, ResourceType: str, Index: int) -> dict:
        return {
            "AssetTag": f"{LoadId}-{Index}",
            "Alias": HostName,
            "Type": ResourceType,
            "Os": "Linux",
            "Location": "CapacityLab",
            "Notes": f"Host sintetico {HostName} generado para pruebas de capacity y performance",
        }

    def BuildSamples(self, LoadId: str, Services: list[dict], Resources: list[dict], Profile: str, Days: int, Random: random.Random) -> list[dict]:
        Metrics = ["CPU", "RAM", "Storage", "IOPS", "Network", "Latency", "Throughput", "Errors", "Saturation"]
        Samples = []
        Now = datetime.now(UTC)
        for ResourceIndex, Resource in enumerate(Resources):
            Service = Services[ResourceIndex % len(Services)]
            for Metric in Metrics:
                for Offset in range(Days, -1, -1):
                    ObservedAt = Now - timedelta(days=Offset)
                    Samples.append(
                        {
                            "SampleId": f"{LoadId}-{Resource['ResourceId']}-{Metric}-{Offset}",
                            "LoadId": LoadId,
                            "ResourceId": Resource["ResourceId"],
                            "HostName": Resource["Name"],
                            "TechnologyDomain": self.DomainForResource(Resource),
                            "BusinessService": Service["Name"],
                            "BusinessServiceId": Service["ServiceId"],
                            "MetricName": Metric,
                            "ObservedAt": ObservedAt.isoformat(),
                            "Value": round(self.ValueFor(Profile, Offset, Days, Random), 2),
                            "Unit": "Percent" if Metric not in {"Latency", "Throughput", "Errors"} else "Count",
                            "Source": "Synthetic",
                            "IsTestData": True,
                        }
                    )
        return Samples

    def DomainForResource(self, Resource: dict) -> str:
        Mapping = {
            "Server": "Infrastructure",
            "Database": "Database",
            "Storage": "Infrastructure",
            "Network": "Infrastructure",
            "Dependency": "EnterpriseApplication",
        }
        return Mapping.get(Resource.get("ResourceType"), "Infrastructure")

    def BuildKpis(self, LoadId: str, Resources: list[dict], Profile: str, Random: random.Random) -> list[dict]:
        return [self.BuildMetricOutput(LoadId, Resource, "Kpi", Profile, Random) for Resource in Resources]

    def BuildForecasts(self, LoadId: str, Resources: list[dict], Profile: str, Random: random.Random) -> list[dict]:
        return [self.BuildMetricOutput(LoadId, Resource, "Forecast", Profile, Random) for Resource in Resources]

    def BuildRisks(self, LoadId: str, Resources: list[dict], Profile: str) -> list[dict]:
        return [
            {
                "RiskAssessmentId": f"{LoadId}-Risk-{Index}",
                "LoadId": LoadId,
                "ScopeType": "Resource",
                "ScopeId": Resource["ResourceId"],
                "OverallRisk": self.StatusFor(Profile),
                "Reason": f"Escenario sintetico {Profile}",
                "CalculatedAt": datetime.now(UTC).isoformat(),
                "IsTestData": True,
            }
            for Index, Resource in enumerate(Resources, start=1)
        ]

    def BuildRecommendations(self, LoadId: str, Risks: list[dict]) -> list[dict]:
        return [
            {
                "RecommendationId": f"{Risk['RiskAssessmentId']}-Recommendation",
                "LoadId": LoadId,
                "RiskAssessmentId": Risk["RiskAssessmentId"],
                "ScopeType": Risk["ScopeType"],
                "ScopeId": Risk["ScopeId"],
                "Priority": "High" if Risk["OverallRisk"] == "Critical" else "Medium",
                "Action": f"Revisar capacidad del host asociado por riesgo {Risk['OverallRisk']}",
                "Reason": Risk["Reason"],
                "Status": "Open",
                "IsTestData": True,
            }
            for Risk in Risks
        ]

    def BuildMetricOutput(self, LoadId: str, Resource: dict, Kind: str, Profile: str, Random: random.Random) -> dict:
        Base = self.ValueFor(Profile, 0, 90, Random)
        return {
            f"{Kind}Id": f"{LoadId}-{Kind}-{Resource['ResourceId']}",
            "LoadId": LoadId,
            "ResourceId": Resource["ResourceId"],
            "MetricName": "CPU",
            "CalculatedAt": datetime.now(UTC).isoformat(),
            "AverageUtilization": round(max(0, Base - 8), 2),
            "PeakUtilization": round(min(100, Base + 8), 2),
            "P95Utilization": round(min(100, Base + 5), 2),
            "MonthlyGrowthRate": round(Random.uniform(1, 12), 2),
            "HeadroomAvailable": round(max(0, 100 - Base), 2),
            "Forecast30Days": round(min(100, Base + 5), 2),
            "Forecast60Days": round(min(100, Base + 10), 2),
            "Forecast90Days": round(min(100, Base + 15), 2),
            "Forecast180Days": round(min(100, Base + 25), 2),
            "Forecast365Days": round(min(100, Base + 35), 2),
            "DaysToSaturation": 90 if Base < 85 else 30,
            "Confidence": "High",
            "IsTestData": True,
        }

    def BuildEnterpriseOutputs(self, LoadId: str, Services: list[dict], Resources: list[dict], Profile: str, Random: random.Random) -> dict:
        Scoring = EnterpriseScoringService()
        EvidenceStates = [State.value for State in EvidenceState]
        Domains = [
            {"DomainId": f"{LoadId}-Domain-Infrastructure", "LoadId": LoadId, "Name": "Infrastructure", "Description": "Infraestructura", "Status": "Active", "IsTestData": True},
            {"DomainId": f"{LoadId}-Domain-Database", "LoadId": LoadId, "Name": "Database", "Description": "Bases de datos", "Status": "Active", "IsTestData": True},
            {"DomainId": f"{LoadId}-Domain-Monitoring", "LoadId": LoadId, "Name": "MonitoringPlatform", "Description": "Monitoreo", "Status": "Active", "IsTestData": True},
        ]
        Components = []
        Evidence = []
        Scores = []
        RiskRegistry = []
        Recommendations = []
        LicenseStatuses = ["Compliant", "NonCompliant", "Unverified", "Unknown"]
        ComplianceStatuses = ["Compliant", "NonCompliant", "AttentionRequired", "Unknown"]
        BacklevelStatuses = ["Current", "Backlevel", "Backlevel", "Current"]
        LifecycleStatuses = ["Supported", "EndOfSupport", "EndOfLife", "Backlevel"]
        for Index, Resource in enumerate(Resources, start=1):
            Domain = Domains[(Index - 1) % len(Domains)]
            Service = Services[(Index - 1) % len(Services)]
            EvidenceStateValue = EvidenceStates[(Index - 1) % len(EvidenceStates)]
            LicenseStatus = LicenseStatuses[(Index - 1) % len(LicenseStatuses)]
            ComplianceStatus = ComplianceStatuses[(Index - 1) % len(ComplianceStatuses)]
            BacklevelStatus = BacklevelStatuses[(Index - 1) % len(BacklevelStatuses)]
            LifecycleStatus = LifecycleStatuses[(Index - 1) % len(LifecycleStatuses)]
            EndOfSupportDate = (datetime.now(UTC) + timedelta(days=365 - (Index * 120))).date().isoformat()
            BaseScore = max(5, 100 - self.ValueFor(Profile, 0, 90, Random))
            AdjustedScore = Scoring.EvidenceAdjustedScore(BaseScore, EvidenceState(EvidenceStateValue))
            Classification = Scoring.Classify(AdjustedScore, EvidenceState(EvidenceStateValue)).value
            ComponentId = f"{LoadId}-Component-{Index}"
            Components.append(
                {
                    "ComponentId": ComponentId,
                    "LoadId": LoadId,
                    "ComponentName": Resource["Name"],
                    "TechnologyType": Resource["ResourceType"],
                    "DomainId": Domain["DomainId"],
                    "DomainName": Domain["Name"],
                    "Version": "1.0",
                    "Vendor": "Synthetic",
                    "Environment": "Demo",
                    "BusinessServiceId": Service["ServiceId"],
                    "Owner": Service["Owner"],
                    "SupportStatus": "Unknown" if EvidenceStateValue == "Missing" else LifecycleStatus,
                    "LifecycleStatus": "Unknown" if EvidenceStateValue == "Missing" else LifecycleStatus,
                    "LicenseStatus": LicenseStatus,
                    "ComplianceStatus": ComplianceStatus,
                    "BacklevelStatus": BacklevelStatus,
                    "EndOfSupportDate": EndOfSupportDate,
                    "EvidenceState": EvidenceStateValue,
                    "IsTestData": True,
                }
            )
            Evidence.append(
                {
                    "EvidenceId": f"{LoadId}-Evidence-{Index}",
                    "LoadId": LoadId,
                    "SourceSystem": "SyntheticDataset",
                    "EvidenceType": "Telemetry",
                    "ComponentId": ComponentId,
                    "BusinessServiceId": Service["ServiceId"],
                    "ObservedAt": datetime.now(UTC).isoformat(),
                    "FreshnessStatus": "Fresh" if EvidenceStateValue == "Available" else "Unknown",
                    "EvidenceState": EvidenceStateValue,
                    "EvidenceReference": f"synthetic:{LoadId}:{ComponentId}",
                    "IsTestData": True,
                }
            )
            for ScoreType in ["Capacity", "Performance", "Availability", "Lifecycle", "Compliance", "MonitoringConfidence"]:
                Scores.append(
                    {
                        "ScoreAssessmentId": f"{LoadId}-Score-{ScoreType}-{Index}",
                        "LoadId": LoadId,
                        "AssessmentRunId": f"{LoadId}-EnterpriseRun",
                        "ScoreType": ScoreType,
                        "ScopeType": "TechnologyComponent",
                        "ScopeId": ComponentId,
                        "ScoreValue": AdjustedScore,
                        "Classification": Classification,
                        "EvidenceState": EvidenceStateValue,
                        "CalculatedAt": datetime.now(UTC).isoformat(),
                        "IsTestData": True,
                    }
                )
            HealthScore = Scoring.TechnologyHealthScore([AdjustedScore] * 5, AdjustedScore)
            Scores.append(
                {
                    "ScoreAssessmentId": f"{LoadId}-Score-TechnologyHealth-{Index}",
                    "LoadId": LoadId,
                    "AssessmentRunId": f"{LoadId}-EnterpriseRun",
                    "ScoreType": "TechnologyHealth",
                    "ScopeType": "TechnologyComponent",
                    "ScopeId": ComponentId,
                    "ScoreValue": HealthScore,
                    "Classification": Scoring.Classify(HealthScore, EvidenceState(EvidenceStateValue)).value,
                    "EvidenceState": EvidenceStateValue,
                    "CalculatedAt": datetime.now(UTC).isoformat(),
                    "IsTestData": True,
                }
            )
            Severity = "Critical" if AdjustedScore < 40 else "High" if AdjustedScore < 60 else "Medium" if AdjustedScore < 75 else "Low"
            RiskId = f"{LoadId}-EnterpriseRisk-{Index}"
            RiskRegistry.append(
                {
                    "RiskId": RiskId,
                    "LoadId": LoadId,
                    "RiskCategory": "Capacity",
                    "Severity": Severity,
                    "Impact": f"Riesgo enterprise sobre {Resource['Name']}",
                    "AffectedTechnologyId": ComponentId,
                    "AffectedServiceId": Service["ServiceId"],
                    "RecommendedAction": "Revisar evidencia, capacidad y plan de mitigacion",
                    "Owner": Service["Owner"],
                    "EvidenceState": EvidenceStateValue,
                    "Status": "Open",
                    "IsTestData": True,
                }
            )
            if LicenseStatus in {"NonCompliant", "Unverified", "Unknown"} or ComplianceStatus != "Compliant":
                RiskRegistry.append(
                    {
                        "RiskId": f"{LoadId}-EnterpriseComplianceRisk-{Index}",
                        "LoadId": LoadId,
                        "RiskCategory": "Compliance",
                        "Severity": "Critical" if LicenseStatus == "NonCompliant" else "High",
                        "Impact": f"Riesgo de licencia/compliance sobre {Resource['Name']}",
                        "AffectedTechnologyId": ComponentId,
                        "AffectedServiceId": Service["ServiceId"],
                        "RecommendedAction": "Validar licencia, normalizar compliance y documentar evidencia",
                        "Owner": Service["Owner"],
                        "EvidenceState": EvidenceStateValue,
                        "Status": "Open",
                        "IsTestData": True,
                    }
                )
            if BacklevelStatus == "Backlevel" or LifecycleStatus in {"EndOfSupport", "EndOfLife"}:
                RiskRegistry.append(
                    {
                        "RiskId": f"{LoadId}-EnterpriseLifecycleRisk-{Index}",
                        "LoadId": LoadId,
                        "RiskCategory": "Lifecycle",
                        "Severity": "Critical" if LifecycleStatus == "EndOfLife" else "High",
                        "Impact": f"Software backlevel o fuera de soporte en {Resource['Name']}",
                        "AffectedTechnologyId": ComponentId,
                        "AffectedServiceId": Service["ServiceId"],
                        "RecommendedAction": "Planificar upgrade, validar soporte y reducir deuda tecnologica",
                        "Owner": Service["Owner"],
                        "EvidenceState": EvidenceStateValue,
                        "Status": "Open",
                        "IsTestData": True,
                    }
                )
            Recommendations.append(
                {
                    "RecommendationId": f"{RiskId}-Recommendation",
                    "LoadId": LoadId,
                    "RiskId": RiskId,
                    "Priority": Severity,
                    "Action": "Priorizar remediacion enterprise",
                    "Rationale": f"Score {AdjustedScore} con evidencia {EvidenceStateValue}",
                    "DecisionOwner": Service["Owner"],
                    "Status": "Open",
                    "IsTestData": True,
                }
            )
        return {
            "EnterpriseDomains": Domains,
            "EnterpriseComponents": Components,
            "EnterpriseEvidence": Evidence,
            "EnterpriseScores": Scores,
            "EnterpriseRiskRegistry": RiskRegistry,
            "EnterpriseRecommendations": Recommendations,
        }

    def ValidateTools(self, LoadId: str | None = None) -> list:
        TargetSuffix = f" para {LoadId}" if LoadId else ""
        return [
            BuildToolValidationResult("Grafana", "http://localhost:3000", "HTTP", True, f"Disponible{TargetSuffix}"),
            BuildToolValidationResult("Zabbix Web", "http://localhost:8080", "HTTP", True, f"Disponible{TargetSuffix}"),
            BuildToolValidationResult("VictoriaMetrics", "http://localhost:8428", "HTTP", True, f"Disponible{TargetSuffix}"),
            BuildToolValidationResult("PostgreSQL", "localhost:5432", "TCP", True, f"Disponible{TargetSuffix}"),
            BuildToolValidationResult("Zabbix Server", "localhost:10051", "TCP", True, f"Disponible{TargetSuffix}"),
        ]

    def StatusFor(self, Profile: str) -> str:
        if Profile == "critical":
            return "Critical"
        if Profile in {"warning", "underprovisioned"}:
            return "Warning"
        return "OK"

    def ValueFor(self, Profile: str, Offset: int, Days: int, Random: random.Random) -> float:
        Ranges = {
            "normal": (25, 55),
            "warning": (60, 78),
            "critical": (82, 96),
            "overprovisioned": (5, 25),
            "underprovisioned": (78, 93),
            "mixed": (30, 92),
        }
        Low, High = Ranges[Profile]
        Trend = (Days - Offset) / max(Days, 1) * Random.uniform(0, 10)
        return min(100, Random.uniform(Low, High) + Trend)
