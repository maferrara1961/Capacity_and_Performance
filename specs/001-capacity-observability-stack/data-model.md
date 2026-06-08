# Data Model: Capacity Observability Stack

## Entity: Service

**Purpose**: Business or technical capability monitored for capacity and risk.

**Fields**:
- `ServiceId`: Stable identifier.
- `Name`: Display name.
- `Owner`: Responsible team or person.
- `Criticality`: Business criticality: Low, Medium, High, Critical.
- `SlaTarget`: Availability or service-level target.
- `SloTarget`: Performance or reliability target.
- `Status`: OK, Warning, Critical, Unknown.
- `CreatedAt`: Creation timestamp.
- `UpdatedAt`: Last update timestamp.

**Relationships**:
- Has many `Application` records.
- Has many `ServiceResourceMap` records.
- Has many `RiskAssessment` records.
- Has many `Recommendation` records.

**Validation Rules**:
- `Name` is required and unique.
- `Criticality` must be one of the allowed values.
- `SlaTarget` and `SloTarget`, when present, must be valid positive percentages or documented text.

## Entity: Application

**Purpose**: Software system associated with a service and monitored infrastructure.

**Fields**:
- `ApplicationId`: Stable identifier.
- `ServiceId`: Parent service.
- `Name`: Display name.
- `Environment`: Production, Staging, Development, or other approved value.
- `HealthStatus`: OK, Warning, Critical, Unknown.
- `EndToEndPerformanceStatus`: OK, Warning, Critical, Unknown.

**Relationships**:
- Belongs to `Service`.
- Has many `ServiceResourceMap` records.
- Has many `Dependency` records.

**Validation Rules**:
- `Name` and `ServiceId` are required.
- `Environment` must be an approved value.

## Entity: MonitoredResource

**Purpose**: Infrastructure component whose capacity and performance are measured.

**Fields**:
- `ResourceId`: Stable identifier.
- `ResourceType`: Server, Database, Storage, Network, Dependency, or ApplicationComponent.
- `Name`: Display name.
- `Platform`: Source platform or subsystem.
- `CapacityUnit`: Percent, Bytes, IOPS, RequestsPerSecond, PacketsPerSecond, or Milliseconds.
- `TotalCapacity`: Optional total capacity value.
- `Status`: OK, Warning, Critical, Unknown.

**Relationships**:
- Has many `MetricSample` records.
- Has many `CapacityKpi` records.
- Has many `ForecastResult` records.
- Has many `RiskAssessment` records.
- May map to many `Service` and `Application` records through `ServiceResourceMap`.

**Validation Rules**:
- `Name`, `ResourceType`, and `CapacityUnit` are required.
- `TotalCapacity`, when present, must be positive.

## Entity: ServiceResourceMap

**Purpose**: Maps services and applications to supporting resources.

**Fields**:
- `MapId`: Stable identifier.
- `ServiceId`: Associated service.
- `ApplicationId`: Optional associated application.
- `ResourceId`: Associated resource.
- `Role`: Primary, Supporting, Shared, Dependency, or Other.
- `ImpactWeight`: Relative impact score from 1 to 100.

**Relationships**:
- Belongs to `Service`.
- Optionally belongs to `Application`.
- Belongs to `MonitoredResource`.

**Validation Rules**:
- `ServiceId` and `ResourceId` are required.
- `ImpactWeight` must be between 1 and 100.
- Shared resources may map to multiple services.

## Entity: MetricSample

**Purpose**: Time-based observed value for a monitored resource.

**Fields**:
- `MetricSampleId`: Stable identifier.
- `ResourceId`: Measured resource.
- `MetricName`: CPU, RAM, Storage, IOPS, Network, Latency, Throughput, Errors, or Saturation.
- `ObservedAt`: Sample timestamp.
- `Value`: Numeric measurement.
- `Unit`: Measurement unit.
- `Source`: Source collector or platform.

**Relationships**:
- Belongs to `MonitoredResource`.

**Validation Rules**:
- `MetricName`, `ObservedAt`, `Value`, and `Unit` are required.
- `Value` must be non-negative unless the metric explicitly permits negative deltas.
- Duplicate samples for the same resource, metric, source, and timestamp are rejected or merged by
  deterministic policy.

## Entity: AlertThreshold

**Purpose**: Defines resource and service boundaries used for visual alerts and risk classification.

**Fields**:
- `ThresholdId`: Stable identifier.
- `ScopeType`: Global, Service, Application, ResourceType, or Resource.
- `ScopeId`: Optional scope identifier.
- `MetricName`: Target metric.
- `WarningValue`: Warning threshold.
- `CriticalValue`: Critical threshold.
- `Comparison`: GreaterThan, GreaterOrEqual, LessThan, LessOrEqual.
- `Enabled`: Boolean.

**Relationships**:
- May apply to `Service`, `Application`, or `MonitoredResource`.

**Validation Rules**:
- `WarningValue` and `CriticalValue` are required.
- Critical threshold must be stricter than warning threshold according to `Comparison`.
- Disabled thresholds are ignored by risk calculations.

## Entity: Baseline

**Purpose**: Reference values used for comparison against current usage.

**Fields**:
- `BaselineId`: Stable identifier.
- `ResourceId`: Resource being baselined.
- `MetricName`: Metric being baselined.
- `PeriodStart`: Start timestamp.
- `PeriodEnd`: End timestamp.
- `AverageValue`: Baseline average.
- `P95Value`: Baseline p95.
- `PeakValue`: Baseline peak.

