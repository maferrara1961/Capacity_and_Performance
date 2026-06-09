# Research: Grafana Dashboard Optimization

## Decision: Separate Executive and Technical Dashboard Purposes

**Decision**: Keep executive dashboards focused on risk, forecast, headroom, and recommended action; keep technical dashboards focused on metric diagnosis, affected resources, services, severity, and trends.

**Rationale**: The feature requires two different decision contexts. Executives need prioritization without raw metric inspection, while operations teams need enough metric detail to improve service performance. Separating these purposes reduces cognitive load and makes each dashboard independently testable.

**Alternatives considered**:

- Single combined dashboard: rejected because it mixes decision summaries with operational detail and makes both audiences scan irrelevant information.
- Fully duplicated executive and technical dashboards: rejected because it would duplicate KPI logic and increase maintenance without improving user value.

## Decision: Reuse Existing Capacity and Performance Signals

**Decision**: Use existing capacity KPI, forecast, risk, recommendation, service mapping, and synthetic performance signals as the dashboard data contract.

**Rationale**: The current stack already contains data required by the specification: average, peak, percentile 95, monthly growth, headroom, forecast windows, days to saturation, service-resource mapping, and synthetic time series. Reuse satisfies DRY and YAGNI while keeping the scope limited to dashboard optimization.

**Alternatives considered**:

- Add new storage tables or new metric families: rejected because current signals cover the requested dashboards.
- Add a new analytics engine: rejected because it would violate the no-new-dependency constraint and duplicate existing capacity engine responsibilities.

## Decision: Validate With Existing Synthetic Profiles

**Decision**: Use normal, warning, critical, and mixed verification scenarios as the dashboard validation baseline.

**Rationale**: These profiles already represent the key operating states required by executive and technical dashboards. They allow repeatable validation without production data and prove that both risk-oriented and metric-oriented panels populate.

**Alternatives considered**:

- Manual validation with production-like data: rejected because it is less repeatable and can hide missing panel coverage.
- Create a large number of scenario-specific profiles: rejected because the existing four profiles cover the current acceptance criteria.

## Decision: Keep Grafana Provisioning as Repository Artifacts

**Decision**: Continue managing dashboards and datasources as repository-controlled provisioning files mounted into Grafana at startup.

**Rationale**: Repository-controlled dashboards are testable, reviewable, versioned, and compatible with the existing stack. They avoid manual UI drift and support repeatable deployment.

**Alternatives considered**:

- Manage dashboards manually through the Grafana UI: rejected because it is not repeatable or test-friendly.
- Add a dashboard generation tool: rejected because it adds unnecessary complexity and would likely require new dependencies.

## Decision: Empty-State Behavior Is Required at Panel Purpose Level

**Decision**: Empty-state handling is validated by panel purpose and expected query coverage rather than adding a separate runtime component.

**Rationale**: Grafana panels can display no-data states, but the important business requirement is that dashboard design distinguishes missing data from healthy zero-risk conditions. This can be validated by query coverage, panel titles, and quickstart scenarios.

**Alternatives considered**:

- Build a custom empty-state service: rejected because it is unnecessary for the current dashboard provisioning scope.
- Ignore empty states: rejected because users could mistake missing data for healthy conditions.
