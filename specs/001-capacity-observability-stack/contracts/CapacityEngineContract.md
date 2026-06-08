# Contract: Capacity Engine

## Purpose

Defines the required behavior and inputs/outputs for the daily capacity calculation engine.

## Trigger Contract

**Trigger**: Daily scheduled run.

**Preconditions**:
- Authenticated system execution context is available.
- Catalog and thresholds have passed validation.
- At least one monitored resource exists.

**Inputs**:
- Service catalog mappings.
- Metric samples or query results for monitored resources.
- Alert thresholds.
- Baselines.
- Forecast windows: 30, 60, and 90 days.

**Validation**:
- Reject missing resource identifiers.
- Reject unsupported metric names.
- Reject malformed threshold definitions.
- Mark forecasts as Low confidence when usable history is less than 30 days.
- Reject negative values unless the metric explicitly allows negative deltas.

## Output Contract

Each successful run MUST produce:
- One `CapacityRun` audit record.
- `CapacityKpi` records for eligible resource and metric windows.
- `ForecastResult` records for 30, 60, and 90 day windows.
- `RiskAssessment` records for resources and affected services.
- `Recommendation` records for Warning and Critical risks when an action can be determined.

## KPI Rules

- Average utilization is the arithmetic mean of usable samples in the calculation window.
- Peak utilization is the maximum usable sample in the calculation window.
- P95 utilization is the 95th percentile of usable samples in the calculation window.
- Monthly growth is the relative change between the current window and comparable prior window.
- Headroom is the difference between the active saturation threshold and current projected usage.
- Days to saturation is Unknown when growth is not positive or history is insufficient.

## Risk Rules

- Risk dimensions include CPU, RAM, storage, IOPS, and network.
- Critical threshold breach results in Critical risk.
- Warning threshold breach results in Warning risk unless Critical also applies.
- Overall service risk is the highest risk among mapped resources, weighted by impact where
  service-resource mappings define weights.

## Failure Contract

When a run fails:
- The `CapacityRun` status MUST be Failed.
- Failure reason MUST be recorded.
- Existing successful results from previous runs MUST remain available.
- Dashboards MUST show the latest successful calculation and indicate stale or failed refresh state.
