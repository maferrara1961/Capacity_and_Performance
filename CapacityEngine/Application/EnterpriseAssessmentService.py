from datetime import UTC, datetime

from CapacityEngine.Application.EnterpriseScoringService import EnterpriseScoringService
from CapacityEngine.Domain.EnterpriseConstants import EvidenceState, ScopeType, ScoreType
from CapacityEngine.Domain.EnterpriseEntities import ScoreAssessment


class EnterpriseAssessmentService:
    DomainScoreTypes = [
        ScoreType.CAPACITY,
        ScoreType.PERFORMANCE,
        ScoreType.AVAILABILITY,
        ScoreType.LIFECYCLE,
        ScoreType.COMPLIANCE,
    ]

    def __init__(self, ScoringService: EnterpriseScoringService | None = None) -> None:
        self.ScoringService = ScoringService or EnterpriseScoringService()

    def BuildTechnologyHealthScore(self, AssessmentRunId: str, ScopeId: str, Scores: list[ScoreAssessment], MonitoringConfidence: float) -> ScoreAssessment:
        HealthValue = self.ScoringService.TechnologyHealthScore([Score.ScoreValue for Score in Scores], MonitoringConfidence)
        EvidenceStateValue = self.MostConstrainedEvidenceState([Score.EvidenceState for Score in Scores])
        Classification = self.ScoringService.Classify(HealthValue, EvidenceStateValue)
        return ScoreAssessment(
            ScoreAssessmentId=f"{AssessmentRunId}-TechnologyHealth-{ScopeId}",
            AssessmentRunId=AssessmentRunId,
            ScoreType=ScoreType.TECHNOLOGY_HEALTH,
            ScopeType=ScopeType.ENTERPRISE,
            ScopeId=ScopeId,
            ScoreValue=HealthValue,
            Classification=Classification,
            EvidenceState=EvidenceStateValue,
            CalculatedAt=datetime.now(UTC),
        )

    def MostConstrainedEvidenceState(self, States: list[EvidenceState]) -> EvidenceState:
        Order = [EvidenceState.MISSING, EvidenceState.UNKNOWN, EvidenceState.INCOMPLETE, EvidenceState.UNVERIFIED, EvidenceState.AVAILABLE]
        for State in Order:
            if State in States:
                return State
        return EvidenceState.UNKNOWN
