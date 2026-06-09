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
from CapacityEngine.Domain.EnterpriseEntities import (
    BusinessService,
    EvidenceRecord,
    ForecastResult,
    Recommendation,
    RiskAssessment,
    RiskRegistryEntry,
    ScoreAssessment,
    ServiceComponentMap,
    TechnologyComponent,
    TechnologyDomain,
)
from CapacityEngine.Domain.Exceptions import ValidationError
from CapacityEngine.Domain.Validators import RequireText


def RequireEnum(Value, EnumType, FieldName: str) -> None:
    if not isinstance(Value, EnumType):
        raise ValidationError(f"{FieldName} is unsupported")


def ValidateTechnologyDomain(Domain: TechnologyDomain) -> None:
    RequireText(Domain.DomainId, "DomainId")
    RequireEnum(Domain.Name, TechnologyDomainName, "Name")
    RequireText(Domain.Description, "Description")
    RequireEnum(Domain.Status, EnterpriseStatus, "Status")


def ValidateTechnologyComponent(Component: TechnologyComponent) -> None:
    RequireText(Component.ComponentId, "ComponentId")
    RequireText(Component.ComponentName, "ComponentName")
    RequireText(Component.TechnologyType, "TechnologyType")
    RequireText(Component.DomainId, "DomainId")
    RequireEnum(Component.EvidenceState, EvidenceState, "EvidenceState")
    if Component.EvidenceState == EvidenceState.MISSING and Component.LifecycleStatus not in {"Unknown", "Missing"}:
        raise ValidationError("Missing lifecycle evidence must not produce a known lifecycle status")


def ValidateBusinessService(Service: BusinessService) -> None:
    RequireText(Service.BusinessServiceId, "BusinessServiceId")
    RequireText(Service.ServiceName, "ServiceName")
    RequireText(Service.ServiceOwner, "ServiceOwner")
    RequireEnum(Service.Criticality, EnterpriseRiskSeverity, "Criticality")


def ValidateServiceComponentMap(MapValue: ServiceComponentMap) -> None:
    RequireText(MapValue.MapId, "MapId")
    RequireText(MapValue.BusinessServiceId, "BusinessServiceId")
    RequireText(MapValue.ComponentId, "ComponentId")
    RequireText(MapValue.Role, "Role")
    if MapValue.ImpactWeight < 0 or MapValue.ImpactWeight > 100:
        raise ValidationError("ImpactWeight must be between 0 and 100")


def ValidateEvidenceRecord(Evidence: EvidenceRecord) -> None:
    RequireText(Evidence.EvidenceId, "EvidenceId")
    RequireText(Evidence.SourceSystem, "SourceSystem")
    RequireText(Evidence.EvidenceType, "EvidenceType")
    RequireEnum(Evidence.FreshnessStatus, FreshnessStatus, "FreshnessStatus")
    RequireEnum(Evidence.EvidenceState, EvidenceState, "EvidenceState")
    RequireText(Evidence.EvidenceReference, "EvidenceReference")


def ValidateScoreAssessment(Score: ScoreAssessment) -> None:
    RequireText(Score.ScoreAssessmentId, "ScoreAssessmentId")
    RequireEnum(Score.ScoreType, ScoreType, "ScoreType")
    RequireEnum(Score.ScopeType, ScopeType, "ScopeType")
    RequireText(Score.ScopeId, "ScopeId")
    if Score.ScoreValue < 0 or Score.ScoreValue > 100:
        raise ValidationError("ScoreValue must be between 0 and 100")
    RequireEnum(Score.Classification, ScoreClassification, "Classification")
    RequireEnum(Score.EvidenceState, EvidenceState, "EvidenceState")
    if Score.EvidenceState == EvidenceState.MISSING and Score.Classification in {ScoreClassification.EXCELLENT, ScoreClassification.HEALTHY}:
        raise ValidationError("Missing evidence cannot produce healthy classification")


def ValidateRiskAssessment(Risk: RiskAssessment) -> None:
    RequireText(Risk.RiskAssessmentId, "RiskAssessmentId")
    RequireEnum(Risk.RiskCategory, RiskCategory, "RiskCategory")
    RequireEnum(Risk.Severity, EnterpriseRiskSeverity, "Severity")
    RequireText(Risk.Impact, "Impact")
    RequireEnum(Risk.EvidenceState, EvidenceState, "EvidenceState")
    RequireText(Risk.Reason, "Reason")


def ValidateRiskRegistryEntry(Entry: RiskRegistryEntry) -> None:
    RequireText(Entry.RiskId, "RiskId")
    if not Entry.AffectedTechnologyIds:
        raise ValidationError("AffectedTechnologyIds is required")
    RequireText(Entry.RecommendedAction, "RecommendedAction")
    RequireEnum(Entry.Severity, EnterpriseRiskSeverity, "Severity")


def ValidateRecommendation(RecommendationValue: Recommendation) -> None:
    RequireText(RecommendationValue.RecommendationId, "RecommendationId")
    RequireText(RecommendationValue.RiskId, "RiskId")
    RequireText(RecommendationValue.Action, "Action")
    RequireText(RecommendationValue.Rationale, "Rationale")


def ValidateForecastResult(Forecast: ForecastResult) -> None:
    RequireText(Forecast.ForecastId, "ForecastId")
    RequireText(Forecast.ComponentId, "ComponentId")
    RequireText(Forecast.MetricName, "MetricName")
    RequireEnum(Forecast.EvidenceState, EvidenceState, "EvidenceState")
    RequireEnum(Forecast.Confidence, ForecastConfidence, "Confidence")
    if Forecast.EvidenceState in {EvidenceState.MISSING, EvidenceState.INCOMPLETE} and Forecast.Forecast365Days is not None:
        raise ValidationError("Insufficient evidence cannot produce long horizon forecast")
