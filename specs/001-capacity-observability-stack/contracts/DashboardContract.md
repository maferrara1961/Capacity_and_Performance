# Contract: Dashboard Views

## Purpose

Defines the required dashboard families, visible states, filters, and protected access behavior.

## Shared Contract

All dashboard views MUST:
- Require authenticated access.
- Support time range filtering.
- Show stale-data or failed-refresh state when capacity calculations are not current.
- Display OK, Warning, Critical, and Unknown states consistently.
- Reject malformed filters with deterministic validation messages.

## Executive Capacity Dashboard

**Audience**: Executives and operations leaders.

**Required Views**:
- Overall capacity state.
- Services with saturation risk.
- Forecast for 30, 60, and 90 days.
- Capacity used versus available.
- Top 10 risks.
- Recommended actions.

**Acceptance Contract**:
- A service with Critical risk appears above Warning and OK services.
- Forecast and days to saturation are visible for services with enough history.
- Services with insufficient history show Unknown forecast confidence, not misleading certainty.

## Technical Performance Dashboard

**Audience**: Platform and operations engineers.

**Required Views**:
- CPU, memory, disk, network, IOPS, latency, throughput, errors, and saturation.
- Average, peak, and p95 values.
- Threshold breaches.
- Platform and resource filters.

**Acceptance Contract**:
- A threshold breach is visually visible in the same view as the metric.
- Users can drill from service risk to affected resource dimensions.

## Capacity Planning Dashboard

**Audience**: Capacity planners and service owners.

**Required Views**:
- Historical trends.
- Monthly growth.
- Forecast 30/60/90 days.
- Estimated exhaustion date.
- Oversized resources.
- Undersized resources.
- Headroom available.
- Baseline comparison.

**Acceptance Contract**:
- Resources with positive growth and limited headroom show a saturation estimate.
- Resources with sustained low usage and high headroom appear as oversized candidates.

## Application Dashboard

**Audience**: Service and application owners.

**Required Views**:
- Application health.
- Associated infrastructure.
- SLA/SLO status.
- End-to-end performance.
- Critical dependencies.

**Acceptance Contract**:
- A degraded critical dependency affects the application risk state.
- The dashboard shows all mapped servers, databases, storage, network resources, and dependencies.
