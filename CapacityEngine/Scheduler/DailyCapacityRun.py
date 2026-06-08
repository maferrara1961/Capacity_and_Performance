from datetime import UTC, datetime, timedelta

from CapacityEngine.Application.CapacityCalculator import CapacityCalculator
from CapacityEngine.Application.RecommendationService import RecommendationService
from CapacityEngine.Application.RiskScorer import RiskScorer
from CapacityEngine.Domain.Constants import MetricName
from CapacityEngine.Domain.Entities import AlertThreshold, CapacityRun, MetricSample


def RunDailyCapacity() -> CapacityRun:
    StartedAt = datetime.now(UTC)
    Run = CapacityRun(CapacityRunId=f"Run-{StartedAt.strftime('%Y%m%d%H%M%S')}", StartedAt=StartedAt, Status="Running")
    Calculator = CapacityCalculator()
    Scorer = RiskScorer()
    Recommendations = RecommendationService()
    Samples = [
        MetricSample("S1", "ResourceA", MetricName.CPU, StartedAt - timedelta(days=1), 70.0, "Percent", "Sample"),
        MetricSample("S2", "ResourceA", MetricName.CPU, StartedAt, 90.0, "Percent", "Sample"),
    ]
    Threshold = AlertThreshold("T1", "Resource", MetricName.CPU, 75.0, 90.0)
    Kpi = Calculator.BuildKpi("Kpi-ResourceA-Cpu", Samples, Threshold.CriticalValue, PreviousAverage=60.0)
    Forecast = Calculator.BuildForecast("Forecast-ResourceA-Cpu", Kpi, Threshold.CriticalValue)
    Risk = Scorer.ScoreKpi(Kpi, Threshold)
    Recommendation = Recommendations.BuildRecommendation("Recommendation-ResourceA-Cpu", Risk)
    Run.Kpis.append(Kpi)
    Run.Forecasts.append(Forecast)
    Run.Risks.append(Risk)
    if Recommendation:
        Run.Recommendations.append(Recommendation)
    Run.ProcessedResourceCount = 1
    Run.Status = "Succeeded"
    Run.FinishedAt = datetime.now(UTC)
    return Run


if __name__ == "__main__":
    Result = RunDailyCapacity()
    print(f"{Result.CapacityRunId} {Result.Status} resources={Result.ProcessedResourceCount}")
