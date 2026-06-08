from CapacityEngine.Domain.Constants import RiskLevel
from CapacityEngine.Domain.Entities import Recommendation, RiskAssessment


class RecommendationService:
    def BuildRecommendation(self, RecommendationId: str, Risk: RiskAssessment) -> Recommendation | None:
        if Risk.OverallRisk == RiskLevel.OK:
            return None
        Priority = "Critical" if Risk.OverallRisk == RiskLevel.CRITICAL else "High"
        return Recommendation(
            RecommendationId=RecommendationId,
            RiskAssessmentId=Risk.RiskAssessmentId,
            ScopeType=Risk.ScopeType,
            ScopeId=Risk.ScopeId,
            Priority=Priority,
            Action="Review capacity allocation and remediation plan",
            Reason=Risk.Reason,
        )
