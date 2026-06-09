from datetime import UTC, datetime, timedelta
import random

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
        Samples = self.BuildSamples(LoadId, Resources, Profile, Days, Random)
        Kpis = self.BuildKpis(LoadId, Resources, Profile, Random)
        Forecasts = self.BuildForecasts(LoadId, Resources, Profile, Random)
        Risks = self.BuildRisks(LoadId, Resources, Profile)
        Recommendations = self.BuildRecommendations(LoadId, Risks)
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

    def BuildSamples(self, LoadId: str, Resources: list[dict], Profile: str, Days: int, Random: random.Random) -> list[dict]:
        Metrics = ["CPU", "RAM", "Storage", "IOPS", "Network", "Latency", "Throughput", "Errors", "Saturation"]
        Samples = []
        Now = datetime.now(UTC)
        for Resource in Resources:
            for Metric in Metrics:
                for Offset in range(Days, -1, -1):
                    ObservedAt = Now - timedelta(days=Offset)
                    Samples.append(
                        {
                            "SampleId": f"{LoadId}-{Resource['ResourceId']}-{Metric}-{Offset}",
                            "LoadId": LoadId,
                            "ResourceId": Resource["ResourceId"],
                            "HostName": Resource["Name"],
                            "MetricName": Metric,
                            "ObservedAt": ObservedAt.isoformat(),
                            "Value": round(self.ValueFor(Profile, Offset, Days, Random), 2),
                            "Unit": "Percent" if Metric not in {"Latency", "Throughput", "Errors"} else "Count",
                            "Source": "Synthetic",
                            "IsTestData": True,
                        }
                    )
        return Samples

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
                "Priority": "High" if Risk["OverallRisk"] == "Critical" else "Medium",
                "Action": "Revisar capacidad sintetica y plan de remediacion",
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
            "DaysToSaturation": 90 if Base < 85 else 30,
            "Confidence": "High",
            "IsTestData": True,
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