**Relationships**:
- Belongs to `MonitoredResource`.
- Referenced by `CapacityKpi`.

**Validation Rules**:
- Period end must be after period start.
- Baseline values must be non-negative.

## Entity: CapacityKpi

**Purpose**: Derived measurement used for dashboards and planning.

**Fields**:
- `CapacityKpiId`: Stable identifier.
- `ResourceId`: Target resource.
- `MetricName`: Target metric.
- `CalculatedAt`: Calculation timestamp.
- `WindowStart`: Measurement window start.
- `WindowEnd`: Measurement window end.
- `AverageUtilization`: Average usage.
- `PeakUtilization`: Peak usage.
- `P95Utilization`: Percentile 95 usage.
- `MonthlyGrowthRate`: Monthly growth percentage.
- `HeadroomAvailable`: Remaining capacity before threshold.
- `BaselineDelta`: Difference from baseline.

**Relationships**:
- Belongs to `MonitoredResource`.
- May reference `Baseline`.
- Feeds `ForecastResult` and `RiskAssessment`.

**Validation Rules**:
- `WindowEnd` must be after `WindowStart`.
- Utilization and growth values must be numeric.
- `P95Utilization` cannot exceed `PeakUtilization` for the same calculation window.

## Entity: ForecastResult

**Purpose**: Projection for future resource usage and exhaustion.

**Fields**:
- `ForecastResultId`: Stable identifier.
- `ResourceId`: Target resource.
- `MetricName`: Target metric.
- `CalculatedAt`: Calculation timestamp.
- `Forecast30Days`: Projected value after 30 days.
- `Forecast60Days`: Projected value after 60 days.
- `Forecast90Days`: Projected value after 90 days.
- `DaysToSaturation`: Estimated days until threshold saturation.
- `Confidence`: Low, Medium, High.

**Relationships**:
- Belongs to `MonitoredResource`.
- References `CapacityKpi`.
- Feeds `RiskAssessment` and `Recommendation`.

**Validation Rules**:
- Forecast values must be numeric.
- `DaysToSaturation` must be positive, zero, or Unknown.
- Confidence is Low when there are fewer than 30 days of usable history.

## Entity: RiskAssessment

**Purpose**: OK, Warning, or Critical classification for a resource, service, or application.

**Fields**:
- `RiskAssessmentId`: Stable identifier.
- `ScopeType`: Service, Application, or Resource.
- `ScopeId`: Target identifier.
- `ResourceRiskCpu`: OK, Warning, Critical, Unknown.
- `ResourceRiskRam`: OK, Warning, Critical, Unknown.
- `ResourceRiskStorage`: OK, Warning, Critical, Unknown.
- `ResourceRiskIops`: OK, Warning, Critical, Unknown.
- `ResourceRiskNetwork`: OK, Warning, Critical, Unknown.
- `OverallRisk`: OK, Warning, Critical, Unknown.
- `Reason`: Human-readable reason.
- `CalculatedAt`: Calculation timestamp.

**Relationships**:
- May reference `ForecastResult`, `CapacityKpi`, `Service`, `Application`, or `MonitoredResource`.
- Has many `Recommendation` records.

**Validation Rules**:
- `OverallRisk` must be the highest effective risk across included dimensions unless explicitly
  overridden by documented service rules.
- `Reason` is required for Warning and Critical states.

## Entity: Recommendation

**Purpose**: Action suggestion tied to a risk, trend, or capacity issue.

**Fields**:
- `RecommendationId`: Stable identifier.
- `RiskAssessmentId`: Related risk.
- `ScopeType`: Service, Application, or Resource.
- `ScopeId`: Target identifier.
- `Priority`: Low, Medium, High, Critical.
- `Action`: Suggested action.
- `Reason`: Why the action is recommended.
- `Status`: Open, Accepted, Deferred, Closed.

**Relationships**:
- Belongs to `RiskAssessment`.

**Validation Rules**:
- `Action`, `Reason`, and `Priority` are required.
- Critical recommendations must reference a Warning or Critical risk.

## Entity: CapacityRun

**Purpose**: Audit record for daily capacity calculation execution.

**Fields**:
- `CapacityRunId`: Stable identifier.
- `StartedAt`: Start timestamp.
- `FinishedAt`: Finish timestamp.
- `Status`: Pending, Running, Succeeded, Failed.
- `ProcessedResourceCount`: Number of resources processed.
- `FailedResourceCount`: Number of resources failed.
- `ErrorMessage`: Optional failure reason.

**Relationships**:
- Produces `CapacityKpi`, `ForecastResult`, `RiskAssessment`, and `Recommendation` records.

**Validation Rules**:
- A run cannot move from Failed or Succeeded back to Running.
- `FinishedAt` is required when status is Succeeded or Failed.
- `FailedResourceCount` must not exceed `ProcessedResourceCount`.

## State Transitions

### CapacityRun

```text
Pending -> Running -> Succeeded
Pending -> Running -> Failed
Failed -> Pending (manual retry creates a new run record)
Succeeded -> terminal
```

### Recommendation

```text
Open -> Accepted -> Closed
Open -> Deferred -> Open
Open -> Closed
Deferred -> Closed
```
