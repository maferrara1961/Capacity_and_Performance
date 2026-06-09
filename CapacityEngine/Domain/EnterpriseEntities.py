from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from CapacityEngine.Domain.EnterpriseConstants import (
    EnterpriseRiskSeverity,
    EnterpriseStatus,
    EvidenceState,
    ForecastConfidence,
    FreshnessStatus,
    RiskCategory,
    ScopeType,
    ScoreClassification,
    ScoreType,
    TechnologyDomainName,
)


@dataclass(frozen=True)
class TechnologyDomain:
    DomainId: str
    Name: TechnologyDomainName
    Description: str
    Status: EnterpriseStatus = EnterpriseStatus.ACTIVE


@dataclass(frozen=True)
class TechnologyComponent:
    ComponentId: str
    ComponentName: str
    TechnologyType: str
    DomainId: str
    Version: str = "Unknown"
    Vendor: str = "Unknown"
    Environment: str = "Unknown"
    BusinessServiceId: Optional[str] = None
    Owner: str = "Unknown"
    SupportStatus: str = "Unknown"
    LifecycleStatus: str = "Unknown"
    EvidenceState: EvidenceState = EvidenceState.UNKNOWN


@dataclass(frozen=True)
class BusinessService:
    BusinessServiceId: str
    ServiceName: str
    ServiceOwner: str
    Criticality: EnterpriseRiskSeverity = EnterpriseRiskSeverity.MEDIUM
    Status: EnterpriseStatus = EnterpriseStatus.ACTIVE


@dataclass(frozen=True)
class ServiceComponentMap:
    MapId: str
    BusinessServiceId: str
    ComponentId: str
    Role: str
    ImpactWeight: int


@dataclass(frozen=True)
class EvidenceRecord:
    EvidenceId: str
    SourceSystem: str
    EvidenceType: str
    ObservedAt: datetime
    FreshnessStatus: FreshnessStatus
    EvidenceState: EvidenceState
    EvidenceReference: str
    ComponentId: Optional[str] = None
    BusinessServiceId: Optional[str] = None


@dataclass(frozen=True)
class AssessmentRun:
    AssessmentRunId: str
    StartedAt: datetime
    Scope: str
    EvidenceWindowStart: datetime
    EvidenceWindowEnd: datetime
    Status: str = "Running"
    CompletedAt: Optional[datetime] = None


@dataclass(frozen=True)
class ScoreAssessment:
    ScoreAssessmentId: str
    AssessmentRunId: str
    ScoreType: ScoreType
    ScopeType: ScopeType
    ScopeId: str
    ScoreValue: float
    Classification: ScoreClassification
    EvidenceState: EvidenceState
    CalculatedAt: datetime


@dataclass(frozen=True)
class RiskAssessment:
    RiskAssessmentId: str
    AssessmentRunId: str
    RiskCategory: RiskCategory
    Severity: EnterpriseRiskSeverity
    Impact: str
    ScopeType: ScopeType
    ScopeId: str
    EvidenceState: EvidenceState
    Reason: str
    CalculatedAt: datetime


@dataclass(frozen=True)
class RiskRegistryEntry:
    RiskId: str
    RiskAssessmentId: str
    RiskCategory: RiskCategory
    Severity: EnterpriseRiskSeverity
    Impact: str
    AffectedTechnologyIds: tuple[str, ...]
    RecommendedAction: str
    Owner: str
    EvidenceState: EvidenceState
    AffectedServiceIds: tuple[str, ...] = field(default_factory=tuple)
    Status: str = "Open"


@dataclass(frozen=True)
class Recommendation:
    RecommendationId: str
    RiskId: str
    Priority: EnterpriseRiskSeverity
    Action: str
    Rationale: str
    DecisionOwner: str
    Status: str = "Open"


@dataclass(frozen=True)
class ForecastResult:
    ForecastId: str
    AssessmentRunId: str
    ComponentId: str
    MetricName: str
    EvidenceState: EvidenceState
    Confidence: ForecastConfidence
    Forecast30Days: Optional[float] = None
    Forecast90Days: Optional[float] = None
    Forecast180Days: Optional[float] = None
    Forecast365Days: Optional[float] = None
    DaysToExhaustion: Optional[int] = None
