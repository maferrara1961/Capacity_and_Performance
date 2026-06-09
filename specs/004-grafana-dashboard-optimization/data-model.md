# Data Model: Grafana Dashboard Optimization

## DashboardView

Represents a dashboard view intended for a specific user audience and decision type.

**Fields**:

- `Name`: Human-readable dashboard name.
- `Audience`: `Executive`, `Technical`, or `Planning`.
- `Purpose`: Decision or operational outcome supported by the view.
- `Sections`: Ordered groups of panels.
- `RequiredSignals`: Capacity, performance, service, risk, or recommendation signals required for the view.
- `EmptyStateExpectation`: Description of what the user should understand when no data is present.

**Relationships**:

- Contains multiple `DashboardSection` records.
- References `CapacitySignal`, `PerformanceSignal`, `ServiceContext`, and `RiskSummary` depending on purpose.

**Validation Rules**:

- `Name`, `Audience`, and `Purpose` are required.
- Executive views must include status, risk, forecast, headroom, and recommendation sections.
- Technical views must include metric-level performance sections and affected-resource context.

## DashboardSection

Represents a logical group of dashboard panels.

**Fields**:

- `Title`: User-facing section title.
- `DecisionPurpose`: Why the section exists.
- `Audience`: Target audience for the section.
- `SignalType`: Capacity, performance, service, risk, recommendation, or verification.
- `Priority`: Ordering priority within the dashboard.

**Relationships**:

- Belongs to a `DashboardView`.
- Uses one or more signals.

**Validation Rules**:

- Each section must have a clear decision or operational purpose.
- Executive sections must prioritize summaries and actions.
- Technical sections must preserve enough context to identify service, resource, metric, and severity.

## CapacitySignal

Represents a capacity indicator used for planning and decision dashboards.

**Fields**:

- `ResourceId`: Affected resource.
- `ServiceId`: Related service when available.
- `MetricName`: Capacity metric name.
- `AverageUtilization`: Average utilization for the analysis window.
- `PeakUtilization`: Peak utilization for the analysis window.
- `P95Utilization`: Percentile 95 utilization.
- `MonthlyGrowthRate`: Estimated monthly growth.
- `HeadroomAvailable`: Remaining usable capacity.
- `Forecast30Days`: Forecast after 30 days.
- `Forecast60Days`: Forecast after 60 days.
- `Forecast90Days`: Forecast after 90 days.
- `DaysToSaturation`: Estimated time until saturation.
- `BaselineDelta`: Difference from expected baseline.

**Relationships**:

- Connects to `ServiceContext` through resource-service mapping.
- Feeds `RiskSummary` and executive recommendation sections.

**Validation Rules**:

- Utilization and headroom values must be bounded percentages.
- Forecast windows must be present for decision-oriented dashboards.
- Days to saturation must be visible when risk is warning or critical.

## PerformanceSignal

Represents operational measurements used for technical diagnosis.

**Fields**:

- `ResourceId`: Affected resource.
- `ServiceId`: Related service when available.
- `MetricName`: CPU, memory, storage, IOPS, network, latency, throughput, errors, or saturation.
- `ObservedAt`: Time of observation.
- `Value`: Observed measurement.
- `Severity`: OK, Warning, or Critical when classifiable.

**Relationships**:

- Connects to `ServiceContext` through resource-service mapping.
- Supports technical dashboard sections and outlier views.

**Validation Rules**:

- Required technical metrics must be represented in dashboard coverage.
- Resource and metric context must be visible for warning and critical states.

## ServiceContext

Represents business-service mapping for infrastructure and dependencies.

**Fields**:

- `ServiceId`: Service identifier.
- `ApplicationId`: Related application identifier when available.
- `ResourceId`: Mapped infrastructure resource.
- `Owner`: Responsible owner.
- `Criticality`: Business criticality.
- `Role`: Resource role within the service.
- `ImpactWeight`: Relative impact of the resource.

**Relationships**:

- Links `CapacitySignal`, `PerformanceSignal`, and `RiskSummary` to business context.

**Validation Rules**:

- Dashboards must not show critical resource risk without enough context to identify the affected service or application.
- Shared resources must remain visible as shared impact.

## RiskSummary

Represents risk classification and recommended response.

**Fields**:

- `ScopeType`: Service, application, or resource.
- `ScopeId`: Affected object.
- `OverallRisk`: OK, Warning, or Critical.
- `Reason`: Explanation of the risk.
- `Priority`: Recommended action priority.
- `Action`: Recommended action.

**Relationships**:

- Derived from `CapacitySignal` and service context.
- Displayed in executive and planning views.

**Validation Rules**:

- Warning and critical risk summaries must have a reason and recommended action.
- Executive views must show the highest-priority risk summaries first.

## VerificationScenario

Represents repeatable test data used to validate dashboard behavior.

**Fields**:

- `LoadId`: Scenario identifier.
- `Profile`: Normal, warning, critical, or mixed.
- `Volume`: Small, medium, or large.
- `GeneratedAt`: Creation timestamp.
- `ExpectedDashboardCoverage`: Dashboard categories expected to populate.

**Relationships**:

- Produces `CapacitySignal`, `PerformanceSignal`, `ServiceContext`, and `RiskSummary` data.

**Validation Rules**:

- Load identifiers must be validated before execution.
- Each required profile must populate both executive and technical dashboard categories.
