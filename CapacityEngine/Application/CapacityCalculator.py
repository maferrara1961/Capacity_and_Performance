from datetime import UTC, datetime
from math import ceil
from statistics import mean

from CapacityEngine.Domain.Constants import Confidence
from CapacityEngine.Domain.Entities import Baseline, CapacityKpi, ForecastResult, MetricSample
from CapacityEngine.Domain.Exceptions import CapacityCalculationError


class CapacityCalculator:
    def Average(self, Values: list[float]) -> float:
        self._RequireValues(Values)
        return mean(Values)

    def Peak(self, Values: list[float]) -> float:
        self._RequireValues(Values)
        return max(Values)

    def P95(self, Values: list[float]) -> float:
        self._RequireValues(Values)
        Sorted = sorted(Values)
        Index = max(0, ceil(0.95 * len(Sorted)) - 1)
        return Sorted[Index]

    def MonthlyGrowthRate(self, PreviousAverage: float, CurrentAverage: float) -> float:
        if PreviousAverage <= 0:
            return 0.0
        return ((CurrentAverage - PreviousAverage) / PreviousAverage) * 100.0

    def Headroom(self, ThresholdValue: float, CurrentValue: float) -> float:
        return ThresholdValue - CurrentValue

    def BaselineDelta(self, BaselineValue: float, CurrentValue: float) -> float:
        return CurrentValue - BaselineValue

    def DaysToSaturation(self, CurrentValue: float, DailyGrowth: float, ThresholdValue: float) -> int | None:
        if DailyGrowth <= 0:
            return None
        Remaining = ThresholdValue - CurrentValue
        if Remaining <= 0:
            return 0
        return ceil(Remaining / DailyGrowth)

    def ForecastValue(self, CurrentValue: float, DailyGrowth: float, Days: int) -> float:
        return CurrentValue + (DailyGrowth * Days)

    def BuildKpi(
        self,
        KpiId: str,
        Samples: list[MetricSample],
        ThresholdValue: float,
        PreviousAverage: float = 0.0,
        Baseline: Baseline | None = None,
    ) -> CapacityKpi:
        if not Samples:
            raise CapacityCalculationError("At least one sample is required")
        Values = [Sample.Value for Sample in Samples]
        WindowStart = min(Sample.ObservedAt for Sample in Samples)
        WindowEnd = max(Sample.ObservedAt for Sample in Samples)
        AverageValue = self.Average(Values)
        PeakValue = self.Peak(Values)
        P95Value = self.P95(Values)
        BaselineValue = Baseline.AverageValue if Baseline else AverageValue
        return CapacityKpi(
            CapacityKpiId=KpiId,
            ResourceId=Samples[0].ResourceId,
            MetricName=Samples[0].MetricName,
            CalculatedAt=datetime.now(UTC),
            WindowStart=WindowStart,
            WindowEnd=WindowEnd,
            AverageUtilization=AverageValue,
            PeakUtilization=PeakValue,
            P95Utilization=P95Value,
            MonthlyGrowthRate=self.MonthlyGrowthRate(PreviousAverage, AverageValue),
            HeadroomAvailable=self.Headroom(ThresholdValue, P95Value),
            BaselineDelta=self.BaselineDelta(BaselineValue, AverageValue),
        )

    def BuildForecast(self, ForecastId: str, Kpi: CapacityKpi, ThresholdValue: float, UsableHistoryDays: int = 30) -> ForecastResult:
        DailyGrowth = (Kpi.AverageUtilization * (Kpi.MonthlyGrowthRate / 100.0)) / 30.0
        ConfidenceValue = Confidence.LOW if UsableHistoryDays < 30 else Confidence.HIGH
        return ForecastResult(
            ForecastResultId=ForecastId,
            ResourceId=Kpi.ResourceId,
            MetricName=Kpi.MetricName,
            CalculatedAt=datetime.now(UTC),
            Forecast30Days=self.ForecastValue(Kpi.AverageUtilization, DailyGrowth, 30),
            Forecast60Days=self.ForecastValue(Kpi.AverageUtilization, DailyGrowth, 60),
            Forecast90Days=self.ForecastValue(Kpi.AverageUtilization, DailyGrowth, 90),
            DaysToSaturation=self.DaysToSaturation(Kpi.AverageUtilization, DailyGrowth, ThresholdValue),
            Confidence=ConfidenceValue,
        )

    def TopConsumers(self, Kpis: list[CapacityKpi], Limit: int = 10) -> list[CapacityKpi]:
        return sorted(Kpis, key=lambda Kpi: Kpi.P95Utilization, reverse=True)[:Limit]

    def _RequireValues(self, Values: list[float]) -> None:
        if not Values:
            raise CapacityCalculationError("Values are required")
