from datetime import UTC, datetime

from CapacityEngine.Domain.EnterpriseConstants import EvidenceState, ForecastConfidence
from CapacityEngine.Domain.EnterpriseEntities import ForecastResult


class EnterpriseForecastService:
    def BuildForecast(self, AssessmentRunId: str, ComponentId: str, MetricName: str, Values: list[float]) -> ForecastResult:
        CleanValues = [float(Value) for Value in Values]
        if len(CleanValues) < 30:
            return ForecastResult(
                ForecastId=f"{AssessmentRunId}-{ComponentId}-{MetricName}-Forecast",
                AssessmentRunId=AssessmentRunId,
                ComponentId=ComponentId,
                MetricName=MetricName,
                EvidenceState=EvidenceState.INCOMPLETE,
                Confidence=ForecastConfidence.LOW,
                Forecast30Days=self.Project(CleanValues, 30) if CleanValues else None,
            )
        Confidence = ForecastConfidence.HIGH if len(CleanValues) >= 90 else ForecastConfidence.MEDIUM
        return ForecastResult(
            ForecastId=f"{AssessmentRunId}-{ComponentId}-{MetricName}-Forecast",
            AssessmentRunId=AssessmentRunId,
            ComponentId=ComponentId,
            MetricName=MetricName,
            EvidenceState=EvidenceState.AVAILABLE,
            Confidence=Confidence,
            Forecast30Days=self.Project(CleanValues, 30),
            Forecast90Days=self.Project(CleanValues, 90),
            Forecast180Days=self.Project(CleanValues, 180),
            Forecast365Days=self.Project(CleanValues, 365),
            DaysToExhaustion=self.DaysToExhaustion(CleanValues),
        )

    def Project(self, Values: list[float], Days: int) -> float:
        if not Values:
            return 0.0
        Trend = (Values[-1] - Values[0]) / max(len(Values) - 1, 1)
        return round(min(100.0, max(0.0, Values[-1] + Trend * Days)), 2)

    def DaysToExhaustion(self, Values: list[float]) -> int | None:
        if len(Values) < 2:
            return None
        Trend = (Values[-1] - Values[0]) / max(len(Values) - 1, 1)
        if Trend <= 0:
            return None
        return max(0, int((100 - Values[-1]) / Trend))

    def CalculatedAt(self) -> str:
        return datetime.now(UTC).isoformat()
