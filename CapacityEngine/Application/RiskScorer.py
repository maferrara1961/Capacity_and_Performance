from datetime import UTC, datetime

from CapacityEngine.Domain.Constants import MetricName, RiskLevel
from CapacityEngine.Domain.Entities import AlertThreshold, CapacityKpi, RiskAssessment


class RiskScorer:
    def ScoreValue(self, Value: float, Threshold: AlertThreshold) -> RiskLevel:
        if not Threshold.Enabled:
            return RiskLevel.UNKNOWN
        if self._Matches(Value, Threshold.CriticalValue, Threshold.Comparison):
            return RiskLevel.CRITICAL
        if self._Matches(Value, Threshold.WarningValue, Threshold.Comparison):
            return RiskLevel.WARNING
        return RiskLevel.OK

    def ScoreKpi(self, Kpi: CapacityKpi, Threshold: AlertThreshold) -> RiskAssessment:
        Risk = self.ScoreValue(Kpi.P95Utilization, Threshold)
        Reason = "Within threshold" if Risk == RiskLevel.OK else f"{Kpi.MetricName.value} breached {Risk.value} threshold"
        Risks = {
            "ResourceRiskCpu": RiskLevel.UNKNOWN,
            "ResourceRiskRam": RiskLevel.UNKNOWN,
            "ResourceRiskStorage": RiskLevel.UNKNOWN,
            "ResourceRiskIops": RiskLevel.UNKNOWN,
            "ResourceRiskNetwork": RiskLevel.UNKNOWN,
        }
        Map = {
            MetricName.CPU: "ResourceRiskCpu",
            MetricName.RAM: "ResourceRiskRam",
            MetricName.STORAGE: "ResourceRiskStorage",
            MetricName.IOPS: "ResourceRiskIops",
            MetricName.NETWORK: "ResourceRiskNetwork",
        }
        if Kpi.MetricName in Map:
            Risks[Map[Kpi.MetricName]] = Risk
        return RiskAssessment(
            RiskAssessmentId=f"Risk-{Kpi.CapacityKpiId}",
            ScopeType="Resource",
            ScopeId=Kpi.ResourceId,
            OverallRisk=Risk,
            Reason=Reason,
            CalculatedAt=datetime.now(UTC),
            **Risks,
        )

    def ClassifySizing(self, Kpi: CapacityKpi) -> str:
        if Kpi.P95Utilization < 30 and Kpi.HeadroomAvailable > 50:
            return "Oversized"
        if Kpi.P95Utilization > 85 or Kpi.HeadroomAvailable < 10:
            return "Undersized"
        return "RightSized"

    def PropagateDependencyRisk(self, Risks: list[RiskAssessment]) -> RiskLevel:
        Values = [Risk.OverallRisk for Risk in Risks]
        if RiskLevel.CRITICAL in Values:
            return RiskLevel.CRITICAL
        if RiskLevel.WARNING in Values:
            return RiskLevel.WARNING
        if RiskLevel.UNKNOWN in Values:
            return RiskLevel.UNKNOWN
        return RiskLevel.OK

    def _Matches(self, Value: float, ThresholdValue: float, Comparison: str) -> bool:
        if Comparison == "GreaterThan":
            return Value > ThresholdValue
        if Comparison == "GreaterOrEqual":
            return Value >= ThresholdValue
        if Comparison == "LessThan":
            return Value < ThresholdValue
        if Comparison == "LessOrEqual":
            return Value <= ThresholdValue
        return False
