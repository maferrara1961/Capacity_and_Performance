from CapacityEngine.Domain.EnterpriseConstants import EvidenceState, ScoreClassification
from CapacityEngine.Domain.Exceptions import ValidationError


class EnterpriseScoringService:
    def Classify(self, ScoreValue: float, EvidenceStateValue: EvidenceState = EvidenceState.AVAILABLE) -> ScoreClassification:
        if ScoreValue < 0 or ScoreValue > 100:
            raise ValidationError("ScoreValue must be between 0 and 100")
        if EvidenceStateValue in {EvidenceState.MISSING, EvidenceState.UNKNOWN, EvidenceState.INCOMPLETE, EvidenceState.UNVERIFIED}:
            if ScoreValue >= 75:
                return ScoreClassification.ATTENTION_REQUIRED
        if ScoreValue >= 90:
            return ScoreClassification.EXCELLENT
        if ScoreValue >= 75:
            return ScoreClassification.HEALTHY
        if ScoreValue >= 60:
            return ScoreClassification.ATTENTION_REQUIRED
        if ScoreValue >= 40:
            return ScoreClassification.AT_RISK
        return ScoreClassification.CRITICAL

    def TechnologyHealthScore(self, Scores: list[float], MonitoringConfidence: float) -> float:
        if not Scores:
            return 0
        Values = [float(Value) for Value in Scores] + [float(MonitoringConfidence)]
        return round(sum(Values) / len(Values), 2)

    def EvidenceAdjustedScore(self, ScoreValue: float, EvidenceStateValue: EvidenceState) -> float:
        Penalties = {
            EvidenceState.AVAILABLE: 0,
            EvidenceState.UNVERIFIED: 10,
            EvidenceState.INCOMPLETE: 20,
            EvidenceState.UNKNOWN: 35,
            EvidenceState.MISSING: 50,
        }
        return max(0, round(float(ScoreValue) - Penalties[EvidenceStateValue], 2))
