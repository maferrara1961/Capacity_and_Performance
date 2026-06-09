# Data Model: Datos de Prueba para Monitoreo, Performance y Capacity

## TestLoad

Represents one synthetic data load.

**Fields**:
- `LoadId`: unique identifier for the generated load.
- `ScenarioProfile`: normal, warning, critical, overprovisioned, underprovisioned, or mixed.
- `RequestedVolume`: small, medium, large, or explicit bounded count.
- `CreatedAt`: timestamp when generation started.
- `FinishedAt`: timestamp when generation finished.
- `Status`: Planned, Running, Succeeded, Failed, PartiallyDeleted, Deleted.
- `GeneratedServiceCount`
- `GeneratedResourceCount`
- `GeneratedMetricSampleCount`
- `GeneratedKpiCount`
- `GeneratedForecastCount`
- `GeneratedRiskCount`
- `GeneratedRecommendationCount`
- `ErrorMessage`: optional deterministic error detail.
- `IsTestData`: always true for generated records.

**Validation**:
- `LoadId` is required, unique, and safe for identifiers.
- `ScenarioProfile` must be one of the approved values.
- `RequestedVolume` must be inside configured bounds.
- Delete-all requires explicit confirmation.

**State Transitions**:
- Planned -> Running -> Succeeded
- Planned -> Running -> Failed
- Succeeded -> PartiallyDeleted
- Succeeded -> Deleted
- Failed -> Deleted

## SyntheticService

Represents a service or application group used by dashboards.

**Fields**:
- `ServiceId`
- `LoadId`
- `Name`
- `Owner`
- `Criticality`
- `SlaTarget`
- `SloTarget`
- `Status`
- `IsTestData`

**Relationships**:
- Owns one or more `SyntheticApplication`.
- Maps to many `SyntheticResource`.

## SyntheticApplication

Represents an application instance associated with a service.

**Fields**:
- `ApplicationId`
- `LoadId`
- `ServiceId`
- `Name`
- `Environment`
- `HealthStatus`
- `EndToEndPerformanceStatus`
- `IsTestData`

## SyntheticResource

Represents infrastructure under test.

**Fields**:
- `ResourceId`
- `LoadId`
- `ResourceType`: Server, Database, Storage, Network, Dependency.
- `Name`
- `Platform`
- `CapacityUnit`
- `TotalCapacity`
- `Status`
- `IsTestData`

**Relationships**:
- Mapped to services through `SyntheticServiceResourceMap`.
- Has many metric samples, KPIs, forecasts, risks, and recommendations.

## SyntheticMetricSample

Represents monitoring and performance time-series samples.

**Fields**:
- `SampleId`
- `LoadId`
- `ResourceId`
- `MetricName`: CPU, Memory, Disk, Network, Latency, Throughput, Errors, Saturation, IOPS.
- `ObservedAt`
- `Value`
- `Unit`
- `Source`
- `IsTestData`

**Validation**:
- Timestamp must fall within the requested synthetic history window.
- Values must be non-negative and coherent with the metric unit.
- Scenario profile controls ranges and trend shape.

## SyntheticCapacityKpi

Represents calculated capacity indicators.

**Fields**:
- `CapacityKpiId`
- `LoadId`
- `ResourceId`
- `MetricName`
- `CalculatedAt`
- `WindowStart`
- `WindowEnd`
- `AverageUtilization`
- `PeakUtilization`
- `P95Utilization`
- `MonthlyGrowthRate`
- `HeadroomAvailable`
- `BaselineDelta`
- `IsTestData`

## SyntheticForecast

Represents projected usage.

**Fields**:
- `ForecastResultId`
- `LoadId`
- `ResourceId`
- `MetricName`
- `CalculatedAt`
- `Forecast30Days`
- `Forecast60Days`
- `Forecast90Days`
- `DaysToSaturation`
- `Confidence`
- `IsTestData`

## SyntheticRisk

Represents resource or service risk.

**Fields**:
- `RiskAssessmentId`
- `LoadId`
- `ScopeType`
- `ScopeId`
- `OverallRisk`
- `Reason`
- `CalculatedAt`
- `IsTestData`

## SyntheticRecommendation

Represents suggested action derived from risk.

**Fields**:
- `RecommendationId`
- `LoadId`
- `RiskAssessmentId`
- `ScopeType`
- `ScopeId`
- `Priority`
- `Action`
- `Reason`
- `Status`
- `IsTestData`

## ToolValidationResult

Represents validation of installed tools after load/delete operations.

**Fields**:
- `ToolName`
- `Target`
- `Protocol`
- `Status`
- `Message`
- `ValidatedAt`

## Deletion Rules

- Delete by `LoadId` removes only records marked with that `LoadId` and `IsTestData`.
- Delete all removes only records where `IsTestData` is true and requires explicit confirmation.
- Operational records without the test marker are never deleted.
