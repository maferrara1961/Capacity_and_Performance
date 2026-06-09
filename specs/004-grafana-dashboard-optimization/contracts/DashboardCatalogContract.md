# Contract: Dashboard Catalog

## Purpose

Defines the expected dashboard catalog for optimized executive and technical Grafana views.

## Required Dashboard Categories

### Executive Capacity

**Audience**: Executive stakeholders and decision makers.

**Required Outcomes**:

- Overall capacity state is visible.
- Top capacity risks are visible.
- Forecast for 30, 60, and 90 days is visible.
- Used capacity and available headroom are visible.
- Recommended actions are visible and prioritized.

**Acceptance Contract**:

- The dashboard title clearly identifies executive capacity purpose.
- Panels prioritize business risk and action over raw metric lists.
- At least one panel shows risk status.
- At least one panel shows forecast windows.
- At least one panel shows recommendations.

### Technical Performance

**Audience**: Operations and platform engineers.

**Required Outcomes**:

- CPU, memory, storage, IOPS, network, latency, throughput, errors, and saturation are visible.
- Affected resource and metric context is visible.
- Warning and critical states can be traced to a service or resource.
- Top consumers and outliers can be identified.

**Acceptance Contract**:

- The dashboard title clearly identifies technical performance purpose.
- Required performance metric groups are represented.
- Metric panels include resource context.
- KPI or threshold panels show affected resources and severity.

### Capacity Planning

**Audience**: Capacity planners and service owners.

**Required Outcomes**:

- Monthly growth is visible.
- Headroom and baseline comparison are visible.
- Days to saturation is visible.
- Overprovisioned and underprovisioned resources are identifiable.

**Acceptance Contract**:

- The dashboard title clearly identifies planning purpose.
- Growth, headroom, forecast, and sizing signals are represented.
- Resource classification is visible.

### Application and Service

**Audience**: Service owners and operations teams.

**Required Outcomes**:

- Application health is visible.
- Associated infrastructure is visible.
- Critical dependencies are visible.
- End-to-end performance context is visible.

**Acceptance Contract**:

- Service or application context appears wherever risk or degraded performance is shown.
- Dependencies and infrastructure mappings are visible.

## Empty-State Contract

When no matching data exists, dashboards must not imply an OK state. The user must be able to tell that data is missing or outside the selected range.

## Protected Access Contract

Dashboard access remains a protected operational surface. Users must authenticate through the existing access mechanism before viewing protected dashboard content.
