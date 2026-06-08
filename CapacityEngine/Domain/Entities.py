from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from CapacityEngine.Domain.Constants import Confidence, MetricName, ResourceType, RiskLevel


@dataclass(frozen=True)
class Service:
    ServiceId: str
    Name: str
    Owner: str
    Criticality: str
    SlaTarget: Optional[str] = None
    SloTarget: Optional[str] = None
    Status: RiskLevel = RiskLevel.UNKNOWN


@dataclass(frozen=True)
class Application:
    ApplicationId: str
    ServiceId: str
    Name: str
    Environment: str
    HealthStatus: RiskLevel = RiskLevel.UNKNOWN
    EndToEndPerformanceStatus: RiskLevel = RiskLevel.UNKNOWN


@dataclass(frozen=True)
class MonitoredResource:
    ResourceId: str
    ResourceType: ResourceType
    Name: str
    Platform: str
    CapacityUnit: str
    TotalCapacity: Optional[float] = None
    Status: RiskLevel = RiskLevel.UNKNOWN


@dataclass(frozen=True)
class ServiceResourceMap:
    MapId: str
    ServiceId: str
    ResourceId: str
    Role: str
    ImpactWeight: int
    ApplicationId: Optional[str] = None


@dataclass(frozen=True)
class MetricSample:
    MetricSampleId: str
    ResourceId: str
    MetricName: MetricName
    ObservedAt: datetime
    Value: float
    Unit: str
    Source: str


@dataclass(frozen=True)
class AlertThreshold:
    ThresholdId: str
    ScopeType: str
    MetricName: MetricName
    WarningValue: float
    CriticalValue: float
    Comparison: str = "GreaterOrEqual"
    Enabled: bool = True
    ScopeId: Optional[str] = None


@dataclass(frozen=True)
class Baseline:
    BaselineId: str
    ResourceId: str
    MetricName: MetricName
    PeriodStart: datetime
    PeriodEnd: datetime
    AverageValue: float
    P95Value: float
    PeakValue: float


@dataclass(frozen=True)
class CapacityKpi:
    CapacityKpiId: str
    ResourceId: str
    MetricName: MetricName
    CalculatedAt: datetime
    WindowStart: datetime
    WindowEnd: datetime
    AverageUtilization: float
    PeakUtilization: float
    P95Utilization: float
    MonthlyGrowthRate: float
    HeadroomAvailable: float
    BaselineDelta: float = 0.0


@dataclass(frozen=True)
class ForecastResult:
    ForecastResultId: str
    ResourceId: str
    MetricName: MetricName
    CalculatedAt: datetime
    Forecast30Days: float
    Forecast60Days: float
    Forecast90Days: float
    DaysToSaturation: Optional[int]
    Confidence: Confidence


@dataclass(frozen=True)
class RiskAssessment:
    RiskAssessmentId: str
    ScopeType: str
    ScopeId: str
    OverallRisk: RiskLevel
    Reason: str
    CalculatedAt: datetime
    ResourceRiskCpu: RiskLevel = RiskLevel.UNKNOWN
    ResourceRiskRam: RiskLevel = RiskLevel.UNKNOWN
    ResourceRiskStorage: RiskLevel = RiskLevel.UNKNOWN
    ResourceRiskIops: RiskLevel = RiskLevel.UNKNOWN
    ResourceRiskNetwork: RiskLevel = RiskLevel.UNKNOWN


@dataclass(frozen=True)
class Recommendation:
    RecommendationId: str
    RiskAssessmentId: str
    ScopeType: str
    ScopeId: str
    Priority: str
    Action: str
    Reason: str
    Status: str = "Open"


@dataclass
class CapacityRun:
    CapacityRunId: str
    StartedAt: datetime
    Status: str = "Pending"
    FinishedAt: Optional[datetime] = None
    ProcessedResourceCount: int = 0
    FailedResourceCount: int = 0
    ErrorMessage: Optional[str] = None
    Kpis: list[CapacityKpi] = field(default_factory=list)
    Forecasts: list[ForecastResult] = field(default_factory=list)
    Risks: list[RiskAssessment] = field(default_factory=list)
    Recommendations: list[Recommendation] = field(default_factory=list)
